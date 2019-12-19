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


#SUGAR: for disabling motor (so that it be manually slid) and return whether it is at the end
def disable_motor():
	GPIO.output(ENABLE_PIN, True)  # left without clean up to keep motor disabled


# general GPIO & pin setup
def setup_GPIO():
	GPIO.setwarnings(False)  # ignore any important warnings
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)

	motor_pins = [DIRECTION_PIN, PULSE_PIN, ENABLE_PIN]
	for pin in motor_pins:
		GPIO.setup(pin, GPIO.OUT)

	stop_pins = [OPEN_STOP_PIN, CLOSED_STOP_PIN]
	for pin in stop_pins:
		GPIO.setup(pin, GPIO.IN)


# send a pulse to motor, then check whether the curtain has reached fully open/close
def step_motor_to_steps_or_to_end(opposing_stop_pin, steps_to_move):
	while 0 < steps_to_move:
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, True)
		sleep(.0000001)
		GPIO.output(PULSE_PIN, False)
		sleep(.0000001)
		steps_to_move -= 3
		if GPIO.input(opposing_stop_pin): return steps_to_move  # check reached end of span

	return 0
		


# main activation function
def move_curtain(direction, steps_to_move, stop_pin):
	# position is approaching 0 (closed) if negative steps; else increasing position (open)
	stop_pin = CLOSED_STOP_PIN if steps_to_move < 0 else OPEN_STOP_PIN

	import RPi.GPIO as GPIO
	setup_GPIO()

	# run motor
	GPIO.output(ENABLE_PIN, False)  # VERY NECESSARY: lets driver have control
	GPIO.output(DIRECTION_PIN, direction)
	end_count = step_motor_to_steps_or_to_end(stop_pin, abs(steps_to_move))

	disable_motor()
	return end_count  # return final number of steps not taken
