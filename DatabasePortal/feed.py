#!/usr/bin/env python3
__author__ = "MPZinke"

###################################################
#
#	-Runs AIO to connect to Google Asst via IFTTT
#	 to open/close
#
###################################################

from Adafruit_IO import MQTTClient
import init
from time import sleep, time

#openkey=###OPENKEY
#closekey=###CLOSEKEY

class Vars:
	def __init__(self):
		self.key = "###KEY"  #CUSTOMIZE: add your key here
		self.name = "###NAME"  #CUSTOMIZE: add your user name here



def connect(client):
	#CUSTOMIZE: put your feeds here
	for item in ["###OPENKEY", "###CLOSEKEY"]:
		client.subscribe(item)


def disconnect(client):
	print("Connection error", time())


def action(client, feed_id, payload, retain):
	cnx = init.start_connection("localhost")
	if feed_id == "###OPENKEY":  #CUSTOMIZE: replace with your feed
		print(init.initiate(cnx, 'O') or "Failed to initiate")
	elif feed_id == "###CLOSEKEY":  #CUSTOMIZE: replace with your feed
		print(init.initiate(cnx, 'C') or "Failed to initiate")



def loop():
	gbl = Vars()
	
	while True:
		try:
			
			print("Client loop begun")
			client = MQTTClient(gbl.name, gbl.key)

			client.on_connect = connect
			client.on_disconnect = disconnect
			client.on_message = action

			client.connect()

			client.loop_blocking()
		except:
			print("Execution error", time())
			sleep(5)



if __name__ == "__main__":
	loop()


""" created by: MPZinke on 06.20.18
	edited by: MPZinke on 01.19.19 for quick installation """