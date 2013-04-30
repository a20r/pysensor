
import pyserialcom
import pygame
import threading
import time

class MovementAlarm(pyserialcom.SerialEventHandler):

	def __init__(self):
		pyserialcom.SerialEventHandler.__init__(self)
		pygame.init()

	@pyserialcom.SerialEventHandler.add_key('MOTION')
	def motion_sensed(self, *args):
		#print '\tMotion Sensed!\n'
		self.movement_stopped = False
		self.alarm_thread = threading.Thread(target = self.alarm_loop)
		self.alarm_thread.start()

	@pyserialcom.SerialEventHandler.add_key('MOTIONENDED')
	def sensor_release(self, *args):
		self.movement_stopped = True
		pygame.mixer.music.stop()

	@pyserialcom.SerialEventHandler.add_key('KILLCOM')
	def kill(self, *args):
		self.sensor_release()
		self.close_connection()

	def alarm_loop(self):
		pygame.mixer.music.load('sounds/alarmsound.mp3')
		while not self.movement_stopped:
			pygame.mixer.music.play()
			time.sleep(10)
			pygame.mixer.music.stop()

if __name__ == "__main__":
	try:
		ma = MovementAlarm()
		ma.read_values()
	except KeyboardInterrupt:
		print "Killing..."
		ma.kill()