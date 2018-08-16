'''
	This is an attempt to model the nRF24E1 in terms of access to SFR.
	This is the MCU for the old Eco node.
	This is based on the cc2540sfr.py. It is much simpler than CC2540.

	The data is taken from the data sheet "nrf24e1.pdf", page 11,
	Table 2-1 "SFR Register map"; and also better summary is on
	Table 10-9 "Special Function Registers summary", pages 79-80.

	1/8/2014 - it is not working yet

'''
import cc_8051
from cc_8051 import CC_8051 as CodeCapsule
class nRF24E1SFR:
	'''
		This class nRF24E1SFR is just a container for a static hash
		tables of hash tables of stuff to provide the SFR definitions.
	'''


	_SFR = {
			############### GPIO ##################
			'P0': {
					'address': 0x80, 'module': 'CPU',
					'default': 0xFF, 'access': 'R/W',
					'bitfields': { },
					'description': 'Port 0. General-purpsoe I/O port.  Bit-addressable from SFR.',
				},
			'P1': {
					'address': 0x90, 'module': 'CPU', 'description': 'Port 1',
					'default': 0xFF, 'access': 'R/W',
					'bitfields': { },
					'description': 'Port 1. General-purpsoe I/O port.  Bit-addressable from SFR.',
				},
			'P2': {
					'address': 0xa0, 'module': 'CPU', 'description': 'Port 2',
					'default': 0xFF, 'access': 'R/W',
					'bitfields': { },
					'description': 'Port 2. General-purpsoe I/O port.  Bit-addressable from SFR.  Overlaps with RADIO',
				},

			########## SFRs at addresses 80-87 ##########

			'SP': {
					'address': 0x81, 'module': 'CPU', 'description': 'Stack pointer',
					'default': 0x07, 'access': 'RW',
				},
			'DPL': {
					'address': 0x82, 'module': 'CPU',
					'description': 'Data pointer low byte',
				},
			'DPH': {
					'address': 0x83, 'module': 'CPU',
					'description': 'Data pointer high byte',
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
			'DPS': {
					'address': 0x86, 'module': 'CPU',
					'description': 'Data pointer select',
					'default': 0x00,
					'bitfields': {
							'-reserved': {'slice': (7,1), 'access': 'R',
								'description': 'Reserved'
							},
							'SEL': {'slice': (0,), 'acccess': 'RW',
								'description': 'Data pointer select. Selects active data pointer. 0: DPTR0. 1: DPTR1.'
							},
						},
				},
			'PCON': {
					'address': 0x87, 'module': 'CPU',
					'description': 'Power mode control',
					'default': 0x00,
					'bitfields': {
						'SMOD': {
							'slice': (7,), 'description': '''Serial Port baud-rate doubler enable.  When SMOD = 1, the baud rate for Serial Port is doubled.''',
							},
						'-reserved': {
							'slice': (6,4), 'description': 'Reserved',
						},
						'GF1': {
							'slice': (3,), 'description': 'General purpose flag 1. Bit-addressable, general purpose flag for software control',
						},
						'GF0': {
							'slice': (2,), 'description': 'General purpose flag 0. Bit-addressable, general purpose flag for software control',
						},
						'STOP': {
							'slice': (1,), 'description': '''(Section 9.2) Stop mode select. Setting the STOP bit places the nRF24E1 in stop mode. Stop mode is identical to idle mode, except that the only way to exit stop mode is by watchdog reset. Since there is little power saving, stop mode is not recommended, as it is more efficient to use power down mode.''',
						},
						'IDLE': {
							'slice': (0,),
							'description': '''(Section 9.1) Idle mode select. Setting the IDLE bit places the nRF24E1 in idle mode.  In idle mode, CPU processing is suspended and internal registers and memory maintain their current data.  However, unlike the standard 8051, the CPU clock is not disabled internally, thus not much power is saved.

There are two ways to exit idle mode: activate any enabled interrupt or watchdog reset. Activation of any enabled interrupt causes the hardware to clear the IDLE bit and terminate idle mode. The CPU executes the ISR associated with the received interrupt. The RETI instruction at the end of the ISR returns the CPU to the instruction following the one that put the nRF24E1 into idle mode. A watch reset causes the nRF24E1 to exit idle mode, reset internal registers, execute its reset sequence and begin program execution at the standard reset vector address 0x0000.
''',
						},
					},
				},

			### SFR 0x88 - 0x8F
			'TCON': {
					'address': 0x88, 'module': 'CPU',
					'description': 'Interrupt flags',
					'bitfields': {
							'TF1': {
								'slice': (7,), 
								'description': 'Timer 1 overflow flag. Set to 1 when the Timer 1 counter overflows and cleared when the CPU vectors to the interrupt service routine',
							},
							'TR1': {
								'slice': (6,),
								'description': 'Timer 1 run control. Set to 1 to enable counting on Timer 1.'
							},
							'TF0': {
								'slice': (5,),
								'description': 'Timer 0 overflow flag. Set to 1 when the Timer 0 count overflows and cleared when the CPU vectors to the interrupt service routine.',
							},
							'TR0': {
								'slice': (4,),
								'description': 'Timer 0 run control. Set to 1 to enable counting on Timer 0.'
							},
							'IE1': {
								'slice': (3,), 
								'description': 'Interrupt 1 edge detect. If external intererupt 1 is configured to be edge-sensitive (IT1 = 1), IE1 is set by hardware when a negative edge is detected on the INT1_N external interrupt pin and is automatically cleared when the CPU vectors to the corresponding interrupt service routine. In edge-sensitive mode, IE1 can also be cleared by software. If external interrupt 1 is configured to be level sensitive (IT1=0), IE1 is set when the INT1_N pin is low and cleared when the INT1_N pin is high. In level-sensitive mode, software cannot write to IE1.',
							},
							'IT1': {
								'slice': (2,), 
								'description': 'Interrupt 1 type select. When IT1 = 1, the nRF24E1 detects external interrupt pin INT1_N on the falling edge (edge-sensitive). When IT1 = 0, the nRF24E1 detects IT1_N as a low level (level-sensitive)',
							},
							'IE0': {
								'slice': (1,), 
								'description': 'Interrupt 0 edge detect. If external intererupt 0 is configured to be edge-sensitive (IT0 = 1), IE1 is set by hardware when a negative edge is detected on the INT0_N external interrupt pin and is automatically cleared when the CPU vectors to the corresponding interrupt service routine. In edge-sensitive mode, IE0 can also be cleared by software. If external interrupt 0 is configured to be level sensitive (IT0=0), IE0 is set when the INT0_N pin is low and cleared when the INT0_N pin is high. In level-sensitive mode, software cannot write to IE0.',
							},
							'IT1': {
								'slice': (0,), 
								'description': 'Interrupt 0 type select. When IT0 = 1, the nRF24E1 detects external interrupt pin INT0_N on the falling edge (edge-sensitive). When IT0 = 0, the nRF24E1 detects IT0_N as a low level (level-sensitive)',
							},
					},
				},
			'TMOD': {
					'address': 0x89, 'module': 'timer',
					'description': '''Timer mode register (Table 10-13)''',
					'bitfields': {
						'GATE_1': {
								'slice': (7,),
								'description': '''Timer 1 gate control. When GATE=1, Timer 1 will clock only when external interrupt INT1_N = 1 and TR1 (TCON.6) = 1.  When GATE = 0, Timer 1 will clock only when TR1 = 1, regardless of the state of INT1_N.''',
							},
						'CT_1': {
								'slice': (6,),
								'description': '''(C/T) Counter/Timer select. When C/T = 0, Timer 1 is clocked by CPU_clk/4 or CPU_clk/12, depending on the state of T1M (CKCON.4). When C/T = 1, Timer 1 is clocked by the t1 pin.'''
							},
						'M_1_1': {
								'slice': (5,),
								'description': '''Timer 1 mode select bit 1''',
							},
						'M_1_0': {
								'slice': (4,),
								'description': '''Timer 1 mode select bit 0''',
							},
						'M_1': {
								'slice': (5,4),
								'description': '''M1 M0 fields concatenated for timer 1.
00: (Mode 0) 13-bit counter
01: (Mode 1) 16-bit counter
10: (Mode 2) 8-bit counter with auto-reload
11: (Mode 3) two 8-bit counters''',
							},
						'GATE_0': {
								'slice': (3,),
								'description': '''Timer 0 gate control. When GATE=1, Timer 0 will clock only when external interrupt INT0_N = 1 and TR0 (TCON.4) = 1.  When GATE = 0, Timer 0 will clock only when TR0 = 1, regardless of the state of INT0_N.''',
							},
						'CT_0': {
								'slice': (2,),
								'description': '''(C/T) Counter/Timer select. When C/T = 0, Timer 0 is clocked by CPU_clk/4 or CPU_clk/12, depending on the state of T0M (CKCON.4). When C/T = 1, Timer 0 is clocked by the t0 pin.'''
							},
						'M_0_1': {
								'slice': (1,),
								'description': '''Timer 0 mode select bit 1''',
							},
						'M_0_0': {
								'slice': (0,),
								'description': '''Timer 0 mode select bit 0''',
							},
						'M_0': {
								'slice': (1,0),
								'description': '''M1 M0 fields concatenated for timer 0.
00: (Mode 0) 13-bit counter
01: (Mode 1) 16-bit counter
10: (Mode 2) 8-bit counter with auto-reload
11: (Mode 3) two 8-bit counters''',
							},
						},
				},

			'TL0': {
					'address': 0x8A,
					'module': 'timer',
					'description': '''Timer/counter 0 value, low byte''',
				},
			'TL1': {
					'address': 0x8B,
					'module': 'timer',
					'description': '''Timer/counter 1 value, low byte''',
				},
			'TH0': {
					'address': 0x8C,
					'module': 'timer',
					'description': '''Timer/counter 0 value, high byte''',
				},
			'TH1': {
					'address': 0x8D,
					'module': 'timer',
					'description': '''Timer/counter 1 value, high byte''',
				},
			'CKCON': {
					'address': 0x8E, 'default': 0x01,
					'module': 'timer',
					'bitfields': {
						'-reserved': {
								'slice': (7,6),
							},
						'T2M': {
								'slice': (5,),
								'description': '''Timer 2 clock select. When T2M = 0, Timer 2 uses CPU_clk/12 (for compatibility with 80C32); when T2M = 1, Timer 2 uses CPU_clk/4. This bit has no effect when Timer 2 is configured for baud rate generation.''',
							},
						'T1M': {
								'slice': (4,),
								'description': '''Timer 1 clock select. When T1M = 0, Timer 1 uses CPU_clk/12 (for compatibility with 80C32); when T1M = 1, Timer 1 uses CPU_clk/4.''',
							},
						'T0M': {
								'slice': (3,),
								'description': '''Timer 0 clock select. When T0M = 0, Timer 0 uses CPU_clk/12 (for compatibility with 80C32); when T1M = 1, Timer 1 uses CPU_clk/4.''',
							},
						'CKCON.MD': {
								'slice': (2,0),
								'description': '''Control the number of cycles to be used for external MOVX instructions; number of cycles is 2 + { MD2, MD1, MD0 }''',
							},
						},
				},
			'SPC_FNC': {
					'address': 0x8F,
					'module': 'CPU',
					'description': "Do not use!",
				},

			##### SFRs 0x91 - 0x99
			'EXIF': {
					'address': 0x91,
					'module': 'CPU',
					'bitfields': {
							'IE5': {
									'slice': (7,), 
									'description': '''Interrupt 5 flag. IE5 = 1 indicates that a rising edge was detected on the RADIO.DR2 signal. (see ch. 5.1 RADIO) IE5 must be cleared by software. Setting IE5 in software generates an interrupt, if enabled.''',
								},
							'IE4': {
									'slice': (6,),
									'description': '''Interrupt 4 flag. IE4 = 1 indicates that a rising edge was detectedo n the RADIO.DR1 signal. (see ch. 5.1 RADIO) IE4 must be cleared by software. Setting IE4 in software generates an interrupt, if enabled.''',
								},
							'IE3': {
									'slice': (5,),
									'description': '''Interrupt 3 flag. IE3 = 1 indicates that the internal SPI module has sent or received 8 bits, and is ready for a new command. IE3 must be cleared by software. Setting IE3 in software generates an interrupt, if enabled.''',
								},
							'IE2': {
									'slice': (4,),
									'description': '''Interrupt 2 flag. IE2 = 1 indicates that a rising edge was detected on the ADC_EOC signal. (see ch.5.3.1 End of conversion.)  IE2 must be cleared by software. Setting IE2 in software generates an interrupt, if enabled.''',
								},
							'-reserved': {
									'slice': (3,), 'default': 1, 'access': 'R',
									'description': 'Reserved. read as 1.',
								},
							'--reserved': {
									'slice': (2,0), 'default': 0, 'access': 'R',
									'description': 'Reserved. read as 0.',
								},
						},
				},

			'MPAGE': {
					'address': 0x92,
					'module': 'CPU',
					'description': 'program/data memory page address. It provides memory paging function. During MOVX A, @R1 and MOVX @Ri, A instructions, the contents of the MPAGE register are placed on the upper eight address bits of memory address.',
				},

			'P0_DIR': {
					'address': 0x94,
					'module': 'CPU',
					'default': 0xff, 'access': 'R/W',
					'description': '''Direction for each bit of Port 0.
0: Output
1: Input
Direction is overridden if alternate function is selected for a pin.''',
				},

			'P0_ALT': {
					'address': 0x95,
					'module': 'CPU',
					'default': 0x00, 'access': 'R/W',
					'description': '''Select alternate functions for each pin of P0, if corresponding bit in P0_ALT is set, as listed in Table 3-2: Port 0 (P0) functions, P0.0 has no alternate function, as it is intended as CS for external boot flash memory. It will function as a GPIO bit regardless of P0_ALT.0.''',
				},

			'P1_DIR': {
					'address': 0x96,
					'module': 'CPU',
					'default': 0xff, 'access': 'R/W',
					'description': '''Direction for each bit of Port 1
0: Output
1: Input
Direction is overridden if alternate function is selected for a pin, or if SPI_CTRL=01. bit0, DIN0 is always input.''',
					'size': 3, # 3 bits only!!!
				},

			'P1_ALT': {
					'address': 0x97,
					'module': 'CPU',
					'default': 0x00, 'access': 'R/W',
					'description': '''Select alternate functions for each pin of P1 if corresponding bit in P1_ALT is sete, as listed in Table 3-4: Port 1 (P1) functions
If SPI_CTRL is '01', the P1 port is used as SPI master data and clock:
2 -> SDI - input to nRF24E1 from slave
1 -> SDO - output from nRF24E1 to slave
0 -> SCK - output from nRF24E1 to slave''',
				},

			'SCON': {
					'address': 0x98,
					'module': 'UART',
					'bitfields': {
							'SM0': {
									'slice': (7,),
									'description': '''Serial port mode bit 0''',
								},
							'SM1': {
									'slice': (6,),
									'description': '''Serial port mode bit 1''',
								},
							'SM': {
									'slice': (7,6),
									'description': '''Serial port mode:
SM1 SM0 Mode
 0   0: mode 0
 0   1: mode 2
 1   0: mode 1
 1   1: mode 3''',
 								},
							'SM2': {
									'slice': (5,),
									'description': '''Multiprocessor communication enable. In modes 2 and 3, SM2 enables the multiprocessor communication feature. If SM2 = 1 in mode 2 or 3, RI will not be activated if the received 9th bit is 0. If SM2 = 1 in mode 1, RI will be activated only if a valid stop is received. In mode 0, SM2 establishes the baud rate: when SM2 = 0, the baud rate is CPU_clk/12; when SM2 =  1, the baud rate is CPU_clk/4.''',
									},
							'REN': {
									'slice': (4,),
									'description': '''Receive enable. When REN = 1, reception is enabled.''',
								},
							'TB8': {
									'slice': (3,),
									'description': '''Defines the state of the 9th data bit transmitted in modes 2 and 3.''',
								},
							'RB8': {
									'slice': (2,),
									'description': '''In modes 2 and 3, RB8 indicates the state of the 9th bit received. In mode 1, RB8 indicates the state of the received stop bit. In mode 0, RB8 is not used.''',
								},
							'TI': {
									'slice': (1,),
									'description': '''Transmit interrupt flag.  Indicates that the transmit data word has been shifted out. In mode 0, TI is set at the end of the 8th data bit. In all other modes, TI is set when the stop bit is placed on the TxD pin. TI must be cleared by the software.''',
								},
							'RI': {
									'slice': (0,),
									'description': '''Receive interrupt flag. Indicates that a serial data word has been received. In mode 0, RI is set at the end of the 8th data bit. In mode 1, RI is set after the last sample of the incoming stop bit, subject to the state of SM2. In mode 2 and 3, RI is set at the end of the last sample of RB8. RI must be cleared by the software.''',
								},
						},
				},

			'SBUF': {
					'address': 0x99,
					'module': 'UART',
					'description': '''Serial port data buffer''',
				},


			##### SFR 0xA0 to 0xA4
			'RADIO': {
					'address': 0xA0,
					'default': 0x80,
					'module': 'RF',
					'bitfields': {
							'PWR_UP': {
									'slice': (7,),
									'description': 'power on radio',
								},
							'CE': {
									'slice': (6,),
									'description': '''CE, Activate Rx or Tx mode''',
								},
							'CLK2': {
									'slice': (5,),
									'description': '''clock for receiver 2 data out''',
								},
							'-unused': {
									'slice': (4,),
								},
							'CS': {
									'slice': (3,),
									'description': '''Chip select configuration mode''',
								},
							'--unused': {
									'slice': (2,),
								},
							'CLK1': {
									'slice': (1,),
									'description': '''clock for data input or receive 1 data out''',
								},
							'DATA': {
									'slice': (0,),
									'description': '''configuration or Tx data input''',
								},
						},
				},

			'ADCCON': {
					'address': 0xA1, 'module': 'ADC',
					'default': 0x80,
					'bitfields': {
							'CSTARTN': {
									'slice': (7,),
									'description': '''Toggle H -> L -> H to start A/D conversion. This bit is internally synchronized to the ADC clock. Ignore if ADCRUN is set.''',
								},
							'ADCRUN': {
									'slice': (6,),
									'description': '''Set to have the A/D converter run continuously.  CSTARTN is ignored in this case.''',
								},
							'NPD': {
									'slice': (5,),
									'description': '''Set to 0 to put A/D conveter in power down state.''',
								},
							'EXTREF': {
									'slice': (4,),
									'description': '''Select reference for A/D converter
0: Use internal band gap reference (nominally 1.22V)
1: Use external pin AREF for reference.
Ignore if ADCSEL = 8. ''',
								},
							'ADCSEL': { 
									'slice': (3, 0),
									'description': '''Select input AIN0 to AIN7.  ADCSEL=8 will select internal VDD/3, and also automatically select internal bandgap reference. For n = 0..7, ADCSEL=n will select input pin AINn.''',
								},
						},
				},

			'ADC_DATAH': {
					'address': 0xA2, 'module': 'ADC',
					'description': '''Most significant 8 bits of A/D converter result. For 6-bit conversion, ADCDATAH.7-6 is '00'.'''
				},

			'ADC_DATAL': {
					'address': 0xA3, 'module': 'ADC',
					'bitfields': {
							'ADCDATAL': {
									'slice': (7,4),
									'description': '''Least significant part of A/D converter result
									when resolution is 12 or 10 bits, left justified. For 10-bit
									conversions ADCDATAH.5-4 is '00'.''',
								},
							'-unused': {
									'slice': (3,),
									'description': 'not used',
								},
							'ADCUF': {
									'slice': (2,),
									'description': '''Underflow in conversion. Data is all 0's.''',
								},
							'ADCOF': {
									'slice': (1,),
									'description': '''Overflow in conversion. Data is all 1's.''',
								},
							'ADCRNG': {
								'slice': (0,),
								'description': '''Overflow or underflow in conversion (ADCUF | ADCOF)''',
								},
						},
				},

			'ADC_STATIC': {
					'address': 0xA4, 'module': 'ADC',
					'default': 0x0A,
					'bitfields': {
							'DIFFM': {
									'slice': (7,),
									'description': '''Enable differential measurements, AIN0 must be used as inverting input and one of the other inputs AIN1 to AIN7, as selected by ADCSEL must be used as noninverting input.''',
								},
							'SLEEP': {
									'slice': (6,),
									'description': '''Set A/D converter in a reduced power mode.''',
								},
							'CLK8': {
									'slice': (5,),
									'description': '''0: ADCCLK frequency = CPU clock diviced by 32.
1: ADCCLK frequency = CPU clock divided by 8.''',
								},
							'ADCBIAS': {
									'slice': (4,2),
									'description': '''Control A/D converter bias current. No need to change for nRF24E1 operation.''',
								},
							'ADCRES': {
									'slice': (1,0),
									'description': '''Select A/D converter resolution.
00: 6-bit, result in ADCDATAH 5-0
01: 8-bit, result in ADCDATAH
10: 10-bit, result in ADCDATAH, ADCDATAL.7-6
11: 12-bit, result in ADCDATAH, ADCDATAL.7-4''',
								},
						},
				},


			#### SFRs at 0xA9-0xAD #####

			'PWMCON': {
					'address': 0xA9,
					'module': 'PWM',
					'default': 0x0,
					'bitfields': {
							'PWM_LENGTH': {
									'slice': (7,6),
									'description': '''mode
00: PWM inactive
01: frequency = fxo / (63 * (PWMCON[5:0]+1)), duty = PWMDUTY[5:0]/63
10: frequency = fxo / (127* (PWMCON[5:0]+1)), duty = PWMDUTY[6:0]/127
11: frequency = fxo / (255* (PWMCON[5:0]+1)), duty = PWMDUTY / 255''',
								},
							'PWM_PRESCALE': {
									'slice': (5,0),
									'description': 'PWM scaler',
								},
						},
				},


			'PWMDUTY': {
					'address': 0xAA,
					'default': 0x0,
					'module': 'PWM',
					'description': '''PWM duty cycle''',
				},

			'REGX_MSB': {
					'address': 0xAB,
					'default': 0x0,
					'module': 'watchdog',
					'description': 'high byte of watchdog/RTC register',
				},

			'REGX_LSB': {
					'address': 0xAC,
					'default': 0x0,
					'module': 'watchdog',
					'description': 'low byte of watchdog/RTC register',
				},

			'REGX_CTRL': {
					'address': 0xAD,
					'module': 'watchdog',
					'default': 0x0,
					'description': '''control of interface to watchdog and RTC''',
					'bitfields': {
							'busy': {
									'slice': (4,)
								},
							'REGX_CTRL': {
									'slice': (3,0),
									'description': '''Control for 16 bit register for
									interface to Watchdog and RTC. Bit 4 is only available on
									read and is used to flag the interface unit as busy.  Bits
									3:0 is read/write with the encoding:
0 000: Read from WD register (16 bit)
1 000: Write to WD register (16 bit)
0 010: Read from RTC latch register (16 bit)
1 010: Write to RTC latch register (16 bit)
0 011: Read from RTC counter reg. (16 bit)
1 011: Disable RTC counter (no data)''',
								},
						},
				},

			#### SFRs at addresses 0xB1 - 0xB7 #####

			'RSTREAS': {
					'address': 0xB1,
					'module': 'CPU',
					'default': 0x2,
					'description': 'Reset control register',
					'bitfields': {
							'UseIROMforRV': {
									'slice': (1,),
									'description': '''Use IROM for reset vector.
0: Reset vectors to 0x0000.
1: Reset vectors to 0x8000.''',
								},
							'ResetReason': {
									'slice': (0,),
									'description': '''Reason for last reset.
0: POR
1: Any other reset source
Clear this bit in software to force a reboot after jump to zero (boot loader
will load code RAM if this bit is 0''',
								},
						},
				},

			'SPI_DATA': {
					'address': 0xB2,
					'default': 0x0,
					'module': 'SPI',
					'description': 'SPI data input/output',
				},

			'SPI_CTRL': {
					'address': 0xB3,
					'module': 'SPI',
					'default': 0x0,
					'description': '''SPI control''',
					'bitfields': {
						'SPI_CTRL': {
								'slice': (1,0), 'default': 0,
								'description': '''00 -> SPI not used, no clock generated
01 -> SPI connected to port P1 (as for booting). Another GPIO must be used as chip select (see also Table 3-4: Port 1 (P1) functions)
10 -> SPI connected to RADIO transmitter/receiver 1 for Tx or RX or for transceiver configuration
11 -> SPI connected to RADIO receiver 2 for RX chip select is a bit of RADIO register (see Table 4-2: RADIO register)''',
							},
						},
				},

			'SPI_CLK': {
					'address': 0xB4,
					'module': 'SPI', 'default': 0,
					'description': 'SPI clock configuration',
					'bitfields': {
							'SPICLK': {
									'slice': (1,0),
									'description': '''Divider factor from CPU clock to SPI clock
00: 1/8 of CPU clock frequency
01: 1/16 of CPU clock frequency
10: 1/32 of CPU clock frequency
11: 1/64 of CPU clock frequency
The CPU clock is the oscillator generated clock described in Crystal Specification page 108.'''
								},
						},
				},

			'TICK_DV': {
					'address': 0xB5,
					'module': 'watchdog',
					'default': 0x1D,
					'description': '''TICK control register. Divider that is used in generating TICK from LP_OSC frequency.
ftick = fLP_OSC / (1 + TICK_DV)
The default value gives a TICK of 10 ms nominal as default.''',
				},

			'CK_CTRL': {
					'address': 0xB6,
					'module': 'CPU',
					'default': 0x0,
					'description': 'clock control',
					'bitfields': {
							'STOP_CLOCK': {
									'slice': (1,),
									'description': '''Setting the STOP_CLOCK bit places the nRF24E1 in power down mode.''',
								},
							'-unused': {
									'slice': (0,),
								},
						},
				},

			'TEST_MODE': {
					'address': 0xB7,
					'module': 'CPU',
					'default': 0x0,
					'description': '''Test mode register. This register must always be 0 in normal mode.''',
				},

			##### SFRs at addresses 0xB8 - 0xBE ######
			'IP': {
					'address': 0xB8,
					'module': 'CPU',
					'description': '''Interrupt priority''',
					'bitfields': {
							'-reserved': {
									'slice': (7,),
									'description': 'Reserved. Read as 1.'
								},
							'-reserved': {
									'slice': (6,),
									'description': 'Reserved. Read as 0.',
								},
							'PT2': {
									'slice': (5,),
									'description': '''Timer 2 interrupt priority control. PT2 = 0 sets Timer 2 interrupt (TF2) to low priority. PT2 = 1 sets Timer 2 interrupt to high priority.''',
								},
							'PS': {
									'slice': (4,),
									'description': '''Serial Port interrupt priority control.  PS = 0 sets Serial Port interrupt (TI or RI) to low priority. PS = 1 sets Serial Port interrupt to high priority.''',
								},
							'PT1': {
									'slice': (3,),
									'description': '''Timer 1 interrupt priority control. PT1 = 0 sets Timer 1 interrupt (TF1) to low priority. PT1 = 1 sets Timer 1 interrupt to high priority.''',
								},
							'PX1': {
									'slice': (2,),
									'description': '''External interrupt 1 priority control.  PX1 = 0 sets external interrupt 1 (INT1_N) to low priority. PT1 = 1 sets external interrupt 1 to high priority.''',
								},
							'PT0': {
									'slice': (1,),
									'description': '''Timer 0 interrupt priority control. PT0 = 0 sets Timer 0 interrupt (TF0) to low priority. PT0 = 1 sets Timer 0 interrupt to high priority.''',
								},
							'PX0': {
									'slice': (0,),
									'description': '''External interrupt 0 priority control.  PX0 = 0 sets external interrupt 0 (INT0_N) to low priority. PT0 = 1 sets external interrupt 0 to high priority.''',
								},
						},
				},

			'T1_1V2': {
					'address': 0xBC,
					'module': 'CPU',
					'description': '''one of the 3 other test mode registers. Initial values must not be changed.''',
				},
			'T2_1V2': {
					'address': 0xBD,
					'module': 'CPU',
					'description': '''one of the 3 other test mode registers. Initial values must not be changed.''',
				},
			'DEV_OFFSET': {
					'address': 0xBE,
					'module': 'CPU',
					'description': '''one of the 3 other test mode registers. Initial values must not be changed.''',
				},

			###### SFRs at addresses 0xC8 - 0xCD ######

			'T2CON': {
					'address': 0xC8,
					'module': 'timer',
					'description': '''(Table 10-16) Timer-2 control. Timer 2 runs only in 16-bit mode and offers several capabilities not available with Timer 0 and 1. The modes available with Timer 2 are:
- 16-bit timer/counter
- 16-bit timer with capture
- 16-bit auto-reload timer/counter
- baud-rate generator.
It is used in conjunction with the following SFRs: RCAP2L, RCAP2H, TL2, TH2''',
					'bitfields':  {
							'TF2': {
									'slice': (7,),
									'description': '''Timer 2 overflow flag. Hardware will set TF2 when Timer 2 overflows from 0xFFFF. TF2 must be cleared to 0 by the software. TF2 will only be set to a 1 if RCLK and TCLK are both cleared to 0. Writing a 1 to TF2 forces a Timer 2 interrupt if enabled.''',
								},
							'EXF2': {
									'slice': (6,),
									'description':  '''Timer 2 external flag. Hardware will set EXF2 when a reload or capture is caused by a high-to-low transition on the t2ex pin, and EXEN2 is set. EXF2 must be cleared to 0 by the software. Writing a 1 to EXF2 forces a Timer 2 interrupt if enabled.''',
								},
							'RCLK': {
									'slice': (5,),
									'description': '''Receive clock flag. Determines whether Timer 1 or Timer 2 is used for Serial port timing of received data in serial mode 1 or 3. RCLK = 1 selects Timer 2 overflow as the receive clock.  RCLK =  0 selects Timer 1 overflow as the receive clock.''',
								},
							'TCLK': {
									'slice': (4,),
									'description': '''Transmit clock flag. Determines whether Timer 1 or Timer 2 is used for Serial port timing of transmit data in serial mode 1 or 3. TCLK = 1 selects Timer 2 overflow as the transmit clock. TCLK = 0 selects Timer 1 overflow as the transmit clock.''',
								},
							'EXEN2': {
									'slice': (3,),
									'description': '''Timer 2 external enable. EXEN2 = 1 enables capture or reload to occur as a result of a high-to-low transition on t2ex, if Timer 2 is not generating baud rates for the serial port. EXEN2 = 0 causes Timer 2 to ignore all external events at t2ex.''',
								},
							'TR2': {
									'slice': (2,),
									'description': '''Timer 2 run control flag. TR2 = 1 starts Timer 2.  TR2 = 0  stops Timer 2.''',
								},
							'C_T2': {
									'slice': (1,),
									'description': '''(C/T) Counter/timer select.  C/T2 = 0 selects a timer function for Timer 2. C/T2 = 1 selects a counter of falling transitions on the t2 pin. When used as a timer, Timer 2 runs at four clocks per increment or twelve clocks per increment as programmed by CKCON.5, in all modes except baud-rate generator mode.  When used in baud-rate generator mode, Timer 2 runs at two clocks per increment, independent of the state of CKCON.5.''',
								},
							'CP_RL2': {
									'slice': (0,),
									'description': '''(CP/RL2) Capture/reload flag. When CP/RL2 = 1,Timer 2 captures occur on high-to-low transitions of t2ex, if EXEN2 = 1.  When CP/RL2 = 0, auto-reloads occur when Timer 2 overflows or when high-to-low transitions occur on t2ex, if EXEN2 = 1. If either RCLK or TCLK is set to 1, CP/RL2 will not function, and Timer 2 will operate in auto-reload mode following each overflow.''',
								},
						},
				},

			'RCAP2L': {
					'address': 0xCA,
					'module': 'timer',
					'description': 'Timer/counter 2 capture or reload, low byte',
				},
			'RCAP2H': {
					'address': 0xCB,
					'module': 'timer',
					'description': 'Timer/counter 2 capture or reload, high byte',
				},
			'TL2': {
					'address': 0xCC,
					'module': 'timer',
					'description': 'Timer 2 low byte',
				},
			'TH2': {
					'address': 0xCD,
					'module': 'timer',
					'description': 'Timer 2 high byte',
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

			'EICON': {
					'address': 0xD8,
					'module': 'CPU',
					'bitfields': {
							'-unused': {
									'slice': (7,),
									'description': 'Not used.',
								},
							'-reserved': {
									'slice': (6,4),
									'description': 'Reserved.',
									'default': 0x4,
									'access': 'R',
								},
							'WDTI': {
									'slice': (3,),
									'description': '''RTC wakeup timer interrupt flag. WDTI = 1 indicates a wakeup timer interrupt was detected. WDTI must be cleared by software before exiting the interrupt service routine.  Otherwise, the interrupt occurs again. Setting the WDTI in software generates a wakeup timer interrupt, if enabled.''',
								},
							'--reserved': {
								'slice': (2,0),
								'description': '''Reserved. Read as 0.''',
								'default': 0,
								'access': 'R',
							},
						},
				},


			'ACC': {
					'address': 0xE0, 'module': 'CPU',
					'description': 'Accumulator',
					'bitfields': { },  ## bit addressable by bit index
				},

			'EIE': {
					'address': 0xE8,
					'module': 'CPU',
					'bitfields': {
							'-reserved': {
									'slice': (7,5),
									'description': 'Reserved. Read as 1.',
								},
							'EWDI': {
									'slice': (4,),
									'description': '''Enable RTC wakeup timer interrupt.  EWDI = 0 disables wakeup timer interrupt (wdti). EWDI =  1 enables interrupts generated by wakeup.''',
								},
							'EX5': {
									'slice': (3,),
									'description': '''Enable interrupt 5. EX5 = 0 disables interrupt 5 (RADIO.DR2). EX5 = 1 enables interrupts generated by the RADIO.DR2 signal.''',
								},
							'EX4': {
									'slice': (2,),
									'description': '''Enable interrupt 4. EX4 = 0 disables interrupt 4 (RADIO.DR1). EX4 = 1 enables interrupts generated by the RADIO.DR1 signal.''',
								},
							'EX3': {
									'slice': (1,),
									'description': '''Enable interrupt 3. EX3 = 0 disables interrupt 3 (SPI_READY). EX3 = 1 enables interrupts generated by the SPI_READY signal.''',
								},
							'EX2': {
									'slice': (0,),
									'description': '''Enable interrupt 2. EX2 = 0 disables interrupt 2 (ADC_EOC). EX2 = 1 enables interrupts generated by the ADC_EOC signal.''',
								},
						},
				},

			'B': {
					'address': 0xF0, 'module': 'CPU',
					'description': 'B register',
					'bitfields': { }, ## bit addressable by bit index
				},

			'EIP': {
					'address': 0xF8,
					'module': 'CPU',
					'bitfields': {
							'-reserved': {
									'slice': (7,5),
									'access': 'R', 'default': 0x3,
								},
							'PWDI': {
									'slice': (4,),
									'description': '''(WDPI?) RTC wakeup timer interrupt priority control. WDPI = 0 sets wakeup timer interrupt (wdti) to low priority. PS = 1 sets wakeup timer interrupt to high priority.''',
								},
							'PX5': {
									'slice': (3,),
									'description': '''interrupt 5 priority control. PX5 = 0 sets interrupt 5 (RADIO.DR2) to low priority. PX5 = 1 sets interrupt 5 to high priority.''',
								},
							'PX4': {
									'slice': (2,),
									'description': '''interrupt 4 priority control. PX4 = 0 sets interrupt 4 (RADIO.DR1) to low priority. PX4 = 1 sets interrupt 4 to high priority.''',
								},
							'PX3': {
									'slice': (1,),
									'description': '''interrupt 3 priority control. PX3 = 0 sets interrupt 3 (SPI_READY) to low priority. PX3 = 1 sets interrupt 3 to high priority.''',
								},
							'PX2': {
									'slice': (0,),
									'description': '''interrupt 2 priority control. PX2 = 0 sets interrupt 2 (ADC_EOC) to low priority. PX2 = 1 sets interrupt 2 to high priority.''',
								},
						},
				},
			}

	def sanityCheck(self):
		# do a sanity check
		# extract all field names and sort and list them.
		SFRNames = self._SFR.keys()
		#print sorted(SFRNames)

		SFRFieldSet = map(set, map(lambda x: self._SFR[x].keys(), SFRNames))
		# print sorted(SFRFieldSet)
		## now do a merge
		U = reduce(lambda x, y: x | y, SFRFieldSet)
		print 'First level field names:', U
		## Go to the bitfield level

class SFR:
	'''This is a ``factory'' that constructs the SFRs.
	  Each one is initialized to its default value.
		The behavior depends on its access previlege.
	'''
	def __init__(self, sfrName, mcu=None):
		'''sfrName must be one of those SFR names. It can be used for
		generating assembly code.
		'''
		import copy
		if nRF24E1SFR._SFR.has_key(sfrName):
			defn = copy.deepcopy(nRF24E1SFR._SFR[sfrName])
		else:
			raise NameError(sfrName)
		self.__dict__['_name']        = sfrName
		self.__dict__['_defn']        = defn
		self.__dict__['_address']     = defn['address']
		try:
			self.__dict__['_module']      = defn['module']
			self.__dict__['_description'] = defn['module']
		except Exception:
			print 'sfrName %s has no module' % sfrName
		self.__dict__['_value']       = 0
		# self.__dict__['_C'] = 0
		# self.__dict__['_A'] = 0
		self.__dict__['_code'] = None
		self.__dict__['_mcu'] = mcu
		# initialize the value to the power-up default, if any.
		self.powerUpInit()

	def getVarType(self):
		return 'uint8'

	def powerUpInit(self):
		''' sets it to the default value locally.
		   The MCU side is initialized by hardware reset!
		'''
		self._value = 0
		if self._defn.has_key('default'):
			self._value = self._defn['default']
			return
		if not self._defn.has_key('bitfields'):
			# no initialization then
			return
		# otherwise, dig into each bit in the field. everything else is
		# initialized to 0.
		for field in self._defn['bitfields'].values():
			s = field['slice']
			val = field.get('default',0)
			if (type(val) != type(0)):
				raise TypeError("type of val of %s is %s", self._name, type(val))
			if (len(s) == 1):
				self._value |= (val & 1) << s[0]
			elif (len(s) == 2):
				j = 1 << s[1]
				for i in range(s[1], s[0]+1):
					self._value |= (val & j) << i
					j <<= 1
			else:
				## malformed slice. fail silently?
				raise ValueError("bad slice for SFR %s: %s" % (self_.name, s))

	def setattr(self, name, value):
		return self.__setattr__(name, value)

	def __setattr__(self, name, value):
		'''This is the dot-notation, used for setting a bit field or a
		slice in an SFR.  Python will give a syntax error if we do
		port.1 or dot-digit. so we need to make it an identifier by
		port._1 instead.  The value to set is in A, regardless if it is
		single bit.
		@@@ Should check write permission!?
		'''
		if self.__dict__.has_key(name):
			self.__dict__[name] = value
			return
			# regular attribute access, no return value
		if isinstance(value, CodeCapsule):
			self._code = value
		else:
			self._code = CodeCapsule(self._mcu, dest=self,
					src=self)
		if len(name) == 2 and name[0] == '_' and name[1] in '01234567':
			# special handling: as bit index
			bitindex = int(name[1])
			# print "bit index %d" % bitindex
			return self._writeBit(self._address, bitindex, value)

		# now look up name
		if not self._defn.has_key('bitfields') or \
				not self._defn['bitfields'].has_key(name):
			# uh oh... no bit name has been defined for it
			raise NameError("bit name `%s' not found in SFR `%s'" % (name, self._name))
		# need to determine slice size.
		# this should work. if no 'slice' entry then original definition
		# is malformed!!
		s = self._defn['bitfields'][name]['slice']
		if (len(s) == 1):
			# this is a bit access.
			return self._writeBit(self._address, s[0], value)
		# otherwise, we have a slice. read as a byte first,
		# then mask it and extract.
		elif (len(s) != 2):
			# if neither 1 or 2, then definition is malformed!
			raise NameError('malformed slice %s' % s)
		# To write, we first clear the slice with AND, then OR in the # bits.
		# construct the slice mask from bit s[0] downto s[1]
		# find out many bits wide, shift (1 << bitsWide) - 1
		# example. 2 bit wide: (1 << 2 = 4)-1 = 3 = 0b11
		# then, shift the mask up to s[1] position.
		# complement it to AND, then shift the value up to region and OR.
		p = s[1]
		mask = ((1 << (s[0]-p+1)) - 1) << p
		maskN = 0xff ^ mask  # complement the whole byte, nothing more.
		if (isinstance(value, int)):
			self._SFRandByte(maskN)  # clear out the part we'll write in.
			valMask = (value << p) & mask
			self._SFRorByte(valMask)
		elif (isinstance(value, CodeCapsule)):
			# byte assumed already in A. need to shift left by s[1]
			# positions.
			if (p == 0):
				pass  # nothing to do. the result is ready.
			elif (p == 1):
				self._emit('RL A')  # rotate right once is like shifting right
			elif (p == 2):
				self._emit('RL A')
				self._emit('RL A')  # shifting right twice = two rotate rights
			elif (p == 3):
				self._emit('SWAP A')  # swap is left or right by 4 positions
				self._emit('RR A')    # shift one position back
			elif (p == 4):
				self._emit('SWAP A')  # swap is shift by 4 positions
			elif (p == 5):
				self._emit('SWAP A')
				self._emit('RL A')    # 4 positions + 1
			elif (p == 6):
				self._emit('RR A')    # >> 6 is rotate left twice
				self._emit('RR A')
			elif (p == 7):
				self._emit('RR A')
			self._SFRandOrByte(maskN, mask)
		# self._value &= maskN    # clear out the bit to write
		# self._value |= valMask  # write in the new bits
		return self._code


	def writeSFR(self, value):
		'''This is to write the SFR (by MOV instruction) 
		   We locally simulate this by writing _value.
		   Option: check write permission?
			 if address is over 0xff then it's an XREG. use MOVX.
		'''
		if value is None:
			return
		if isinstance(value, CodeCapsule):
			self._code = value
		else:
			self._code = CodeCapsule(self._mcu, dest=self,
					src=self)
		if (isinstance(value, SFR)) or (isinstance(value, nrf24e1var.VAR)) \
				or isinstance(value, CodeCapsule):
			# either case the runtime already called value.readSFR() or
			# value.readVar() and put result into A.
			# now is time to write A back into SFR.
			if (self._address > 0xff):
				self._emit('MOV DPTR, #0x%x', self._address)
				self._emit('MOVX @DPTR, A')
			else:
				# need to handle not only constant value but also SFR and VAR
				self._emit('MOV 0x%x, A', self._address)
		elif (isinstance(value, int)):
			if (self._address > 0xff):
				self._emit('MOV DPTR, #0x%x', self._address)
				self._emit('MOV A, #0x%x', value)
				self._emit('MOVX @DPTR, A')
			else:
				# need to handle not only constant value but also SFR and VAR
				self._emit('MOV 0x%x, #0x%x', self._address, value)
		else:
			raise Exception('writeSFR unsupported value %s' % value)
		self._value = value
		return self._code

	def getattr(self, name):
		return self.__getattr__(name)

	def __getattr__(self, name):
		'''This is the dot-notation, used for reading a bit field in an
		SFR.  Python will give a syntax error if we do port.1 or a
		dot-digit. so we need to make it an identifier by port._1 instead.
		Decide whether it is a read byte, read slice (done as a
		read-byte, followed by masking), or read bit operation.
		'''
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		# print "sfr.__getattr__(%s)" % name
		if len(name) == 2 and name[0] == '_' and name[1] in '01234567':
			self._code = CodeCapsule(self._mcu, src=self,
					dest=self._mcu.lookupVar('C'))  # outlet is assumed to be accumulator?
			# special handling: as bit index
			bitindex = int(name[1])
			# If the SFR is bit addressable (i.e., modulo 8) then access
			# using a bit instruction. Otherwise, access as word and return
			# value.
			return self._readBit(self._address, bitindex)
		else:
			self._code = CodeCapsule(self._mcu, src=self,
					dest=self._mcu.lookupVar('A'))  # outlet is assumed to be accumulator?

		if not self._defn.has_key('bitfields') or \
				not self._defn['bitfields'].has_key(name):
			# uh oh... no bit name has been defined for it
			raise NameError("bit name `%s' not found in SFR `%s'" % (name, self._name))
		# need to determine slice size.
		# this should work. if no 'slice' entry then original definition
		# is malformed!!
		s = self._defn['bitfields'][name]['slice']
		if (len(s) == 1):
			# this is a bit access.
			return self._readBit(self._address, s[0])
		# otherwise, we have a slice. read as a byte first,
		# then mask it and extract.
		if (len(s) != 2):
			# if neither 1 or 2, then definition is malformed!
			raise NameError('malformed slice %s' % s)
		# Now, construct the mask from bit s[0] downto s[1]
		# find out many bits wide, shift (1 << bitsWide) - 1
		# example. 2 bit wide: (1 << 2 = 4)-1 = 3 = 0b11
		# then, shift the mask up to s[1] position.
		mask = ((1 << (s[0]-s[1]+1)) - 1) << s[1]
		self._loadByte(self._address)
		self._AandByte(mask)
		# now shift right, using a combination of rotate and swap.
		# Because we already masked out the lower bits, rotate will not
		# cause problems.
		# >> 1: rotate right once. >> 2: rotate right twice.
		# >> 3: swap and rotate left once. # >> 4: swap.
		# >> 5: swap and rotate right once. # >> 6: rotate left twice
		# >> 7: rotate left once.
		p = s[1]   # make the code shorter
		if (p == 0):
			pass  # nothing to do. the result is ready.
		elif (p == 1):
			self._emit('RR A')  # rotate right once is like shifting right
		elif (p == 2):
			self._emit('RR A')
			self._emit('RR A')  # shifting right twice = two rotate rights
		elif (p == 3):
			self._emit('SWAP A')  # swap is left or right by 4 positions
			self._emit('RL A')    # shift one position back
		elif (p == 4):
			self._emit('SWAP A')  # swap is shift by 4 positions
		elif (p == 5):
			self._emit('SWAP A')
			self._emit('RR A')    # 4 positions + 1
		elif (p == 6):
			self._emit('RL A')    # >> 6 is rotate left twice
			self._emit('RL A')
		elif (p == 7):
			self._emit('RL A')
		# self._A = (self._value & mask) >> p
		return self._code

	def _emit (self, formatStr, *operands):
		self._code.emit(formatStr, *operands)

	def _loadBit(self, bitAddress):
		self._emit('MOV C, 0x%x', bitAddress)
		# self._C = (self._value >> (bitAddress & 0x7) ) & 1
		return self._code

	def _writeBit(self, address, bitindex, value):
		'''
			use either setb or clr if bit addressable,
			or use AND/OR trick
		'''
		if self._address % 8 != 0 or self._address > 0xff:
			# must AND or OR the mask byte depending on if 0 or 1.
			mask = (1 << bitindex)
			if (isinstance(value, int)): # maybe also allow string of '0''1'
				if (value == 0):
					# and with the bit cleared: invert mask
					mask ^= 0xff
					self._SFRandByte(mask)
					self._value &= mask
					return self._code
				elif (value == 1):
					# OR with the bit set
					self._SFRorByte(mask)
					self._value |= mask
					return self._code
				else:
					# value too large
					raise ValueError('value %d overflow for bit assignment' %
							value)
			else: # assume bit is in C
				# use the Rotate-through-C trick!
				self._loadByte(self._address)
				if (bitindex == 7):
					self._emit('RLC A')  # rotate left thru C, so bit 7 is replaced by C!
					self._emit('RR A')   # rotate back, so C replaces bit 7
				elif (bitindex == 6):
					self._emit('RL A')
					self._emit('RLC A')
					self._emit('RR A')
					self._emit('RR A')
				elif (bitindex == 5):
					self._emit('RL A')
					self._emit('RL A')
					self._emit('RLC A')
					self._emit('RL A')
					self._emit('SWAP A')
				elif (bitindex == 4):
					self._emit('SWAP A')
					self._emit('RRC A')
					self._emit('RL A')
					self._emit('SWAP A')
				elif (bitindex == 3):
					self._emit('SWAP A')
					self._emit('RLC A')
					self._emit('RR A')
					self._emit('SWAP A')
				elif (bitindex == 2):
					self._emit('RR A')
					self._emit('RR A')
					self._emit('RRC A')
					self._emit('SWAP A')
					self._emit('RR A')
				elif (bitindex == 1):
					self._emit('RR A')
					self._emit('RRC A')
					self._emit('RL A')
					self._emit('RL A')
				elif (bitindex == 0):
					self._emit('RRC A')
					self._emit('RL A')
				return self._code

		else:  # modulo 8 => bit address is simply byte address + bitindex
			# use setb or clr
			if (isinstance(value, int)):
				if (value == 0):
					self._emit('CLR 0x%x', (address+bitindex))
					self._value &= (0xff ^ (1 << bitindex))
					return self._code
				elif (value == 1):
					self._emit('SETB 0x%x', (address+bitindex))
					self._value |= (1 << bitindex)
					return self._code
				else:
					# value too large
					raise ValueError('value %d overflow for bit assignment' %
							value)
			else: # assume bit is in C
				self._emit('MOV 0x%x, C', (address+bitindex))
				return self._code
		raise ValueError('binary value expected but %s given' % value)

	def _readBit(self, address, bitindex):
		'''uses either MOV byte and extract bit or MOV bit instruction to
			read the bit at address.bitindex from memory.
			If it is a multiple of 8 then it can use bit MOV instruction.
			otherwise, it must use byte MOV instruction and extract bit.
		'''
		if (address > 0xff) or (address % 8 != 0):
			# do byte access and extract bit
			self._loadByte(self._address) # this does it to memory with MOV
			return self._extractBit(bitindex)  # save in bit accumulator C
			# was: return (self._value >> bitindex) & 1
		else:
			# the bit address is simply the byte address + bit index!
			# by 8051 convention.
			return self._loadBit(self._address + bitindex)


	def _loadByte(self, address):
		'''This generates the MOV instruction to move in a byte if SFR,
		   or use MOVX if XREG (address > 255)
		'''
		if (self._address <= 0xff):
			self._emit('MOV A, 0x%x', address)
		else:
			self._emit('MOV DPTR, #0x%x', address)
			self._emit('MOVX A, @DPTR')

		# self._A = self._value 
		return self._code

	def _AorByte(self, mask):
		'''This generates ORL code to and A with a mask, put back to A.
		   This does not overwrite the result, as it is only temporary
			 variable.
		'''
		self._emit('ORL A, #0x%x', mask)
		# self._A |= mask
		return self._code

	def _AandByte(self, mask):
		'''This generates ANL code to and A with a mask, put back to A.
		   This does not overwrite the result, as it is only temporary
			 variable.
		'''
		self._emit('ANL A, #0x%x', mask)
		# self._A &= mask
		return self._code

	def _SFRorByte(self, mask):
		'''This generates ORL code to OR SFR with a mask and put back to
		SFR.'''
		if (self._address <= 0xff):
			self._emit('ORL 0x%x, #0x%x', self._address, mask)
		else:
			# read in the byte, OR it into A, and write back.
			self._loadByte(self._address)
			self._AorByte(mask)
			self._emit('MOVX @DPTR, A')  # no need to change DPTR address!
		return self._code

	def _SFRandByte(self, mask):
		'''This generates ANL code to and SFR with a mask and put back to
		SFR.'''
		if (self._address <= 0xff):
			self._emit('ANL 0x%x, #0x%x', self._address, mask)
		else:
			# read in the byte, AND it into A, and write it back
			self._loadByte(self._address)
			self._AandByte(mask)
			self._emit('MOVX @DPTR, A')  # no need to change DPTR address!
		return self._code

	def _SFRandOrByte(self, maskN, mask):
		'''The value to assign is in A.
		   but we need to construct a mask that we can AND in to the
			 target.  So, we do A |= maskN  (maskN is the unchanged bits)
			 save A into temp, then load target byte into A,
			 A |= mask, then A &= temp.
			 finally, write back. avoid unnecessary reloading.
		'''
		self._AorByte(maskN)  # make mask of bits to clear in A
		temp = self._code.allocTemp()
		self._emit('MOV R%d, A', temp.varAddress())  # Save A into R0 as temporary
		if (self._address <= 0xff):
			self._emit('ORL 0x%x, #0x%x', self._address, mask)
					# turn on all bits to be affected
			self._emit('ANL A, R%d', temp.varAddress()) # clear affected bits
		else:
			self._loadByte(self._address)
			self._AorByte(mask)  # turn on all bits affected
			self._emit('ANL A R%d', temp.varAddress()) # clear affected bits
			self._storeByte()  # no need to change DPTR address!
		self._code.freeTemp(temp)
		return self._code

	def _extractBit(self, bitindex):
		'''This puts the A.index bit into C'''
		self._emit('MOV C, ACC.%d', bitindex)
		# self._C = (self._A >> bitindex) & 1
		return self._code

	def readSFR(self, dest=None):
		'''This is called by the mcu.SFR to generate instructions to
		   load from SFR as a byte
		'''
		if dest is None: dest = self._mcu.lookupVar('A')
		self._code = CodeCapsule(self._mcu, src=self,
				dest=dest)
		return self._loadByte(self._address)

	def _storeByte(self):
		'''This is the outside routine to write value in A
		   into this SFR (by MOV instruction)
			 if address is more than 1-byte then it's an XREG. use MOVX
			 instead.
		'''
		if (self._address > 0xff):
			self._emit('MOVX @DPTR, A')  # no need to change DPTR address!
		else:
			self._emit('MOV 0x%x, A', self._address)
		return self._code

	def name():
		return self._name

	def __repr__(self):
		return str(self.__class__.__name__+"('"+self._name+"')")

	def __str__(self):
		return repr(self)

	#### making everything int compatible ####

	def __int__(self):
		return self._value

	def __hex__(self):
		return hex(self._value)

	# to do: (8/29)
	# - use [ ] operator for bit addressing?
	#   this can be viewed as alternative syntax for the dot notation?
	# - perhaps the function-call version?
	# - SFR "aliases": 
	#   example: AB  = A concatenated with B
	#   example: a lot of SFRs with the H and L (high and low)
	#   arbitrary variables
	#   => such an alias would not have one address!
  #   => probably should not handle as subclass of SFR?


	# any need for other operations? both evaluate locally and generate
	# code remotely?


if __name__ == '__main__':
	c = nRF24E1SFR()
	c.sanityCheck()
	ADCCON = SFR('ADCCON')
	ADCCON.ADCSEL
	ADC_STATIC = SFR('ADC_STATIC')
	ADC_STATIC.SLEEP
	ADC_STATIC.CLK8
	ADC_STATIC.ADCBIAS
	ADC_STATIC.ADCRES
