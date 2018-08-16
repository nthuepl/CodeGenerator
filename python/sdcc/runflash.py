'''
	This is the Python program for programming the flash followed by
	calling the code and returning
	example: python runflash.py testhello.bin ''
'''
import CG_Comm
import struct
import sys

if len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == '--help' or \
			len(sys.argv) >= 3 and sys.argv[1][-4:] != '.bin':
			sys.exit("usage: " + sys.argv[0] + """ file.bin typePattern
(example: python runflash.py testhello.bin '')
where type pattern can be
		'<h' = int16 little endian, > makes it big endian
		'<H' = uint16 little endian
		'b' = signed char => python int; 'B' = unsigned char => python int
		'c' = char = string of length 1
		'?' = boolean
		'i' = C int to python int
		'I' = C unsigned int to python int""")

BINARY = sys.argv[1]

FORMAT = sys.argv[2]  # for raw string (should be same as 's')


def sendMain(CG, code):
	return CG.send(1, 4, code)

def sendCallBacks(CG, code):
	return CG.send(1, 1, code)

def sendJumpTable(CG, code):
	return CG.send(1, 0, code)

if __name__ == '__main__':
	CG = None
	UseSerialPort = True
	if UseSerialPort:
		com_dic = CG_Comm.scan_com_port()

		print "Available COM ports"
		for x in range(len(com_dic)):
			print str(x+1)+": "+com_dic[x+1]
	
		port = com_dic[int(raw_input("Select COM port: "))]
		CG = CG_Comm.CG_Comm(port)
		nodeNumber = int(raw_input("Select node: "))
	
	while True:
		CG.connect(nodeNumber)
		
		if 'CallBacks' in sys.argv[1]:
			fh = open(BINARY, 'rb')
			callbacksCode = [i for i in bytearray(fh.read())]
			fh.close()
			
			fh = open( sys.argv[1][0:6]+"/CodeGeneratorJumpTable.bin", 'rb' )
			tableCode = [i for i in bytearray(fh.read())]
			fh.close()
			
			print "\nProgramming Jump Table."
			retVal = sendJumpTable(CG, tableCode)
			
			print "\nProgramming CallBacks Machine Code."
			retVal = sendCallBacks(CG, callbacksCode)
		else:
			fh = open(BINARY, 'rb')
			machineCode = [i for i in bytearray(fh.read())]
			fh.close()
			retVal = sendMain(CG, machineCode)
			
		if FORMAT == '':
			print retVal  # print as raw string
		else:
			print struct.unpack(FORMAT, retVal)
		
		CG.disconnect()
		
		raw_input("type any key to reprogram " + sys.argv[1] + " or Ctrl+C to exit\n>" )
		