import requests
import os
from subprocess import call
import time
import signal
import sys
import math


ether_url = "http://piratepad.be/p/bla/export/txt"


def play():
	start = time.time()
	r = requests.get(ether_url)

	t = str(r.text.encode('utf-8'))

	cmd = "("

	t = t.split('\n')

	cmd += 'echo "' + t[0] + '"'

	del t[0]

	for line in t:
		cmd += ' && echo "' + line + '" '

	cmd += ")| sonic_pi "

	#print "XX",cmd,"XX"

	os.popen(cmd)
	return time.time() - start



if __name__ == "__main__":



	def signal_handler(signal, frame):
		print '\nShutting down!'
		os.popen("sonic_pi stop")
		quit()
			
	signal.signal(signal.SIGINT, signal_handler)
	if sys.argv[0]:
		print

	beat_length = 60 / 60 #length of one beat in seconds
	refresh_counter = 4 #every how many beats do we refresh the loop?
	early_buffer = 0.5 #thats empirical, sonic pi takes roughly half a second to start playing
	
	#here we go, lets play!
	play()
	time.sleep(early_buffer)
	#lets remember at which point in time we started playing
	init = time.time()
	#we dont have to skip a beat right now
	skip = 0
	while True:
		#a new phrase started!
		print "---------------"
		for x in range(refresh_counter -1):
			if skip > 0: #if the skip counter is unequal to zwero, lets skip a beat
				skip -= 1
				print "tick",x+1
				print "WE SKIPPED A BEAT, but thats not fatal. Anyways, your internetconnection is slow"
				continue
			print "tick",x+1
			print time.time() - init
			time.sleep(beat_length)

		print "tick 4"
		print time.time() - init
		behind = math.fmod(time.time() - init,beat_length) #how far are we behind where we actually should be?
		print "now we execute"
		#play returns the time it took to download the etherpad and to play it.
		playtime = play()
		if playtime >beat_length:
			#if that plus our behind variable is longer than a beat, we have a problem and will ned to skip one
			skip = math.floor(playtime+ behind)
			playtime = math.fmod(playtime+behind,beat_length)
		print "we executed, time passed:" ,playtime
		print time.time() - init
		sleeptime = beat_length- playtime-behind
		if sleeptime < 0:
			sleeptime = 0
		print "now we sleep", sleeptime
		time.sleep(sleeptime) 
		print time.time() - init
		
		


