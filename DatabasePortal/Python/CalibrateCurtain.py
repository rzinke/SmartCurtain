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

from Definitions import *
import ErrorWriter

# —————————————————— UTILITY ——————————————————

#SUGAR: for disabling motor (so that it be manually slid) and return whether it is at the end
def disable_motor():
	GPIO.output(ENABLE_PIN, True)  # left without clean up to keep motor disabled


# general GPIO & pin setup
def setup_GPIO():
	GPIO.setwarnings(False)
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)

	motor_pins = [DIRECTION_PIN, PULSE_PIN, ENABLE_PIN]  # direction, pulse, enable
	for pin in motor_pins:
		GPIO.setup(pin, GPIO.OUT)

	stop_pins = [OPEN_STOP_PIN, CLOSED_STOP_PIN]
	for pin in stop_pins:
		GPIO.setup(pin, GPIO.IN)


# ——————————————— KNOWN DIRECTION ————————————————

def count_steps_from_closed_to_open():
	count = 0
	while True:
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		count += 1
		if GPIO.input(OPEN_STOP_PIN): return count


def move_to_closed(closed_direction):
	GPIO.output(DIRECTION_PIN, closed_direction)

	while True:
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		if GPIO.input(CLOSED_STOP_PIN): return
		elif GPIO.input(OPEN_STOP_PIN): raise Exception("Direction is not properly set")



# strictly for distance calibration (NOT FOR DIRECTION WHICH MUST BE PRESET)
def calibrate(cnx, cursor):
	try:
		import RPi.GPIO as GPIO
		from DBFunctions import direction, set_total_steps

		setup_GPIO()

		closed_direction = direction(cursor)
		move_to_closed(closed_direction)
		step_count = count_steps_from_closed_to_open()
		set_total_steps(cnx, cursor, step_count)  # write count to DB
	except Exception as error:
		ErrorWriter.write_error("CalibrateCurtain.calibrate", str(error))


# ——————————————— UNKNOW DIRECTION ———————————————

def count_steps_to_end(opposite_pin):
	GPIO.output(DIRECTION_PIN, False)

	count = 0
	while True:
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		count += 1
		if GPIO.input(OPEN_STOP_PIN): return count


def move_to_an_end():
	GPIO.output(DIRECTION_PIN, True)

	while True:
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		if GPIO.input(CLOSED_STOP_PIN): return CLOSED_STOP_PIN
		elif GPIO.input(OPEN_STOP_PIN): return OPEN_STOP_PIN



def setup():
	import RPi.GPIO as GPIO
	from DBFunctions import set_direction_switch, set_total_steps

	setup_GPIO()

	if GPIO.input(OPEN_STOP_PIN) or GPIO.input(CLOSED_STOP_PIN):
		raise Exception("To determine direction, curtain cannot be at an end")

	# move to end and orient
	first_stop_pin = move_to_an_end()
	# True (pin) & going "negative" (CLOSED_STOP_PIN) is `direction` = False
	# True (pin) & going "positive" (OPEN_STOP_PIN) is `direction` = True
	closed_direction = False if first_stop_pin == CLOSED_STOP_PIN else True
	set_direction_switch(cnx, cursor, closed_direction)  # write direction to DB

	# get number of steps
	if OPEN_STOP_PIN == first_stop_pin: opposite_pin = CLOSED_STOP_PIN 
	else: opposite_pin = OPEN_STOP_PIN
	step_count = count_steps_to_end(opposite_pin)
	set_total_steps(cnx, cursor, step_count)  # write count to DB
