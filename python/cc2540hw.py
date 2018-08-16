"""
   This is an attempt to model the CC2540 built-in features with the
	 goals of
	 - introspection of MCU's resource and how they are modeled
	 - interactive execution of instructions
	 - digital simulation .

	 However... don't try this yet, because there are many issues
	 involved.  I don't know if I understand the problem enough for this
	 to work.  it will take more time.

	 The idea here is to model enough of the hardware resources and the
	 connectivity, so that one can infer the necessary settings or
	 allowed resource sharing (e.g., sharing GPIO pins)
"""

class CC2540:
	# common description of pins across all instances of CC2540. should
	# be read-only.
	_pin = {
			'AVDD1':  { 'pinNum': 28, 'type': 'APwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V analog power-supply connection'},
			'AVDD2':  { 'pinNum': 27, 'type': 'APwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V analog power-supply connection'},
			'AVDD3':  { 'pinNum': 24, 'type': 'APwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V analog power-supply connection'},
			'AVDD4':  { 'pinNum': 29, 'type': 'APwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V analog power-supply connection'},
			'AVDD5':  { 'pinNum': 21, 'type': 'APwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V analog power-supply connection'},
			'AVDD6':  { 'pinNum': 31, 'type': 'APwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V analog power-supply connection'},
			'DCOUPL': { 'pinNum': 40, 'type': 'DPwr', 'Volt': (1.8, 'V'),
				'description': '1.8V digital power-supply decoupling. Do not use for supplying external circuits'},
			'DGND_USB': { 'pinNum': 1, 'type': 'Gnd',
				'description': 'Connect to GND'},
			'DVDD_USB': { 'pinNum': 4, 'type': 'DPwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V digital power-supply connection'},
			'DVDD1': { 'pinNum': 39, 'type': 'DPwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V digital power-supply connection'},
			'DVDD2': { 'pinNum': 10, 'type': 'DPwr',
				'Vmin': (2, 'V'), 'Vmax': (3.6, 'V'),
				'description': '2-3.6V digital power-supply connection'},
			'GND': { 'pinNum': 'pad', 'type': 'Gnd',
				'description': 'The ground pad must be connected to a solid ground plane'},

				'P0_0': { 'pinNum': 19, 'type': 'DIO', 'description': 'Port 0.0'},
				'P0_1': { 'pinNum': 18, 'type': 'DIO', 'description': 'Port 0.1'},
				'P0_2': { 'pinNum': 17, 'type': 'DIO', 'description': 'Port 0.2'},
				'P0_3': { 'pinNum': 16, 'type': 'DIO', 'description': 'Port 0.3'},
				'P0_4': { 'pinNum': 15, 'type': 'DIO', 'description': 'Port 0.4'},
				'P0_5': { 'pinNum': 14, 'type': 'DIO', 'description': 'Port 0.5'},
				'P0_6': { 'pinNum': 13, 'type': 'DIO', 'description': 'Port 0.6'},
				'P0_7': { 'pinNum': 12, 'type': 'DIO', 'description': 'Port 0.7'},

				'P1_0': { 'pinNum': 11, 'type': 'DIO', 'description': 'Port 1.0 -- 20mA drive capability'},
				'P1_1': { 'pinNum':  9, 'type': 'DIO', 'description': 'Port 1.1 -- 20mA drive capability'},
				'P1_2': { 'pinNum':  8, 'type': 'DIO', 'description': 'Port 1.2'},
				'P1_3': { 'pinNum':  7, 'type': 'DIO', 'description': 'Port 1.3'},
				'P1_4': { 'pinNum':  6, 'type': 'DIO', 'description': 'Port 1.4'},
				'P1_5': { 'pinNum':  5, 'type': 'DIO', 'description': 'Port 1.5'},
				'P1_6': { 'pinNum': 38, 'type': 'DIO', 'description': 'Port 1.6'},
				'P1_7': { 'pinNum': 37, 'type': 'DIO', 'description': 'Port 1.7'},

				'P2_0': { 'pinNum': 36, 'type': 'DIO', 'description': 'Port 2.0'},
				'P2_1': { 'pinNum': 35, 'type': 'DIO', 'description': 'Port 2.1'},
				'P2_2': { 'pinNum': 34, 'type': 'DIO', 'description': 'Port 2.2'},
				'P2_3': { 'pinNum': 33, 'type': ['DIO', 'AIO'],
					'description': 'Port 2.3'},
				'P2_4': { 'pinNum': 32, 'type': ['DIO', 'AIO'],
					'description': 'Port 2.4'},

				'RBIAS': { 'pinNum': 30, 'type': 'AIO' },
				'RESET_N': { 'pinNum':  20, 'type': 'DI',
						'description': 'Reset, active-low', 'polarity': 'low' },
				'RF_N': { 'pinNum': 26, 'type': 'RFIO',
						'description': 'Negative RF input signal to LNA during Rx; Negative RF output signal from PA during Tx' },
				'RF_P': { 'pinNum': 25, 'type': 'RFIO',
						'description': 'Positive RF input signal to LNA during Rx; Positive RF output signal from PA during Tx' },

				'USB_N': { 'pinNum': 3, 'type': 'DIO', 'description': 'USB N' },
				'USB_P': { 'pinNum': 2, 'type': 'DIO', 'description': 'USB P' },

				'XOSC_Q1': { 'pinNum': 22, 'type': 'AIO',
						'description': '32-MHz crystal oscillator pin 1 or external-clock input' },
				'XOSC_Q2': { 'pinNum': 23, 'type': 'AIO', 
						'description': '32-MHz crystal oscillator pin 2'},
				}

	_blocks = [
			'8051 CPU Core',
			'DMA',
			'IRQ Ctrl',
			'Debug Interface',
			'Analog Comparator',
			'Op-Amp',
			'Delta-Sigma ADC Audio/DC',
			'AES Encryption and Description',
			'USB',
			'USART0',
			'USART1',
			'Timer 1 (16-bit)',
			'Timer 2 (BLE LL Timer)',
			'Timer 3 (8-bit)',
			'Timer 4 (8-bit)',
			'Memory Arbiter',
			'Flash',
			'Flash Ctrl',
			'Radio Arbiter',
			'FIFOCTRL',
			'1 KB SRAM',
			'Radio Registers',
			'Link Layer Engine',
			'Demodulator',
			'Synth',
			'Modulator',
			'Receive',
			'Frequency Synthesizer',
			'Transmit',
			'Sleep Timer',
			'Power Management Controller',
			'On-Chip Voltage Regulator',
			'Power-on Reset Brown Out',
			'Clock MUX and Calibration',
			'Watchdog Timer',
			'Reset',
			'High-speed RC-OSC',
			'32-kHz RC-OSC',
			'32.768-kHz Crystal OSC',
			'32-kHz Crystal OSC',
			]


	def __init__(self, name):
		self._name = name

	def __setattr__(self, identifier):
		if 

