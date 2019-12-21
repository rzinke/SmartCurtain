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

import RPi.GPIO as GPIO
from time import sleep

from Definitions import *
import ErrorWriter
import GPIOUtility


# send a pulse to motor, then check whether the curtain has reached fully open/close
def step_motor_to_location_or_to_end(opposing_stop_pin, steps_to_move):
	while 0 < steps_to_move:
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		steps_to_move -= 3
		if not GPIO.input(opposing_stop_pin): return steps_to_move  # check reached end of span

	return 0


# ——————————————— RUNNING FUNCTIONS ———————————————

# main activation function
def move_curtain(direction, steps_to_move, stop_pin):
	# run motor
	GPIOUtility.enable_motor()  # VERY NECESSARY: lets driver have control
	GPIO.output(DIRECTION_PIN, direction)
	end_count = step_motor_to_location_or_to_end(stop_pin, abs(steps_to_move))

	GPIOUtility.disable_motor()  # left without clean up to keep motor disabled
	return end_count  # return final number of steps not taken


def close_curtain(direction):
	# run motor
	GPIOUtility.enable_motor()  # VERY NECESSARY: lets driver have control
	GPIO.output(DIRECTION_PIN, direction)

	while True:
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		if not GPIO.input(CLOSED_STOP_PIN): break

	GPIOUtility.disable_motor()


def open_curtain(direction):
	# run motor
	GPIOUtility.enable_motor()  # VERY NECESSARY: lets driver have control
	GPIO.output(DIRECTION_PIN, direction)

	while True:
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, True)
		sleep(PULSE_WAIT)
		GPIO.output(PULSE_PIN, False)
		sleep(PULSE_WAIT)
		if not GPIO.input(OPEN_STOP_PIN): break

	GPIOUtility.disable_motor()
