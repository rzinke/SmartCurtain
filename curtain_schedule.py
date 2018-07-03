#! /usr/bin/env python3

#curtain_schedule

import calendar
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.cluster import KMeans
import initiate_curtain
from time import sleep, time



class DaysOfWeek:
	def __init__(self, day):
		self.day = day
		self.centoids = []
		self.k_value = 0
		self.times = []  # created externally and holds ///Events


	def set_k_value(self):
		total_days = []
		for i in range(len(self.times)):
			if self.times[i].log.date() not in total_days:
				total_days.append(self.times[i].log.date())
		try: self.k_value = int(round(len(self.times) / len(total_days)))
		except: pass


	def calculate_centoids(self):
		time_array = []
		for time in self.times:  # for 4 week, edit to four_week_logs
			time_array.append([time.decimal])
		time_array = np.array(time_array)
		centers = KMeans(n_clusters=self.k_value)
		try: centers.fit(time_array)
		except: return
		for i in range(centers.n_clusters):
			combined = []
			temp = time_array[np.where(centers.labels_ == i)]
			for sub_list in temp:
				combined.append(sub_list[0])
			self.centoids.append(Centoid(float(centers.cluster_centers_[i]), combined))



""" class for events to store data """
class Event:
	def __init__(self, log):
		self.log = log
		self.decimal = round(self.log.hour + self.log.minute / 60, 3)




class Centoid:
	def __init__(self, start_center, possessed_times):
		self.center = start_center
		self.possessed_times = possessed_times
		self.valid_logs = []
		self.is_valid = self.check_validity() # is either average of usable points or False


	""" check if three or more points are within eachother
		 if they are, returns the average of points """
	def check_validity(self):
		self.possessed_times.sort()
		time_group = []
		for i in range(len(self.possessed_times)-2):
			if self.possessed_times[i] + 1 >= self.possessed_times[i+2]:
				time_group.extend(self.possessed_times[i:i+2])
				for j in range(i+2, len(self.possessed_times)):
					if self.possessed_times[j] <= self.possessed_times[i] + 1: time_group.append(self.possessed_times[j])
			if time_group: return sum(time_group) / len(time_group)
		return False




"""----------------for main----------------"""

def open_log(file_name):
	file_in = open(file_name, "r")
	return file_in



def create_objects():
	groups = {"open": [], "close" : []}
	for group in groups:
		for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
			groups[group].append(DaysOfWeek(i))
	return groups



def write_times(objects, file):
	schedule = file.readlines()
	file.close()

	to_be_rewritten = ""
	for line in schedule:
		log = datetime.strptime(line[:16], "%Y-%m-%d %H:%M")
		if not log_is_relevent(log, 7):
			continue
		to_be_rewritten += line
		day_of_week = calendar.day_name[log.weekday()]
		for i in range(len(objects[line[28:].rstrip('\n')])):
			if objects[line[28:].rstrip('\n')][i].day == day_of_week:
				if log_is_relevent(log, 4): objects[line[28:].rstrip('\n')][i].times.append(Event(log))
	# to store files that are longer than 4 weeks, change /weeks_int or delete if statement
	new = open("log.txt", "w")  #TODO change file name to override used file
	new.write(to_be_rewritten.rstrip("\n"))
	new.close()



"""-----------------utility----------------"""

# if the log is within weeks_int
def log_is_relevent(log, weeks_int):
	elapsed = datetime.today() - timedelta(weeks=weeks_int)
	if elapsed < log: return True
	return False


def date_of_next_day(day):
	today = datetime.today()
	while calendar.day_name[today.weekday()] != day:
		today += timedelta(days=1)
	return today


def to_horological(date, decimal):
	minute = str(int((decimal - int(decimal)) * 60))
	minute = datetime.strptime(str(int(decimal)) + ":" + minute, "%H:%M")
	return datetime.combine(date, minute.time())



"""------------------main------------------"""

# I don't like how much power this one holds
def scheduler():
	file = open_log("./text_files/log.txt")
	groups = create_objects()
	write_times(groups, file)
	write_out = open("./text_files/future_events.txt", "w")
	to_be_written = ""
	for state in groups:
		for dow in range(len(groups[state])):
			groups[state][dow].set_k_value()
			groups[state][dow].calculate_centoids()
			for centoid in groups[state][dow].centoids:
				date = date_of_next_day(groups[state][dow].day).date()
				if centoid.is_valid and to_horological(date, centoid.is_valid) > datetime.now():
					# print(groups[state][dow].day, centoid.center)
					if to_be_written: to_be_written += "\n"
					to_be_written += str(to_horological(date, centoid.is_valid)) + " " * 7 + "; " + state
	write_out.write(to_be_written)
	write_out.close()
	


#TODO add part that forces it closed at another time (protocols for bad calculations)

def main():
	scheduler()
	last_calculation = datetime.now()
	while True:
		if last_calculation.date() != datetime.now().date():
			scheduler()
			last_calculation = datetime.now()

		upcoming_events = open("./text_files/future_events.txt", "r")
		events = upcoming_events.readlines()
		upcoming_events.close()

		if any(datetime.strptime(event[:16], "%Y-%m-%d %H:%M") < datetime.now() for event in events):
			future_events = ""
			for event in events:
				if datetime.strptime(event[:16], "%Y-%m-%d %H:%M") < datetime.now():
					state = initiate_curtain.curtain_is_open()
					if "close" in event and state:
						initiate_curtain.close_window()
					elif "open" in event and not state:
						initiate_curtain.open_window()

				else: future_events += event
			
			rewrite_future = open("./text_files/future_events.txt", "w")
			rewrite_future.write(future_events.rstrip("\n"))
			rewrite_future.close()

		print("Executed")
		sleep(300)




if __name__ == "__main__":
	main()


"""created by: MPZinke 06.28.18"""