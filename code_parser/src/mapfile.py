#
# mapfile.py
#
from codecapsule import CodeCapsule
from cc2540var import sizeInBits, isSigned

class MapFile:
	'''This is the mapfile data structure, which allows you to
		look up a function's info by name. 
		- type signature
		- code model:
		  - near (16-bit pointer),
			- far (24-bit pointer),
			- banked code with relay
		- addresses: 
		  - function's address
			- ?CALL_IND's address (library function for making near or far
				calls, or making banked indirect function call.)
			- ?BDISPATCH's address (library function for making banked call)
			- ??function?relay address (auto generated for each function)

		Note that this is just an example file that hardwires a lot of the
		data that is manually extracted from the map file.  In practice,
		these should be parsed from the map file and the source files
		(.c or .h), which can probably inferred from the file paths for
		the .r51 or .lib files (replace the suffix).
	'''

	_map = {
			# called for near, far, or banked indirect call
			'?CALL_IND': {
				'address': 0x00001C3D,
				'module': '?CALL_IND',
				'size': 2,
			},
			# we probably don't need to call this directly
			'?BDISPATCH_FF': {
				'address': 0x00000117,
				},
			'HalAdcInit': {
				'service': 'HalADC',
				'returnType': 'void',
				'paramTypes': (),
				'paramNames': (),
				'address': 0x0001DD63,
				'stacks': ('ISTACK',),
				'relay': 0x00000A52,
				'description': '''This ADC initialization function is called once at the startup. This function has to be called before any other ADC functions can be called. It enables ADC to be initialized with both required and optional parameters.''',
				},
			'HalAdcRead': {
				'service': 'HalADC',
				'returnType': 'uint16',
				'paramTypes': ('uint8', 'uint8'),
				'paramNames': ('channel', 'resolution'),
				'paramValues': [ { \
						'HAL_ADC_CHANNEL_0': 0,
						'HAL_ADC_CHANNEL_1': 1,
						'HAL_ADC_CHANNEL_2': 2,
						'HAL_ADC_CHANNEL_3': 3,
						'HAL_ADC_CHANNEL_4': 4,
						'HAL_ADC_CHANNEL_5': 5,
						'HAL_ADC_CHANNEL_6': 6,
						'HAL_ADC_CHANNEL_7': 7,
					}, { \
						'HAL_ADC_RESOLUTION_8': 8,
						'HAL_ADC_RESOLUTION_10': 10,
						'HAL_ADC_RESOLUTION_12': 12,
						'HAL_ADC_RESOLUTION_14': 14,
					}\
				],
				'address': 0x0001DD74,
				'stacks': ('XSTACK',),
				'relay': 0x00000A58,
				'description': '''this function reads and returns the value of the ADC conversion at specified channel and resolution.
channel: input channels 0-7;
resolution: 8, 10, 12, or 14-bit.'''
				},
			'HalLedState': {
				'service': 'HalLED',
				'address': 0x00000422,
				'storageClass': 'XDATA_Z',
				'size': 1, #byte
				'segmentPart': 6,
				'file': r'C:\Documents and Settings\Brett\Desktop\ECG\CC2540DB\CC2540\Obj\hal_led.r51',
				'module': 'hal_led',
				},
			'HalLedSet': {
					'service': 'HalLED',
					'address': 0x00007FE2,
					'storageClass': ('BANKED_CODE','CODE_C'),
					'bank': 1,
					'size':  0x10, # bytes
					'segmentPart': 9,
					'stacks': ('ISTACK',),
					'returnType': 'void',
					'paramTypes': ('uint8', 'uint8'),
					'paramNames': ('led', 'mode'),
					'paramValues': [ { \
							'HAL_LED_1': 1,
							'HAL_LED_2': 2,
							'HAL_LED_3': 3,
							'HAL_LED_4': 4,
							'HAL_LED_ALL': 5,
						}, { \
							'HAL_LED_MODE_OFF': 1,
							'HAL_LED_MODE_ON': 2,
							'HAL_LED_MODE_BLNK': 3,
							'HAL_LED_MODE_FLASH': 4,
							'HAL_LED_MODE_TOGGLE': 5,
						} \
					],
				'file': r'C:\Documents and Settings\Brett\Desktop\ECG\CC2540DB\CC2540\Obj\hal_led.r51',
				'module': 'hal_led',
					'description': '''This function will set the given LED On, OFF, BLINK, FLASH, or TOGGLE. If BLINK and FLASH mode are used, a set of default parameters will be used. To customize these parameters, HalLedBlink() has to be used.''',

				},
			'HalLedEnterSleep': { \
					'service': 'HalLED',
					'address': 0x00007FF2,
					'storageClass': ('BANKED_CODE', 'CODE_C'),
					'bank': 1,
					'size': 3,
					'segmentPart': 15,
					'returnType': 'void',
					'paramTypes': (),
					'paramNames': (),
					'relay': 0x00000AC4,
					'file': r'C:\Documents and Settings\Brett\Desktop\ECG\CC2540DB\CC2540\Obj\hal_led.r51',
					'module': 'hal_led',
					'description': '''This function stores the current state of the LEDs and turn off all the LEDs to conserve power. It also sets a global state variable indicating sleep mode has been entered. This global state variable will stop the interrupt from processing the LED during while in sleep mode.''',
				},
			'HalLedExitSleep': {
					'service': 'HalLED',
					'address': 0x00007FF5,
					'storageClass': ('BANKED_CODE','CODE_C'),
					'bank': 1,
					'segmentPart': 17,
					'returnType': 'void', 
					'paramTypes': (),
					'relay': 0x00000ACA,
					'file': r'C:\Documents and Settings\Brett\Desktop\ECG\CC2540DB\CC2540\Obj\hal_led.r51',
					'module': 'hal_led',
					'description': '''This function restores the original state of
					the LEDs before the device entered sleep mode.'''
			},
			'HalKeyInit': {
					'service': 'HalKey',
					'address': 0x0001D9B1,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'segmentPart': 24,
					'size': 1, # byte
					'relay':   0x00000A9A,
					'returnType': 'void',
					'paramTypes': ('void*',),
					'paramNames': ('init',),
					'file': r'C:\Documents and Settings\Brett\Desktop\ECG\CC2540DB\CC2540\Obj\hal_led.r51',
					'module': 'hal_led',
					'description': '''This initialization funciton is called once at the startup. This function has to be called before any other function that uses keys/switches/joysticks can be called. It enables keys/switches/joysticks to be initialized with both required and optional parameters.''',
				},
			'HalKeyConfigured': {
					'service': 'HalKey',
					'address': 0x00000420,
					'storageClass': 'XDATA',
					'size': 1, #byte
					'returnType': 'void',
					'paramTypes': ('bool', 'halKeyCBack_t*'),
					'paramNames': ('interruptEnable', 'cback'),
					'file': r'C:\Documents and Settings\Brett\Desktop\ECG\CC2540DB\CC2540\Obj\hal_led.r51',
					'module': 'hal_led',
					'paramDescriptions': ( 
						'''TRUE or FALSE. Enable or disable the interrupt. If interrupt is disabled, the keys/switches/joysticks will be polled. Otherwise, the keys/switches/joysticks will be on interrupt. For maximum power savings, ensure that interruptEnable is set to TRUE so that the background key poll timer is not running keeping the device from entering sleep for long periods of time.''' ,
						'''this call back occurs when a key, switch or joystick is active. If the callback is set to NULL, the event will not be handled.
	typedef void (halKeyCback_t) (uint8 key, uint8 state);
	key - the key/switch/joystick that will cause the callback when it's triggered. Key code varies per platform (Check key table for typical key definitions for evaluation/development board.
	state - current state of the key/switch/joystick that causes the callback. Check State table.'''),
					},
			'HalKeyRead': {
					'service': 'HalKey',
					'returnType': 'uint8',
					'paramTypes': (),
					'paramNames': (),
					'address': 0x0001D9D7,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x1b, # bytes
					'segmentPart': 29,
					'calls': 'direct',
					'stacks': ('XSTACK',),
					'description': '''This function is used to read the current state of the Key/Switch/Joystick. If the Key Service is set to polling, this function will be called by the Hal Driver Task every 100 ms. If the Key Service is set to interrupt driven, this function will be called by the Hal Driver Task 25ms after the interrupt occurs. If a callback is registered during HalKeyConfig(), that callback will be sent back to the application with the new status of the keys. Otherwise, there will be no further action.''',
					'returnDescription': '''Return the key code. Key code varies per platform (Check Keys table for typical key code definitions for evaluation/development board). Key code could be comprised of bits indicating individual key/switch, as is the case for the typical key code for evaluation/development board. Some platforms, which have more keys than can be represented by 8 bits, define key code as enumerated value or as a value comprised of bits indicating row number and bits indicating column number of a key matrix.''',
					},
			'HalKeyEnterSleep': {
					'service': 'HalKey',
					'address': 0x0001DAA3,
					'size': 3, # bytes'
					'returnType': 'void',
					'paramTypes': (),
					'paramNames': (),
					'relay': 0x00000AB2,
					'description': '''This function sets a global state variable indicating sleep mode has been entered. This global state variable is used to stop the interrupt from processing the keys during sleep mode.''',
					},
			'HalKeyExitSleep': {
					'service': 'HalKey',
					'address': 0x0001DAA6,
					'returnType': 'void',
					'paramTypes': (),
					'paramNames': (),
					'calls': 'direct',
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0xa, # bytes
					'segmentPart': 40,
					'calls': 'direct',
					'stacks': ('ISTACK',),
					'relay': 0x00000A9A,
					'description': '''This function sets a global state variable indicating sleep mode has been exited. It also processes those keys that are stored by the key interrupt.''',
					},
			'HalKeyPoll': {
				'service': 'HalKey',
				'returnType': 'void',
				'paramTypes': (),
				'paramNames': (),
				'address': 0x0001D9F7,
				'calls': 'direct',
				'stacks': ('XSTACK',),
				'storageClass': 'BANKED_CODE',
				'bank': 3,
				'size': 0x51, # bytes
				'segmentPart': 32,
				'relay': 0x00000AA6,
				'description': '''This routine is used internally by hal driver''',
				},
			'HalUARTWrite': {
					'returnType': 'uint16',
					'paramTypes': ('uint8', 'uint8*', 'uint16'),
					'paramNames': ('port', 'buf', 'length'),
					'address': 0x00017FFA,
					'storageClass': 'BANKED_CODE',
					'bank': 2, 
					'size': 0x2, # bytes
					'segmentPart': 13,
					'relay': 0x00000AEE,
					'description': '''This function writes a buffer of specified length into the serial port. The function will check if the Tx buffer is full or not. If the Tx Buffer is not full, the data will be loaded into the buffer and then will be sent to the Tx data register. If the Tx buffer is full, the function will return 0. Otherwise, the length of the data that was sent will be returned.''',
					'paramDescriptions': (
							'''specified serial port that data will be read''',
							'''buffer of the data''',
							'''the length of the data'''
						),
					'paramValues': [ { \
						'HAL_UART_PORT_1': 1,
						'HAL_UART_PORT_2': 2,
						},
						None,
					],
					'returnDescription': '''Runs the length of the data that is successfully written or 0 otherwise.''',
				},
			'osal_msg_allocate': {
					'address': 0x00018F04,
					'calls': 'direct',
					'stacks': ('XSTACK',),
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x4d, # bytes
					'segmentPart': 48,
					'relay': 0x00000764,
					'returnType': 'uint8*',
					'paramTypes': ('uint16',),
					'paramNames': ('len',),
					'description': '''This function is called by a task to allocate a mesasge buffer, the task/function will then fill in the message and call osal_msg_send() to send the message to another task. If the buffer cannot be allocated, msg_ptr will be set to NULL.
Note: Do not confuse this function with osal_mem_alloc(), this function is used to allocate a buffer to send messages between tasks [using osal_msg_send()]. Use osal_mem_alloc() to allocate blocks of memory.''',
					'paramDescriptions': ('len is the length of the message.'),
					'returnDescription': '''The return value is a pointer to the buffer allocated for the message. A NULL return indicates the message allocation operation failed.''',
				},
			'osal_msg_deallocate': {
					'address': 0x00018F58,
					'relay': 0x0000076A,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x22, # bytes
					'segmentPart': 51,
					'calls': 'direct',
					'stacks': ('XSTACK', 'ISTACK'),
					'returnType': 'uint8',
					'paramTypes': ('uint8*',),
					'paramNames': ('msg_ptr',),
					'description': '''This function is used to de-allocate a message buffer. This function is called by a task (or processing element) after it has finished procesing a received message.''',
					'paramDescription': '''msg_ptr is a pointer to the message buffer that needs to be de-allocated.''',
					'returnDescription': '''Return value indicates the result of the operation''',
					'returnValue': {
							'SUCCESS': 'De-allocation Successful',
							'INVALID_MSG_POINTER': 'Invalid message pointer',
							'MSG_BUFFER_NOT_AVAIL': 'Buffer is queued.',
						},
				},
			'osal_msg_send': {
					'address': 0x00018F81,
					'returnType': 'uint8',
					'paramTypes': ('uint8', 'uint8*'),
					'paramNames': ('destination_task', 'msg_ptr'),
					'returnDescription': '''Return value is a 1-byte field indicating the result of the operation.''',
					'returnValue': {
						'SUCCESS': 'Message sent successfully',
						'INVALID_MSG_POINTER': 'Invalid Message Pointer',
						'INVALID_TASK': 'Destination_task is not valid',
						},
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0xa, # bytes
					'segmentPart': 54,
					'calls': 'direct',
					'stacks': ('XSTACK'),
					'relay': 0x00000770,
				},
			'osal_msg_receive': {
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x88, # bytes
					'segmentPart': 61,
					'address': 0x00019003,
					'calls': 'direct',
					'stacks': ('XSTACK',),
					'relays': 0x00000782,
					'returnType': 'uint8*',
					'paramTypes': ('uint8',),
					'paramNames': ('task_id',),
					'paramDescriptions': ( 'task_id is the identifier of the calling task (to which the message was destined).', ),
					'returnDescription': '''Return value is a pointer to a buffer containing the message or NULL if there is no receive message.''',
				},
			'osal_msg_find': {
					'returnType': 'osal_event_hdr_t*',
					'paramTypes': ('uint8', 'uint8'),
					'paramNames': ('task_id', 'event'),
					'description': '''This function searches for an existing OSAL message matching the task_id and event parameters''',
					'paramDescriptions': ('''task_id is the identifier that the enqueued OSAL message will match.''',
						'''event is the OSAL event id that the enqueued OSAL message must match.''',

						),
					'returnDescription': '''Return value is a pointer to the matching OSAL message on success or NULL on failure''',
					},
			'osal_set_event': {
					'address': 0x000191B7,
					'stacks': ('XSTACK',),
					'relay': 0x0000079A,
					'returnType': 'uint8',
					'paramTypes': ('uint8', 'uint16'),
					'paramNames': ('task_id', 'event_flags'),
					'paramDescriptions': ( \
							'''task_id is the identifier of the task for which the event is to be set.''',
							'''event_flag is a 2-byte bitmap which which each bit specifying an event. There is only one system event (SYS_EVENT_MSG), the rest of the events/bits are defined by the receiving task.''',
							),
					'returnDescription': '''Return value indicates the result of the operation.''',
					'returnValue': {
							'SUCCESS': 'success',
							'INVALID_TASK': 'Invalid Task',
						},
				},
			'osal_start_timerEx': {
					'returnType': 'uint8',
					'paramTypes': ('uint8', 'uint16', 'uint32'),
					'paramNames': ('taskID', 'event_id', 'timeout_value'),
					'paramDescriptions': ( \
							'''taskID is the task ID of the task that is to get the event when the timer expires.''',
							'''event_id is a user defined event bit. When the timer expires the calling task will be notified (event).''',
							'''timeout_value is the amount of time (in milliseconds) before the timer event is set.''',
							),
					'returnDescription': '''Return value indicates the result of the operation.''',
					'returnValue': {
							'SUCCESS': 'Timer Start Successful',
							'NO_TIMER_AVAILABLE': 'Unable to start the timer',
						},
				},
			'osal_stop_timerEx': {
					'address': 0x00019F43,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x32, # bytes
					'segmentPart': 26,
					'calls': 'direct',
					'stack': 'XSTACK',
					'relay': 0x0000081E,
					'returnType': 'uint8',
					'paramTypes': ('uint8', 'uint16'),
					'paramNames': ('task_id', 'event_id'),
					'description': '''This function is called to stop a timer that has already been started. If successful, the function will cancel the timer and prevent the event associated with the timer.''',
					'paramDescriptions': ( \
							'''task_id is the task for which to stop the timer.''',
							'''event_id is the identifier of the timer that is to be stopped.''',
						),
					'returnDescription': '''Return value indicates the result of the operation''',
					'returnValue': {
							'SUCCESS': 'Timer Stopped Successfully',
							'INVALID_EVENT_ID': 'Invalid Event',
						},
				},
			'osal_int_disable': {
					'address': 0x0001922B,
					'returnType': 'uint8',
					'paramTypes': ('uint8',),
					'paramNames': ('interrupt_id'),
					'description': '''This function is called to disable an interrupt. When a disabled interrupt occurs, the service routine associated with that interrupt is not called.''',
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x12, # bytes
					'segmentPart': 97,
					'paramDescription': ('''Interrupt_id identifies the interrupt to be disabled.''',),
					'returnDescription': '''Return value indicates the result of the operation.''',
					'returnValue': {
						'SUCCESS': 'Interrupt Disabled Successfully',
						'INVALID_INTERRUPT_ID': 'Invalid Interrupt',
					},
				},
			'osal_init_system': {
					'address': 0x0001923D,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x1f, # bytes
					'relay': 0x000007AC,
					'segmentPart': 99,
					'returnType': 'uint8',
					'paramTypes': (),
					'paramNames': (),
					'description': '''This function initializes the OSAL system.  The function must be called at startup prior to using any other OSAL function.''',
					'returnDescription': '''Return value indicates the result of the operation''',
					'returnValue': {
						'SUCCESS': 'success',
					},
				},
				'osal_start_system': {
					'address': 0x0001925C,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x9, # bytes
					'segmentPart': 101,
					'calls': 'direct',
					'stacks': 'ISTACK',
					'relay': 0x000007B2,
					'returnType': 'void',
					'paramTypes': (),
					'paramNames': (),
					'description': '''This function is the main loop function of the task system, repeatedly calling osal_run_system(), from an infinite loop. This function never returns. When using a different scheduler, it should call osal_run_system() directly and not use this function.''',
				},
				'osal_run_system': {
					'address': 0x00019265,
					'storageClass': 'BANKED_CODE',
					'bank': 3,
					'size': 0x99, # bytes
					'segmentPart': 103,
					'calls': 'direct',
					'stacks': 'XSTACK',
					'relay': 0x000007B8,
					'returnType': 'void',
					'paramTypes': (),
					'paramNames': (),
					'description': '''This function will make one pass through the OSAL taskEvents table and call the task_event_processor function for the first task that is found with at least one event pending. After an event is serviced, any remaining events will be returned back to the main loop for next time around. If there are no pending events (for all tasks), this function puts the processor into a Sleep mode.''',
				},
				'osal_mem_alloc': {
						'address': 0x0001CF40,
						'stacks': 'XSTACK',
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x15d, # bytes
						'segmentPart': 15,
						'relay': 0x000007D6,
						'description': '''This function is a simple memory allocation function that returns a pointer to a buffer (if successful).''',
						'returnType': 'void*',
						'paramTypes': ('unit16',),
						'paramNames': ('size',),
						'paramDescriptions': ('size - the number of bytes wanted in the buffer',),
						'returnDescription': '''A void pointer (which should be cast to the intended buffer type) to the newly allocated buffer. A NULL pointer is returned if there is not enough memory to allocate.''',
					},
				'osal_mem_free': {
						'address': 0x0001D09D,
						'stacks': ('XSTACK', 'ISTACK'),
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x3a, # bytes
						'segmentPart': 17,
						'relay': 0x000007DC,
						'returnType': 'void',
						'paramTypes': ('void*',),
						'paramNames': ('ptr',),
						'description': '''This function frees the allocated memory to be used again. This only works if the memory had already been allocated with osal_mem_alloc().''',
					},
				'osal_pwrmgr_init': {
						'address': 0x0000FF73,
						'stacks': 'ISTACK',
						'storageClass': ('BANKED_CODE', 'XDATA_ROM_C_FLASH'),
						'bank': 1,
						'size': 0xe, # bytes
						'segmentPart': 8,
						'relay': 0x000007E2,
						'returnType': 'void',
						'paramTypes': (),
						'paramNames': (),
						'description': '''This function will initialize variables used by the power management system. IMPORTANT: Do not call this function, it is already called by osal_init_system().''',
					},
				'osal_pwrmgr_powerconserve': {
						'address': 0x0000FFD3,
						'calls': 'direct',
						'stacks': 'XSTACK',
						'storageClass': ('BANKED_CODE', 'XDATA_ROM_C_FLASH'),
						'bank': 1,
						'size': 0x2c, # bytes
						'segmentPart': 15,
						'calls': 'direct',
						'stacks': 'XSTACK',
						'relay': 0x000007EE,
						'returnType': 'void',
						'paramTypes': (),
						'description': '''This function is called to go into power down mode. IMPORTANT: Do not call this function, it is already called in the OSAL main loop [osal_start_system()].''',
					},
				'osal_pwrmgr_task_state': {
						'address': 0x0000FF89,
						'stacks': 'XSTACK',
						'segmentPart': 13,
						'storageClass': ('BANKED_CODE', 'XDATA_ROM_C_FLASH'),
						'bank': 1,
						'size': 0x4a, # bytes
						'segmentPart': 13,
						'returnType': 'uint8',
						'paramTypes': ('uint8', 'uint8'),
						'paramNames': ('task_id' 'state'),
						'description': '''This function is called by each task to state whether or not this task wants to conserve power.  The task will call this function to vote whether it wants the OSAL to conserve power or it wants to hold off on the power savings. By default, when a task is created, its own power state is set to conserve. If the task always wants to converse power, it does not need to call this function at all.''',
						'paramValue': {'state': {
								'PWRMGR_CONSERVE': '''Turns power savings on, all tasks have to agree. This is the default state when a task is initialized.''',
								'PWRMGR_HOLD': '''Turns power savings off.''',
							}, },
					},
				'osal_snv_read': {
						'address': 0x00017B36,
						'calls': 'direct',
						'stacks': 'XSTACK',
						'storageClass': 'BANKED_CODE',
						'bank': 2,
						'size': 0x34, # bytes
						'segmentPart': 59,
						'relay': 0x00000B6C,
						'returnType': 'uint8',
						'paramTypes': ('osalSnvId_t', 'osalSnvLen_t', 'void*'),
						'paramNames': ('id', 'len', 'pBuf'),
						'description': '''Read data from NV. This function can be used to read an entire item from NV. Read data is copied into *pBuf.''',
						'paramDescription': (
							'''id - User-defined item ID''',
							'''len - Item length in bytes.''',
							'''*pBuf - Data is read into this buffer''',
						),
						'returnDescription': '''Return value indicates the result of the operation. Note that an attempt to read an item, which was never written before, would result into the NV_OPER_FAILED return code.''',
						'returnValue': {
							'SUCCESS': 'Success',
							'NV_OPER_FAILED': 'Operation failed',
						},
				},
				'osal_snv_write': {
					'address': 0x00017A18,
					'calls': 'direct',
					'stacks': 'XSTACK',
					'storageClass': 'BANKED_CODE',
					'bank': 2,
					'size': 0x108, # bytes
					'segmentPart': 55,
					'relay': 0x00000B66,
					'returnType': 'uint8',
					'paramTypes': ('osalSnvId_t', 'osalSnvLen_t', 'void*'),
					'paramNames': ('id', 'len', 'pBuf'),
					'description': '''Write data to NV. This function can be used to write an entire item to NV.''',
					'paramDescriptions': (
						'''id - User-defind item ID.''',
						'''len - Item length in bytes.'''
						'''*pBuf - Data to write.''',
						),
					'returnDescription': '''Return value indicates the result of the operation. Note that it is allowed to write an item that was never before initialized into the NV system by other means.''',
					'returnValue': { 
						'SUCCESS': 'success',
						'NV_OPER_FAILED': 'Operation failed',
					},
				},
				'osalTimeUpdate': {
						'address': 0x0001DAB0,
						'calls': 'direct',
						'stacks': 'XSTACK', 
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0xe8, # bytes
						'segmentPart': 13,
						'relay': 0x000007C4,
						'returnType': 'void',
						'paramTypes': (),
						'paramNames': (),
						'description': '''Called from osal_run_system() to update the time. This function reads the number of MAC 320usec ticks to maintain the OSAL Clock time. Do not call this function anywhere else.''',
				},
				'osal_rand': {
						'address': 0x00018EFB,
						'calls': 'direct',
						'stacks': 'ISTACK',
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x9, # bytes
						'segmentPart': 46,
						'relay': 0x0000075E,
						'returnType': 'uint16',
						'paramTypes': (),
						'paramNames': (),
						'description': '''This function returns a 16-bit random number''',
					},
				'osal_memcmp': {
						'address': 0x00018E7C,
						'stacks': 'XSTACK',
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x4a, # bytes
						'segmentPart': 24,
						'relay': 0x00000752,
						'returnType': 'uint16',
						'paramTypes': (),
						'paramNames': (),
					},
				'osal_memcmp': {
						'address': 0x00018E7C,
						'stacks': 'XSTACK',
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x4a, # bytes
						'segmentPart': 24,
						'relay': 0x00000752,
						'returnType': 'uint8',
						'paramTypes': ('const void GENERIC *', 'const void GENERIC *',
								'unsigned int'),
						'paramNames': ('src1', 'src2', 'len'),
						'description': 'Compare to memory sections.',
						'paramDescription': (
								'''src1 - memory compare location 1.''',
								'''src2 - memory compare location 2.''',
								'''len - length of compare''',
							),
						'returnDescription': 'TRUE - same, FALSE - different.',
					},
				'osal_memset': {
						'address': 0x00018EDA,
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x21, # bytes
						'segmentPart': 28,
						'calls': 'direct',
						'stacks': 'XSTACK',
						'relay': 0x00000758,
						'description': 'Sets a buffer to a specific value',
						'returnType': 'void*',
						'paramTypes': ('void*', 'uint8', 'int'),
						'paramNames': ('dest', 'value', 'len'),
						'paramDescriptions': (
							'dest - memory buffer to set "value" to.',
							'value - what to set each byte of "dest".'
							'len - length to set "value" in "dest".',
						),
						'returnDescription': 'Pointer to where in the buffer this function stopped.',
				},
				'osal_memcpy': {
						'address': 0x00018DC3,
						'storageClass': 'BANKED_CODE',
						'bank': 3,
						'size': 0x36, # bytes
						'segmentPart': 18,
						'stacks': ( 'XSTACK', 'ISTACK'),
						'relay': 0x00000740,
						'returnType': 'void*',
						'paramTypes': ('void*', 'const void GENERIC *',
							'unsigned int'),
						'paramNames': ('dst', 'src', 'len'),
						'description': 'Copies one buffer to another buffer',
						'paramDescription': (
							'dst - destination buffer',
							'src - source buffer',
							'len - length of copy',
						),
						'returnDescription': 'Pointer to end of destination buffer',
					},
		}

class API:
	def __init__(self, name, mcu):
		if not mcu._mapAPI.has_key(name):
			raise NameError("name %s not in map file" % name)
		self._name = name
		# look up the info
		self._info = mcu._mapAPI[name]
		self._mcu = mcu

	def appendCode(self, cap):
		'''a pass-through for code capsule operaton'''
		self._code.appendCode(cap)

	def emit(self, formatStr, *operands):
		self._code.emit(formatStr, *operands)

	def __call__(self, *param):
		'''this object is being *called* with the parameter.
				we need to check and typecast the parameters.
				Two phases:
				(1) we code-gen each item and pass as parameter, by
						allocating the designated parameter registers.
				(2) generate code to make the call, to the relay function if
						necessary.
				(3) generate code to fetch the return value, and
						free up the parameter registers.
		'''
		# generate code for passing parameters
		self.passParam(*param)
		# generate code for making the call
		self.makeCall()
		# generate code for fetching the return value
		self.grabReturnValue()
		return self._code

	def allocUint8Reg(self):
		'''This is a private method for allocating a register for uint8
			parameter
		'''
		if len(self.regAvail) == 0:
			raise ValueError('param register overflow - stack not implemented')
		regNum = self.regAvail.pop(0)
		self.uint8Stack.append(regNum)

	def popUint8Reg(self):
		return self.uint8Stack.pop()

	def allocBitReg(self):
		'''This is a private method for allocating a register for a
			boolean (bit) parameter
		'''
		if (len(self.boolStack) >= 8):
			raise ValueError('bit params overflow - VB not implemented')
		self.boolStack.append(len(self.boolStack))

	def popBitReg(self):
		'''This is a private method that does the reverse of allocBitReg
		   by popping it off the stack and return its number
		'''
		return self.boolStack.pop()

	def allocUint16Reg(self):
		if (3 in self.regAvail) and (2 in self.regAvail):
			# allocate them for param passing
			self.uint16Stack.append((2,3))
			self.regAvail.remove(2)
			self.regAvail.remove(3)
		elif (5 in self.regAvail) and (4 in self.regAvail):
			self.uint16Stack.append((4,5))
			self.regAvail.remove(4)
			self.regAvail.remove(5)
		else:
			raise ValueError('out of registers for passing uint16 param')

	def popUint16Reg(self):
		return self.uint16Stack.pop()
		# no need to replenish regAvail, because that is always
		# replenished by the next passParam

	def passParam(self, *paramList):
		'''this is the helper method to generate code to pass parameters
			to a function call. the paramList is essentially a list of
			code capsules. one issue is with the use of registers and
			accumulators. we could try to lock down parameter registers
			(but we would have no way to know at the time of code gen)
			but the surest way is to 
			- code-gen each param expression and push each onto stack before
				code-gen and push next, including bits too!
			- after pushing everything on stack, copy (and pop) each 
			  into the register(s). 
			The use of stack is what enables arbitrary expressions,
			including function call expressions, as parameter values.
			e.g., f(g(x+h(y))-i)
		'''
		paramTypes = self._info['paramTypes']
		paramNames = self._info['paramNames']
		if (len(paramTypes) != len(paramNames)):
			raise AttributeError('param type list and param name list mismatch')
		# now make sure we have the right number of actual parameters 
		# we don't (yet) support variable parameter list or passing by
		# name, but eventually we probably can.
		if len(paramList) != len(paramTypes):
			raise TypeError('parameter list mismatch: %d expected, %d passed' %\
					(len(paramTypes), len(paramList)))
		# check and convert type if necessary
		self._code = CodeCapsule(self._mcu)
		################# evaluate each parameter ##################
		# Now define some variables for register allocation for param
		# passing according to IAR's passing convention.  See the doc
		# EW8051_compilerreference.pdf phyisical page 167, logical page 135
		# 1-bit values: B.0,...B.7, VB.0, ..VB.7
		# 8-bit values: R1, ...R5
		# 16-bit values: R3:R2 or R5:R4.
		# 32-bit values: R5:R2
		# the rest are supposed to be pushed on stack.
		# order is strictly left to right.
		# registers are allocated on first-available, not most packed.
		self.boolStack = [ ]  # stack of boolean variables
		self.regAvail  = [ 1, 2, 3, 4, 5 ]  # registers available
		self.uint8Stack = [ ]  # register numbers in order allocated
		self.uint16Stack = [ ]  # tuples for register pairs allocated
		for (actual, formalType, formalName) in map(None, paramList, paramTypes, paramNames):
			# we check each parameter and (generate code to) push it on the
			# stack. Then we pop them to pass in the register(s).
			if isinstance(actual, int) or isinstance(actual, bool):
				# user passes an integer literal.
				# no need to generate code to evaluate them for now.
				# later, copy them directly to the registers involved.
				if formalType == 'uint8':
					# push takes a direct address. so need to put the imm in A,
					# and then push it as ACC.
					# self.emit('MOV A, #0x%x', actual)
					# self.emit('PUSH ACC')
					self.allocUint8Reg()
				elif formalType == 'bool':
					# the only thing is maybe check overflow
					if (actual < 0) or (actual > 1):
						raise ValueError('actual parameter %s overflows for boolean' \
								% actual)
					# self.emit('MOV A, #0x%x', actual)  # load literal value
					# self.emit('PUSH ACC')  # push value onto stack
					self.allocBitReg()

				elif formalType == 'uint16' or formalType[-1] == '*':
					# we treat (data) pointer as uint16.
					# Need to check if callback pointers can still work by passing the
					# address of the 16-bit relay.
					# push two bytes, little-endian byte order
					# use DPTR - saves one byte and a few cycles
					# self.emit('MOV DPTR, #0x%x', actual)
					# self.emit('PUSH DPL0') # we assume DPTR0
					# self.emit('PUSH DPH0') # we assume DPTR0
					# try R3:R2, then R5:R4
					self.allocUint16Reg()
				else:
					raise TypeError('actual parameter type int mismatches with formal parameter type %s' % formalType )

			elif isinstance(actual, CodeCapsule):
				actualType = actual.getResultType()
				if actualType == 'bool':
					# if bit, push entire Carry. somewhat wasteful but it's a
					# price to pay
					if formalType == 'bool':
						self.appendCode(actual)
						self.emit('PUSH PSW')
						self.allocBitReg()
					elif formalType == 'uint8':
						# should convert boolean to a byte. Clear A and rotate C in.
						self.appendCode(actual) # assume actual's code puts it into C
						self.emit('CLR A')  # set A = 0
						self.emit('RLC')    # rotate C into A.0
						self.emit('PUSH ACC')
						self.allocUint8Reg()
					else:
						raise TypeError("passing %s to %s param unsupported" %\
								(actualType, formalType))
				elif actualType == 'uint8':
					if formalType == 'uint8':
						self.appendCode(actual)
						self.emit('PUSH ACC')  # for now, but should push _dest??
						self.allocUint8Reg()
					else:
						# if formalType == 'bool':
							# we could convert this to boolean? based on zero or
							# nonzero? but for now we don't allow it. can always do
							# != 0 to force conversion.
						raise TypeError("passing %s to %s param unsupported" %\
								(actualType, formalType))
				elif actualType == 'uint16' or actualType[-1] == '*':
					# where do we put the two bytes?
					pass
				else:
					raise TypeError("passing %s as %s param unsupported" % \
									(actualType, formalType))
			else:
				raise ValueError("cannot pass %s as parameter" % type(actual))
		################# now pop the parameters to reg ##################
		F = paramTypes[-1::-1]
		A = paramList[-1::-1]
		for (formalType, actual) in map(None, F, A):
			# pop the parameter
			if formalType == 'bool':
				regNum = self.popBitReg()
				if isinstance(actual, CodeCapsule):
					# pop back to ACC, rotate into CY, then 
					self.emit('POP ACC') # pop whole PSW back into A
					self.emit('RRC')     # rotate right to get A.0 into C 
					self.emit('MOV B.%d, C', self.popBitReg())
				elif isinstance(actual, bool) and (actual == True) or \
						isinstance(actual, int) and (actual == 1):
					# literal value 1 or True
					self.emit('SETB B.%d', regNum)
				elif isinstance(actual, bool) and (actual == False) or \
						isinstance(actual, int) and (actual == 0):
					# literal value 0 or False
					self.emit('CLR B.%d', regNum)
				else:
					# probably out of range?
					raise ValueError('%s not valid boolean param' % actual)
			elif formalType == 'uint8':
				regNum = self.popUint8Reg()
				if isinstance(actual, CodeCapsule):
					self.emit('POP 0x%x', regNum)
				elif isinstance(actual, int) or isinstance(actual, bool):
					actual = int(actual)
					# should probably check out of range
					self.emit('MOV R%d, #0x%x', regNum, actual)
				else:
					raise ValueError('%s not valid uint8 param' % actual)
				# assume we use only register bank zero! 
				# this allows us to pop directly into the register's direct
				# address, because we can't pop into just a register.
			elif formalType == 'uint16' or formalType[-1] == '*':
				# similar to unit8 except we need to do two bytes.
				higher, lower = self.popUint16Reg()
				if isinstance(actual, CodeCapsule):
					self.emit('POP 0x%x', higher)
					self.emit('POP 0x%x', lower)
				elif isinstance(actual, int) or isinstance(actual, bool):
					actual = int(actual)
					self.emit('MOV R%d, #0x%x', higher, (actual >> 8) & 0xff)
					self.emit('MOV R%d, #0x%x', lower, actual & 0xff)
				else:
					raise ValueError('%s not valid uint16 param' % actual)
			else:
				raise TypeError("param type %s not supported" % formalType)

	def makeCall(self):
		'''make either a direct call or call the relay function'''
		if self._info.has_key('relay'):
			# make a call to relay function
			self.emit('LCALL 0x%x', self._info['relay'])
		else:
			# make a direct call to its address
			self.emit('LCALL 0x%x', self._info['address'])


	def grabReturnValue(self):
		'''
		12/20/2013: This method should be changed in the following ways:
		- it should set the return type in CodeCapsule but not generate
		  the code to grab return value -- CodeCapsule should do that.
		- this method should, however, move 8-bit return value from R1 to A.
		  this is assumed by everyone else.
		- It would be nice to have a code optimization pass so we can eliminate
		  unnecessary copying, but this would require knowing basic blocks.

		this method generates the code that immediately follows the
		LCALL instruction. it should grab the return value and put it
		into the return buffer.
		See Table 31, page 137 of the EW8051_compilerreference document.
		we assume little endian here , which is not external stack.
		1-bit value: C
		8-bit value: R1
		16-bit value: R3:R2
		24-bit value: R3:R2:R1
		32-bit value: R5:R4:R3:R2
    Our format:
		[length][byte 0][byte 1][byte 2][byte 3]
		'''
		t = self._info['returnType']
		self._code.setResultType(t)
		if (t == 'uint8'):
			self.emit('MOV A, R1')
