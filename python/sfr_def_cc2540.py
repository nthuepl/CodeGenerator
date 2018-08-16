#
# sfr_def_cc2540.py
#
# this is the sfr definition class for the TI CC2540 MCU.
# It is extracted, so that different code generators (C or assembly)
# can reuse it.  Also, the naming convention is we group all sfr
# definitions with the sfr_defn prefix.
#
class SFR_DEF_CC2540:
	'''
		This class SFR_DEF_CC2540 is just a container for two static hash
		tables of hash tables of stuff to provide the SFR definitions:
		one for all the SFRs and one for XREG.
	'''

	# CC2540's special function registers.  The data is taken from the
	# data sheet "swru191d.pdf", page 29-, Table 2-1 "SFR Overview"

	_SFR = {
			################ ADC ##############
			'ADCCON1': {
					'address': 0xB4, 'module': 'ADC',
					'description': 'ADC control 1',
					'bitfields': {
							'EOC': {
									'slice': (7,),
									'default': 0, 'access': 'R/H0',
									'description': '''End of conversion. Cleared when ADCH has been read. If a new conversion is completed before the previous data has been read, the EOC bit remains high.
0: Conversion not complete
1: Conversion completed''',
							},
							'ST': {
									'slice': (6,),
									'default': 0, 'access': 'R/W1/H0',
									'description': '''Start conversion. Read as 1 until conversion has completed.
0: No conversion in progress
1: Start a conversion sequence if ADCCON1.STSEL = 11 and no sequence
is running.''',
							},
							'STSEL': {
									'slice': (5,4),
									'default': 0b11, 'access': 'R/W',
									'description': '''Start select. Selects the event that starts a new conversion sequence
00: External trigger on P20 pin
01: Full speed. Do not wait for triggers
10: Timer 1 channel 0 compare event
11: ADCCON1.ST = 1''',
							},
							'RTCRL': {
									'slice': (3,2), 'default': 0, 'access': 'R/W',
									'description': '''Controls the 16-bit random-number generator. When 01 is written, the setting automatically returns to 00 when the operation has completed.
00: Normal operation. (13x unrolling)
01: Clock the LFSR once (13x unrolling)
10: Reserved
11: Stopped. Random-number generator is turned off. ''',
							},
							'-reserved2': {
								'slice': (1,0), 'default': 0b11, 'access': 'R/W',
								'description': 'Reserved. Always set to 11',
							},
					},
				},
			'ADCCON2': {
					'address': 0xB5, 'module': 'ADC', 'description': 'ADC control 2',
					'bitfields': {
							'SREF': {
									'slice': (7,6), 'default': 0, 'access': 'R/W',
									'description': '''Selects reference voltage used for the sequence of conversions
00: Internal reference',
01: External reference on AIN7 pin
10: ADD5 pin
11: External reference on AIN6-AIN7 differential input''',
							},
							'SDIV': {
									'slice': (5,4), 'default': 0b01, 'access': 'R/W',
									'description': '''Sets the decimation rate for channels included in the sequence of conversions.  The decimation rate also determines the resolution and time required to complete a conversion.
00: 64 decimation rate (7 bits ENOB setting)
01: 128 decimation rate (9 bits ENOB setting)
10: 256 decimation rate (10 bits ENOB setting)
11: 512 decimation rate (12 bits ENOB setting)''',
							},
							'SCH': {
									'slice': (3,0), 'default': 0, 'access': 'R/W',
									'description': '''Sequence channel select. Selects the end of the sequence. A sequence can either be from AIN0 to AIN7 (SCH <= 7) or from differential input AIN0-AIN1 to AIN6-AIN7 (8 <= SCH <= 11). For other settings, only one conversion is performed.
When read, these bits indicate the channel number on which a conersion
is ongoing.
0000: AIN0
0001: AIN1
0010: AIN2
0011: AIN3
0100: AIN4
0101: AIN5
0110: AIN6
0111: AIN7
1000: AIN0-AIN1
1001: AIN2-AIN3
1010: AIN4-AIN5
1011: AIN6-AIN7
1100: GND
1101: Reserved
1110: Temperature sensor
1111: VDD/3''',
							},
					}, },
			'ADCCON3': {
					'address': 0xB6, 'module': 'ADC', 'description': 'ADC control 3',
					'bitfields': {
							'EREF': {
									'slice': (7,6), 'default': 0, 'access': 'R/W',
									'description': '''Selects reference voltage used for the extra conversion
00: Internal reference',
01: External reference on AIN7 pin
10: ADD5 pin
11: External referenceo n AIN6-AIN7 differential input''',
							},
							'EDIV': {
									'slice': (5,4), 'default': 0, 'access': 'R/W',
									'description': '''Sets the decimation rate for extra conversion.  The decimation rate also determines the resolution and time required to complete a conversion.
00: 64 decimation rate (7 bits ENOB setting)
01: 128 decimation rate (9 bits ENOB setting)
10: 256 decimation rate (10 bits ENOB setting)
11: 512 decimation rate (12 bits ENOB setting)''',
							},
							'ECH': {
									'slice': (3,0), 'default': 0, 'access': 'R/W',
									'description': '''Single channel select. Selects the channel number of the single conversion that is triggered by writing to ADCCON3.
0000: AIN0
0001: AIN1
0010: AIN2
0011: AIN3
0100: AIN4
0101: AIN5
0110: AIN6
0111: AIN7
1000: AIN0-AIN1
1001: AIN2-AIN3
1010: AIN4-AIN5
1011: AIN6-AIN7
1100: GND
1101: Reserved
1110: Temperature sensor
1111: VDD/3''',
							},
					},
				},
			'ADCL': {
					'address': 0xBA, 'module': 'ADC', 'description': 'ADC data low',
					'bitfields': {
							'ADC5_0': {
									'slice': (7,2), 'default': 0, 'access': 'R',
									'description': 'Least-significant part of ADC conversion result',
							},
							'-reserved': {
								'slice': (1,0), 'default': 0, 'access': 'R0',
								'description': 'Reserved. Always read as 0',
							},
					},
				},
			'ADCH': {
					'address': 0xBB, 'module': 'ADC',
					'default': 0, 'access': 'R',
					'description': 'ADC data high',
				},
			############# Random number generator part of ADC #############
			'RNDL': {
					'address': 0xBC, 'module': 'ADC',
					'default': 0xFF, 'access': 'R/W',
					'description': 'Random number generator data low. Random value/seed or CRC result, lower byte. When used for random-number generation, writing to this register twice seeds the random-number generator. Writing to this register copies the 8 LSBs of the LFSR to the 8 MSBs and replaces the 8 LSBs with the data value written. The value returned when reading from this register is the 8 LSBs of the LFSR. When used for random-number generation, reading this register returns the 8 LSBs of the random number. When used for CRC calculations, reading this register returns the 8 LSBs of the CRC result',
				},
			'RNDH': {
					'address': 0xBD, 'module': 'ADC',
					'default': 0xFF, 'access': 'R/W',
					'description': 'Random number generator data high. Random value/seed or CRC result, high byte. When written, a CRC16 calculation is triggered, and the data value written is processed starting with the MSB. The value returned when reading from this register is the 8 MSBs of the LFSR. When used for random-number generation, reading this register returns the 8 MSBs of the random number. When used for CRC calculations, reading this register returns the 8 MSBs of the CRC result.',
				},
			################### AES #####################
			'ENCDI': {
					'address': 0xB1, 'module': 'AES',
					'default': 0, 'access': 'R/W',
					'description':'Encryption/decryption input data'
				},
			'ENCDO': {
					'address': 0xB2, 'module': 'AES',
					'default': 0, 'access': 'R/W',
					'description':'Encryption/decryption output data'
				},
			'ENCCS': {
					'address': 0xB3, 'module': 'AES',
					'description':'Encryption/decryption control and status',
					'bitfields': {
							'-reserved': {
									'slice': (7,), 'default': 0, 'access': 'R0',
									'description': 'Reserved, always read as 0',
							},
							'MODE': {
									'slice': (6,4), 'default': 0, 'access': 'R/W',
									'description': '''Encryption/decryption mode
000: CBC
001: CFB
010: OFB
011: CTR
100: ECB
101: CBC MAC
110: Reserved
111: Reserved''',
							},
							'RDY': {
									'slice': (3,), 'default': 1, 'access': 'R',
									'description': '''Encryption/decryption ready status
0: Encryption/decryption in progress
1: Encryption/decryption is completed.''',
							},
							'CMD': {
									'slice': (2,1), 'default': 0, 'access': 'R/W',
									'description': '''Command to be performed when a 1 is written to ST
00: Encrypt block
01: Decrypt block
10: Load key
11: Load IV/nonce''',
							},
							'ST': {
										'slice': (0,), 'default': 0, 'access': 'R/W1 H0',
										'description': 'Start processing command set by CMD. Must be issued for each command or 128-bit block of data. Cleared by hardware.',
							},
					},
				},
			############### GPIO ##################
			'P0': {
					'address': 0x80, 'module': 'CPU',
					'xaddress': 0x7080, 'default': 0xFF, 'access': 'R/W',
					'bitfields': { },
					'description': 'Port 0. General-purpsoe I/O port.  Bit-addressable from SFR. This CPU-internal register is readable, but not writable, from XDATA (0x7080).',
				},
			'P1': {
					'address': 0x90, 'module': 'CPU', 'description': 'Port 1',
					'xaddress': 0x7090,'default': 0xFF, 'access': 'R/W',
					'bitfields': { },
					'description': 'Port 1. General-purpsoe I/O port.  Bit-addressable from SFR. This CPU-internal register is readable, but not writable, from XDATA (0x7090).',
				},
			'P2': {
					'address': 0xA0, 'module': 'CPU', 'description': 'Port 2',
					'xaddress': 0x70A0,
					'bitfields': {
							'--reserved': {
									'slice': (7,5), 'default': 0x0, 'access': 'R0',
									'description': 'Reserved',
							},
							'_4': {
									'slice': (4,), 'default': 1, 'access': 'R/W',
							},
							'_3': {
									'slice': (3,), 'default': 1, 'access': 'R/W',
							},
							'_2': {
									'slice': (2,), 'default': 1, 'access': 'R/W',
							},
							'_1': {
									'slice': (1,), 'default': 1, 'access': 'R/W',
							},
							'_0': {
									'slice': (0,), 'default': 1, 'access': 'R/W',
							},
					},
				},
			'SP': {
					'address': 0x81, 'module': 'CPU', 'description': 'Stack pointer',
					'default': 0x07, 'access': 'RW',
				},
			'DPL0': {
					'address': 0x82, 'module': 'CPU',
					'description': 'Data pointer 0 low byte',
				},
			'DPH0': {
					'address': 0x83, 'module': 'CPU',
					'description': 'Data pointer 0 high byte',
					'default': 0x00, 'access': 'RW',
				},
			'DPL1': {
					'address': 0x84, 'module': 'CPU',
					'description': 'Data pointer 1 low byte',
					'default': 0x00, 'access': 'RW',
				},
			'DPH1': {
					'address': 0x85, 'module': 'CPU',
					'description': 'Data pointer 1 high byte',
					'default': 0x00, 'access': 'RW',
				},
			'PCON': {
					'address': 0x87, 'module': 'CPU',
					'description': 'Power mode control',
					'default': 0x00,
					'bitfields': {
						'-reserved': {
							'slice': (7,1), 'description': 'Reserved, always write as 0000 000',
							'access': 'R/W',
						},
						'IDLE': {
							'slice': (0,), 'access': 'R0/W H0',
							'description': 'Power mode control.  Writing 1 to this bit forces the device to enter the power mode set by SLEEPCMD.MODE (note that MODE=0x00 AND IDLE = 1 stops the CPU core activity). This bit is always read as 0. All enabled interrupts clear this bit when active, and the device re-enters active mode.'
						},
					},
				},
			'TCON': {
					'address': 0x88, 'module': 'CPU',
					'description': 'Interrupt flags',
					'default': 0x05,
					'bitfields': {
							'URX1IF': {
								'slice': (7,), 'access': 'R/W H0',
								'description': 'USART 1 Rx interrupt flag. set to 1 when USART 1 Rx interrupt occurs and cleared when CPU vectors to the interrupt service routine.'
							},
							'-reserved1': {
								'slice': (6,), 'access': 'R/W',
								'description': 'Reserved'
							},
							'ADCIF': {
								'slice': (5,), 'access': 'R/W H0',
								'description': 'ADC interrupt flag. set to 1 when ADC interrupt occurs and cleared when CPU vectors to the interrupt service routine.'
							},
							'-reserved2': {
								'slice': (4,), 'access': 'R/W',
								'description': 'Reserved'
							},
							'URX0IF': {
								'slice': (3,), 'access': 'R/W H0',
								'description': 'USART 0 Rx interrupt flag. set to 1 when USART 0 Rx interrupt occurs and cleared when CPU vectors to the interrupt service routine.'
							},
							'IT1': {
								'slice': (2,), 'access': 'R/W',
								'description': 'Reserved. Must always be set to 1.  Setting a zero enables low-leel interrupt detection, which is almost always the case (one-shot when interrupt request is initiated.',
							},
							'RFERRIF': {
								'slice': (1,), 'access': 'R/W H0',
								'description': 'RF core error interruptflag. Set to 1 when RFERR interrupt occurs and cleared when CPU vectors to the interrupt service routine.',
							},
							'IT0': {
								'slice': (0,), 'access': 'R/W',
								'description': 'Reserved. Must always be set to 1.  Setting a zero enables low-leel interrupt detection, which is almost always the case (one-shot when interrupt request is initiated.',
							},
					},
				},
			'DPS': {
					'address': 0x92, 'module': 'CPU',
					'description': 'Data pointer select',
					'default': 0x00,
					'bitfields': {
							'-reserved': {'slice': (7,1), 'access': 'R',
								'description': 'Reserved'
							},
							'DPS': {'slice': (0,), 'acccess': 'RW',
								'description': 'Data pointer select. Selects active data pointer. 0: DPTR0. 1: DPTR1.'
							},
						},
				},
			'S0CON': {
					'address': 0x98, 'module': 'CPU',
					'description': 'Interrupt flags 2',
					'access': 'R/W',
					'default': 0x00,
					'bitfields': {
						'-reserved': { 'slice': (7,2), 'description': 'Reserved'},
						'ENCIF_1': {
								'slice': (1,),
								'description': 'AES interrupt. ENC has two interrupt flags, ENCIF_1 and ENCIF_0. Setting one of these flags requests interrupt service. Both flags are set when the AES coprocessor requests the interrupt. 0: interrupt not pending. 1: interrupt pending.'
							},
						'ENCIF_0': {
								'slice': (0,),
								'description': 'AES interrupt. ENC has two interrupt flags, ENCIF_1 and ENCIF_0. Setting one of these flags requests interrupt service. Both flags are set when the AES coprocessor requests the interrupt. 0: interrupt not pending. 1: interrupt pending.'
							},
					},
				},
			'IEN2': {
					'address': 0x9A, 'module': 'CPU',
					'description': 'Interrupt enable 2',
					'default': 0x00,
					'bitfields': {
							'-reserved': {
								'slice': (7,6), 'access': 'R0',
								'description': 'Reserved. Read as 0',
							},
							'WDTIE': {
								'slice': (5,), 'access': 'R/W',
								'description': 'Watchdog Timer interrupt enable'
							},
							'P1IE': {
								'slice': (4,), 'access': 'R/W',
								'description': 'Port 1 interrupt enable'
							},
							'UTX1IE': {
								'slice': (3,), 'access': 'R/W',
								'description': 'USART 1 Tx interrupt enable',
							},
							'UTX0IE': {
								'slice': (2,), 'access': 'R/W',
								'description': 'USART 0 Tx interrupt enable',
							},
							'P2IE': {
								'slice': (1,), 'access': 'R/W',
								'description': 'Port 2 and USB interrupt enable',
							},
							'RFIE': {
								'slice': (0,), 'access': 'R/W',
								'description': 'RF general interrupt enable',
							},
						},
				},
			'S1CON': {
					'address': 0x9B, 'module': 'CPU',
					'description': 'Interrupt flags 3',
					'access': 'R/W',
					'default': 0x00,
					'bitfields': {
						'-reserved': { 'slice': (7,2), 'description': 'Reserved'},
						'ENCIF_1': {
								'slice': (1,),
								'description': 'RF general interrupt. RF has two interrupt flags, RFIF_1 and RFIF_0. Setting one of these flags requests interrupt service. Both flags are set when the radio requests the interrupt. 0: interrupt not pending. 1: interrupt pending.'
							},
						'ENCIF_0': {
								'slice': (0,),
								'description': 'RF general interrupt. RF has two interrupt flags, RFIF_1 and RFIF_0. Setting one of these flags requests interrupt service. Both flags are set when the radio requests the interrupt. 0: interrupt not pending. 1: interrupt pending.'
							},
					},
				},
			'IEN0': {
					'address': 0xA8, 'module': 'CPU',
					'description': 'Interrupt enable 0',
					'bitfields': {
							'EA': { 'slice': (7,), 'access': 'R/W',
									'description': 'Disable all interrupts. 0: no interrupt is acknowledged. 1: Each interrupt source is individually enabled or disabled by setting its corresponding enable bit.' },
							'-reserved': { 'slice': (6,), 'access': 'R0',
									'description': 'Reserved. Read as 0.'},
							'STIE': { 'slice': (5,), 'access': 'R/W',
									'description': 'Sleep Timer Interrupt enable. 0: Interrupt disabled. 1: interrupt enabled.'},
							'ENCIE': { 'slice': (4,), 'access': 'R/W',
									'description': 'AES encryption/decryption interrupt enable'},
							'URX1IE': { 'slice': (3,), 'access': 'R/W',
									'description': 'USART 1 Rx interrupt enable'},
							'URX0IE': { 'slice': (2,), 'access': 'R/W',
									'description': 'USART 0 Rx interrupt enable'},
							'ADCIE': { 'slice': (1,), 'access': 'R/W',
									'description': 'ADC interrupt enable'},
							'RFERRIE': { 'slice': (0,), 'access': 'R/W',
									'description': 'RF core error interrupt enable'},
						}
				},
			'IP0': {
					'address': 0xA9, 'module': 'CPU',
					'description': 'Interrupt priority 0',
					'default': 0x00, 'access': 'R/W',
					'bitfields': {
							'-reserved': {
									'slice': (7,6), 'description': 'Reserved',
							},
							'IP0_IPG5': {
								'slice': (5,), 'description': 'Interrupt group 5, priority control bit 0',
							},
							'IP0_IPG4': {
								'slice': (4,), 'description': 'Interrupt group 4, priority control bit 0',
							},
							'IP0_IPG3': {
								'slice': (3,), 'description': 'Interrupt group 3, priority control bit 0',
							},
							'IP0_IPG2': {
								'slice': (2,), 'description': 'Interrupt group 2, priority control bit 0',
							},
							'IP0_IPG1': {
								'slice': (1,), 'description': 'Interrupt group 1, priority control bit 0',
							},
							'IP0_IPG0': {
								'slice': (0,), 'description': 'Interrupt group 0, priority control bit 0',
							},
					},
				},
			'IEN1': {
					'address': 0xB8, 'module': 'CPU',
					'description': 'Interrupt enable 1',
					'default': 0x00,
					'bitfields': {
							'-reserved': {
								'slice': (7,6), 'access': 'R0',
								'description': 'Reserved. Read as 0',
								},
							'P0IE': {
								'slice': (5,), 'access': 'R/W',
								'description': 'Port 0 interrupt enable',
								},
							'T4IE': {
								'slice': (4,), 'access': 'R/W',
								'description': 'Timer 4 interrupt enable',
								},
							'T3IE': {
								'slice': (3,), 'access': 'R/W',
								'description': 'Timer 3 interrupt enable',
								},
							'T2IE': {
								'slice': (2,), 'access': 'R/W',
								'description': 'Timer 2 interrupt enable',
								},
							'T1IE': {
								'slice': (1,), 'access': 'R/W',
								'description': 'Timer 1 interrupt enable',
								},
							'DMAIE': {
								'slice': (0,), 'access': 'R/W',
								'description': 'DMA transfer interrupt enable',
								},
						},
				},
			'IP1': {
					'address': 0xB9, 'module': 'CPU',
					'description': 'Interrupt priority 1',
					'default': 0x00, 'access': 'R/W',
					'bitfields': {
						'-reserved': {
							'slice': (7,6), 'description': 'Reserved',
						},
						'IP1_IPG5': {
							'slice': (5,), 'description': 'Interrupt group 5, priority control bit 1',
						},
						'IP1_IPG4': {
							'slice': (4,), 'description': 'Interrupt group 4, priority control bit 1',
						},
						'IP1_IPG3': {
							'slice': (3,), 'description': 'Interrupt group 3, priority control bit 1',
						},
						'IP1_IPG2': {
							'slice': (2,), 'description': 'Interrupt group 2, priority control bit 1',
						},
						'IP1_IPG1': {
							'slice': (1,), 'description': 'Interrupt group 1, priority control bit 1',
						},
						'IP1_IPG0': {
							'slice': (0,), 'description': 'Interrupt group 0, priority control bit 1',
						},
					}
				},
			'IRCON': {
					'address': 0xC0, 'module': 'CPU',
					'description': 'Interrupt flags 4',
					'default': 0x00,
					'bitfields': {
							'STIF': {
								'slice': (7,), 'access': 'R/W',
								'description': 'Sleep Timer interrupt flag: 0.  interrupt not pending, 1: interrupt pending',
							},
							'-reserved': {
								'slice': (6,), 'access': 'R/W',
								'description': 'Must be written 0. Writing a 1 always enables the interrupt source.',
							},
							'P0IF': {
								'slice': (5,), 'access': 'R/W',
								'description': 'Port 0 interrupt flag. 0: interrupt not pending. 1: interrupt pending.'
							},
							'T4IF': {
								'slice': (4,), 'access': 'R/W H0',
								'description': 'Timer 4 interrupt flag. Set to 1 when Timer 4 interrupt occurs and cleared when CPU vectors to the interrupt service routine. 0: interrupt not pending. 1: interrupt pending.'
							},
							'T3IF': {
								'slice': (3,), 'access': 'R/W H0',
								'description': 'Timer 3 interrupt flag. Set to 1 when Timer 3 interrupt occurs and cleared when CPU vectors to the interrupt service routine. 0: interrupt not pending. 1: interrupt pending.'
							},
							'T2IF': {
								'slice': (2,), 'access': 'R/W H0',
								'description': 'Timer 2 interrupt flag. Set to 1 when Timer 2 interrupt occurs and cleared when CPU vectors to the interrupt service routine. 0: interrupt not pending. 1: interrupt pending.'
							},
							'T1IF': {
								'slice': (1,), 'access': 'R/W H0',
								'description': 'Timer 1 interrupt flag. Set to 1 when Timer 1 interrupt occurs and cleared when CPU vectors to the interrupt service routine. 0: interrupt not pending. 1: interrupt pending.'
							},
							'DMAIF': {
								'slice': (0,), 'access': 'R/W',
								'description': 'DMA-complete interrupt flag. 0: interrupt not pending. 1: interrupt pending'
							},
					},
				},
			'PSW': {
					'address': 0xD0, 'module': 'CPU',
					'description': 'Program status Word',
					'access': 'RW', 'default': 0x00,
					'bitfields': {
							'CY': {'slice': (7,)},
							'AC': {'slice': (6,)},
							'F0': {'slice': (5,)},
							'RS': {'slice': (4,3), 'descripton': 'Register bank select bits. Selects which set of R7-R0 registers to use from four possible banks in DATA space. 00: Register bank 0, 0x00-0x07. 01: Register bank 1, 0x08-0x0F. 10: Register bank 2, 0x10-0x17. 11: Register bank 3, 0x18-0x1F.'},
							'OV': {'slice': (2,), 'description': 'Overflow flag, set by arithmetic operations. Set to 1 when the last arithmetic operation is a carry (addition), borrow (subtraction), or overflow (multiply or divide).  Otherwise, the bit is cleared to 0 by all arithmetic operations.'},
							'F1': {'slice': (1,), 'description': 'User-defined, bit-addressable'},
							'P':  {'slice': (0,), 'description': 'Parity flag, parity of accumulator set by hardware to 1 if it contains an odd number of 1s; otherwise it is cleared to 0'},
					},
				},
			'ACC': {
					'address': 0xE0, 'module': 'CPU',
					'description': 'Accumulator',
					'bitfields': { },  ## bit addressable by bit index
				},
			'IRCON2': {
					'address': 0xE8, 'module': 'CPU',
					'description': 'Interrupt flags 5',
					'default': 0x00, 'access': 'R/W',
					'bitfields':  {
							'-reserved': {
								'slice': (7,5), 'description': 'Reserved'
							},
							'WDTIF': {
								'slice': (4,),
								'description': 'Watchdog Timer interrupt flag. 0: interrupt not pending. 1: interrupt pending',
							},
							'P1IF': {
								'slice': (3,),
								'description': 'Port 1 interrupt flag',
							},
							'UTX1IF': {
								'slice': (2,),
								'description': 'USART 1 Tx interrupt flag',
							},
							'UTX0IF': {
								'slice': (1,),
								'description': 'USART 0 Tx interrupt flag',
							},
							'P2IF': {
								'slice': (0,),
								'description': 'Port 2 interrupt flag',
							},
					},
				},
			'B': {
					'address': 0xF0, 'module': 'CPU',
					'description': 'B register',
					'bitfields': { }, ## bit addressable by bit index
				},
			################ DMA SFRs #################
			'DMAIRQ': {
					'address': 0xD1, 'module': 'DMA',
					'description': 'DMA interrupt flag',
					'default': 0,
					'bitfields': {
							'-reserved': {
									'slice': (7,5), 'access': 'R0',
									'description': 'Reserved',
							},
							'DMAIF4': {
									'slice': (4,), 'access': 'R/W0',
									'description': '''DMA channel-4 interrupt flag
0: DMA channel transfer not complete
1: DMA channel transfer complete/interrupt pending''',
							},
							'DMAIF3': {
									'slice': (3,), 'access': 'R/W0',
									'description': '''DMA channel-3 interrupt flag
0: DMA channel transfer not complete
1: DMA channel transfer complete/interrupt pending''',
							},
							'DMAIF2': {
									'slice': (2,), 'access': 'R/W0',
									'description': '''DMA channel-2 interrupt flag
0: DMA channel transfer not complete
1: DMA channel transfer complete/interrupt pending''',
							},
							'DMAIF1': {
									'slice': (1,), 'access': 'R/W0',
									'description': '''DMA channel-1 interrupt flag
0: DMA channel transfer not complete
1: DMA channel transfer complete/interrupt pending''',
							},
							'DMAIF0': {
									'slice': (0,), 'access': 'R/W0',
									'description': '''DMA channel-0 interrupt flag
0: DMA channel transfer not complete
1: DMA channel transfer complete/interrupt pending''',
							},

					},
				},
			'DMA1CFGL': {
					'address': 0xD2, 'module': 'DMA',
					'description': 'DMA channel 1-4 configuration address low',
					'default': 0, 'access': 'R/W',
				},
			'DMA1CFGH': {
					'address': 0xD3, 'module': 'DMA',
					'description': 'DMA channel 1-4 configuration address high',
					'default': 0, 'access': 'R/W',
				},
			'DMA0CFGL': {
					'address': 0xD4, 'module': 'DMA',
					'description': 'DMA channel 0 configuration address low',
					'default': 0, 'access': 'R/W',
				},
			'DMA0CFGH': {
					'address': 0xD5, 'module': 'DMA',
					'description': 'DMA channel 0 configuration address high',
					'default': 0, 'access': 'R/W',
				},
			'DMAARM': {
					'address': 0xD6, 'module': 'DMA',
					'description': 'DMA channel armed',
					'default': 0,
					'bitfields': {
							'ABORT': {
								'slice': (7,), 'access': 'R0/W',
								'description': 'DMA abort. The bit is used to stop ongoing DMA transfers. Writing a 1 to this bit aborts all channels which are selected by setting the corresponding DMAARM bit to 1. 0: Normal operation. 1: Abort all selected channels.',
								},
							'-reserved': {
									'slice': (6,5), 'access': 'R/W',
									'description': 'Reserved',
							},
							'DMAARM4': {
									'slice': (4,), 'access': 'R/W1',
									'description': 'DMA arm channel 4. This bit must be set in order for ay DMA transfers to occur on the channel. For nonrepetitive transfer modes, the bit is automatically cleared on completion.',
							},
							'DMAARM3': {
									'slice': (3,), 'access': 'R/W1',
									'description': 'DMA arm channel 3. This bit must be set in order for ay DMA transfers to occur on the channel. For nonrepetitive transfer modes, the bit is automatically cleared on completion.',
							},
							'DMAARM2': {
									'slice': (2,), 'access': 'R/W1',
									'description': 'DMA arm channel 2. This bit must be set in order for ay DMA transfers to occur on the channel. For nonrepetitive transfer modes, the bit is automatically cleared on completion.',
							},
							'DMAARM1': {
									'slice': (1,), 'access': 'R/W1',
									'description': 'DMA arm channel 1. This bit must be set in order for ay DMA transfers to occur on the channel. For nonrepetitive transfer modes, the bit is automatically cleared on completion.',
							},
							'DMAARM0': {
									'slice': (0,), 'access': 'R/W1',
									'description': 'DMA arm channel 0. This bit must be set in order for ay DMA transfers to occur on the channel. For nonrepetitive transfer modes, the bit is automatically cleared on completion.',
							},
					},
				},
			'DMAREQ': {
					'address': 0xD7, 'module': 'DMA',
					'description': 'DMA channel start request and status',
					'default': 0,
					'bitfields': {
							'-reserved': {
								'slice': (7,5), 'access': 'R0',
								'description': 'Reserved',
							},
							'DMAREQ4': {
									'slice': (4,), 'access': 'R/W1 H0',
									'description': 'DMA transfer request, channel 4.  When set to 1, activate the DMA channel (has the same effect as a single trigger event). This bit is cleared when DMA transfer is started',
							},
							'DMAREQ3': {
									'slice': (3,), 'access': 'R/W1 H0',
									'description': 'DMA transfer request, channel 3.  When set to 1, activate the DMA channel (has the same effect as a single trigger event). This bit is cleared when DMA transfer is started',
							},
							'DMAREQ2': {
									'slice': (2,), 'access': 'R/W1 H0',
									'description': 'DMA transfer request, channel 2.  When set to 1, activate the DMA channel (has the same effect as a single trigger event). This bit is cleared when DMA transfer is started',
							},
							'DMAREQ1': {
									'slice': (1,), 'access': 'R/W1 H0',
									'description': 'DMA transfer request, channel 1.  When set to 1, activate the DMA channel (has the same effect as a single trigger event). This bit is cleared when DMA transfer is started',
							},
							'DMAREQ0': {
									'slice': (0,), 'access': 'R/W1 H0',
									'description': 'DMA transfer request, channel 0.  When set to 1, activate the DMA channel (has the same effect as a single trigger event). This bit is cleared when DMA transfer is started',
							},

					},
				},
			############## Reserved ##############
			'-reservedSFR1': {
					'address': 0xAA, 'module': '--',
					'description': 'Reserved',
				},
			'-reservedSFR2': {
					'address': 0x8E, 'module': '--',
					'description': 'Reserved',
				},
			'-reservedSFR3': {
					'address': 0x99, 'module': '--',
					'description': 'Reserved',
				},
			'-reservedSFR4': {
					'address': 0xB0, 'module': '--',
					'description': 'Reserved',
				},
			'-reservedSFR5': {
					'address': 0xB7, 'module': '--',
					'description': 'Reserved',
				},
			'-reservedSFR6': {
					'address': 0xC8, 'module': '--',
					'description': 'Reserved',
				},
			############ I/O Controller ###############
			'P0IFG': {
					'address': 0x89, 'module': 'IOC',
					'description': 'Port 0 interrupt status flag',
					'bitfields': {
						'P0IF': {
							'slice': (7,0), 'default': 0, 'access': 'R/W',
							'description': 'Port 0, inputs 7 to 0 interrupt status flags. When an input port pin has an interrupt request pending, the corresponding flag bit is set.'
						},
					},
				},
			'P1IFG': {
					'address': 0x8A, 'module': 'IOC',
					'description': 'Port 1 interrupt status flag',
					'bitfields': {
						'P1IF': {
							'slice': (7,0), 'default': 0, 'access': 'R/W',
							'description': 'Port 1, inputs 7 to 0 interrupt status flags. When an input port pin has an interrupt request pending, the corresponding flag bit is set.'
						},
					},
				},
			'P2IFG': {
					'address': 0x8B, 'module': 'IOC',
					'description': 'Port 2 interrupt status flag',
					'bitfields': {
							'-reserved': {
									'slice': (7,6), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
							},
							'DPIF': {
								'slice': (5,), 'default': 0, 'access': 'R/W0',
								'description': 'USB D+ interrupt-status flag. This flag is set when the D+ line has an interrupt request pending and is used to detect USB resume events in USB suspend state. This flag is not set when the USB controller is not suspended',
							},
							'P2IF': {
								'slice': (4,0), 'default': 0, 'access': 'R/W0',
								'description': 'Port 2, input 4 to 0 interrupt status flags. When an input port pin has an interrupt request pending, the corresponding flag bit is set',
							},
					},
				},
			'PICTL': {
					'address': 0x8C, 'module': 'IOC',
					'description': 'Port pins interrupt mask and edge',
					'bitfields': {
						'PADSC': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': 'Drive strength control for I/O pins in output mode. Selects output drive strength enhancement to account for low I/O supply voltage on pin DVDD (this to ensure the same drive strength at lower voltages as at higher). 0: Minimum drive strength enhancement. DVDD1/2 equal to or greater than 2.6V. 1: Maximum drive strength enhancement. DVDD1/2 less than 2.6V',
						},
						'-reserved': {
								'slice': (6,4), 'default': 0, 'access': 'R0',
								'description': 'Reserved',
						},
						'P2ICON': {
								'slice': (3,), 'default': 0, 'access': 'R/W',
								'description': 'Port 2, inputs 7 to 4 interrupt configuration. This bit selects the interrupt request condition for Port 2 inputs 4 to 0. 0: Rising edge on input gives interrupt. 1: Falling edge on input gives interrupt.',
						},
						'P1ICONH': {
								'slice': (2,), 'default': 0, 'access': 'R/W',
								'description': 'Port 1, inputs 7 to 4 interrupt configuration. This bit selects the interrupt request condition for the high nibble of Port 1 inputs. 0: Rising edge on input gives interrupt. 1: Falling edge on input gives interrupt.',
						},
						'P1ICONL': {
								'slice': (1,), 'default': 0, 'access': 'R/W',
								'description': 'Port 1, inputs 3 to 0 interrupt configuration. This bit selects the interrupt request condition for the low nibble of Port 1 inputs. 0: Rising edge on input gives interrupt. 1: Falling edge on input gives interrupt.',
						},
						'P0ICON': {
								'slice': (0,), 'default': 0, 'access': 'R/W',
								'description': 'Port 0, inputs 7 to 0 interrupt configuration. This bit selects the interrupt request condition for all of Port 0 inputs. 0: Rising edge on input gives interrupt. 1: Falling edge on input gives interrupt.',
						},
					},
				},
			'P0IEN': {
					'address': 0xAB, 'module': 'IOC',
					'description': 'Port 0 interrupt mask. 0: interrupts are disabled. 1: interrupts are enabled.',
				},
			'P1IEN': {
					'address': 0x8D, 'module': 'IOC',
					'description': 'Port 1 interrupt mask. 0: interrupts are disabled. 1: interrupts are enabled.',
				},
			'P2IEN': {
					'address': 0xAC, 'module': 'IOC',
					'description': 'Port 2 interrupt mask',
					'bitfields': {
							'-reserved': {
									'slice': (7,6), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
							},
							'DPIEN': {
								'slice': (5,), 'default': 0, 'access': 'R/W',
								'description': 'USB D+ interrupt enable. 0: USB D+ interrupt disabled. 1: USB D+ interrupt enabled.',
							},
							'P2_IEN': {
									'slice': (4,0), 'default': 0, 'access': 'R/W',
									'description': 'Port P2.4 to P2.0 interrupt enable.  0: interrupts are disabled. 1: interrupts are enabled',
							},
					},
				},
			'P0INP': {
					'address': 0x8F, 'module': 'IOC',
					'description': 'Port 0 input mode',
					'bitfields': {
						'MDP0_': {
							'slice': (7,0), 'default': 0x0, 'description': 'P0.7 to P0.7 I/O input mode. 0: Pullup/pulldown. 1: 3-state.',
							},
					}
				},
			'PERCFG': {
					'address': 0xF1, 'module': 'IOC',
					'description': 'Peripheral I/O control',
					'default': 0x00,
					'bitfields':  {
							'-reserved1': {
								'slice': (7,), 'access': 'R0',
								'description': 'Reserved',
							},
							'T1CFG': {
									'slice': (6,), 'access': 'R/W',
									'description': 'Timer 1 I/O location. 0: Alternative 1 location. 1: Alternative 2 location.',
							},
							'T3CFG': {
									'slice': (5,), 'access': 'R/W',
									'description': 'Timer 3 I/O location. 0: Alternative 1 location. 1: Alternative 2 location.',
							},
							'T4CFG': {
									'slice': (4,), 'access': 'R/W',
									'description': 'Timer 4 I/O location. 0: Alternative 1 location. 1: Alternative 2 location.',
							},
							'-reserved2': {
								'slice': (3, 2), 'access': 'R/W',
								'description': 'Reserved',
							},
							'U1CFG': {
									'slice': (1,), 'access': 'R/W',
									'description': 'USART 1 I/O location. 0: Alternative 1 location. 1: Alternative 2 location',
							},
							'U0CFG': {
									'slice': (0,), 'access': 'R/W',
									'description': 'USART 0 I/O location. 0: Alternative 1 location. 1: Alternative 2 location',
							},
					},
				},
			'APCFG': {
					'address': 0xF2, 'module': 'IOC',
					'description': 'Analog peripheral I/O configuration.  APCFG[7:0] selects P0.7-P0.0 as analog I/O',
					'default': 0x00, 'access': 'R/W',
				},
			'P0SEL': {
					'address': 0xF3, 'module': 'IOC',
					'description': 'Port 0 function select. 0: General-purpose I/O. 1: Peripheral function',
				},
			'P1SEL': {
					'address': 0xF4, 'module': 'IOC',
					'description': 'Port 1 function select. 0: General-purpose I/O. 1: Peripheral function',
				},
			'P2SEL': {
					'address': 0xF5, 'module': 'IOC',
					'description': 'Port 2 function select',
					'bitfields': {
						'-reserved': {
								'slice': (7,), 'default': 0, 'access': 'R0',
								'description': 'Reserved',
						},
						'PRI3P1': {
							'slice': (6,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when modules are assigned to the same pins. 0: USART 0 has priority. 1: USART 1 has priority',
						},
						'PRI2P1': {
							'slice': (5,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when PERCFG assigns USART 1 and Timer 3 to the same pins. 0: USART 1 has priority. 1: Timer 3 has priority',
						},
						'PRI1P1': {
							'slice': (4,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when PERCFG assigns Timer 1 and Timer 4 to the same pins. 0: Timer 1 has priority. 1: Timer 4 has priority', },
						'PRI0P1': {
							'slice': (3,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when PERCFG assigns USART 0 and Timer 1 to the same pins. 0: USART 0 has priority. 1: Timer 1 has priority',
						},
						'SELP2_4': {
							'slice': (2,), 'default': 0, 'access': 'R/W',
							'description': 'P2.4 function select. 0: General-purpose I/O. 1: Peripheral function',
						},
						'SELP2_3': {
							'slice': (1,), 'default': 0, 'access': 'R/W',
							'description': 'P2.3 function select. 0: General-purpose I/O. 1: Peripheral function',
						},
						'SELP2_0': {
							'slice': (0,), 'default': 0, 'access': 'R/W',
							'description': 'P2.0 function select. 0: General-purpose I/O. 1: Peripheral function',
						},
					},
				},
			'P1INP': {
					'address': 0xF6, 'module': 'IOC',
					'description': 'Port 1 input mode',
					'bitfields': {
							'MDP1_': {
									'slice': (7,2), 'default': 0, 'access': 'R/W',
									'description': 'P1.7 to P1.2 I/O input mode. 0: pullup/pulldown. 1: 3-state',
									### note: the index follows port's!!
							},
							'-reserved': {
									'slice': (1, 0), 'default': 0, 'access': 'R0',
							},
						},
				},
			'P2INP': {
					'address': 0xF7, 'module': 'IOC',
					'description': 'Port 2 input mode',
					'default': 0x00, 'access': 'R/W',
					'bitfields': {
						'PDUP2': {
							'slice': (7,),
							'description': 'Port 2 pullup/pulldown select. Selects function for all Port 2 pins configured as pullup/pulldown inputs. 0: pullup. 1: pulldown.'
						},
						'PDUP1': {
							'slice': (6,),
							'description': 'Port 1 pullup/down select. Selects function for all Port 1 pin configured as pullup/pulldown inputs. 0: pullup. 1: pulldown',
							},
						'PDUP0': {
							'slice': (5,),
							'description': 'Port 0 pullup/pulldown select. Selects function for all Port 0 pins configured as pullup/pulldown inputs. 0: pullup, 1: pulldown.',
						},
						'MDP2_': {
								'slice': (4,0),
								'description': 'P2.4 to P2.0 I/O input mode. 0: Pullup/pulldown. 1: 3-state.',
						},
					},
				},
			'P0DIR': {
					'address': 0xFD, 'module': 'IOC',
					'default': 0x00, 'access': 'R/W',
					'description': 'Port 0 direction. 0: input. 1: output.',
				},
			'P1DIR': {
					'address': 0xFE, 'module': 'IOC',
					'default': 0x00, 'access': 'R/W',
					'description': 'Port 1 direction. 0: input. 1: output.',
				},
			'P2DIR': {
					'address': 0xFF, 'module': 'IOC',
					'description': 'Port 2 direction and Port 0 Peripheral Priority Control',
					'bitfields': {
						'PRIP0': {
								'slice': (7,6), 'default': 0, 'access': 'R/W',
								'description': '''Port 0 peripheral priority control.
These bits determine the order of priority in the case when PERCFG assigns several peripherals to the same pins. Detailed by priority list:
00:
1st priority: USART 0
								2nd priority: USART 1
								3rd priority: Timer 1
								01:
								1st priority: USART 1
								2nd priority: USART 0,
								3rd priority: Timer 1.
								10:
								1st priority: Timer 1 channels 0-1
								2nd priority: USART 1
								3rd priority: USART 0
								4th priority: Timer 1 channels 2-3
								11:
								1st priority: Timer 1 channels 2-3
								2nd priority: USART 0
								3rd priority: USART 1
								4th priority: Timer 1 channels 0-1''',
						},
						'-reserved': {
							'slice': (5,), 'access': 'R0', 'description': 'Reserved',
						},
						'DIRP2': {
							'slice': (4,0), 'access': 'R/W', 'description': 'P2.4 to P2.0 I/O direction. 0: input. 1: output',
						},
					},
				},
			'PMUX': {
					'address': 0xAE, 'module': 'IOC',
					'description': 'Power-down signal mux',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'CKOEN': {
									'slice': (7,),
									'description': 'Clock Out Enable. When this bit is set, the selected 32-kHz clock is output on one of the P0 pins. CKOPIN selects the pin to use. This overrides all other configuration for the selected pin. The clock is output in all power modes; however, in PM3 the clock stops',
							},
							'CKOPIN': {
									'slice': (6, 4),
									'description': 'Clock Out Pin. Selects which P0 pin is to be used to output the selected 32-kHz clock.',
							},
							'DREGSTA': {
									'slice': (3,),
									'description': 'Digital RegulatorStatus. When this bit is set, the status of the digital regulator is output on one of the P1 pins. DREGSTAPIN selects the pin. When DREGSTA is set, all other configurations for the selected pin are overridden. The selected pin outputs 1 when the 1.8-V on-chip digital regulator is powered up (chip has regulated power).  The selected pin outputs 0 when the 1.8-V on-chip digital regulator is powered down.',
							},
							'DREGSTAPIN': {
									'slice': (2,0),
									'description': 'Digital Regulator Status Pin.  Selects which P1 pin is to be used to output DREGSTA signal',
							},
					},
				},
			############## Memory ################
			'MPAGE': {
					'address': 0x93, 'module': 'MEMORY',
					'description': 'Memory page select',
				},
			'MEMCTR': {
					'address': 0xC7, 'module': 'MEMORY',
					'description': 'Memory system control',
					'bitfields': {
							'-reserved': {
									'slice': (7,4), 'default': 0, 'access': 'R0',
											'description': 'Reserved',
								}, 
							'XMAP': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
									'description': '''XDATA map to code. When this bit is set, the SRAM XDATA region, from 0x0000 through (SRAM_SIZE-1) is mapped into the CODE region from 0x8000 through (0x8000 + SRAM_SIZE-1). This enables execution of program code from RAM.
0: SRAM map into CODE feature disabled.
1: SRAM map into CODE feature enabled.''',
							'XBANK': {
									'slice': (2,0), 'default': 0, 'access': 'R/W',
									'description': '''XDATA bank select. Controls which code bank of the physical flash memory is mapped into the XDATA region (0x8000-0xFFFF). When set to 0, the root bank is mapped in.

Valid settings depend on the flash size for the device. Writing an invalid setting is ignored, i.e., no update to XBANK[2:0] is performed.
32-KB version: 0 only (i.e., the root bank is always mapped in.)
64-KB version: 0-1
96-KB version: 0-2
128-KB version: 0-3
256-KB version: 0-7''',
							},
						},
					},
				},
			'FMAP': {
					'address': 0x9F, 'module': 'MEMORY',
					'description': 'Flash-memory bank mapping',
					'bitfields': {
							'-reserved': {
									'slice': (7,3), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
								},
							'MAP': {
									'slice': (2,0), 'default': 0b001, 'access': 'R/W',
									'description': '''Flash bank map. Controls which bank is mapped into the bank area of the CODE memory space (0x8000-0xFFFF). When set to 0, the root bank is mapped in. Valid settings depend on the flash size for the device. Writing an invalid setting is ignored, i.e., no update to MAP[2:0] is performed.

32-KB version: No value can be written. Bank area is only used for running program code from SRAM. See MEMCTR.XMAP.
64-KB version: 0-1
96-KB version: 0-2
128-KB version: 0-3
256-KB version: 0-7.''',
								},
					},
				},
			'RFIRQF1': {
					'address': 0x91, 'module': 'RF',
					'description': 'RF interrupt flags MSB',
				},
			'RFD': {
					'address': 0xD9, 'module': 'RF',
					'description': 'RF data',
				},
			'RFST': {
					'address': 0xE1, 'module': 'RF',
					'description': 'RF command strobe',
				},
			'RFIRQF0': {
					'address': 0xE9, 'module': 'RF',
					'description': 'RF interrupt flags LSB',
				},
			'RFERRF': {
					'address': 0xBF, 'module': 'RF',
					'description': 'RF error interrupt flags',
				},
			'ST0': {
					'address': 0x95, 'module': 'ST',
					'default': 0, 'access': 'R/W',
					'description': 'Sleep Timer 0 count/compare value. When read, this register returns the low bits [7:0] of the Sleep Timer count. When writing, this register sets the low bits [7:0] of the compare value. Writes to this register are ignored unless STLOAD.LDRDY is 1',
				},
			'ST1': {
					'address': 0x96, 'module': 'ST',
					'default': 0, 'access': 'R/W',
					'description': 'Sleep Timer 1 count/compare value. When read, this register returns the middle bits [15:8] of the Sleep Timer count. When writing, this register sets the middle bits [15:8] of the compare value. The value read is latched at the time of reading register ST0. The value written is latched when ST0 is written',
				},
			'ST2': {
					'address': 0x97, 'module': 'ST',
					'default': 0, 'access': 'R/W',
					'description': 'Sleep Timer 2 count/compare value. When read, this register returns the high bits [23:16] of the Sleep Timer count. When writing, this register sets the high bits [23:16] of the compare value. The value read is latched at the time of reading register ST0. The value written is latched when ST0 is written',
				},
			'STLOAD': {
					'address': 0x95, 'module': 'ST',
					'description': 'Sleep-timer load status',
					'bitfields': {
							'-reserved': {
									'slice': (7,1), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
							},
							'LDRDY': {
									'slice': (0,), 'default': 1, 'access': 'R',
									'description': 'Load ready. This bit is 0 while the Sleep Timer loads the 24-bit compare value and 1 when the Sleep Timer is ready to start loading a new compare value.',
							},
					},
				},
			######### Power Management control ##########
			'SLEEPCMD': {
					'address': 0xBE, 'module': 'PMC',
					'description': 'Sleep-mode control command',
					'default': 0x04,
					'bitfields': {
							'OSC32K_CALDIS': {
								'slice': (7,), 'access': 'R/W',
								'description': 'Disable 32-kHz RC oscillator calibration. 0: 32-kHz RC oscillator calibration is enabled. 1: 32-kHz RC oscillator calibration is disabled. This setting can be written at any time, but does not take effect before the chip has been running on the 16-MHz high-frequency RC oscillator.',
							},
							'-reserved1': {
								'slice': (6,3), 'access': 'R0',
								'description': 'Reserved',
							},
							'-reserved2': {
								'slice': (2,), 'access': 'R/W',
								'description': 'Reserved. Always write as 1',
							},
							'MODE': {
								'slice': (1,0), 'access': 'R/W',
								'description': 'Power-mode setting. 00: Active/idle mode. 01: Power mode 1 (PM1). 10: Power mode 2 (PM2).  11: Power mode 3 (PM3)',
							},
					},
				},
			'SLEEPSTA': {
					'address': 0x9D, 'module': 'PMC', 'access': 'R',
					'description': 'Sleep-mode control status',
					'bitfields': {
							'OSC32K_CALDIS': {
									'slice': (7,),
									'default': 0,
									'description': '32-kHz RC oscillator calibration status. SLEEPSTA.OSC32K_CALDIS shows the current status of disabling of the 32-kHz RC calibration.  The bit is not set to the same value as SLEEPCMD.OSC32K_CALDIS before the chip has been run on the 32-kHz RC oscillator.',
							},
							'-reserved1': {
									'slice': (6, 5), 'default': 0, 'description': 'Reserved',
							},
							'RST': {
								'slice': (4,3),
								'description': 'Status bit indicating the cause of the last reset. If there are multiple resets, the register only contains the last event.',
							},
							'-reserved2': {
								'slice': (2,1), 'default': 0, 'description': 'Reserved',
							},
							'CLK32K': {
								'slice': (0,), 'default': 0,
								'description': 'The 32-kHz clock signal (synchronized to the system clock)',
							},
					},
				},
			'CLKCONCMD': {
					'address': 0xC6, 'module': 'PMC',
					'description': 'Clock control command',
					'default': 0xC9, # 11001001
					'access': 'R/W',
					'bitfields': {
							'OSC32K': {
									'slice': (7,),
									'description': '32-kHz clock-source selct. Setting this bit initiates a clock-source change only. CLKCONSTA.OSC32K reflects the current setting. The 16-MHz RCOSC must be selected as system clock when this bit is to be changed. This bit does not give an indication of the stability of the 32-kHz XOSC.',
							},
							'OSC': {
									'slice': (6,),
									'description': 'System clock-source select. Setting this bit initiates a clock-source change only.  CLKCONSTA.OSC reflects the current setting. 0: 32 MHz XOSC, 1: 16 MHz RCOSC.',
							},
							'TICKSPD': {
									'slice': (5,3),
									'description': 'Timer ticks output setting. Cannot be higher than system clock setting given by OSC bit setting. 000: 32 MHz. 001: 16 MHz, 010: 8 MHz, 011: 4 MHz, 100: 2 MHz, 101: 1 MHz, 110: 500 kHz, 111: 250 kHz. Note that CLKCONCMD.TICKSPD can be set to any value, but the effect is limited by the CLKCONCMD.OSC setting; i.e., if CLKCONCMD.OSC = 1 and the CLKCONCMD.TICKSPD = 000, CLKCONSTA.TICKSPD reads 001, and the real TICKSPD is 16 MHz',
							},
							'CLKSPD': {
									'slice': (2,0),
									'description': 'Clock speed. Cannot be higher than system clock setting given by the OSC bit settings.  Indicates current system-clock frequency. 000: 32 Mhz. 001: 16 MHz. 010: 8 MHz. 011: 4 MHz. 100: 2 MHz. 101: 1 MHz. 110: 500 kHz. 111: 250 kHz.  Note that CLKCONCMD.CLKSPD can be set to any value, but the effect is limited by the CLKCONCMD.OSC setting; i.e., if CLKCONCMD.OSC=1 and CLKCONCMD.CLKSPD=000, CLKCONSTA.CLKSPD reads 001, and the real CLKSPD is 16 MHz. Note also that the debugger cannot be used with a divided system clock. When running the debugger, the value of CLKCONCM. CLKSPD should be set to 000 when CLKCONCMD.OSC = 0 or to 001 when CLKCONCMD.OSC = 1',
							},
					},
				},
			'CLKCONSTA': {
					'address': 0x9E, 'module': 'PMC',
					'description': 'Clock control status',
					'default': 0xC5,
					'access': 'R',
					'bitfields': {
							'OSC32K': {
									'slice': (7,),
									'description': 'Current 32-kHz clock source selected: 0: 32-kHz X)SC. 1: 32-kHz RCOSC.'
							},
							'OSC': {
									'slice': (6,),
									'description': 'Current system clock selected: 0: 32-MHz XOSC. 1: 16-MHz RCOSC.',
							},
							'TICKSPD':  {
									'slice': (5,3),
									'description': 'Current timer ticks output settings.  000: 32 MHz. 001: 16 MHz. 010: 8 MHz. 011: 4 MHz.  100: 2 MHz. 101: 500 kHz. 111: 250 kHz',
							},
							'CLKSPD': {
									'slice': (2,0),
									'description': 'Current clock speed.  000: 32 MHz. 001: 16 MHz. 010: 8 MHz. 011: 4 MHz.  100: 2 MHz. 101: 500 kHz. 111: 250 kHz',
							},
						},
				},
			############# Timers #############
			'T1CC0L': {
					'address': 0xDA, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 0 capture/compare value low-order byte. Data written to this register is stored in a buffer but not written to T1CC0[7:0] until, and at the same time as, a later write to T1CC0H takes effect',
				},
			'T1CC0H': {
					'address': 0xDB, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 0 capture/compare value high-order byte. Writing to this register when T1CCTL0.MODE = 1(compare mode) causes the T1CC0[15:0] update to the written value to be delayed until T1CNT=0x0000.',
				},
			'T1CC1L': {
					'address': 0xDC, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 1 capture/compare value low-order byte. Data written to this register is stored in a buffer but not written to T1CC1[7:0] until, and at the same time as, a later write to T1CC1H takes effect.',
				},
			'T1CC1H': {
					'address': 0xDD, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 1 capture/compare value high-order byte. Writing to this register when T1CCTL1.MODE=1 (compare mode) causes the T1CC1[15:0] update to the written value to be delayed until T1CNT = 0x0000.',
				},
			'T1CC2L': {
					'address': 0xDE, 'module': 'Timer 1',
					'description': 'Timer 1 channel 2 capture/compare value low-order byte. Data written to this register is stored in a buffer but not written to T1CC2[7:0] until, and at the same time as, a later write to T1CC2H takes effect.',
					'default': 0, 'access': 'R/W',
				},
			'T1CC2H': {
					'address': 0xDF, 'module': 'Timer 1',
					'description': 'Timer 1 channel 2 capture/compare value high-order byte. Writing to this register when T1CCTL2.MODE=1 (compare mode) causes the T1CC2[15:0] update to the written value to be delayed until T1CNT = 0x0000',
					'default': 0, 'access': 'R/W',
				},
			'T1CNTL': {
					'address': 0xE2, 'module': 'Timer 1',
					'description': 'Timer 1 counter low',
				},
			'T1CNTH': {
					'address': 0xE3, 'module': 'Timer 1',
					'description': 'Timer 1 counter high-order byte. Contains the high byte of the 16-bit timer counter buffered at the time T1CNTL is read',
					'default': 0, 'access': 'R',
				},
			'T1CTL': {
					'address': 0xE4, 'module': 'Timer 1',
					'description': 'Timer 1 control and status',
				},
			'T1CCTL0': {
					'address': 0xE5, 'module': 'Timer 1',
					'description': 'Timer 1 channel 0 capture/compare control',
					'bitfields': {
							'RFIRQ': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
									'description': 'When set, use RF interrupt for capture intead of regular capture input.',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': 'Channel 0 interrupt mask. Enables interrupt request when set.',
							},
							'CMP': {
									'slice': (5,3), 'default': 0, 'access': 'R/W',
									'description': '''Channel 0 compare-mode select.  Selects action on output when timer value equals compare value in T1CC0
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on 0
100: Clear output on compare-up, set on 0
101: Reserved
110: Reserved
111: Initialize output pin. CMP[2:0] is not changed.''',
							},
							'MODE': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
									'description': '''Mode. Select Timer 1 channel 0 capture or compare mode
0: Capture mode
1: Compare mode''',
							},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Channel 0 capture-mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on all edges''',
							},
					},
				},
			'T1CCTL1': {
					'address': 0xE6, 'module': 'Timer 1',
					'description': 'Timer 1 channel 1 capture/compare control',
					'bitfields': {
							'RFIRQ': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': 'When set, use RF interrupt for capture instead of regular capture input.',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': 'Channel 1 interrupt mask. Enables interrupt request when set',
							},
							'CMP': {
								'slice': (5,3), 'default': 0, 'access': 'R/W',
								'description': '''Channel 1 compare-mode select.  Selects action on output when timer value equals compare value in T1CC1.
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on compare-down in up-down mode.  Otherwise set output on compare, clear on 0.
100: Clear output on compare-up, set on compare-down in up-down mode.  Otherwise clear output on compare, set on 0.
101: Clear when equal T1CC0, set when equal T1CC1
110: Set when equal T1CC0, clear when equal T1CC1
111: Initialize output pin. CMP[2:0] is not changed.''',
							},
							'MODE': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
									'description': '''Mode. Select Timer 1 channel 1 capture or compare mode
0: Capture mode
1: Compare mode''',
							},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Channel 1 capture-mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on all edges''',
							}
					},

				},
			'T1CCTL2': {
					'address': 0xE7, 'module': 'Timer 1',
					'description': 'Timer 1 channel 2 capture/compare control',
					'bitfields': {
							'RFIRQ': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': 'When set, use RF interrupt for capture instead of regular capture input.',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': 'Channel 2 interrupt mask. Enables interrupt request when set',
							},
							'CMP': {
								'slice': (5,3), 'default': 0, 'access': 'R/W',
								'description': '''Channel 2 compare-mode select.  Selects action on output when timer value equals compare value in T1CC2.
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on compare-down in up-down mode.  Otherwise set output on compare, clear on 0.
100: Clear output on compare-up, set on compare-down in up-down mode.  Otherwise clear output on compare, set on 0.
101: Clear when equal T1CC0, set when equal T1CC2
110: Set when equal T1CC0, clear when equal T1CC2
111: Initialize output pin. CMP[2:0] is not changed.''',
							},
							'MODE': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
									'description': '''Mode. Select Timer 1 channel 2 capture or compare mode
0: Capture mode
1: Compare mode''',
							},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Channel 2 capture-mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on all edges''',
							}
					},
				},
			'T1STAT': {
					'address': 0xAF, 'module': 'Timer 1',
					'description': 'Timer 1 status',
				},
			'T2CTRL': {
					'address': 0x94, 'module': 'Timer 2',
					'description': 'Timer 2 control',
				},
			'T2EVTCFG': {
					'address': 0x9C, 'module': 'Timer 2',
					'description': 'Timer 2 event configuration',
				},
			'T2IRQF': {
					'address': 0xA1, 'module': 'Timer 2',
					'description': 'Timer 2 interrupt flags',
				},
			'T2M0': {
					'address': 0xA2, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed register 0',
				},
			'T2M1': {
					'address': 0xA3, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed register 1',
				},
			'T2MOVF0': {
					'address': 0xA4, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed overflow register 0',
				},
			'T2MOVF1': {
					'address': 0xA5, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed overflow register 1',
				},
			'T2MOVF2': {
					'address': 0xA6, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed overflow register 2',
				},
			'T2IRQM': {
					'address': 0xA7, 'module': 'Timer 2',
					'description': 'Timer 2 interrupt mask',
				},
			'T2MSEL': {
					'address': 0xC3, 'module': 'Timer 2',
					'description': 'Timer 2 multiplex select',
				},
			'T3CNT': {
					'address': 0xCA, 'module': 'Timer 3',
					'default': 0, 'access': 'R',
					'description': 'Timer 3 counter. Contains the current value of the 8-bit counter',
				},
			'T3CTL': {
					'address': 0xCB, 'module': 'Timer 3',
					'description': 'Timer 3 control',
					'bitfields': {
							'DIV': {
									'slice': (7,5), 'default': 0, 'access': 'R/W',
									'description': '''Prescalar divider value.  Generates the active clock edge used to clock the timer from CLKCONCMD.TICKSPD as follows:
000: Tick frequency/1
001: Tick frequency/2
010: Tick frequency/4
011: Tick frequency/8
100: Tick frequency/16
101: Tick frequency/32
110: Tick frequency/64
111: Tick frequency/128''',
							},
							'START': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
									'description': 'Start timer. Normal operation when set, suspended when cleared',
							},
							'OVFIM': {
									'slice': (3,), 'default': 1, 'access': 'R/W',
									'description': '''Overflow interrupt mask
0: interrupt is disabled.
1: interrupt is enabled.''',
							},
							'CLR': {
									'slice': (2,), 'default': 0, 'access': 'R0/W1',
									'description': 'Clear counter. Writing a 1 to CLR resets the counter to 0x00 and initializes all output pins of associated channels. Always read as 0.',
							},
							'MODE': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Timer 3 mode. Select the mode as follows:
00: Free-running, repeated count from 0x00 to 0xff
01: Down, count from T3CC0 to 0x00
10: Modulo, repeatedly count from 0x00 to T3CC0
11: Up/down, repeatedly count from 0x00 to T3CC0 and down to 0x00''',
							},
					},
				},
			'T3CCTL0': {
					'address': 0xCC, 'module': 'Timer 3',
					'description': 'Timer 3 channel 0 compare control',
					'bitfields': {
							'-default': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
									'description': 'Reserved',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': '''Channel 0 interrupt mask
0: interrupt is disabled.
1: interrupt is enabled.''',
							},
							'CMP': {
									'slice': (5,3), 'default': 0, 'access': 'R/W',
									'description': '''Channel 0 compare output mode select. Specified action occurs on output when timer value equals compare value in T3CC0
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on 0
100: Clear output on compare-up, set on 0
101: Set output on compare, clear on 0xFF
110: Clear output on compare, set on 0x00
111: Initialize output pin. CMP[2:0] is not changed.'''
							},
							'MODE': {
										'slice': (2,), 'default': 0, 'access': 'R/W',
										'description': '''Mode. Select Timer 3 channel 0 mode
0: Capture mode
1: Compare mode''',
								},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Capture mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on both edges''',
							},
					},
				},
			'T3CC0': {
					'address': 0xCD, 'module': 'Timer 3',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 3 channel 0 compare value. Writing to this register when T3CCTL.MODE=1 (compare mode) causes the T3CC0.VAL[7:0] update to the written value to be delayed until T3CNT.CNT[7:0]=0x00',
				},
			'T3CCTL1': {
					'address': 0xCE, 'module': 'Timer 3',
					'description': 'Timer 3 channel 1 compare control',
					'bitfields': {
							'-reserved': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'IM': {
								'slice': (6,), 'default': 1, 'access': 'R/W',
								'description': '''Channel 1 interrupt mask
0: interrupt is disabled
1: interrupt is enabled''',
							},
							'CMP': {
									'slice': (5,3), 'default': 0, 'access': 'R/W',
									'description': '''Channel 1 compare output mode select. Specified action occurs on output when timer value equals compare value in T3CC1
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on 0
100: Clear output on compare-up, set on 0
101: Set output on compare, clear on 0xFF
110: Clear output on compare, set on 0x00
111: Initialize output pin. CMP[2:0] is not changed.'''
							},
							'MODE': {
										'slice': (2,), 'default': 0, 'access': 'R/W',
										'description': '''Mode. Select Timer 3 channel 1 mode
0: Capture mode
1: Compare mode''',
								},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Capture mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on both edges''',
							},
					},
				},
			'T3CC1': {
					'address': 0xCF, 'module': 'Timer 3',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 3 channel 1 compare value. Writing to this register when T3CCTL1.MODE=1 (comapre mode) causes T3CC1.VAL[7:0] update to the writte nvalue to be delayed until T3CNT.CNT[7:0]=0x00',
				},
			'T4CNT': {
					'address': 0xEA, 'module': 'Timer 4',
					'default': 0, 'access': 'R',
					'description': 'Timer 4 counter. Contains the current value of the 8-bit counter',
				},
			'T4CTL': {
					'address': 0xEB, 'module': 'Timer 4',
					'description': 'Timer 4 control',
					'bitfields': {
							'DIV': {
									'slice': (7,5), 'default': 0, 'access': 'R/W',
									'description': '''Prescaler divider value. Generates the active clock edge used to clock the timer from CLKCONCMD.TICKSPD as follows:
000: Tick frequency / 1
001: Tick frequency / 2
010: Tick frequency / 4
011: Tick frequency / 8
100: Tick frequency / 16
101: Tick frequency / 32
110: Tick frequency / 64
111: Tick frequency / 128''',
							},
							'START': {
									'slice': (4,), 'access': 'R/W',
									'description': 'Start timer. Normal operation when set, suspended when cleared',
							},
							'OVFIM': {
								'slice': (3,), 'default': 1, 'access': 'R/W',
								'description': 'Overflow interrupt mask',
							},
							'CLR': {
								'slice': (2,), 'default': 0, 'access': 'R0/W1',
								'description': 'Clear counter. Writing a 1 to CLR resets the counter to 0x00 and initializees all output pins of associated channels. Always read as 0',
							},
							'MODE': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Timer 4 mode. Select the mode as follows:
00: Free running repeated count from 0x00 to 0xff
01: Down, count from T4CC0 to 0x00
10: Modulo, repeatedly count from 0x00 to T4CC0
11: Up/down, repeatedly count from 0x00 to T4CC0 and down to 0x00''',
							},
					},
				},
			'T4CCTL0': {
					'address': 0xEC, 'module': 'Timer 4',
					'description': 'Timer 4 channel 0 compare control',
					'bitfields': {
							'-default': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
									'description': 'Reserved',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': '''Channel 0 interrupt mask
0: interrupt is disabled.
1: interrupt is enabled.''',
							},
							'CMP': {
									'slice': (5,3), 'default': 0, 'access': 'R/W',
									'description': '''Channel 0 compare output mode select. Specified action occurs on output when timer value equals compare value in T4CC0
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on 0
100: Clear output on compare-up, set on 0
101: Set output on compare, clear on 0xFF
110: Clear output on compare, set on 0x00
111: Initialize output pin. CMP[2:0] is not changed.'''
							},
							'MODE': {
										'slice': (2,), 'default': 0, 'access': 'R/W',
										'description': '''Mode. Select Timer 4 channel 0 mode
0: Capture mode
1: Compare mode''',
								},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Capture mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on both edges''',
							},
					},
				},
			'T4CC0': {
					'address': 0xED, 'module': 'Timer 4',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 4 channel 0 compare value. Writing to this register when T4CCTL0.MODE=1 (compare mode) causes the T4CC0.VAL[7:0] update to the written value to be delayed until T4CNT.CNT[7:0] = 0x00',
				},
			'T4CCTL1': {
					'address': 0xEE, 'module': 'Timer 4',
					'description': 'Timer 4 channel 1 compare control',
					'bitfields': {
							'-reserved': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'IM': {
								'slice': (6,), 'default': 1, 'access': 'R/W',
								'description': '''Channel 1 interrupt mask
0: interrupt is disabled
1: interrupt is enabled''',
							},
							'CMP': {
									'slice': (5,3), 'default': 0, 'access': 'R/W',
									'description': '''Channel 1 compare output mode select. Specified action occurs on output when timer value equals compare value in T4CC1
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on 0
100: Clear output on compare-up, set on 0
101: Set output on compare, clear on 0xFF
110: Clear output on compare, set on 0x00
111: Initialize output pin. CMP[2:0] is not changed.'''
							},
							'MODE': {
										'slice': (2,), 'default': 0, 'access': 'R/W',
										'description': '''Mode. Select Timer 4 channel 1 mode
0: Capture mode
1: Compare mode''',
								},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Capture mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on both edges''',
							},
					},
				},
			'T4CC1': {
					'address': 0xEF, 'module': 'Timer 4',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 4 channel 1 compare value. Writing to this register when T4CCTL1.MODE=1 (comapre mode) causes the T4CC1.VAL[7:0] update to the written value to be delayed until T4CNT.CNT[7:0] = 0x00',
				},
			'TIMIF': {
					'address': 0xD8, 'module': 'TMINT',
					'description': 'Timers 1/3/4 joint interrupt mask/flags. ',
					'bitfields': {
							'-reserved': {
									'slice': (7,), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
								},
							'T1OVFIM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': 'Timer 1 overflow interrupt mask',
							},
							'T4CH1IF': {
									'slice': (5,), 'default': 0, 'access': 'R/W0',
									'description': '''Timer 4 channel 1 interrupt flag
0: No interrupt is pending
1: interrupt is pending''',
							},
							'T4CH0IF': {
									'slice': (4,), 'default': 0, 'access': 'R/W0',
									'description': '''Timer 4 channel 0 interrupt flag
0: No interrupt is pending
1: interrupt is pending''',
							},
							'T4OVFIF': {
									'slice': (3,), 'default': 0, 'access': 'R/W0',
									'description': '''Timer 4 overflow interrupt flag
0: No interrupt is pending
1: interrupt is pending''',
							},
							'T3CH1IF': {
									'slice': (2,), 'default': 0, 'access': 'R/W0',
									'description': '''Timer 3 channel 1 interrupt flag
0: No interrupt is pending
1: interrupt is pending''',
							},
							'T3CH0IF': {
									'slice': (1,), 'default': 0, 'access': 'R/W0',
									'description': '''Timer 3 channel 0 interrupt flag
0: No interrupt is pending
1: interrupt is pending''',
							},
							'T3OVFIF': {
									'slice': (0,), 'default': 0, 'access': 'R/W0',
									'description': '''Timer 3 overflow interrupt flag
0: No interrupt is pending
1: interrupt is pending''',
							},
					},
				},
			################## USART ####################
			'U0CSR': {
					'address': 0x86, 'module': 'USART 0',
					'description': 'USART 0 control and status',
					'bitfields': {
							'MODE': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': '''USART mode select
0: SPI mode
1: UART mode''',
							},
							'RE': {
								'slice': (6,), 'default': 0, 'access': 'R/W',
								'description': '''UART receiver enable. Note: Do not enable receive before UART is fully configured.
0: Receiver disabled
1: Receiver enabled''',
							},
							'SLAVE': {
								'slice': (5,), 'default': 0, 'access': 'R/W',
								'description': '''SPI master or slave mode select
0: SPI mode
1: UART mode''',
							},
							'FE': {
								'slice': (4,), 'default': 0, 'access': 'R/W0',
								'description': '''UART framing error status. This bit is automatically cleared on a read of the U0CSR register or bits in the U0CSR register.
0: No framing error detected
1: Byte received with incorrect stop-bit level''',
							},
							'ERR': {
								'slice': (3,), 'default': 0, 'access': 'R/W0',
								'description': '''UART parity error status. This bit is automatically cleared on a read of the U0CSR register or bits in the U0CSR register
0: No parity error detected
1: Byte received with parity error''',
							},
							'RX_BYTE': {
								'slice': (2,), 'default': 0, 'access': 'R/W0',
								'description': '''Receive byte status. UART mode and SPI slave mode. This bit is automatically cleared when reading U0DBUF; clearing this bit by writing 0 to it effectively discards the data in U0DBUF.
0: No byte received
1: Received byte ready''',
							},
							'TX_BYTE': {
								'slice': (1,), 'default': 0, 'access': 'R/W0',
								'description': '''Transmit byte status. UART mode and SPI master mode
0: Byte not transmitted
1: Last byte written to data-buffer register has been transmitted''',
							},
							'ACTIVE': {
								'slice': (0,), 'default': 0, 'access': 'R/W',
								'description': '''USART transmit/receive active status. In SPI slave mode, this bit equals slave select.
0: USART idle
1: USART busy in transmit or receive mode''',
							},
					},
				},
			'U0DBUF': {
					'address': 0xC1, 'module': 'USART 0',
					'description': 'USART 0 receive/transmit data buffer. When writing this register, the data written is written to the internal transmit-data register. When reading this register, the data from the internal read-data register is read.',
					'default': 0, 'access': 'R/W',
				},
			'U0BAUD': {
					'address': 0xC2, 'module': 'USART 0',
					'default': 0, 'access': 'R/W',
					'description': 'USART 0 baud-rate control. Baud-rate mantissa value. BAUD_E along with BAUD_M decides the UART baud rate and the SPI master SCK clock frequency.',
				},
			'U0UCR': {
					'address': 0xC4, 'module': 'USART 0',
					'description': 'USART 0 UART control',
					'bitfields': {
							'FLUSH': {
								'slice': (7,), 'default': 0, 'access': 'R0/W1',
								'description': 'Flush unit. When set, this event stops the current operation and returns the unit to the idle state.',
							},
							'FLOW': {
								'slice': (6,), 'default': 0, 'access': 'R/W',
								'description': '''UART hardware flow enable. Selects use of hardware flow control with RTS and CTS pins
0: Flow control disabled
1: Flow control enabled''',
							},
							'D9': {
								'slice': (5,), 'default': 0, 'access': 'R/W',
								'description': '''If parity is enabled (see PARITY, bit 3 in this register), then this bit sets the parity level as follows:
0: Odd parity
1: Even parity''',
							},
							'BIT9': {
								'slice': (4,), 'default': 0, 'access': 'R/W',
								'description': '''Set this bit to 1 in order to enable the parity bit transfer (as 9th bit). The content of this 9th bit is given by D9, if parity is enabled by PARITY
0: 8-bit transfer
1: 9-bit transfer''',
							},
							'PARITY': {
								'slice': (3,), 'default': 0, 'access': 'R/W',
								'description': '''UART parity enable. One must set BIT9 in addition to setting this bit for parity to be calculated.
0: Parity disabled
1: Parity enabled''',
							},
							'SPB': {
								'slice': (2,), 'default': 0, 'access': 'R/W',
								'description': '''UART number of stop bits. Selects the number of stop bits to transmit
0: 1 stop bit
1: 2 stop bits''',
							},
							'STOP': {
								'slice': (1,), 'default': 1, 'access': 'R/W',
								'description': '''UART stop-bit level must be different from the start-bit level
0: Low stop bit
1: High stop bit''',
							},
							'START': {
								'slice': (0,), 'default': 0, 'access': 'R/W',
								'description': '''UART start-bit level. Ensure that the polarity of the start bit is opposit the level of the idle line.
0: Low start bit
1: High start bit''',
							},
					},
				},
			'U0GCR': {
					'address': 0xC5, 'module': 'USART 0',
					'description': 'USART 0 generic control',
					'bitfields': {
							'CPOL': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': '''SPI clock polarity
0: Negative clock polarity
1: Positive clock polarity''',
							},
							'CPHA': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
									'description': '''SPI clock phase
0: Data is output on MOSI when SCK goes from CPOL inverted to CPOL, and data input is sampled on MISO when SCK goes from CPOL to CPOL inverted.
1: Data is output on MOSI when SCK goes from CPOL to CPOL inverted, and data input is sampled on MISO when SCK goes from CPOL inverted to CPOL.''',
							},
							'ORDER': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
									'description': '''Bit order for transfers
0: LSB first
1: MSB first''',
							},
							'BAUD_E': {
									'slice': (4,0), 'default': 0, 'access': 'R/W',
									'description': 'Baud rate exponent value. BAUD_E along with BAUD_M determines the UART baud rate and the SPI master SCK clock frequency.'
							},
					},
				},


			'P0IEN': {
					'address': 0xAB, 'module': 'IOC',
					'description': 'Port 0 interrupt mask',
				},
			'P1IEN': {
					'address': 0x8D, 'module': 'IOC',
					'description': 'Port 1 interrupt mask',
				},
			'P2IEN': {
					'address': 0xAC, 'module': 'IOC',
					'description': 'Port 2 interrupt mask',
				},
			'P0INP': {
					'address': 0x8F, 'module': 'IOC',
					'description': 'Port 0 input mode',
					'bitfields': {
						'MDP0_': {
							'slice': (7,0), 'default': 0x0, 'description': 'P0.7 to P0.7 I/O input mode. 0: Pullup/pulldown. 1: 3-state.',
							},
					}
				},
			'PERCFG': {
					'address': 0xF1, 'module': 'IOC',
					'description': 'Peripheral I/O control',
					'default': 0x00,
					'bitfields':  {
							'-reserved1': {
								'slice': (7,), 'access': 'R0',
								'description': 'Reserved',
							},
							'T1CFG': {
									'slice': (6,), 'access': 'R/W',
									'description': 'Timer 1 I/O location. 0: Alternative 1 location. 1: Alternative 2 location.',
							},
							'T3CFG': {
									'slice': (5,), 'access': 'R/W',
									'description': 'Timer 3 I/O location. 0: Alternative 1 location. 1: Alternative 2 location.',
							},
							'T4CFG': {
									'slice': (4,), 'access': 'R/W',
									'description': 'Timer 4 I/O location. 0: Alternative 1 location. 1: Alternative 2 location.',
							},
							'-reserved2': {
								'slice': (3, 2), 'access': 'R/W',
								'description': 'Reserved',
							},
							'U1CFG': {
									'slice': (1,), 'access': 'R/W',
									'description': 'USART 1 I/O location. 0: Alternative 1 location. 1: Alternative 2 location',
							},
							'U0CFG': {
									'slice': (0,), 'access': 'R/W',
									'description': 'USART 0 I/O location. 0: Alternative 1 location. 1: Alternative 2 location',
							},
					},
				},
			'APCFG': {
					'address': 0xF2, 'module': 'IOC',
					'description': 'Analog peripheral I/O configuration.  APCFG[7:0] selects P0.7-P0.0 as analog I/O',
					'default': 0x00, 'access': 'R/W',
				},
			'P0SEL': {
					'address': 0xF3, 'module': 'IOC',
					'description': 'Port 0 function select. 0: General-purpose I/O. 1: Peripheral function',
				},
			'P1SEL': {
					'address': 0xF4, 'module': 'IOC',
					'description': 'Port 1 function select. 0: General-purpose I/O. 1: Peripheral function',
				},
			'P2SEL': {
					'address': 0xF5, 'module': 'IOC',
					'description': 'Port 2 function select',
					'bitfields': {
						'-reserved': {
								'slice': (7,), 'default': 0, 'access': 'R0',
								'description': 'Reserved',
						},
						'PRI3P1': {
							'slice': (6,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when modules are assigned to the same pins. 0: USART 0 has priority. 1: USART 1 has priority',
						},
						'PRI2P1': {
							'slice': (5,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when PERCFG assigns USART 1 and Timer 3 to the same pins. 0: USART 1 has priority. 1: Timer 3 has priority',
						},
						'PRI1P1': {
							'slice': (4,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when PERCFG assigns Timer 1 and Timer 4 to the same pins. 0: Timer 1 has priority. 1: Timer 4 has priority', },
						'PRI0P1': {
							'slice': (3,), 'default': 0, 'access': 'R/W',
							'description': 'Port 1 peripheral priority control. This bit determines which module has priority in the case when PERCFG assigns USART 0 and Timer 1 to the same pins. 0: USART 0 has priority. 1: Timer 1 has priority',
						},
						'SELP2_4': {
							'slice': (2,), 'default': 0, 'access': 'R/W',
							'description': 'P2.4 function select. 0: General-purpose I/O. 1: Peripheral function',
						},
						'SELP2_3': {
							'slice': (1,), 'default': 0, 'access': 'R/W',
							'description': 'P2.3 function select. 0: General-purpose I/O. 1: Peripheral function',
						},
						'SELP2_0': {
							'slice': (0,), 'default': 0, 'access': 'R/W',
							'description': 'P2.0 function select. 0: General-purpose I/O. 1: Peripheral function',
						},
					},
				},
			'P1INP': {
					'address': 0xF6, 'module': 'IOC',
					'description': 'Port 1 input mode',
					'bitfields': {
							'MDP1_': {
									'slice': (7,2), 'default': 0, 'access': 'R/W',
									'description': 'P1.7 to P1.2 I/O input mode. 0: pullup/pulldown. 1: 3-state',
									### note: the index follows port's!!
							},
							'-reserved': {
									'slice': (1, 0), 'default': 0, 'access': 'R0',
							},
						}
				},
			'P2INP': {
					'address': 0xF7, 'module': 'IOC',
					'description': 'Port 2 input mode',
					'default': 0x00, 'access': 'R/W',
					'bitfields': {
						'PDUP2': {
							'slice': (7,),
							'description': 'Port 2 pullup/pulldown select. Selects function for all Port 2 pins configured as pullup/pulldown inputs. 0: pullup. 1: pulldown.'
						},
						'PDUP1': {
							'slice': (6,),
							'description': 'Port 1 pullup/down select. Selects function for all Port 1 pin configured as pullup/pulldown inputs. 0: pullup. 1: pulldown',
							},
						'PDUP0': {
							'slice': (5,),
							'description': 'Port 0 pullup/pulldown select. Selects function for all Port 0 pins configured as pullup/pulldown inputs. 0: pullup, 1: pulldown.',
						},
						'MDP2_': {
								'slice': (4,0),
								'description': 'P2.4 to P2.0 I/O input mode. 0: Pullup/pulldown. 1: 3-state.',
						},
					},
				},
			'P0DIR': {
					'address': 0xFD, 'module': 'IOC',
					'default': 0x00, 'access': 'R/W',
					'description': 'Port 0 direction. 0: input. 1: output.',
				},
			'P1DIR': {
					'address': 0xFE, 'module': 'IOC',
					'default': 0x00, 'access': 'R/W',
					'description': 'Port 1 direction. 0: input. 1: output.',
				},
			'P2DIR': {
					'address': 0xFF, 'module': 'IOC',
					'description': 'Port 2 direction and Port 0 Peripheral Priority Control',
					'bitfields': {
						'PRIP0': {
								'slice': (7,6), 'default': 0, 'access': 'R/W',
								'description': '''Port 0 peripheral priority control.
These bits determine the order of priority in the case when PERCFG assigns several peripherals to the same pins. Detailed by priority list:
00:
1st priority: USART 0
								2nd priority: USART 1
								3rd priority: Timer 1
								01:
								1st priority: USART 1
								2nd priority: USART 0,
								3rd priority: Timer 1.
								10:
								1st priority: Timer 1 channels 0-1
								2nd priority: USART 1
								3rd priority: USART 0
								4th priority: Timer 1 channels 2-3
								11:
								1st priority: Timer 1 channels 2-3
								2nd priority: USART 0
								3rd priority: USART 1
								4th priority: Timer 1 channels 0-1''',
						},
						'-reserved': {
							'slice': (5,), 'access': 'R0', 'description': 'Reserved',
						},
						'DIRP2': {
							'slice': (4,0), 'access': 'R/W', 'description': 'P2.4 to P2.0 I/O direction. 0: input. 1: output',
						},
					},
				},
			'PMUX': {
					'address': 0xAE, 'module': 'IOC',
					'description': 'Power-down signal mux',
				},
			############## Memory ################
			'RFIRQF1': {
					'address': 0x91, 'module': 'RF',
					'description': 'RF interrupt flags MSB',
				},
			'RFD': {
					'address': 0xD9, 'module': 'RF',
					'description': 'RF data',
				},
			'RFST': {
					'address': 0xE1, 'module': 'RF',
					'description': 'RF command strobe',
				},
			'RFIRQF0': {
					'address': 0xE9, 'module': 'RF',
					'description': 'RF interrupt flags LSB',
				},
			'RFERRF': {
					'address': 0xBF, 'module': 'RF',
					'description': 'RF error interrupt flags',
				},
			'ST0': {
					'address': 0x95, 'module': 'ST',
					'description': 'Sleep Timer 0',
				},
			'ST1': {
					'address': 0x96, 'module': 'ST',
					'description': 'Sleep Timer 1',
				},
			'ST2': {
					'address': 0x97, 'module': 'ST',
					'description': 'Sleep Timer 2',
				},
			'STLOAD': {
					'address': 0x95, 'module': 'ST',
					'description': 'Sleep-timer load status',
				},
			######### Power Management control ##########
			'SLEEPCMD': {
					'address': 0xBE, 'module': 'PMC',
					'description': 'Sleep-mode control command',
					'default': 0x40,
					'bitfields': {
							'OSC32K_CALDIS': {
								'slice': (7,), 'access': 'R/W',
								'description': 'Disable 32-kHz RC oscillator calibration. 0: 32-kHz RC oscillator calibration is enabled. 1: 32-kHz RC oscillator calibration is disabled. This setting can be written at any time, but does not take effect before the chip has been running on the 16-MHz high-frequency RC oscillator.',
							},
							'-reserved1': {
								'slice': (6,3), 'access': 'R0',
								'description': 'Reserved',
							},
							'-reserved2': {
								'slice': (2,), 'access': 'R/W',
								'description': 'Reserved. Always write as 1',
							},
							'MODE': {
								'slice': (1,0), 'access': 'R/W',
								'description': 'Power-mode setting. 00: Active/idle mode. 01: Power mode 1 (PM1). 10: Power mode 2 (PM2).  11: Power mode 3 (PM3)',
							},
					},
				},
			'SLEEPSTA': {
					'address': 0x9D, 'module': 'PMC', 'access': 'R',
					'description': 'Sleep-mode control status',
					'bitfields': {
							'OSC32K_CALDIS': {
									'slice': (7,),
									'default': 0,
									'description': '32-kHz RC oscillator calibration status. SLEEPSTA.OSC32K_CALDIS shows the current status of disabling of the 32-kHz RC calibration.  The bit is not set to the same value as SLEEPCMD.OSC32K_CALDIS before the chip has been run on the 32-kHz RC oscillator.',
							},
							'-reserved1': {
									'slice': (6, 5), 'default': 0, 'description': 'Reserved',
							},
							'RST': {
								'slice': (4,3),
								'description': 'Status bit indicating the cause of the last reset. If there are multiple resets, the register only contains the last event.',
							},
							'-reserved2': {
								'slice': (2,1), 'default': 0, 'description': 'Reserved',
							},
							'CLK32K': {
								'slice': (0,), 'default': 0,
								'description': 'The 32-kHz clock signal (synchronized to the system clock)',
							},
					},
				},
			'CLKCONCMD': {
					'address': 0xC6, 'module': 'PMC',
					'description': 'Clock control command',
					'default': 0xC9, # 11001001
					'access': 'R/W',
					'bitfields': {
							'OSC32K': {
									'slice': (7,),
									'description': '32-kHz clock-source selct. Setting this bit initiates a clock-source change only. CLKCONSTA.OSC32K reflects the current setting. The 16-MHz RCOSC must be selected as system clock when this bit is to be changed. This bit does not give an indication of the stability of the 32-kHz XOSC.',
							},
							'OSC': {
									'slice': (6,),
									'description': 'System clock-source select. Setting this bit initiates a clock-source change only.  CLKCONSTA.OSC reflects the current setting. 0: 32 MHz XOSC, 1: 16 MHz RCOSC.',
							},
							'TICKSPD': {
									'slice': (5,3),
									'description': 'Timer ticks output setting. Cannot be higher than system clock setting given by OSC bit setting. 000: 32 MHz. 001: 16 MHz, 010: 8 MHz, 011: 4 MHz, 100: 2 MHz, 101: 1 MHz, 110: 500 kHz, 111: 250 kHz. Note that CLKCONCMD.TICKSPD can be set to any value, but the effect is limited by the CLKCONCMD.OSC setting; i.e., if CLKCONCMD.OSC = 1 and the CLKCONCMD.TICKSPD = 000, CLKCONSTA.TICKSPD reads 001, and the real TICKSPD is 16 MHz',
							},
							'CLKSPD': {
									'slice': (2,0),
									'description': 'Clock speed. Cannot be higher than system clock setting given by the OSC bit settings.  Indicates current system-clock frequency. 000: 32 Mhz. 001: 16 MHz. 010: 8 MHz. 011: 4 MHz. 100: 2 MHz. 101: 1 MHz. 110: 500 kHz. 111: 250 kHz.  Note that CLKCONCMD.CLKSPD can be set to any value, but the effect is limited by the CLKCONCMD.OSC setting; i.e., if CLKCONCMD.OSC=1 and CLKCONCMD.CLKSPD=000, CLKCONSTA.CLKSPD reads 001, and the real CLKSPD is 16 MHz. Note also that the debugger cannot be used with a divided system clock. When running the debugger, the value of CLKCONCM. CLKSPD should be set to 000 when CLKCONCMD.OSC = 0 or to 001 when CLKCONCMD.OSC = 1',
							},
					},
				},
			'CLKCONSTA': {
					'address': 0x9E, 'module': 'PMC',
					'description': 'Clock control status',
					'default': 0xC5,
					'access': 'R',
					'bitfields': {
							'OSC32K': {
									'slice': (7,),
									'description': 'Current 32-kHz clock source selected: 0: 32-kHz X)SC. 1: 32-kHz RCOSC.'
							},
							'OSC': {
									'slice': (6,),
									'description': 'Current system clock selected: 0: 32-MHz XOSC. 1: 16-MHz RCOSC.',
							},
							'TICKSPD':  {
									'slice': (5,3),
									'description': 'Current timer ticks output settings.  000: 32 MHz. 001: 16 MHz. 010: 8 MHz. 011: 4 MHz.  100: 2 MHz. 101: 500 kHz. 111: 250 kHz',
							},
							'CLKSPD': {
									'slice': (2,0),
									'description': 'Current clock speed.  000: 32 MHz. 001: 16 MHz. 010: 8 MHz. 011: 4 MHz.  100: 2 MHz. 101: 500 kHz. 111: 250 kHz',
							},
						}
				},
			############# Timers #############
			'T1CNTL': {
					'address': 0xE2, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 counter low-order byte. Contains the low byte of the 16-bit timer counter. Writing anything to this register results in the counter being cleared to 0x0000 and initializes all output pins of associated channels.',
				},
			'T1CNTH': {
					'address': 0xE3, 'module': 'Timer 1',
					'description': 'Timer 1 counter high',
				},
			'T1CTL': {
					'address': 0xE4, 'module': 'Timer 1',
					'description': 'Timer 1 control and status',
					'default': 0,
					'bitfields': {
							'-reserved': {
								'slice': (7,4), 'access': 'R0', 'description': 'Reserved',
							},
							'DIV': {
									'slice': (3,2), 'access': 'R/W',
									'description': '''Prescalar divider value. Generates the active clock edge used to update the counter as follows:
00: Tick frequency/1
01: Tick frequency/8
10: Tick frequency/32
11: Tick frequency/128''',
							},
							'MODE': {
									'slice': (1,0), 'access': 'R/W',
									'description': '''Timer 1 mode select. The timer operating mode is selected as follows:
00: Opeeration is suspended.
01: Free-running, repeatedly count from 0x0000 to 0xFFFF.
10: Modulo, repeatedly count from 0x0000 to T1CC0.
11: Up/down, repeatedly count from 0x0000 to T1CC0 and from T1CC0 down to 0x0000.''',
							},
					},
				},
			'T1STAT': {
					'address': 0xAF, 'module': 'Timer 1',
					'description': 'Timer 1 status',
					'bitfields': {
							'-reserved': {
									'slice': (7,6), 'access': 'R0',
									'description': 'Reserved',
							},
							'OVFIF': {
									'slice': (5,), 'access': 'R/W0',
									'description': 'Timer 1 counter-overflow interrupt flag. Set when the counter reaches the terminal count value in free-running or modulo mode, and when zero is reached counting down in up-down mode.  Writing a 1 has no effect.',
							},
							'CH4IF': {
									'slice': (4,), 'access': 'R/W0',
									'description': 'Timer 1 channel 4 interrupt flag.  Set when the channel 4 interrupt condition occurs.  Writing a 1 has no effect.',
							},
							'CH3IF': {
									'slice': (3,), 'access': 'R/W0',
									'description': 'Timer 1 channel 3 interrupt flag.  Set when the channel 3 interrupt condition occurs.  Writing a 1 has no effect.',
							},
							'CH2IF': {
									'slice': (2,), 'access': 'R/W0',
									'description': 'Timer 1 channel 2 interrupt flag.  Set when the channel 2 interrupt condition occurs.  Writing a 1 has no effect.',
							},
							'CH1IF': {
									'slice': (1,), 'access': 'R/W0',
									'description': 'Timer 1 channel 1 interrupt flag.  Set when the channel 1 interrupt condition occurs.  Writing a 1 has no effect.',
							},
							'CH0IF': {
									'slice': (0,), 'access': 'R/W0',
									'description': 'Timer 1 channel 0 interrupt flag.  Set when the channel 0 interrupt condition occurs.  Writing a 1 has no effect.',
							},
					},
				},
			'T2CTRL': {
					'address': 0x94, 'module': 'Timer 2',
					'description': 'Timer 2 control',
				},
			'T2EVTCFG': {
					'address': 0x9C, 'module': 'Timer 2',
					'description': 'Timer 2 event configuration',
				},
			'T2IRQF': {
					'address': 0xA1, 'module': 'Timer 2',
					'description': 'Timer 2 interrupt flags',
				},
			'T2M0': {
					'address': 0xA2, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed register 0',
				},
			'T2M1': {
					'address': 0xA3, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed register 1',
				},
			'T2MOVF0': {
					'address': 0xA4, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed overflow register 0',
				},
			'T2MOVF1': {
					'address': 0xA5, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed overflow register 1',
				},
			'T2MOVF2': {
					'address': 0xA6, 'module': 'Timer 2',
					'description': 'Timer 2 multiplexed overflow register 2',
				},
			'T2IRQM': {
					'address': 0xA7, 'module': 'Timer 2',
					'description': 'Timer 2 interrupt mask',
				},
			'T2MSEL': {
					'address': 0xC3, 'module': 'Timer 2',
					'description': 'Timer 2 multiplex select',
				},
			'T3CCTL0': {
					'address': 0xCC, 'module': 'Timer 3',
					'description': 'Timer 3 channel 0 compare control',
				},
			################## USART ####################
			'U0UCR': {
					'address': 0xC4, 'module': 'USART 0',
					'description': 'USART 0 UART control',
				},
			'U0GCR': {
					'address': 0xC5, 'module': 'USART 0',
					'description': 'USART 0 generic control',
				},


			'U1CSR': {
					'address': 0xF8, 'module': 'USART 1',
					'description': 'USART 1 control and status',
					'bitfields': {
							'MODE': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': '''USART mode select
0: SPI mode
1: UART mode''',
							},
							'RE': {
								'slice': (6,), 'default': 0, 'access': 'R/W',
								'description': '''UART receiver enable. Note: Do not enable receive before UART is fully configured.
0: Receiver disabled
1: Receiver enabled''',
							},
							'SLAVE': {
								'slice': (5,), 'default': 0, 'access': 'R/W',
								'description': '''SPI master or slave mode select
0: SPI mode
1: UART mode''',
							},
							'FE': {
								'slice': (4,), 'default': 0, 'access': 'R/W0',
								'description': '''UART framing error status. This bit is automatically cleared on a read of the U1CSR register or bits in the U1CSR register.
0: No framing error detected
1: Byte received with incorrect stop-bit level''',
							},
							'ERR': {
								'slice': (3,), 'default': 0, 'access': 'R/W0',
								'description': '''UART parity error status. This bit is automatically cleared on a read of the U1CSR register or bits in the U1CSR register
0: No parity error detected
1: Byte received with parity error''',
							},
							'RX_BYTE': {
								'slice': (2,), 'default': 0, 'access': 'R/W0',
								'description': '''Receive byte status. UART mode and SPI slave mode. This bit is automatically cleared when reading U1DBUF; clearing this bit by writing 0 to it effectively discards the data in U1DBUF.
0: No byte received
1: Received byte ready''',
							},
							'TX_BYTE': {
								'slice': (1,), 'default': 0, 'access': 'R/W0',
								'description': '''Transmit byte status. UART mode and SPI master mode
0: Byte not transmitted
1: Last byte written to data-buffer register has been transmitted''',
							},
							'ACTIVE': {
								'slice': (0,), 'default': 0, 'access': 'R/W',
								'description': '''USART transmit/receive active status. In SPI slave mode, this bit equals slave select.
0: USART idle
1: USART busy in transmit or receive mode''',
							},
					},
				},
			'U1DBUF': {
					'address': 0xF9, 'module': 'USART 1',
					'description': 'USART 1 receive/transmit data buffer. When writing this register, the data written is written to the internal transmit-data register. When reading this register, the data from the internal read-data register is read.',
				},
			'U1BAUD': {
					'address': 0xFA, 'module': 'USART 1',
					'description': 'USART 1 baud-rate control. Baud-rate mantissa value. BAUD_E along with BAUD_M decides the UART baud rate and the SPI master SCK clock frequency.',
				},
			'U1UCR': {
					'address': 0xFB, 'module': 'USART 1',
					'description': 'USART 1 UART control',
					'bitfields': {
							'FLUSH': {
								'slice': (7,), 'default': 0, 'access': 'R0/W1',
								'description': 'Flush unit. When set, this event stops the current operation and returns the unit to the idle state.',
							},
							'FLOW': {
								'slice': (6,), 'default': 0, 'access': 'R/W',
								'description': '''UART hardware flow enable. Selects use of hardware flow control with RTS and CTS pins
0: Flow control disabled
1: Flow control enabled''',
							},
							'D9': {
								'slice': (5,), 'default': 0, 'access': 'R/W',
								'description': '''If parity is enabled (see PARITY, bit 3 in this register), then this bit sets the parity level as follows:
0: Odd parity
1: Even parity''',
							},
							'BIT9': {
								'slice': (4,), 'default': 0, 'access': 'R/W',
								'description': '''Set this bit to 1 in order to enable the parity bit transfer (as 9th bit). The content of this 9th bit is given by D9, if parity is enabled by PARITY
0: 8-bit transfer
1: 9-bit transfer''',
							},
							'PARITY': {
								'slice': (3,), 'default': 0, 'access': 'R/W',
								'description': '''UART parity enable. One must set BIT9 in addition to setting this bit for parity to be calculated.
0: Parity disabled
1: Parity enabled''',
							},
							'SPB': {
								'slice': (2,), 'default': 0, 'access': 'R/W',
								'description': '''UART number of stop bits. Selects the number of stop bits to transmit
0: 1 stop bit
1: 2 stop bits''',
							},
							'STOP': {
								'slice': (1,), 'default': 1, 'access': 'R/W',
								'description': '''UART stop-bit level must be different from the start-bit level
0: Low stop bit
1: High stop bit''',
							},
							'START': {
								'slice': (0,), 'default': 0, 'access': 'R/W',
								'description': '''UART start-bit level. Ensure that the polarity of the start bit is opposit the level of the idle line.
0: Low start bit
1: High start bit''',
							},
					},
				},
			'U1GCR': {
					'address': 0xFC, 'module': 'USART 1',
					'description': 'USART 1 generic control',
					'bitfields': {
							'CPOL': {
								'slice': (7,), 'default': 0, 'access': 'R/W',
								'description': '''SPI clock polarity
0: Negative clock polarity
1: Positive clock polarity''',
							},
							'CPHA': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
									'description': '''SPI clock phase
0: Data is output on MOSI when SCK goes from CPOL inverted to CPOL, and data input is sampled on MISO when SCK goes from CPOL to CPOL inverted.
1: Data is output on MOSI when SCK goes from CPOL to CPOL inverted, and data input is sampled on MISO when SCK goes from CPOL inverted to CPOL.''',
							},
							'ORDER': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
									'description': '''Bit order for transfers
0: LSB first
1: MSB first''',
							},
							'BAUD_E': {
									'slice': (4,0), 'default': 0, 'access': 'R/W',
									'description': 'Baud rate exponent value. BAUD_E along with BAUD_M determines the UART baud rate and the SPI master SCK clock frequency.'
							},
					},


				},

			############ Watchdog Timer #############
			'WDCTL': {
					'address': 0xC9, 'module': 'WDT',
					'description': 'Watchdog Timer control',
					'bitfields': {
							'CLR': {
								'slice': (7,4), 'default': 0, 'access': 'R0/W',
								'description': 'Clear timer. In watchdog mode, when 0xA followed by 0x5 is written to these bits, the timer is cleared (i.e. loaded with 0). Note that the timer is only cleared when 0x5 is written within one watchdog clock period after 0xA was written. Writing these bits when the Watchdog Timer is IDLE has no effect. When operating in timer mode, the timer can be cleared to 0x0000 (but not stopped) by writing 1 to CLR[0] (the other 3 bits are dont-care)',
							},
							'MODE': {
								'slice': (3,2), 'default': 0, 'access': 'R/W',
								'description': '''Mode select. These bits are used to start the WDT in watchdog mode or timer mode. Setting these bits to IDLE stops the timer when in timer mode.  Note: to switch to watchdog mode when operating in timer mode, first stop the WDT - then start the WDT in Watchdog mode. When operating in Watchdog mode, writing these bits has no effect.
00: IDLE
01: Reserved
10: Watchdog mode
11: Timer mode''',
							},
							'INT': {
								'slice': (1,0), 'default': 0, 'access': 'R/W',
								'description': '''Timer interval select. These bits select the timer interval, which is defined as a given number of 32-kHz oscillator periods. Note that the interval can only be changed when the WDT is IDLE, so the interval must be set at the same time as the timer is started.
00: Clock period x 32768 (~1 s) when running the 32-Hz XOSC
01: Clock period x 8192 (~0.25 s)
10: Clock period x 512 (~15.625 ms)
11: Clock period x 64 (~1.9 ms)
For CC253x and CC2540, when clock division is enabled through CLKCONCMD.CLKSPD, the length of the watchdog timer interval is reduced by a factor equal to the current oscillator clock frequency divided by the set clock speed. E.g., if 32-MHz crystal is selected and clock speed is set to 4 Mhz, then the watchdog timeout is reduced by a factor of 32 MHz / 4 MHz = 8. If the watchdog interval set by WDCTL.INT was 1 s, nominally it is 1/8 s with this clock division factor. For CC2541, the watchdog timer interval is independent of the clock division rate.''',
							},
					},
				},
			}


	# additional registers in XDATA memory space, mainly for radio
	# configuration and control and I2C on CC2541.
	# taken from the # data sheet "swru191d.pdf", page 32-,
	# Table 2-2 "Overview of XREG Registers".
	#
	# Specific references are from Section 24.1, Section 21.12, ..
	# but these should not be accessed by the user code directly.
	_XREG = {
			################ ADC ##############
			'RFSTAT': {  ### Not user accessible
					'address': 0x618D, 'module': 'RF',
					'description': 'RF Core Status',
				},
			'RFC_OBS': {  ### Not user accessible
					'address': 0x61AE, 'module': 'RF',
					'description': 'RF Observation Mux Control 0',
				},
			'RFC_OBS_CTRL1': {  #### Not user accessible
					'address': 0x61AF, 'module': 'RF',
					'description': 'RF Observation Mux Control 1',
				},
			'RFC_OBS_CTRL2': {  #### Not user accessible
					'address': 0x61B0, 'module': 'RF',
					'description': 'RF Observation Mux Control 2',
				},
			'ATEST': {  #### Not user accessible
					'address': 0x61A9, 'module': 'RF',
					'description': 'Analog Test Control',
				},
			################# OPAMP #################
			'OPAMPMC': {
					'address': 0x61AD, 'module': 'OPAMP',
					'description': 'Operational amplifier mode control',
					'bitfields': {
							'-reserved': {
									'slice': (7,2), 'default': 0, 'access': 'R/W',
									'description': 'Reserved. Always write 0000 00',
							},
							'MODE': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Operational amplifier mode
00 and 01: Non-chop mode -- Higher offset (~500 uV), but no chopper ripple. Use in conjunction with Mode 10 if offset cancellation is required. Offset for these two modes is the opposite of the offset seen in Mode 10.
10: Non-chop mode -- Higher offset (~500 uV), but no chopper ripple.  Use in conjunction with Mode 00 or Mode 01 to double sample and correct for the offset by averaging the two samples.
11: Chop mode -- Very low offset (~50 uV), and very low noise (1/f noise shifted to 1 Mhz due to chopping), and 1 Mhz ripple''',
							},
					},
				},
			############# skipping I2C -- not on CC2540 #########
			########## observation output control register #########
			'OBSSEL0': {
					'address': 0x6243, 'module': 'OBSCTL',
					'description': 'Observation output control register 0',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'EN': {
								'slice': (7,),
								'description': 'Bit controlling the observation output 0 on P1[0]. 0: observation output disabled. 1: observation output enabled. Note: If enabled, this overwrites the standard GPIO behavior of P1.0',
							},
							'SEL': {
									'slice': (6,0),
									'description': '''Select output signal on observation output 0.
111 1011 (123): rfc_obs_sig0
111 1100 (124): rfc_obs_sig1
111 1101 (125): rfc_obs_sig2
Others: Reserved
''',
							},
					},
				},
			'OBSSEL1': {
					'address': 0x6244, 'module': 'OBSCTL',
					'description': 'Observation output control register 1',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'EN': {
								'slice': (7,),
								'description': '''Bit controlling observation output 1 on P1[1].
0: observation output disabld
1: observation output enabled
Note: if enabled, this overwrites the standard GPIO behavior of P1.1.'''
							},
							'SEL': {
								'slice': (6,0),
								'description': '''Select output signal on observation output 1
111 1011 (123) rfc_obs_sig0
111 1110 (124) rfc_obs_sig1
111 1101 (125) rfc_obs_sig2
Others: Reserved''',
							},
					},
				},
			'OBSSEL2': {
					'address': 0x6245, 'module': 'OBSCTL',
					'description': 'Observation output control register 2',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'EN': {
								'slice': (7,),
								'description': '''Bit controlling observation output 1 on P1[2].
0: observation output disabld
1: observation output enabled
Note: if enabled, this overwrites the standard GPIO behavior of P1.2.'''
							},
							'SEL': {
								'slice': (6,0),
								'description': '''Select output signal on observation output 2
111 1011 (123) rfc_obs_sig0
111 1110 (124) rfc_obs_sig1
111 1101 (125) rfc_obs_sig2
Others: Reserved''',
							},
					},
				},
			'OBSSEL3': {
					'address': 0x6246, 'module': 'OBSCTL',
					'description': 'Observation output control register 3',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'EN': {
								'slice': (7,),
								'description': '''Bit controlling observation output 3 on P1[3].
0: observation output disabld
1: observation output enabled
Note: if enabled, this overwrites the standard GPIO behavior of P1.3.'''
							},
							'SEL': {
								'slice': (6,0),
								'description': '''Select output signal on observation output 3
111 1011 (123) rfc_obs_sig0
111 1110 (124) rfc_obs_sig1
111 1101 (125) rfc_obs_sig2
Others: Reserved''',
							},
					},
				},
			'OBSSEL4': {
					'address': 0x6247, 'module': 'OBSCTL',
					'description': 'Observation output control register 4',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'EN': {
								'slice': (7,),
								'description': '''Bit controlling observation output 4 on P1[4].
0: observation output disabld
1: observation output enabled
Note: if enabled, this overwrites the standard GPIO behavior of P1.4.'''
							},
							'SEL': {
								'slice': (6,0),
								'description': '''Select output signal on observation output 4
111 1011 (123) rfc_obs_sig0
111 1110 (124) rfc_obs_sig1
111 1101 (125) rfc_obs_sig2
Others: Reserved''',
							},
					},
				},
			'OBSSEL5': {
					'address': 0x6248, 'module': 'OBSCTL',
					'description': 'Observation output control register 5',
					'default': 0, 'access': 'R/W',
					'bitfields': {
							'EN': {
								'slice': (7,),
								'description': '''Bit controlling observation output 5 on P1[5].
0: observation output disabld
1: observation output enabled
Note: if enabled, this overwrites the standard GPIO behavior of P1.5.'''
							},
							'SEL': {
								'slice': (6,0),
								'description': '''Select output signal on observation output 5
111 1011 (123) rfc_obs_sig0
111 1110 (124) rfc_obs_sig1
111 1101 (125) rfc_obs_sig2
Others: Reserved''',
							},
					},
				},
			'CHVER': {
					'address': 0x6249, 'module': 'Flash',
					'description': 'Chip version',
					'access': 'R',
				},
			'CHIPID': {
					'address': 0x624A, 'module': 'Flash',
					'description': 'Chip identification. CC2530: 0xA5. CC2531: 0xB5. CC2533: 0x95. CC2540: 0x8D. CC2541: 0x41',
					'access': 'R',
				},
			'TR0': {
					'address': 0x624B, 'module': 'Test',
					'description': 'Test register 0',
					'bitfields': {
							'-reserved': {
									'slice': (7,1),
									'default': 0, 'access': 'R0',
									'description': 'Reserved. Write as 0',
							},
							'ADCTM': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
									'description': 'Set to 1 to connect the temperature sensor to the SOC-ADC. See also ATEST register description to enable the temperature sensor',
								},
					},
				},
			'DBGDATA': {
					'address': 0x6260, 'module': 'Test',
					'description': 'Debug interface write data',
					'default': 0x00, 'access': 'R',
				},

#			'SRCRC': {  ### CC2533 and CC2541 only
#					'address': 0x6262,
#					'description': 'Sleep reset CRC',
#				},
			'BATTMON': {
					'address': 0x6264, 'module': 'Battery Monitor',
					'description': 'Battery monitor',
				},
			'IVCTRL': {
					'address': 0x6265, 'module': 'Analog Control',
					'description': 'Analog control register',
				},
			'FCTL': {
					'address': 0x6270, 'module': 'Flash',
					'description': 'Flash control',
					'bitfields': {
						'BUSY': {
								'slice': (7,), 'access': 'R', 'default': 0,
								'description': 'Indicates that write or erase is in operation. This flag is set when the WRITe or ERASE bit is set. 0: No write or erase operation active. 1: Write or erase operation activated.',
						},
						'FULL': {
								'slice': (6,), 'access': 'R/H0',
								'description': 'Write buffer-full status. This flag is set when 4 bytes have been written to FWDATA during flash write. The write buffer is then full and does not accept more data; i.e., writes to FWDATA are ignored when the FULL flag is set. The full flag is cleared when the write buffer again is ready to receive 4 more bytes. This flag is only needed when the CPU is used to write to the flash.',
						},
						'ABORT': {
								'slice': (5,), 'access': 'R/H0', 'default': 0,
								'description': 'Abort status. This bit is set when a write operation or page erase is aborted. An operation is aborted when the page accessed is locked. The abort bit is cleared when a write or page erase is started.',
						},
						'-reserved': {
								'slice': (4,), 'access': 'R',
						},
						'CM': {
							'slice': (3,2), 'access': 'R/W', 'default': 0b01,
							'description': 'Cache mode. 00: Cache disabled. 01: Cache enabled. 10: Cache enabledf, prefetch mode. 11: Cache enabled, real-time mode. Cache mode. Disabling the cahce increases the power consumption and reduces performance. Prefetching , for most applications, improves performance by up to 33% at the expense of potentially increasing power consumption. Real-time mode provides predictable flash-read access time; the execution time is equal to that in cahce-disabled mode, but the power consumption is lower.',
						},
						'WRITE': {
								'slice': (1,), 'access': 'R/W1/H0', 'default': 0,
								'description': 'Write. Start writing word at location given by FADDRH:FADDRL. The WRITE bit stays at 1 until the write completes. The clearing of this bit indicates that the erase has completed, i.e., it has timed out or aborted. If ERASE is also set to 1, a page erase of the whole page addressed by FADDRH[7:1] is performed before the write. SettingWRITE to 1 when ERASE is 1 has no effect.',
						},
						'ERASE': {
							'slice': (0,), 'access': 'R/W1/H0', 'default': 0,
							'description': 'Page erase. Erase the page that is given by FADDRH[7:1] (CC2530/CC2531/CC2540/CC2541) or FADDRH[6:0] (CC2533). The ERASE bit stays at 1 until the erase completes. The clearing of this bit indicates that the erase has completed successfully or aborted. Setting ERASE to 1 when WRITE is 1 has no effect.',
						},
					},
				},
			'FADDRL': {
					'address': 0x6271, 'module': 'Flash',
					'description': 'Flash address low. Low byte of flash word address.',
					'access': 'R/W',
					'default': 0x00,
				},
			'FADDRH': {
					'address': 0x6272, 'module': 'Flash',
					'description': 'Flash address high. Page address/high byte of flash word address. Bits [7:1] (CC2530/2531/2540/2541) or bits [6:0] (CC2533) select which page to access',
					'access': 'R/W',
					'default': 0x00,
				},
			'FWDATA': {
					'address': 0x6273, 'module': 'Flash',
					'description': 'Flash write data. This register can only be written to when FCTL.WRITE is 1.',
					'access': 'R0/W', 'default': 0x00,
				},
			'CHIPINFO0': {
					'address': 0x6276, 'module': 'Flash',
					'description': 'Chip information byte 0',
					'bitfields': {
						'-reserved1': {
							'slice': (7,), 'default': 0, 'access': 'R0',
							'description': 'Reserved.  Always 0.' },
						'FLASHSIZE': {
							'slice': (6,4), 'access': 'R',
							'description': 'Flash size. 001 = 32KB, 010 = 64KB, 011 = 128KB (for CC2533: 011 = 96KB), 100 = 256KB',
						},
						'USB': {
							'slice': (3,), 'access': 'R',
							'description': '1 if chip has USB, 0 otherwise',
						},
						'-reserved2': {
							'slice': (2,), 'default': 1, 'access': 'R1',
							'description': 'Reserved. always 1',
						},
						'-reserved3': {
							'slice': (1,0), 'default': 0, 'access': 'R0',
							'description': 'Reserved. always 00',
						},
					},
				},
			'CHIPINFO1': {
					'address': 0x6277, 'module': 'Flash',
					'description': 'Chip information byte 1',
					'access': 'R',
					'bitfields': {
							'-reserved': {
								'slice': (7,3), 'description': 'Reserved',
							},
							'SRAMSIZE': {
								'slice': (2,0), 'description': 'SRAM size in KB minus 1. For example, a 4-KB device has this field set to 011. Add 1 to the number to get the number of KB available.'
							},
					},
				},
			'IRCTL': {
					'address': 0x6281, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 IR generation control',
					'bitfields': {
							'-reserved': {
									'slice': (7,1), 'description': 'Reserved',
							},
							'IRGEN': {
								'slice': (0,), 'description': 'When this bit is set, a connection between Timer 3 channel 1 and Timer 1 tick input is made so that the timers can be used to generate modulated IR codes',
							},
					},
				},
			'CLD': {
					'address': 0x6290, 'module': 'CPU',
					'description': 'Clock-loss detection',
					'default': 0x00,
					'bitfields': {
						'-reserved': {
								'slice': (7,1), 'access': 'R0', 'description': 'Reserved',
						},
						'EN': {
							'slice': (0,), 'access': 'R/W',
							'description': 'Clock-loss detector enable',
						}
					},
				},
			'T1CCTL0': {
					'address': 0x62A0, 'module': 'Timer 1',
					'description': 'Timer 1 channel 0 capture/compare control (additional XREG mapping of SFR register at 0xE5)',
				},
			'T1CCTL1': {
					'address': 0x62A1, 'module': 'Timer 1',
					'description': 'Timer 1 channel 1 capture/compare control (additional XREG mapping of SFR register at 0xE6)',
				},
			'T1CCTL2': {
					'address': 0x62A2, 'module': 'Timer 1',
					'description': 'Timer 1 channel 2 capture/compare control (additional XREG mapping of SFR register at 0xE7)',
				},
			'T1CCTL3': {
					'address': 0x62A3, 'module': 'Timer 1',
					'description': 'Timer 1 channel 3 capture/compare control',
					'bitfields': {
							'RFIRQ': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
									'description': 'When set, use RF interrupt for capture instead of regular capture input.',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': 'Channel 3 interrupt mask. Enables interrupt request when set.',
							},
							'CMP': {
								'slice': (5,3), 'default': 0, 'access': 'R/W',
								'description': '''Channel 3 compare-mode select.  Selects action on output when timer value equals compare value in T1CC3.
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on compare-down in up-down mode.  Otherwise set output on compare, clear on 0.
100: Clear output on compare-up, set on compare-down in up-down mode.  Otherwise clear output on compare, set on 0.
101: Clear when equal T1CC0, set when equal T1CC3
110: Set when equal T1CC0, clear when equal T1CC3
111: Initialize output pin. CMP[2:0] is not changed.''',
							},
							'MODE': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
									'description': '''Mode. Select Timer 1 channel 3 capture or compare mode
0: Capture mode
1: Compare mode''',
							},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Channel 3 capture-mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on all edges''',
							}
					},
				},
			'T1CCTL4': {
					'address': 0x62A4, 'module': 'Timer 1',
					'description': 'Timer 1 channel 4 capture/compare control',
					'bitfields': {
							'RFIRQ': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
									'description': 'When set, use RF interrupt for capture instead of regular capture input.',
							},
							'IM': {
									'slice': (6,), 'default': 1, 'access': 'R/W',
									'description': 'Channel 4 interrupt mask. Enables interrupt request when set.',
							},
							'CMP': {
								'slice': (5,3), 'default': 0, 'access': 'R/W',
								'description': '''Channel 4 compare-mode select.  Selects action on output when timer value equals compare value in T1CC4.
000: Set output on compare
001: Clear output on compare
010: Toggle output on compare
011: Set output on compare-up, clear on compare-down in up-down mode.  Otherwise set output on compare, clear on 0.
100: Clear output on compare-up, set on compare-down in up-down mode.  Otherwise clear output on compare, set on 0.
101: Clear when equal T1CC0, set when equal T1CC4
110: Set when equal T1CC0, clear when equal T1CC4
111: Initialize output pin. CMP[2:0] is not changed.''',
							},
							'MODE': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
									'description': '''Mode. Select Timer 1 channel 4 capture or compare mode
0: Capture mode
1: Compare mode''',
							},
							'CAP': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Channel 4 capture-mode select
00: No capture
01: Capture on rising edge
10: Capture on falling edge
11: Capture on all edges''',
							}
					},
				},
			'T1CC0L': {
					'address': 0x62A6, 'module': 'Timer 1',
					'description': 'Timer 1 channel 0 capture/compare value low (additional XREG mapping of SFR register)',
				},
			'T1CC0H': {
					'address': 0x62A7, 'module': 'Timer 1',
					'description': 'Timer 1 channel 0 capture/compare value high (additional XREG mapping of SFR register)',
				},
			'T1CC1L': {
					'address': 0x62A8, 'module': 'Timer 1',
					'description': 'Timer 1 channel 1 capture/compare value low (additional XREG mapping of SFR register)',
				},
			'T1CC1H': {
					'address': 0x62A9, 'module': 'Timer 1',
					'description': 'Timer 1 channel 1 capture/compare value high (additional XREG mapping of SFR register at 0xDD)',
				},
			'T1CC2L': {
					'address': 0x62AA, 'module': 'Timer 1',
					'description': 'Timer 1 channel 2 capture/compare value low (additional XREG mapping of SFR register)',
				},
			'T1CC2H': {
					'address': 0x62AB, 'module': 'Timer 1',
					'description': 'Timer 1 channel 2 capture/compare value high (additional XREG mapping of SFR register)',
				},
			'T1CC3L': {
					'address': 0x62AC, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 3 capture/compare value low-order byte. Data written to this register is stored in a buffer but not written to T1CC3[7:0] until, and at the same time as, a later write to T1CC3H takes effect.',
				},
			'T1CC3H': {
					'address': 0x62AD, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 3 capture/compare value high-order byte. Writing to this register when T1CCTL3.MODE=1 (compare mode) causes the T1CC3[15:0] update to the written value to be delayed until T1CNT=0x0000',
				},
			'T1CC4L': {
					'address': 0x62AE, 'module': 'Timer 1',
					'description': 'Timer 1 channel 4 capture/compare value low-order byte. Data written to this register is stored in a buffer but not written to T1CC4[7:0] until, and at the same time as, a later write to T1CC4H takes effect.',
				},
			'T1CC4H': {
					'address': 0x62AF, 'module': 'Timer 1',
					'default': 0, 'access': 'R/W',
					'description': 'Timer 1 channel 4 capture/compare value high-order byte. Writing to this register when T1CCTL4.MODE=1 (compare mode) causes the T1CC4[15:0] update to the written value to be delayed until T1CNT=0x0000.',
				},
			'STCC': {
					'address': 0x62B0, 'module': 'SleepTimer',
					'description': 'Sleep Timer capture control',
					'bitfields': {
							'-reserved': {
									'slice': (7,5), 'default': 0, 'access': 'R/W',
									'description': 'Reserved',
							},
							'PORT': {
									'slice': (4,3), 'default': 0b11, 'access': 'R',
									'description': 'Port select. Valid settings are 0-2.  Capture is disabled when set to 3, i.e., an invalid setting is selected.',
							},
							'PIN': {
									'slice': (2,0), 'default': 0b111,
									'description': 'Pin select. Valid settings are 0-7 when PORT[1:0] is 0 or 1, 0-5 when Port[1:0] is 2.  Capture is disabled when an invalid setting is selected.',
							},
					},
				},
			'STCS': {
					'address': 0x62B1, 'module': 'SleepTimer',
					'description': 'Sleep Timer capture status',
					'bitfields': {
							'-reserved': {
									'slice': (7,1), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
							},
							'VALID': {
									'slice': (0,), 'default': 0, 'access': 'R/W0',
									'description': 'Capture valid flag. Set to 1 when capture value in STCV has been updated. Cleare explicitly to allow new capture',
							},
					},
				},
			'STCV0': {
					'address': 0x62B2, 'module': 'SleepTimer',
					'default': 0, 'access': 'R',
					'description': 'Sleep Timer capture value byte 0',
				},
			'STCV1': {
					'address': 0x62B3, 'module': 'SleepTimer',
					'default': 0, 'access': 'R',
					'description': 'Sleep Timer capture value byte 1',
				},
			'STCV2': {
					'address': 0x62B4, 'module': 'SleepTimer',
					'default': 0, 'access': 'R',
					'description': 'Sleep Timer capture value byte 2',
				},
			'OPAMPC': {
					'address': 0x62C0, 'module': 'OpAmp',
					'description': 'Operational amplifier control',
					'bitfields': {
							'-reserved': {
									'slice': (7,2), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
							},
							'CAL': {
									'slice': (1,), 'default': 0, 'access': 'W1/R0',
									'description': 'Start calibration. Calibration only starts if OPAMPC.EN is 1',
							},
							'EN': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
									'description': 'Operational amplifier enable',
							},
					},
				},
			'OPAMPS': {
					'address': 0x62C1, 'module': 'OpAmp',
					'description': 'Operational amplifier status',
					'bitfields': {
							'-reserved': {
								'slice': (7,1), 'default': 0, 'access': 'R0',
								'description': 'Reserved',
							},
							'CAL_BUSY': {
									'slice': (0,), 'default': 0, 'access': 'R',
									'description': 'calibration in progress',
							},
						},
				},
			'CMPCTL': {
					'address': 0x62D0, 'module': 'AnalogComparator',
					'description': 'Analog comparator control and status',
					'bitfields': {
							'-reserved': {
									'slice': (7,2), 'default': 0, 'access': 'R0',
									'description': 'Reserved',
							},
							'EN': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
									'description': 'Comparator enable',
							},
							'OUTPUT': {
									'slice': (0,), 'default': 0, 'access': 'R',
									'description': 'Comparator output',
							},
					},

				},
				'USBADDR': {
						'address': 0x6200, 'description': 'USB function address',
						'module': 'USB',
						'bitfields': {
								'UPDATE': {
											'slice': (7,), 'default': 0, 'access': 'R',
											'description': 'This bit is set when the USBADDR register is written and cleared when the address becomes effective',
								},
								'USBADDR': {
											'slice': (6,0), 'default': 0, 'access': 'R/W',
											'description': 'Device address',
								},
						},
					},
				'USBPOW': {
							'address': 0x6201,
							'description': 'USB power/control register',
							'module': 'USB',
							'bitfields': {
										'ISL_WAIT_SOF': {
												'slice': (7,), 'default': 0, 'access': 'R/W',
												'description': 'When this bit is set to 1, the USB controller sends zero-length data packets from the time INPKT_RDY is asserted and until the first SOF token has been received. This only applies to isochronous endpoints.',
										},
										'-reserved': {
												'slice': (6,4), 'default': 0, 'access': 'R0',
												'description': 'Reserved',
										},
										'RST': {
												'slice': (3,), 'default': 0, 'access': 'R',
												'description': 'During reset signaling, this bit is set to 1',
											},
										'RESUME': {
												'slice': (2,), 'default': 0, 'access': 'R/W',
												'description': 'Drives resume signaling for remote wakeup. According to the USB Specification, the duration of driving resume must be at least 1 ms and no more than 15 ms.  It is recommended to keep this bit set for apprixmiately 10 ms.',
										},
										'SUSPEND': {
												'slice': (1,), 'default': 0, 'access': 'R',
												'description': 'Suspend mode entered. This bit is only used when SUSPEND_EN = 1. Read the USBCIF register or asserting RESUME clears this bit.',
										},
										'SUSPEND_EN': {
												'slice': (0,), 'default': 0, 'access': 'R/W',
												'description': 'Suspend enable. When this bit is set to 1, suspend mode is entered when the USB has been idle for 3 ms',
										},
							},
					},
				'USBIIF': {
							'address': 0x6202, 'module': 'USB',
							'description': 'USB IN Endpoints and EP0 Interrupt Flags',
							'bitfields': {
									'-reserved': {
											'slice': (7,6), 'default': 0, 'access': 'R0',
											'description': 'Reserved',
									},
									'INEP5IF': {
											'slice': (5,), 'default': 0, 'access': 'R, H0',
											'description': 'Interrupt flag for IN endpoint 5. Cleared by hardware when read.',
									},
									'INEP4IF': {
											'slice': (4,), 'default': 0, 'access': 'R, H0',
											'description': 'Interrupt flag for IN endpoint 4. Cleared by hardware when read.',
									},
									'INEP3IF': {
											'slice': (3,), 'default': 0, 'access': 'R, H0',
											'description': 'Interrupt flag for IN endpoint 3. Cleared by hardware when read.',
									},
									'INEP2IF': {
											'slice': (2,), 'default': 0, 'access': 'R, H0',
											'description': 'Interrupt flag for IN endpoint 2. Cleared by hardware when read.',
									},
									'INEP1IF': {
											'slice': (1,), 'default': 0, 'access': 'R, H0',
											'description': 'Interrupt flag for IN endpoint 1. Cleared by hardware when read.',
									},
									'EP0IF': {
											'slice': (0,), 'default': 0, 'access': 'R, H0',
											'description': 'Interrupt flag for endpoint 0. Cleared by hardware when read.',
									},
							},
					},
				'USBOIF': {
						'address': 0x6204, 'module': 'USB',
						'description': 'OUT-Endpoint Interrupt Flags',
						'bitfields': {
								'-reserved1': {
											'slice': (7,6), 'access': 'R0',
											'description': 'Reserved',
									},
								'OUTEP5IF': {
										'slice': (5,), 'access': 'R, H0', 'default': 0,
										'description': 'Interrupt flag for OUT endpoint 5.  Cleared by hardware when read',
									},
								'OUTEP4IF': {
										'slice': (4,), 'access': 'R, H0', 'default': 0,
										'description': 'Interrupt flag for OUT endpoint 4.  Cleared by hardware when read',
									},
								'OUTEP3IF': {
										'slice': (3,), 'access': 'R, H0', 'default': 0,
										'description': 'Interrupt flag for OUT endpoint 3.  Cleared by hardware when read',
									},
								'OUTEP2IF': {
										'slice': (2,), 'access': 'R, H0', 'default': 0,
										'description': 'Interrupt flag for OUT endpoint 2.  Cleared by hardware when read',
									},
								'OUTEP1IF': {
										'slice': (1,), 'access': 'R, H0', 'default': 0,
										'description': 'Interrupt flag for OUT endpoint 1.  Cleared by hardware when read',
									},
								'OUTEP0IF': {
										'slice': (0,), 'access': 'R, H0', 'default': 0,
										'description': 'Interrupt flag for OUT endpoint 0.  Cleared by hardware when read',
									},
								'-reserved0': {
											'slice': (0,), 'access': 'R0',
											'description': 'Reserved',
									},
							},
					},
				'USBIIE': {
						'address': 0x6207, 'module': 'USB',
						'description': 'IN Endpoints and EP0 Interrupt-Enable Mask',
						'bitfields': {
								'-reserved': {
									'slice': (7,6), 'default': 0, 'access': 'R/W',
									'description': 'Reserved. Always write 00',
								},
								'INEP5IE': {
										'slice': (5,), 'default': 1, 'access': 'R/W',
										'description': '''IN endpoint-5 interrupt enable
0: Interrupt disabled
1: Interrupt enabled''',
									},
								'INEP4IE': {
										'slice': (4,), 'default': 1, 'access': 'R/W',
										'description': '''IN endpoint-4 interrupt enable
0: Interrupt disabled
1: Interrupt enabled''',
									},
								'INEP3IE': {
										'slice': (3,), 'default': 1, 'access': 'R/W',
										'description': '''IN endpoint-3 interrupt enable
0: Interrupt disabled
1: Interrupt enabled''',
									},
								'INEP2IE': {
										'slice': (2,), 'default': 1, 'access': 'R/W',
										'description': '''IN endpoint-2 interrupt enable
0: Interrupt disabled
1: Interrupt enabled''',
									},
								'INEP1IE': {
										'slice': (1,), 'default': 1, 'access': 'R/W',
										'description': '''IN endpoint-1 interrupt enable
0: Interrupt disabled
1: Interrupt enabled''',
									},
								'INEP0IE': {
										'slice': (0,), 'default': 1, 'access': 'R/W',
										'description': '''IN endpoint-0 interrupt enable
0: Interrupt disabled
1: Interrupt enabled''',
									},
							},
					},
				'USBOIE': {
						'address': 0x6209,  'module': 'USB', 
						'description': 'Out Endpoints Interrupt Enable Mask',
						'bitfields':  {
								'-reserved1': {
										'slice': (7,6), 'default': 0, 'access': 'R/W',
										'description': 'Reserved. Always write 00',
									},
								'OUTEP5IE': {
										'slice': (5,), 'default': 1, 'access': 'R/W',
										'description': '''OUT endpoint 5 interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'OUTEP4IE': {
										'slice': (4,), 'default': 1, 'access': 'R/W',
										'description': '''OUT endpoint 4 interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'OUTEP3IE': {
										'slice': (3,), 'default': 1, 'access': 'R/W',
										'description': '''OUT endpoint 3 interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'OUTEP2IE': {
										'slice': (2,), 'default': 1, 'access': 'R/W',
										'description': '''OUT endpoint 2 interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'OUTEP1IE': {
										'slice': (1,), 'default': 1, 'access': 'R/W',
										'description': '''OUT endpoint 1 interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'-reserved0': {
										'slice': (0,), 'default': 1, 'access': 'R0',
										'description': 'Reserved',
									},
							},
					},
				'USBCIE': {
						'address': 0x620B, 'module': 'USB',
						'description': 'Common USB Interrupt-Enable Mask',
						'bitfields': {
								'-reserved': {
										'slice': (7,4), 'access': 'R0',
										'description': 'Reserved',
									},
								'SOFIE': {
										'slice': (3,), 'access': 'R/W', 'default': 0,
										'description': '''Start-of-frame interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'RSTIE': {
										'slice': (2,), 'access': 'R/W', 'default': 1,
										'description': '''Reset interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'RESUMEIE': {
										'slice': (1,), 'access': 'R/W', 'default': 1,
										'description': '''Resume interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
								'SUSPENDIE': {
										'slice': (0,), 'access': 'R/W', 'default': 0,
										'description': '''Suspend interrupt enable
0: interrupt disabled
1: interrupt enabled''',
									},
							},
					},
				'USBFRML': {
						'address': 0x620C, 'module': 'USB',
						'description': 'Current Frame Number (Low Byte of 11-bit)',
						'default': 0, 'access': 'R',
					},
				'USBFRMH': {
						'address': 0x620D, 'module': 'USB',
						'description': 'Current Frame Number (High Byte of 11-bit)',
						'bitfields': {
								'-reserved': {
										'slice': (7,3), 'access': 'R0',
										'description': 'Reserved',
									},
								'FRAME': {
									'slice': (2,0), 'access': 'R', 'default': 0,
									'description': '3 MSBs of 11-bit frame number',
									},
							},
					},
				'USBINDEX': {
						'address': 0x620E, 'module': 'USB',
						'description': 'Current-Endpoint Index Register',
						'bitfields': {
								'-reserved': {
										'slice': (7,4), 'access': 'R0', 
										'description': 'Reserved',
									},
								'USBINDEX': {
										'slice': (3,0), 'access': 'R/W', 'default': 0,
										'description': 'Endpoint selected. Must be set to a value in the range 0-5',
									},
							},
					},
				'USBCTRL': {
						'address': 0x620F, 'module': 'USB', 
						'description': 'USB Control Register',
						'bitfields': {
								'PLL-LOCKED': {
										'slice': (7,), 'default': 0, 'access': 'R',
										'description': 'PLL locked status',
									},
								'-reserved0': {
										'slice': (6,3), 'access': 'R0',
										'description': 'Reserved',
									},
								'-reserved1': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': 'Reserved. Always write 0',
									},
								'PLL_EN': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description': '''48-MHz USB PLL enabled. When this bit is set, the 48-MHz PLL is started.  However, the USB must not be accessed before the PLL has locked, i.e., PLL_LOCKED is 1. This bit can only be set when USB_EN = 1.
Note: The PLL must be disabled before exiting active and re-enabled after entering active mode.''',
									},
								'USB_EN': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
									'description': 'USB enable. The USB controller is reset when writing 0 to this bit',
									},
							},
					},
				'USBMAXI': {
						'address': 0x6210, 'module': 'USB',
						'description': 'Max. Packet Size for IN Endpoint (1-5)',
						'default': 0, 'access': 'R/W',
						'description': '''Maximum packet size, in units of 8 bytes, for IN endpoint selected by USBINDEX register. The value of this register should correspond to the wMaxPacketSize field in the standard endpoint descriptor for the endpoint. This register must not be set to a value greater than the available FIFO memory for the endpoint.''',
					},
				'USBCS0': {
						'address': 0x6211, 'module': 'USB',
						'description': 'EP0 Control and Status (USBINDEX = 0)',
						'bitfields': {
							'CLR_SETUP_END': {
								'slice': (7,), 'default': 0, 'access': 'R/W H0',
								'description': 'Set this bit to 1 to de-assert the SETUP_END bit of this register. This bit is cleared automatically.'
								},
							'CLR_OUTPKT_RDY': {
								'slice': (6,), 'default': 0, 'access': 'R/W H0',
								'description': 'Set this bit to 1 to de-assert the OUTPKT_RDY bit of this register. This bit is cleared automatically.'
								},
							'SEND_STALL': {
								'slice': (5,), 'default': 0, 'access': 'R/W H0',
								'description': 'Set this bit to 1 to terminate the current transaction. The USB controller sends the STALL handshake and this bit is de-asserted.'
								},
							'SETUP_END': {
								'slice': (4,), 'default': 0, 'access': 'R',
								'description': 'This bit is set if the control transfer ends due to a premature end-of-control transfer. The FIFO is flushed and an interrupt request (EP0) is generated if the interrupt is enabled.  Setting CLR_SETUP_END = 1 de-assert this bit',
								},
							'DATA_END': {
								'slice': (3,), 'default': 0, 'access': 'R/W H0',
								'description': '''This bit is used to signal the end of a data transfer and must be asserted in the following three situations:
1: When the last data packet has been loaded and USBCS0.INPKT_RDY is set to 1
2: When the last data packet has been unloaded and USBCS0.CLR_OUTPKT_READY is set to 1
3: When USBCS0.INPKT_RDY has been asserted without having loaded the FIFO (for sending a zero-length data packet).
The USB controller clears this bit automatically.''',
								},
							'SENT_STALL': {
									'slice': (2,), 'default': 0, 'access': 'R/W H1',
									'description': 'This bit is set when a STALL handshake has been sent. An interrupt request (EP0) is generated if the interrupt is enabled. This bit must be cleared from firmware.',
								},
							'INPKT_RDY': {
									'slice': (1,), 'default': 0, 'access': 'R/W H0',
									'description': 'Set this bit when a data packet has been loaded into the EP0 FIFO to notify the USB controller that a new data packet is ready to be transferred. When the data packet has been sent, this bit is cleared, and an interrupt request (EP0) is generated if the interrupt is enabled.',
								},
							'OUTPKT_RDY': {
									'slice': (0,), 'default': 0, 'access': 'R',
									'description': 'Data packet received. This bit is set when an incoming data packet has been placed in the OUT FIFO. An interrupt request (EP0) is generated if the interrupt is enabled. Set CLR_OUTPKT_RDY = 1 to de-assert this bit.',
								},
							},
					},
				'USBCSIL': {
						'address': 0x6211, 'module': 'USB', 
						'description': 'IN EP{1-5} Control and Status, Low',
						'bitfields': {
								'-reserved': {
									'slice': (7,), 'access': 'R0',
									'description': 'Reserved',
								},
								'CLR_DATA_TOG': {
									'slice': (6,), 'default': 0, 'access': 'R/W H0',
									'description': 'Setting this bit resets the data toggle to 0. Thus, setting this bit forces the next data packet to be a DATA0 packet. This bit is automatically cleared.'
									},
								'SENT_STALL': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
									'description': 'This bit is set when a STALL handshake has been sent. The FIFO is flushed and the INPKT_RDY bit is this register is de-asserted. An interrupt request (IN EP{1-5}) is generated if the interrupt is enabled. This bit must be cleared from firmware.'
									},
								'SEND_STALL': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
									'description': 'Set this bit to 1 to make the USB controller reply with a STALL handshake when receiving IN tokens. Firmware must clear this bit to end the STALL condition. It is not possible to stall an isochronous endpoint; thus, this bit only has an effect if the IN endpoint is configured as bulk/interrupt.'
									},
								'FLUSH_PACKET': {
									'slice': (3,), 'default': 0, 'access': 'R/W H0',
									'description': 'Set to 1 to flush next packet that is ready to transfer from the IN FIFO. The INPKT_RDY bit in this register is cleared. If there are two packets in the IN FIFO due to double buffering, this bit must be set twice to copletely flush the IN FIFO. This bit is automatically cleared.',
									},
								'UNDERRUN': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
									'description': 'In isochronous mode, this bit is set if an IN token is received when INPKT_RDY = 0, and a zero-length data packet is transmitted in response to the IN token. In bulk/interrupt mode, this bit is set when a NAK is returned in resonse to an IN token. Firmware should clear this bit.',
									},
								'PKT_PRESENT': {
									'slice': (1,), 'default': 0, 'access': 'R',
									'description': 'This bit is 1 when there is at least one packet in the IN FIFO',
									},
								'INPKT_RDY': {
									'slice': (0,), 'default': 0, 'access': 'R/W H0',
									'description': 'Set this bit when a data packet has been loaded into the IN FIFO to notify the USB controller that a new data packet is ready to be transferred. When the data packet has been sent, this bit is cleared, and an interrupt request (IN EP{1-5}) is generated if the interrupt is enabled',
									},
							},
						},
				# to continue on page 194 of sru191d.pdf
			}

	def sanityCheck(self):
		# do a sanity check
		# extract all field names and sort and list them.
		SFRNames = self._SFR.keys()
		XREGNames = self._XREG.keys()
		#print sorted(SFRNames)

		SFRFieldSet = map(set, map(lambda x: self._SFR[x].keys(), SFRNames))
		XREGFieldSet = map(set, map(lambda x: self._XREG[x].keys(), XREGNames))
		# print sorted(SFRFieldSet)
		## now do a merge
		U = reduce(lambda x, y: x | y, SFRFieldSet+XREGFieldSet)
		print 'First level field names:', U
		## Go to the bitfield level

if __name__ == '__main__':
	c = SFR_DEF_CC2540()
	c.sanityCheck()
