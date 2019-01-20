#!/usr/bin/env python3
__author__ = "MPZinke"

###################################################
#
#	-Service that loops to activate curtains after 
#	 a scheduled event has passed
#	-Creates future events based on passed events
#
###################################################

from datetime import datetime, timedelta
import numpy as np
from sklearn.cluster import KMeans
from db_functions import get_events_for_day_of_week, get_passed_future_events, set_future_event, start_connection
from time import sleep


""" object for each centiod """
class Centoid:
	def __init__(self, start_center, possessed_times):
		self.center = start_center
		self.avg = start_center  # used to record average of most common
		self.possessed_times = possessed_times
		self.valid_logs = []
		self.is_valid = self.check_validity() # is either average of usable points or False


	""" check if three or more points are within eachother
		 if they are, returns the average of points """
	def check_validity(self):
		while True:
			surrounding_times = [time for time in self.possessed_times if((self.avg-.5) < time < (self.avg+.5))]
			avg_of_surroundings = sum(surrounding_times) / len(surrounding_times)
			if avg_of_surroundings == self.avg: break
			self.avg = avg_of_surroundings
		if len(surrounding_times) > 2: return True
		return False



def get_possible_centoid_count(events):
	number_of_days = len({(time.day,time.month,time.year) for (time) in events})
	number_of_events = events.rowcount
	try: return int(number_of_events / number_of_days)  # 0/0=0 does not work
	except: return None


def convert_time_to_decimal_value_of_day(events):
	return [round(time.hour + time.minute / 60, 3) for (time) in events]


def convert_decimal_value_of_day_to_time(times):
	return [':'.join([format(int(time), "02"), str((time-int(time))*60)[:2], "00"]) for time in times]


def covert_time_datetime(day, times):
	return [datetime.strptime(day.date().strftime("%Y-%m-%d ")+time, '%Y-%m-%d %H:%M:%S') for time in times]


def create_centoids(decimal_times, k_value):
	centoids = []
	times = np.array(decimal_times)
	centers = KMeans(n_clusters=k_value, random_state=0)
	try: centers.fit(times.reshape(-1,1))
	except: return
	for i in range(centers.n_clusters):
		combined = times[np.where(centers.labels_ == i)]
		centoids.append(Centoid(float(centers.cluster_centers_[i]), combined))
	return centoids



def schedule_future_events(cnx, furthest_calculated_day):
	# get up through the next 7 days
	for x in range((furthest_calculated_day - datetime.now()).days+2, 8):
		for state in ['C', 'O']:
			day = (datetime.now() + timedelta(days=x))  # formated to mysql (Monday:1, Tuesday:2,...Sunday:7)
			successful_query_data = get_events_for_day_of_week(cnx, day.weekday(), state)

			# now the math starts
			if not successful_query_data or not successful_query_data: continue
			decimal_times = convert_time_to_decimal_value_of_day(successful_query_data)
			k_value = get_possible_centoid_count(successful_query_data)
			centoids = create_centoids(decimal_times, k_value)
			centoid_avgs = [centoid.avg for centoid in centoids]
			future_times = convert_decimal_value_of_day_to_time(centoid_avgs)
			future_events = covert_time_datetime(day, future_times)
			
			for event in future_events:
				set_future_event(cnx, state, time)

		furthest_calculated_day = datetime.now() + timedelta(days=x)
	return furthest_calculated_day


def main():
	furthest_calculated_day = datetime.now()
	while(True):
		cnx = start_connection("localhost")
		if cnx == False: print("Could not connect")
		else:
			print(datetime.now())
			# option to turn off self calculating events
			if True: furthest_calculated_day = schedule_future_events(cnx, furthest_calculated_day)
			future_events = get_passed_future_events(cnx.cursor())
			for (event_key, event_action, event_time) in future_events:
				print(initiate(cnx, event_action) or "Failed to initiate")
				print(remove_future_event(cnx, event_key) or "Failed to delete")
			cnx.close()
		sleep(30)

if __name__ == '__main__':
	main()


""" created by: MPZinke on 01.14.18 """