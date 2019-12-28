#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on ..
#
#	DESCRIPTION: Function library to pull from curtain.sql to get/set values & events.
#						`curtain_details` table should contain 1 entry for storing primary curtain
#						data.
#	BUGS:
#	FUTURE:
#
###########################################################################

from Definitions import *
import ErrorWriter


# —————————————————— GETTERS ——————————————————

def current_position(cursor):
	query = (	"SELECT `curtain_position` FROM `curtain_details` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


# get number of stepper motor steps from one side of the curtain to the other (open vs closed)
def curtain_length(cursor):
	query = (	"SELECT `curtain_length` FROM `curtain_details` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


# bool for if the curtain's desired position is current catalogued position 
def desire_position_does_not_equal_current(cursor, desired):
	query = (	"SELECT `curtain_position`FROM `curtain_details` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	current = cursor._rows[0][0]
	if not current: return 5 < desired
	return 5 < (abs(current - desired) / current)


def direction(cursor):
	query = (	"SELECT `direction` FROM `curtain_details` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


# BOOL/INT: check for practical purposes if an event (same position) is already set
def event_set_at_approximate_time(cursor, event, time):
	from datetime import timedelta
	time_lower_bound = time - timedelta(seconds=SAME_EVENT_TIME_DIFFERENCE)
	time_upper_bound = time + timedelta(seconds=SAME_EVENT_TIME_DIFFERENCE)
	query = (	"SELECT * FROM `events` \
				WHERE `time` > '%s' AND `time` < '%s' \
				AND `desired_position` = '%d';")
	cursor.execute(query % (	time_lower_bound,
								time_upper_bound,
								event))
	return cursor.rowcount


# —————————————————— OPTIONS ——————————————————

def adafruit_feed(cursor):
	query = (	"SELECT `adafruit_feed` FROM `options` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


def event_prediction(cursor):
	query = (	"SELECT `event_prediction` FROM `options` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


def sunrise_open(cursor):
	query = (	"SELECT `sunrise_open` FROM `options` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


def sunset_close(cursor):
	query = (	"SELECT `sunset_close` FROM `options` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


# —————————————————— EVENTS ——————————————————

def all_non_activated_events(cursor):
	query = (	"SELECT `event_key`, `desired_position` FROM `events` \
				WHERE `time` < CURRENT_TIMESTAMP \
				AND `activated` = FALSE \
				ORDER BY `time` DESC;")
	cursor.execute(query)
	return cursor._rows


def events_for_previous_weeks(cursor):
	from datetime import datetime, timedelta
	oldest_desired_date = datetime.now() - timedelta(weeks=CLUSTER_SPAN)
	query = (	"SELECT `desired_position`, `time` FROM `events` \
				WHERE `time` > '%s' AND `time` < CURRENT_TIMESTAMP")
	cursor.execute(query % (str(oldest_desired_date)))
	return cursor._rows


def newest_non_activated_event(cursor):
	query = (	"SELECT `event_key`, `desired_position` FROM `events` \
				WHERE `time` < CURRENT_TIMESTAMP \
				AND `activated` = FALSE \
				ORDER BY `time` DESC LIMIT 1;")
	cursor.execute(query)
	return cursor._rows[0]


def oldest_non_activated_event(cursor):
	query = (	"SELECT `event_key`, `desired_position` FROM `events` \
				WHERE `time` < CURRENT_TIMESTAMP \
				AND `activated` = FALSE \
				ORDER BY `time` ASC LIMIT 1;")
	cursor.execute(query)
	return cursor._rows[0]


# —————————————————— SETTERS ——————————————————

# move to DBFunctions.py
def add_event(cnx, cursor, desired_position, time):
	query = (	"INSERT INTO `events` \
				(`desired_position`, `activated`, `time`) VALUES \
				('%d', FALSE, '%s');")
	cursor.execute(query % (desired_position, time.strftime(DATETIME_STRING_FORMAT)))
	return cnx.commit()


def mark_event_as_activated(cnx, cursor, event_key):
	query = (	"UPDATE `events` SET `activated` = TRUE \
				WHERE `event_key` = '%d';")
	cursor.execute(query % (event_key))
	return cnx.commit()


# assign the curtain's current position to `curtain_details`.`curtain_position` in DB
def new_position(cnx, cursor, position_in_steps):
	query = (	"UPDATE `curtain_details` SET `curtain_position` = '%d' \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query % (position_in_steps))
	return cnx.commit()


def set_curtain_length(cnx, cursor, total_steps):
	query = (	"UPDATE `curtain_details` SET `curtain_length` = '%d' \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query % (total_steps))
	return cnx.commit() 


def set_direction_switch(cnx, cursor, switch_value):
	query = (	"UPDATE `curtain_details` SET `direction` = '%d' \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query % (switch_value))
	return cnx.commit() 


def write_curtain_error(cnx, cursor, current, desired, error, module=None):
	if not module:
		import traceback
		module = traceback.format_exc().split("\n")[-4].strip()

	# change delimiter if exists
	error_message = str(error).replace(DELIMITER, ',' if ',' is not DELIMITER else ' ')
	query = (	"INSERT INTO `error_log` \
				(`curtain_position`, `desired_position`, `error`, `path`) VALUES \
				('%d', '%d', '%s', '%s');")
	cursor.execute(query % (current, desired, error, module))
	return cnx.commit()


# ———————————————— CONNECTION —————————————————
# ————————————————————————————————————————

def start_connection():
	try:
		import mysql.connector
		cnx = mysql.connector.connect(	user=DB_USER, password=DB_PASSWD,
						                              host=DB_IP, port=DB_PORT,
						                              database=DB_NAME)
		return cnx
	except Exception as error:
		ErrorWriter.write_error(error)
		return None


def connect_to_DB():
	cnx = start_connection()
	while is_null_sleep_then(cnx):
		cnx = start_connection()  # connect
	cursor = cnx.cursor(buffered=True)
	return cnx, cursor