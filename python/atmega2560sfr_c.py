'''
	This is an attempt to model the ATMega2560 MCU in terms of access to SFR.
	It is a candidate for restructuring.
	Address   Registers
	00 - 1F:  32 registers (directly bit addressable also using SBI and CBI)
	20 - 5F:  64 I/O registers (used by IN and OUT but mapped to I/O address 00-3F)
	60 - 1FF: 416 External I/O registers (need LD/ST instructions)
	200 - 21FF: Internal SRAM (8192 x 8 bits)
	2200 - FFFF: External SRAM (0 - 64K x 8 bits)


	This version, as opposed to atmega2560sfr.py, is temporary while
	I'm playing around with generating C instead of AVR assembly.
	(actually so far it's still the same, except for importing cc_c just below)
'''
# import atmega2560var
from cc_c import CC_C as CodeCapsule
class ATMEGA2560SFR:
	'''
		This class ATMEGA2560SFR is just a container for two static hash
		tables of hash tables of stuff to provide the SFR definitions:
	'''

	# ATMega2560 document
	# http://www.atmel.com/images/doc2549.pdf

	_SFR = {

			'PINA': {
					'address': 0x20, 'module': 'GPIO',
					'description': 'Port A Input Pins Address',
					'bitfields': {
							'PINA7': {
									'slice': (7,),
									'default': 0, 'access': 'R/W',
							},
							'PINA6': {
									'slice': (6,),
									'default': 0, 'access': 'R/W',
							},
							'PINA5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PINA4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PINA3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PINA2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PINA1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PINA0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRA': {
					'address': 0x21, 'module': 'GPIO',
					'description': 'Port A Data Direction Register',
					'bitfields': {
							'DDA7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'DDA6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'DDA5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDA4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDA3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDA2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDA1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDA0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTA': {
					'address': 0x22, 'module': 'GPIO',
					'description': 'Port A Data Register',
					'bitfields': {
							'PORTA7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'PORTA6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'PORTA5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTA4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTA3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTA2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTA1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTA0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},

			'PINB': {
					'address': 0x23, 'module': 'GPIO',
					'description': 'Port B Input Pins Address',
					'bitfields': {
							'PINB7': {
									'slice': (7,),
									'default': 0, 'access': 'R/W',
							},
							'PINB6': {
									'slice': (6,),
									'default': 0, 'access': 'R/W',
							},
							'PINB5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PINB4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PINB3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PINB2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PINB1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PINB0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRB': {
					'address': 0x24, 'module': 'GPIO',
					'description': 'Port B Data Direction Register',
					'bitfields': {
							'DDB7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'DDB6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'DDB5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDB4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDB3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDB2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDB1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDB0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTB': {
					'address': 0x25, 'module': 'GPIO',
					'description': 'Port B Data Register',
					'bitfields': {
							'PORTB7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'PORTB6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'PORTB5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTB4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTB3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTB2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTB1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTB0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},

			'PINC': {
					'address': 0x26, 'module': 'GPIO',
					'description': 'Port C Input Pins Address',
					'bitfields': {
							'PINC7': {
									'slice': (7,),
									'default': 0, 'access': 'R/W',
							},
							'PINC6': {
									'slice': (6,),
									'default': 0, 'access': 'R/W',
							},
							'PINC5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PINC4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PINC3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PINC2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PINC1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PINC0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRC': {
					'address': 0x27, 'module': 'GPIO',
					'description': 'Port C Data Direction Register',
					'bitfields': {
							'DDC7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'DDC6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'DDC5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDC4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDC3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDC2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDC1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDC0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTC': {
					'address': 0x28, 'module': 'GPIO',
					'description': 'Port C Data Register',
					'bitfields': {
							'PORTC7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'PORTC6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'PORTC5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTC4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTC3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTC2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTC1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTC0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},

			'PIND': {
					'address': 0x29, 'module': 'GPIO',
					'description': 'Port D Input Pins Address',
					'bitfields': {
							'PIND7': {
									'slice': (7,),
									'default': 0, 'access': 'R/W',
							},
							'PIND6': {
									'slice': (6,),
									'default': 0, 'access': 'R/W',
							},
							'PIND5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PIND4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PIND3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PIND2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PIND1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PIND0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRD': {
					'address': 0x2A, 'module': 'GPIO',
					'description': 'Port D Data Direction Register',
					'bitfields': {
							'DDD7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'DDD6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'DDD5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDD4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDD3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDD2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDD1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDD0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTD': {
					'address': 0x2B, 'module': 'GPIO',
					'description': 'Port D Data Register',
					'bitfields': {
							'PORTD7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'PORTD6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'PORTD5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTD4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTD3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTD2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTD1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTD0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},

			'PINE': {
					'address': 0x2C, 'module': 'GPIO',
					'description': 'Port E Input Pins Address',
					'bitfields': {
							'PINE7': {
									'slice': (7,),
									'default': 0, 'access': 'R/W',
							},
							'PINE6': {
									'slice': (6,),
									'default': 0, 'access': 'R/W',
							},
							'PINE5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PINE4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PINE3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PINE2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PINE1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PINE0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRE': {
					'address': 0x2D, 'module': 'GPIO',
					'description': 'Port E Data Direction Register',
					'bitfields': {
							'DDE7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'DDE6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'DDE5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDE4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDE3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDE2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDE1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDE0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTE': {
					'address': 0x2E, 'module': 'GPIO',
					'description': 'Port E Data Register',
					'bitfields': {
							'PORTE7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'PORTE6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'PORTE5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTE4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTE3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTE2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTE1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTE0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},

			'PINF': {
					'address': 0x2F, 'module': 'GPIO',
					'description': 'Port F Input Pins Address',
					'bitfields': {
							'PINF7': {
									'slice': (7,),
									'default': 0, 'access': 'R/W',
							},
							'PINF6': {
									'slice': (6,),
									'default': 0, 'access': 'R/W',
							},
							'PINF5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PINF4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PINF3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PINF2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PINF1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PINF0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRF': {
					'address': 0x30, 'module': 'GPIO',
					'description': 'Port F Data Direction Register',
					'bitfields': {
							'DDF7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'DDF6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'DDF5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDF4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDF3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDF2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDF1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDF0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTF': {
					'address': 0x31, 'module': 'GPIO',
					'description': 'Port F Data Register',
					'bitfields': {
							'PORTF7': {
									'slice': (7,), 'default': 0, 'access': 'R/W',
							},
							'PORTF6': {
									'slice': (6,), 'default': 0, 'access': 'R/W',
							},
							'PORTF5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTF4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTF3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTF2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTF1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTF0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},

			'PING': {
					'address': 0x32, 'module': 'GPIO',
					'description': 'Port G Input Pins Address',
					'bitfields': {
							'PING5': {
									'slice': (5,),
									'default': 0, 'access': 'R/W',
							},
							'PING4': {
									'slice': (4,),
									'default': 0, 'access': 'R/W',
							},
							'PING3': {
									'slice': (3,),
									'default': 0, 'access': 'R/W',
							},
							'PING2': {
									'slice': (2,),
									'default': 0, 'access': 'R/W',
							},
							'PING1': {
									'slice': (1,),
									'default': 0, 'access': 'R/W',
							},
							'PING0': {
									'slice': (0,),
									'default': 0, 'access': 'R/W',
							},
					},
				},
			'DDRG': {
					'address': 0x33, 'module': 'GPIO',
					'description': 'Port G Data Direction Register',
					'bitfields': {
							'DDG5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'DDG4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'DDG3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'DDG2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'DDG1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'DDGF0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'PORTG': {
					'address': 0x34, 'module': 'GPIO',
					'description': 'Port G Data Register',
					'bitfields': {
							'PORTG5': {
									'slice': (5,), 'default': 0, 'access': 'R/W',
							},
							'PORTG4': {
									'slice': (4,), 'default': 0, 'access': 'R/W',
							},
							'PORTG3': {
									'slice': (3,), 'default': 0, 'access': 'R/W',
							},
							'PORTG2': {
									'slice': (2,), 'default': 0, 'access': 'R/W',
							},
							'PORTG1': {
									'slice': (1,), 'default': 0, 'access': 'R/W',
							},
							'PORTG0': {
									'slice': (0,), 'default': 0, 'access': 'R/W',
							},
					},
				},
			'TIFR0': {
					'address': 0x35, 'module': 'Timer',
					'description': 'Timer/Counter 0 Interrupt Flag Register',
					'bitfields': {
							'OCF0B': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 0 Output Compare B Match Flag

The OCF0B bit is set when a Compare Match occurs between the Timer/Counter and the data in OCR0B - Output Compare Register0 B.  OCF0B is cleared by hardware when executing the corresponding interrupt handling vector.  Alternatively, OCF0B is cleared by writing a logic one to the flag.  When the I-bit SREG, OCIE0B (Timer/Counter Compare B Match Interrupt Enable), and OCF0B are set, the Timer/Counter Compare Match Interrupt is executed.''',
								},
							'OCF0A': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 0 Output Compare A Match Flag

The OCF0A bit is set when a Compare Match occurs between the Timer/Counter0 and the data in OCR0A - Output Compare Register0 A.  OCF0A is cleared by hardware when executing the corresponding interrupt handling vector.  Alternatively, OCF0A is cleared by writing a logic one to the flag.  When the I-bit SREG, OCIE0A (Timer/Counter0 Compare Match Interrupt Enable), and OCF0A are set, the Timer/Counter0 Compare Match Interrupt is executed.''',
								},
							'TOV0': {
								'slice': (0,),
								'access': 'R/W',
								'default': 0,
								'description': '''Timer/Counter0 Overflow Flag

The bit TOV0 is set when an overflow occurs in Timer/Counter0.  TOV0 is cleared by hardware when executing the corresponding interrupt handling vector. Alternatively, TOV0 is cleared by writing a logic one to the flag.  When the SREG I-bit, TOIE0 (Timer/Counter0 Overflow Interrupt Enable), and TOV0 are set, the Timer/Counter0 Overflow Interrupt is executed.

The setting of this flag is dependent of the WGM0 2:0 bit setting. Refer to Table 16-8, "Waveform Generation Mode Bit Description" on page 131.''',
								},
						},
				},
			'TIFR1': {
					'address': 0x36, 'module': 'Timer',
					'description': 'Timer/Counter 1 Interrupt Flag Register',
					'bitfields': {
							'ICF1': {
								'slice': (5,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 1, Interupt Capture Flag

This flag is set when a capture event occurs on the ICP1 pin. When the Interrupt Capture Register (CR1) is set by the WGM1 3:0 to be used as the TOP value, the ICF1 flag is set when the counter reaches the TOP value.

ICF1 is automatically cleared when the Input Capture Interrupt Vector is executed. Alternatively, ICF1 can be cleared by writing a logic one to its bit location.''',
							},
							'OCF1C': {
								'slice': (3,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 1, Output Compare C Match Flag

This flag is set in the timer clock cycle after the counter (TCNT1) value matches the Output Compare Register C (OCR1C).

Note that a Forced Output Compare (FOC1C) strobe will not set the CCF1C Flag.

OCF1C is automatically cleared when the Output Compare Match C Interrupt Vector is executed. Alternatively, OCF1C can be cleared by writing a logic one to its bit location.
''',
							},
							'OCF1B': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 1, Output Compare B Match Flag

This flag is set in the timer clock cycle after the counter (TCNT1) value matches the Output Compare Register B (OCR1B).

Note that a Forced Output Compare (FOC1B) strobe will not set the OCF1B Flag.

OCF1B is automatically cleared when the Output Compare Match B Interrupt Vector is executed. Alternatively, OCF1B can be cleared by writing a logic one to its bit location.''',
								},
							'OCF1A': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 1, Output Compare A Match Flag

This flag is set in the timer clock cycle after the counter (TCNT1) value matches the Output Compare Register A (OCR1A).

Note that a Forced Output Compare (FOC1A) strobe will not set the OCF1A Flag.

OCF1A is automatically cleared when the Output Compare Match A Interrupt Vector is executed. Alternatively, OCF1A can be cleared by writing a logic one to its bit location.''',
								},
							'TOV1': {
								'slice': (0,),
								'access': 'R/W',
								'default': 0,
								'description': '''Timer/Counter 1, Overflow Flag

The setting of this flag is dependent of the WGM1 3:0 bits setting. In Normal and CTC modes, the TOV1 Flag is set when the timer overflows. Refer to Table 17-2 on page 148 for the TOV1 Flag behavior when using another WGM1 3:0 bit setting.

TOV1 is automtaically cleared when the Timer/Counter 1 Overflow Interrupt Vector is executed. Alternatvely, TOV1 can be cleared by writing a logic one to its bit location.''',
								},
						},
				},
			'TIFR2': {
					'address': 0x37, 'module': 'Timer',
					'description': 'Timer/Counter 2 Interrupt Flag Register',
					'bitfields': {
							'OCF2B': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 2 Output Compare B Match Flag

The OCF2B bit is set (one) when a compare match occurs between the Timer/Counter2 and the data in OCR2B - Output Compare Register2.  OCF2B is cleared by hardware when executing the corresponding interrupt handling vector.  Alternatively, OCF2B is cleared by writing a logic one to the flag.  When the I-bit SREG, OCIE2B (Timer/Counter2 Compare B Match Interrupt Enable), and OCF2B are set, the Timer/Counter2 Compare Match Interrupt is executed.''',
								},
							'OCF2A': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Output Compare Flag 2 A

The OCF2A bit is set (one) when a compare match occurs between the Timer/Counter2 and the data in OCR2A - Output Compare Register2.  OCF2A is cleared by hardware when executing the corresponding interrupt handling vector.  Alternatively, OCF2A is cleared by writing a logic one to the flag.  When the I-bit SREG, OCIE2A (Timer/Counter2 Compare Match Interrupt Enable), and OCF2A are set, the Timer/Counter2 Compare Match Interrupt is executed.''',
								},
							'TOV2': {
								'slice': (0,),
								'access': 'R/W',
								'default': 0,
								'description': '''Timer/Counter2 Overflow Flag

The bit TOV2 is set (one) when an overflow occurs in Timer/Counter2.  TOV2 is cleared by hardware when executing the corresponding interrupt handling vector. Alternatively, TOV2 is cleared by writing a logic one to the flag.  When the SREG I-bit, TOIE2A (Timer/Counter2 Overflow Interrupt Enable), and TOV2 are set, the Timer/Counter2 Overflow Interrupt is executed.  In PWM mode, this bit is set when Timer/Counter2 changes counting direction at 0x00.''',
								},
						},
				},
			'TIFR3': {
					'address': 0x38, 'module': 'Timer',
					'description': 'Timer/Counter 3 Interrupt Flag Register',
					'bitfields': {
							'ICF3': {
								'slice': (5,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 3, Interupt Capture Flag

This flag is set when a capture event occurs on the ICP3 pin. When the Interrupt Capture Register (CR3) is set by the WGM3 3:0 to be used as the TOP value, the ICF3 flag is set when the counter reaches the TOP value.

ICF3 is automatically cleared when the Input Capture Interrupt Vector is executed. Alternatively, ICF3 can be cleared by writing a logic one to its bit location.''',
							},
							'OCF3C': {
								'slice': (3,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 3, Output Compare C Match Flag

This flag is set in the timer clock cycle after the counter (TCNT3) value matches the Output Compare Register C (OCR3C).

Note that a Forced Output Compare (FOC3C) strobe will not set the CCF3C Flag.

OCF3C is automatically cleared when the Output Compare Match C Interrupt Vector is executed. Alternatively, OCF3C can be cleared by writing a logic one to its bit location.
''',
							},
							'OCF3B': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 3, Output Compare B Match Flag

This flag is set in the timer clock cycle after the counter (TCNT3) value matches the Output Compare Register B (OCR3B).

Note that a Forced Output Compare (FOC3B) strobe will not set the OCF3B Flag.

OCF3B is automatically cleared when the Output Compare Match B Interrupt Vector is executed. Alternatively, OCF3B can be cleared by writing a logic one to its bit location.''',
								},
							'OCF3A': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 3, Output Compare A Match Flag

This flag is set in the timer clock cycle after the counter (TCNT3) value matches the Output Compare Register A (OCR3A).

Note that a Forced Output Compare (FOC3A) strobe will not set the OCF3A Flag.

OCF3A is automatically cleared when the Output Compare Match A Interrupt Vector is executed. Alternatively, OCF3A can be cleared by writing a logic one to its bit location.''',
								},
							'TOV3': {
								'slice': (0,),
								'access': 'R/W',
								'default': 0,
								'description': '''Timer/Counter 3, Overflow Flag

The setting of this flag is dependent of the WGM3 3:0 bits setting. In Normal and CTC modes, the TOV3 Flag is set when the timer overflows. Refer to Table 17-2 on page 148 for the TOV3 Flag behavior when using another WGM3 3:0 bit setting.

TOV3 is automtaically cleared when the Timer/Counter 3 Overflow Interrupt Vector is executed. Alternatvely, TOV3 can be cleared by writing a logic one to its bit location.''',
								},
						},
				},
			'TIFR4': {
					'address': 0x39, 'module': 'Timer',
					'description': 'Timer/Counter 4 Interrupt Flag Register',
					'bitfields': {
							'ICF4': {
								'slice': (5,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 4, Interupt Capture Flag

This flag is set when a capture event occurs on the ICP4 pin. When the Interrupt Capture Register (CR4) is set by the WGM4 4:0 to be used as the TOP value, the ICF4 flag is set when the counter reaches the TOP value.

ICF4 is automatically cleared when the Input Capture Interrupt Vector is executed. Alternatively, ICF4 can be cleared by writing a logic one to its bit location.''',
							},
							'OCF4C': {
								'slice': (3,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 4, Output Compare C Match Flag

This flag is set in the timer clock cycle after the counter (TCNT4) value matches the Output Compare Register C (OCR4C).

Note that a Forced Output Compare (FOC4C) strobe will not set the CCF4C Flag.

OCF4C is automatically cleared when the Output Compare Match C Interrupt Vector is executed. Alternatively, OCF4C can be cleared by writing a logic one to its bit location.
''',
							},
							'OCF4B': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 4, Output Compare B Match Flag

This flag is set in the timer clock cycle after the counter (TCNT4) value matches the Output Compare Register B (OCR4B).

Note that a Forced Output Compare (FOC4B) strobe will not set the OCF4B Flag.

OCF4B is automatically cleared when the Output Compare Match B Interrupt Vector is executed. Alternatively, OCF4B can be cleared by writing a logic one to its bit location.''',
								},
							'OCF4A': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 4, Output Compare A Match Flag

This flag is set in the timer clock cycle after the counter (TCNT4) value matches the Output Compare Register A (OCR4A).

Note that a Forced Output Compare (FOC4A) strobe will not set the OCF4A Flag.

OCF4A is automatically cleared when the Output Compare Match A Interrupt Vector is executed. Alternatively, OCF4A can be cleared by writing a logic one to its bit location.''',
								},
							'TOV4': {
								'slice': (0,),
								'access': 'R/W',
								'default': 0,
								'description': '''Timer/Counter 4, Overflow Flag

The setting of this flag is dependent of the WGM4 3:0 bits setting. In Normal and CTC modes, the TOV4 Flag is set when the timer overflows. Refer to Table 17-2 on page 148 for the TOV4 Flag behavior when using another WGM4 3:0 bit setting.

TOV4 is automtaically cleared when the Timer/Counter 4 Overflow Interrupt Vector is executed. Alternatvely, TOV4 can be cleared by writing a logic one to its bit location.''',
								},
						},
				},
			'TIFR5': {
					'address': 0x3A, 'module': 'Timer',
					'description': 'Timer/Counter 5 Interrupt Flag Register',
					'bitfields': {
							'ICF5': {
								'slice': (5,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 5, Interupt Capture Flag

This flag is set when a capture event occurs on the ICP5 pin. When the Interrupt Capture Register (CR5) is set by the WGM5 3:0 to be used as the TOP value, the ICFn flag is set when the counter reaches the TOP value.

ICF5 is automatically cleared when the Input Capture Interrupt Vector is executed. Alternatively, ICFn can be cleared by writing a logic one to its bit location.''',
							},
							'OCF5C': {
								'slice': (3,), 'access': 'R/W', 'default': 0,
								'description': '''Timer/Counter 5, Output Compare C Match Flag

This flag is set in the timer clock cycle after the counter (TCNT5) value matches the Output Compare Register C (OCR5C).

Note that a Forced Output Compare (FOC5C) strobe will not set the CCF5C Flag.

OCF5C is automatically cleared when the Output Compare Match C Interrupt Vector is executed. Alternatively, OCF5C can be cleared by writing a logic one to its bit location.
''',
							},
							'OCF5B': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 5, Output Compare B Match Flag

This flag is set in the timer clock cycle after the counter (TCNT5) value matches the Output Compare Register B (OCR5B).

Note that a Forced Output Compare (FOC5B) strobe will not set the OCF5B Flag.

OCF5B is automatically cleared when the Output Compare Match B Interrupt Vector is executed. Alternatively, OCF5B can be cleared by writing a logic one to its bit location.''',
								},
							'OCF5A': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0, 
								'description': '''Timer/Counter 5, Output Compare A Match Flag

This flag is set in the timer clock cycle after the counter (TCNT5) value matches the Output Compare Register A (OCR5A).

Note that a Forced Output Compare (FOC5A) strobe will not set the OCF5A Flag.

OCF5A is automatically cleared when the Output Compare Match A Interrupt Vector is executed. Alternatively, OCF5A can be cleared by writing a logic one to its bit location.''',
								},
							'TOV5': {
								'slice': (0,),
								'access': 'R/W',
								'default': 0,
								'description': '''Timer/Counter 5, Overflow Flag

The setting of this flag is dependent of the WGM5 3:0 bits setting. In Normal and CTC modes, the TOV5 Flag is set when the timer overflows. Refer to Table 17-2 on page 148 for the TOV5 Flag behavior when using another WGM5 3:0 bit setting.

TOV5 is automtaically cleared when the Timer/Counter 5 Overflow Interrupt Vector is executed. Alternatvely, TOV5 can be cleared by writing a logic one to its bit location.''',
								},
						},
				},
				'PCIFR': {
						'address': 0x3B, 'module': 'interrupt',
						'bitfields': {
							'PCIF2': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': '''Pin Change Interrupt Flag 1

When a logic change on any PCINT23:16 pin triggers an interrupt request,
PCIF2 becomes set (one). If the I-bit in SREG and the PCIE2 bit in PCICR are
set (one), the MCU will jump to the corresponding Interrupt Vector. The flag
is cleared when the interrupt routine is executed. Alternatively, the flag
can be cleared by writing a logical one to it.''',
								},
							'PCIF1': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description': '''PCIF1: Pin Change Interrupt Flag 1

When a logic change on any PCINT15:8 pin triggers an interrupt request, PCIF1 becomes set (one). If the I-bit in SREG and the PCIE1 bit in PCICR are set (one), the MCU will jump to the corresponding Interrupt Vector. The flag is cleared when the interrupt routine is executed. Alternatively, the flag can be cleared by writing a logical one to it.''',
								},
							'PCIF0': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
									'description': '''PCIF0: Pin Change Interrupt Flag 0

When a logic change on any PCINT7:0 pin triggers an interrupt request, PCIF0 becomes set (one). If the I-bit in SREG and the PCIE0 bit in PCICR are set (one), the MCU will jump to the corresponding Interrupt Vector. The flag is cleared when the interrupt routine is executed. Alternatively, the flag can be cleared by writing a logical one to it.''',
								},
							},
				},
				'EIFR': {
						'address': 0x3C, 'module': 'CPU',
						'access': 'R/W', 'default': 0,
						'bitfields': {
								'INTF7': {
										'slice': (7,),
									},
								'INTF6': {
										'slice': (6,),
									},
								'INTF5': {
										'slice': (5,),
									},
								'INTF4': {
										'slice': (4,),
									},
								'INTF3': {
										'slice': (3,),
									},
								'INTF2': {
										'slice': (2,),
									},
								'INTF1': {
										'slice': (1,),
									},
								'INTF0': {
										'slice': (7,),
									},
							},
						'description': '''INTF7:0: External Interrupt Flags 7 - 0

When an edge or logic change on the INT7:0 pin triggers an interrupt request, INTF7:0 becomes set (one). If the I-bit in SREG and the corresponding interrupt enable bit, INT7:0 in EIMSK, are set (one), the MCU will jump to the interrupt vector.  The flag is cleared when the interrupt routine is executed.  Alternatively, the flag can be cleared by writing a logical one to it. These flags are always cleared when INT7:0 are configured as level interrupt. Note that when entering sleep mode with the INT3:0 interrupts disabled, the input buffers on these pins will be disabled. This may cause a logic change in internal signals which will set the INTF3:0 flags. See "Digital Input Enable and Sleep Modes" on page 74 for more information.''',
				},
				'EIMSK': {
						'address': 0x3D, 'module': 'CPU', 'access': 'R/W', 'default': 0,
						'description': '''INT7:0: External Interrupt Request 7 - 0 Enable

When an INT7:0 bit is written to one and the I-bit in the Status Register (SREG) is set (one), the corresponding external pin interrupt is enabled.  The Interrupt Sense Control bits in the External Interrupt Control Registers - EICRA and EICRB - defines whether the external interrupt is activated on rising or falling edge or level sensed. Activity on any of these pins will trigger an interrupt request even if the pin is enabled as an output. This provides a way of generating a software interrupt.

''',
				},
				'GPIOR0': {
						'address': 0x3E, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
						'description': '''General Purpose I/O Register 0''',
					},
				'EECR': {
						'address': 0x1F, 'module': 'EEPROM', 'description': '''The EEPROM Control Register''',
						'bitfields': {
								'EEPM': {
										'slice': (5,4), 'access': 'R/W', 'default': 0,
										'description': '''EEPROM Programming Mode Bits

The EEPROM Programming mode bit setting defines which programming action that will be triggered when writing EEPE. It is possible to program data in one atomic operation (erase the old value and program the new value) or to split the Erase and Write operations in two different operations. The Programming times for the different modes are shown in Table 9-1 on page 36.  While EEPE is set, any write to EEPMn will be ignored. During reset, the EEPMn bits will be reset to 0b00 unless the EEPROM is busy programming.

EEPM<1:0>  Programming Time    Operation
00:            3.4 ms          Erase and Write in one operation (atomic)
01:            1.8 ms          Erase only
10:            1.8 ms          Write only
11:             -              Reserved for future use''',
									},
								'EERIE': {
										'slice': (3,), 'access': 'R/W', 'default': 0,
										'description': '''EEPROM Ready Interrupt Enable

Writing EERIE to one enables the EEPROM Ready Interrupt if the I bit in SREG is set. Writing EERIE to zero disables the interrupt. The EEPROM Ready interrupt generates a constant inter- rupt when EEPE is cleared.''',
									},
								'EEMPE': {
										'slice': (2,), 
									},
							},
					},
				'EEDR': {
						'address': 0x40, 'module': 'EEPROM',  'access': 'R/W', 'default': 0,
						'description': '''EEPROM Data

For the EEPROM write operation, the EEDR Register contains the data to be written to the EEPROM in the address given by the EEAR Register. For the EEPROM read operation, the EEDR contains the data read out from the EEPROM at the address given by EEAR.''',
					},
				'EEARL': {
						'address': 0x41, 'module': 'EEPROM',  'access': 'R/W', 'default': 0,
						'description': '''The EEPROM Address Register low

EEARH and EEARL together specify the EEPROM address in the 4Kbytes EEPROM space. The EEPROM data bytes are addressed linearly between 0 and 4096. The initial value of EEAR is undefined. A proper value must be written before the EEPROM may be accessed.''',
					},
				'EEARH': {
						'address': 0x42, 'module': 'EEPROM',  'description': '''The EEPROM Address Register high

EEARH and EEARL together specify the EEPROM address in the 4Kbytes EEPROM space. The EEPROM data bytes are addressed linearly between 0 and 4096. The initial value of EEAR is undefined. A proper value must be written before the EEPROM may be accessed.''',
						'bitfields': {
								'EEAR11': {
										'slice': (11,), 'access': 'R/W', 'default': 0,
									},
								'EEAR10': {
										'slice': (10,), 'access': 'R/W', 'default': 0,
									},
								'EEAR9': {
										'slice': (9,), 'access': 'R/W', 'default': 0,
									},
								'EEAR8': {
										'slice': (8,), 'access': 'R/W', 'default': 0,
									},
							},
					},
				'GTCCR': {
						'address': 0x23, 'module': 'TimerCounter',
						'description': 'General Timer/Counter Control Register',
						'bitfields': {
								'TSM': {
									'slice': (7,),
									'access': 'R/W',
									'description': '''Timer/Counter Synchronization Mode

Writing the TSM bit to one activates the Timer/Counter Synchronization mode. In this mode, the value that is written to the PSRASY and PSRSYNC bits is kept, hence keeping the correspond- ing prescaler reset signals asserted. This ensures that the corresponding Timer/Counters are halted and can be configured to the same value without the risk of one of them advancing during configuration. When the TSM bit is written to zero, the PSRASY and PSRSYNC bits are cleared by hardware, and the Timer/Counters start counting simultaneously.''',
								},
								'PSRASY': {
									'slice': (1,),
									'access': 'R/W',
									'description': '''Prescaler Reset Timer/Counter2

When this bit is one, the Timer/Counter2 prescaler will be reset. This bit is normally cleared immediately by hardware.  If the bit is written when Timer/Counter2 is operating in asynchronous mode, the bit will remain one until the prescaler has been reset. The bit will not be cleared by hardware if the TSM bit is set. Refer to the description of the "Bit 7 - TSM: Timer/Counter Synchronization Mode" on page 170 for a description of the Timer/Counter Synchronization mode.''',
								'PSRSYNC': {
										'slice': (0,),
										'access': 'R/W',
										'description': '''Prescaler Reset for Synchronous Timer/Counters

When this bit is one, Timer/Counter0, Timer/Counter1, Timer/Counter3, Timer/Counter4 and Timer/Counter5 prescaler will be Reset. This bit is normally cleared immediately by hardware, except if the TSM bit is set. Note that Timer/Counter0, Timer/Counter1, Timer/Counter3, Timer/Counter4 and Timer/Counter5 share the same prescaler and a reset of this prescaler will affect all timers.''',
								},
						},
					},
				},
				'TCCR0A': {
						'address': 0x44, 'module': 'TimerCounter0',
						'description': 'TCCR0A - Timer/Counter Control Register A',
						'bitfields': {
							'COM0A': {
									'slice': (7,6),
									'access': 'R/W',
									'description': '''COM0A Compare Match Output A Mode

These bits control the Output Compare pin (OC0A) behavior. If one or both of the COM0A<1:0> bits are set, the OC0A output overrides the normal port functionality of the I/O pin it is connected to. However, note that the Data Direction Register (DDR) bit corresponding to the OC0A pin must be set in order to enable the output driver.

When OC0A is connected to the pin, the function of the COM0A<1:0> bits depends on the WGM0<2:0> bit setting. Table 16-2 shows the COM0A<1:0> bit functionality when the WGM0<2:0> bits are set to a normal or CTC mode (non-PWM).

COM0A  Description - Compare Output Mode, non-PWM Mode
-----  -----------------------------------------------
00:    Normal port operation, OC0A disconnected
01:    Toggle OC0A on Compare Match
10:    Clear OC0A on Compare Match
11:    Set OC0A on Compare Match

COM0A  Description - Compare Output Mode, Fast PWM Mode
-----  ------------------------------------------------
00:     Normal port operation, OC0A disconnected
01:     WGM02 = 0: Normal Port Operation, OC0A Disconnected 
10:     Clear OC0A on Compare Match, set OC0A at BOTTOM (non-inverting mode)
11:     Set OC0A on Compare Match, clear OC0A at BOTTOM (inverting mode)

Note: A special case occurs when OCR0A equals TOP and COM0A1 is set. In this case, the Compare Match is ignored, but the set or clear is done at BOTTOM. See "Fast PWM Mode" on page 124 for more details.

COM0A   Description - Compare Output Mode, Phase Correct PWM Mode
-----   ---------------------------------------------------------
00:     Normal port operation, OC0A disconnected
01:     WGM02 = 0: Normal Port Operation, OC0A Disconnected
        WGM02 = 1: Toggle OC0A on Compare Match
10:     Clear OC0A on Compare Match when up-counting. Set OC0A on Compare Match when down-counting
11:     Set OC0A on Compare Match when up-counting. Clear OC0A on Compare Match when down-counting

A special case occurs when OCR0A equals TOP and COM0A1 is set. In this case, the Compare Match is ignored, but the set or clear is done at TOP. See "Phase Correct PWM Mode" on page 126 for more details.''',
								},
						'COM0B': {
							'slice': (5,4), 'access': 'R/W', 'default': 0,
							'description': '''Compare Match Output B Mode

These bits control the Output Compare pin (OC0B) behavior. If one or both of the COM0B<1:0> bits are set, the OC0B output overrides the normal port functionality of the I/O pin it is connected to. However, note that the Data Direction Register (DDR) bit corresponding to the OC0B pin must be set in order to enable the output driver.

When OC0B is connected to the pin, the function of the COM0B<1:0> bits depends on the WGM0<2:0> bit setting. Table 16-5 shows the COM0B<1:0> bit functionality when the WGM0<2:0> bits are set to a normal or CTC mode (non-PWM).

COM0B   Description - Compare Output Mode, non-PWM Mode
-----   -----------------------------------------------
00:     Normal port operation, OC0B disconnected
01:     Toggle OC0B on Compare Match
10:     Clear OC0B on Compare Match
11:     Set OC0B on Compare Match

COM0B   Description - Compare Output Mode, Fast PWM Mode
-----   ------------------------------------------------
00:     Normal port operation, OC0B disconnected
01:     Reserved
10:     Clear OC0B on Compare Match, set OC0B at BOTTOM (non-inverting mode)
11:     Set OC0B on Compare Match, clear OC0B at BOTTOM (inverting mode)

A special case occurs when OCR0B equals TOP and COM0B1 is set. In this case, the Compare Match is ignored, but the set or clear is done at BOTTOM. See "Fast PWM Mode" on page 124 for more details.

COM0B   Description - Compare Output Mode, Phase Correct PWM Mode
-----   ---------------------------------------------------------
00:     Normal port operation, OC0B disconnected
01:     Reserved
10:     Clear OC0B on Compare Match when up-counting. Set OC0B on Compare Match when down-counting
11:     Set OC0B on Compare Match when up-counting. Clear OC0B on Compare Match when down-counting

A special case occurs when OCR0B equals TOP and COM0B1 is set. In this case, the Compare Match is ignored, but the set or clear is done at TOP. See "Phase Correct PWM Mode" on page 126 for more details.
''',

						  },
						'Res': {
								'slice': (3,2),
								'description': '''These bits are reserved bits and will always read as zero.''',
							},
						'WGM0': {
								'slice': (1, 0),
								'description': '''Waveform Generation Mode WGM0<1:0>

Combined with the WGM02 bit found in the TCCR0B Register, these bits control the counting sequence of the counter, the source for maximum (TOP) counter value, and what type of waveform generation to be used, see Table 16-8. Modes of operation supported by the Timer/Counter unit are: Normal mode (counter), Clear Timer on Compare Match (CTC) mode, and two types of Pulse Width Modulation (PWM) modes (see "Modes of Operation" on page 148).

Table 16-8. Waveform Generation Mode Bit Description
Mode WGM0<2:0> Timer/Counter Mode of Op  TOP  Update of OCRx at TOV Flag Set on
---- --------- ------------------------  ---  ----------------- ---------------
0     000       Normal                  0xFF     Immediate         MAX
1     001       PWM, Phase Correct      0xFF     TOP               BOTTOM
2     010       CTC                     OCRA     Immediate         MAX
3     011       Fast PWM                0xFF     TOP               MAX
4     100       Reserved                -        -                 -
5     101       PWM, Phase Correct      OCRA     TOP               BOTTOM
6     110       Reserved                -        -                 -
7     111       Fast PWM                OCRA     BOTTOM            TOP

Note: 1. MAX = 0xFF 2. BOTTOM = 0x00
''',
							},
						},
				},
				'TCCR0B': {
					'address': 0x45, 'module': 'TimerCounter0',
					'description': '''Timer/Counter Control Register B''',
					'bitfields': {
						'FOC0A': {
							'slice': (7,),
							'access': 'W',
							'default': 0,
							'description': '''Force Output Compare A

The FOC0A bit is only active when the WGM bits specify a non-PWM mode.  However, for ensuring compatibility with future devices, this bit must be set to zero when TCCR0B is written when operating in PWM mode. When writing a logical one to the FOC0A bit, an immediate Compare Match is forced on the Waveform Generation unit. The OC0A output is changed according to its COM0A<1:0> bits setting. Note that the FOC0A bit is implemented as a strobe.  Therefore it is the value present in the COM0A<1:0> bits that determines the effect of the forced compare.

A FOC0A strobe will not generate any interrupt, nor will it clear the timer in CTC mode using OCR0A as TOP.

The FOC0A bit is always read as zero.''',
						},
						'FOC0B': {
							'slice': (6,),
							'access': 'W',
							'default': 0,
							'description': '''Force Output Compare B

The FOC0B bit is only active when the WGM bits specify a non-PWM mode.

However, for ensuring compatibility with future devices, this bit must be set to zero when TCCR0B is written when operating in PWM mode. When writing a logical one to the FOC0B bit, an immediate Compare Match is forced on the Waveform Generation unit. The OC0B output is changed according to its COM0B<1:0> bits setting. Note that the FOC0B bit is implemented as a strobe.  Therefore it is the value present in the COM0B<1:0> bits that determines the effect of the forced compare.

A FOC0B strobe will not generate any interrupt, nor will it clear the timer in CTC mode using OCR0B as TOP.

The FOC0B bit is always read as zero.''',
						},
						'WGM02': {
							'slice': (3,),
							'access': 'R/W',
							'default': 0,
							'description': '''Waveform Generation Mode

See the description in the "TCCR0A - Timer/Counter Control Register A" on page 129.'''
						},
						'CS0': {
							'slice': (2,0),
							'access': 'R/W',
							'default': 0,
							'description': '''Clock Select

The three Clock Select bits select the clock source to be used by the Timer/Counter, see Table 16-9 on page 133.  

Clock Select Bit Description

CS0<2:0>  Description
--------  -----------
000:      No clock source (Timer/Counter stopped)
001:      clkI/O/(No prescaling)
010:      clkI/O/8 (From prescaler)
011:      clkI/O/64 (From prescaler)
100:      clkI/O/256 (From prescaler)
101:      clkI/O/1024 (From prescaler)
110:      External clock source on T0 pin. Clock on falling edge
111:      External clock source on T0 pin. Clock on rising edge

If external pin modes are used for the Timer/Counter0, transitions on the T0 pin will clock the counter even if the pin is configured as an output. This feature allows software control of the counting.''',
						},
					},
				},
				'TCNT0': {
						'address': 0x46, 'module': 'TimerCounter0', 'access': 'R/W', 'default': 0,
						'description': '''Timer/Counter Register

The Timer/Counter Register gives direct access, both for read and write operations, to the Timer/Counter unit 8-bit counter. Writing to the TCNT0 Register blocks (removes) the Compare Match on the following timer clock.  Modifying the counter (TCNT0) while the counter is running, introduces a risk of missing a Compare Match between TCNT0 and the OCR0x Registers.''',
				},
				'OCR0A': {
						'address': 0x47, 'module': 'TimerCounter0', 'access': 'R/W', 'default': 0,
						'description': '''Output Compare Register A

The Output Compare Register A contains an 8-bit value that is continuously compared with the counter value (TCNT0). A match can be used to generate an Output Compare interrupt, or to generate a waveform output on the OC0A pin.''',
				},
				'OCR0B': {
						'address': 0x48, 'module': 'TimerCounter0', 'access': 'R/W', 'default': 0,
						'description': '''Output Compare Register B

The Output Compare Register B contains an 8-bit value that is continuously compared with the counter value (TCNT0). A match can be used to generate an Output Compare interrupt, or to generate a waveform output on the OC0B pin.''',
				},
				'GPIOR1': {
						'address': 0x4A, 'access': 'R/W', 'default': 0,
						'module': 'GPIO',
						'description': '''General Purpose I/O Register 1''',
				},
				'GPIOR2': {
						'address': 0x4B, 'access': 'R/W', 'default': 0,
						'module': 'GPIO',
						'description': '''General Purpose I/O Register 2''',
				},
				'SPCR': {
						'address': 0x4C, 'access': 'R/W', 'default': 0,
						'module': 'SPI',
						'description': '''SPI Control Register''',
						'bitfields': {
							'SPIE': {
								'slice': (7,),
								'description': '''SPI Interrupt Enable

This bit causes the SPI interrupt to be executed if SPIF bit in the SPSR Register is set and the if the Global Interrupt Enable bit in SREG is set.''',
							},
							'SPE': {
								'slice': (6,),
								'description': '''SPI Enable

When the SPE bit is written to one, the SPI is enabled. This bit must be set to enable any SPI operations.''',
							},
							'DORD': {
								'slice': (5,),
								'description': '''Data Order

When the DORD bit is written to one, the LSB of the data word is transmitted first. When the DORD bit is written to zero, the MSB of the data word is
transmitted first.''',
							},
							'MSTR': {
								'slice': (4,),
								'description': '''Master/Slave Select

This bit selects Master SPI mode when written to one, and Slave SPI mode when written logic zero. If /SS is configured as an input and is driven low while MSTR is set, MSTR will be cleared, and SPIF in SPSR will become set. The user will then have to set MSTR to re-enable SPI Master mode.''',
							},
							'CPOL': {
								'slice': (3,),
								'description': '''Clock Polarity

When this bit is written to one, SCK is high when idle. When CPOL is written to zero, SCK is low when idle. Refer to Figure 21-3 on page 201 and Figure 21-4 on page 201 for an example. The CPOL functionality is summarized in Table 21-3.

CPOL  Leading Edge  Trailing Edge
---   ------------  ------------
0       Rising       Falling
1       Falling      Rising
''',
							},
							'CPHA': {
								'slice': (2,),
								'description': '''Clock Phase

The settings of the Clock Phase bit (CPHA) determine if data is sampled on
the leading (first) or trailing (last) edge of SCK. Refer to Figure 21-3 on
page 201 and Figure 21-4 on page 201 for an example. The CPOL functionality
is summarized in Table 21-4.

CPHA  Leading Edge  Trailing Edge
----  ------------  -------------
0       Sample        Setup
1       Setup         Sample
''',
							},
						'SPR': {
								'slice': (1,0),
								'description': '''SPI Clock Rate Select 1 and 0

These two bits control the SCK rate of the device configured as a Master.  SPR1 and SPR0 have no effect on the Slave. The relationship between SCK and the Oscillator Clock frequency f_osc is shown in Table 21-5.

Table 21-5. Relationship Between SCK and the Oscillator Frequency

SPI2X  SPR1  SPR0  SCK Frequency
-----  ----------  -------------
0       00:        fosc/4
0       01:        fosc/16
0       10:        fosc/64
0       11:        fosc/128
1       00:        fosc/2
1       01:        fosc/8
1       10:        fosc/32
1       11:        fosc/64
''',
							},
						},
				},
				'SPSR': {
						'address': 0x4D, 'description': 'SPI Status Register',
						'module': 'SPI',
						'bitfields': {
							'SPIF': {
									'slice': (7,),
									'access': 'R',
									'default': 0,
									'description': '''SPI Interrupt Flag

When a serial transfer is complete, the SPIF Flag is set. An interrupt is generated if SPIE in SPCR is set and global interrupts are enabled.  If /SS is an input and is driven low when the SPI is in Master mode, this will also set the SPIF Flag. SPIF is cleared by hardware when executing the corresponding interrupt handling vector. Alternatively, the SPIF bit is cleared by first reading the SPI Status Register with SPIF set, then accessing the SPI Data Register (SPDR).''',
								},
							'WCOL': {
									'slice': (6,),
									'access': 'R',
									'default': 0,
									'description': '''Write COLlision Flag

The WCOL bit is set if the SPI Data Register (SPDR) is written during a data transfer. The WCOL bit (and the SPIF bit) are cleared by first reading the SPI Status Register with WCOL set, and then accessing the SPI Data Register.''',
								},
							'SPI2X': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Double SPI Speed Bit

When this bit is written logic one the SPI speed (SCK Frequency) will be doubled when the SPI is in Master mode (see Table 21-5). This means that the minimum SCK period will be two CPU clock periods.  When the SPI is configured as Slave, the SPI is only guaranteed to work at fosc/4 or lower.  The SPI interface on the ATmega640/1280/1281/2560/2561 is also used for program memory and EEPROM downloading or uploading.  See "Serial Downloading" on page 349 for serial programming and verification.''',
								},
							},
				},
			'SPDR': {
					'address': 0x4E,
					'module': 'SPI',
					'default': 0,
					'access': 'R/W',
					'description': '''SPI Data Register

The SPI Data Register is a read/write register used for data transfer between the Register File and the SPI Shift Register. Writing to the register initiates data transmission. Reading the register causes the Shift Register Receive buffer to be read.''',
				},
			'ACSR': {
					'address': 0x50,
					'module': 'Analog Comparator',
					'description': '''Analog Comparator Control and Status Register''',
					'bitfields': {
							'ACD': {
									'slice': (7,),
									'access': 'R/W',
									'default': 0,
									'description': '''Analog Comparator Disable

When this bit is written logic one, the power to the Analog Comparator is switched off. This bit can be set at any time to turn off the Analog Comparator. This will reduce power consumption in Active and Idle mode. When changing the ACD bit, the Analog Comparator Interrupt must be disabled by clearing the ACIE bit in ACSR. Otherwise an interrupt can occur when the bit is changed.''',
								},
							'ACBG': {
									'slice': (6,),
									'access': 'R/W',
									'default': 0,
									'description': '''Analog Comparator Bandgap Select

When this bit is set, a fixed bandgap reference voltage replaces the positive input to the Analog Comparator. When this bit is cleared, AIN0 is applied to the positive input of the Analog Comparator. When the bandgap reference is used as input to the Analog Comparator, it will take a certain time for the voltage to stabilize. If not stabilized, the first conversion may give a wrong value. See "Internal Voltage Reference" on page 62.''',
								},
							'ACO': {
									'slice': (5,),
									'access': 'R',
									'default': 0,
									'description': '''Analog Comparator Output

The output of the Analog Comparator is synchronized and then directly connected to ACO. The synchronization introduces a delay of 1 - 2 clock cycles.  ''',
								},
							'ACI': {
								'slice': (4,),
								'access': 'R/W',
								'default': 0,
								'description': '''Analog Comparator Interrupt Flag

This bit is set by hardware when a comparator output event triggers the interrupt mode defined by ACIS1 and ACIS0. The Analog Comparator interrupt routine is executed if the ACIE bit is set and the I-bit in SREG is set. ACI is cleared by hardware when executing the corresponding interrupt handling vector. Alternatively, ACI is cleared by writing a logic one to the flag.''',
							},
							'ACIE': {
								'slice': (3,),
								'access': 'R/W',
								'default': 0,
								'description': '''ACIE: Analog Comparator Interrupt Enable

When the ACIE bit is written logic one and the I-bit in the Status Register is set, the Analog Comparator interrupt is activated. When written logic zero, the interrupt is disabled.''',
							},
							'ACIC': {
								'slice': (2,),
								'access': 'R/W',
								'default': 0,
								'description': '''ACIC: Analog Comparator Input Capture Enable

When written logic one, this bit enables the input capture function in Timer/Counter1 to be triggered by the Analog Comparator. The comparator output is in this case directly connected to the input capture front-end logic, making the comparator utilize the noise canceler and edge select features of the Timer/Counter1 Input Capture interrupt. When written logic zero, no connection between the Analog Comparator and the input capture function exists. To make the comparator trigger the Timer/Counter1 Input Capture interrupt, the ICIE1 bit in the Timer Interrupt Mask Register (TIMSK1) must be set.''',
								},
							'ACIS': {
								'slice': (1,0),
								'access': 'R/W',
								'default': 0,
								'description': '''Analog Comparator Interrupt Mode Select

These bits determine which comparator events that trigger the Analog Comparator interrupt. The different settings are shown in Table 25-2.

ACIS<1:0>   Interrupt Mode
00: Comparator Interrupt on Output Toggle
01: Reserved
10: Comparator Interrupt on Falling Output Edge
11: Comparator Interrupt on Rising Output Edge

When changing the ACIS1/ACIS0 bits, the Analog Comparator Interrupt must be disabled by clearing its Interrupt Enable bit in the ACSR Register. Otherwise an interrupt can occur when the bits are changed.''',
							},
						},
				},
			'OCDR': {
					'address': 0x51, 'module': 'JTAG',
					'access': 'R/W', 'default': 0,
					'description': '''On-Chip Debug Register

The OCDR Register provides a communication channel from the running program in the microcontroller to the debugger.  The CPU can transfer a byte to the debugger by writing to this location. At the same time, an internal flag; I/O Debug Register Dirty - IDRD - is set to indicate to the debugger that the register has been written. When the CPU reads the OCDR Register the 7 LSB will be from the OCDR Register, while the MSB is the IDRD bit. The debugger clears the IDRD bit when it has read the information.

In some AVR devices, this register is shared with a standard I/O location. In this case, the OCDR Register can only be accessed if the OCDEN Fuse is programmed, and the debugger enables access to the OCDR Register. In all other cases, the standard I/O location is accessed.

Refer to the debugger documentation for further information on how to use this register.''',
				},
			'SMCR': {
					'address': 0x53,
					'module': 'Power Manager',
					'description': '''Sleep Mode Control Register''',
					'bitfields': {
						'SM': {
								'slice': (3,1),
								'access': 'R/W',
								'default': 0,
								'description': '''Sleep Mode Select bits

These bits select between the five available sleep modes as shown in
Table 11-2.

SM<2:0>    Sleep Mode
000:       Idle
001:       ADC Noise Reduction
010:       Power-down
011:       Power-save
100:       Reserved
101:       Reserved
110:       Standby(1)
111        Extended Standby(1)

Note: 1. Standby modes are only recommended for use with external crystals or resonators.
''',
							},
						'SE': {
								'slice': (0,),
								'description': '''Sleep Enable

The SE bit must be written to logic one to make the MCU enter the sleep mode when the SLEEP instruction is executed. To avoid the MCU entering the sleep mode unless it is the programmer's purpose, it is recommended to write the Sleep Enable (SE) bit to one just before the execution of the SLEEP instruction and to clear it immediately after waking up.''',
							},
						},
				},
			'MCUSR': {
					'address': 0x54, 'module': 'CPU',
					'description': '''MCU Status Register

The MCU Status Register provides information on which reset source caused an MCU reset.''',
					'bitfields': {
							'JTRF': {
								'slice': (4,), 'access': 'R/W',
									'description': '''JTAG Reset Flag

This bit is set if a reset is being caused by a logic one in the JTAG Reset Register selected by the JTAG instruction AVR_RESET. This bit is reset by a Power-on Reset, or by writing a logic zero to the flag.''',
								},
							'WDRF': {
								'slice': (3,), 'access': 'R/W',
									'description': '''Watchdog Reset Flag

This bit is set if a Watchdog Reset occurs. The bit is reset by a Power-on Reset, or by writing a logic zero to the flag.''',
								},
							'BORF': {
								'slice': (2,), 'access': 'R/W',
									'description': '''Brown-out Reset Flag

This bit is set if a Brown-out Reset occurs. The bit is reset by a Power-on Reset, or by writing a logic zero to the flag.''',
								},
							'EXTRF': {
								'slice': (1,), 'access': 'R/W',
									'description': '''External Reset Flag

This bit is set if an External Reset occurs. The bit is reset by a Power-on Reset, or by writing a logic zero to the flag.''',
								},
							'PORF': {
								'slice': (0,), 'access': 'R/W',
									'description': '''Power-on Reset Flag

This bit is set if a Power-on Reset occurs. The bit is reset only by writing a logic zero to the flag.

To make use of the Reset Flags to identify a reset condition, the user should read and then Reset the MCUSR as early as possible in the program. If the register is cleared before another reset occurs, the source of the reset can be found by examining the Reset Flags.''',
								},
						},
				},
			'MCUCR': {
					'address': 0x55, 'module': 'CPU',
				},
			'SPMCSR': {
					'address': 0x57, 'module': 'CPU',
				},
			'RAMPZ': {
					'address': 0x5B, 'module': 'CPU',
				},
			'EIND': {
					'address': 0x5C, 'module': 'CPU',
				},
			'SPL': {
					'address': 0x5D, 'module': 'CPU',
				},
			'SPH': {
					'address': 0x5E, 'module': 'CPU',
				},
			'SREG': {
					'address': 0x5F, 'module': 'CPU',
					'description': 'Status Register',
					'bitfields': {
							'I': {
									'slice': (7,),
									'access': 'R/W',
									'default': 0,
									'description': '''
									The Global Interrupt Enable bit must be set for the interrupts to be enabled. The individual inter- rupt enable control is then performed in separate control registers. If the Global Interrupt Enable Register is cleared, none of the interrupts are enabled independent of the individual interrupt enable settings. The I-bit is cleared by hardware after an interrupt has occurred, and is set by the RETI instruction to enable subsequent interrupts. The I-bit can also be set and cleared by the application with the SEI and CLI instructions''',
								},
							'T': {
									'slice': (6,),
									'access': 'R',
									'default': 0,
									'description': '''
									The Bit Copy instructions BLD (Bit LoaD) and BST (Bit STore) use the T-bit as source or desti- nation for the operated bit. A bit from a register in the Register File can be copied into T by the BST instruction, and a bit in T can be copied into a bit in a register in the Register File by the BLD instruction.''',
								},
							'H': {
									'slice': (5,),
									'access': 'R',
									'default': 0,
									'description': '''
									The Half Carry Flag H indicates a Half Carry in some arithmetic operations. Half Carry Is useful in BCD arithmetic.''',
								},
							'S': {
									'slice': (4,),
									'access': 'R',
									'default': 0,
									'description': '''
									The S-bit is always an exclusive or between the Negative Flag N and the Two's Complement Overflow Flag V.''',
								},
							'V': {
									'slice': (3,),
									'access': 'R',
									'default': 0,
									'description': '''
									The Two's Complement Overflow Flag V supports two's complement arithmetics.''',
								},
							'N': {
									'slice': (2,),
									'access': 'R',
									'default': 0,
									'description': '''
									The Negative Flag N indicates a negative result in an arithmetic or logic operation.''',
								},
							'Z': {
									'slice': (1,),
									'access': 'R',
									'default': 0,
									'description': '''
									The Zero Flag Z indicates a zero result in an arithmetic or logic operation.''',
								},
							'C': {
									'slice': (0,),
									'access': 'R',
									'default': 0,
									'description': '''
									The Carry Flag C indicates a carry in an arithmetic or logic operation.''',
								},


					}
				},
			'WDTCSR': {
					'address': 0x60, 'module': 'WDT',
					'description': 'Watchdog Timer Control Register',
					'bitfields': {
							'WDIF': {
									'slice': (7,),
									'access': 'R/W',
									'default': 0,
									'description': '''WDIF: Watchdog Interrupt Flag

This bit is set when a time-out occurs in the Watchdog Timer and the Watchdog Timer is config ured for interrupt. WDIF is cleared by hardware when executing the corresponding interrupt handling vector. Alternatively, WDIF is cleared by writing a logic one to the flag. When the I-bit in SREG and WDIE are set, the Watchdog Time-out Interrupt is executed.''',
								},
							'WDIE': {
								'slice': (6,),
								'description': '''Watchdog Interrupt Enable

When this bit is written to one and the I-bit in the Status Register is set, the Watchdog Interrupt is enabled. If WDE is cleared in combination with this setting, the Watchdog Timer is in Interrupt Mode, and the corresponding interrupt is executed if time-out in the Watchdog Timer occurs.

If WDE is set, the Watchdog Timer is in Interrupt and System Reset Mode. The first time-out in the Watchdog Timer will set WDIF. Executing the corresponding interrupt vector will clear WDIE and WDIF automatically by hardware (the Watchdog goes to System Reset Mode).  This is useful for keeping the Watchdog Timer security while using the interrupt. To stay in Interrupt and System Reset Mode, WDIE must be set after each interrupt. This should however not be done within the interrupt service routine itself, as this might compromise the safety-function of the Watchdog System Reset mode. If the interrupt is not executed before the next time-out, a System Reset will be applied.

Table 12-1. Watchdog Timer Configuration

WDTON(1) WDE WDIE Mode               Action on Time-out
-------- --- ---- ----               ------------------
1         0   0:  Stopped            None
1         0   1:  Interrupt Mode     Interrupt
1         1   0:  System Reset Mode  Reset
1         1   1:  Interrupt and      Interrupt, then go to System Reset Mode
                  System Reset Mode
0         x   x:  System Reset Mode  Reset

Note: 1. WDTON Fuse set to "0" means programmed and "1" means unprogrammed.
''',
							},
							'WDCE': {
								'slice': (4,),
								'description': '''Watchdog Change Enable

This bit is used in timed sequences for changing WDE and prescaler bits. To clear the WDE bit, and/or change the prescaler bits, WDCE must be set.

Once written to one, hardware will clear WDCE after four clock cycles.''',
							},
							'WDE': {
								'slice': (3, ),
								'description': '''Watchdog System Reset Enable

WDE is overridden by WDRF in MCUSR. This means that WDE is always set when WDRF is set. To clear WDE, WDRF must be cleared first. This feature ensures multiple resets during conditions causing failure, and a safe start-up after the failure.''',
							},
							'WDP3': {
								'slice': (5,),
								'description': 'Watchdog Timer Prescaler 3',
							},
							'WDP2': {
								'slice': (2,),
								'description': 'Watchdog Timer Prescaler 2',
							},
							'WDP1': {
								'slice': (1,),
								'description': 'Watchdog Timer Prescaler 1',
							},
							'WDP0': {
								'slice': (0,),
								'description': '''Watchdog Timer Prescaler 0

The WDP3:0 bits determine the Watchdog Timer prescaling when the Watchdog Timer is running. The different prescaling values and their corresponding time-out periods are shown in Table 12-2 on page 69.

WDP<3:0> Number of WDT Oscillator Cycles Typical Time-out at VCC = 5.0V
-------- ------------------------------- ------------------------------
0 0 0 0: 2K (2048) cycles                16ms
0 0 0 1: 4K (4096) cycles                32ms
0 0 1 0: 8K (8192) cycles                64ms
0 0 1 1: 16K (16384) cycles              0.125s
0 1 0 0: 32K (32768) cycles              0.25s
0 1 0 1: 64K (65536) cycles              0.5s
0 1 1 0: 128K (131072) cycles            1.0s
0 1 1 1: 256K (262144) cycles            2.0s
1 0 0 0: 512K (524288) cycles            4.0s
1 0 0 1: 1024K (1048576) cycles          8.0s
1 0 1 0: Reserved
1 0 1 1:
1 1 0 0:
1 1 0 1:
1 1 1 0:
1 1 1 1:
''',
							},
						},
				},
			'CLKPR': {
					'address': 0x61, 'module': 'CPU',
					'description': '''Clock Prescaler Register''',
					'bitfields': {
							'CLKPCE': {
									'slice': (7,),
									'access': 'R/W',
									'default': 0,
									'description': '''Clock Prescaler Change Enable

The CLKPCE bit must be written to logic one to enable change of the CLKPS bits. The CLKPCE bit is only updated when the other bits in CLKPR are simultaneously written to zero. CLKPCE is cleared by hardware four cycles after it is written or when CLKPS bits are written. Rewriting the CLKPCE bit within this time-out period does neither extend the time-out period, nor clear the CLKPCE bit.''',
								},
							'CLKPS': {
									'slice': (3,0),
									'access': 'R/W',
									'description': '''Clock Prescaler Select Bits

These bits define the division factor between the selected clock source and the internal system clock. These bits can be written run-time to vary the clock frequency to suit the application requirements. As the divider divides the master clock input to the MCU, the speed of all synchronous peripherals is reduced when a division factor is used. The division factors are given in Table 10-15 on page 51.

The CKDIV8 Fuse determines the initial value of the CLKPS bits. If CKDIV8 is unprogrammed, the CLKPS bits will be reset to "0000". If CKDIV8 is programmed, CLKPS bits are reset to "0011", giving a division factor of 8 at start up. This feature should be used if the selected clock source has a higher frequency than the maximum frequency of the device at the present operat- ing conditions. Note that any value can be written to the CLKPS bits regardless of the CKDIV8 Fuse setting. The Application software must ensure that a sufficient division factor is chosen if the selected clock source has a higher frequency than the maximum frequency of the device at the present operating conditions.  The device is shipped with the CKDIV8 Fuse programmed.

Table 10-15. Clock Prescaler Select

CLKPS<3:0> Clock Division Factor
---------- ---------------------
0 0 0 0:   1
0 0 0 1:   2
0 0 1 0:   4
0 0 1 1:   8
0 1 0 0:   16
0 1 0 1:   32
0 1 1 0:   64
0 1 1 1:   128
1 0 0 0:   256
1 0 0 1:   Reserved
1 0 1 0:   Reserved
1 0 1 1:   Reserved
1 1 0 0:   Reserved
1 1 0 1:   Reserved
1 1 1 0:   Reserved
1 1 1 1:   Reserved
''',
								},
						},
				},
			'PRR0': {
					'address': 0x64, 'module': 'Power Manager',
					'description': '''Power Reduction Register 0''',
					'bitfields': {
							'PRTWI': {
									'slice': (7,),
									'access': 'R/W',
									'default': 0,
									'description': '''Power Reduction TWI

Writing a logic one to this bit shuts down the TWI by stopping the clock to the module. When waking up the TWI again, the TWI should be re initialized to ensure proper operation.''',
								},
							'PRTIM2': {
									'slice': (6,),
									'access': 'R/W',
									'default': 0,
									'description': '''PRTIM2: Power Reduction Timer/Counter2

Writing a logic one to this bit shuts down the Timer/Counter2 module in synchronous mode (AS2 is 0). When the Timer/Counter2 is enabled, operation will continue like before the shutdown.''',
								},
							'PRTIM0': {
									'slice': (5,),
									'access': 'R/W',
									'default': 0,
									'description': '''Power Reduction Timer/Counter0

Writing a logic one to this bit shuts down the Timer/Counter0 module. When the Timer/Counter0 is enabled, operation will continue like before the shutdown.''',
								},
							'PRTIM1': {
									'slice': (3,),
									'access': 'R/W',
									'default': 0,
									'description': '''Power Reduction Timer/Counter1

Writing a logic one to this bit shuts down the Timer/Counter1 module. When the Timer/Counter1 is enabled, operation will continue like before the shutdown.''',
								},
							'PRSPI': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''Power Reduction Serial Peripheral Interface

Writing a logic one to this bit shuts down the Serial Peripheral Interface by stopping the clock to the module. When waking up the SPI again, the SPI should be re initialized to ensure proper operation.''',
								},
							'PRUSART0': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''Power Reduction USART0

Writing a logic one to this bit shuts down the USART0 by stopping the clock to the module. When waking up the USART0 again, the USART0 should be reinitialized to ensure proper operation.''',
								},
							'PRADC': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Power Reduction ADC

Writing a logic one to this bit shuts down the ADC.  The ADC must be disabled before shut down. The analog comparator cannot use the ADC input MUX when the ADC is shut down.''',
								},
						},
				},
			'PRR1': {
					'address': 0x65, 'module': 'Power Manager',
					'description': '''Power Reduction Register 1''',
					'slice': {
							'PRTIM5': {
									'slice': (5,),
									'description': '''Power Reduction Timer/Counter5

Writing a logic one to this bit shuts down the Timer/Counter5 module. When the Timer/Counter5 is enabled, operation will continue like before the shutdown.''',
								},
							'PRTIM4': {
									'slice': (4,),
									'description': '''Power Reduction Timer/Counter4

Writing a logic one to this bit shuts down the Timer/Counter4 module. When the Timer/Counter4 is enabled, operation will continue like before the shutdown.''',
								},
							'PRTIM3': {
									'slice': (3,),
									'description': '''Power Reduction Timer/Counter3

Writing a logic one to this bit shuts down the Timer/Counter3 module. When the Timer/Counter3 is enabled, operation will continue like before the shutdown.''',
								},
							'PRUSART3': {
									'slice': (2,),
									'description': '''Power Reduction USART3

Writing a logic one to this bit shuts down the USART3 by stopping the clock to the module. When waking up the USART3 again, the USART3 should be reinitialized to ensure proper operation.''',
								},
							'PRUSART2': {
									'slice': (1,),
									'description': '''Power Reduction USART2

Writing a logic one to this bit shuts down the USART2 by stopping the clock to the module. When waking up the USART2 again, the USART2 should be reinitialized to ensure proper operation.''',
								},
							'PRUSART1': {
									'slice': (0,),
									'description': '''Power Reduction USART1

Writing a logic one to this bit shuts down the USART1 by stopping the clock to the module. When waking up the USART1 again, the USART1 should be reinitialized to ensure proper operation.''',
								},
						},
				},
			'OSCCAL': {
					'address': 0x66, 'module': 'CPU', 
					'description': '''Oscillator Calibration Register

The Oscillator Calibration Register is used to trim the Calibrated Internal RC Oscillator to remove process variations from the oscillator frequency. A pre-programmed calibration value is automatically written to this register during chip reset, giving the Factory calibrated frequency as specified in Table 31-1 on page 371.  The application software can write this register to change the oscillator frequency. The oscillator can be calibrated to frequencies as specified in Table 31- 1 on page 371. Calibration outside that range is not guaranteed.

Note that this oscillator is used to time EEPROM and Flash write accesses, and these write times will be affected accordingly. If the EEPROM or Flash are written, do not calibrate to more than 8.8 MHz.  Otherwise, the EEPROM or Flash write may fail.''',
					'bitfields': {
							'CAL7': {
								'slice': (7,), 'access': 'R/W',
									'description': '''The CAL7 bit determines the range of operation for the oscillator. Setting this bit to 0 gives the lowest frequency range, setting this bit to 1 gives the highest frequency range. The two fre- quency ranges are overlapping, in other words a setting of OSCCAL = 0x7F gives a higher frequency than OSCCAL = 0x80.''',
								},
							'CAL6_0': {
								'slice': (6,0), 'access': 'R/W',
									'description': '''The CAL6..0 bits are used to tune the frequency within the selected range. A setting of 0x00 gives the lowest frequency in that range, and a setting of 0x7F gives the highest frequency in the range.''',
								},
						},
				},
			'PCICR': {
					'address': 0x68, 'module': 'CPU',
					'description': '''Pin Change Interrupt Control Register''',
					'bitfields': {
							'PCIE2': {
									'slice': (2,),
									'description': '''Pin Change Interrupt Enable 1

When the PCIE2 bit is set (one) and the I-bit in the Status Register (SREG) is set (one), pin change interrupt 2 is enabled. Any change on any enabled PCINT23:16 pin will cause an interrupt. The corresponding interrupt of Pin Change Interrupt Request is executed from the PCI2 Interrupt Vector.  PCINT23:16 pins are enabled individually by the PCMSK2 Register.''',
								},
							'PCIE1': {
									'slice': (1,),
									'description': '''Pin Change Interrupt Enable 1

When the PCIE1 bit is set (one) and the I-bit in the Status Register (SREG) is set (one), pin change interrupt 1 is enabled. Any change on any enabled PCINT15:8 pin will cause an interrupt. The corresponding interrupt of Pin Change Interrupt Request is executed from the PCI1 Interrupt Vector.  PCINT15:8 pins are enabled individually by the PCMSK1 Register.''',
								},
							'PCIE0': {
									'slice': (0,),
									'description': '''Pin Change Interrupt Enable 0

When the PCIE0 bit is set (one) and the I-bit in the Status Register (SREG) is set (one), pin change interrupt 0 is enabled. Any change on any enabled PCINT7:0 pin will cause an interrupt. The corresponding interrupt of Pin Change Interrupt Request is executed from the PCI0 Interrupt Vector.  PCINT7:0 pins are enabled individually by the PCMSK0 Register.''',
								},
						},
				},
			'EICRA': {
					'address': 0x69, 'module': 'CPU',
					'description': '''External Interrupt Control Register A

The External Interrupts 3 - 0 are activated by the external pins INT3:0 if the SREG I-flag and the corresponding interrupt mask in the EIMSK is set. The level and edges on the external pins that activate the interrupts are defined in Table 15-1 on page 114. Edges on INT3:0 are registered asynchronously. Pulses on INT3:0 pins wider than the minimum pulse width given in Table 15-2 on page 114 will generate an interrupt. Shorter pulses are not guaranteed to generate an interrupt. If low level interrupt is selected, the low level must be held until the completion of the currently executing instruction to generate an interrupt. If enabled, a level triggered interrupt will generate an interrupt request as long as the pin is held low. When changing the ISCn bit, an interrupt can occur. Therefore, it is recommended to first disable INTn by clearing its Interrupt Enable bit in the EIMSK Register. Then, the ISCn bit can be changed. Finally, the INTn interrupt flag should be cleared by writing a logical one to its Interrupt Flag bit (INTFn) in the EIFR Register before the interrupt is re-enabled.

Table 15-1. Interrupt Sense Control(1)

ISCn1 ISCn0 Description
----- ----- -----------
0     0     The low level of INTn generates an interrupt request
0     1     Any edge of INTn generates asynchronously an interrupt request
1     0     The falling edge of INTn generates asynchronously an interrupt request
1     1     The rising edge of INTn generates asynchronously an interrupt request

Note: 1. n = 3, 2, 1 or 0.
When changing the ISCn1/ISCn0 bits, the interrupt must be disabled by clearing its Interrupt Enable bit in the EIMSK Register. Otherwise an interrupt can occur when the bits are changed.

Table 15-2. Asynchronous External Interrupt Characteristics

Symbol Parameter                                               Condition Min Typ Max Units
------ ---------                                               --------- --- --- --- -----
tINT   Minimum pulse width for asynchronous external interrupt            50         ns
''',

					'bitfields': {
							'ISC31': {
									'slice': (7,), 'access': 'R/W',
								},
							'ISC30': {
									'slice': (6,), 'access': 'R/W',
								},
							'ISC3': {
									'slice': (7,6), 'access': 'R/W',
									'description': '''External Interrupt 3 Sense Control Bits

00: The low level of INT3 generates an interrupt request
01: Any edge of INT3 generates asynchronously an interrupt request
10: The falling edge of INT3 generates asynchronously an interrupt request
11: The rising edge of INT3 generates asynchronously an interrupt request
''',
								},

							'ISC21': {
									'slice': (5,), 'access': 'R/W',
								},
							'ISC20': {
									'slice': (4,), 'access': 'R/W',
								},
							'ISC2': {
									'slice': (5,4), 'access': 'R/W',
									'description': '''External Interrupt 2 Sense Control Bits

00: The low level of INT2 generates an interrupt request
01: Any edge of INT2 generates asynchronously an interrupt request
10: The falling edge of INT2 generates asynchronously an interrupt request
11: The rising edge of INT2 generates asynchronously an interrupt request
''',
								},

							'ISC11': {
									'slice': (3,), 'access': 'R/W',
								},
							'ISC10': {
									'slice': (2,), 'access': 'R/W',
								},
							'ISC1': {
									'slice': (3,2), 'access': 'R/W',
									'description': '''External Interrupt 1 Sense Control Bits

00: The low level of INT1 generates an interrupt request
01: Any edge of INT1 generates asynchronously an interrupt request
10: The falling edge of INT1 generates asynchronously an interrupt request
11: The rising edge of INT1 generates asynchronously an interrupt request
''',
								},
							'ISC01': {
									'slice': (1,), 'access': 'R/W',
								},
							'ISC00': {
									'slice': (0,), 'access': 'R/W',
								},
							'ISC0': {
									'slice': (1,0), 'access': 'R/W',
									'description': '''External Interrupt 0 Sense Control Bits

00: The low level of INT0 generates an interrupt request
01: Any edge of INT0 generates asynchronously an interrupt request
10: The falling edge of INT0 generates asynchronously an interrupt request
11: The rising edge of INT0 generates asynchronously an interrupt request
''',
								},
						},
				},
			'EICRB': {
					'address': 0x6A, 'module': 'CPU',
					'description': '''External Interrupt Control Register B''',
					'bitfields': {
							'ISC7': {
								'slice': (7, 6), 'access': 'R/W',
									'description': '''External Interrupt 7 Sense Control Bits

The External Interrupt 7 is activated by the external pin INT7 if the SREG I-flag and the corresponding interrupt mask in the EIMSK is set.  The level and edges on the external pins that activate the interrupts are defined in Table 15-3. The value on the INT7 pin is sampled before detecting edges. If edge or toggle interrupt is selected, pulses that last longer than one clock period will generate an interrupt. Shorter pulses are not guaranteed to generate an interrupt. Observe that CPU clock frequency can be lower than the XTAL frequency if the XTAL divider is enabled. If low level interrupt is selected, the low level must be held until the completion of the currently executing instruction to generate an interrupt. If enabled, a level triggered interrupt will generate an interrupt request as long as the pin is held low.

00: The low level of INT7 generates an interrupt request
01: Any logical change on INT7 generates an interrupt request
10: The falling edge between two samples of INT7 generates an interrupt request
11: The rising edge between two samples of INT7 generates an interrupt request

Note: When changing the ISC7 bits, the interrupt must be disabled by clearing its Interrupt Enable bit in the EIMSK Register.  Otherwise an interrupt can occur when the bits are changed.''',
								},
							'ISC6': {
								'slice': (5, 4), 'access': 'R/W',
									'description': '''External Interrupt 6 Sense Control Bits

00: The low level of INT6 generates an interrupt request
01: Any logical change on INT6 generates an interrupt request
10: The falling edge between two samples of INT6 generates an interrupt request
11: The rising edge between two samples of INT6 generates an interrupt request

Note: When changing the ISC6 bits, the interrupt must be disabled by clearing its Interrupt Enable bit in the EIMSK Register.  Otherwise an interrupt can occur when the bits are changed.''',
								},
							'ISC5': {
								'slice': (3, 2), 'access': 'R/W',
									'description': '''External Interrupt 5 Sense Control Bits

00: The low level of INT5 generates an interrupt request
01: Any logical change on INT5 generates an interrupt request
10: The falling edge between two samples of INT5 generates an interrupt request
11: The rising edge between two samples of INT5 generates an interrupt request

Note: When changing the ISC5 bits, the interrupt must be disabled by clearing its Interrupt Enable bit in the EIMSK Register.  Otherwise an interrupt can occur when the bits are changed.''',
								},
							'ISC4': {
								'slice': (1, 0), 'access': 'R/W',
									'description': '''External Interrupt 4 Sense Control Bits

00: The low level of INT4 generates an interrupt request
01: Any logical change on INT4 generates an interrupt request
10: The falling edge between two samples of INT4 generates an interrupt request
11: The rising edge between two samples of INT4 generates an interrupt request

Note: When changing the ISC4 bits, the interrupt must be disabled by clearing its Interrupt Enable bit in the EIMSK Register.  Otherwise an interrupt can occur when the bits are changed.''',
								},
						},
				},
			'PCMSK0': {
					'address': 0x6B, 'module': 'CPU',
					'description': '''Pin Change Mask Register 0

Each PCINT7:0 bit selects whether pin change interrupt is enabled on the corresponding I/O pin. If PCINT7:0 is set and the PCIE0 bit in PCICR is set, pin change interrupt is enabled on the corresponding I/O pin. If PCINT7:0 is cleared, pin change interrupt on the corresponding I/O pin is disabled.''',
					'bitfields': {
						'PCINT7': {
							'slice': (7,), 'access': 'R/W', 'default': 0,
						},
						'PCINT6': {
							'slice': (6,), 'access': 'R/W', 'default': 0,
						},
						'PCINT5': {
							'slice': (5,), 'access': 'R/W', 'default': 0,
						},
						'PCINT4': {
							'slice': (4,), 'access': 'R/W', 'default': 0,
						},
						'PCINT3': {
							'slice': (3,), 'access': 'R/W', 'default': 0,
						},
						'PCINT2': {
							'slice': (2,), 'access': 'R/W', 'default': 0,
						},
						'PCINT1': {
							'slice': (1,), 'access': 'R/W', 'default': 0,
						},
						'PCINT0': {
							'slice': (0,), 'access': 'R/W', 'default': 0,
						},
					},
				},
			'PCMSK1': {
					'address': 0x6C, 'module': 'CPU',
					'description': '''Pin Change Mask Register 1

Pin Change Enable Mask 15:8
Each PCINT15:8-bit selects whether pin change interrupt is enabled on the corresponding I/O pin. If PCINT15:8 is set and the PCIE1 bit in EIMSK is set, pin change interrupt is enabled on the corresponding I/O pin. If PCINT15:8 is cleared, pin change interrupt on the corresponding I/O pin is disabled.  ''',
					'bitfields': {
							'PCINT15': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'PCINT14': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'PCINT13': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
								},
							'PCINT12': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'PCINT11': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'PCINT10': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'PCINT9': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'PCINT8': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'PCMSK2': {
					'address': 0x6D, 'module': 'CPU',
					'description': '''Pin Change Mask Register 2

Bit 7:0 - PCINT23:16: Pin Change Enable Mask 23:16

Each PCINT23:16-bit selects whether pin change interrupt is enabled on the corresponding I/O pin. If PCINT23:16 is set and the PCIE2 bit in PCICR is set, pin change interrupt is enabled on the corresponding I/O pin. If PCINT23:16 is cleared, pin change interrupt on the corresponding I/O pin is disabled.''',
					'bitfields': {
							'PCINT23': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'PCINT22': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'PCINT21': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
								},
							'PCINT20': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'PCINT19': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'PCINT18': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'PCINT17': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'PCINT16': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'TIMSK0': {
					'address': 0x6E, 'module': 'TimerCounter0',
					'description': '''Timer/Counter Interrupt Mask Register''',
					'bitfields': {
							'OCIE0B': {
								'slice': (2,),
								'description': '''Timer/Counter Output Compare Match B Interrupt Enable

When the OCIE0B bit is written to one, and the I-bit in the Status Register is set, the Timer/Counter Compare Match B interrupt is enabled. The corresponding interrupt is executed if a Compare Match in Timer/Counter occurs, that is, when the OCF0B bit is set in the Timer/Counter Interrupt Flag Register - TIFR0.''',
							},
							'OCIE0A': {
								'slice': (1,),
								'description': '''Timer/Counter0 Output Compare Match A Interrupt Enable

When the OCIE0A bit is written to one, and the I-bit in the Status Register is set, the Timer/Counter0 Compare Match A interrupt is enabled. The corresponding interrupt is executed if a Compare Match in Timer/Counter0 occurs, that is, when the OCF0A bit is set in the Timer/Counter 0 Interrupt Flag Register - TIFR0.''',
							},
							'TOIE0': {
								'slice': (0,),
								'description': '''Timer/Counter0 Overflow Interrupt Enable

When the TOIE0 bit is written to one, and the I-bit in the Status Register is set, the Timer/Counter0 Overflow interrupt is enabled. The corresponding interrupt is executed if an overflow in Timer/Counter0 occurs, that is, when the TOV0 bit is set in the Timer/Counter 0 Interrupt Flag Register - TIFR0.''',
						},
				},
			},
			'TIMSK1': {
					'address': 0x6F, 'module': 'TimerCounter1',
					'description': '''Timer/Counter 1 Interrupt Mask Register''',
					'bitfields': {
							'ICIE1': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter1, Input Capture Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter1 Input Capture interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the ICF1 Flag, located in TIFR1, is set.''',
								},
							'OCIE1C': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter1, Output Compare C Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter1 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF1C Flag, located in TIFR1, is set.''',
								},
							'OCIE1B': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter1, Output Compare B Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter1 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF1B Flag, located in TIFR1, is set.''',
								},
							'OCIE1A': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter1, Output Compare A Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter1 Output Compare A Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF1A Flag, located in TIFR1, is set.''',
								},
							'TOIE1': {
									'slice': (0,),
									'description': '''Timer/Counter1, Overflow Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter1 Overflow interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the TOV1 Flag, located in TIFR1, is set.''',
								},
						},
				},
			'TIMSK2': {
					'address': 0x70, 'module': 'TimerCounter2',
					'description': '''Timer/Counter2 Interrupt Mask Register''',
					'bitfields': {
							'OCIE2B': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': '''OCIE2B: Timer/Counter2 Output Compare Match B Interrupt Enable

When the OCIE2B bit is written to one and the I-bit in the Status Register is set (one), the Timer/Counter2 Compare Match B interrupt is enabled.  The corresponding interrupt is executed if a compare match in Timer/Counter2 occurs, that is, when the OCF2B bit is set in the Timer/Counter 2 Interrupt Flag Register - TIFR2.''',
								},
							'OCIE2A': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description':  '''OCIE2A: Timer/Counter2 Output Compare Match A Interrupt Enable

When the OCIE2A bit is written to one and the I-bit in the Status Register is set (one), the Timer/Counter2 Compare Match A interrupt is enabled.  The corresponding interrupt is executed if a compare match in Timer/Counter2 occurs, that is, when the OCF2A bit is set in the Timer/Counter 2 Interrupt Flag Register - TIFR2.''',
								},
							'TOIE2': {
									'slice': (0,),
									'description': '''When the TOIE2 bit is written to one and the I-bit in the Status Register is set (one), the Timer/Counter2 Overflow interrupt is enabled. The corresponding interrupt is executed if an overflow in Timer/Counter2 occurs, that is, when the TOV2 bit is set in the Timer/Counter2 Interrupt Flag Register - TIFR2.''',
								},
						},
				},
			'TIMSK3': {
					'address': 0x71, 'module': 'TimerCounter3',
					'description': '''Timer/Counter 3 Interrupt Mask Register''',
					'bitfields': {
							'ICIE3': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter3, Input Capture Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter3 Input Capture interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the ICF3 Flag, located in TIFR3, is set.''',
								},
							'OCIE3C': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter3, Output Compare C Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter3 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF3C Flag, located in TIFR3, is set.''',
								},
							'OCIE3B': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter3, Output Compare B Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter3 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF3B Flag, located in TIFR3, is set.''',
								},
							'OCIE3A': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter3, Output Compare A Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter3 Output Compare A Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF3A Flag, located in TIFR3, is set.''',
								},
							'TOIE3': {
									'slice': (0,),
									'description': '''Timer/Counter3, Overflow Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter3 Overflow interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the TOV3 Flag, located in TIFR3, is set.''',
								},
						},
				},
			'TIMSK4': {
					'address': 0x72, 'module': 'TimerCounter4',
					'description': '''Timer/Counter 4 Interrupt Mask Register''',
					'bitfields': {
							'ICIE4': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter4, Input Capture Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter4 Input Capture interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the ICF4 Flag, located in TIFR4, is set.''',
								},
							'OCIE4C': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter4, Output Compare C Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter4 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF4C Flag, located in TIFR4, is set.''',
								},
							'OCIE4B': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter4, Output Compare B Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter4 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF4B Flag, located in TIFR4, is set.''',
								},
							'OCIE4A': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter4, Output Compare A Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter4 Output Compare A Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF4A Flag, located in TIFR4, is set.''',
								},
							'TOIE4': {
									'slice': (0,),
									'description': '''Timer/Counter4, Overflow Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter4 Overflow interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the TOV4 Flag, located in TIFR4, is set.''',
								},
						},
				},
			'TIMSK5': {
					'address': 0x73, 'module': 'TimerCounter5',
					'description': '''Timer/Counter 5 Interrupt Mask Register''',
					'bitfields': {
							'ICIE5': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter5, Input Capture Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter5 Input Capture interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the ICF5 Flag, located in TIFR5, is set.''',
								},
							'OCIE5C': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter5, Output Compare C Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter5 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF5C Flag, located in TIFR5, is set.''',
								},
							'OCIE5B': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter5, Output Compare B Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter5 Output Compare C Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF5B Flag, located in TIFR5, is set.''',
								},
							'OCIE5A': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
									'description': '''Timer/Counter5, Output Compare A Match Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter5 Output Compare A Match interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the OCF5A Flag, located in TIFR5, is set.''',
								},
							'TOIE5': {
									'slice': (0,),
									'description': '''Timer/Counter5, Overflow Interrupt Enable

When this bit is written to one, and the I-flag in the Status Register is set (interrupts globally enabled), the Timer/Counter5 Overflow interrupt is enabled. The corresponding Interrupt Vector (see "Interrupts" on page 105) is executed when the TOV5 Flag, located in TIFR5, is set.''',
								},
						},
				},
			'XMCRA': {
					'address': 0x74, 'module': 'CPU',
					'description': '''External Memory Control Register A''',
					'bitfields': {
							'SRE': {
									'slice': (7,),
									'description': '''External SRAM/XMEM Enable

Writing SRE to one enables the External Memory Interface. The pin functions AD7:0, A15:8, ALE, /WR, and /RD are activated as the alternate pin functions.  The SRE bit overrides any pin direction settings in the respective data direction registers. Writing SRE to zero, disables the External Memory Interface and the normal pin and data direction settings are used.''',
								},
							'SRL': {
									'slice': (6,4),
									'description': '''Wait-state Sector Limit

It is possible to configure different wait-states for different External Memory addresses. The external memory address space can be divided in two sectors that have separate wait-state bits. The SRL<2:0> bits select the split of the sectors, see Table 9-2 on page 38 and Figure 9-1 on page 28. By default, the SRL<2:0> bits are set to zero and the entire external memory address space is treated as one sector. When the entire SRAM address space is
configured as one sector, the wait-states are configured by the SRW11
and SRW10 bits.

SRL<2:0>  Sector Limits
--------  -------------
00x:      Lower sector = N/A,             Upper sector = 0x2200 - 0xFFFF
010:      Lower sector = 0x2200 - 0x3FFF, Upper sector = 0x4000 - 0xFFFF
011:      Lower sector = 0x2200 - 0x5FFF, Upper sector = 0x6000 - 0xFFFF
100:      Lower sector = 0x2200 - 0x7FFF, Upper sector = 0x8000 - 0xFFFF
101:      Lower sector = 0x2200 - 0x9FFF, Upper sector = 0xA000 - 0xFFFF
110:      Lower sector = 0x2200 - 0xBFFF, Upper sector = 0xC000 - 0xFFFF
111:      Lower sector = 0x2200 - 0xDFFF, Upper sector = 0xE000 - 0xFFFF
''',
								},
						},
				},
			'XMCRB': {
					'address': 0x75, 'module': 'CPU',
					'description': '''External Memory Control Register B''',
					'bitfields': {
							'XMBK': {
									'slice': (7,),
									'description': '''External Memory Bus-keeper Enable

Writing XMBK to one enables the bus keeper on the AD7:0 lines. When the bus keeper is enabled, AD7:0 will keep the last driven value on the lines even if the XMEM interface has tristated the lines.  Writing XMBK to zero disables the bus keeper. XMBK is not qualified with SRE, so even if the XMEM interface is disabled, the bus keepers are still activated as long as XMBK is one.''',
									'default': 0,
									'access': 'R/W',
								},
							'XMM': {
									'slice': (2,0),
									'description': '''External Memory High Mask

When the External Memory is enabled, all Port C pins are default used for the high address byte. If the full 60Kbytes address space is not required to access the External Memory, some, or all, Port C pins can be released for normal Port Pin function as described in Table 9-4. As described in "Using all 64Kbytes Locations of External Memory" on page 33, it is possible to use the XMMn bits to access all 64Kbytes locations of the External Memory.

Table 9-4. Port C Pins Released as Normal Port Pins when the External Memory is Enabled

XMM<2:0> # Bits for External Memory Address Released Port Pins
-------- ---------------------------------- ------------------
0 0 0    8 (Full 56Kbytes space)            None
0 0 1    7                                  PC7
0 1 0    6                                  PC7 - PC6
0 1 1    5                                  PC7 - PC5
1 0 0    4                                  PC7 - PC4
1 0 1    3                                  PC7 - PC3
1 1 0    2                                  PC7 - PC2
1 1 1    No Address high bits               Full Port C''',
								},
						},
				},
			'ADCL': {
					'address': 0x78, 'module': 'ADC',
					'access': 'R', 'default': 0,
					'description': '''ADC Data Register Low Byte

When an ADC conversion is complete, the result is found in ADCL and ADCH registers. If differential channels are used, the result is presented in two's complement form.

When ADCL is read, the ADC Data Register is not updated until ADCH is read. Consequently, if the result is left adjusted and no more than 8-bit precision (7 bit + sign bit for differential input channels) is required, it is sufficient to read ADCH. Otherwise, ADCL must be read first, then ADCH.

The ADLAR bit in ADMUX, and the MUXn bits in ADMUX affect the way the result is read from the registers. If ADLAR is set, the result is left adjusted. If ADLAR is cleared (default), the result is right adjusted.  

That is, if ADLAR = 0 then it contains ADC bits 7:0.
If ADLAR = 1 then it contains ADC bits 1:0 in its most-significant positions.
''',
					'bitfields': {
							'ADC1': {
									'slice': (7,),
									'description': '''data bit 1 if ADLAR = 1''',
								},
							'ADC0': {
									'slice': (6,),
									'description': '''data bit 0 if ADLAR = 1''',
								},
						},
				},
			'ADCH': {
					'address': 0x79, 'module': 'ADC', 'description': '''ADC Data Register High Byte

If ADLAR = 0 then ADCH contains data bits 9:8 in its least significant positions.
If ADLAR = 1 then ADCH contains data bits 9:2.
''',
					'bitfields': {
							'ADC9': {
									'slice': (1,),
									'access': 'R',
									'description': '''data bit 9 if ADLAR = 0'''
								},
							'ADC8': {
									'slice': (0,),
									'access': 'R',
									'description': '''data bit 8 if ADLAR = 0'''
								},
							'ADC98': {
									'slice': (1,0),
									'access': 'R',
									'description': '''data bits 9:8 if ADLAR = 0'''
								},
						},
				},
			'ADCSRA': {
					'address': 0x7A, 'module': 'ADC',
					'description': '''ADC Control and Status Register A''',
					'access': 'R/W', 'default': 0,
					'bitfields': {
							'ADEN': {
									'slice': (7,),
									'description': '''ADC Enable

Writing this bit to one enables the ADC. By writing it to zero, the ADC is turned off. Turning the ADC off while a conversion is in progress, will terminate this conversion.'''
								},
							'ADSC': {
									'slice': (6,),
									'description': '''ADC Start Conversion

In Single Conversion mode, write this bit to one to start each conversion. In Free Running mode, write this bit to one to start the first conversion. The first conversion after ADSC has been written after the ADC has been enabled, or if ADSC is written at the same time as the ADC is enabled, will take 25 ADC clock cycles instead of the normal 13. This first conversion performs initialization of the ADC.

ADSC will read as one as long as a conversion is in progress. When the conversion is complete, it returns to zero. Writing zero to this bit has no effect.''',
								},
							'ADATE': {
									'slice': (5,),
									'description': '''ADC Auto Trigger Enable

When this bit is written to one, Auto Triggering of the ADC is enabled. The ADC will start a conversion on a positive edge of the selected trigger signal. The trigger source is selected by setting the ADC Trigger Select bits, ADTS in ADCSRB.''',
								},
							'ADIF': {
									'slice': (4,),
									'description': '''ADC Interrupt Flag

This bit is set when an ADC conversion completes and the Data Registers are updated. The ADC Conversion Complete Interrupt is executed if the ADIE bit and the I-bit in SREG are set. ADIF is cleared by hardware when executing the corresponding interrupt handling vector. Alternatively, ADIF is cleared by writing a logical one to the flag. Beware that if doing a Read-Modify- Write on ADCSRA, a pending interrupt can be disabled. This also applies if the SBI and CBI instructions are used. ''',
								},
							'ADIE': {
									'slice': (3,),
									'description': '''ADC Interrupt Enable

When this bit is written to one and the I-bit in SREG is set, the ADC
Conversion Complete Interrupt is activated.  
''',
								},
							'ADPS': {
									'slice': (2,0),
									'description': '''ADC Prescaler Select Bits

These bits determine the division factor between the XTAL frequency and the input clock to the ADC.

Bits  Division Factor
----  ---------------
000:  2
001:  2
010:  4
011:  8
100:  16
101:  32
110:  64
111:  128
'''
								},
						},
				},
			'ADCSRB': {
					'address': 0x7B, 'module': 'ADC',
					'description': '''ADC Control and Status Register B''',
					'bitfields': {
							'ACME': {
									'slice': (6,),
								},
							'MUX5': {
									'slice': (3,),
									'description': '''Analog Channel and Gain Selection Bit

This bit is used together with MUX4:0 in ADMUX to select which
combination in of analog inputs are connected to the ADC. See Table
26-4 for details. If this bit is changed during a conversion, the
change will not go in effect until this conversion is complete.
This bit is not valid for ATmega1281/2561.

Table 26-4. Input Channel Selections

MUX<5:0> Single Ended Inp Pos. Diff. Inp Neg Diff Input  Gain
-------- ---------------- -------------- --------------  ----
000000   ADC0              N/A            N/A            N/A
000001   ADC1              N/A            N/A            N/A
000010   ADC2              N/A            N/A            N/A
000011   ADC3              N/A            N/A            N/A
000100   ADC4              N/A            N/A            N/A
000101   ADC5              N/A            N/A            N/A
000110   ADC6              N/A            N/A            N/A
000111   ADC7              N/A            N/A            N/A
001000   N/A               ADC0           ADC0           10x
001001   N/A               ADC1           ADC0           10x
001010   N/A               ADC0           ADC0           200x
001011   N/A               ADC1           ADC0           200x
001100   N/A               ADC2           ADC2           10x
001101   N/A               ADC3           ADC2           10x
001110   N/A               ADC2           ADC2           200x
001111   N/A               ADC3           ADC2           200x
010000   N/A               ADC0           ADC1           1x
010001   N/A               ADC1           ADC1           1x
010010   N/A               ADC2           ADC1           1x
010011   N/A               ADC3           ADC1           1x
010100   N/A               ADC4           ADC1           1x
010101   N/A               ADC5           ADC1           1x
010110   N/A               ADC6           ADC1           1x
010111   N/A               ADC7           ADC1           1x
011000   N/A               ADC0           ADC2           1x
011001   N/A               ADC1           ADC2           1x
011010   N/A               ADC2           ADC2           1x
011011   N/A               ADC3           ADC2           1x
011100   N/A               ADC4           ADC2           1x
011101   N/A               ADC5           ADC2           1x
011110   1.1V (V_BG)       N/A            N/A            N/A
011110   0V (GND)          N/A            N/A            N/A
100000   ADC8              N/A            N/A            N/A
100001   ADC9              N/A            N/A            N/A
100010   ADC10             N/A            N/A            N/A
100011   ADC11             N/A            N/A            N/A
100100   ADC12             N/A            N/A            N/A
100101   ADC13             N/A            N/A            N/A
100110   ADC14             N/A            N/A            N/A
100111   ADC15             N/A            N/A            N/A
101000   N/A               ADC8           ADC8           10x
101000   N/A               ADC9           ADC8           10x
101000   N/A               ADC8           ADC8           200x
101000   N/A               ADC9           ADC8           200x
101000   N/A               ADC10          ADC10          10x
101000   N/A               ADC11          ADC10          10x
101000   N/A               ADC10          ADC10          200x
101000   N/A               ADC11          ADC10          200x
110000   N/A               ADC8           ADC9           1x
110001   N/A               ADC9           ADC9           1x
110010   N/A               ADC10          ADC9           1x
110011   N/A               ADC11          ADC9           1x
110100   N/A               ADC12          ADC9           1x
110101   N/A               ADC13          ADC9           1x
110110   N/A               ADC14          ADC9           1x
110111   N/A               ADC15          ADC9           1x
111000   N/A               ADC8           ADC10          1x
111001   N/A               ADC9           ADC10          1x
111010   N/A               ADC10          ADC10          1x
111011   N/A               ADC11          ADC10          1x
111100   N/A               ADC12          ADC10          1x
111101   N/A               ADC13          ADC10          1x
111110   Reserved          N/A            N/A            N/A
111111   Reserved          N/A            N/A            N/A

Note: 1. To reach the given accuracy, 10x or 200x Gain should not be used for operating voltage below 2.7V.
''',
								},
							'ADTS': {
									'slice': (2,0),
									'description': '''ADC Auto Trigger Source

If ADATE in ADCSRA is written to one, the value of these bits selects
which source will trigger an ADC conversion. If ADATE is cleared, the
ADTS2:0 settings will have no effect. A conversion will be triggered
by the rising edge of the selected interrupt flag. Note that switching
from a trigger source that is cleared to a trigger source that is set,
will generate a positive edge on the trigger signal. If ADEN in ADCSRA
is set, this will start a new conversion. Switching to Free Running
mode (ADTS[2:0]=0) will not cause a trigger event, even if the ADC
Interrupt Flag is set.

Table 26-6. ADC Auto Trigger source selections.

ADTS    Trigger Source
----    --------------
000     Free Running mode
001     Analog comparator
010     External Interrupt Request 0
011     Timer/Counter0 Compare Match A
100     Timer/Counter0 Overflow
101     Timer/Counter1 Compare Match B
110     Timer/Counter1 Overflow
111     Timer/Counter1 Capture Event

Note: Free running mode cannot be used for differential channels (see chapter "Differential Channels" on page 281).
''',
								},
						},
				},
			'ADMUX': {
					'address': 0x7C, 'module': 'ADC',
					'description': '''ADC Multiplexer Selection Register''',
					'bitfields': {
							'REFS': {
									'slice': (7,6),
									'description': '''Reference Selection Bits

These bits select the voltage reference for the ADC, as shown in Table 26-3. If these bits are changed during a conversion, the change will not go in effect until this conversion is complete (ADIF in ADCSRA is set). The internal voltage reference options may not be used if an external reference voltage is being applied to the AREF pin.

Table 26-3. Voltage Reference Selections for ADC

REFS<1:0>   Voltage Reference Selection(1)
---------   ------------------------------
00:         AREF, Internal VREF turned off
01:         AVCC with external capacitor at AREF pin
10:         Internal 1.1V Voltage Reference with external capacitor at AREF pin
11:         Internal 2.56V Voltage Reference with external capacitor at AREF pin

Note: 1. If 10x or 200x gain is selected, only 2.56V should be used as Internal Voltage Reference. For differential conversion, only 1.1V cannot be used as internal voltage reference.
''',
								},
							'ADLAR': {
									'slice': (5,),
									'description': '''ADC Left Adjust Result

The ADLAR bit affects the presentation of the ADC conversion result in the ADC Data Register. Write one to ADLAR to left adjust the result. Otherwise, the result is right adjusted. Changing the ADLAR bit will affect the ADC Data Register immediately, regardless of any ongoing conver- sions. For a complete description of this bit, see "ADCL and ADCH - The ADC Data Register" on page 294.''',
								},
							'MUX': {
									'slice': (4,0),
									'description': '''Analog Channel and Gain Selection Bits

The value of these bits selects which combination of analog inputs are connected to the ADC. See Table 26-4 for details. If these bits are changed during a conversion, the change will not go in effect until this conversion is complete (ADIF in ADCSRA is set).''',
								},
							'MUX4': { 'slice': (4,), },
							'MUX3': { 'slice': (3,), },
							'MUX2': { 'slice': (2,), },
							'MUX1': { 'slice': (1,), },
							'MUX0': { 'slice': (0,), },
						},
				},
			'DIDR2': {
					'address': 0x7D, 'module': 'GPIO',
					'description': '''Digital Input Disable Register 2''',
					'bitfields': {
						'ADC15D_ADC8D': {
							'slice': (7,0),
							'description': '''ADC15:8 Digital Input Disable

When this bit is written logic one, the digital input buffer on the corresponding ADC pin is disabled. The corresponding PIN Register bit will always read as zero when this bit is set. When an analog signal is applied to the ADC15:8 pin and the digital input from this pin is not needed, this bit should be written logic one to reduce power consumption in the digital input buffer.''',
						},
					},
				},
			'DIDR0': {
					'address': 0x7E, 'module': 'GPIO',
					'description': '''Digital Input Disable Register 0''',
					'bitfields': {
							'ADC7D_ADC0D': {
									'slice': (7,0),
									'description': '''ADC7:0 Digital Input Disable

When this bit is written logic one, the digital input buffer on the corresponding ADC pin is disabled. The corresponding PIN Register bit will always read as zero when this bit is set. When an analog signal is applied to the ADC7:0 pin and the digital input from this pin is not needed, this bit should be written logic one to reduce power consumption in the digital input buffer.''',
								},
						},
				},
			'DIDR1': {
					'address': 0x7F, 'module': 'GPIO',
					'description': '''Digital Input Disable Register 1''',
					'bitfields': {
							'AIN1D': {
									'slice': (1,),
									'description': '''AIN1 Digital Input Disable
									
When this bit is written logic one, the digital input buffer on the AIN1 pin is disabled. The corresponding PIN Register bit will always read as zero when this bit is set. When an analog signal is applied to the AIN1 pin and the digital input from this pin is not needed, this bit should be written logic one to reduce power consumption in the digital input buffer.''',
								},
							'AIN0D': {
									'slice': (0,),
									'description': '''AIN0 Digital Input Disable
									
When this bit is written logic one, the digital input buffer on the AIN0 pin is disabled. The corresponding PIN Register bit will always read as zero when this bit is set. When an analog signal is applied to the AIN0 pin and the digital input from this pin is not needed, this bit should be written logic one to reduce power consumption in the digital input buffer.''',
								},
						},
				},
			'TCCR1A': {
					'address': 0x80, 'module': 'TimerCounter1',
					'description': '''Timer/Counter 1 Control Register A''',
					'bitfields': {
							'COM1A1': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'COM1A0': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'COM1B1': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
								},
							'COM1B0': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'COM1C1': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'COM1C0': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'WGM11': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'WGM10': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'TCCR1B': {
					'address': 0x81, 'module': 'TimerCounter1',
					'description': '''Timer/Counter 1 Control Register B''',
					'bitfields': {
							'ICNC1': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'ICES1': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'WGM13': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'WGM12': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'CS12': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'CS11': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'CS10': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'TCCR1C': {
					'address': 0x82, 'module': 'TimerCounter1',
					'description': '''Timer/Counter 1 Control Register C''',
					'bitfields': {
							'FOC1A': {
									'slice': (7,), 'access': 'W', 'default': 0,
								},
							'FOC1B': {
									'slice': (6,), 'access': 'W', 'default': 0,
								},
							'FOC1C': {
									'slice': (5,), 'access': 'W', 'default': 0,
								},
						},
				},
			'TCNT1L': {
					'address': 0x84, 'module': 'TimerCounter1',
					'description': 'Timer/Counter 1 low byte',
				},
			'TCNT1H': {
					'address': 0x85, 'module': 'TimerCounter1',
					'description': 'Timer/Counter 1 high byte',
				},
			'ICR1L': {
					'address': 0x86, 'module': 'TimerCounter1',
					'description': 'Input Capture Register 1 low byte',
				},
			'ICR1H': {
					'address': 0x87, 'module': 'TimerCounter1',
					'description': 'Input Capture Register 1 high byte',
				},
			'OCR1AL': {
					'address': 0x88, 'module': 'TimerCounter1',
					'description': 'Output Compare Register 1A low byte',
				},
			'OCR1AH': {
					'address': 0x89, 'module': 'TimerCounter1',
					'description': 'Output Compare Register 1A high byte',
				},
			'OCR1BL': {
					'address': 0x8A, 'module': 'TimerCounter1',
					'description': 'Output Compare Register 1B low byte',
				},
			'OCR1BH': {
					'address': 0x8B, 'module': 'TimerCounter1',
					'description': 'Output Compare Register 1B high byte',
				},
			'OCR1CL': {
					'address': 0x8C, 'module': 'TimerCounter1',
					'description': 'Output Compare Register 1C low byte',
				},
			'OCR1CH': {
					'address': 0x8D, 'module': 'TimerCounter1',
					'description': 'Output Compare Register 1C high byte',
				},
			'TCCR3A': {
					'address': 0x90, 'module': 'TimerCounter3',
					'description': 'Timer/Counter 3 Control Register A',
					'bitfields': {
							'COM3A1': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'COM3A0': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'COM3B1': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
								},
							'COM3B0': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'COM3C1': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'COM3C0': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'WGM31': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'WGM30': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'TCCR3B': {
					'address': 0x91, 'module': 'TimerCounter3',
					'description': 'Timer/Counter 3 Control Register B',
					'bitfields': {
							'ICNC3': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'ICES3': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'WGM33': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'WGM32': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'CS32': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'CS31': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'CS30': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},

						},
				},
			'TCCR3C': {
					'address': 0x92, 'module': 'TimerCounter3',
					'description': 'Timer/Counter 3 Control Register C',
					'bitfields': {
							'FOC3A': {
									'slice': (7,), 'access': 'W', 'default': 0,
								},
							'FOC3B': {
									'slice': (6,), 'access': 'W', 'default': 0,
								},
							'FOC3C': {
									'slice': (5,), 'access': 'W', 'default': 0,
								},
						},
				},
			'TCNT3L': {
					'address': 0x94, 'module': 'TimerCounter3',
					'description': 'Timer/Counter 3 low byte',
					'access': 'R/W', 'default': 0,
				},
			'TCNT3H': {
					'address': 0x95, 'module': 'TimerCounter3',
					'description': 'Timer/Counter 3 high byte',
					'access': 'R/W', 'default': 0,
				},
			'ICR3L': {
					'address': 0x96, 'module': 'TimerCounter3',
					'description': 'Input Capture Register 3 low byte',
				},
			'ICR3H': {
					'address': 0x97, 'module': 'TimerCounter3',
					'description': 'Input Capture Register 3 high byte',
				},
			'OCR3AL': {
					'address': 0x98, 'module': 'TimerCounter3',
					'description': 'Output Compare Register 3 A low byte',
				},
			'OCR3AH': {
					'address': 0x99, 'module': 'TimerCounter3',
					'description': 'Output Compare Register 3 A high byte',
				},
			'OCR3BL': {
					'address': 0x9A, 'module': 'TimerCounter3',
					'description': 'Output Compare Register 3 B low byte',
				},
			'OCR3BH': {
					'address': 0x9B, 'module': 'TimerCounter3',
					'description': 'Output Compare Register 3 B high byte',
				},
			'OCR3CL': {
					'address': 0x9C, 'module': 'TimerCounter3',
					'description': 'Output Compare Register 3 C low byte',
				},
			'OCR3CH': {
					'address': 0x9D, 'module': 'TimerCounter3',
					'description': 'Output Compare Register 3 C high byte',
				},
			'TCCR4A': {
					'address': 0xA0, 'module': 'TimerCounter4',
					'description': '''Timer/Counter 4 Control Register A''',
					'bitfields': {
							'COM4A1': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'COM4A0': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'COM4B1': {
									'slice': (5,), 'access': 'R/W', 'default': 0,
								},
							'COM4B0': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'COM4C1': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'COM4C0': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'WGM41': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'WGM40': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'TCCR4B': {
					'address': 0xA1, 'module': 'TimerCounter4',
					'description': '''Timer/Counter 4 Control Register B''',
					'bitfields': {
							'ICNC4': {
									'slice': (7,), 'access': 'R/W', 'default': 0,
								},
							'ICES4': {
									'slice': (6,), 'access': 'R/W', 'default': 0,
								},
							'WGM43': {
									'slice': (4,), 'access': 'R/W', 'default': 0,
								},
							'WGM42': {
									'slice': (3,), 'access': 'R/W', 'default': 0,
								},
							'CS42': {
									'slice': (2,), 'access': 'R/W', 'default': 0,
								},
							'CS41': {
									'slice': (1,), 'access': 'R/W', 'default': 0,
								},
							'CS40': {
									'slice': (0,), 'access': 'R/W', 'default': 0,
								},
						},
				},
			'TCCR4C': {
					'address': 0xA2, 'module': 'TimerCounter4',
					'description': '''Timer/Counter 4 Control Register C''',
					'bitfields': {
							'FOC4A': {
									'slice': (7,), 'access': 'W', 'default': 0,
								},
							'FOC4B': {
									'slice': (6,), 'access': 'W', 'default': 0,
								},
							'FOC4C': {
									'slice': (5,), 'access': 'W', 'default': 0,
								},
						},
				},
			'TCNT4L': {
					'address': 0xA4, 'module': 'TimerCounter4',
					'description': 'Timer/Counter 4 low byte',
				},
			'TCNT4H': {
					'address': 0xA5, 'module': 'TimerCounter4',
					'description': 'Timer/Counter 4 high byte',
				},
			'ICR4L': {
					'address': 0xA6, 'module': 'TimerCounter4',
					'description': 'Input Capture Register 4 low byte',
				},
			'ICR4H': {
					'address': 0xA7, 'module': 'TimerCounter4',
					'description': 'Input Capture Register 4 high byte',
				},
			'OCR4AL': {
					'address': 0xA8, 'module': 'TimerCounter4',
					'description': 'Output Compare Register 4 A low byte',
				},
			'OCR4AH': {
					'address': 0xA9, 'module': 'TimerCounter4',
					'description': 'Output Compare Register 4 A high byte',
				},
			'OCR4BL': {
					'address': 0xAA, 'module': 'TimerCounter4',
					'description': 'Output Compare Register 4 B low byte',
				},
			'OCR4BH': {
					'address': 0xAB, 'module': 'TimerCounter4',
					'description': 'Output Compare Register 4 B high byte',
				},
			'OCR4CL': {
					'address': 0xAC, 'module': 'TimerCounter4',
					'description': 'Output Compare Register 4 C low byte',
				},
			'OCR4CH': {
					'address': 0xAD, 'module': 'TimerCounter4',
					'description': 'Output Compare Register 4 C high byte',
				},
			'TCCR2A': {
					'address': 0xB0, 'module': 'TimerCounter2',
					'description': 'Timer/Counter Control Register A',
					'bitfields': {
							'COM2A1': {
									'slice': (7,6),
									'description': '''Compare Match Output A mode

These bits control the Output Compare pin (OC2A) behavior. If one or both of the COM2A1:0 bits are set, the OC2A output overrides the normal port functionality of the I/O pin it is connected to. However, note that the Data Direction Register (DDR) bit corresponding to the OC2A pin must be set in order to enable the output driver.  When OC2A is connected to the pin, the function of the COM2A1:0 bits depends on the WGM22:0 bit setting. Table 20-2 shows the COM2A1:0 bit functionality when the WGM22:0 bits are set to a normal or CTC mode (non-PWM).

Table 20-2. Compare Output Mode, non-PWM Mode

COM2A<1:0> Description
---------- -----------
00         Normal port operation, OC2A disconnected
01         Toggle OC2A on Compare Match
10         Clear OC2A on Compare Match
11         Set OC2A on Compare Match

Table 20-3 shows the COM2A1:0 bit functionality when the WGM21:0 bits are set to fast PWM mode.

Table 20-3. Compare Output Mode, Fast PWM Mode(1)

COM2A<1:0> Description
---------- -----------
00:        Normal port operation, OC2A disconnected
01:        WGM22 = 0: Normal Port Operation, OC2A Disconnected WGM22 = 1: Toggle OC2A on Compare Match
10:        Clear OC2A on Compare Match, set OC2A at BOTTOM (non-inverting mode)
11:        Set OC2A on Compare Match, clear OC2A at BOTTOM (inverting mode)

Note: 1. A special case occurs when OCR2A equals TOP and COM2A1 is set. In this case, the Compare Match is ignored, but the set or clear is done at BOTTOM. See "Fast PWM Mode" on page 178 for more details.

Table 20-4 on page 188 shows the COM2A1:0 bit functionality when the WGM22:0 bits are set to phase correct PWM mode.

Table 20-4. Compare Output Mode, Phase Correct PWM Mode(1)

COM2A<1:0> Description
---------- -----------
00:         Normal port operation, OC2A disconnected
01:         WGM22 = 0: Normal Port Operation, OC2A Disconnected WGM22 = 1: Toggle OC2A on Compare Match
10:         Clear OC2A on Compare Match when up-counting Set OC2A on Compare Match when down-counting
11:         Set OC2A on Compare Match when up-counting Clear OC2A on Compare Match when down-counting

Note: 1. A special case occurs when OCR2A equals TOP and COM2A1 is set. In this case, the Compare Match is ignored, but the set or clear is done at TOP. See "Phase Correct PWM Mode" on page 179 for more details.  ''',
								},
							'COM2B': {
									'slice': (5,4),
									'description': '''Compare Match Output B Mode

These bits control the Output Compare pin (OC2B) behavior. If one or both of the COM2B1:0 bits are set, the OC2B output overrides the normal port functionality of the I/O pin it is connected to. However, note that the Data Direction Register (DDR) bit corresponding to the OC2B pin must be set in order to enable the output driver.

When OC2B is connected to the pin, the function of the COM2B1:0 bits depends on the WGM22:0 bit setting. Table 20-5 shows the COM2B1:0 bit functionality when the WGM22:0 bits are set to a normal or CTC mode (non-PWM).

Table 20-5. Compare Output Mode, non-PWM Mode
COM2B<1:0> Description
---------- -----------
00:        Normal port operation, OC2B disconnected
01:        Toggle OC2B on Compare Match
10:        Clear OC2B on Compare Match
11         Set OC2B on Compare Match


Table 20-6 shows the COM2B1:0 bit functionality when the WGM22:0 bits
are set to fast PWM mode.

Table 20-6. Compare Output Mode, Fast PWM Mode(1)
COM2B<1:0> Description
---------- -----------
00:        Normal port operation, OC2B disconnected
01:        Reserved
10:        Clear OC2B on Compare Match, set OC2B at BOTTOM (non-inverting mode)
11:        Set OC2B on Compare Match, clear OC2B at BOTTOM (inverting mode)

Note: 1. A special case occurs when OCR2B equals TOP and COM2B1 is set. In this case, the Compare Match is ignored, but the set or clear is done at BOTTOM. See "Fast PWM Mode" on page 178 for more details.

Table 20-7 shows the COM2B1:0 bit functionality when the WGM22:0 bits are set to phase cor- rect PWM mode.
Table 20-7. Compare Output Mode, Phase Correct PWM Mode(1)

COM2B<1:0> Description
---------- -----------
00:        Normal port operation, OC2B disconnected
01:        Reserved
10:        Clear OC2B on Compare Match when up-counting Set OC2B on Compare Match when down-counting
11:        Set OC2B on Compare Match when up-counting Clear OC2B on Compare Match when down-counting

Note: 1. A special case occurs when OCR2B equals TOP and COM2B1 is set. In this case, the Com- pare Match is ignored, but the set or clear is done at TOP. See "Phase Correct PWM Mode" on page 179 for more details.
''',
								},
							'WGM2': {
									'slice': (1,0),
									'description': '''Waveform Generation Mode

Combined with the WGM22 bit found in the TCCR2B Register, these bits control the counting sequence of the counter, the source for maximum (TOP) counter value, and what type of waveform generation to be used, see Table 20-8. Modes of operation supported by the Timer/Counter unit are: Normal mode (counter), Clear Timer on Compare Match (CTC) mode, and two types of Pulse Width Modulation (PWM) modes (see "Modes of Operation" on page 176).

Table 20-8. Waveform Generation Mode Bit Description

Mode WGM<2:0> Timer/Counter Mode TOP  Update of OCRx at TOV Flag Set on(1)(2)
---- -------- ------------------ ---  ----------------- ---------------------
0    0 0 0    Normal             0xFF Immediate         MAX
1    0 0 1    PWM, Phase Correct 0xFF TOP               BOTTOM
2    0 1 0    CTC                OCRA Immediate         MAX
3    0 1 1    Fast PWM           0xFF BOTTOM            MAX
4    1 0 0    Reserved           -    -                 -
5    1 0 1    PWM, Phase Correct OCRA TOP               BOTTOM
6    1 1 0    Reserved           -    -                 -
7    1 1 1    Fast PWM           OCRA BOTTOM            TOP

Notes: 1. MAX = 0xFF. 2. BOTTOM = 0x00.
''',
								},
						},
				},
			'TCCR2B': {
					'address': 0xB1, 'module': 'TimerCounter2',
					'bitfields': {
							'FOC2A': {
									'slice': (7,),
									'description': '''Force Output Compare A

The FOC2A bit is only active when the WGM bits specify a non-PWM mode.

However, for ensuring compatibility with future devices, this bit must be set to zero when TCCR2B is written when operating in PWM mode. When writing a logical one to the FOC2A bit, an immediate Compare Match is forced on the Waveform Generation unit. The OC2A output is changed according to its COM2A1:0 bits setting. Note that the FOC2A bit is implemented as a strobe. Therefore it is the value present in the COM2A1:0 bits that determines the effect of the forced compare.

A FOC2A strobe will not generate any interrupt, nor will it clear the timer in CTC mode using OCR2A as TOP.

The FOC2A bit is always read as zero.''',
								},
							'FOC2B': {
									'slice': (6,),
									'description': '''Force Output Compare B

The FOC2B bit is only active when the WGM bits specify a non-PWM mode.

However, for ensuring compatibility with future devices, this bit must be set to zero when TCCR2B is written when operating in PWM mode. When writing a logical one to the FOC2B bit, an immediate Compare Match is forced on the Waveform Generation unit. The OC2B output is changed according to its COM2B1:0 bits setting. Note that the FOC2B bit is implemented as a strobe. Therefore it is the value present in the COM2B1:0 bits that determines the effect of the forced compare.

A FOC2B strobe will not generate any interrupt, nor will it clear the timer in CTC mode using OCR2B as TOP.

The FOC2B bit is always read as zero.
''',
								},
							'WGM22': {
									'slice': (3,),
									'description': '''Waveform Generation Mode

See the description in the TCCR2A - Timer/Counter Control Register" on page 187.''',
								},
							'CS2': {
									'slice': (2,0),
									'description': '''Clock Select

The three Clock Select bits select the clock source to be used by the
Timer/Counter, see Table 20-9 on page 191.

Table 20-9. Clock Select Bit Description

CS2<2:0> Description
-------- -----------
0 0 0:   No clock source (Timer/Counter stopped)
0 0 1:   clkT2S/(No prescaling)
0 1 0:   clkT2S/8 (From prescaler)
0 1 1:   clkT2S/32 (From prescaler)
1 0 0:   clkT2S/64 (From prescaler)
1 0 1:   clkT2S/128 (From prescaler)
1 1 0:   clkT2S/256 (From prescaler)
1 1 1:   clkT2S/1024 (From prescaler)

If external pin modes are used for the Timer/Counter0, transitions on the T0 pin will clock the counter even if the pin is configured as an output. This feature allows software control of the counting.  ''',
								},
						},
				},
			'TCNT2': {
					'address': 0xB2, 'module': 'TimerCounter2',
					'access': 'R/W', 'default': 0,
					'description': '''Timer/Counter Register

The Timer/Counter Register gives direct access, both for read and write operations, to the Timer/Counter unit 8-bit counter. Writing to the TCNT2 Register blocks (removes) the Compare Match on the following timer clock. Modifying the counter (TCNT2) while the counter is running, introduces a risk of missing a Compare Match between TCNT2 and the OCR2x Registers.''',
				},
			'OCR2A': {
					'address': 0xB3, 'module': 'TimerCounter2',
					'description': '''Output Compare Register A

The Output Compare Register A contains an 8-bit value that is continuously compared with the counter value (TCNT2). A match can be used to generate an Output Compare interrupt, or to generate a waveform output on the OC2A pin.''',
				},
			'OCR2B': {
					'address': 0xB4, 'module': 'TimerCounter2',
					'description': '''Output Compare Register B

The Output Compare Register B contains an 8-bit value that is continuously compared with the counter value (TCNT2). A match can be used to generate an Output Compare interrupt, or to generate a waveform output on the OC2B pin. ''',
				},
			'ASSR': {
					'address': 0xB6, 'module': 'TimerCounter',
					'description': '''Asynchronous Status Register''',
					'bitfields': {
							'EXCLK': {
									'slice': (6,),
									'description': '''Enable External Clock Input

When EXCLK is written to one, and asynchronous clock is selected, the external clock input buffer is enabled and an external clock can be input on Timer Oscillator 1 (TOSC1) pin instead of a 32kHz crystal.  Writing to EXCLK should be done before asynchronous operation is selected. Note that the crystal Oscillator will only run when this bit is zero.''',
								},
							'AS2': {
									'slice': (5,),
									'description': '''Asynchronous Timer/Counter2

When AS2 is written to zero, Timer/Counter2 is clocked from the I/O clock, clkI/O. When AS2 is written to one, Timer/Counter2 is clocked from a crystal Oscillator connected to the Timer Oscillator 1 (TOSC1) pin. When the value of AS2 is changed, the contents of TCNT2, OCR2A, OCR2B, TCCR2A and TCCR2B might be corrupted.''',
								},
							'TCN2UB': {
									'slice': (4,),
									'description': '''Timer/Counter2 Update Busy

When Timer/Counter2 operates asynchronously and TCNT2 is written, this bit becomes set. When TCNT2 has been updated from the temporary storage register, this bit is cleared by hardware. A logical zero in this bit indicates that TCNT2 is ready to be updated with a new value.''',
								},
							'OCR2AUB': {
									'slice': (3,),
									'description': '''Output Compare Register2 Update Busy

When Timer/Counter2 operates asynchronously and OCR2A is written, this bit becomes set. When OCR2A has been updated from the temporary storage register, this bit is cleared by hardware. A logical zero in this bit indicates that OCR2A is ready to be updated with a new value.''',
								},
							'OCR2BUB': {
									'slice': (2,),
									'description': '''Output Compare Register2 Update Busy

When Timer/Counter2 operates asynchronously and OCR2B is written, this bit becomes set. When OCR2B has been updated from the temporary storage register, this bit is cleared by hardware. A logical zero in this bit indicates that OCR2B is ready to be updated with a new value.'''
								},
							'TCR2AUB': {
									'slice': (1,),
									'description': '''Timer/Counter Control Register2 Update Busy

When Timer/Counter2 operates asynchronously and TCCR2A is written, this bit becomes set. When TCCR2A has been updated from the temporary storage register, this bit is cleared by hardware. A logical zero in this bit indicates that TCCR2A is ready to be updated with a new value.''',
								},
							'TCR2BUB': {
									'slice': (0,),
									'description': '''Timer/Counter Control Register2 Update Busy

When Timer/Counter2 operates asynchronously and TCCR2B is written, this bit becomes set. When TCCR2B has been updated from the temporary storage register, this bit is cleared by hardware. A logical zero in this bit indicates that TCCR2B is ready to be updated with a new value.

If a write is performed to any of the five Timer/Counter2 Registers while its update busy flag is set, the updated value might get corrupted and cause an unintentional interrupt to occur.

The mechanisms for reading TCNT2, OCR2A, OCR2B, TCCR2A and TCCR2B are different. When reading TCNT2, the actual timer value is read. When reading OCR2A, OCR2B, TCCR2A and TCCR2B the value in the temporary storage register is read.''',
							},
						},
				},
			'TWBR': {
					'address': 0xB8, 'module': 'TWI',
					'description': '''TWI Bit Rate Register

TWBR selects the division factor for the bit rate generator. The bit rate generator is a frequency divider which generates the SCL clock frequency in the Master modes. See "Bit Rate Generator Unit" on page 247 for calculating bit rates.''',
				},
			'TWSR': {
					'address': 0xB9, 'module': 'TWI',
					'description': '''TWI Status Register''',
					'bitfields': {
							'TWS': {
									'slice': (7,3),
									'description': '''TWI Status

These five bits reflect the status of the TWI logic and the 2-wire Serial Bus. The different status codes are described later in this section. Note that the value read from TWSR contains both the 5-bit status value and the 2-bit prescaler value. The application designer should mask the prescaler bits to zero when checking the Status bits. This makes status checking independent of prescaler setting. This approach is used in this datasheet, unless otherwise noted. ''',
								},
							'TWPS': {
									'slice': (1,0),
									'description': '''TWI Prescaler Bits

These bits can be read and written, and control the bit rate prescaler.

Table 24-7. TWI Bit Rate Prescaler

TWPS<1:0> Prescaler Value
--------- ---------------
0 0       1
0 1       4
1 0       16
1 1       64

To calculate bit rates, see "Bit Rate Generator Unit" on page 247. The value of TWPS1:0 is used in the equation.
''',
								},
						},
				},
			'TWAR': {
					'address': 0xBA, 'module': 'TWI',
					'description': '''TWI (Slave) Address Register

The TWAR should be loaded with the 7-bit Slave address (in the seven most significant bits of TWAR) to which the TWI will respond when programmed as a Slave Transmitter or Receiver, and not needed in the Master modes. In multimaster systems, TWAR must be set in masters which can be addressed as Slaves by other Masters.

The LSB of TWAR is used to enable recognition of the general call address (0x00). There is an associated address comparator that looks for the slave address (or general call address if enabled) in the received serial address. If a match is found, an interrupt request is generated''',
					'bitfields': {
							'TWA': {
									'slice': (7,1),
									'description': '''TWI (Slave) Address Register

These seven bits constitute the slave address of the TWI unit.''',
								},
							'TWGCE': {
									'slice': (0,),
									'description': '''TWI General Call Recognition Enable Bit

If set, this bit enables the recognition of a General Call given over the 2-wire Serial Bus.''',
								},
						},
				},
			'TWDR': {
					'address': 0xBB, 'module': 'TWI',
					'default': 0xff, 'access': 'R/W',
					'description':  '''TWI Data Register

In Transmit mode, TWDR contains the next byte to be transmitted. In Receive mode, the TWDR contains the last byte received. It is writable while the TWI is not in the process of shifting a byte. This occurs when the TWI Interrupt Flag (TWINT) is set by hardware. Note that the Data Register cannot be initialized by the user before the first interrupt occurs. The data in TWDR remains stable as long as TWINT is set. While data is shifted out, data on the bus is simultaneously shifted in. TWDR always contains the last byte present on the bus, except after a wake up from a sleep mode by the TWI interrupt. In this case, the contents of TWDR is undefined. In the case of a lost bus arbitration, no data is lost in the transition from Master to Slave.  Handling of the ACK bit is controlled automatically by the TWI logic, the CPU cannot access the ACK bit directly.''',
					'bitfields': {
							'TWD': {
								'slice': (7,0),
								'description': '''TWI Data Register

These eight bits constitute the next data byte to be transmitted, or the latest data byte received on the 2-wire Serial Bus.''',
								},
						},
				},
			'TWCR': {
					'address': 0xBC, 'module': 'TWI',
					'default': 0,
					'description': '''TWI Control Register

The TWCR is used to control the operation of the TWI. It is used to enable the TWI, to initiate a Master access by applying a START condition to the bus, to generate a Receiver acknowledge, to generate a stop condition, and to control halting of the bus while the data to be written to the bus are written to the TWDR. It also indicates a write collision if data is attempted written to TWDR while the register is inaccessible''',
					'bitfields': {
							'TWINT': {
									'slice': (7,),
									'description': '''TWI Interrupt Flag

This bit is set by hardware when the TWI has finished its current job and expects application software response. If the I-bit in SREG and TWIE in TWCR are set, the MCU will jump to the TWI Interrupt Vector. While the TWINT Flag is set, the SCL low period is stretched. The TWINT Flag must be cleared by software by writing a logic one to it. Note that this flag is not automatically cleared by hardware when executing the interrupt routine. Also note that clearing this flag starts the operation of the TWI, so all accesses to the TWI Address Register (TWAR), TWI Status Register (TWSR), and TWI Data Register (TWDR) must be complete before clearing this flag.''',
								},
							'TWEA': {
									'slice': (6,),
									'description': '''TWEA: TWI Enable Acknowledge Bit

The TWEA bit controls the generation of the acknowledge pulse. If the TWEA bit is written to one, the ACK pulse is generated on the TWI bus if the following conditions are met:

1. The device's own slave address has been received.
2. A general call has been received, while the TWGCE bit in the TWAR is set.
3. A data byte has been received in Master Receiver or Slave Receiver mode.

By writing the TWEA bit to zero, the device can be virtually disconnected from the 2-wire Serial Bus temporarily. Address recognition can then be resumed by writing the TWEA bit to one again.''',
								},
							'TWSTA': {
									'slice': (5,),
									'description': '''TWI START Condition Bit

The application writes the TWSTA bit to one when it desires to become a Master on the 2-wire Serial Bus.  The TWI hardware checks if the bus is available, and generates a START condition on the bus if it is free. However, if the bus is not free, the TWI waits until a STOP condition is detected, and then generates a new START condition to claim the bus Master status. TWSTA must be cleared by software when the START condition has been transmitted.''',
								},
							'TWSTO': {
									'slice': (4,),
									'description': '''TWI STOP Condition Bit

Writing the TWSTO bit to one in Master mode will generate a STOP condition on the 2-wire Serial Bus.  When the STOP condition is executed on the bus, the TWSTO bit is cleared automatically. In Slave mode, setting the TWSTO bit can be used to recover from an error condition. This will not generate a STOP condition, but the TWI returns to a well-defined unaddressed Slave mode and releases the SCL and SDA lines to a high impedance state.''',
								},
						},
				},
			'TWAMR': {
					'address': 0xBD, 'module': 'TWI',
					'description': '''TWI (Slave) Address Mask Register''',
					'bitfields': {
							'TWAM': {
									'slice': (7,1),
									'description': '''TWI Address Mask

The TWAMR can be loaded with a 7-bit Slave Address mask. Each of the bits in TWAMR can mask (disable) the corresponding address bit in the TWI Address Register (TWAR). If the mask bit is set to one then the address match logic ignores the compare between the incoming address bit and the corresponding bit in TWAR. Figure 24-22 shows the address match logic in detail.''',
								},
						},
				},
			'UCSR0A': {
					'address': 0xC0, 'module': 'USART',
					'description': '''USART Control and Status Register A''',
					'bitfields': {
							'RXC0': {
									'slice': (7,),
									'description': '''USART Receive Complete

This flag bit is set when there are unread data in the receive buffer and cleared when the receive buffer is empty (that is, does not contain any unread data). If the Receiver is disabled, the receive buffer will be flushed and consequently the RXC0 bit will become zero.  The RXC0 Flag can be used to generate a Receive Complete interrupt (see description of the RXCIE0 bit).''',
								},
							'TXC0': {
									'slice': (6,),
									'description': '''USART Transmit Complete

This flag bit is set when the entire frame in the Transmit Shift Register has been shifted out and there are no new data currently present in the transmit buffer (UDR0). The TXC0 Flag bit is automatically cleared when a transmit complete interrupt is executed, or it can be cleared by writing a one to its bit location. The TXC0 Flag can generate a Transmit Complete interrupt (see description of the TXCIE0 bit).''',
								},
							'UDRE0': {
									'slice': (5,),
									'description': '''USART Data Register Empty

The UDRE0 Flag indicates if the transmit buffer (UDR0) is ready to receive new data. If UDRE0 is one, the buffer is empty, and therefore ready to be written. The UDRE0 Flag can generate a Data Register Empty interrupt (see description of the UDRIE0 bit).

UDRE0 is set after a reset to indicate that the Transmitter is ready.''',
								},
							'FE0': {
									'slice': (4,),
									'description': '''Frame Error

This bit is set if the next character in the receive buffer had a Frame Error when received, that is, when the first stop bit of the next character in the receive buffer is zero. This bit is valid until the receive buffer (UDR0) is read. The FE0 bit is zero when the stop bit of received data is one. Always set this bit to zero when writing to UCSR0A.''',
								},
							'DOR0': {
									'slice': (3,),
									'description': '''Data OverRun

This bit is set if a Data OverRun condition is detected. A Data OverRun occurs when the receive buffer is full (two characters), it is a new character waiting in the Receive Shift Register, and a new start bit is detected. This bit is valid until the receive buffer (UDR0) is read. Always set this bit to zero when writing to UCSR0A.''',
								},
							'UPE0': {
									'slice': (2,),
									'description': '''USART Parity Error

This bit is set if the next character in the receive buffer had a Parity Error when received and the Parity Checking was enabled at that point (UPM01 = 1). This bit is valid until the receive buffer (UDR0) is read. Always set this bit to zero when writing to UCSR0A.''',
								},
							'U2X0': {
									'slice': (1,),
									'description': '''Double the USART Transmission Speed

This bit only has effect for the asynchronous operation. Write this bit to zero when using synchronous operation.

Writing this bit to one will reduce the divisor of the baud rate divider from 16 to 8 effectively doubling the transfer rate for asynchronous communication.''',
								},
							'MPCM0': {
									'slice': (0,),
									'description': '''Multi-processor Communication Mode

This bit enables the Multi-processor Communication mode. When the MPCM0 bit is written to one, all the incoming frames received by the USART Receiver that do not contain address information will be ignored. The Transmitter is unaffected by the MPCM0 setting. For more detailed information see "Multi-processor Communication Mode" on page 221.''',
								},
						},
				},
			'UCSR0B': {
					'address': 0xC1, 'module': 'USART',
					'description': '''USART Control and Status Register 0 B''',
					'bitfields': {
							'RXCIE0': {
									'slice': (7,),
									'description': '''RX Complete Interrupt Enable 0

Writing this bit to one enables interrupt on the RXC0 Flag. A USART Receive Complete interrupt will be generated only if the RXCIE0 bit is written to one, the Global Interrupt Flag in SREG is written to one and the RXC0 bit in UCSR0A is set.''',
								},
							'TXCIE0': {
									'slice': (6,),
									'description': '''TX Complete Interrupt Enable 0

Writing this bit to one enables interrupt on the TXC0 Flag. A USART Transmit Complete interrupt will be generated only if the TXCIE0 bit is written to one, the Global Interrupt Flag in SREG is written to one and the TXC0 bit in UCSR0A is set.''',
								},
							'UDRIE0': {
									'slice': (5,),
									'description': '''USART Data Register Empty Interrupt Enable 0

Writing this bit to one enables interrupt on the UDRE0 Flag. A Data Register Empty interrupt will be generated only if the UDRIE0 bit is written to one, the Global Interrupt Flag in SREG is written to one and the UDRE0 bit in UCSR0A is set.''',
								},
							'RXEN0': {
									'slice': (4,),
									'description': '''Receiver Enable 0

Writing this bit to one enables the USART Receiver.  The Receiver will override normal port operation for the RxD0 pin when enabled. Disabling the Receiver will flush the receive buffer invalidating the FE0, DOR0, and UPE0 Flags.''',
								},
							'TXEN0': {
									'slice': (3,),
									'description': '''Transmitter Enable 0

Writing this bit to one enables the USART Transmitter. The Transmitter will override normal port operation for the TxD0 pin when enabled. The disabling of the Transmitter (writing TXEN0 to zero) will not become effective until ongoing and pending transmissions are completed, that is, when the Transmit Shift Register and Transmit Buffer Register do not contain data to be transmitted. When disabled, the Transmitter will no longer override the TxD0 port.''',
								},
							'UCSZ02': {
									'slice': (2,),
									'description': '''Character Size 0

The UCSZ02 bits combined with the UCSZ0<1:0> bit in UCSR0C sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.''',
								},
							'RXB80': {
									'slice': (1,),
									'description': '''Receive Data Bit 8 0

RXB80 is the ninth data bit of the received character when operating with serial frames with nine data bits. Must be read before reading the low bits from UDR0.''',
								},
							'TXB80': {
									'slice': (0,),
									'description': '''Transmit Data Bit 8 0

TXB80 is the ninth data bit in the character to be transmitted when operating with serial frames with nine data bits. Must be written before writing the low bits to UDR0.''',
								},
						},
				},
			'UCSR0C': {
					'address': 0xC2, 'module': 'USART',
					'description': '''USART Control and Status Register 0 C''',
					'bitfields': {
							'UMSEL0': {
									'slice': (7,6),
									'description': '''USART Mode Select

These bits select the mode of operation of the USART0 as shown in Table 22-4.

Table 22-4. UMSEL0 Bits Settings

UMSEL0<1:0> Mode
----------- ---
0 0         Asynchronous USART
0 1         Synchronous USART
1 0         (Reserved)
1 1         Master SPI (MSPIM)(1)

Note: 1. See "USART in SPI Mode" on page 232 for full description of the Master SPI Mode (MSPIM) operation.
''',
								},
							'UPM0': {
									'slice': (5,4),
									'description': '''Parity Mode

These bits enable and set type of parity generation and check. If enabled, the Transmitter will automatically generate and send the parity of the transmitted data bits within each frame. The Receiver will generate a parity value for the incoming data and compare it to the UPM0 setting. If a mismatch is detected, the UPE0 Flag in UCSR0A will be set.

Table 22-5. UPM0 Bits Settings

UPM0<1:0> Parity Mode
--------- -----------
0 0       Disabled
0 1       Reserved
1 0       Enabled, Even Parity
1 1       Enabled, Odd Parity
''',
								},
							'USBS0': {
									'slice': (3,),
									'description': '''Stop Bit Select

This bit selects the number of stop bits to be inserted by the Transmitter. The Receiver ignores this setting.

Table 22-6. USBS Bit Settings

USBS0 Stop Bit(s)
----- -----------
0     1-bit
1     2-bit
''',
								},
							'UCSZ0': {
									'slice': (2,1),
									'description': '''Character Size

The UCSZ0<1:0> bits combined with the UCSZ02 bit in UCSR0B sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.

Table 22-7. UCSZ0 Bits Settings

UCSZ0<2:0> Character Size
---------- --------------
0 0 0      5-bit
0 0 1      6-bit
0 1 0      7-bit
0 1 1      8-bit
1 0 0      Reserved
1 0 1      Reserved
1 1 0      Reserved
1 1 1      9-bit
''',
								},
							'UCPOL0': {
									'slice': (0,),
									'description': '''Clock Polarity

This bit is used for synchronous mode only. Write this bit to zero when asynchronous mode is used. The UCPOL0 bit sets the relationship between data output change and data input sample, and the synchronous clock (XCK0).

Table 22-8.  UCPOL0 Bit Settings

UCPOL0 Transmitted Data Changed Received Data Sampled 
       (Output of TxD0 Pin)     (Input on RxD0 Pin)
------ ------------------------ ---------------------
0       Rising XCK0 Edge         Falling XCK0 Edge
1       Falling XCK0 Edge        Rising XCK0 Edge
''',
								},
						},
				},
			'UBRR0L': {
					'address': 0xC4, 'module': 'USART',
					'description': '''USART Baud Rate Register low byte

This is the low byte of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UBRR0H': {
					'address': 0xC5, 'module': 'USART',
					'description': '''USART Baud Rate Register high byte

This is the high nibble of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UDR0': {
					'module': 'USART', 'address': 0xC6,
					'description': '''USART I/O Data Register 0

The USART Transmit Data Buffer Register and USART Receive Data Buffer Registers share the same I/O address referred to as USART Data Register or UDR0. The Transmit Data Buffer Register (TXB) will be the destination for data written to the UDR0 Register location.  Reading the UDR0 Register location will return the contents of the Receive Data Buffer Register (RXB).

For 5-bit, 6-bit, or 7-bit characters the upper unused bits will be ignored by the Transmitter and set to zero by the Receiver.

The transmit buffer can only be written when the UDRE0 Flag in the UCSR0A Register is set. Data written to UDR0 when the UDRE0 Flag is not set, will be ignored by the USART Transmitter. When data is written to the transmit buffer, and the Transmitter is enabled, the Transmitter will load the data into the Transmit Shift Register when the Shift Register is empty. Then the data will be serially transmitted on the TxD0 pin.  The receive buffer consists of a two level FIFO. The FIFO will change its state whenever the receive buffer is accessed. Due to this behavior of the receive buffer, do not use Read-Modify-Write instructions (SBI and CBI) on this location. Be careful when using bit test instructions (SBIC and SBIS), since these also will change the state of the FIFO.
''',
				},
			'UCSR1A': {
					'address': 0xC8, 'module': 'USART',
					'description': '''USART Control and Status Register A''',
					'bitfields': {
							'RXC1': {
									'slice': (7,),
									'description': '''USART Receive Complete

This flag bit is set when there are unread data in the receive buffer and cleared when the receive buffer is empty (that is, does not contain any unread data). If the Receiver is disabled, the receive buffer will be flushed and consequently the RXCn bit will become zero.  The RXCn Flag can be used to generate a Receive Complete interrupt (see description of the RXCIEn bit).''',
								},
							'TXC1': {
									'slice': (6,),
									'description': '''USART Transmit Complete

This flag bit is set when the entire frame in the Transmit Shift Register has been shifted out and there are no new data currently present in the transmit buffer (UDR1). The TXC1 Flag bit is automatically cleared when a transmit complete interrupt is executed, or it can be cleared by writing a one to its bit location. The TXC1 Flag can generate a Transmit Complete interrupt (see description of the TXCIE1 bit).''',
								},
							'UDRE1': {
									'slice': (5,),
									'description': '''USART Data Register Empty

The UDRE1 Flag indicates if the transmit buffer (UDR1) is ready to receive new data. If UDRE1 is one, the buffer is empty, and therefore ready to be written. The UDRE1 Flag can generate a Data Register Empty interrupt (see description of the UDRIE1 bit).

UDRE1 is set after a reset to indicate that the Transmitter is ready.''',
								},
							'FE1': {
									'slice': (4,),
									'description': '''Frame Error

This bit is set if the next character in the receive buffer had a Frame Error when received, that is, when the first stop bit of the next character in the receive buffer is zero. This bit is valid until the receive buffer (UDR1) is read. The FE1 bit is zero when the stop bit of received data is one. Always set this bit to zero when writing to UCSR1A.''',
								},
							'DOR1': {
									'slice': (3,),
									'description': '''Data OverRun

This bit is set if a Data OverRun condition is detected. A Data OverRun occurs when the receive buffer is full (two characters), it is a new character waiting in the Receive Shift Register, and a new start bit is detected. This bit is valid until the receive buffer (UDR1) is read. Always set this bit to zero when writing to UCSR1A.''',
								},
							'UPE1': {
									'slice': (2,),
									'description': '''USART Parity Error

This bit is set if the next character in the receive buffer had a Parity Error when received and the Parity Checking was enabled at that point (UPM11 = 1). This bit is valid until the receive buffer (UDR1) is read. Always set this bit to zero when writing to UCSR1A.''',
								},
							'U2X1': {
									'slice': (1,),
									'description': '''Double the USART Transmission Speed

This bit only has effect for the asynchronous operation. Write this bit to zero when using synchronous operation.

Writing this bit to one will reduce the divisor of the baud rate divider from 16 to 8 effectively doubling the transfer rate for asynchronous communication.''',
								},
							'MPCM1': {
									'slice': (0,),
									'description': '''Multi-processor Communication Mode

This bit enables the Multi-processor Communication mode. When the MPCM1 bit is written to one, all the incoming frames received by the USART Receiver that do not contain address information will be ignored. The Transmitter is unaffected by the MPCM1 setting. For more detailed information see "Multi-processor Communication Mode" on page 221.''',
								},
						},
				},
			'UCSR1B': {
					'address': 0xC9, 'module': 'USART',
					'description': '''USART Control and Status Register 1 B''',
					'bitfields': {
							'RXCIE1': {
									'slice': (7,),
									'description': '''RX Complete Interrupt Enable 1

Writing this bit to one enables interrupt on the RXC1 Flag. A USART Receive Complete interrupt will be generated only if the RXCIE1 bit is written to one, the Global Interrupt Flag in SREG is written to one and the RXC1 bit in UCSR1A is set.''',
								},
							'TXCIE1': {
									'slice': (6,),
									'description': '''TX Complete Interrupt Enable 1

Writing this bit to one enables interrupt on the TXC1 Flag. A USART Transmit Complete interrupt will be generated only if the TXCIE1 bit is written to one, the Global Interrupt Flag in SREG is written to one and the TXC1 bit in UCSR1A is set.''',
								},
							'UDRIE1': {
									'slice': (5,),
									'description': '''USART Data Register Empty Interrupt Enable 1

Writing this bit to one enables interrupt on the UDRE1 Flag. A Data Register Empty interrupt will be generated only if the UDRIE1 bit is written to one, the Global Interrupt Flag in SREG is written to one and the UDRE0 bit in UCSR1A is set.''',
								},
							'RXEN1': {
									'slice': (4,),
									'description': '''Receiver Enable 1

Writing this bit to one enables the USART Receiver.  The Receiver will override normal port operation for the RxD1 pin when enabled. Disabling the Receiver will flush the receive buffer invalidating the FE1, DOR1, and UPE1 Flags.''',
								},
							'TXEN1': {
									'slice': (3,),
									'description': '''Transmitter Enable 1

Writing this bit to one enables the USART Transmitter. The Transmitter will override normal port operation for the TxD1 pin when enabled. The disabling of the Transmitter (writing TXEN1 to zero) will not become effective until ongoing and pending transmissions are completed, that is, when the Transmit Shift Register and Transmit Buffer Register do not contain data to be transmitted. When disabled, the Transmitter will no longer override the TxD1 port.''',
								},
							'UCSZ12': {
									'slice': (2,),
									'description': '''Character Size 1

The UCSZ12 bits combined with the UCSZ1<1:0> bit in UCSR1C sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.''',
								},
							'RXB81': {
									'slice': (1,),
									'description': '''Receive Data Bit 8 1

RXB81 is the ninth data bit of the received character when operating with serial frames with nine data bits. Must be read before reading the low bits from UDR1.''',
								},
							'TXB81': {
									'slice': (0,),
									'description': '''Transmit Data Bit 8 1

TXB81 is the ninth data bit in the character to be transmitted when operating with serial frames with nine data bits. Must be written before writing the low bits to UDR1.''',
								},
						},
				},
			'UCSR1C': {
					'address': 0xCA, 'module': 'USART',
					'description': '''USART Control and Status Register 1 C''',
					'bitfields': {
							'UMSEL1': {
									'slice': (7,6),
									'description': '''USART Mode Select

These bits select the mode of operation of the USART1 as shown in Table 22-4.

Table 22-4. UMSEL1 Bits Settings

UMSEL1<1:0> Mode
----------- ---
0 0         Asynchronous USART
0 1         Synchronous USART
1 0         (Reserved)
1 1         Master SPI (MSPIM)(1)

Note: 1. See "USART in SPI Mode" on page 232 for full description of the Master SPI Mode (MSPIM) operation.
''',
								},
							'UPM1': {
									'slice': (5,4),
									'description': '''Parity Mode

These bits enable and set type of parity generation and check. If enabled, the Transmitter will automatically generate and send the parity of the transmitted data bits within each frame. The Receiver will generate a parity value for the incoming data and compare it to the UPM1 setting. If a mismatch is detected, the UPE1 Flag in UCSR1A will be set.

Table 22-5. UPM1 Bits Settings

UPM1<1:0> Parity Mode
--------- -----------
0 0       Disabled
0 1       Reserved
1 0       Enabled, Even Parity
1 1       Enabled, Odd Parity
''',
								},
							'USBS1': {
									'slice': (3,),
									'description': '''Stop Bit Select

This bit selects the number of stop bits to be inserted by the Transmitter. The Receiver ignores this setting.

Table 22-6. USBS Bit Settings

USBS1 Stop Bit(s)
----- -----------
0     1-bit
1     2-bit
''',
								},
							'UCSZ1': {
									'slice': (2,1),
									'description': '''Character Size

The UCSZ1<1:0> bits combined with the UCSZ12 bit in UCSR1B sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.

Table 22-7. UCSZ1 Bits Settings

UCSZ1<2:0> Character Size
---------- --------------
0 0 0      5-bit
0 0 1      6-bit
0 1 0      7-bit
0 1 1      8-bit
1 0 0      Reserved
1 0 1      Reserved
1 1 0      Reserved
1 1 1      9-bit
''',
								},
							'UCPOL1': {
									'slice': (0,),
									'description': '''Clock Polarity

This bit is used for synchronous mode only. Write this bit to zero when asynchronous mode is used. The UCPOL1 bit sets the relationship between data output change and data input sample, and the synchronous clock (XCK1).

Table 22-8.  UCPOL1 Bit Settings

UCPOL1 Transmitted Data Changed Received Data Sampled 
       (Output of TxD1 Pin)     (Input on RxD1 Pin)
------ ------------------------ ---------------------
0       Rising XCK1 Edge         Falling XCK1 Edge
1       Falling XCK1 Edge        Rising XCK1 Edge
''',
								},
						},
				},
			'UBRR1L': {
					'address': 0xCC, 'module': 'USART',
					'description': '''USART Baud Rate Register low byte

This is the low byte of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UBBR1H': {
					'address': 0xCD, 'module': 'USART',
					'description': '''USART Baud Rate Register high byte

This is the high nibble of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UDR1': {
					'address': 0xCE, 'module': 'USART',
					'module': 'USART',
					'description': '''USART I/O Data Register 1

The USART Transmit Data Buffer Register and USART Receive Data Buffer Registers share the same I/O address referred to as USART Data Register or UDR1. The Transmit Data Buffer Register (TXB) will be the destination for data written to the UDR1 Register location.  Reading the UDR1 Register location will return the contents of the Receive Data Buffer Register (RXB).

For 5-bit, 6-bit, or 7-bit characters the upper unused bits will be ignored by the Transmitter and set to zero by the Receiver.

The transmit buffer can only be written when the UDRE1 Flag in the UCSR1A Register is set. Data written to UDR1 when the UDRE1 Flag is not set, will be ignored by the USART Transmitter. When data is written to the transmit buffer, and the Transmitter is enabled, the Transmitter will load the data into the Transmit Shift Register when the Shift Register is empty. Then the data will be serially transmitted on the TxD1 pin.  The receive buffer consists of a two level FIFO. The FIFO will change its state whenever the receive buffer is accessed. Due to this behavior of the receive buffer, do not use Read-Modify-Write instructions (SBI and CBI) on this location. Be careful when using bit test instructions (SBIC and SBIS), since these also will change the state of the FIFO.
''',
				},
			'UCSR2A': {
					'address': 0xD0, 'module': 'USART',
					'description': '''USART Control and Status Register A''',
					'bitfields': {
							'RXC2': {
									'slice': (7,),
									'description': '''USART Receive Complete

This flag bit is set when there are unread data in the receive buffer and cleared when the receive buffer is empty (that is, does not contain any unread data). If the Receiver is disabled, the receive buffer will be flushed and consequently the RXCn bit will become zero.  The RXCn Flag can be used to generate a Receive Complete interrupt (see description of the RXCIEn bit).''',
								},
							'TXC2': {
									'slice': (6,),
									'description': '''USART Transmit Complete

This flag bit is set when the entire frame in the Transmit Shift Register has been shifted out and there are no new data currently present in the transmit buffer (UDR2). The TXC2 Flag bit is automatically cleared when a transmit complete interrupt is executed, or it can be cleared by writing a one to its bit location. The TXC2 Flag can generate a Transmit Complete interrupt (see description of the TXCIE2 bit).''',
								},
							'UDRE2': {
									'slice': (5,),
									'description': '''USART Data Register Empty

The UDRE2 Flag indicates if the transmit buffer (UDR2) is ready to receive new data. If UDRE2 is one, the buffer is empty, and therefore ready to be written. The UDRE2 Flag can generate a Data Register Empty interrupt (see description of the UDRIE2 bit).

UDRE2 is set after a reset to indicate that the Transmitter is ready.''',
								},
							'FE2': {
									'slice': (4,),
									'description': '''Frame Error

This bit is set if the next character in the receive buffer had a Frame Error when received, that is, when the first stop bit of the next character in the receive buffer is zero. This bit is valid until the receive buffer (UDR2) is read. The FE2 bit is zero when the stop bit of received data is one. Always set this bit to zero when writing to UCSR2A.''',
								},
							'DOR2': {
									'slice': (3,),
									'description': '''Data OverRun

This bit is set if a Data OverRun condition is detected. A Data OverRun occurs when the receive buffer is full (two characters), it is a new character waiting in the Receive Shift Register, and a new start bit is detected. This bit is valid until the receive buffer (UDR2) is read. Always set this bit to zero when writing to UCSR2A.''',
								},
							'UPE2': {
									'slice': (2,),
									'description': '''USART Parity Error

This bit is set if the next character in the receive buffer had a Parity Error when received and the Parity Checking was enabled at that point (UPM21 = 1). This bit is valid until the receive buffer (UDR2) is read. Always set this bit to zero when writing to UCSR2A.''',
								},
							'U2X2': {
									'slice': (1,),
									'description': '''Double the USART Transmission Speed

This bit only has effect for the asynchronous operation. Write this bit to zero when using synchronous operation.

Writing this bit to one will reduce the divisor of the baud rate divider from 16 to 8 effectively doubling the transfer rate for asynchronous communication.''',
								},
							'MPCM2': {
									'slice': (0,),
									'description': '''Multi-processor Communication Mode

This bit enables the Multi-processor Communication mode. When the MPCM2 bit is written to one, all the incoming frames received by the USART Receiver that do not contain address information will be ignored. The Transmitter is unaffected by the MPCM2 setting. For more detailed information see "Multi-processor Communication Mode" on page 221.''',
								},
						},
				},
			'UCSR2B': {
					'address': 0xD1, 'module': 'USART',
					'description': '''USART Control and Status Register 2 B''',
					'bitfields': {
							'RXCIE2': {
									'slice': (7,),
									'description': '''RX Complete Interrupt Enable 2

Writing this bit to one enables interrupt on the RXC2 Flag. A USART Receive Complete interrupt will be generated only if the RXCIE2 bit is written to one, the Global Interrupt Flag in SREG is written to one and the RXC2 bit in UCSR2A is set.''',
								},
							'TXCIE2': {
									'slice': (6,),
									'description': '''TX Complete Interrupt Enable 2

Writing this bit to one enables interrupt on the TXC2 Flag. A USART Transmit Complete interrupt will be generated only if the TXCIE2 bit is written to one, the Global Interrupt Flag in SREG is written to one and the TXC2 bit in UCSR2A is set.''',
								},
							'UDRIE2': {
									'slice': (5,),
									'description': '''USART Data Register Empty Interrupt Enable 2

Writing this bit to one enables interrupt on the UDRE2 Flag. A Data Register Empty interrupt will be generated only if the UDRIE2 bit is written to one, the Global Interrupt Flag in SREG is written to one and the UDRE0 bit in UCSR2A is set.''',
								},
							'RXEN2': {
									'slice': (4,),
									'description': '''Receiver Enable 2

Writing this bit to one enables the USART Receiver.  The Receiver will override normal port operation for the RxD2 pin when enabled. Disabling the Receiver will flush the receive buffer invalidating the FE2, DOR2, and UPE2 Flags.''',
								},
							'TXEN2': {
									'slice': (3,),
									'description': '''Transmitter Enable 2

Writing this bit to one enables the USART Transmitter. The Transmitter will override normal port operation for the TxD2 pin when enabled. The disabling of the Transmitter (writing TXEN2 to zero) will not become effective until ongoing and pending transmissions are completed, that is, when the Transmit Shift Register and Transmit Buffer Register do not contain data to be transmitted. When disabled, the Transmitter will no longer override the TxD2 port.''',
								},
							'UCSZ22': {
									'slice': (2,),
									'description': '''Character Size 2

The UCSZ22 bits combined with the UCSZ2<1:0> bit in UCSR2C sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.''',
								},
							'RXB82': {
									'slice': (1,),
									'description': '''Receive Data Bit 8 2

RXB82 is the ninth data bit of the received character when operating with serial frames with nine data bits. Must be read before reading the low bits from UDR2.''',
								},
							'TXB82': {
									'slice': (0,),
									'description': '''Transmit Data Bit 8 2

TXB82 is the ninth data bit in the character to be transmitted when operating with serial frames with nine data bits. Must be written before writing the low bits to UDR2.''',
								},
						},
				},
			'UCSR2C': {
					'address': 0xD2, 'module': 'USART',
				},
			'UBRR2L': {
					'address': 0xD4, 'module': 'USART',
				},
			'UBRR2H': {
					'address': 0xD5, 'module': 'USART',
					'description': '''USART Baud Rate Register high byte

This is the high nibble of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UDR2': {
					'address': 0xD6, 'module': 'USART',
					'description': '''USART I/O Data Register 2

The USART Transmit Data Buffer Register and USART Receive Data Buffer Registers share the same I/O address referred to as USART Data Register or UDR2. The Transmit Data Buffer Register (TXB) will be the destination for data written to the UDR2 Register location.  Reading the UDR2 Register location will return the contents of the Receive Data Buffer Register (RXB).

For 5-bit, 6-bit, or 7-bit characters the upper unused bits will be ignored by the Transmitter and set to zero by the Receiver.

The transmit buffer can only be written when the UDRE2 Flag in the UCSR2A Register is set. Data written to UDR2 when the UDRE2 Flag is not set, will be ignored by the USART Transmitter. When data is written to the transmit buffer, and the Transmitter is enabled, the Transmitter will load the data into the Transmit Shift Register when the Shift Register is empty. Then the data will be serially transmitted on the TxD2 pin.  The receive buffer consists of a two level FIFO. The FIFO will change its state whenever the receive buffer is accessed. Due to this behavior of the receive buffer, do not use Read-Modify-Write instructions (SBI and CBI) on this location. Be careful when using bit test instructions (SBIC and SBIS), since these also will change the state of the FIFO.
''',
				},
			'PINH': {
					'address': 0x100, 'module': 'GPIO', 'default': 0, 'access': 'R/W',
					'description': '''Port H Input Pins Address''',
				},
			'DDRH': {
					'address': 0x101, 'module': 'GPIO', 'default': 0, 'access': 'R/W',
					'description': '''Port H Data Direction Register''',
				},
			'PORTH': {
					'address': 0x102, 'module': 'GPIO', 'default': 0, 'access': 'R/W',
					'description': '''Port H Data Register''',
				},
			'PINJ': {
					'address': 0x103, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port J Input Pins Address''',
				},
			'DDRJ': {
					'address': 0x104, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Pojrt J Data Direction Register''',
				},
			'PORTJ': {
					'address': 0x105, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port J Data Register''',
				},
			'PINK': {
					'address': 0x106, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port K Input Pins Address''',
				},
			'DDRK': {
					'address': 0x107, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port K Data Direction Register''',
				},
			'PORTK': {
					'address': 0x108, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port K Input Pins Address''',
				},
			'PINL': {
					'address': 0x109, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port L Input Pins Address''',
				},
			'DDRL': {
					'address': 0x10A, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port L Data Direction Register''',
				},
			'PORTL': {
					'address': 0x10B, 'module': 'GPIO', 'access': 'R/W', 'default': 0,
					'description': '''Port L Data Register''',
				},
			'TCCR5A': {
					'address': 0x120, 'module': 'TimerCounter5',
					'description': '''Timer/Counter 5 Control Register A

The COM5A1:0, COM5B1:0, and COM5C1:0 control the output compare pins (OC5A, OC5B, and OC5C respectively) behavior. If one or both of the COM5A1:0 bits are written to one, the OC5A output overrides the normal port functionality of the I/O pin it is connected to. If one or both of the COM5B1:0 bits are written to one, the OC5B output overrides the normal port functionality of the I/O pin it is connected to. If one or both of the COM5C1:0 bits are written to one, the OC5C output overrides the normal port functionality of the I/O pin it is connected to. However, note that the Data Direction Register (DDR) bit corresponding to the OC5A, OC5B or OC5C pin must be set in order to enable the output driver.

When the OC5A, OC5B or OC5C is connected to the pin, the function of the COM5x<1:0> bits is dependent of the WGM5<3:0> bits setting. Table 17-3 on page 159 shows the COM5x<1:0> bit functionality when the WGM5<3:0> bits are set to a normal or a CTC mode (non-PWM).''',
					'bitfields': {
							'COM5A': {
									'slice': (7,6),
									'access': 'R/W',
									'default': 0,
									'description': '''Compare Output Mode for Channel A''',
								},
							'COM5B': {
									'slice': (5,4),
									'access': 'R/W',
									'default': 0,
									'description': '''Compare Output Mode for Channel B''',
								},
							'COM5C_32': {
								'slice': (3,2),
								'access': 'R/W',
								'default': 0,
								'description': '''Compare Output Mode for Channel C

Combined with the WGM5<3:2> bits found in the TCCR5B Register, these bits control the counting sequence of the counter, the source for maximum (TOP) counter value, and what type of waveform generation to be used, see Table 17-2 on page 148. Modes of operation supported by the Timer/Counter unit are: Normal mode (counter), Clear Timer on Compare match (CTC) mode, and three types of Pulse Width Modulation (PWM) modes. For more information on the different modes, see "Modes of Operation" on page 148.

Table 17-3. Compare Output Mode, non-PWM
COM5[ABC]<1:0> Description
-------------- -----------
0 0            Normal port operation, OC5[ABC] disconnected
0 1            Toggle OC5[ABC] on compare match
1 0            Clear OC5[ABC] on compare match (set output to low level)
1 1            Set OC5[ABC] on compare match (set output to high level)

Table 17-4 shows the COM5x<1:0> bit functionality when the WGM5<3:0> bits are set to the fast PWM mode.

Table 17-4. Compare Output Mode, Fast PWM

COM5[ABC]<1:0> Description
-------------- -----------
0 0            Normal port operation, OC5[ABC] disconnected
0 1            WGM1<3:0> = 14 or 15: Toggle OC1A on Compare Match, OC1B and OC1C disconnected (normal port operation). For all other WGM1 settings, normal port operation, OC1[ABC] disconnected
1 0            Clear OC5[ABC] on compare match, set OC5[ABC] at BOTTOM (non-inverting mode)
1 1            Set OC5[ABC] on compare match, clear OC5[ABC] at BOTTOM (inverting mode)

Note: A special case occurs when OCR5[ABC] equals TOP and COM5[ABC]1 is set. In this case the compare match is ignored, but the set or clear is done at BOTTOM. See "Fast PWM Mode" on page 150. for more details.

Table 17-5 shows the COM5x<1:0> bit functionality when the WGM5<3:0> bits are set to the phase correct and frequency correct PWM mode.
Table 17-5. Compare Output Mode, Phase Correct and Phase and Frequency Correct PWM

COM5[ABC]<1:0> Description
-------------- -----------
0 0            Normal port operation, OC5[ABC] disconnected
0 1            WGM1<3:0> =9 or 11: Toggle OC1A on Compare Match, OC1B and OC1C disconnected (normal port operation). For all other WGM1 settings, normal port operation, OC1[ABC] disconnected
1 0            Clear OC5[ABC] on compare match when up-counting Set OC5[ABC] on compare match when downcounting
1 1            Set OC5[ABC] on compare match when up-counting Clear OC5[ABC] on compare match when downcounting

Note: A special case occurs when OCR5[ABC] equals TOP and COM5[ABC]1 is set. See "Phase Correct PWM Mode" on page 152. for more details.
''',
							},
							'WGM51': {
								'slice': (1,), 'access': 'R/W', 'default': 0,
							},
							'WGM50': {
								'slice': (0,), 'access': 'R/W', 'default': 0,
							},
						},
				},
			'TCCR5B': {
					'address': 0x121, 'module': 'TimerCounter5',
					'default': 0,
					'description': '''Timer/Counter 5 Control Register B''',
					'bitfields': {
							'ICNC5': {
									'slice': (7,),
									'description': '''ICNC5: Input Capture Noise Canceler

Setting this bit (to one) activates the Input Capture Noise Canceler. When the Noise Canceler is activated, the input from the Input Capture Pin (ICP5) is filtered. The filter function requires four successive equal valued samples of the ICP5 pin for changing its output. The input capture is therefore delayed by four Oscillator cycles when the noise canceler is enabled.''',
								},
							'ICES5': {
									'slice': (6,),
									'description': '''Input Capture Edge Select

This bit selects which edge on the Input Capture Pin (ICP5) that is used to trigger a capture event. When the ICES5 bit is written to zero, a falling (negative) edge is used as trigger, and when the ICES5 bit is written to one, a rising (positive) edge will trigger the capture.

When a capture is triggered according to the ICES5 setting, the counter value is copied into the Input Capture Register (ICR5). The event will also set the Input Capture Flag (ICF5), and this can be used to cause an Input Capture Interrupt, if this interrupt is enabled.

When the ICR5 is used as TOP value (see description of the WGM5<3:0> bits located in the TCCR5A and the TCCR5B Register), the ICP5 is disconnected and consequently the input capture function is disabled.''',
								},
							'WGM53': {
									'slice': (4,),
									'description': '''Waveform Generation Mode bit 3

See TCCRnA register description''',
								},
							'WGM52': {
									'slice': (3,),
									'description': '''Waveform Generation Mode bit 2

See TCCRnA register description''',
								},
							'WGM5_32': {
									'slice': (4,3),
									'description': '''Waveform Generation Mode bits 3:2'''
								},
							'CS5_20': {
									'slice': (2,0),
									'description': '''Clock Select

The three clock select bits select the clock source to be used by the Timer/Counter, see Figure 17-10 on page 156 and Figure 17-11 on page 156.

Table 17-6. Clock Select Bit Description

CS5<2:0> Description
-------- -----------
0 0 0     No clock source. (Timer/Counter stopped)
0 0 1     clkI/O/1 (No prescaling)
0 1 0     clkI/O/8 (From prescaler)
0 1 1     clkI/O/64 (From prescaler)
1 0 0     clkI/O/256 (From prescaler)
1 0 1     clkI/O/1024 (From prescaler)
1 1 0     External clock source on Tn pin. Clock on falling edge
1 1 1     External clock source on Tn pin. Clock on rising edge

If external pin modes are used for the Timer/Countern, transitions on the Tn pin will clock the counter even if the pin is configured as an output. This feature allows software control of the counting.''',
								},
						},
				},
			'TCCR5C': {
					'address': 0x122, 'module': 'TimerCounter5',
					'description': '''Timer/Counter 5 Control Register C

The FOC5[ABC] bits are only active when the WGM5<3:0> bits specifies a non-PWM mode. When writing a logical one to the FOC5[ABC] bit, an immediate compare match is forced on the waveform generation unit. The OC5[ABC] output is changed according to its COM5x<1:0> bits setting. Note that the FOC5[ABC] bits are implemented as strobes. Therefore it is the value present in the COM5x<1:0> bits that determine the effect of the forced compare.

A FOC5[ABC] strobe will not generate any interrupt nor will it clear the timer in Clear Timer on Compare Match (CTC) mode using OCR5A as TOP.

The FOC5[ABC] bits are always read as zero.''',

					'bitfields': {
							'FOC5A': {
									'slice': (7,), 'access': 'W', 'default': 0,
									'description': '''Force Output Compare for Channel A''',
								},
							'FOC5B': {
									'slice': (6,), 'access': 'W', 'default': 0,
									'description': '''Force Output Compare for Channel B''',
								},
							'FOC5C': {
									'slice': (5,), 'access': 'W', 'default': 0,
									'description': '''Force Output Compare for Channel C''',
								},
						},
				},
			'TCNT5L': {
					'address': 0x124,
					'module': 'TimerCounter5',
					'description': '''Timer/Counter 5 low byte

The two Timer/Counter I/O locations (TCNT5H and TCNT5L, combined TCNT5) give direct access, both for read and for write operations, to the Timer/Counter unit 16-bit counter. To ensure that both the high and low bytes are read and written simultaneously when the CPU accesses these registers, the access is performed using an 8-bit temporary High Byte Register (TEMP). This temporary register is shared by all the other 16-bit registers. See "Accessing 16-bit Registers" on page 138.

Modifying the counter (TCNT5) while the counter is running introduces a risk of missing a compare match between TCNT5 and one of the OCR5x Registers.

Writing to the TCNT5 Register blocks (removes) the compare match on the following timer clock for all compare units.''',
				},
			'TCNT5H': {
					'address': 0x125, 'module': 'TimerCounter5',
					'description': '''Timer/Counter 5 high byte

The two Timer/Counter I/O locations (TCNT5H and TCNT5L, combined TCNT5) give direct access, both for read and for write operations, to the Timer/Counter unit 16-bit counter. To ensure that both the high and low bytes are read and written simultaneously when the CPU accesses these registers, the access is performed using an 8-bit temporary High Byte Register (TEMP). This temporary register is shared by all the other 16-bit registers. See "Accessing 16-bit Registers" on page 138.

Modifying the counter (TCNT5) while the counter is running introduces a risk of missing a compare match between TCNT5 and one of the OCR5x Registers.

Writing to the TCNT5 Register blocks (removes) the compare match on the following timer clock for all compare units.''',
				},
			'ICR5L': {
					'address': 0x126, 'module': 'TimerCounter5',
					'description': '''Input Capture Register 5 low byte

The Input Capture is updated with the counter (TCNT5) value each time an event occurs on the ICP5 pin (or optionally on the Analog Comparator output for Timer/Counter5). The Input Capture can be used for defining the counter TOP value.

The Input Capture Register is 16-bit in size. To ensure that both the high and low bytes are read simultaneously when the CPU accesses these registers, the access is performed using an 8-bit temporary High Byte Register (TEMP). This temporary register is shared by all the other 16-bit registers. See "Accessing 16-bit Registers" on page 138.''',
				},
			'ICR5H': {
					'address': 0x127, 'module': 'TimerCounter5',
					'description': '''Input Capture Register 5 high byte

The Input Capture is updated with the counter (TCNT5) value each time an event occurs on the ICP5 pin (or optionally on the Analog Comparator output for Timer/Counter5). The Input Capture can be used for defining the counter TOP value.

The Input Capture Register is 16-bit in size. To ensure that both the high and low bytes are read simultaneously when the CPU accesses these registers, the access is performed using an 8-bit temporary High Byte Register (TEMP). This temporary register is shared by all the other 16-bit registers. See "Accessing 16-bit Registers" on page 138.''',
				},
			'OCR5AL': {
					'address': 0x128, 'module': 'TimerCounter5',
					'description': '''Output Compare Register 5 A low byte''',
				},
			'OCR5AH': {
					'address': 0x129, 'module': 'TimerCounter5',
					'description': '''Output Compare Register 5 A high byte''',
				},
			'OCR5BL': {
					'address': 0x12A, 'module': 'TimerCounter5',
					'description': '''Output Compare Register 5 B low byte''',
				},
			'OCR5BH': {
					'address': 0x12B, 'module': 'TimerCounter5',
					'description': '''Output Compare Register 5 B high byte''',
				},
			'OCR5CL': {
					'address': 0x12C, 'module': 'TimerCounter5',
					'description': '''Output Compare Register 5 C low byte''',
				},
			'OCR5CH': {
					'address': 0x12D, 'module': 'TimerCounter5',
					'description': '''Output Compare Register 5 C high byte

The Output Compare Registers contain a 16-bit value that is continuously compared with the counter value (TCNT5). A match can be used to generate an Output Compare interrupt, or to generate a waveform output on the OC5x pin.

The Output Compare Registers are 16-bit in size. To ensure that both the high and low bytes are written simultaneously when the CPU writes to these registers, the access is performed using an 8-bit temporary High Byte Register (TEMP). This temporary register is shared by all the other 16-bit registers. See "Accessing 16-bit Registers" on page 138.''',
				},
			'UCSR3A': {
					'address': 0x130, 'module': 'USART',
					'description': '''USART Control and Status Register A''',
					'bitfields': {
							'RXC3': {
									'slice': (7,),
									'description': '''USART Receive Complete

This flag bit is set when there are unread data in the receive buffer and cleared when the receive buffer is empty (that is, does not contain any unread data). If the Receiver is disabled, the receive buffer will be flushed and consequently the RXC3 bit will become zero.  The RXC3 Flag can be used to generate a Receive Complete interrupt (see description of the RXCIE3 bit).''',
								},
							'TXC3': {
									'slice': (6,),
									'description': '''USART Transmit Complete

This flag bit is set when the entire frame in the Transmit Shift Register has been shifted out and there are no new data currently present in the transmit buffer (UDR3). The TXC3 Flag bit is automatically cleared when a transmit complete interrupt is executed, or it can be cleared by writing a one to its bit location. The TXC3 Flag can generate a Transmit Complete interrupt (see description of the TXCIE3 bit).''',
								},
							'UDRE3': {
									'slice': (5,),
									'description': '''USART Data Register Empty

The UDRE3 Flag indicates if the transmit buffer (UDR3) is ready to receive new data. If UDRE3 is one, the buffer is empty, and therefore ready to be written. The UDRE3 Flag can generate a Data Register Empty interrupt (see description of the UDRIE3 bit).

UDRE3 is set after a reset to indicate that the Transmitter is ready.''',
								},
							'FE3': {
									'slice': (4,),
									'description': '''Frame Error

This bit is set if the next character in the receive buffer had a Frame Error when received, that is, when the first stop bit of the next character in the receive buffer is zero. This bit is valid until the receive buffer (UDR3) is read. The FE3 bit is zero when the stop bit of received data is one. Always set this bit to zero when writing to UCSR3A.''',
								},
							'DOR3': {
									'slice': (3,),
									'description': '''Data OverRun

This bit is set if a Data OverRun condition is detected. A Data OverRun occurs when the receive buffer is full (two characters), it is a new character waiting in the Receive Shift Register, and a new start bit is detected. This bit is valid until the receive buffer (UDR3) is read. Always set this bit to zero when writing to UCSR3A.''',
								},
							'UPE3': {
									'slice': (2,),
									'description': '''USART Parity Error

This bit is set if the next character in the receive buffer had a Parity Error when received and the Parity Checking was enabled at that point (UPM31 = 1). This bit is valid until the receive buffer (UDR3) is read. Always set this bit to zero when writing to UCSR3A.''',
								},
							'U2X3': {
									'slice': (1,),
									'description': '''Double the USART Transmission Speed

This bit only has effect for the asynchronous operation. Write this bit to zero when using synchronous operation.

Writing this bit to one will reduce the divisor of the baud rate divider from 16 to 8 effectively doubling the transfer rate for asynchronous communication.''',
								},
							'MPCM3': {
									'slice': (0,),
									'description': '''Multi-processor Communication Mode

This bit enables the Multi-processor Communication mode. When the MPCM3 bit is written to one, all the incoming frames received by the USART Receiver that do not contain address information will be ignored. The Transmitter is unaffected by the MPCM3 setting. For more detailed information see "Multi-processor Communication Mode" on page 221.''',
								},
						},
				},
			'UCSR3B': {
					'address': 0x131, 'module': 'USART',
					'description': '''USART Control and Status Register 3 B''',
					'bitfields': {
							'RXCIE3': {
									'slice': (7,),
									'description': '''RX Complete Interrupt Enable 3

Writing this bit to one enables interrupt on the RXC3 Flag. A USART Receive Complete interrupt will be generated only if the RXCIE3 bit is written to one, the Global Interrupt Flag in SREG is written to one and the RXC3 bit in UCSR3A is set.''',
								},
							'TXCIE3': {
									'slice': (6,),
									'description': '''TX Complete Interrupt Enable 3

Writing this bit to one enables interrupt on the TXC3 Flag. A USART Transmit Complete interrupt will be generated only if the TXCIE3 bit is written to one, the Global Interrupt Flag in SREG is written to one and the TXC3 bit in UCSR3A is set.''',
								},
							'UDRIE3': {
									'slice': (5,),
									'description': '''USART Data Register Empty Interrupt Enable 3

Writing this bit to one enables interrupt on the UDRE3 Flag. A Data Register Empty interrupt will be generated only if the UDRIE3 bit is written to one, the Global Interrupt Flag in SREG is written to one and the UDRE3 bit in UCSR3A is set.''',
								},
							'RXEN3': {
									'slice': (4,),
									'description': '''Receiver Enable 3

Writing this bit to one enables the USART Receiver.  The Receiver will override normal port operation for the RxD3 pin when enabled. Disabling the Receiver will flush the receive buffer invalidating the FE3, DOR3, and UPE3 Flags.''',
								},
							'TXEN3': {
									'slice': (3,),
									'description': '''Transmitter Enable 3

Writing this bit to one enables the USART Transmitter. The Transmitter will override normal port operation for the TxD3 pin when enabled. The disabling of the Transmitter (writing TXEN3 to zero) will not become effective until ongoing and pending transmissions are completed, that is, when the Transmit Shift Register and Transmit Buffer Register do not contain data to be transmitted. When disabled, the Transmitter will no longer override the TxD3 port.''',
								},
							'UCSZ32': {
									'slice': (2,),
									'description': '''Character Size 3

The UCSZ32 bits combined with the UCSZ3<1:0> bit in UCSR3C sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.''',
								},
							'RXB83': {
									'slice': (1,),
									'description': '''Receive Data Bit 8 3

RXB83 is the ninth data bit of the received character when operating with serial frames with nine data bits. Must be read before reading the low bits from UDR3.''',
								},
							'TXB83': {
									'slice': (0,),
									'description': '''Transmit Data Bit 8 3

TXB83 is the ninth data bit in the character to be transmitted when operating with serial frames with nine data bits. Must be written before writing the low bits to UDR3.''',
								},
						},
				},
			'UCSR3C': {
					'address': 0x132, 'module': 'USART',
					'description': '''USART Control and Status Register 3 C''',
					'bitfields': {
							'UMSEL3': {
									'slice': (7,6),
									'description': '''USART Mode Select

These bits select the mode of operation of the USART3 as shown in Table 22-4.

Table 22-4. UMSEL3 Bits Settings

UMSEL3<1:0> Mode
----------- ---
0 0         Asynchronous USART
0 1         Synchronous USART
1 0         (Reserved)
1 1         Master SPI (MSPIM)(1)

Note: 1. See "USART in SPI Mode" on page 232 for full description of the Master SPI Mode (MSPIM) operation.
''',
								},
							'UPM3': {
									'slice': (5,4),
									'description': '''Parity Mode

These bits enable and set type of parity generation and check. If enabled, the Transmitter will automatically generate and send the parity of the transmitted data bits within each frame. The Receiver will generate a parity value for the incoming data and compare it to the UPM3 setting. If a mismatch is detected, the UPE3 Flag in UCSR3A will be set.

Table 22-5. UPM3 Bits Settings

UPM3<1:0> Parity Mode
--------- -----------
0 0       Disabled
0 1       Reserved
1 0       Enabled, Even Parity
1 1       Enabled, Odd Parity
''',
								},
							'USBS3': {
									'slice': (3,),
									'description': '''Stop Bit Select

This bit selects the number of stop bits to be inserted by the Transmitter. The Receiver ignores this setting.

Table 22-6. USBS Bit Settings

USBS3 Stop Bit(s)
----- -----------
0     1-bit
1     2-bit
''',
								},
							'UCSZ3': {
									'slice': (2,1),
									'description': '''Character Size

The UCSZ3<1:0> bits combined with the UCSZ32 bit in UCSR3B sets the number of data bits (Character SiZe) in a frame the Receiver and Transmitter use.

Table 22-7. UCSZ3 Bits Settings

UCSZ3<2:0> Character Size
---------- --------------
0 0 0      5-bit
0 0 1      6-bit
0 1 0      7-bit
0 1 1      8-bit
1 0 0      Reserved
1 0 1      Reserved
1 1 0      Reserved
1 1 1      9-bit
''',
								},
							'UCPOL3': {
									'slice': (0,),
									'description': '''Clock Polarity

This bit is used for synchronous mode only. Write this bit to zero when asynchronous mode is used. The UCPOL3 bit sets the relationship between data output change and data input sample, and the synchronous clock (XCK3).

Table 22-8.  UCPOL3 Bit Settings

UCPOL3 Transmitted Data Changed Received Data Sampled 
       (Output of TxD3 Pin)     (Input on RxD3 Pin)
------ ------------------------ ---------------------
0       Rising XCK3 Edge         Falling XCK3 Edge
1       Falling XCK3 Edge        Rising XCK3 Edge
''',
								},
						},
				},
			'UBRR3L': {
					'address': 0x134, 'module': 'USART',
					'description': '''USART Baud Rate Register low byte

This is the low byte of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UBRR3H': {
					'address': 0x135, 'module': 'USART',
					'description': '''USART Baud Rate Register high byte

This is the high nibble of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
			'UDR3': {
					'address': 0x136, 'module': 'USART',
					'description': '''USART Baud Rate Register low byte

This is the low byte of a 12-bit register which contains the USART baud rate. The UBRRH contains the four most significant bits and the UBRRL contains the eight least significant bits of the USART baud rate. Ongoing transmissions by the Transmitter and Receiver will be corrupted if the baud rate is changed. Writing UBRRL will trigger an immediate update of the baud rate prescaler.''',
				},
		} # SFR


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
		if ATMEGA2560SFR._SFR.has_key(sfrName):
			defn = copy.deepcopy(ATMEGA2560SFR._SFR[sfrName])
		elif ATMEGA2560SFR._XREG.has_key(sfrName):
			defn = copy.deepcopy(ATMEGA2560SFR._XREG[sfrName])
		else:
			raise NameError(sfrName)
		self.__dict__['_name']        = sfrName
		self.__dict__['_defn']        = defn
		self.__dict__['_address']     = defn['address']
		self.__dict__['_module']      = defn['module']
		self.__dict__['_description'] = defn['module']
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
			if not isinstance(val, int):  # (type(val) != type(0)):
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
		Assumption: per http://msoe.us/taylor/tutorial/ce2810/candasm
		8-bit: R24
		16-bit: R25:24
		32-bit: R25:22
		64-bit: R25:18
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
			# since AVR has very similar instructions for rotate and swap
			# and shift, we just map the code from 8051 version to AVR.
			if (p == 0):
				pass  # nothing to do. the result is ready.
			elif (p == 1):
				self._emit('LSR R24')  # shifting right
			elif (p == 2):
				self._emit('LSR R24')
				self._emit('LSR R24')  # shifting right twice
			elif (p == 3):
				self._emit('LSR R24')
				self._emit('LSR R24')
				self._emit('LSR R24')  # shifting right three times
			elif (p == 4):
				self._emit('SWAP R24')  # swap is shift by 4 positions
			elif (p == 5):
				self._emit('SWAP R24')
				self._emit('LSR R24')    # 4 positions + 1
			elif (p == 6):
				self._emit('SWAP R24')
				self._emit('LSR R24')    # >> 6 is swap and right twice
				self._emit('LSR R24')
			elif (p == 7):
				self._emit('ROR R24')
				self._emit('ROR R24')   # shift 7 is rotate-thru-carry twice!
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
		print "-----------writeSFR--------" + str(value) + "-------------------"
		if value is None:
			return
		if isinstance(value, CodeCapsule):
			self._code = value
		else:
			self._code = CodeCapsule(self._mcu, dest=self, src=self)
		# TODONR: handle VAR later
		# if (isinstance(value, SFR)) \
		# 		or (isinstance(value, atmega2560var.VAR)) \
		# 		or isinstance(value, CodeCapsule):
		if (isinstance(value, SFR)):
			self._emit('((*(uint8_t *)%d) = %s)', self._address, value._loadByte(value._address))
		elif (isinstance(value, CodeCapsule)):
			self._emit('((*(uint8_t *)%d) = %s)', self._address, value.getCode())
		elif isinstance(value, int) or isinstance(value, str):
			if isinstance(value, str):
				if len(value) == 0:
					value = 0
				elif len(value) == 1:
					value = ord(value)
				else:
					raise ValueError('Cannot assign string %s to SFR %s' % (value,
						self._name))
			self._emit('((*(uint8_t *)%d) = %s)', self._address, value)
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
					dest=self._mcu.lookupVar('R24'))  # outlet is assumed to be R24
			# special handling: as bit index
			bitindex = int(name[1])
			return self._readBit(self._address, bitindex)
		else:
			self._code = CodeCapsule(self._mcu, src=self,
					dest=self._mcu.lookupVar('R24'))  # outlet is assumed to be accumulator?

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
			self._emit('LSR R24')  # shifting right
		elif (p == 2):
			self._emit('LSR R24')
			self._emit('LSR R24')  # shifting right twice 
		elif (p == 3):
			self._emit('LSR R24')
			self._emit('LSR R24')
			self._emit('LSR R24')    # shift right 3 times
		elif (p == 4):
			self._emit('SWAP R24')  # swap is shift by 4 positions
		elif (p == 5):
			self._emit('SWAP R24')
			self._emit('LSR R24')    # 4 positions + 1
		elif (p == 6):
			self._emit('SWAP R24')
			self._emit('LSR R24')    # 4 positions + 2
			self._emit('LSR R24')
		elif (p == 7):
			self._emit('ROL R24')    # rotate thru carry twice
			self._emit('ROL R24')
		# self._A = (self._value & mask) >> p
		return self._code

	def _emit(self, formatStr, *operands):
		self._code.emit(formatStr, *operands)

#	def _loadBit(self, bitAddress):
# We don't use _loadBit because unlike 8051, AVR does not have a
# bit-addressable memory space.
#		self._emit('MOV C, 0x%x', bitAddress)
#		# self._C = (self._value >> (bitAddress & 0x7) ) & 1
#		self._code.setResultType('bool')
#		return self._code

	def _writeBit(self, address, bitindex, value):
		'''
			use either setb or clr if bit addressable,
			or use AND/OR trick
		'''
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
		else: # assume bit is in T
			# use the Rotate-through-C trick!
			self._loadByte(self._address)
			self._emit('BST R24, %d', bitindex)
			self._storeByte(self)
			return self._code


	def _readBit(self, address, bitindex):
		'''read a whole SFR into a register and access its bit 
		  and put it into T register
		'''
		self._loadByte(self._address) # this does it to memory with MOV
		return self._extractBit(bitindex)  # save in bit accumulator C


	def _loadByte(self, address):
		'''This generates the LD instruction to move in a byte if SFR
		   is above 0x5f,
		   or use IN if <= 0x5f.
		'''
		self._emit('(*(uint8_t *)%d)' % address)
		return self._code

	def _AorByte(self, mask):
		'''This generates ORI code to and R24 with a mask, put back to R24.
		   This does not overwrite the result, as it is only temporary
			 variable.
		'''
		self._emit('ORI R%d, 0x%x', 24, mask)
		# self._A |= mask
		return self._code

	def _AandByte(self, mask):
		'''This generates ANDI code to and R24 with a mask, put back to R24.
		   This does not overwrite the result, as it is only temporary
			 variable.
		'''
		self._emit('ANDI R%d, 0x%x', 24, mask)
		# self._A &= mask
		return self._code

	def _SFRorByte(self, mask):
		'''This generates ORL code to OR SFR with a mask and put back to
		SFR.'''
		self._loadByte(self._address)
		self._AorByte(mask)
		self._emit('ST X, R24')  # no need to change DPTR address!
		return self._code

	def _SFRandByte(self, mask):
		'''This generates ANL code to and SFR with a mask and put back to
		SFR.'''
		self._loadByte(self._address)
		self._AandByte(mask)
		self._emit('ST X, R24')  # no need to change DPTR address!
		return self._code

	def _SFRandOrByte(self, maskN, mask):
		'''The value to assign is in R24 (AVR's "accumulator").
		   but we need to construct a mask that we can AND in to the
			 target.  So, we do A |= maskN  (maskN is the unchanged bits)
			 save A into temp, then load target byte into A,
			 A |= mask, then A &= temp.
			 finally, write back. avoid unnecessary reloading.
		'''
		self._AorByte(maskN)  # make mask of bits to clear in A
		temp = self._code.allocTemp()
		self._emit('MOV R%d, R24', temp.varAddress())  # Save A into R0 as temporary
		self._loadByte(self._address)
		self._AorByte(mask)  # turn on all bits affected
		self._emit('AND R24, R%d', temp.varAddress()) # clear affected bits
		self._storeByte()  # no need to change DPTR address!
		elf._code.freeTemp(temp)
		return self._code

	def _extractBit(self, bitindex):
		'''This puts the R24.index bit into T'''
		self._emit('BST R24, %d', bitindex)
		self._code.setResultType('bool')
		# self._C = (self._A >> bitindex) & 1
		return self._code

	def readSFR(self, dest=None):
		'''This is called by the mcu.SFR to generate instructions to
		   load from SFR as a byte.
		'''
		if dest is None: dest = self._mcu.lookupVar('R24')
		self._code = CodeCapsule(self._mcu, src=self,
				dest=dest)
		self._code.setResultType('uint8')
		return self._loadByte(self._address)

	def _storeByte(self):
		'''This is the outside routine to write value in R24 (like A)
		   into this SFR (by OUT or ST instruction).
			 It is used ONLY after the address has already been set (in X),
			 so we don't have to load the address again.
		'''
		address = self._address
		if (address <= 0x5f):
			self._emit('OUT R24, 0x%x', address - 0x20)
		else:
			self._emit('ST R24, X', address)
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
	c = ATMEGA2560SFR()
	c.sanityCheck()