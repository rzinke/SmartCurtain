#!/usr/bin/env python3
__author__ = "MPZinke"

###################################################
#
#	-Function page for futures.py & feed.py to 
#	 activate curtain motor
#
###################################################

import mysql.connector
import db_functions
from time import sleep


def initiate(cnx, state):
	success = True
	if desired_state_already_achieved(cnx, state) or not db_functions.set_state(cnx, 'W'): return not success
	motor_control(state == 'C')  # false for open, true for close
	if not db_functions.set_state(cnx, state) or not db_functions.log_event(cnx, state): success = False
	if not success:
		db_functions.error_report(cnx, state)
		return False
	return "Curtains successfully changed"


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



def desired_state_already_achieved(cnx, desired_state):
	state = db_functions.get_state(cnx.cursor())
	if state == 'W':
		sleep(10)
		return desired_state_already_achieved(cnx, state)
	else: return state == desired_state



def main():
	if not intiate_curtains('O'): print("Failed")
	else: print("Success")

if __name__ == "__main__":
	main()

""" created by: MPZinke on 01.09.18 """