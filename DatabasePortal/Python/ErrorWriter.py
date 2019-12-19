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

from datetime import datetime

from Definitions import *


def write_error(module, error):
	try:
		# change delimiter if exists
		error = error.replace(DELIMITER, ',' if ',' is not DELIMITER else ' ')
		current_timestamp = datetime.now().strftime(DATETIME_STRING_FORMAT)
		with open(ERROR_FILE_NAME, "a") as error_file:
			error_file.write("%s%c%s%c%s\n" % (	module, DELIMITER,
														error, DELIMITER, 
														current_timestamp))
	except: pass
