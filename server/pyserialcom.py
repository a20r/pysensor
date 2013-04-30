#!/usr/bin/env python
# -*- coding: utf-8 -*-
# serial_device PWM Signal API
import serial
import threading
import time

class SerialCommunication:

	def __init__(self, _portDir = '/dev/ttyACM', _BAUD = 9600):
		self.BAUD = _BAUD
		self.portDir = _portDir
		self.mapVal = lambda x, in_min, in_max, out_min, out_max: int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
		self.START_BYTE = '\x00'
		self.END_BYTE = '\x02'
		self.SEP_BYTE = '\x01'
		self.create_serial_connection()
	
	def create_serial_connection(self, serRange = [0,5], readTime = 0.05):
		for p in range(serRange[0],serRange[1]):
			try:
				PORT = self.portDir + str(p)
				ser = serial.Serial(PORT, self.BAUD, timeout = readTime) 
				self.connection = True 
				self.PORT = PORT
				self.ser = ser
				return
			except serial.SerialException:
				self.connection = False
		if self.connection is False:
			print 'No serial connection available'
			exit()
	
	# sending a byte signal (values of 0 to 255)
	def send(self, vals, delim = 'A'): 
		self.ser.write(delim + ''.join([chr(vals[i]) for i in range(len(vals))]))

	def close_connection(self): 
		self.ser.close()

	def read(self):
		arg_list = list()
		ar_event = str()

		# flushes before reading to avoid reading serial junk
		self.ser.flush()

		# waits for the starting byte
		while self.ser.read() != self.START_BYTE:
			pass

		# parses the command
		while True:
			ar_event_char = self.ser.read()
			if ar_event_char != self.SEP_BYTE:
				if ar_event_char != self.START_BYTE and ar_event_char != self.END_BYTE:
					ar_event += ar_event_char
			else:
				break

		# parses the arguments (simply byte arguments at the moment)
		while True:
			ar_arg = self.ser.read()
			if ar_arg != self.END_BYTE:
				arg_list += [ar_arg]
			else:
				break
		return ar_event, arg_list	

class SerialEventHandler(threading.Thread, SerialCommunication):

	func_map = dict()

	def __init__(self):
		self.finished = False
		threading.Thread.__init__(self)
		SerialCommunication.__init__(self)

	@staticmethod
	def add_key(value):
		def _decorator(func):
			try:
				SerialEventHandler.func_map[value] += [func]
			except KeyError:
				SerialEventHandler.func_map[value] = [func]
			return func
		return _decorator

	def read_values(self):
		while not self.finished:
			ar_event, ar_arg = self.read()
			if ar_event != '' and ar_event != None:
				print 'Event: ', ar_event, ' ', time.asctime()
				try:
					for fn in SerialEventHandler.func_map[ar_event]:
						fn(self, ar_arg)
				except KeyError:
					pass

	def run(self):
		self.read_values()

	def stop(self):
		self.finished = True

if __name__ == "__main__":
	serial_device = SerialCommunication()
	serial_device.create_serial_connection()
	import time
	while True:
		print serial_device.read()
		time.sleep(0.5)