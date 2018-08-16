List Available COM-ports
-
The program will list available COM-ports on your computer. You have to select the COM-port the dongle is connected.
	
	Available COM ports
    1: COM1
	2: COM3
    Select COM port: 
	
Scan Node
-
In "scan" function, the dungle will scan other devices and display the No. and MAC address of each device.

    >>>comm.scan()
    Starting device scan
    1: 00:00:00:00:00:FF
    2: 00:00:00:00:00:00   
    Scan Done

Connect to a Node
-
Use connect(number) to connet to the device. "number" is the No. of the device displayed on the screen when it is scanned.

    comm.connect(1)

Send Code to a Node
-
Send code by using send(code, id, seq). "code" is the code you want to send to device. The format is a integer list. "id" is the ID of the MCU. Default is 1. "seq" is the sequence number of this code. Default is 0. This function will return the result from the node.

    comm.send([0x63, 0x80, 0x20], 1, 1)

Disconnect to a Node
-  
Use disconnect(id) to disconnect the connection. "id" is the ID of the device. First device is "1". Second is "2" and so on. Default is "1".

    comm.disconnect(1)
	
Close program
-
Use close(comm) to close program. "comm" is the CG_comm object. This API will disconnect to all node that the dongle is connecting and close the serial port.