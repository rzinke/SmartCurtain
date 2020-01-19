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

from threading import Thread
from time import sleep

from Definitions import *

import AdafruitFeed
import DaytimeEvents
import ErrorWriter
import EventPredictor


def main():
	# program loop
	while True:
		try:
			threads =	[
							Thread(target=AdafruitFeed.start_client_loop),
							Thread(target=DaytimeEvents.sunrise_loop),
							Thread(target=DaytimeEvents.sunset_loop),
							Thread(target=EventPredictor.predictor_loop)
						]
			for thread in threads:
				thread.start()
			for thread in threads:
				thread.join()

		except Exception as error:
			try: ErrorWriter.write_error(error)  # doubly protect main program loop
			except: print(error)
		sleep(ERROR_WAIT)  # something messed up; give it time to reset


if __name__ == '__main__':
	main()
