import os
import sys
import collections
import serial
import time
import struct
import threading

from ble_builder import BLEBuilder
from ble_parser import BLEParser
from serial.tools import list_ports

class CodeGen():

	TRANSMIT = 0
	RECIEVE = 1
	DATA = 0
	ACK = 1
	devicecnt = 0
	addr_dic = {}
	packet_list = []
	mcu_list = []
	id_dic = {1: '0000', 2: '0001', 3: '0002', 4: '0003'}
	ch_dic = {'0000': 1, '0001': 2, '0002': 3, '0003': 4}
	mutex = threading.Lock()
	state = 0
	max_len = 0
	
	def __init__(self, com_port):
		self.serial_port = serial.Serial(port=com_port, baudrate=57600)
		self.ble_builder = BLEBuilder(self.serial_port)
		self.ble_parser = BLEParser(self.serial_port, callback=self.analyse_packet)
		self.devicecnt = 0
		#initialise the device
		self.ble_builder.send("fe00")
		#get an operating parameter value
		self.ble_builder.send("fe31", param_id="\x15")
		self.scan()
		
	def analyse_packet(self, (packet, dictionary)):

		packet = packet.encode("hex")
		if packet[6:10] == "0d06" and packet[12:14] == "04":
			addr1, addr2, addr3, addr4, addr5, addr6 = struct.unpack('2s2s2s2s2s2s',packet[16:28])
			address = addr1.upper()+":"+addr2.upper()+":"+addr3.upper()+":"+addr4.upper()+":"+addr5.upper()+":"+addr6.upper()
			self.devicecnt += 1
			self.addr_dic.update({self.devicecnt:address})
			print str(self.devicecnt) + ": " + address

		elif packet[6:10] == "1b05":
			"""
			Type: 0x04 (Event)
			EventCode: 0xFF (HCI_LE_ExtEvent)
			Data Length: 0x0A bytes(s)
			Event: 0x051B (ATT_HandleValueNotification)
			Status: 0x00 (Success)
			ConnHandle: 0x0000
			EventLen: 0x04
			AttrHandle: 0x003A
			Value: 4A 04
			Dump(Rx):
			04 FF 0A 1B 05 00 00 00 04 3A 00 4A 04
			"""
			conn_handle = packet[12:16]
			value = packet[22:len(packet)].decode("hex")
			#revc_seq = int(value[0:2])
			#revc_result = value[3:len(value)]
			i = 0
			for item in self.packet_list:
					if item[2] == self.ch_dic[conn_handle]:
						self.packet_list[i].append(value)
						self.packet_list[i][0] = 1	
						break
					else:
						i += 1
			
	def connect(self, inaddr):
		"""
		inaddr: No. of device you want to connect
		"""
		
		print "addr_dic = ", self.addr_dic
		addr = self.addr_dic[inaddr].replace(':', "")

		addr = addr.decode("hex")
		self.ble_builder.send("fe09", peer_addr=addr)

	def disconnect(self, id = 1):

		conn_handle = id_dic[id].decode("hex")
		self.ble_builder.send("fe0a", conn_handle = conn_handle)


	def sendACK(self, id):
		
		self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = "\x39\x00", value = chr(0))

		
	def send(self, code = [0x63, 0x80, 0x20, 0x22], id = 1, seq = 0, retval_type = None, destination_id = None):
		
		"""
		code: The code will be execute
		id: ID of MCU
		seq: Sequence number of this code
		"""
		codetmp = ''
		self.packet_list.append([0, seq, id])
		code_len = len(code)
		data_len = 19
		index = len(self.packet_list)-1
		
		if(code_len%data_len == 0):
			seg = (code_len/data_len)
		else:
			seg = (code_len/data_len) + 1
		
		codetmp = chr(seq/255) + chr(seq%255) + chr(seg) + chr(code_len)
		self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = "\x36\x00", value = codetmp)
		
		#Toggle LED code: [99, 128, 32]
		
		time.sleep(2)
		for i in range(seg):
			codetmp = ''	
			if code_len <= data_len:		
				for j in range(code_len):
					codetmp = codetmp + struct.pack("B", code[j])					 
				for j in range(data_len-code_len):
					codetmp = codetmp + "\x00"
				self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = "\x39\x00", value = codetmp)
			elif (i+1)*data_len <= code_len:
				for j in range(data_len):
					codetmp = codetmp + struct.pack("B", code[j+i*data_len])
				self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = "\x00\x00", value = codetmp)
			else:
				for j in range(code_len-i*data_len):
					codetmp = codetmp + struct.pack("B", code[j+i*data_len])
				
				for j in range(data_len-(code_len-i*data_len)):
					codetmp = codetmp + "\x00"
				
				self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = "\x00\x00", value = codetmp)
			

		while self.packet_list[index][0] == 0:
			pass
		
		result = self.packet_list[index][3]
		del self.packet_list[index]
		
		return result

	def scan(self):
	
		self.devicecnt = 0
		self.addr_dic = {}		
		#start a device discovery scan
		self.ble_builder.send("fe04", mode="\x03")
		print("Starting device scan")
		#sleep main thread for 15 seconds - allow results of device scan to return
		time.sleep(5)
		#cancel scan
		self.ble_builder.send("fe05")
		print("Scan Done")

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
	
if __name__ == "__main__":
		
	com_dic = scan_com_port()	
	
	print "Available COM ports"
	for x in range(len(com_dic)):
		print str(x+1)+": "+com_dic[x+1]
	
	port = com_dic[int(raw_input("Select COM port: "))]
	CG = CodeGen(port)
	
	