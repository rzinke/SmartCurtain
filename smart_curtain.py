#!/usr/bin/env python3

# main activation of smart curtain

from datetime import datetime
# import RPi.GPIO as GPIO

def read_file():
	file_name = "./text_files/curtain_state.txt"
	file_in = open(file_name, "r")
	return file_in


def curtain_is_open(file):
	state = int(file.readline()[6])
	file.close()
	return state


def close_window():
	try:
		print("motor closing window")  #TODO replace with code to activate motors
		rewrite_file("0")
		log_writer("close")
	except:
		print("Mechanical Failure")

def open_window():
	try:
		print("motor opening window")  #TODO replace with code to activate motors
		rewrite_file("1")
		log_writer("open")
	except:
		print("Mechanical Failure")


def rewrite_file(string):
	file = open("./text_files/curtain_state.txt", "w")
	file.write("state:" + string + "\n#0 == closed, 1 == open\
		\n" + str(datetime.today())[11:19])
	file.close()


def log_writer(process):
	time = str(datetime.now()) + "; " + process
	logs = open("./text_files/log.txt", "r+")
	if logs.readline(): time = "\n" + time
	logs.write(time)
	logs.close()


def main():
	
	file = read_file()
	
	if curtain_is_open(file):
		close_window()
	else:
		open_window()




if __name__ == "__main__":
	main()

""" created by MPZinke on 06.28.18 """