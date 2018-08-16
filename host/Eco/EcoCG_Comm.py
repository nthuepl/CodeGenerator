import os
import sys
import collections
import serial
import time
import struct
import threading

from serial.tools import list_ports



class ThreadQuitException(Exception):
	pass

class EcoCG_Comm(threading.Thread):

	TRANSMIT = 0
	RECIEVE = 1
	IDLE = 0
	WAIT_FOR_DATA = 1
	WAIT_FOR_ACK = 2
	devicecnt = 0
	addr_dic = {}
	packet_list = []
	mcu_list = []
	id_dic = {1: '0000', 2: '0001', 3: '0002', 4: '0003'}
	ch_dic = {'0000': 1, '0001': 2, '0002': 3, '0003': 4}
	state = 0
	max_len = 28
	STATE = 0
	
	def __init__(self, com_port):
		
		super(EcoCG_Comm, self).__init__()
		self.serial_port = serial.Serial(port=com_port, baudrate=19200)
		self.packetcnt = 0
		self._thread_continue = True
		self._stop = threading.Event()
		self.STATE = self.IDLE
		self.start()		
	
	def run(self):
		
		read = ''
		data = ''
		self.packetcnt = 0
		
		while True:
			try:
				if not self._thread_continue:
					raise ThreadQuitException
				
				read = self.serial_port.read()
				
				if self.STATE == self.WAIT_FOR_ACK:

					data = data + read					
					self.packetcnt = self.packetcnt + 1
					
					if self.packetcnt == self.max_len:
						self.packetcnt = 0
						self.STATE = self.IDLE
						data = ''
				
				elif self.STATE == self.WAIT_FOR_DATA:
					
					data = data + read					
					self.packetcnt = self.packetcnt + 1
					
					if self.packetcnt == self.max_len:
						self.packet_list[0].append(data)
						self.packet_list[0][0] = 1						
						self.packetcnt = 0
						self.STATE = self.IDLE
						data = ''
						
				#print read.encode('hex'),
				#sys.stdout.softspace=0
				
			except ThreadQuitException:
				break
	
	def stop(self):
		self._thread_continue = False
		self.serial_port.close()
		self._stop.set()
		
	def analyse_packet(self):
		
		packet = ""
		
		len = int(self.serial_port.read().encode("hex"), 16)
		for i in range(len):
			packet = packet + self.serial_port.read()
				
		#packet = packet.encode("hex")
		id = packet[0]
		value = packet[1:len(packet)]#.decode("hex")
		#revc_seq = int(value[0:2])
		#revc_result = value[3:len(value)]
		i = 0
		for item in self.packet_list:
			if item[2] == id:
				self.packet_list[i].append(value)
				self.packet_list[i][0] = 1	
				break
			else:
				i += 1
						
	#def connect(self, inaddr):
		
		

	#def disconnect(self, id = 1):

		

	def sendpacket(self, packet):
		
		packet_len = len(packet)
		self.packetcnt = 0

		#print packet 
		
		for x in packet:
			self.serial_port.write(x)		
				
		
	def send(self, code = [0x63,0x80,0x20, 0x00, 0x00, 
	 0x00, 0x00, 0x00, 0x00, 0x00
	 ,0x00, 0x00, 0x00, 0x00, 0x00
	 ,0x00, 0x00, 0x00, 0x00, 0x00
	 ,0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x22 ], id = 1, seq = 0):
		
		"""
		code: The code will be execute
		id: ID of MCU
		seq: Sequence number of this code
		"""
		head = []
		payload = []
		self.packet_list.append([0, seq, id])
		data_len = 28
		code_len = len(code)
		total_len = code_len + (data_len-(len(code)%data_len))		
		index = len(self.packet_list)-1
		result = ''
		
		if(code_len%data_len == 0):
			seg = (code_len/data_len)
		else:
			seg = (code_len/data_len) + 1

		head.append(chr(seq/255))
		head.append(chr(seq%255))
		head.append(chr(seg))
		head.append(chr(total_len))
		for i in range(data_len-4):
			head.append("\x00")	
		
		self.STATE = self.WAIT_FOR_ACK
		self.sendpacket(head)			
		while self.STATE == self.WAIT_FOR_ACK:
			pass			
		time.sleep(1)
		
		for i in range(seg):
			payload = []	
			if code_len <= data_len:		
				for j in range(code_len):
					payload.append(struct.pack("B", code[j+i*data_len]))					 
				for j in range(data_len-code_len):
					payload.append("\x00")
				#print payload
				self.STATE = self.WAIT_FOR_DATA
				self.sendpacket(payload)

			else:
				for j in range(data_len):
					payload.append(struct.pack("B", code[j+i*data_len]))
				code_len = code_len - data_len
				self.STATE = self.WAIT_FOR_ACK
				self.sendpacket(payload)
				while self.STATE == self.WAIT_FOR_ACK:
					pass
				time.sleep(0.5)			
						
		while self.packet_list[index][0] == 0:
			pass
		
		
		result = self.packet_list[index][3]
		del self.packet_list[index]
		
		return result
				

def serial_ports():

	if os.name == 'nt':
		for i in range(256):
			try:
				s = serial.Serial(i)
				s.close()				
				yield serial.device(i)
			except serial.SerialException:
				pass
	else:
		for port in list_ports.comports():
			yield port[0]
			
def scan_com_port():
	dic = {}
	x = list(serial_ports())
	i = 1	
	for item in x:
		dic.update({i:item})
		i = i+1
				
	return dic

def close(Comm = None):
	if Comm != None:
		Comm.stop()		
	sys.exit(0)
	
if __name__ == "__main__":
		
	com_dic = scan_com_port()	
	
	print "Available COM ports"
	for x in range(len(com_dic)):
		print str(x+1)+": "+com_dic[x+1]
	
	port = com_dic[int(raw_input("Select COM port: "))]
	
	if port != 0:
		CG = EcoCG_Comm(port)
	