#!/usr/bin/env python3
__author__ = "MPZinke"

###################################################
#
#	-Used with futures.py, init.py & feed.py to 
#	 connect to db `curtain` as part of created
#	 service Future & AIO
#
###################################################


def all_future_events(cursor):
	try:
		query = ("SELECT * FROM `future`;")
		cursor.execute(query)
		return cursor
	except: return False


def current_state(cursor):
	try:
		query = ("SELECT `state` FROM `state`;")
		cursor.execute(query)
		return cursor._rows[0][0]
	except: return False


def error_report(cnx, cursor, error, state):
	#TODO: add error message column to DB
	try:
		query = ("INSERT INTO `error` (`starting_state`, `time`) VALUES ('%s', CURRENT_TIMESTAMP());")
		cursor.execute(query % (state))
		cnx.commit()
		return True
	except: return False


def events_for_day_of_week(cursor, day_of_week, event):
	try:
		four_weeks_ago = datetime.now() - timedelta(weeks=4)
		query = "SELECT `time` FROM `log` WHERE `time` >= '%s' AND `finish_state` = '%s' AND DAYOFWEEK(`time`) = '%s';"
		cursor.execute(query % (four_weeks_ago, event, day_of_week))
		return [time[0] for (time) in cursor]
	except: return None


def log_event(cnx, cursor, state):
	try:
		query = ("INSERT INTO `log` (`finish_state`, `time`) VALUES ('%s', CURRENT_TIMESTAMP());")
		cursor.execute(query % (state))
		cnx.commit()
		return True
	except: return False


def passed_future_events(cursor):
	try:
		query = ("SELECT * FROM `future` WHERE `event_time` <= CURRENT_TIMESTAMP();")
		cursor.execute(query)
		return cursor
	except: return False


def remove_future_event(cnx, cursor, event_key):
	try:
		query = ("DELETE FROM `future` WHERE `event_key` = '%d';")
		cursor.execute(query % (event_key))
		cnx.commit()
		return True
	except: return False


def set_future_event(cnx, cursor, state, time):
	try:
		query = ("INSERT INTO `future` (`event_action`, `event_time`) VALUES ('%s', '%s');")
		cursor.execute(query % (state, time))
		cnx.commit()
		return True
	except: return False


def set_state(cnx, cursor, state):
	try:
		query = ("UPDATE `state` SET `state` = '%s' WHERE `state_key` = 1;")
		cursor.execute(query % (state))
		cnx.commit()
		return True
	except: return False


def start_connection(ip):
	try:
		import mysql.connector
		cnx = mysql.connector.connect(user='pi', password='',
		                              host=ip, port=3306,
		                              database='curtain')
		return cnx
	except: return False



""" created by: MPZinke on 01.09.18 """