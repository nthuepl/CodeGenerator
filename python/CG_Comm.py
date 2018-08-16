import os
import sys
import collections
import serial
import time
import struct
import threading
import time

from ble_builder import BLEBuilder
from ble_parser import BLEParser
from serial.tools import list_ports

class CG_Comm():

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
	connect_cnt = 0
	ble_header_handle = "\x49\x00"
	ble_code_handle =  "\x4C\x00" 
	ble_isflashcode_handle = "\x52\x00"
	ble_codesection_handle = "\x55\x00"
	
	isConnected = False;
	isWrote = False;
	
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
		duplicate = 0
		packet = packet.encode("hex")
		if packet[6:10] == "0d06" and packet[12:14] == "04":
			addr1, addr2, addr3, addr4, addr5, addr6 = struct.unpack('2s2s2s2s2s2s',packet[16:28])
			address = addr1.upper()+":"+addr2.upper()+":"+addr3.upper()+":"+addr4.upper()+":"+addr5.upper()+":"+addr6.upper()
			for value in self.addr_dic.values():
				if value == address:
					duplicate = 1
					break
			if duplicate == 0 :
				self.devicecnt += 1
				self.addr_dic.update({self.devicecnt:address})
				if self.devicecnt < 10:
					print str(self.devicecnt) + ":  " + address
				else:
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
		elif packet[6:10] == "1305" and packet[10:12] == "00": # writeRsp
			self.set_write_attr_status()
			#print "writeRsp\n"
			"""
			-Type		: 0x04 (Event)
			-EventCode	: 0xFF (HCI_LE_ExtEvent)
			-Data Length	: 0x06 (6) bytes(s)
			 Event		: 0x0513 (ATT_WriteRsp)
			 Status		: 0x00 (Success)
			 ConnHandle	: 0x0000 (0)
			 PduLen		: 0x00 (0)
			Dump(Rx):
			04 FF 06 13 05 00 00 00 00 
			"""
		elif packet[6:10] == "0506" and packet[10:12] == "00": # GAP_EstablishLink
			self.set_connection_status()
			"""
			-Type		: 0x04 (Event)
			-EventCode	: 0xFF (HCI_LE_ExtEvent)
			-Data Length	: 0x13 (19) bytes(s)
			 Event		: 0x0605 (GAP_EstablishLink)
			 Status		: 0x00 (Success)
			 DevAddrType	: 0x00 (Public)
			 DevAddr		: AA:AA:AA:AA:AA:15
			 ConnHandle	: 0x0000 (0)
			 ConnInterval	: 0x0050 (80)
			 ConnLatency	: 0x0000 (0)
			 ConnTimeout	: 0x07D0 (2000)
			 ClockAccuracy	: 0x00 (0)
			Dump(Rx):
			04 FF 13 05 06 00 00 15 AA AA AA AA AA 00 00 50 
			00 00 00 D0 07 00 
			"""
		
	def connect(self, inaddr):
		"""
		inaddr: No. of device you want to connect
		"""
		
		addr = self.addr_dic[inaddr].replace(':', "")

		addr = addr.decode("hex")
		self.clear_connection_status()
		self.ble_builder.send("fe09", peer_addr=addr)
		
		#print self.isConnected
		# wait for connect ack
		self.wait_connection_response()
		self.connect_cnt = self.connect_cnt + 1;
		print '\n> Device Connected',
		#print self.isConnected

	def disconnect(self, id = 1):
		conn_handle = self.id_dic[id].decode("hex")
		self.ble_builder.send("fe0a", conn_handle = conn_handle)
		self.connect_cnt = self.connect_cnt - 1;

	def sendACK(self, id):
		
		self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = "\x39\x00", value = chr(0))

	#def send(self, location = 0, section = 0, code = [0x63, 0x80, 0x20, 0x22], id = 1, seq = 0):
	#def send(self, location = 0, section = 0, code = [0x63, 0xa0, 0x02, 0x22], id = 1, seq = 0):
	#def send(self, location = 1, section = 4, code = [0x63, 0xa0, 0x02, 0x02, 0x01, 0x22], id = 1, seq = 0):
	# performPeriodicTask
	#def send(self, location = 1, section = 4, code = [0x02,0xA0,0x03,0x12,0x0A,0x07,0x02,0x01,0x22,0x22 ], id = 1, seq = 0):
	
	# uartWriteByte
	def send(self, location = 1, section = 4, code = [0x75,0x82,0x45,0x12,0xA0,0x14,0x02,0x01,0x22,0x22
		,0x12,0x0A,0x07,0x22,0xAA,0x82,0x12,0x07,0xFD,0x22
		,0xA9,0x82,0x12,0x08,0x03,0x22], id = 1, seq = 0):
		
		"""
		location: RAM or flash, 0 for ram, 1 for flash
		section: flash code section. Section 4 is ready now, memory access is 0x6A000. 
		code: The code will be execute
		id: ID of MCU
		seq: Sequence number of this code
		"""
		
		codetmp = ''
		self.packet_list.append([0, seq, id])
		code_len = len(code)
		data_len = 20
		index = len(self.packet_list)-1
		self.clear_write_attr_status()
		
		
		if(code_len%data_len == 0):
			seg = (code_len/data_len)
		else:
			seg = (code_len/data_len) + 1
		
		print "> Code size: ", code_len

		#time.sleep(1)
		start_time = time.time()
		
		# set isFlashCode flag
		codetmp = chr(location)
		self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = self.ble_isflashcode_handle, value = codetmp)
		self.wait_write_attr_response()
		print "> Sent location packet."
		
		# set Flash Code Section
		if location == 1:
			codetmp = chr(section)
			self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = self.ble_codesection_handle, value = codetmp)
			self.wait_write_attr_response()
			print "> Sent section packet."

		# set header
		#codetmp = chr(seq/255) + chr(seq%255) + chr(seg) + chr(code_len)
		codetmp = chr(seq/256) + chr(seq%256) + chr(seg/256) + chr(seg%256) 
		self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = self.ble_header_handle, value = codetmp)
		self.wait_write_attr_response()
		print "> Sent total code segment: ", seg
		
		#Toggle LED code: [99, 128, 32]
		
		print "Programming Progress:"
		for i in range(seg):
			codetmp = ''	
			if code_len <= data_len:		
				for j in range(code_len):
					codetmp = codetmp + struct.pack("B", code[j])					 
				for j in range(data_len-code_len):
					codetmp = codetmp + "\x00" 
				self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = self.ble_code_handle, value = codetmp)
			elif (i+1)*data_len <= code_len:
				for j in range(data_len):
					codetmp = codetmp + struct.pack("B", code[j+i*data_len])
				self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = self.ble_code_handle, value = codetmp)
			else:
				for j in range(code_len-i*data_len):
					codetmp = codetmp + struct.pack("B", code[j+i*data_len])
					
				for j in range(data_len-(code_len-i*data_len)):
					codetmp = codetmp + "\x00"
				
				self.ble_builder.send("fd92", conn_handle = self.id_dic[id].decode("hex"), handle = self.ble_code_handle, value = codetmp)
			
			self.wait_write_attr_response()
			update_progress( int(round((float(i+1)/float(seg))*100)) )
		
		print '%s%5.2f%s'%( 'elapsed ',time.time()-start_time,' seconds.')

		while self.packet_list[index][0] == 0:
			pass
		
		result = self.packet_list[index][3]
		del self.packet_list[index]
		
		return result

	def scan(self):
		old_devicecnt = 0
		self.devicecnt = 0
		self.addr_dic = {}		
		#start a device discovery scan
		self.ble_builder.send("fe04", mode="\x03")
		print("Starting device scan")
		time.sleep(2)
		#cancel scan
		self.ble_builder.send("fe05")
		
		while old_devicecnt != self.devicecnt:
			old_devicecnt = self.devicecnt	# store devicecnt for next comparison
			#re scan
			self.ble_builder.send("fe04", mode="\x03")
			time.sleep(2)
			#cancel re scan
			self.ble_builder.send("fe05")
		print("Scan Done")
		
	def clear_write_attr_status(self):
		self.isWrote = False

	def clear_connection_status(self):
		self.isConnected = False

	def wait_write_attr_response(self):
		while self.isWrote == False:
			pass
		self.clear_write_attr_status()
		
	def wait_connection_response(self):
		while self.isConnected == False:
			pass
		self.clear_connection_status()
		
	def set_write_attr_status(self):
		self.isWrote = True
		
	def set_connection_status(self):
		self.isConnected = True

def serial_ports():

	if os.name == 'nt' or os.name== 'posix':
		for i in range(256):
			try:
				s = serial.Serial(i)
				s.close()				
				yield serial.device(i)
			except serial.SerialException:
				pass
			except OSError:
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
		if Comm.connect_cnt != 0:
			for i in range(Comm.connect_cnt):
				Comm.disconnect(i+1)
		Comm.ble_parser.stop()		
	sys.exit(0)

def update_progress(progress):
	if progress == 100:
		print '\r[{0}{1}] {2}%'.format('#'*(progress/2), ' '*(50-(progress/2)), progress)
	else:
		print '\r[{0}{1}] {2}%'.format('#'*(progress/2), ' '*(50-(progress/2)), progress),

if __name__ == "__main__":
		
	com_dic = scan_com_port()	
	
	if len(com_dic) > 0:
		print "Available COM ports"
		for x in range(len(com_dic)):
			print str(x+1)+": "+com_dic[x+1]
		
		port = com_dic[int(raw_input("Select COM port: "))]
		if port != 0:
			comm = CG_Comm(port)
			if len(comm.addr_dic) > 0:
				nodeNumber = int(raw_input("Select Node: "))
				if nodeNumber != 0:
					comm.connect(nodeNumber)
	else:
		print "No Available COM port"