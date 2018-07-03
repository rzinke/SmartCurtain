#!/usr/bin/env python3
# Curtain Adafruit IO feed loop

from Adafruit_IO import MQTTClient
import initiate_curtain
from time import sleep, time

class Vars:
	def __init__(self):
		self.key = "7aad007f269d46219ac27a4b602571ce"
		self.name = "MPZinke"



def connect(client):
	client.subscribe("open-curtain")
	client.subscribe("close-curtain")


def disconnect(client):
	print("Error", time())


#TODO restructure when the file is closed, b/c it closes it before it
# is able to process the file a second time
def action(client, feed_id, payload, retain):
	
	state = initiate_curtain.curtain_is_open()
	if feed_id == "open-curtain":
		if state:
			print("Curtains are already open")
			return
		initiate_curtain.open_window()
	elif feed_id == "close-curtain":
		if not state:
			print("Curtains are already closed")
			return
		initiate_curtain.close_window()




def loop():
	gbl = Vars()
	
	while True:
		# try:
		print("Client loop begun")
		client = MQTTClient(gbl.name, gbl.key)

		client.on_connect = connect
		client.on_disconnect = disconnect
		client.on_message = action

		client.connect()

		client.loop_blocking()
		# except:
		# 	print("Error", time())
		# 	sleep(5)



if __name__ == "__main__":
	loop()


