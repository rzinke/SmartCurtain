#!/usr/bin/env python3
__author__ = "MPZinke"

###################################################
#
#	-Function page for futures.py & feed.py to 
#	 activate curtain motor
#
###################################################

import mysql.connector
from db_functions import *
from time import sleep


# check if motor should be used; set DB entries
def initiate(cnx, cursor, new_state):
	if already_desired_state(cursor, state): return "Desired state already acheived"
	elif not set_state(cnx, cursor, 'W'): return "Could not set operational state"

	motor_control(state == 'C')  # false for open, true for close; change to 'O' to reverse direction

	if not set_state(cnx, cursor, new_state): return "Could not set state"
	elif not log_event(cnx, cursor, state): return "Could not log event"

	return False  # no errors


def motor_control(direction):
	distance = float("###DISTANCE") #CUSTOMIZE: travel distance in inches
	travel_units = int(distance * 3200 * .3225)

	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)

	control_pins = [7,11,13]  # Direction, Pulse, Enable
	for pin in control_pins:
		GPIO.setup(pin, GPIO.OUT)

	GPIO.output(13, False)  # Very necessary
	GPIO.output(7, direction)

	for i in range(travel_units):
		GPIO.output(11, True)
		sleep(.0000001)
		GPIO.output(11, False)
		sleep(.0000001)
	GPIO.output(13, True)  # left without clean up to keep motor disabled



def already_desired_state(cursor, desired_state):
	state = db_functions.curtain_state(cursor)
	if state is not 'W': return state == desired_state

	sleep(10)  # give pi time to finish process if other script is using motor
	return already_desired_state(cursor, desired_state)  # recheck 



def main():
	if not intiate_curtains('O'): print("Failed")
	else: print("Success")


if __name__ == "__main__":
	main()

""" created by: MPZinke on 01.09.19
	edited on: 7.7.19 to fix double activation bug """