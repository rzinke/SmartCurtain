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

from time import sleep

from Definitions import *

import CalibrateCurtain
import DBFunctions
import ErrorWriter
import SetCurtain


# —————————————————— UTILITY ——————————————————–

def curtain_final_position(remaining_steps, stop_pin, total_steps):
	if not remaining_steps: return new_position_steps  # success
	return total_steps if stop_pin == OPEN_STOP_PIN else 0


#SUGAR: used in if statements: check if value null; if null, sleep; return truthiness
def is_null_sleep_then(evalutated_value, sleep_amount=5):
	if not evalutated_value: sleep(sleep_amount)
	return not bool(evalutated_value)


def needed_steps(cursor, new_percentage_position, total_steps):
	current_step_position = DBFunctions.current_position(cursor)
	new_position_steps = int(new_percentage_position * total_steps / 100)
	return new_position_steps - current_step_position



# ——————————————— PRIMARY PROCESSES ———————————————

# check DB to orient the motor direction, calculate steps & move curtain
def activate_curtain(cnx, cursor, new_percentage_position):
	print("Main::activate_curtain()", end=" ")
	print(new_percentage_position)
	total_steps = DBFunctions.curtain_length(cursor)
	# check if curtain length not set up
	if not total_steps: CalibrateCurtain.calibrate(cnx, cursor)

	# calculate steps needed to take from current position to desired
	steps_to_move = needed_steps(cursor, new_percentage_position, total_steps)

	# move curtain to position: direction based on DB switch
	direction = (steps_to_move < 0) ^ DBFunctions.direction(cursor)
	# pin of stop switch, into which curtain can run
	stop_pin = CLOSED_STOP_PIN if steps_to_move < 0 else OPEN_STOP_PIN
	remaining_steps = SetCurtain.move_curtain(direction, steps_to_move, stop_pin)

	final_position = curtain_final_position(remaining_steps, stop_pin, total_steps)
	DBFunctions.new_position(cnx, cursor, final_position)

	return remaining_steps



def check_and_run_any_pending_events(cnx, cursor):
	print("Main::check_and_run_any_pending_events")
	# get events [(event_key, desire_position)]
	non_activated_events = DBFunctions.all_non_activated_events(cursor)
	if non_activated_events:
		# run newest; ignore others
		remaining_steps = activate_curtain(cnx, cursor, non_activated_events[0][1])
		for event in non_activated_events:
			DBFunctions.mark_event_as_activated(cnx, cursor, event[0])

		return remaining_steps
	return None


def check_if_calibration_necessary(cnx, cursor, remaining_steps):
	if not remaining_steps: return

	total_steps = DBFunctions.curtain_length(cursor)
	# check if motor stopped prematurely
	leniency = STOPPED_PERCENT_LENIENCY * total_steps / 100
	if leniency < remaining_steps: CalibrateCurtain.calibrate()



def main():
	# program loop
	while True:
		try:
			# main process loop
			while True:
				print("Main::process loop")
				cnx = DBFunctions.start_connection()  # connect
				if is_null_sleep_then(cnx): continue  # check if connection is established
				cursor = cnx.cursor(buffered=True)

				if PREDICT_EVENTS: EventPrediction.schedule_future_events(cnx, cursor)

				print("Main::main")
				remaining_steps = check_and_run_any_pending_events(cnx, cursor)
				if AUTO_CALIBRATE_IF_CURTAIN_STOPPED:
					check_if_calibration_necessary(cnx, cursor, remaining_steps)

				cnx.close()

				sleep(1)  # save some resources

		except Exception as error:
			try: ErrorWriter.write_error("main", str(error))  # doubly protect main program loop
			except: print(str(error))  #TESTING
			# except: pass
		sleep(5)  # something messed up; give it time to reset


if __name__ == '__main__':
	main()
