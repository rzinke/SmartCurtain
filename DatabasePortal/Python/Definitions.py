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

# ——————————————— PROGRAM SWITCHES ———————————————
PREDICT_EVENTS = False
AUTO_CALIBRATE_IF_CURTAIN_STOPPED = True


# ——————————————————— TIME ———————————————————

DATETIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"
CLUSTER_SPAN = 4  # number of weeks looked back on to determine applicable logs


# ————————————————— ERROR LOG —————————————————

DELIMITER = '|'  # how values are sepparated in logs
ERROR_FILE_NAME = "ErrorLog.txt"


# —————————————————— RPI.GPIO ——————————————————

DIRECTION_PIN = 7
PULSE_PIN = 11
ENABLE_PIN = 13

OPEN_STOP_PIN = 16
CLOSED_STOP_PIN = 18

PULSE_WAIT = .0000001


# ————————————————— DATABASE ——————————————————

DB_NAME = "curtain"
DB_USER = "python_db_user"
DB_PASSWD = ""
DB_IP = "localhost"
DB_PORT = 3306


# —————————————————— OTHER ———————————————————

STOPPED_PERCENT_LENIENCY = 5  # percentage of remaining steps before 
