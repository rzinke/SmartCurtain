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

# get number of stepper motor steps from one side of the curtain to the other (open vs closed)
def curtain_length(cursor):
	query = (	"SELECT `curtain_length` FROM `curtain_details` \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query)
	return cursor._rows[0][0]


def current_position(cursor):
	query = (	"SELECT `curtain_position` FROM `curtain_details` \
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


def events_for_previous_weeks(cursor):
	from datetime import datetime, timedelta
	oldest_desired_date = datetime.now() - timedelta(weeks=CLUSTER_SPAN)
	query = (	"SELECT `desired_position`, `time` FROM `future` \
				WHERE `time` > '%s' AND `time` < CURRENT_TIMESTAMP")
	cursor.execute(query % (str(oldest_desired_date)))
	return cursor._rows


# ———— GETTERS: NON-ACTIVATED EVENTS ————

def all_non_activated_events(cursor):
	query = (	"SELECT `event_key`, `desired_position` FROM `future` \
				WHERE `time` < CURRENT_TIMESTAMP \
				AND `activated` = FALSE \
				ORDER BY `time` DESC;")
	cursor.execute(query)
	return cursor._rows


def newest_non_activated_event(cursor):
	query = (	"SELECT `event_key`, `desired_position` FROM `future` \
				WHERE `time` < CURRENT_TIMESTAMP \
				AND `activated` = FALSE \
				ORDER BY `time` DESC LIMIT 1;")
	cursor.execute(query)
	return cursor._rows[0]


def oldest_non_activated_event(cursor):
	query = (	"SELECT `event_key`, `desired_position` FROM `future` \
				WHERE `time` < CURRENT_TIMESTAMP \
				AND `activated` = FALSE \
				ORDER BY `time` ASC LIMIT 1;")
	cursor.execute(query)
	return cursor._rows[0]


# —————————————————— SETTERS ——————————————————

def mark_event_as_activated(cnx, cursor, event_key):
	query = (	"UPDATE `future` SET `activated` = TRUE \
				WHERE `event_key` = '%d';")
	cursor.execute(query % (event_key))
	cnx.commit()


# assign the curtain's current position to `curtain_details`.`curtain_position` in DB
def new_position(cnx, cursor, position_in_steps):
	query = (	"UPDATE `curtain_details` SET `curtain_position` = '%d' \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query % (position_in_steps))
	cnx.commit()


def set_direction_switch(cnx, cursor, switch_value):
	query = (	"UPDATE `curtain_details` SET `direction` = '%d' \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query % (switch_value))
	cnx.commit() 


def set_total_steps(cnx, cursor, total_steps):
	query = (	"UPDATE `curtain_details` SET `curtain_length` = '%d' \
				WHERE `pseudo_key` = '1';")
	cursor.execute(query % (total_steps))
	cnx.commit() 


# ———————————————— CONNECTION —————————————————–

def start_connection():
	try:
		import mysql.connector
		cnx = mysql.connector.connect(	user=DB_USER, password=DB_PASSWD,
						                              host=DB_IP, port=DB_PORT,
						                              database=DB_NAME)
		return cnx
	except Exception as error:
		ErrorWriter.write_error("start_connection", str(error))
		return None
