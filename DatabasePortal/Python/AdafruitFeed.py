#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on ..
#
#	DESCRIPTION:
#	BUGS:
#	FUTURE:
#
###########################################################################


from Adafruit_IO import MQTTClient
from time import sleep, time
from threading import Thread

from Definitions import *
import DBFunctions
import ErrorWriter

# —————————————————— UTILITY ——————————————————–

def steps_to_take(cursor, event_position):
	total_steps = DBFunctions.curtain_length(cursor)
	event_position_steps = total_steps * event_position / 100
	return DBFunctions.current_position() - event_position_steps


# —————————————— ADAFRUIT CLIENT —————————————————

def connect_to_feeds(client):
	for feed in [OPEN_KEY, CLOSE_KEY]:
		client.subscribe(feed)


def disconnect(client):
	raise Exception("MQTTClient disconnected")


def feed_actions(client, feed_id, payload):
	from datetime import datetime

	cnx, cursor = DBFunctions.connect_to_DB()

	try: curtain = int(payload)
	except: return
	if feed_id == OPEN_KEY:
		DBFunctions.full_open_immediate_event(cnx, cursor, curtain)
	elif feed_id == CLOSE_KEY:
		DBFunctions.close_immediate_event(cnx, cursor, curtain)

	cnx.close()


def active_feed(client):
	client.connect()
	client.loop_blocking()


def feed_loop(client):
	while True:
		cnx, cursor = DBFunctions.connect_to_DB()

		for curtain in DBFunctions.curtain_ids(cursor):
			feed_option_is_selected =  DBFunctions.adafruit_feed(cursor, curtain) 
			if feed_option_is_selected and not client.is_connected():
				thread = Thread(target=activate_feed, args=(client,))
				thread.start()
				thread.join()
			elif not feed_option_is_selected and client.is_connected():
				client.disconnect()

		cnx.close()
		sleep(FEED_CLIENT_CHECK_LOOP)


def start_client_loop():
	client = MQTTClient(USER_FEED_NAME, USER_FEED_KEY)

	client.on_connect = connect_to_feeds
	client.on_disconnect = disconnect
	client.on_message = feed_actions

	feed_loop(client)
