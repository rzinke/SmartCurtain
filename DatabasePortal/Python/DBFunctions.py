#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on ..
#
#	DESCRIPTION: Function library to pull from curtain.sql to get/set values & events.
#						`curtains` table should contain 1 entry for storing primary curtain
#						data.
#	BUGS:
#	FUTURE:
#
###########################################################################

from Definitions import *
import ErrorWriter


# —————————————————— GETTERS ——————————————————

def current_position(cursor, curtain):
	query = (	"SELECT `curtain_position` FROM `curtains` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


def curtain_ids(cursor):
	query = (	"SELECT `curtain_id` FROM `curtains`;")
	cursor.execute(query)
	return [curtain[0] for curtain in cursor._rows]	


# get number of stepper motor steps from one side of the curtain to the other (open vs closed)
def curtain_length(cursor, curtain):
	query = (	"SELECT `curtain_length` FROM `curtains` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


# bool for if the curtain's desired position is current catalogued position 
def desire_position_does_not_equal_current(cursor, curtain, desired):
	query = (	"SELECT `curtain_position` FROM `curtains` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	current = cursor._rows[0][0]
	if not current: return 5 < desired
	return 5 < (abs(current - desired) / current)


def direction(cursor, curtain):
	query = (	"SELECT `curtain_direction` FROM `curtains` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


# BOOL/INT: check for practical purposes if an event (same position) is already set
def event_set_at_approximate_time(cursor, curtain, event, time):
	from datetime import timedelta
	time_lower_bound = time - timedelta(seconds=SAME_EVENT_TIME_DIFFERENCE)
	time_upper_bound = time + timedelta(seconds=SAME_EVENT_TIME_DIFFERENCE)
	query = (	"SELECT * FROM `events` \
				WHERE `event_time` > '%s' AND `event_time` < '%s' \
				AND `event_position` = '%d' \
				AND `curtain_id` = '%d';")
	cursor.execute(query % (	time_lower_bound, time_upper_bound,
								event, curtain))
	return cursor.rowcount


# —————————————————— OPTIONS ——————————————————

def adafruit_feed(cursor, curtain):
	query = (	"SELECT `adafruit_feed` FROM `options` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


def auto_calibration(cursor, curtain):
	query = (	"SELECT `auto_calibration` FROM `options` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


def event_predictor(cursor, curtain):
	query = (	"SELECT `event_predictor` FROM `options` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


def sunrise_open(cursor, curtain):
	query = (	"SELECT `sunrise_open` FROM `options` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


def sunset_close(cursor, curtain):
	query = (	"SELECT `sunset_close` FROM `options` \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (curtain))
	return cursor._rows[0][0]


# —————————————————— EVENTS ——————————————————

def all_non_activated_events(cursor):
	query = (	"SELECT `event_id`, `event_position` FROM `events` \
				WHERE `event_time` < CURRENT_TIMESTAMP \
				AND `event_activated` = FALSE \
				ORDER BY `event_time` DESC;")
	cursor.execute(query)
	return cursor._rows


def events_for_previous_weeks(cursor, curtain):
	from datetime import datetime, timedelta
	oldest_desired_date = datetime.now() - timedelta(weeks=CLUSTER_SPAN)
	query = (	"SELECT `event_position`, `event_time` FROM `events` \
				WHERE `event_time` > '%s' AND `event_time` < CURRENT_TIMESTAMP \
				AND `curtain_id` = '%d';")
	cursor.execute(query % (str(oldest_desired_date), curtain))
	return cursor._rows


def newest_non_activated_event(cursor):
	query = (	"SELECT `event_id`, `event_position` FROM `events` \
				WHERE `event_time` < CURRENT_TIMESTAMP \
				AND `event_activated` = FALSE \
				ORDER BY `event_time` DESC LIMIT 1;")
	cursor.execute(query % (curtain))
	return cursor._rows[0]


def oldest_non_activated_event(cursor, curtain):
	query = (	"SELECT `event_id`, `event_position` FROM `events` \
				WHERE `event_time` < CURRENT_TIMESTAMP \
				AND `event_activated` = FALSE \
				AND `curtain_id` = '%d' \
				ORDER BY `event_time` ASC LIMIT 1;")
	cursor.execute(query % (curtain))
	return cursor._rows[0]


# —————————————————— SETTERS ——————————————————

# move to DBFunctions.py
def add_event(cnx, cursor, curtain, event_position, time):
	query = (	"INSERT INTO `events` \
				(`curtain_id`, `event_position`, `event_activated`, `event_time`) VALUES \
				('%d', '%d', FALSE, '%s');")
	cursor.execute(query % (	curtain, event_position,
								time.strftime(DATETIME_STRING_FORMAT)))
	return cnx.commit()


def close_immediate_event(cnx, cursor, curtain):
	query = (	"INSERT INTO `events` \
				(`curtain_id`, `event_position`, `event_activated`) VALUES \
				('%d', '%d', FALSE);")
	cursor.execute(query % (curtain, 0))
	return cnx.commit()


def full_open_immediate_event(cnx, cursor, curtain):
	length = curtain_length(cursor)

	query = (	"INSERT INTO `events` \
				(`curtain_id`, `event_position`, `event_activated`) VALUES \
				('%d', '%d', FALSE);")
	cursor.execute(query % (curtain, length))
	return cnx.commit()


def mark_event_as_activated(cnx, cursor, event_key):
	query = (	"UPDATE `events` SET `event_activated` = TRUE \
				WHERE `event_id` = '%d';")
	cursor.execute(query % (event_key))
	return cnx.commit()


# assign the curtain's current position to `curtains`.`curtain_position` in DB
def new_position(cnx, cursor, position_in_steps):
	query = (	"UPDATE `curtains` SET `curtain_position` = '%d' \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (position_in_steps))
	return cnx.commit()


def set_current_position(cnx, cursor, position):
	query = (	"UPDATE `curtains` SET `curtain_position` = '%d' \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (position))
	return cnx.commit() 


def set_curtain_length(cnx, cursor, total_steps):
	query = (	"UPDATE `curtains` SET `curtain_length` = '%d' \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (total_steps))
	return cnx.commit() 


def set_direction_switch(cnx, cursor, switch_value):
	query = (	"UPDATE `curtains` SET `curtain_direction` = '%d' \
				WHERE `curtain_id` = '%d';")
	cursor.execute(query % (switch_value))
	return cnx.commit() 


def write_curtain_error(cnx, cursor, current, desired, error, module=None):
	if not module:
		import traceback
		module = traceback.format_exc().split("\n")[-4].strip()

	# change delimiter if exists
	error_message = str(error).replace(DELIMITER, ',' if ',' is not DELIMITER else ' ')
	query = (	"INSERT INTO `error_log` \
				(`curtain_position`, `event_position`, `error`, `path`) VALUES \
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