#!/usr/bin/env python3
# main activation of smart curtain

#TODO implement motor functions

from datetime import datetime
import os
# import RPi.GPIO as GPIO


def curtain_is_open():
	file_name = "./text_files/curtain_state.txt"
	file_in = open(file_name, "r")
	state = int(file_in.readline()[6])
	file_in.close()
	return state


def close_window():
	# try:
	print("motor closing window")  #TODO replace with code to activate motors
	rewrite_file("0")
	log_writer("close")
	# except:
		# print("Mechanical Failure")

def open_window():
	# try:
	print("motor opening window")  #TODO replace with code to activate motors
	rewrite_file("1")
	log_writer("open")
	# except:
		# print("Mechanical Failure")


def rewrite_file(string):
	file = open("./text_files/curtain_state.txt", "w")
	file.write("state:" + string + "\n#0 == closed, 1 == open\
		\n" + str(datetime.today())[11:19])
	file.close()


def log_writer(process):
	time = str(datetime.now()) + "; " + process
	print(time)
	logs = open("./text_files/log.txt", "a+")
	if os.stat("./text_files/log.txt").st_size != 0: time = "\n" + time
	logs.write(time)
	logs.close()


def main():
	
	if curtain_is_open():
		close_window()
	else:
		open_window()




if __name__ == "__main__":
	main()

""" created by MPZinke on 06.28.18 """