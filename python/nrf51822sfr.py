'''
	This is an attempt to model nRF51822 SFR in terms of memory load/store.
	This is simpler than 8051 beause there is just one address space.

	There are two levels of use: (1) read/write the register -- should
	be done in the context of MCU, (2) read/write a bit or slice.
	This file includes just SFR and can do (2).  To access in the
	context of MCU, load it from nrf51822mcu.py.

	Convention:
	R0: scalar values ("accumulator")
	R1: concatenated for 64-bit or temporary (other operand)
	R2: temporary (other operand)
	R3: pointer

'''
import nrf51822var
from cc_thumb import CC_Thumb as CodeCapsule # was codecapsule for CC2540
class nRF51822SFR:
	'''
		This class nRF51822SFR is just a container for one static hash
		table of hash tables of stuff to provide the SFR definitions.
		The data is taken from the data sheet "nRF51_Series_Reference_Manual_v2.1.pdf"

		The memory map looks like
		0x00000000: Code (nonvolatile)
		0x10000000: FICR factory-info config regs (read-only parameters, config details)
		       400: READY
					 504: CONFIG (configuration register)
					 508: ERASEPAGE (code region 1), aka ERASEPCR1
					 510: ERASEPCR0 (code region 0)
					 50C: ERASEALL (erase all nonvolatile user memory)
					 514: ERASEUICR (erase user info config reg)

		0x10001000: UICR (user-writable info block)
		0x20000000: RAM
		0x40000000: APB peripherals
		      0000: Power, Clock
					1000: Radio
					2000: UART0
					3000: SPI0, TWI0 (I2C)
					4000: SPI1, TWI1, SPIS (slave)
					6000: GPIOTE (T = task, E = event)
					7000: ADC
					8000: Timer0
					9000: Timer1
					A000: Timer2
					B000: RTC0
					C000: Temperature sensor
					D000: Random number generator
					E000: Crypto ECB
					F000: AES CCM mode encryption, accelerated CCM, accelerated addr resolver
				 10000: WDT (watchdog timer)
				 11000: RTC1
				 12000: QDEC
				 13000: LPCOMP (low-power comparator)
				 1E000: NVMC (nonvolatile memory controller)
				 1F000: PPI (programmable peripheral interconnect)

		0x50000000: AHB peripherals (GPIO)
		0xE0000000: Private Peripherals Bus
	'''
	_ModuleBase = {
			"POWER":  0x40000000,
			"CLOCK":  0x40000000,
			"RADIO":  0x40001000,
			"UART0":  0x40002000,
			"SPI0":   0x40003000,
			"TWI0":   0x40003000,
			"SPI1":   0x40004000,
			"TWI1":   0x40004000,
			"SPIS1":  0x40004000,
			"GPIOTE": 0x40006000,
			"ADC":    0x40007000,
			"TIMER0": 0x40008000,
			"TIMER1": 0x40009000,
			"TIMER2": 0x4000A000,
			"RTC0":   0x4000B000,
			"TEMP":   0x4000C000,
			"RNG":    0x4000D000,
			"ECB":    0x4000E000,
			"CCM":    0x4000F000,
			"AAR":    0x4000F000,
			"WDT":    0x40010000,
			"RTC1":   0x40011000,
			"QDEC":   0x40012000,
			"LPCOMP": 0x40013000,
			"NVMC":   0x4001E000,
			"PPI":    0x4001F000,
			"P0":     0x50000000,
			"FICR":   0x10000000,
			"UICR":   0x10001000,
		}

	_SFR = {
			################ Nonvolatile memory controller ##############
			'NVMC_READY': {
					'address': 0x4001E400, 'module': 'NVMC',
					'default': 0, 'access': 'R',
					'description': '''Ready flag.
0: busy
1: ready''',
				},
			'NVMC_CONFIG': {
					'address': 0x4001E504, 'module': 'NVMC',
					'description': 'Configuration register',
					'bitfields': {
							'WEN': {
									'slice': (1,0), 'default': 0, 'access': 'R/W',
									'description': '''Program memory access mode. It is
									strongly recommended to only active erase and write modes
									when they are actively used.
00: (REN) Read-only access.
01: (WEN) Write-enabled.
10: (EEN) Erase enabled.
''',
							},
						},
					},
			'NVMC_ERASEPCR1': {
					'address': 0x4001E508, 'module': 'NVMC',
					'description': '''Register for erasing a page in code region 1.  Equivalent to ERASEPAGE.  The value is the address of the page to be erased (addresses of first word in page). Note that code erase must be enabled by CONFIG.EEN before any pages in code region 1 can be erased.
					
See product specification for information about the total code size of the device you are using. Attempts to erase pages that are outside the code area may result in undesirable behavior, for example, the wrong page may be
erased.''',
				},
			'NVMC_ERASEPCR0': {
					'address': 0x4001E510, 'module': 'NVMC',
					'default': 0, 'access': 'R/W',
					'description': '''Register for erasing a page in code region 0.  The value is the address of the page to be erased (addresses of first word in page). Only page addresses in code region 0 are allowed.  This register can only be accessed from a program running in code memory region 0. A hard fault will be generated if the register is attempted accessed from a program in RAM or code memory region 1. = Writing to ERASEPCR0 from the Serial Wire Debug (SWD) will have no effect.  CONFIG.EEN has to be set to enable erase.

See product specification for information about the total code size of the device you are using. Attempts to erase pages that are outside the code area may result in undesirable behavior, for example, the wrong page may be erased.''',
				},
			'NVMC_ERASEALL': {
					'address': 0x4001E50C, 'module': 'NVMC',
					'default': 0, 'access': 'R/W',
					'description': '''Erase all non-volatile memory including UICR registers. Code erase has to be enabled by CONFIG.EEN before the nonvolatile memory can be erased. Note: FICR is not erased.

0: No operation.
1: Start chip erase.''',
				},
			'NVMC_ERASEUICR': {
					'address': 0x4001E514, 'module': 'NVMC',
					'default': 0, 'access': 'R',
					'description': '''Register for erasing User Information Configuration Registers.

0: NVMC is busy (on-going write or erase operation).
1: NVMC is ready.
'''
				},
			'FICR_CODEPAGESIZE': {
					'address': 0x10000010, 'module': 'FICR',
					'default': 0xFFFFFFFF, 'access': 'R',
					'description': '''Code memory page size in bytes.''',
				},
			'FICR_CODESIZE': {
					'address': 0x10000014, 'module': 'FICR',
					'default': 0xFFFFFFFF, 'access': 'R',
					'description':'''Code memory size in number of pages. Total code space is: CODEPAGESIZE * CODESIZE''',
				},
			'FICR_CLENR0': {
					'address': 0x10000028, 'module': 'AES',
					'default': 0xFFFFFFFF, 'access': 'R',
					'description':'''Length of code region 0 in bytes.  The value must be multiple of "code page size" bytes (FICR.CODEPAGESIZE). This register is only used when pre-programmed factory code is present on the chip, see PPFC.

N (max value) is (FICR.CODEPAGESIZE*FICR.CODESIZE-1, but not larger than 255.  This register can only be written if content is 0xFFFFFFFF.

0xFFFFFFFF: Value if there is no pre-programmed code in the chip. Interpreted as 0.''',
				},
			'FICR_PPFC': {
					'address': 0x1000002C, 'module': 'FICR',
					'description':'Pre-programmed factory code present',
					'default': 0xFFFFFFFF, 'access': 'R',
					'bitfields': {
							'ADDR': {
									'slice': (7,0), 'default': 0xFFFFFFFF, 'access': 'R',
									'description': '''0x00: Present
0xFF: Not present.''',
							},
						},
					},
			'FICR_NUMRAMBLOCK': {
					'address': 0x10000034, 'module': 'FICR',
					'description': '''Number of individually controllable RAM blocks.''',
					'default': 0xFFFFFFFF, 'access': 'R',
				},
			'FICR_SIZERAMBLOCK0': {
					'address': 0x10000038, 'module': 'FICR',
					'description': 'Size of RAM block 0 in bytes',
					'default': 0xFFFFFFFF, 'access': 'R',
				},
			'FICR_SIZERAMBLOCK1': {
					'address': 0x1000003C, 'module': 'FICR',
					'description': 'Size of RAM block 1 in bytes',
					'default': 0xFFFFFFFF, 'access': 'R',
				},
			'FICR_SIZERAMBLOCK2': {
					'address': 0x10000040, 'module': 'FICR',
					'description': 'Size of RAM block 2 in bytes',
					'default': 0xFFFFFFFF, 'access': 'R',
				},
			'FICR_SIZERAMBLOCK3': {
					'address': 0x10000044, 'module': 'FICR',
					'description': 'Size of RAM block 3 in bytes',
					'default': 0xFFFFFFFF, 'access': 'R',
				},


			'FICR_CONFIGID': {
					'address': 0x1000005C, 'module': 'FICR',
					'description': 'Configuration Identifier',
					'bitfields': {
							'HWID': {
									'slice': (15,0), 'default': 0xFFFF, 'access': 'R',
									'description': 'Identification number for the HW',
							},
							'FICR_FWID': {
									'slice': (31,16), 'default': 0xFFFF, 'access': 'R',
									'description': 'Identification number for the firmware that is pre-loaded into the chip.',
							},
					},
				},

			'FICR_DEVICEID0': {
					'address': 0x10000060, 'module': 'FICR',
					'description': 'Device identifier, bit 31-0, unique for each unit',
					'default': 0xFFFFFFFF, 'access': 'R',
				},
			'FICR_DEVICEID1': {
					'address': 0x10000064, 'module': 'FICR',
					'description': 'Device identifier, bit 63-32, unique for each unit',
					'default': 0xFFFFFFFF, 'access': 'R',
				},

			'FICR_ER0': {
					'address': 0x10000080, 'module': 'FICR',
					'description': 'Encryption root, bit 31-0', 'access': 'R',
					'default': 0xFFFFFFFF,
				},
			'FICR_ER1': {
					'address': 0x10000084, 'module': 'FICR',
					'description': 'Encryption root, bit 63-32', 'access': 'R',
					'default': 0xFFFFFFFF,
				},
			'FICR_ER2': {
					'address': 0x10000088, 'module': 'FICR',
					'description': 'Encryption root, bit 95-64', 'access': 'R',
					'default': 0xFFFFFFFF,
				},
			'FICR_ER3': {
					'address': 0x1000008C, 'module': 'FICR',
					'description': 'Encryption root, bit 127-96', 'access': 'R',
					'default': 0xFFFFFFFF,
				},

			'FICR_IR0': {
					'address': 0x10000090, 'module': 'FIRC',
					'description': 'Identity root, bit 31-0',
					'access': 'R', 'default': 0xFFFFFFFF,
				},
			'FICR_IR1': {
					'address': 0x10000094, 'module': 'FIRC',
					'description': 'Identity root, bit 63-32',
					'access': 'R', 'default': 0xFFFFFFFF,
				},
			'FICR_IR2': {
					'address': 0x10000098, 'module': 'FIRC',
					'description': 'Identity root, bit 95-64',
					'access': 'R', 'default': 0xFFFFFFFF,
				},
			'FICR_IR3': {
					'address': 0x10000099, 'module': 'FIRC',
					'description': 'Identity root, bit 127-96',
					'access': 'R', 'default': 0xFFFFFFFF,
				},

			'FICR_DEVICEADDRTYPE': {
					'address': 0x100000A04, 'module': 'FICR',
					'default': 0xFFFFFFFF, 'access': 'R',
					'description': '''Device address type.
0: Public
1: Random''',
				},
			
			'FICR_DEVICEADDR0': {
					'address': 0x100000A4, 'module': 'FICR',
					'description': 'Device address bit 31-0',
					'default': 0xFFFFFFFF, 'access': 'R',
				},
			'FICR_DEVICEADDR1': {
					'address': 0x100000A8, 'module': 'FICR',
					'description': 'Device address bit 47-32',
					'default': 0xFFFFFFFF, 'access': 'R',
					'bitfields': {
						'ADDR': {
								'slice': (15,0), 'description': 'Device address bit 47-32',
								'access': 'R/W', 'default': 0xFFFF,
							},
						},
				},
			'FICR_OVERRIDDEN': {
					'address': 0x100000AC, 'module': 'FICR',
					'description': 'Override enable',
					'default': 0xFFFFFFFF, 'access': 'R',
					'bitfields': {
							'NRF_1MBIT': {
								'slice': (0,),
								'access': 'R',
								'description': '''0: Override default value for NRF_1MBIT mode.
1: Use default value for NRF_1MBIT mode.''',
								},
							'BLE_1MBIT': {
									'slice': (3,),
									'access': 'R',
									'description': '''0: Override default value for BLE_1MBIT mode.
1: No override value for BLE_1MBIT mode available in FICR.''',
								},
						},
				},

			'FICR_NRF_1MBIT0': {
					'address': 0x100000B0, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[0] value for NRF_1MBIT mode',
				},
			'FICR_NRF_1MBIT1': {
					'address': 0x100000B4, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[1] value for NRF_1MBIT mode',
				},
			'FICR_NRF_1MBIT2': {
					'address': 0x100000B8, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[2] value for NRF_1MBIT mode',
				},
			'FICR_NRF_1MBIT3': {
					'address': 0x100000BC, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[3] value for NRF_1MBIT mode',
				},
			'FICR_NRF_1MBIT4': {
					'address': 0x100000C0, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[4] value for NRF_1MBIT mode',
				},

			'FICR_BLE_1MBIT0': {
					'address': 0x100000EC, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[0] value for BLE_1MBIT mode',
				},
			'FICR_BLE_1MBIT1': {
					'address': 0x100000F0, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[1] value for BLE_1MBIT mode',
				},
			'FICR_BLE_1MBIT2': {
					'address': 0x100000F4, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[2] value for BLE_1MBIT mode',
				},
			'FICR_BLE_1MBIT3': {
					'address': 0x100000F8, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[3] value for BLE_1MBIT mode',
				},
			'FICR_BLE_1MBIT4': {
					'address': 0x100000FC, 'module': 'FICR', 'access': 'R',
					'description': 'RADIO.OVERRIDE[4] value for BLE_1MBIT mode',
				},
			########### UICR: User Information Configuration Registers #########
			'UICR_CLENR0': {
					'address': 0x10001000, 'module': 'UICR',
					'access': 'R/W',
					'description': '''Length of code region 0 in bytes [0..N]. The value must be a multiple of "code page size" bytes (FICR.CODEPAGESIZE).

N (max value) is (FICR.CODEPAGESIZE*FICR.CODESIZE-1), but not larger than 255.

This register can only be written if content if 0xFFFFFFFF.

This register is only used when pre-programmed factory code is not present on the chip, see PPFC in FCIR.''',
				},

			'UICR_RBPCONF': {
					'address': 0x10001004, 'module': 'UICR',
					'description': 'Read back protection configuration. More detail is given in Chapter 8.',
					'bitfields': {
							'PRO': {
									'slice': (7,0), 'access': 'R/W',
									'description': '''Readback protection code region 0. Will be ignored if programmed factory code is present on the chip.

0xFF: Disabled.
0x00: Enabled.''',
								},
							'PALL': {
									'slice': (15,8),
									'access': 'R/W',
									'description': '''Readback protect all code in device.
0xFF: Disabled.
0x00: Enabled.''',
								},
						},
				},
			'UICR_XTALFREQ': {
					'address': 0x10001008, 'access': 'R/W', 'module': 'UICR',
					'description': 'Reset value for XTALFREQ in clock, see Chapter 12 "Clock management (CLOCK)" on page 53.',
					'bitfields': {
							'XTALFREQ': {
									'slice': (7,0), 'access': 'R', 
									'description': '''0xFF: 16 MHz crystal is used.
0x00: 32 MHz crystal is used.''',
								},
						},
				},
			'UICR_FWID': {
					'address': 0x10001010, 'module': 'UICR',
					'description': 'Firmware ID',
					'bitfields': {
							'FWID': {
									'slice': (15,0), 'access': 'R', 
									'description': '''Identification number for the firmware loaded into the chip. This ID is used when the CONFIG.FWID in the FICR is set to 0xFFFF.''',
								},
						},
				},

			##################  MPU: Memory Protection Unit ###################
			### Section 8.2 lists additional SFRs, but it is not clear if
			### they are part of the NVMC or what??
			#### 4001E000:  NVMC (nonvolatile memory controller)
			### PERR0:      0x528: Definition of peripherals in memory region 0
			### RLENR0:     0x52C: Length of RAM region 0
			### PROTENSET0: 0x600: Protection bit enable set register
			### PROTENSET1: 0x604: Protection bit enable set register
			### DISABLEINDEBUG: 0x608: Disable protection mechanism in debug mode
			### 
			##################  marker for where stopped #######################
			'NVMC_PERR0': {
					'address': 0x4001E528, 'module': 'NVMC',
					'description': 'Definition of peripherals in memory region 0',
					'bitfields': {
							'POWER_CLOCK': {
								'slice': (0,), 'access': 'R/W',
									'description': '''Classify POWER and CLOCK and all other peripherals with ID=0, as region 0 or region 1 peripheral''',
								},
							'RADIO': {
									'slice': (1,), 'access': 'R/W',
									'description': 'CLassify RADIO as region 0 or region 1 peripheral',
								},
							'UART0': {
									'slice': (2,), 'access': 'R/W',
									'description': 'Classify UART0 as region 0 or region 1 peripheral',
								},
							'SPI0_TWI0': {
									'slice': (3,), 'access': 'R/W',
									'description': 'Classify SPI0 and TWI0 as region 0 or region 1 peripheral',
								},
							'SPI1_TWI1': {
									'slice': (4,), 'access': 'R/W',
									'description': 'Classify SPI1, SPIS1, and TWI1 as region 0 or region 1 peripheral',
								},
							'GPIOTE': {
									'slice': (6,), 'access': 'R/W',
									'description': 'Classify GPIOTE as region 0 or region 1 peripheral',
								},
							'ADC': {
									'slice': (7,), 'access': 'R/W',
									'description': 'Classify ADC as region 0 or region 1 peripheral',
								},
							'TIMER0': {
									'slice': (8,), 'access': 'R/W',
									'description': 'Classify TIMER0 as region 0 or region 1 peripheral',
								},
							'TIMER1': {
									'slice': (9,), 'access': 'R/W',
									'description': 'Classify TIMER1 as region 0 or region 1 peripheral',
								},
							'TIMER2': {
									'slice': (10,), 'access': 'R/W',
									'description': 'Classify TIMER2 as region 0 or region 1 peripheral',
								},
							'RTC0': {
									'slice': (11,), 'access': 'R/W',
									'description': 'Classify TIMER2 as region 0 or region 1 peripheral',
								},
							'TEMP': {
									'slice': (12,), 'access': 'R/W',
									'description': 'Classify TEMP as region 0 or region 1 peripheral',
								},
							'RNG': {
									'slice': (13,), 'access': 'R/W',
									'description': 'Classify RNG as region 0 or region 1 peripheral',
									},
							'ECB': {
									'slice': (14,), 'access': 'R/W',
									'description': 'Classify ECB as region 0 or region 1 peripheral',
								},
							'CCM_AAR': {
									'slice': (15,), 'access': 'R/W',
									'description': 'Classify CCM and AAR as region 0 or region 1 peripheral',
								},
							'WDT': {
									'slice': (16,), 'access': 'R/W',
									'description': 'Classify WDT as region 0 or region 1 peripheral',
								},
							'RTC1': {
									'slice': (17,), 'access': 'R/W',
									'description': 'Classify RTC1 as region 0 or region 1 peripheral',
								},
							'QDEC': {
									'slice': (18,), 'access': 'R/W',
									'description': 'Classify QDEC as region 0 or region 1 peripheral',
								},
							'COMP_LPCOMP': {
									'slice': (19,), 'access': 'R/W',
									'description': 'Classify COMP_LPCOMP as region 0 or region 1 peripheral',
								},
							'NVMC': {
									'slice': (30,), 'access': 'R/W',
									'description': 'Classify NVMC as region 0 or region 1 peripheral',
								},
							'PPI': {
									'slice': (31,), 'access': 'R/W',
									'description': 'Classify PPI as region 0 or region 1 peripheral',
								},
						},
				},
			'NVMC_RLENR0': {
					'address': 0x4001E52C, 'module': 'NVMC',
					'description': '''Length of RAM region 0.

Given a base address for the RAM called RAMBA, RAM address < RAMBA + RLENR0 are classified as region0 RAM and RAM addresses >= RAMBA + RLENR0 are classified as region
1 RAM.

The address (RAMBA + RLENR0) has to be word-aligned.

RAMBA and the total available RAM is defined in the product specification of the chip you are using.
''',
				},
			'NMVC_PROTENSET0': {
					'address': 0x4001E600, 'module': 'NVMC',
					'description': 'Protection bit enable set register',
					'bitfields': {
							'PROTREG0': {
									'slice': (0,),
									'description':'Protection enable bit for block 0. Enables protection of block 0. Readback value of protection bit 0.',
								},
							'PROTREG1': {
									'slice': (1,),
									'description':'Protection enable bit for block 1. Enables protection of block 1. Readback value of protection bit 1.',
								},
							'PROTREG2': {
									'slice': (2,),
									'description':'Protection enable bit for block 2. Enables protection of block 2. Readback value of protection bit 2.',
								},
							'PROTREG3': {
									'slice': (3,),
									'description':'Protection enable bit for block 3. Enables protection of block 3. Readback value of protection bit 3.',
								},
							'PROTREG4': {
									'slice': (4,),
									'description':'Protection enable bit for block 4. Enables protection of block 4. Readback value of protection bit 4.',
								},
							'PROTREG5': {
									'slice': (5,),
									'description':'Protection enable bit for block 5. Enables protection of block 5. Readback value of protection bit 5.',
								},
							'PROTREG6': {
									'slice': (6,),
									'description':'Protection enable bit for block 6. Enables protection of block 6. Readback value of protection bit 6.',
								},
							'PROTREG7': {
									'slice': (7,),
									'description':'Protection enable bit for block 7. Enables protection of block 7. Readback value of protection bit 7.',
								},
							'PROTREG8': {
									'slice': (8,),
									'description':'Protection enable bit for block 8. Enables protection of block 8. Readback value of protection bit 8.',
								},
							'PROTREG9': {
									'slice': (9,),
									'description':'Protection enable bit for block 9. Enables protection of block 9. Readback value of protection bit 9.',
								},
							'PROTREG10': {
									'slice': (10,),
									'description':'Protection enable bit for block 10. Enables protection of block 10. Readback value of protection bit 10.',
								},
							'PROTREG11': {
									'slice': (11,),
									'description':'Protection enable bit for block 11. Enables protection of block 11. Readback value of protection bit 11', },
							'PROTREG12': {
									'slice': (12,),
									'description':'Protection enable bit for block 12. Enables protection of block 12. Readback value of protection bit 12.',
								},
							'PROTREG13': {
									'slice': (13,),
									'description':'Protection enable bit for block 13. Enables protection of block 13. Readback value of protection bit 13.',
								},
							'PROTREG14': {
									'slice': (14,),
									'description':'Protection enable bit for block 14. Enables protection of block 14. Readback value of protection bit 14.',
								},
							'PROTREG15': {
									'slice': (15,),
									'description':'Protection enable bit for block 15. Enables protection of block 15. Readback value of protection bit 15.',
								},
							'PROTREG16': {
									'slice': (16,),
									'description':'Protection enable bit for block 16. Enables protection of block 16. Readback value of protection bit 16.',
								},
							'PROTREG17': {
									'slice': (17,),
									'description':'Protection enable bit for block 17. Enables protection of block 17. Readback value of protection bit 17.',
								},
							'PROTREG18': {
									'slice': (18,),
									'description':'Protection enable bit for block 18. Enables protection of block 18. Readback value of protection bit 18.',
								},
							'PROTREG19': {
									'slice': (19,),
									'description':'Protection enable bit for block 19. Enables protection of block 19. Readback value of protection bit 19.',
								},
							'PROTREG20': {
									'slice': (20,),
									'description':'Protection enable bit for block 20. Enables protection of block 20. Readback value of protection bit 20.',
								},
							'PROTREG21': {
									'slice': (21,),
									'description':'Protection enable bit for block 21. Enables protection of block 21. Readback value of protection bit 21.',
								},
							'PROTREG22': {
									'slice': (22,),
									'description':'Protection enable bit for block 22. Enables protection of block 22. Readback value of protection bit 22.',
								},
							'PROTREG23': {
									'slice': (23,),
									'description':'Protection enable bit for block 23. Enables protection of block 23. Readback value of protection bit 23.',
								},
							'PROTREG24': {
									'slice': (24,),
									'description':'Protection enable bit for block 24. Enables protection of block 24. Readback value of protection bit 24.',
								},
							'PROTREG25': {
									'slice': (25,),
									'description':'Protection enable bit for block 25. Enables protection of block 25. Readback value of protection bit 25.',
								},
							'PROTREG26': {
									'slice': (26,),
									'description':'Protection enable bit for block 26. Enables protection of block 26. Readback value of protection bit 26.',
								},
							'PROTREG27': {
									'slice': (27,),
									'description':'Protection enable bit for block 27. Enables protection of block 27. Readback value of protection bit 27.',
								},
							'PROTREG28': {
									'slice': (28,),
									'description':'Protection enable bit for block 28. Enables protection of block 28. Readback value of protection bit 28.',
								},
							'PROTREG29': {
									'slice': (29,),
									'description':'Protection enable bit for block 29. Enables protection of block 29. Readback value of protection bit 29.',
								},
							'PROTREG30': {
									'slice': (30,),
									'description':'Protection enable bit for block 30. Enables protection of block 30. Readback value of protection bit 30.',
								},
							'PROTREG31': {
									'slice': (31,),
									'description':'Protection enable bit for block 31. Enables protection of block 31. Readback value of protection bit 31.',
								},
						},

				},
			'NMVC_PROTENSET1': {
					'address': 0x4001E604, 'module': 'NVMC',
					'description': 'Proteciton bit enable set register',
					'bitfields': {
							'PROTREG32': {
									'slice': (0,),
									'description':'Protection enable bit for block 32. Enables protection of block 32. Readback value of protection bit 32.',
								},
							'PROTREG33': {
									'slice': (1,),
									'description':'Protection enable bit for block 33. Enables protection of block 33. Readback value of protection bit 33.',
								},
							'PROTREG34': {
									'slice': (2,),
									'description':'Protection enable bit for block 34. Enables protection of block 34. Readback value of protection bit 34.',
								},
							'PROTREG35': {
									'slice': (3,),
									'description':'Protection enable bit for block 35. Enables protection of block 35. Readback value of protection bit 35.',
								},
							'PROTREG36': {
									'slice': (4,),
									'description':'Protection enable bit for block 36. Enables protection of block 36. Readback value of protection bit 36.',
								},
							'PROTREG37': {
									'slice': (5,),
									'description':'Protection enable bit for block 37. Enables protection of block 37. Readback value of protection bit 37.',
								},
							'PROTREG38': {
									'slice': (6,),
									'description':'Protection enable bit for block 38. Enables protection of block 38. Readback value of protection bit 38.',
								},
							'PROTREG39': {
									'slice': (7,),
									'description':'Protection enable bit for block 39. Enables protection of block 39. Readback value of protection bit 39.',
								},
							'PROTREG40': {
									'slice': (8,),
									'description':'Protection enable bit for block 40. Enables protection of block 40. Readback value of protection bit 40.',
								},
							'PROTREG41': {
									'slice': (9,),
									'description':'Protection enable bit for block 41. Enables protection of block 41. Readback value of protection bit 41.',
								},
							'PROTREG42': {
									'slice': (10,),
									'description':'Protection enable bit for block 42 Enables protection of block 42 Readback value of protection bit 42.',
								},
							'PROTREG43': {
									'slice': (11,),
									'description':'Protection enable bit for block 43. Enables protection of block 43. Readback value of protection bit 43', },
							'PROTREG44': {
									'slice': (12,),
									'description':'Protection enable bit for block 44. Enables protection of block 44. Readback value of protection bit 44.',
								},
							'PROTREG45': {
									'slice': (13,),
									'description':'Protection enable bit for block 45. Enables protection of block 45. Readback value of protection bit 45.',
								},
							'PROTREG46': {
									'slice': (14,),
									'description':'Protection enable bit for block 46. Enables protection of block 46. Readback value of protection bit 46.',
								},
							'PROTREG47': {
									'slice': (15,),
									'description':'Protection enable bit for block 47. Enables protection of block 47. Readback value of protection bit 47.',
								},
							'PROTREG48': {
									'slice': (16,),
									'description':'Protection enable bit for block 48. Enables protection of block 48. Readback value of protection bit 48.',
								},
							'PROTREG49': {
									'slice': (17,),
									'description':'Protection enable bit for block 49. Enables protection of block 49. Readback value of protection bit 49.',
								},
							'PROTREG50': {
									'slice': (18,),
									'description':'Protection enable bit for block 50. Enables protection of block 50. Readback value of protection bit 50.',
								},
							'PROTREG51': {
									'slice': (19,),
									'description':'Protection enable bit for block 51. Enables protection of block 51. Readback value of protection bit 51.',
								},
							'PROTREG52': {
									'slice': (20,),
									'description':'Protection enable bit for block 52. Enables protection of block 52. Readback value of protection bit 52.',
								},
							'PROTREG53': {
									'slice': (21,),
									'description':'Protection enable bit for block 53. Enables protection of block 53. Readback value of protection bit 53.',
								},
							'PROTREG54': {
									'slice': (22,),
									'description':'Protection enable bit for block 54. Enables protection of block 54. Readback value of protection bit 54.',
								},
							'PROTREG55': {
									'slice': (23,),
									'description':'Protection enable bit for block 55. Enables protection of block 55. Readback value of protection bit 55.',
								},
							'PROTREG56': {
									'slice': (24,),
									'description':'Protection enable bit for block 56. Enables protection of block 56. Readback value of protection bit 56.',
								},
							'PROTREG57': {
									'slice': (25,),
									'description':'Protection enable bit for block 57. Enables protection of block 57. Readback value of protection bit 57.',
								},
							'PROTREG58': {
									'slice': (26,),
									'description':'Protection enable bit for block 58. Enables protection of block 58. Readback value of protection bit 58.',
								},
							'PROTREG59': {
									'slice': (27,),
									'description':'Protection enable bit for block 59. Enables protection of block 59. Readback value of protection bit 59.',
								},
							'PROTREG60': {
									'slice': (28,),
									'description':'Protection enable bit for block 60. Enables protection of block 60. Readback value of protection bit 60.',
								},
							'PROTREG61': {
									'slice': (29,),
									'description':'Protection enable bit for block 61. Enables protection of block 61. Readback value of protection bit 61.',
								},
							'PROTREG62': {
									'slice': (30,),
									'description':'Protection enable bit for block 62. Enables protection of block 62. Readback value of protection bit 62.',
								},
							'PROTREG63': {
									'slice': (31,),
									'description':'Protection enable bit for block 63. Enables protection of block 63. Readback value of protection bit 63.',
								},
						},
				},
			'NMVC_DISABLEIDEBUG': {
					'address': 0x4001E608, 'module': 'NVMC',
					'description': '''Disable protection mechanism in debug mode. This register will only disable the protection mechanism if the device is in debug mode.
0: Disable in debug
1: Enable in debug''',
					'default': 0x1,
				},
			############### peripherals over APB, base address 0x40000000
	    #### 0000: Power, Clock ####
			# 'POWERCLOCK_TASK0': { 'module': 'POWERCLOCK', 'address': 0x40000000, },
			'CLOCK_HFCLKSTART': {
					'address': 0x40000000, 'module': 'CLOCK',
					'description': 'Start HFCLK crystal oscillator',
				},
			# 'POWERCLOCK_TASK0': { 'module': 'POWERCLOCK', 'address': 0x40000004, },
			'CLOCK_HFCLKSTOP': {
					'module': 'CLOCK', 'address': 0x40000004,
					'description': 'Stop HFCLK crystal oscillator',
				},
			# 'POWERCLOCK_TASK2': { 'module': 'POWERCLOCK', 'address': 0x40000008, },
			'CLOCK_LFCLKSTART': {
					'module': 'CLOCK', 'address': 0x40000008,
					'description': 'Start LFCLK source',
				},
			# 'POWERCLOCK_TASK3': { 'module': 'POWERCLOCK', 'address': 0x4000000C, },
			'CLOCK_LFCLKSTOP': {
					'module': 'CLOCK', 'address': 0x4000000C,
					'description': 'Stop LFCLK source',
				},
			# 'POWERCLOCK_TASK4': { 'module': 'POWERCLOCK', 'address': 0x40000010, },
			'CLOCK_CAL': {
					'module': 'CLOCK', 'address': 0x40000010,
					'description': 'Start calibration of LFCLK RC oscillator',
				},
			# 'POWERCLOCK_TASK5': { 'module': 'POWERCLOCK', 'address': 0x40000014, },
			'CLOCK_CTSTART': {
					'module': 'CLOCK', 'address': 0x40000014,
					'description': 'Start calibration timer',
				},
			# 'POWERCLOCK_TASK6': { 'module': 'POWERCLOCK', 'address': 0x40000018, },
			'CLOCK_CTSTOP': {
					'module': 'CLOCK', 'address': 0x40000018,
					'description': 'Stop calibration timer',
				},
			# 'POWERCLOCK_TASK30': { 'address': 0x40000078, },
			'POWER_CONSTLAT': {  # same as TASK30
					'address': 0x40000078, 'module': 'POWER',
					'description': 'Enable constant latency mode',
				},
			'POWER_LOWPWR': {
					'address': 0x4000007C, 'module': 'POWER',
						'description': 'Enable low power mode (variable latency)',
				},
			# 'POWERCLOCK_EVENT0': { 'address': 0x40000100, },
			'CLOCK_HFCLKSTARTED': {
					'address': 0x40000100, 'module': 'CLOCK',
					'description': '16 MHz oscillator started',
				},
			# 'POWERCLOCK_EVENT1': { 'address': 0x40000104, },
			'CLOCK_LFCLKSTARTED': {
					'address': 0x40000104, 'module': 'CLOCK',
					'description': '32 KHz oscillator started',
				},
			# 'POWERCLOCK_EVENT2': { 'address': 0x40000108, },
			'POWER_POFWARN': {
					'address': 0x40000108, 'module': 'POWER',
						'description': 'Power failure warning',
					},
			# 'POWERCLOCK_EVENT3': { 'address': 0x4000010C, },
			'CLOCK_DONE': {
					'address': 0x4000010C, 'module': 'CLOCK',
					'description': 'Calibration of LFCLK RC oscillator complete event',
				},
			# 'POWERCLOCK_EVENT4': { 'address': 0x40000110, },
			'CLOCK_CTTO': {
					'address': 0x40000110, 'module': 'CLOCK',
					'description': 'Calibration timer timeout',
				},
			# 'POWERCLOCK_SHORTS':  { 'address': 0x40000200, },
			'POWERCLOCK_INTENSET':{
					'address': 0x40000304, 'module': 'POWERCLOCK',
					'description': 'Interrupt enable set register',
				},
			'POWER_INTENSET':{
					'address': 0x40000304, 'module': 'POWER',
					'description': 'Interrupt enable set register',
				},
			'CLOCK_INTENSET':{
					'address': 0x40000304, 'module': 'CLOCK',
					'description': 'Interrupt enable set register',
				},
			'POWERCLOCK_INTENCLR':{
					'address': 0x40000308, 'module': 'POWERCLOCK',
					'description': 'Interrupt enable clear register',
				},
			'POWER_INTENCLR':{
					'address': 0x40000308, 'module': 'POWER',
					'description': 'Interrupt enable clear register',
				},
			'CLOCK_INTENCLR':{
					'address': 0x40000308, 'module': 'CLOCK',
					'description': 'Interrupt enable clear register',
				},
			# 'POWERCLOCK_REG0':    { 'address': 0x40000400, },
			'POWER_RESETREAS': {
					'address': 0x40000400, 'module': 'POWER',
						'description': 'Reset reason',
						'default': 0x0,
						'bitfields': {
								'RESETPIN': {
										'slice': (0,),
										'description': 'Reset from pin detected',
										'access': 'R/W',
									},
								'DOG': {
										'slice': (1,),
										'description': 'Reset from watchdog detected',
										'access': 'R/W',
									},
								'SREQ': {
										'slice': (2,),
										'description': 'Reset from AIRCR_SYSRESETREQ detected',
										'access': 'R/W',
									},
								'LOCKUP': {
										'slice': (3,),
										'description': 'Reset from CPU lock-up detected',
									},
								'OFF': {
										'slice': (16,),
										'description': 'Reset due to wake-up from OFF mode when wakeup is triggered from the DETECT signal from GPIO',
										'access': 'R/W',
									},
								'LPCOMP': {
										'slice': (17,),
										'description': 'Reset due to wake-up from OFF mode when wakeup is triggered from ANADETECT signal from LPCOMP',
									},
								'DIF': {
										'slice': (18,),
										'description': 'Reset due to wake-up from OFF mode when wakeup is triggered from entering into debug interface mode',
									},
							},
				},
			# 'POWERCLOCK_REG3':    { 'address': 0x4000040C, },
			'CLOCK_HFCLKSTAT':    {
					'address': 0x4000040C, 'module': 'CLOCK',
					'description': 'Which HFCLK source is running',
					'default': 0,
					'bitfields': {
							'SRC': {
									'slice': (0,),
									'description': '''Active clock source.
0: 16 MHz RC oscillator running and generating the HFCLK
1: 16/32 MHz crystal oscillator running and generating the HFCLK.''',
									'access': 'R',
								},
							'STATE': {
									'slice': (16,),
									'description': '''HFCLK state
0: not running
1: running''',
									'access': 'R',
								},
						},
				},
			# 'POWERCLOCK_REG6':    { 'address': 0x40000418, },
			'CLOCK_LFCLKSTAT':    {
					'address': 0x40000418, 'module': 'CLOCK',
					'description': 'Which LFCLK source is running',
					'bitfields': {
							'SRC': {
									'slice': (1,0),
									'description': '''Active clock source
0: 32.768 KHz RC oscillator running and generating the LFCLK
1: 32.768 KHz crystal oscillator running and generating the LFCLK
2: 32.768 KHz synthesizer synthesizing 32.768 KHz from 16 MHz system clock''',
									'access': 'R',
								},
							'STATE': {
									'slice': (16,),
									'description': '''LFCLK state
0: LFCLK not running
1: LFCLK running''',
									'access': 'R',
								},
						},
				},

			'POWER_SYSTEMOFF': {
					'address': 0x40000500, 'module': 'POWER',
					'description': 'System OFF register',
					'access': 'W',
					'default': 0,
				},
			'POWER_POFCON': {
					'address': 0x40000510, 'module': 'POWER',
					'description': 'Power failure configuration',
					'bitfields': {
							'POF': {
									'slice': (0,),
									'description': '''0: Disable power failure comparator
1: Enable power failure comparator''',
								},
							'THRESHOLD': {
									'slice': (2,1),
									'description': '''0: Set threshold to 2.1 V
1: Set threshold to 2.3 V
2: Set threshold to 2.5 V
3: Set threshold to 2.7 V''',
								},
						},
				},
			'CLOCK_LFCLKSRC': {
					'address': 0x40000518, 'module': 'CLOCK',
					'description': 'Clock source for the 32 KHz clock',
					'default': 0,
					'bitfields': {
							'SRC': {
									'slice': (1,0),
									'description': '''clock source
0: 32.768 KHz RC oscillator
1: 32.768 KHz crystal oscillator
2: 32.768 KHz synthesizer synthesizing 32.768 KHz from 16 MHz system clock''',
									'access': 'R/W',
								},
						},
				},
			'POWER_GPREGRET': {
					'address': 0x4000051C, 'module': 'POWER',
					'description': 'General purpose retention register',
					'bitfields': {
							'GPREGRET': {
									'slice': (7,0),
									'access': 'R/W',
								},
						},
				},
			'POWER_RAMON': {
					'address': 0x40000524, 'module': 'POWER',
					'description': 'RAM on/off',
					'bitfields': {
							'ONRAM0': {
									'slice': (0,),
									'description': '''0: Keep RAM block 0 off in ON mode
1: Keep RAM block 0 on in ON mode''',
									'access': 'R/W',
								},
							'ONRAM1': {
									'slice': (1,),
									'description': '''0: Keep RAM block 1 off in ON mode
1: Keep RAM block 1 on in ON mode''',
									'access': 'R/W',
								},
							'ONRAM2': {
									'slice': (2,),
									'description': '''0: Keep RAM block 2 off in ON mode
1: Keep RAM block 2 on in ON mode''', 
									'access': 'R/W',
								},
							'ONRAM3': {
									'slice': (3,),
									'description': '''0: Keep RAM block 3 off in ON mode
1: Keep RAM block 3 on in ON mode''',
									'access': 'R/W',
								},
							'OFFRAM0': {
									'slice': (16,),
									'desciption': '''0: Keep RAM block 0 off in OFF mode
1: Keep RAM block 0 on in OFF mode''',
									'access': 'R/W',
								},
							'OFFRAM1': {
									'slice': (17,),
									'desciption': '''0: Keep RAM block 1 off in OFF mode
1: Keep RAM block 1 on in OFF mode''',
									'access': 'R/W',
								},
							'OFFRAM2': {
									'slice': (18,),
									'desciption': '''0: Keep RAM block 2 off in OFF mode
1: Keep RAM block 2 on in OFF mode''',
									'access': 'R/W',
								},
							'OFFRAM3': {
									'slice': (19,),
									'desciption': '''0: Keep RAM block 3 off in OFF mode
1: Keep RAM block 3 on in OFF mode''',
									'access': 'R/W',
								},
						},
				},
			'CLOCK_CTIV': {
					'address': 0x40000538, 'module': 'CLOCK',
					'description': 'Calibration timer interval',
				},
			'POWER_RESET': {
					'address': 0x40000544, 'module': 'POWER',
					'description': '''Configure reset functionality.
0: Disable
1: Enable''',
					'default': 0x1,
				},
			'CLOCK_XTALFREQ': {
					'address': 0x40000550, 'module': 'CLOCK',
					'description': '''Crystal frequency. Select nominal frequency of external crystal for HFCLK. This register has to match the actual crystal used in design to enable correct behavior.
0xFF: 16 MHz crystal is used.
0x00: 32 MHz crystal is used.''',
					'access': 'R/W',
					'default': 0xFFFFFFFF,
				},
			'POWER_DCDCEN': {
					'address': 0x40000578, 'module': 'POWER',
					'description': '''DCDC enable register.
0: Disable
1: Enable''',
					'default': 0,
				},


			#### 2000: UART0 ####
			# 'UART0_TASK0': { 'address': 0x40002000, },
			'UART0_STARTRX': {
					'address': 0x40002000, 'module': 'UART0',
					'description': 'Start UART receiver',
				},
			# 'UART0_TASK1': { 'address': 0x40002004, },
			'UART0_STOPRX': {
					'address': 0x40002004, 'module': 'UART0',
					'description': 'Stop UART receiver',
				},
			# 'UART0_TASK2': { 'address': 0x40002008, },
			'UART0_STARTTX': {
					'address': 0x40002008, 'module': 'UART0',
					'description': 'Start UART transmitter',
				},
			# 'UART0_TASK3': { 'address': 0x4000200C, },
			'UART0_STOPTX': {
					'address': 0x4000200C, 'module': 'UART0',
					'description': 'Stop UART transmitter',
				},

			# 'UART0_EVENT2': { 'address': 0x40002108, },
			'UART0_RXDRDY': {
					'address': 0x40002108, 'module': 'UART0',
					'description': 'Data received in RXD',
				},
			# 'UART0_EVENT7': { 'address': 0x4000211C, },
			'UART0_TXDRDY': {
					'address': 0x4000211C, 'module': 'UART0',
					'description': 'Data sent from TXD',
				},
			# 'UART0_EVENT9': { 'address': 0x40002124, },
			'UART0_ERROR': {
					'address': 0x40002124, 'module': 'UART0',
					'description': 'Error detected',
				},
			# 'UART0_EVENT17': { 'address': 0x40002144, },
			'UART0_RXTO': {
					'address': 0x40002144, 'module': 'UART0',
					'description': 'Receiver timeout',
				},
			# 'UART0_SHORTS':  { 'address': 0x40002200, },
			'UART0_INTENSET':{
					'address': 0x40002304, 'module': 'UART0',
					'description': 'Interrupt enable set register',
				},
			'UART0_INTENCLR':{
					'address': 0x40002308, 'module': 'UART0',
					'description': 'Interrupt enable clear register',
				},
			'UART0_ERRORSRC': {
					'address': 0x40002480, 'module': 'UART0',
					'description': 'Error source',
					'bitfields': {
							'OVERRUN': {
									'slice': (0,),
									'description': '''Overrun error.
A start bit is received while the previous data still lies in RXD.  (Previous data is lost.)
R 0: Not occurred
R 1: Occurred
W 1: Clear''',
									'access': 'R/W',
									'default': 0,
								},
							'PARITY': {
									'slice': (1,),
									'description': '''Parity error.
A character with bad parity is received, if HW parity check is enabled.
R 0: Not occurred
R 1: Occurred
W 1: Clear''',
									'access': 'R/W',
									'default': 0,
								},
							'FRAMING': {
									'slice': (2,),
									'description': '''Framing error occurred.
A valid stop bit is not detected on the serial data input after all bits in a character have been received.
R 0: Not occurred
R 1: Occurred
W 1: Clear''',
									'access': 'R/W',
									'default': 0,
								},
							'BREAK': {
									'slice': (3,),
									'description': '''Break condition.
The serial data input is '0' for longer than the length of a data frame. (The data frame length is 10 bits without parity bit, and 11 bits with parity bit.)
R 0: Not occurred
R 1: Occurred
W 1: Clear''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'UART0_ENABLE': {
					'address': 0x40002500, 'module': 'UART0',
					'description': 'Enable UART',
					'bitfields': {
							'ENABLE': {
									'slice': (2,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable UART
0: Disable UART
1: Enable UART''',
								},
						},
				},
			'UART0_PSELRTS': {
					'address': 0x40002508, 'module': 'UART0',
					'default': 0xFFFFFFFF,
					'access': 'R/W',
					'description': '''Pin select for RTS. Pin number configuration for UART RTS signal
RW [0..31]: Pin number to route the UART RTS signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'UART0_PSELTXD': {
					'address': 0x4000250C, 'module': 'UART0',
					'default': 0xFFFFFFFF,
					'access': 'R/W',
					'description': '''Pin select for TXD. Pin number configuration for UART TXD signal
RW [0..31]: Pin number to route the UART TXD signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'UART0_PSELCTS': {
					'address': 0x40002510, 'module': 'UART0',
					'default': 0xFFFFFFFF,
					'access': 'R/W',
					'description': '''Pin select for CTS. Pin number configuration for UART CTS signal
RW [0..31]: Pin number to route the UART CTS signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'UART0_PSELRXD': {
					'address': 0x40002514, 'module': 'UART0',
					'default': 0xFFFFFFFF,
					'access': 'R/W',
					'description': '''Pin select for RXD. A Pin number configuration for UART RXD signal
RW [0..31]: Pin number to route the UART RXD signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'UART0_RXD': {
					'address': 0x40002518, 'module': 'UART0',
					'description': 'RXD register',
					'bitfields': {
							'RXD': {
									'slice': (7,0),
									'access': 'R',
									'default': 0,
									'description': 'RX data received in previous transfers.',
								},
						},
				},
			'UART0_TXD': {
					'address': 0x4000251C, 'module': 'UART0',
					'description': 'TXD register',
					'bitfields': {
							'TXD': {
									'slice': (7,0),
									'access': 'W',
									'default': 0,
									'description': 'TX data to be transferred.',
								},
						},
				},
			'UART0_BAUDRATE': {
					'address': 0x40002524, 'module': 'UART0',
					'access': 'R/W',
					'default': 0x01980000,
					'description': '''Baud rate
0x0004F000 (BAUD1200):     1200 baud
0x0009D000 (BAUD2400):     2400 baud
0x0013B000 (BAUD4800):     4800 baud
0x00275000 (BAUD9600):     9600 baud
0x003B0000 (BAUD14400):   14400 baud
0x004EA000 (BAUD19200):   19200 baud
0x0075F000 (BAUD28800):   28800 baud
0x009D5000 (BAUD38400):   38400 baud
0x00EBF000 (BAUD57600):   57600 baud
0x013A9000 (BAUD76800):   76800 baud
0x01D7E000 (BAUD115200): 115200 baud
0x03AFB000 (BAUD230400): 230400 baud
0x04000000 (BAUD250000): 250000 baud
0x075F7000 (BAUD460800): 460800 baud
0X0EBEDFA4 (BAUD921600): 921600 baud
0x10000000 (BAUD1M):     1 megabaud''',
				},
			'UART0_CONFIG': {
					'address': 0x4000256C, 'module': 'UART0',
					'description': 'Configuration of parity and hardware flow control',
					'bitfields': {
							'HWFC': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Hardware flow control
0: Disabled
1: Enabled''',
								},
							'PARITY': {
									'slice': (2,1),
									'access': 'R/W',
									'default': 0b10,
									'description': '''Parity
0x0 Exclude parity bit
0x7 Include parity bit''', ### Is this an error? the field is only 2 bits!
								},
						},
				},

			#### 3000: SPI0, TWI0 (I2C) ####
			# 'SPI0TWI0_TASK0': { 'address': 0x40003000, },
			'TWI0_STARTRX': {
					'address': 0x40003000, 'module': 'TWI0',
					'description': 'Start TWI receive sequence',
				},

			# 'SPI0TWI0_TASK2': { 'address': 0x40003008, },
			'TWI0_STARTTX': {
					'address': 0x40003008, 'module': 'TWI0',
					'description': 'Start TWI transmit sequence',
					},
			# 'SPI0TWI0_TASK5': { 'address': 0x40003014, },
			'TWI0_STOP': {
					'address': 0x40003014, 'module': 'TWI0',
					'description': 'Stop TWI transaction',
				},
			# 'SPI0TWI0_TASK7': { 'address': 0x4000301C, },
			'TWI0_SUSPEND': {
					'address': 0x4000301C, 'module': 'TWI0',
					'description': 'Suspend TWI transaction',
				},

			# 'SPI0TWI0_TASK8': { 'address': 0x40003020, },
			'TWI0_RESUME': {
					'address': 0x40003020, 'module': 'TWI0',
					'description': 'Resume TWI transaction',
				},
			# 'SPI0TWI0_EVENT1': { 'address': 0x40003104, },
			'TWI0_STOPPED': {
					'address': 0x40003104, 'module': 'TWI0',
					'description': 'TWI stopped',
				},
			# 'SPI0TWI0_EVENT2': { 'address': 0x40003108, },
			'SPI0_READY': {
					'address': 0x40003108, 'module': 'TWI0',
					'description': 'TXD byte sent and RXD byte received',
				},
			'TWI0_RXDRDY': {
					'address': 0x40003108, 'module': 'TWI0',
					'description': 'TWI RXD byte received',
				},
			# 'SPI0TWI0_EVENT7': { 'address': 0x4000311C, },
			'TWI0_TXDSENT': {
					'address': 0x4000311C, 'module': 'TWI0',
					'description': 'TWI TXD byte sent',
				},
			# 'SPI0TWI0_EVENT9': { 'address': 0x40003124, },
			'TWI0_ERROR': {
					'address': 0x40003124, 'module': 'TWI0',
					'description': 'TWI error',
				},
			# 'SPI0TWI0_EVENT14': { 'address': 0x40003138, },
			'TWI0_BB': {
					'address': 0x40003138, 'module': 'TWI0',
					'description': 'TWI byte boundary, generated before each byte that is sent or received',
				},

			'TWI0_SHORTS':  {
					'address': 0x40003200, 'module': 'TWI0',
					'description': 'Shortcut register',
					'bitfields': {
							'BB_SUSPEND': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Short-cut between BB event and SUSPEND task
0 Disable
1 Enable''',
								},
							'BB_STOP': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''Short-cut between BB event and STOP task
0: Disable
1: Enable''',
								},
						},
				},
			# 'SPI0TWI0_INTENSET':{ 'address': 0x40003304, },
			'SPI0_INTENSET': {
					'address': 0x40003304, 'module': 'TWI0',
					'description': 'Interrupt enable set register',
				},
			'TWI0_INTENSET': {
					'address': 0x40003304, 'module': 'TWI0',
					'description': 'Interrupt enable set register',
				},
			# 'SPI0TWI0_INTENCLR':{ 'address': 0x40003308, },
			'SPI0_INTENCLR':{
					'address': 0x40003308, 'module': 'SPI0',
					'description': 'Interrupt enable clear register',
				},
			'TWI0_INTENCLR':{
					'address': 0x40003308, 'module': 'TWI0',
					'description': 'Interrupt enable clear register',
				},
			'TWI0_ERRORSRC': {
					'address': 0x400034C4, 'module': 'TWI0',
					'description': 'TWI error source',
					'bitfields': {
							'ANACK': {
									'slice': (1,),
									'description': '''NACK received after sending the address (write '1' to clear)''',
									'access': 'R/W',
									'default': 0,
								},
							'DNACK': {
									'slice': (2,),
									'description': '''NACK received after sending a data byte (write '1' to clear)''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'SPI0_ENABLE':   {
					'address': 0x40003500, 'module': 'SPI0',
				'description': 'Enable SPI',
				'bitfields': {
					'ENABLE': {
							'slice': (2,0),
							'description': '''Enable or disable SPI.
0: Disable
1: Enabled''',
						},
					},
				},
			'TWI0_ENABLE': {
					'address': 0x40003500, 'module': 'TWI0',
					'description': 'Enable TWI master',
					'bitfields': {
							'ENABLE': {
								'slice': (2,0),
								'description': '''0: Disable TWI
5: Enable TWI''',
								'access': 'R/W',
								'default': 0,
							},
						},
				},
			'SPI0_PSELSCK': {
					'address': 0x40003508, 'module': 'SPI0',
					'description': '''Pin select for SCK. Pin number configuration for SPI SCK signal
RW 0..31: pin number to route the SPI SCK signal to
W 0xFFFFFFFF: Disconnect.''',
					'default': 0xFFFFFFFF,
					'access': 'R/W',
				},
			'TWI0_PSELSCL': {
					'address': 0x40003508, 'module': 'TWI0',
					'description': '''Pin select for SCL. Pin number configuration for TWI SCL signal
RW [0..31]: Pin number to route the TWI SCL signal to
W 0xFFFFFFFF Disconnect''',
				},
			'SPI0_PSELMOSI': {
					'address': 0x4000350C, 'module': 'SPI0',
					'description': '''Pin select for MOSI. Pin number configuration for SPI MOSI signal
RW 0..31: pin number to route the SPI MOSI signal to
W 0xFFFFFFFF: Disconnect.''',
				},
			'TWI0_PSELSDA': {
					'address': 0x4000350C, 'module': 'TWI0',
					'description': '''Pin select for SDA. Pin number configuration for TWI SDA signal
RW [0..31] Pin number to route the TWI SDA signal to
W 0xFFFFFFFF Disconnect''',
				},
			'SPI0_PSELMISO': {
					'address': 0x40003510, 'module': 'SPI0',
					'description': '''Pin select for MISO. Pin number configuration for SPI master MISO signal
RW 0..31: Pin number to route the SPI master MISO signal to
W 0xFFFFFFFF: Disconnect.''',
				},
			'SPI0_RXD': {
					'address': 0x40003518, 'module': 'SPI0',
					'description': 'RxD register',
					'bitfields': {
						'RXD': {
							'slice': (7,0),
							'description': '''RX data received. Double buffered.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'TWI0_RXD': {
					'address': 0x40003518, 'module': 'TWI0',
					'description': 'RXD register',
					'bitfields': {
							'RXD': {
									'slice': (7,0),
									'description': '''RX data from last transfer''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'SPI0_TXD': {
					'address': 0x4000351C, 'module': 'SPI0',
					'description': 'TxD register',
					'bitfields': {
						'TXD': {
							'slice': (7,0),
							'description': '''TX data to send. Double buffered.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'TWI0_TXD': {
					'address': 0x4000351C, 'module': 'TWI0',
				'description': 'TXD register',
				'bitfields': {
					'TXD': {
						'slice': (7,0),
						'description': 'TX data for next transfer',
						'access': 'R/W',
						'default': 0,
						},
					},
				},
			'SPI0_FREQUENCY': {
					'address': 0x40003524, 'module': 'SPI0',
					'description': '''SPI frequency. SPI master data rate.
0x02000000: (K125) 125 Kbps
0x04000000: (K250) 250 Kbps
0x08000000: (K500) 500 Kbps
0x10000000: (M1) 1 Mbps
0x20000000: (M2) 2 Mbps
0x40000000: (M4) 4 Mbps
0x80000000: (M8) 8 Mbps''',
					'default': 0,
					'access': 'R/W',
				},
			'TWI0_FREQUENCY': {
					'address': 0x40003524, 'module': 'TWI0',
					'access': 'R/W',
					'default': 0x04000000,
					'description': '''TWI frequency. TWI master clock frequency
0x01980000 (K100): 100 Kbps
0x40000000 (K250): 250 Kbps
0x06680000 (K400): 400 Kbps''',
				},
			'SPI0_CONFIG': {
					'address': 0x40003554, 'module': 'SPI0',
					'description': 'Configuration register',
					'bitfields': {
							'ORDER': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: MSB first
1: LSB first''',
								},
							'CPOL': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: Active high
1: Active low''',
								},
							'CPHA': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: leading - sample on leading edge of clock, shift serial data on trailing edge
1: trailing - sample on trailing edge of clock, shift serial data on leading edge.''',
								},
						},
				},
			'TWI0_ADDRESS': {
					'address': 0x40003588, 'module': 'TWI0',
					'description': 'Address used in the TWI transfer',
					'bitfields': {
						'ADDRESS': {
							'slice': (6,0),
							'description': 'TWI address',
							'default': 0,
							'access': 'R/W',
						},
					},
				},

			#### 4000: SPI1, TWI1, SPIS (slave) ####
			# 'SPI1TWI1SPIS_TASK0': { 'address': 0x40004000, },
			'TWI1_STARTRX': {
					'address': 0x40004000, 'module': 'TWI1',
					'description': 'Start TWI receive sequence',
				},
			# 'SPI1TWI1SPIS_TASK2': { 'address': 0x40004008, },
			'TWI1_STARTTX': {
					'address': 0x40004008, 'module': 'TWI1',
					'description': 'Start TWI transmit sequence',
					},
			# 'SPI1TWI1SPIS_TASK5': { 'address': 0x40004014, },
			'TWI1_STOP': {
					'address': 0x40004014, 'module': 'TWI1',
					'description': 'Stop TWI transaction',
				},
			# 'SPI1TWI1SPIS_TASK7': { 'address': 0x4000401C, },
			'TWI1_SUSPEND': {
					'address': 0x4000401C, 'module': 'TWI1',
					'description': 'Suspend TWI transaction',
				},
			# 'SPI1TWI1SPIS_TASK8': { 'address': 0x40004020, },
			'TWI1_RESUME': {
					'address': 0x40004020, 'module': 'TWI1',
					'description': 'Resume TWI transaction',
				},
			# 'SPI1TWI1SPIS_TASK9': { 'address': 0x40004024, },
			'SPIS_ACQUIRE': {
					'address': 0x40004024, 'module': 'SPIS',
					'description': 'Acquire SPI semaphore',
				},
			# 'SPI1TWI1SPIS_TASK10': { 'address': 0x40004028, },
			'SPIS_RELEASE': {
					'address': 0x40004028, 'module': 'SPIS',
					'description': 'Release SPI semaphore, enabling the SPI slave to acquire it.',
				},
			# 'SPI1TWI1SPIS_EVENT1': { 'address': 0x40004104, },
			'SPIS_END': {
					'address': 0x40004104, 'module': 'SPIS',
					'description': 'Granted transaction completed.',
				},
			'TWI1_STOPPED': {
					'address': 0x40004104, 'module': 'TWI1',
					'description': 'TWI stopped',
				},
			# 'SPI1TWI1SPIS_EVENT2': { 'address': 0x40004108, },
			'SPI1_READY': {
					'address': 0x40004108, 'module': 'SPI1',
					'description': 'TXD byte sent and RXD byte received',
				},
			'TWI1_RXDRDY': {
					'address': 0x40004108, 'module': 'TWI1',
					'description': 'TWI RXD byte received',
				},
			# 'SPI1TWI1SPIS_EVENT7': { 'address': 0x4000411C, },
			'TWI1_TXDSENT': {
					'address': 0x4000411C, 'module': 'TWI1',
					'description': 'TWI TXD byte sent',
				},
			# 'SPI1TWI1SPIS_EVENT9': { 'address': 0x40004124, },
			'TWI1_ERROR': {
					'address': 0x40004124, 'module': 'TWI1',
					'description': 'TWI error',
				},
			# 'SPI1TWI1SPIS_EVENT10': { 'address': 0x40004128, },
			'SPIS_ACQUIRED': {
					'address': 0x40004128, 'module': 'SPIS',
					'description': 'Semaphore acquired.',
				},
			# 'SPI1TWI1SPIS_EVENT14': { 'address': 0x40004138, },
			'TWI1_BB': {
					'address': 0x40004138, 'module': 'TWI1',
					'description': 'TWI byte boundary, generated before each byte that is sent or received',
				},
			'SPIS_SHORTS':  {
					'address': 0x40004200, 'module': 'SPIS',
					'description': 'Shortcut for the SPI slave',
					'bitfields': {
							'END_ACQUIRE': {
									'slice': (2,),
									'description': 'Enable or disable shortcut between END event and ACQUIRE task.',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'TWI1_SHORTS':  {
					'address': 0x40004200, 'module': 'TWI1',
					'description': 'Shortcut register',
					'bitfields': {
							'BB_SUSPEND': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Short-cut between BB event and SUSPEND task
0 Disable
1 Enable''',
								},
							'BB_STOP': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''Short-cut between BB event and STOP task
0: Disable
1: Enable''',
								},
						},
				},
			# 'SPI1TWI1SPIS_INTENSET':{ 'address': 0x40004304, },
			'SPI1_INTENSET': {
					'address': 0x40004304, 'module': 'SPI1',
					'description': 'Interrupt enable set register',
				},
			'TWI1_INTENSET': {
					'address': 0x40004304, 'module': 'TWI1',
					'description': 'Interrupt enable set register',
				},
			'SPIS_INTENSET':{
					'address': 0x40004304, 'module': 'SPI1',
					'description': 'Interrupt enable set register',
				},
			# 'SPI1TWI1SPIS_INTENCLR':{ 'address': 0x40004308, },
			'SPI1_INTENCLR':{
					'address': 0x40004308, 'module': 'SPI1',
					'description': 'Interrupt enable clear register',
				},
			'TWI1_INTENCLR':{
					'address': 0x40004308, 'module': 'TWI1',
					'description': 'Interrupt enable clear register',
				},
			'SPIS_INTENCLR':{
					'address': 0x40004308, 'module': 'SPI1',
					'description': 'Interrupt enable clear register',
				},
			# 'SPI1TWI1SPIS_REG0':    { 'address': 0x40004400, },
			'SPIS_SEMSTAT':    {
					'address': 0x40004400, 'module': 'SPI1',
					'description': 'Semaphore status register',
					'bitfields': {
							'SEMSTAT': {
									'slice': (1,0),
									'access': 'R',
									'default': 0b01,
									'description': '''Semaphore status.
0: Free - Semaphore is free
1: CPU - Semaphore is assigned to CPU
2: SPIS - Semaphore is assigned to SPI slave
3: CPUENDING - Semaphore is assigned to SPI but a handover to the CPU is pending.''',
								},
						},
				},
			# 'SPI1TWI1SPIS_REG16':   { 'address': 0x40004440, },
			'SPIS_STATUS':   {
					'address': 0x40004440, 'module': 'SPIS',
					'description': 'Status from last transaction',
					'bitfields': {
							'OVERREAD': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': 'TX buffer over-read detected and prevented.',
								},
							'OVERFLOW': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': 'RX buffer overflow detected and prevented.',
								},
						},
				},
			'TWI1_ERRORSRC': {
					'address': 0x400044C4, 'module': 'TWI1',
					'description': 'TWI error source',
					'bitfields': {
							'ANACK': {
									'slice': (1,),
									'description': '''NACK received after sending the address (write '1' to clear)''',
									'access': 'R/W',
									'default': 0,
								},
							'DNACK': {
									'slice': (2,),
									'description': '''NACK received after sending a data byte (write '1' to clear)''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'SPI1_ENABLE':   {
				'address': 0x40004500, 'module': 'SPI1',
				'description': 'Enable SPI',
				'bitfields': {
					'ENABLE': {
							'slice': (2,0),
							'description': '''Enable or disable SPI.
0: Disable
1: Enabled''',
						},
					},
				},
			'TWI1_ENABLE': {
					'address': 0x40004500, 'module': 'TWI1',
					'description': 'Enable TWI master',
					'bitfields': {
						'ENABLE': {
							'slice': (2,0),
							'description': '''0: Disable TWI
5: Enable TWI''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'SPIS_ENABLE': {
					'address': 0x40004500, 'module': 'SPIS',
					'slice': (2,0),
					'default': 0,
					'description': '''Enable SPI slave
0: Disable SPI slave
2: Enable SPI slave''',
					'access': 'R/W',
				},
			'SPI1_PSELSCK': {
					'address': 0x40004508, 'module': 'SPI1',
					'description': '''Pin select for SCK. Pin number configuration for SPI SCK signal
RW 0..31: pin number to route the SPI SCK signal to
W 0xFFFFFFFF: Disconnect.''',
					'default': 0xFFFFFFFF,
					'access': 'R/W',
				},
			'TWI1_PSELSCL': {
					'address': 0x40004508, 'module': 'TWI1',
					'description': '''Pin select for SCL. Pin number configuration for TWI SCL signal
RW [0..31]: Pin number to route the TWI SCL signal to
W 0xFFFFFFFF Disconnect''',
				},
			'SPIS_PSELSCK': {
					'address': 0x40004508, 'module': 'SPIS',
					'description': '''Pin select for SCK signal.
RW 0..31: Pin number to route the SPI SCK signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'SPI1_PSELMOSI': {
					'address': 0x4000450C, 'module': 'SPI1',
					'description': '''Pin select for MOSI. Pin number configuration for SPI MOSI signal
RW 0..31: pin number to route the SPI MOSI signal to
W 0xFFFFFFFF: Disconnect.''',
				},
			'TWI1_PSELSDA': {
					'address': 0x4000450C, 'module': 'TWI1',
					'description': '''Pin select for SDA. Pin number configuration for TWI SDA signal
RW [0..31] Pin number to route the TWI SDA signal to
W 0xFFFFFFFF Disconnect''',
				},
			'SPIS_PSELMISO': {
					'address': 0x4000450C, 'module': 'SPIS',
					'description': '''Pin select for MISO.
RW 0..31: Pin number to route the SPI MISO signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'SPI1_PSELMISO': {
					'address': 0x40004510, 'module': 'SPI1',
					'description': '''Pin select for MISO. Pin number configuration for SPI master MISO signal
RW 0..31: Pin number to route the SPI master MISO signal to
W 0xFFFFFFFF: Disconnect.''',
				},
			'SPIS_PSELMOSI': {
					'address': 0x40004510, 'module': 'SPIS',
					'description': '''Pin select for MOSI.
RW 0..31: Pin number to route the SPI MOSI signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'SPIS_PSELCSN': {
					'address': 0x40004514, 'module': 'SPIS',
					'access': 'R/W',
					'default': 0xFFFFFFFF,
					'description': '''Pin select for CSN
RW 0..31: Pin number to route the SPI CSN signal to
W 0xFFFFFFFF: Disconnect''',
				},
			'SPI1_RXD': {
					'address': 0x40004518, 'module': 'SPI1',
					'description': 'RxD register',
					'bitfields': {
						'RXD': {
							'slice': (7,0),
							'description': '''RX data received. Double buffered.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'TWI1_RXD': {
					'address': 0x40004518, 'module': 'TWI1',
					'description': 'RXD register',
					'bitfields': {
							'RXD': {
									'slice': (7,0),
									'description': '''RX data from last transfer''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'SPI1_TXD': {
					'address': 0x4000451C, 'module': 'SPI1',
					'description': 'TxD register',
					'bitfields': {
						'TXD': {
							'slice': (7,0),
							'description': '''TX data to send. Double buffered.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'TWI1_TXD': {
					'address': 0x4000451C, 'module': 'TWI1',
				'description': 'TXD register',
				'bitfields': {
						'slice': (7,0),
						'description': 'TX data for next transfer',
						'access': 'R/W',
						'default': 0,
					},
				},
			'SPI1_FREQUENCY': {
					'address': 0x40004524, 'module': 'SPI1',
					'description': '''SPI frequency. SPI master data rate.
0x02000000: (K125) 125 Kbps
0x04000000: (K250) 250 Kbps
0x08000000: (K500) 500 Kbps
0x10000000: (M1) 1 Mbps
0x20000000: (M2) 2 Mbps
0x40000000: (M4) 4 Mbps
0x80000000: (M8) 8 Mbps''',
					'default': 0,
					'access': 'R/W',
				},
			'TWI1_FREQUENCY': {
					'address': 0x40004524, 'module': 'TWI1',
					'access': 'R/W',
					'default': 0x04000000,
					'description': '''TWI frequency. TWI master clock frequency
0x01980000 (K100): 100 Kbps
0x40000000 (K250): 250 Kbps
0x06680000 (K400): 400 Kbps''',
				},
			'SPI1_CONFIG': {
					'address': 0x40004554, 'module': 'SPI1',
					'description': 'Configuration register',
					'bitfields': {
							'ORDER': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: MSB first
1: LSB first''',
								},
							'CPOL': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: Active high
1: Active low''',
								},
							'CPHA': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: leading - sample on leading edge of clock, shift serial data on trailing edge
1: trailing - sample on trailing edge of clock, shift serial data on leading edge.''',
								},
						},
				},
			'SPIS_RXDPTR': {
					'address': 0x40004534, 'module': 'SPIS',
					'description': 'RXD data pointer',
					'access': 'R/W',
					'default': 0,
				},
			'SPIS_MAXRX': {
					'address': 0x40004538, 'module': 'SPIS',
					'description': 'Maximum number of bytes in receive buffer.',
					'bitfields': {
							'MAXRX': {
									'slice': (7,0),
									'access': 'R/W',
									'default': 0,
									'description': 'Maximum number of bytes in receive buffer',
								},
						},
				},
			'SPIS_AMOUNTRX': {
					'address': 0x4000453C, 'module': 'SPIS',
					'description': 'Number of bytes received in last granted transaction.',
					'bitfields': {
							'AMOUNTRX': {
									'slice': (7,0),
									'access': 'R/W',
									'default': 0,
									'description': 'Number of bytes received in the last granted transaction.',
								},
						},
				},
			'SPIS_TXDPTR': {
					'address': 0x40004544, 'module': 'SPIS',
					'description': 'TXD data pointer',
					'access': 'R/W',
					'default': 0,
				},
			'SPIS_MAXTX': {
					'address': 0x40004548, 'module': 'SPIS',
					'description': 'Maximum number of bytes in transmit buffer.',
					'bitfields': {
							'MAXTX': {
									'slice': (7,0),
									'access': 'R/W',
									'default': 0,
									'description': 'Maximum number of bytes in transmit buffer.',
								},
						},
				},
			'SPIS_AMOUNTTX': {
					'address': 0x4000454C, 'module': 'SPIS',
					'description': 'Numberof bytes transmitted in last granted transaction.',
					'bitfields': {
							'AMOUNTTX': {
								'slice': (7,0),
								'access': 'R/W',
								'default': 0,
								'description': 'Number of bytes transmitted in the last granted transaction.',
								}
						},
				},
			'SPIS_CONFIG': {
					'address': 0x40004554, 'module': 'SPIS',
					'description': 'Configuration register',
					'bitfields': {
							'ORDER': {
									'slice': (0,),
									'description': '''Bit order.
0: MSB first
1: LSB first''',
								},
							'CPHA': {
									'slice': (1,),
									'description': '''Serial clock (SCK) phase.
0: Sample on leading edge of clock, shift serial data on trailing edge
1: Sampe on training edge of clock, shift serial data on leading edge''',
								},
							'CPOL': {
									'slice': (2,),
									'description': '''Serial clock (SCK) polarity
0: Active high
1: Active low''',
								},
						},
				},
			'SPIS_DEF': {
					'address': 0x4000455C, 'module': 'SPIS',
					'description': 'Default character. Character clocked out in case of an ignored transaction.',
					'bitfields': {
							'DEF': {
									'slice': (7,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Default character. Clocked out on MISO during an ignored transaction.''',
								},
						},
				},
			'SPI1_RXD': {
					'address': 0x40004518, 'module': 'SPI1',
					'description': 'RxD register',
					'bitfields': {
						'RXD': {
							'slice': (7,0),
							'description': '''RX data received. Double buffered.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'TWI1_RXD': {
					'address': 0x40004518, 'module': 'TWI1',
					'description': 'RXD register',
					'bitfields': {
						'RXD': {
							'slice': (7,0),
							'description': '''RX data from last transfer''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'SPI1_TXD': {
					'address': 0x4000451C, 'module': 'SPI1',
					'description': 'TxD register',
					'bitfields': {
						'TXD': {
							'slice': (7,0),
							'description': '''TX data to send. Double buffered.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'TWI1_TXD': {
					'address': 0x4000451C, 'module': 'TWI1',
				'description': 'TXD register',
				'bitfields': {
					'TXD': {
						'slice': (7,0),
						'description': 'TX data for next transfer',
						'access': 'R/W',
						'default': 0,
						},
					},
				},
			'SPI1_FREQUENCY': {
					'address': 0x40004524, 'module': 'SPI1',
					'description': '''SPI frequency. SPI master data rate.
0x02000000: (K125) 125 Kbps
0x04000000: (K250) 250 Kbps
0x08000000: (K500) 500 Kbps
0x10000000: (M1) 1 Mbps
0x20000000: (M2) 2 Mbps
0x40000000: (M4) 4 Mbps
0x80000000: (M8) 8 Mbps''',
					'default': 0,
					'access': 'R/W',
				},
			'TWI1_FREQUENCY': {
					'address': 0x40004524, 'module': 'TWI1',
					'access': 'R/W',
					'default': 0x04000000,
					'description': '''TWI frequency. TWI master clock frequency
0x01980000 (K100): 100 Kbps
0x40000000 (K250): 250 Kbps
0x06680000 (K400): 400 Kbps''',
				},
			'SPI1_CONFIG': {
					'address': 0x40004554, 'module': 'SPI1',
					'description': 'Configuration register',
					'bitfields': {
							'ORDER': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: MSB first
1: LSB first''',
								},
							'CPOL': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: Active high
1: Active low''',
								},
							'CPHA': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''0: leading - sample on leading edge of clock, shift serial data on trailing edge
1: trailing - sample on trailing edge of clock, shift serial data on leading edge.''',
								},
						},
				},
			'SPIS_ORC': {
					'address': 0x400045C0, 'module': 'SPIS',
					'description': 'Over-read character.',
					'bitfields': {
							'ORC': {
								'slice': (7,0),
								'description': '''Character clocked out after an over-read of the transmit buffer.''',
								'access': 'R/W',
								'default': 0,
							},
						},
				},

			#### 6000: GPIOTE (T = task, E = event)  ####
			# 'GPIOTE_TASK0': { 'address': 0x40006000, },
			'GPIOTE_OUT0': {
					'address': 0x40006000, 'module': 'GPIOTE',
					'description': 'Task for writing to pin specified by PSEL in CONFIG[0]',
				},
			# 'GPIOTE_TASK1': { 'address': 0x40006004, },
			'GPIOTE_OUT1': {
					'address': 0x40006004, 'module': 'GPIOTE',
					'description': 'Task for writing to pin specified by PSEL in CONFIG[1]',
				},
			# 'GPIOTE_TASK2': { 'address': 0x40006008, },
			'GPIOTE_OUT2': {
					'address': 0x40006008, 'module': 'GPIOTE',
					'description': 'Task for writing to pin specified by PSEL in CONFIG[2]',
				},
			# 'GPIOTE_TASK3': { 'address': 0x4000600C, },
			'GPIOTE_OUT3': {
					'address': 0x4000600C, 'module': 'GPIOTE',
					'description': 'Task for writing to pin specified by PSEL in CONFIG[3]',
				},
			# 'GPIOTE_EVENT0': { 'address': 0x40006100, },
			'GPIOTE_IN0': {
					'address': 0x40006100, 'module': 'GPIOTE',
					'description': 'Event generated from pin specified by PSEL in CONFIG[0]',
				},
			# 'GPIOTE_EVENT1': { 'address': 0x40006104, },
			'GPIOTE_IN1': {
					'address': 0x40006104, 'module': 'GPIOTE',
					'description': 'Event generated from pin specified by PSEL in CONFIG[1]',
				},
			# 'GPIOTE_EVENT2': { 'address': 0x40006108, },
			'GPIOTE_IN2': {
					'address': 0x40006108, 'module': 'GPIOTE',
					'description': 'Event generated from pin specified by PSEL in CONFIG[2]',
				},
			# 'GPIOTE_EVENT3': { 'address': 0x4000610C, },
			'GPIOTE_IN3': {
					'address': 0x4000610C, 'module': 'GPIOTE',
					'description': 'Event generated from pin specified by PSEL in CONFIG[3]',
				},
			# 'GPIOTE_EVENT31': { 'address': 0x4000617C, },
			'GPIOTE_PORT': {
					'address': 0x4000617C, 'module': 'GPIOTE',
					'description': 'Event generate from multiple input pins',
				},
			# 'GPIOTE_SHORTS':  { 'address': 0x40006200, 'module': 'GPIOTE', },
			'GPIOTE_INTENSET':{
					'address': 0x40006304, 'module': 'GPIOTE',
					'description': 'Interrupt enable set register',
				},
			'GPIOTE_INTENCLR': {
					'address': 0x40006308, 'module': 'GPIOTE',
					'description': 'Interrupt enable clear register',
				},
			'GPIOTE_CONFIG0': {
					'address': 0x40006510, 'module': 'GPIOTE',
					'description': 'Configuration for OUT[0] task and IN[0] event',
					'bitfields': {
							'MODE': {
									'slice': (1,0),
									'description': '''0: Disabled. Pin specified by PSEL will not be acquired by the GPIOTE module.
1: Event mode. The pin specified by PSEL will be configured as an input and the IN[n] event will be generated if operation specified in POLARITY occurrs on the pin.
3: Task mode. The pin specified by PSEL will be configured as an output and triggering the OUT[n] task will perform the operation specified by POLARITY on the pin. When enabled as a task the GPIOTE module will acquire the pin and the pin can no longer be written as a regular output pin from the GPIO module.''',
								},
							'PSEL': {
									'slice': (12,8),
									'description': '''Pin number associated with OUT[n] task and IN[n] event.''',
								},
							'POLARITY': {
									'slice': (17,16),
									'description': '''When in task mode: Operation to be performed on output when OUT[n] task is triggered.
When in Event mode: Operation on input that shall trigger IN[n] event.
1 (LOTOHI): Task mode: Set pin from OUT[n] task. Event mode: Generate IN[n] event when rising edge on pin.
2 (HITOLO): Task mode: Clear pin from OUT[n] task. Event mode: Generate IN[n] event when falling edge on pin.
3 (TOGGLE): Task mode: Toggle pin from OUT[n]. Event mode: Generate IN[n] event when falling edge on pin.''',
								},
							'OUTINIT': {
									'slice': (20,),
									'description': '''When in event mode: No effect.
0 (LOW): Task mode: Initial value of pin before task triggering is low.
1 (HIGH): Task mode: Initial value of pin before task triggering is high.''',
								},
						},
				},
			'GPIOTE_CONFIG1': {
					'address': 0x40006514, 'module': 'GPIOTE',
					'description': 'Configuration for OUT[1] task and IN[1] event',
					'bitfields': {
							'MODE': {
									'slice': (1,0),
									'description': '''0: Disabled. Pin specified by PSEL will not be acquired by the GPIOTE module.
1: Event mode. The pin specified by PSEL will be configured as an input and the IN[n] event will be generated if operation specified in POLARITY occurrs on the pin.
3: Task mode. The pin specified by PSEL will be configured as an output and triggering the OUT[n] task will perform the operation specified by POLARITY on the pin. When enabled as a task the GPIOTE module will acquire the pin and the pin can no longer be written as a regular output pin from the GPIO module.''',
								},
							'PSEL': {
									'slice': (12,8),
									'description': '''Pin number associated with OUT[n] task and IN[n] event.''',
								},
							'POLARITY': {
									'slice': (17,16),
									'description': '''When in task mode: Operation to be performed on output when OUT[n] task is triggered.
When in Event mode: Operation on input that shall trigger IN[n] event.
1 (LOTOHI): Task mode: Set pin from OUT[n] task. Event mode: Generate IN[n] event when rising edge on pin.
2 (HITOLO): Task mode: Clear pin from OUT[n] task. Event mode: Generate IN[n] event when falling edge on pin.
3 (TOGGLE): Task mode: Toggle pin from OUT[n]. Event mode: Generate IN[n] event when falling edge on pin.''',
								},
							'OUTINIT': {
									'slice': (20,),
									'description': '''When in event mode: No effect.
0 (LOW): Task mode: Initial value of pin before task triggering is low.
1 (HIGH): Task mode: Initial value of pin before task triggering is high.''',
								},
						},
				},
			'GPIOTE_CONFIG2': {
					'address': 0x40006518, 'module': 'GPIOTE',
					'description': 'Configuration for OUT[2] task and IN[2] event',
					'bitfields': {
							'MODE': {
									'slice': (1,0),
									'description': '''0: Disabled. Pin specified by PSEL will not be acquired by the GPIOTE module.
1: Event mode. The pin specified by PSEL will be configured as an input and the IN[n] event will be generated if operation specified in POLARITY occurrs on the pin.
3: Task mode. The pin specified by PSEL will be configured as an output and triggering the OUT[n] task will perform the operation specified by POLARITY on the pin. When enabled as a task the GPIOTE module will acquire the pin and the pin can no longer be written as a regular output pin from the GPIO module.''',
								},
							'PSEL': {
									'slice': (12,8),
									'description': '''Pin number associated with OUT[n] task and IN[n] event.''',
								},
							'POLARITY': {
									'slice': (17,16),
									'description': '''When in task mode: Operation to be performed on output when OUT[n] task is triggered.
When in Event mode: Operation on input that shall trigger IN[n] event.
1 (LOTOHI): Task mode: Set pin from OUT[n] task. Event mode: Generate IN[n] event when rising edge on pin.
2 (HITOLO): Task mode: Clear pin from OUT[n] task. Event mode: Generate IN[n] event when falling edge on pin.
3 (TOGGLE): Task mode: Toggle pin from OUT[n]. Event mode: Generate IN[n] event when falling edge on pin.''',
								},
							'OUTINIT': {
									'slice': (20,),
									'description': '''When in event mode: No effect.
0 (LOW): Task mode: Initial value of pin before task triggering is low.
1 (HIGH): Task mode: Initial value of pin before task triggering is high.''',
								},
						},
				},
			'GPIOTE_CONFIG3': {
					'address': 0x4000651C, 'module': 'GPIOTE',
					'description': 'Configuration for OUT[3] task and IN[3] event',
					'bitfields': {
							'MODE': {
									'slice': (1,0),
									'description': '''0: Disabled. Pin specified by PSEL will not be acquired by the GPIOTE module.
1: Event mode. The pin specified by PSEL will be configured as an input and the IN[n] event will be generated if operation specified in POLARITY occurrs on the pin.
3: Task mode. The pin specified by PSEL will be configured as an output and triggering the OUT[n] task will perform the operation specified by POLARITY on the pin. When enabled as a task the GPIOTE module will acquire the pin and the pin can no longer be written as a regular output pin from the GPIO module.''',
								},
							'PSEL': {
									'slice': (12,8),
									'description': '''Pin number associated with OUT[n] task and IN[n] event.''',
								},
							'POLARITY': {
									'slice': (17,16),
									'description': '''When in task mode: Operation to be performed on output when OUT[n] task is triggered.
When in Event mode: Operation on input that shall trigger IN[n] event.
1 (LOTOHI): Task mode: Set pin from OUT[n] task. Event mode: Generate IN[n] event when rising edge on pin.
2 (HITOLO): Task mode: Clear pin from OUT[n] task. Event mode: Generate IN[n] event when falling edge on pin.
3 (TOGGLE): Task mode: Toggle pin from OUT[n]. Event mode: Generate IN[n] event when falling edge on pin.''',
								},
							'OUTINIT': {
									'slice': (20,),
									'description': '''When in event mode: No effect.
0 (LOW): Task mode: Initial value of pin before task triggering is low.
1 (HIGH): Task mode: Initial value of pin before task triggering is high.''',
								},
						},
				},

			#### 7000: ADC ####
			# 'ADC_TASK0': { 'address': 0x40007000, },
			'ADC_START': {
					'address': 0x40007000, 'module':  'ADC',
					'description': '''Start a new ADC conversion.''',
				},
			# 'ADC_TASK1': { 'address': 0x40007004, },
			'ADC_STOP': {
					'address': 0x40007004, 'module':  'ADC',
					'description': '''Stop ADC.''',
				},
			# 'ADC_EVENT0': { 'address': 0x40007100, },
			'ADC_END': {
					'address': 0x40007100, 'module':  'ADC',
					'description': '''An ADC conversion is completed''',
				},
			# 'ADC_SHORTS':  { 'address': 0x40007200, 'module': 'ADC', },
			'ADC_INTENSET':{
					'address': 0x40007304, 'module':  'ADC',
					'description': '''Interrupt enable set register''',
				},
			'ADC_INTENCLR':{
					'address': 0x40007308, 'module':  'ADC',
					'description': 'Interrupt enable clear register',
				},
			# 'ADC_REG0':    { 'address': 0x40007400, },
			'ADC_BUSY':    {
					'address': 0x40007400, 'module':  'ADC',
					'description': 'ADC busy (conversion in progress)',
					'bitfields': {
						'BUSY': {
							'slice': (0,),
							'access': 'R',
							'default': 0,
							'description': '''0: ADC is ready. No ongoing conversion.
1: ADC is busy. Conversion in progress.''',
						},
					},
				},
			'ADC_ENABLE': {
					'address': 0x40007500, 'module':  'ADC',
					'description': '''Enable ADC. When enabled, the ADC will acquire access to the analog input pins specified in the CONFIG register.''',
					'bitfields': {
							'VAL': {
									'slice': (1,0),
									'access': 'R/W',
									'description': '''0: ADC disabled.
1: ADC enabled.''',
								},
						},
				},
			'ADC_CONFIG': {
					'address': 0x40007504, 'module':  'ADC',
					'description': '''ADC configuration''',
					'bitfields': {
							'RES': {
									'slice': (1,0),
									'access': 'R/W',
									'default': 0,
									'description': '''ADC resolution.
0 (8_BIT): 8 bit
1 (9_BIT): 9 bit
2 (10_BIT): 10 bit''',
								},
							'INPSEL': {
									'slice': (4,2),
									'access': 'R/W',
									'default': 0,
									'description': '''ADC input selection.
0 (AIN_NO_PS):  Analog input pin specified by CONFIG.PSEL with no prescaling.
1 (AIN_2_3_PS): Analog input pin specified by CONFIG. PSEL with 2/3 prescaling. 
2 (AIN_1_3_PS): Analog input pin specified by CONFIG. PSEL with 1/3 prescaling.
5 (VDD_2_3_PS): VDD with 2/3 prescaling.
6 (VDD_1_3_PS): VDD with 1/3 prescaling.''',
								},
							'REFSEL': {
									'slice': (6,5),
									'access': 'R/W',
									'default': 0,
									'description': '''ADC reference selection
0 (VBG): Use internal 1.2 V band gap reference.
1 (EXT): Use external reference specified by CONCFIG EXTREFSEL.
2 (VDD_1_2_PS): Use VDD with 1/2 prescaling. (Only applicable when VDD is in the range 1.7V - 2.6V ).
3 (VDD_1_3_PS): Use VDD with 1/3 prescaling. (Only applicable when VDD is in the range 2.5V - 3.6V ).''',
								},
							'PSEL': {
									'slice': (15,8),
									'access': 'R/W',
									'default': 0,
									'description': '''Select pin to be used as ADC input pin.
0 (DISABLE): Analog input pins disabled.
1 (AIN0):    Use AIN0 as analog input.
2 (AIN1):    Use AIN1 as analog input.
4 (AIN2):    Use AIN2 as analog input.
8 (AIN3):    Use AIN3 as analog input.
16 (AIN4):   Use AIN4 as analog input.
32 (AIN5):   Use AIN5 as analog input.
64 (AIN6):   Use AIN6 as analog input.
128 (AIN7):  Use AIN7 as analog input.''',
								},
							'EXTREFSEL': {
									'slice': (17,16),
									'access': 'R/W',
									'default': 0,
									'description': '''External reference pin selection.
0 (NONE):  Analog reference inputs disabled.
1 (AREF0): Use AREF0 as analog reference.
2 (AREF1): Use AREF1 as analog reference.''',
								},
						},
				},
			'ADC_RESULT': {
					'address': 0x40007508, 'module':  'ADC',
					'description': '''Result of the previous ADC conversion''',
					'bitfields': {
							'RESULT': {
									'slice': (9,0),
									'access': 'R',
									'default': 0,
									'description': '''0..1023: Result of the previous ADC conversion. The value is updated for every completed ADC conversion. The result value is relative to the selected ADC reference input. If the sampled analog input signal is equal to or greater than the ADC reference signal, the result value will be set to the maximum (limited by the selected ADC bit width). The value is right justified (LSB of sample value always on register bit 0).''',
								},
						},
				},

			#### 8000: Timer0 ####
			# 'TIMER0_TASK0': { 'address': 0x40008000, },
			'TIMER0_START': {
					'address': 0x40008000, 'module': 'TIMER0',
					'description': 'Start timer',
				},
			# 'TIMER0_TASK1': { 'address': 0x40008004, },
			'TIMER0_STOP': {
					'address': 0x40008004, 'module': 'TIMER0',
					'description': 'Stop timer',
				},
			# 'TIMER0_TASK2': { 'address': 0x40008008, },
			'TIMER0_COUNT': {
					'address': 0x40008008, 'module': 'TIMER0',
					'description': 'Increment timer (counter mode only)',
				},
			# 'TIMER0_TASK3': { 'address': 0x4000800C, },
			'TIMER0_CLEAR': {
					'address': 0x4000800C, 'module': 'TIMER0',
					'description': 'Clear timer',
				},
			# 'TIMER0_TASK16': { 'address': 0x40008040, },
			'TIMER0_CAPTURE0': {
					'address': 0x40008040, 'module': 'TIMER0',
					'description': 'Capture timer value to CC0 register',
				},
			# 'TIMER0_TASK17': { 'address': 0x40008044, },
			'TIMER0_CAPTURE1': {
					'address': 0x40008044, 'module': 'TIMER0',
					'description': 'Capture timer value to CC1 register',
				},
			# 'TIMER0_TASK18': { 'address': 0x40008048, },
			'TIMER0_CAPTURE2': {
					'address': 0x40008048, 'module': 'TIMER0',
					'description': 'Capture timer value to CC2 register',
				},
			# 'TIMER0_TASK19': { 'address': 0x4000804C, },
			'TIMER0_CAPTURE3': {
					'address': 0x4000804C, 'module': 'TIMER0',
					'description': 'Capture timer value to CC3 register',
				},
			# 'TIMER0_EVENT16': { 'address': 0x40008140, },
			'TIMER0_COMPARE0': {
					'address': 0x40008140, 'module': 'TIMER0',
						'description': 'Compare event on CC[0] match',
				},
			# 'TIMER0_EVENT17': { 'address': 0x40008144, },
			'TIMER0_COMPARE1': {
					'address': 0x40008144, 'module': 'TIMER0',
						'description': 'Compare event on CC[1] match',
				},
			# 'TIMER0_EVENT18': { 'address': 0x40008148, },
			'TIMER0_COMPARE2': {
					'address': 0x40008148, 'module': 'TIMER0',
						'description': 'Compare event on CC[2] match',
				},
			# 'TIMER0_EVENT19': { 'address': 0x4000814C, },
			'TIMER0_COMPARE3': {
					'address': 0x4000814C, 'module': 'TIMER0',
						'description': 'Compare event on CC[3] match',
				},
			'TIMER0_SHORTS':  {
					'address': 0x40008200, 'module': 'TIMER0',
					'description': 'Shortcuts',
					'bitfields': {
							'COMPARE0_CLEAR': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE0 and CLEAR task.''',
								},
							'COMPARE1_CLEAR': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE1 and CLEAR task.''',
								},
							'COMPARE2_CLEAR': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE2 and CLEAR task.''',
								},
							'COMPARE3_CLEAR': {
									'slice': (3,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE3 and CLEAR task.''',
								},
							'COMPARE0_STOP': {
									'slice': (8,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE0 and STOP task.''',
								},
							'COMPARE1_STOP': {
									'slice': (9,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE1 and STOP task.''',
								},
							'COMPARE2_STOP': {
									'slice': (10,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE2 and STOP task.''',
								},
							'COMPARE3_STOP': {
									'slice': (11,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE3 and STOP task.''',
								},
						},
				},
			'TIMER0_INTENSET':{
					'address': 0x40008304, 'module': 'TIMER0',
					'description': 'Interrupt enable set register',
				},
			'TIMER0_INTENCLR':{
					'address': 0x40008308, 'module': 'TIMER0',
					'description': 'Interrupt enable clear register',
				},
			'TIMER0_MODE': {
					'address': 0x40008504, 'module': 'TIMER0',
					'description': 'Timer mode selection',
					'bitfields': {
							'MODE': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Timer mode
0: Select timer mode
1: Select counter mode''',
								},
						},
				},
			'TIMER0_BITMODE': {
					'address': 0x40008508, 'module': 'TIMER0',
					'description': 'Configure the number of bits used by the TIMER',
					'bitfields': {
						'BITMODE': {
							'slice': (1,0),
							'description': '''Timer bit width
0: 16-bit timer bit width
1: 8-bit timer bit width
2: 24-bit timer bit width
3: 32-bit timer bit width''',
						},
					},
				},
			'TIMER0_PRESCALER': {
					'address': 0x40008510, 'module': 'TIMER0',
					'description': 'Timer prescaler register',
					'bitfields': {
							'PRESCALER': {
									'slice': (3,0),
									'description': 'prescaler value 0..9',
									'access': 'R/W',
									'default': 0x4,
								},
						},
				},
			'TIMER0_CC0': {
					'address': 0x40008540, 'module': 'TIMER0',
					'description': 'Capture/Compare register 0',
				},
			'TIMER0_CC1': {
					'address': 0x40008544, 'module': 'TIMER0',
					'description': 'Capture/Compare register 1',
				},
			'TIMER0_CC2': {
					'address': 0x40008548, 'module': 'TIMER0',
					'description': 'Capture/Compare register 2',
				},
			'TIMER0_CC3': {
					'address': 0x4000854C, 'module': 'TIMER0',
					'description': 'Capture/Compare register 3',
				},

			#### 9000: Timer1 ####
			# 'TIMER1_TASK0': { 'address': 0x40009000, },
			'TIMER1_START': {
					'address': 0x40009000, 'module': 'TIMER1',
					'description': 'Start timer',
				},
			# 'TIMER1_TASK1': { 'address': 0x40009004, },
			'TIMER1_STOP': {
					'address': 0x40009004, 'module': 'TIMER1',
					'description': 'Stop timer',
				},
			# 'TIMER1_TASK2': { 'address': 0x40009008, },
			'TIMER1_COUNT': {
					'address': 0x40009008, 'module': 'TIMER1',
					'description': 'Increment timer (counter mode only)',
				},
			# 'TIMER1_TASK3': { 'address': 0x4000900C, },
			'TIMER1_CLEAR': {
					'address': 0x4000900C, 'module': 'TIMER1',
					'description': 'Clear timer',
				},
			# 'TIMER1_TASK16': { 'address': 0x40009040, },
			'TIMER1_CAPTURE0': {
					'address': 0x40009040, 'module': 'TIMER1',
					'description': 'Capture timer value to CC0 register',
				},
			# 'TIMER1_TASK17': { 'address': 0x40009044, },
			'TIMER1_CAPTURE1': {
					'address': 0x40009044, 'module': 'TIMER1',
					'description': 'Capture timer value to CC1 register',
				},
			# 'TIMER1_TASK18': { 'address': 0x40009048, },
			'TIMER1_CAPTURE2': {
					'address': 0x40009048, 'module': 'TIMER1',
					'description': 'Capture timer value to CC2 register',
				},
			# 'TIMER1_TASK19': { 'address': 0x4000904C, },
			'TIMER1_CAPTURE3': {
					'address': 0x4000904C, 'module': 'TIMER1',
					'description': 'Capture timer value to CC3 register',
				},
			# 'TIMER1_EVENT16': { 'address': 0x40009140, },
			'TIMER1_COMPARE0': {
					'address': 0x40009140, 'module': 'TIMER1',
						'description': 'Compare event on CC[0] match',
				},
			# 'TIMER1_EVENT17': { 'address': 0x40009144, },
			'TIMER1_COMPARE1': {
					'address': 0x40009144, 'module': 'TIMER1',
						'description': 'Compare event on CC[1] match',
				},
			# 'TIMER1_EVENT18': { 'address': 0x40009148, },
			'TIMER0_COMPARE2': {
					'address': 0x40008148, 'module': 'TIMER1',
						'description': 'Compare event on CC[2] match',
				},
			# 'TIMER1_EVENT19': { 'address': 0x4000914C, },
			'TIMER1_COMPARE3': {
					'address': 0x4000914C, 'module': 'TIMER1',
						'description': 'Compare event on CC[3] match',
				},
			'TIMER1_SHORTS':  {
					'address': 0x40009200, 'module': 'TIMER1',
					'description': 'Shortcuts',
					'bitfields': {
							'COMPARE0_CLEAR': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE0 and CLEAR task.''',
								},
							'COMPARE1_CLEAR': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE1 and CLEAR task.''',
								},
							'COMPARE2_CLEAR': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE2 and CLEAR task.''',
								},
							'COMPARE3_CLEAR': {
									'slice': (3,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE3 and CLEAR task.''',
								},
							'COMPARE0_STOP': {
									'slice': (8,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE0 and STOP task.''',
								},
							'COMPARE1_STOP': {
									'slice': (9,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE1 and STOP task.''',
								},
							'COMPARE2_STOP': {
									'slice': (10,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE2 and STOP task.''',
								},
							'COMPARE3_STOP': {
									'slice': (11,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE3 and STOP task.''',
								},
						},
				},
			'TIMER1_INTENSET':{
					'address': 0x40009304, 'module': 'TIMER1',
					'description': 'Interrupt enable set register',
				},
			'TIMER1_INTENCLR':{
					'address': 0x40009308, 'module': 'TIMER1',
					'description': 'Interrupt enable clear register',
				},
			'TIMER1_MODE': {
					'address': 0x40009504, 'module': 'TIMER1',
					'description': 'Timer mode selection',
					'bitfields': {
							'MODE': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Timer mode
0: Select timer mode
1: Select counter mode''',
								},
						},
				},
			'TIMER1_BITMODE': {
					'address': 0x40009508, 'module': 'TIMER1',
					'description': 'Configure the number of bits used by the TIMER',
					'bitfields': {
						'BITMODE': {
							'slice': (1,0),
							'description': '''Timer bit width
0: 16-bit timer bit width
1: 8-bit timer bit width
2: 24-bit timer bit width
3: 32-bit timer bit width''',
						},
					},
				},
			'TIMER1_PRESCALER': {
					'address': 0x40009510, 'module': 'TIMER1',
					'description': 'Timer prescaler register',
					'bitfields': {
							'PRESCALER': {
									'slice': (3,0),
									'description': 'prescaler value 0..9',
									'access': 'R/W',
									'default': 0x4,
								},
						},
				},
			'TIMER1_CC0': {
					'address': 0x40009540, 'module': 'TIMER1',
					'description': 'Capture/Compare register 0',
				},
			'TIMER1_CC1': {
					'address': 0x40009544, 'module': 'TIMER1',
					'description': 'Capture/Compare register 1',
				},
			'TIMER1_CC2': {
					'address': 0x40009548, 'module': 'TIMER1',
					'description': 'Capture/Compare register 2',
				},
			'TIMER1_CC3': {
					'address': 0x4000954C, 'module': 'TIMER1',
					'description': 'Capture/Compare register 3',
				},

			#### A000: Timer2 ####
			# 'TIMER2_TASK0': { 'address': 0x4000A000, },
			'TIMER2_START': {
					'address': 0x4000A000, 'module': 'TIMER2',
					'description': 'Start timer',
				},
			# 'TIMER2_TASK1': { 'address': 0x4000A004, },
			'TIMER2_STOP': {
					'address': 0x4000A004, 'module': 'TIMER2',
					'description': 'Stop timer',
				},
			# 'TIMER2_TASK2': { 'address': 0x4000A008, },
			'TIMER2_COUNT': {
					'address': 0x4000A008, 'module': 'TIMER2',
					'description': 'Increment timer (counter mode only)',
				},
			# 'TIMER2_TASK3': { 'address': 0x4000A00C, },
			'TIMER2_CLEAR': {
					'address': 0x4000A00C, 'module': 'TIMER2',
					'description': 'Clear timer',
				},
			# 'TIMER2_TASK16': { 'address': 0x4000A040, },
			'TIMER2_CAPTURE0': {
					'address': 0x4000A040, 'module': 'TIMER2',
					'description': 'Capture timer value to CC0 register',
				},
			# 'TIMER2_TASK17': { 'address': 0x4000A044, },
			'TIMER2_CAPTURE1': {
					'address': 0x4000A044, 'module': 'TIMER2',
					'description': 'Capture timer value to CC1 register',
				},
			# 'TIMER2_TASK18': { 'address': 0x4000A048, },
			'TIMER2_CAPTURE2': {
					'address': 0x4000A048, 'module': 'TIMER2',
					'description': 'Capture timer value to CC2 register',
				},
			# 'TIMER2_TASK19': { 'address': 0x4000A04C, },
			'TIMER2_CAPTURE3': {
					'address': 0x4000904C, 'module': 'TIMER2',
					'description': 'Capture timer value to CC3 register',
				},
			# 'TIMER2_EVENT16': { 'address': 0x4000A140, },
			'TIMER2_COMPARE0': {
					'address': 0x4000A140, 'module': 'TIMER2',
						'description': 'Compare event on CC[0] match',
				},
			# 'TIMER2_EVENT17': { 'address': 0x4000A144, },
			'TIMER2_COMPARE1': {
					'address': 0x4000A144, 'module': 'TIMER2',
						'description': 'Compare event on CC[1] match',
				},
			# 'TIMER2_EVENT19': { 'address': 0x4000A14C, },
			'TIMER2_COMPARE3': {
					'address': 0x4000A14C, 'module': 'TIMER2',
						'description': 'Compare event on CC[3] match',
				},
			'TIMER2_SHORTS':  {
					'address': 0x4000A200, 'module': 'TIMER2',
					'description': 'Shortcuts',
					'bitfields': {
							'COMPARE0_CLEAR': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE0 and CLEAR task.''',
								},
							'COMPARE1_CLEAR': {
									'slice': (1,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE1 and CLEAR task.''',
								},
							'COMPARE2_CLEAR': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE2 and CLEAR task.''',
								},
							'COMPARE3_CLEAR': {
									'slice': (3,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE3 and CLEAR task.''',
								},
							'COMPARE0_STOP': {
									'slice': (8,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE0 and STOP task.''',
								},
							'COMPARE1_STOP': {
									'slice': (9,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE1 and STOP task.''',
								},
							'COMPARE2_STOP': {
									'slice': (10,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE2 and STOP task.''',
								},
							'COMPARE3_STOP': {
									'slice': (11,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between COMPARE3 and STOP task.''',
								},
						},
				},
			'TIMER2_INTENSET':{
					'address': 0x4000A304, 'module': 'TIMER2',
					'description': 'Interrupt enable set register',
				},
			'TIMER2_INTENCLR':{
					'address': 0x4000A308, 'module': 'TIMER2',
					'description': 'Interrupt enable clear register',
				},
			'TIMER2_MODE': {
					'address': 0x4000A504, 'module': 'TIMER2',
					'description': 'Timer mode selection',
					'bitfields': {
							'MODE': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Timer mode
0: Select timer mode
1: Select counter mode''',
								},
						},
				},
			'TIMER2_BITMODE': {
					'address': 0x4000A508, 'module': 'TIMER2',
					'description': 'Configure the number of bits used by the TIMER',
					'bitfields': {
						'BITMODE': {
							'slice': (1,0),
							'description': '''Timer bit width
0: 16-bit timer bit width
1: 8-bit timer bit width
2: 24-bit timer bit width
3: 32-bit timer bit width''',
						},
					},
				},
			'TIMER2_PRESCALER': {
					'address': 0x4000A510, 'module': 'TIMER2',
					'description': 'Timer prescaler register',
					'bitfields': {
							'PRESCALER': {
									'slice': (3,0),
									'description': 'prescaler value 0..9',
									'access': 'R/W',
									'default': 0x4,
								},
						},
				},
			'TIMER2_CC0': {
					'address': 0x4000A540, 'module': 'TIMER2',
					'description': 'Capture/Compare register 0',
				},
			'TIMER2_CC1': {
					'address': 0x4000A544, 'module': 'TIMER2',
					'description': 'Capture/Compare register 1',
				},
			'TIMER3_CC2': {
					'address': 0x4000A548, 'module': 'TIMER2',
					'description': 'Capture/Compare register 2',
				},
			'TIMER3_CC3': {
					'address': 0x4000A54C, 'module': 'TIMER2',
					'description': 'Capture/Compare register 3',
				},

			#### B000: RTC0 ####
			# 'RTC0_TASK0': { 'address': 0x4000B000, },
			'RTC0_START': {
					'address': 0x4000B000, 'module': 'RTC0',
					'description': 'Start RTC COUNTER',
				},
			# 'RTC0_TASK1': { 'address': 0x4000B004, },
			'RTC0_STOP': {
					'address': 0x4000B004, 'module': 'RTC0',
					'description': 'Stop RTC COUNTER',
				},
			# 'RTC0_TASK2': { 'address': 0x4000B008, },
			'RTC0_CLEAR': {
					'address': 0x4000B008, 'module': 'RTC0',
					'description': 'Clear RTC COUNTER',
				},
			# 'RTC0_TASK3': { 'address': 0x4000B00C, },
			'RTC0_TRIGOVRFLW': {
					'address': 0x4000B00C, 'module': 'RTC0',
					'description': 'Set COUNTER to 0xFFFF0.',
				},
			# 'RTC0_EVENT0': { 'address': 0x4000B100, },
			'RTC0_TICK': {
					'address': 0x4000B100, 'module': 'RTC0',
					'description': 'Event on COUNTER increment',
				},
			# 'RTC0_EVENT1': { 'address': 0x4000B104, },
			'RTC0_OVRFLW': {
					'address': 0x4000B104, 'module': 'RTC0',
					'description': 'Event on COUNTER overflow',
				},
			# 'RTC0_EVENT16': { 'address': 0x4000B140, },
			'RTC0_COMPARE0': {
					'address': 0x4000B140, 'module': 'RTC0',
					'description': 'Compare event on CC[0] match.',
				},
			# 'RTC0_EVENT17': { 'address': 0x4000B144, },
			'RTC0_COMPARE1': {
					'address': 0x4000B144, 'module': 'RTC0',
					'description': 'Compare event on CC[1] match.',
				},
			# 'RTC0_EVENT18': { 'address': 0x4000B148, },
			'RTC0_COMPARE2': {
					'address': 0x4000B148, 'module': 'RTC0',
					'description': 'Compare event on CC[2] match.',
				},
			# 'RTC0_EVENT19': { 'address': 0x4000B14C, },
			'RTC0_COMPARE3': {
					'address': 0x4000B14C, 'module': 'RTC0',
					'description': 'Compare event on CC[3] match.',
				},
			# 'RTC0_SHORTS':  { 'address': 0x4000B200, 'module': 'RTC0', },
			'RTC0_INTENSET':{
					'address': 0x4000B304, 'module': 'RTC0',
					'description': 'Configures which events shall generate an RTC interrupt',
				},
			'RTC0_INTENCLR':{
					'address': 0x4000B308, 'module': 'RTC0',
					'description': 'Configures which events shall not generate an RTC interrupt',
				},
			'RTC0_EVTEN': {
					'address': 0x4000B340, 'module': 'RTC0',
					'description': 'Enable or disable event routing to PPI',
					'bitfields': {
							'TICK': {
									'slice': (0,),
									'access': 'R/W',
									'description': '''Enable or disable routing of TICK event to PPI.
1: Enable
0: Disable''',
								},
							'OVERFLW': {
									'slice': (1,),
									'access': 'R/W',
									'description': '''Enable or disable routing of OVRFLW event to PPI.''',
								},
							'COMPARE0': {
									'slice': (16,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[0]event to PPI.''',
								},
							'COMPARE1': {
									'slice': (17,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[1]event to PPI.''',
								},
							'COMPARE2': {
									'slice': (18,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[2]event to PPI.''',
								},
							'COMPARE3': {
									'slice': (19,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[3]event to PPI.''',
								}
						},
				},
			'RTC0_EVTENSET': {
					'address': 0x4000B344, 'module': 'RTC0',
					'description': 'Enable event routing to PPI',
					'bitfields': {
							'TICK': {
								'slice': (0,),
								'description': '''Enable routing of TICK event to PPI.
W1: Enable
R0: Disabled (readback bit0 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'OVRFLW': {
									'slice': (1,),
									'description': '''Enable routing of OVRFLW event to PPI.
W1: Enable
R0: Disabled (readback bit1 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'COMPARE0': {
									'slice': (16,),
									'description': '''Enable routing of COMPARE[0] event to PPI.
W1: Enable
R0: Disabled (readback bit 16 of EVTEN)
R1: Enabled (readback bit 16 of EVTEN)''',
								},
							'COMPARE1': {
									'slice': (17,),
									'description': '''Enable routing of COMPARE[1] event to PPI.
W1: Enable
R0: Disabled (readback bit 17 of EVTEN)
R1: Enabled (readback bit 17 of EVTEN)''',
								},
							'COMPARE2': {
									'slice': (18,),
									'description': '''Enable routing of COMPARE[2] event to PPI.
W1: Enable
R0: Disabled (readback bit 18 of EVTEN)
R1: Enabled (readback bit 18 of EVTEN)''',
								},
							'COMPARE3': {
									'slice': (19,),
									'description': '''Enable routing of COMPARE[3] event to PPI.
W1: Enable
R0: Disabled (readback bit 19 of EVTEN)
R1: Enabled (readback bit 19 of EVTEN)''',
								},
						},
				},
			'RTC0_EVTENCLR': {
					'address': 0x4000B348, 'module': 'RTC0',
					'description': 'Disable event routing to PPI',
					'bitfields': {
							'TICK': {
								'slice': (0,),
								'description': '''Disable routing of TICK event to PPI.
W1: Disable
R0: Disabled (readback bit0 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'OVRFLW': {
									'slice': (1,),
									'description': '''Disable routing of OVRFLW event to PPI.
W1: Disable
R0: Disabled (readback bit1 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'COMPARE0': {
									'slice': (16,),
									'description': '''Disable routing of COMPARE[0] event to PPI.
W1: Disable
R0: Disabled (readback bit 16 of EVTEN)
R1: Enabled (readback bit 16 of EVTEN)''',
								},
							'COMPARE1': {
									'slice': (17,),
									'description': '''Disable routing of COMPARE[1] event to PPI.
W1: Disable
R0: Disabled (readback bit 17 of EVTEN)
R1: Enabled (readback bit 17 of EVTEN)''',
								},
							'COMPARE2': {
									'slice': (18,),
									'description': '''Enable routing of COMPARE[2] event to PPI.
W1: Disable
R0: Disabled (readback bit 18 of EVTEN)
R1: Enabled (readback bit 18 of EVTEN)''',
								},
							'COMPARE3': {
									'slice': (19,),
									'description': '''Disable routing of COMPARE[3] event to PPI.
W1: Disable
R0: Disabled (readback bit 19 of EVTEN)
R1: Enabled (readback bit 19 of EVTEN)''',
								},
						},
				},
			'RTC0_COUNTER': {
					'address': 0x4000B504, 'module': 'RTC0',
						'description': 'Current COUNTER value',
						'bitfields': {
								'COUNTER': {
										'slice': (23,0),
										'description': 'Counter value',
										'default': 0,
									},
							},
					},
			'RTC0_PRESCALER': {
					'address': 0x4000B508, 'module': 'RTC0',
					'description': '12 bit prescaler for COUNTER frequency (32768/(PRESCALER+1)).  Must be written when RTC is stopped',
					'bitfields': {
						'PRESCALER': {
								'slice': (11,0),
								'description': 'PRESCALER value',
								'default': 0,
							},
						},
				},
			'RTC0_CC0': {
					'address': 0x4000B540, 'module': 'RTC0',
					'description': 'Compare register',
					'bitfields': {
							'CC0': {
									'slice': (23,0),
									'description': 'Compare value',
									'default': 0,
								},
						},
				},
			'RTC0_CC1': {
					'address': 0x4000B544, 'module': 'RTC0',
					'description': 'Compare register',
				},
			'RTC0_CC2': {
					'address': 0x4000B548, 'module': 'RTC0',
					'description': 'Compare register',
				},
			'RTC0_CC3': {
					'address': 0x4000B54C, 'module': 'RTC0',
					'description': 'Compare register',
				},

			#### C000: Temperature sensor ####
			# 'TEMP_TASK0': { 'address': 0x4000C000, },
			'TEMP_START': {
					'address': 0x4000C000, 'module': 'TEMP',
					'description': 'Start temperature measurement.',
				},
			# 'TEMP_TASK1': { 'address': 0x4000C004, },
			'TEMP_STOP': {
					'address': 0x4000C004, 'module': 'TEMP',
					'description': 'Stop temperature measurement.',
				},
			# 'TEMP_EVENT0': { 'address': 0x4000C100, },
			'TEMP_DATARDY': {
					'address': 0x4000C100, 'module': 'TEMP',
					'description': 'Temperature measurement complete, data ready.',
				},
			# 'TEMP_SHORTS':  { 'address': 0x4000C200, 'module': 'TEMP',},
			'TEMP_INTENSET': {
					'address': 0x4000C304, 'module': 'TEMP',
					'description': 'Interrupt enable set register.',
				},
			'TEMP_INTENCLR':{
					'address': 0x4000C308, 'module': 'TEMP',
					'description': 'Interrupt enable clear register.',
				},
			'TEMP_TEMP':    {
					'address': 0x4000C508, 'module': 'TEMP',
					'description': '''Temperature. Result of temperature measurement. Die temperature in deg-C, 2's complement format, 0.25 deg-C precision.  Decision point: DATARDY.''',
				},

			#### D000: Random number generator ####
			# 'RNG_TASK0': { 'address': 0x4000D000, },
			'RNG_START': {
					'address': 0x4000D000, 'module': 'RNG',
					'description': 'Task starting the random number generator.',
				},
			# 'RNG_TASK1': { 'address': 0x4000D004, },
			'RNG_STOP': {
					'address': 0x4000D004, 'module': 'RNG',
					'description': 'Task stopping the random number generator.',
				},
			# 'RNG_EVENT0': { 'address': 0x4000D100, },
			'RNG_VALRDY': {
					'address': 0x4000D100, 'module': 'RNG',
					'description': 'Event being generated for every new random number written to the VALUE register.',
				},
			'RNG_SHORTS':  {
					'address': 0x4000D200, 'module': 'RNG',
					'description': 'Shortcut register.',
					'bitfields': {
							'VALRDY_STOP': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Shortcut between VALUE event and STOP task.
0: Disable
1: Enable''',
								},
						},
				},
			'RNG_INTENSET':{
					'address': 0x4000D304, 'module': 'RNG',
					'description': 'Interrupt enable set register.',
				},
			'RNG_INTENCLR':{
					'address': 0x4000D308, 'module': 'RNG',
					'description': 'Interrupt enable clear register.',
				},
			'RNG_CONFIG': {
					'address': 0x4000D504, 'module': 'RNG',
					'description': 'Configuration register.',
					'bitfields': {
							'DERCEN': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Digital error correction
0 Disabled
1 Enabled''',
								},
						},
				},
			'RNG_VALUE': {
					'address': 0x4000D508, 'module': 'RNG',
					'description': 'Output random number.',
					'bitfields': {
							'VALUE': {
									'slice': (7,0),
									'access': 'R/W',
									'default': 0,
									'description': 'Generated random number',
								},
						},
				},

			#### E000: Crypto ECB ####
			# 'ECB_TASK0': { 'address': 0x4000E000, },
			'ECB_STARTECB': {
					'address': 0x4000E000, 'module': 'ECB',
					'description': '''Start ECB block encrypt. If a crypto operation is already running in the AES core, the STARTECB task will not start a new encryption and an ERRORECB event will be triggered.''',
				},
			# 'ECB_TASK1': { 'address': 0x4000E004, },
			'ECB_STOPECB': {
					'address': 0x4000E004, 'module': 'ECB',
					'description': '''Abort a possible executing ECB operation. If a running ECB operation is aborted by STOPECB, the ERRORECB event is triggered.'''
				},
			# 'ECB_EVENT0': { 'address': 0x4000E100, },
			'ECB_ENDECB': {
					'address': 0x4000E100, 'module': 'ECB',
					'description': 'ECB block encrypt complete.',
				},
			# 'ECB_EVENT1': { 'address': 0x4000E104, },
			'ECB_ERRORECB': {
					'address': 0x4000E104, 'module': 'ECB',
					'description': 'ECB block encrypt aborted because of a STOPECB task or due to an error.',
				},
			# 'ECB_SHORTS':  { 'address': 0x4000E200, 'module': 'ECB', },
			'ECB_INTENSET':{
					'address': 0x4000E304, 'module': 'ECB',
					'description': 'Interrupt enable set register.',
				},
			'ECB_INTENCLR':{
					'address': 0x4000E308, 'module': 'ECB',
					'description': 'Interrupt enable clear register.',
				},
			'ECB_ECBDATAPTR': {
					'address': 0x4000E504, 'module': 'ECB',
					'description': 'ECB block encrypt memory pointers.',
				},

			#### F000: AES CCM mode encryption, accelerated CCM, ####
			# 'CCM_TASK0': { 'address': 0x4000F000, 'module': 'CCM', },
			'CCM_KSGEN': {
					'address': 0x4000F000, 'module': 'CCM',
					'description': 'Start generation of key-stream. This operation will stop by itself when completed.'
				},

			# 'CCM_TASK1': { 'address': 0x4000F004, },
			'CCM_CRYPT': {
					'address': 0x4000F004, 'module': 'CCM',
				'description': 'Start encryption/decryption. This operation will stop by itself when completed.',
				},
			# 'CCM_TASK2': { 'address': 0x4000F008, },
			'CCM_STOP': {
					'address': 0x4000F008, 'module': 'CCM',
				'description': 'Stop encryption/decryption',
				},
			# 'CCM_EVENT0': { 'address': 0x4000F100, },
			'CCM_ENDKSGEN': {
					'address': 0x4000F100, 'module': 'CCM',
					'description': 'Key-stream generation complete',
				},
			# 'CCM_EVENT1': { 'address': 0x4000F104, },
			'CCM_ENDCRYPT': {
					'address': 0x4000F104, 'module': 'CCM',
					'description': 'Encrypt/decrypt complete',
				},
			# 'CCM_EVENT2': { 'address': 0x4000F108, },
			'CCM_ERROR': {
					'address': 0x4000F108, 'module': 'CCM',
					'description': 'CCM error event',
				},
			'CCM_SHORTS':  {
					'address': 0x4000F200, 'module': 'CCM',
					'description': 'Shortcut register',
					'bitfields': {
							'ENDKSGEN_CRYPT': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Short-cut between ENDKSGEN event and CRYPT task
0: Disable
1: Enable''',
								},
						},
				},
			'CCM_INTENSET':{
					'address': 0x4000F304, 'module': 'CCM',
					'description': 'Interrupt enable set register',
				},
			'CCM_INTENCLR':{
					'address': 0x4000F308, 'module': 'CCM',
					'description': 'Interrupt enable clear register',
				},
			# 'CCM_REG0':    { 'address': 0x4000F400, },
			'CCM_MICSTATUS':    {
					'address': 0x4000F400, 'module': 'CCM',
					'description': 'MIC check result',
					'bitfields': {
							'MICSTATUS': {
									'slice': (0,),
									'access': 'R',
									'description': '''The result of the MIC check performed during the previous decryption operation.
0: MIC check failed
1: MIC check passed'''
								},
						},
				},
			'CCM_ENABLE':   {
					'address': 0x4000F500, 'module': 'CCM',
					'description': 'Enable',
					'bitfields': {
						'ENABLE': {
							'slice': (1,0),
							'access': 'R',
							'default': 0,
							'description': '''Enable CCM
0: Disable CCM
1: Enable CCM''',
						},
					},
				},
			'CCM_MODE': {
					'address': 0x4000F504, 'module': 'CCM',
					'description': 'Operation mode',
					'bitfields': {
							'MODE': {
									'slice': (0,),
									'access': 'R/W',
									'default': 1,
									'description': '''The mode operation to be used.
0: AES CCM packet encryption mode
1: AES CCM packet decryption mode''',
								},
						},
				},
			'CCM_CNFPTR': {
					'address': 0x4000F508, 'module': 'CCM',
					'description': '''Pointer to data structure holding AES key and NONCE vector.  Pointer to the data structure holding the AES key and the CCM NONCE vector''',
					'access': 'R/W',
				},
			'CCM_INPTR': {
					'address': 0x4000F50C, 'module': 'CCM',
					'description': 'Input pointer',
					'access': 'R/W',
					'default': 0,
				},
			'CCM_OUTPTR': {
					'address': 0x4000F510, 'module': 'CCM',
					'description': 'Output pointer',
					'access': 'R/W',
					'default': 0,
				},
			'CCM_SCRATCHPTR': {
				'address': 0x4000F521,  ######## Odd address!? is it a typo? should it be 520?
				'module': 'CCM',
				'description': '''Pointer to data area used for temporary storage. Pointer to a "scratch" data area used for temporary storage during key-stream generation, MIC generation and encryption/decryption.
The scratch area is used for temporary storage of data during key-stream generation and encryption. A space of minimum 43 bytes must be reserved.''',
			},

			#### 10000: AAR (accelerated address resolver) ####
			'AAR_START': {
					'address': 0x4000F000, 'module': 'AAR',
					'description': 'Start resolving addresses based on IRKs specified in the IRK data structure',
				},
			'AAR_STOP': {
					'address': 0x4000F008, 'module': 'AAR',
					'description': 'Stop resolving addresses',
				},
			'AAR_END': {
					'address': 0x4000F100, 'module': 'AAR',
					'description': 'Address resolution procedure complete',
				},
			'AAR_RESOLVED': {
					'address': 0x4000F104, 'module': 'AAR',
					'description': 'Address resolved',
				},
			'AAR_NOTRESOLVED': {
					'address': 0x4000F108, 'module': 'AAR',
					'description': 'Address not resolved',
				},
			'AAR_INTENSET': {
					'address': 0x4000F304, 'module': 'AAR',
					'description': 'Interrupt enable set register',
				},
			'AAR_INTENCLR': {
					'address': 0x4000F308, 'module': 'AAR',
					'description': 'Interrupt enable clear register',
				},
			'AAR_STATUS': {
					'address': 0x4000F400, 'module': 'AAR',
					'description': 'Resolution status',
					'bitfields': {
							'STATUS': {
									'slice': (3,0),
									'access': 'R',
									'default': 0,
									'description': 'The IRK that was used last time an address was resolved. 0..15.',
								},
						},
				},
			'AAR_ENABLE': {
					'address': 0x4000F500, 'module': 'AAR',
					'description': 'Enable AAR',
					'bitfields': {
							'ENABLE': {
									'slice': (1,0),
									'description': '''Enable or disable AAR.
0: Disable
3: Enable''',
									'default': 0,
									'access': 'R/W',
								},
						},
				},
			'AAR_NIRK': {
					'address': 0x4000F504, 'module': 'AAR',
					'description': 'Number of IRKs',
					'bitfields': {
						'NIRK': {
							'slice': (4,0),
							'description': '''Number of identity root keys available in the IRK data structure. 1..16.''',
							'access': 'R/W',
							'default': 0,
						},
					},
				},
			'AAR_IRKPTR': {
					'address': 0x4000F508, 'module': 'AAR',
					'description': 'Pointer to IRK data structure',
					'access': 'R/W',
					'default': 0,
				},
			'AAR_ADDRPTR': {
					'address': 0x4000F510, 'module': 'AAR',
					'description': 'Pointer to the resolvable address (6 bytes)',
					'access': 'R/W',
					'default': 0,
				},
			'AAR_SCRATCHPTR': {
					'address': 0x4000F514, 'module': 'AAR',
					'description': 'Pointer to the data area used for temporary storage',
					'access': 'R/W',
					'default': 0,
					'description': '''Pointer to a "scratch" area used for temporary storage during resolution. A space of minimum 3 bytes must be reserved.''',
				},
			#### 10000: WDT (watchdog timer) ####
			# 'WDT_TASK0': { 'address': 0x40010000, },
			'WDT_START': {
					'address': 0x40010000, 'module': 'WDT',
					'description': 'Start the watchdog',
				},

			# 'WDT_EVENT0': { 'address': 0x40010100, },
			'WDT_TIMEOUT': {
					'address': 0x40010100, 'module': 'WDT',
						'description': 'Watchdog timeout',
					},
			# 'WDT_SHORTS':  { 'address': 0x40010200, 'module': 'WDT', },
			'WDT_INTENSET':{
					'address': 0x40010304, 'module': 'WDT',
					'description': 'Interrupt enable set register',
				},
			'WDT_INTENCLR':{
					'address': 0x40010308, 'module': 'WDT',
					'description': 'Interrupt enable clear register',
				},
			# 'WDT_REG0':    { 'address': 0x40010400, },
			'WDT_RUNSTATUS':    {
					'address': 0x40010400, 'module': 'WDT',
					'description': 'Run status',
					'bitfields': {
							'RUNSTATUS': {
									'slice': (0,),
									'access': 'R',
									'description': '''Indicates if the watchdog is running.
0: Watchdog is not running.
1: Watchdog is running.''',
								},
						},
				},
			# 'WDT_REG1':    { 'address': 0x40010404, },
			'WDT_REQSTATUS':    {
					'address': 0x40010404, 'module': 'WDT',
					'description': 'Request status',
					'bitfields': {
							'RR0': {
									'slice': (0,),
									'access': 'R',
									'description': '''Request status for RR[0] register
0 RR[0] register is not enabled, or are already requesting reload
1 RR[0] register is enabled, and are not yet requesting reload''',
								},
							'RR1': {
									'slice': (1,),
									'access': 'R',
									'description': '''Request status for RR[1] register
0 RR[1] register is not enabled, or are already requesting reload
1 RR[1] register is enabled, and are not yet requesting reload''',
								},
							'RR2': {
									'slice': (2,),
									'access': 'R',
									'description': '''Request status for RR[2] register
0 RR[2] register is not enabled, or are already requesting reload
1 RR[2] register is enabled, and are not yet requesting reload''',
								}, 
							'RR3': {
									'slice': (3,),
									'access': 'R',
									'description': '''Request status for RR[3] register
0 RR[3] register is not enabled, or are already requesting reload
1 RR[3] register is enabled, and are not yet requesting reload''',
								}, 
							'RR4': {
									'slice': (4,),
									'access': 'R',
									'description': '''Request status for RR[4] register
0 RR[4] register is not enabled, or are already requesting reload
1 RR[4] register is enabled, and are not yet requesting reload''',
								},
							'RR5': {
									'slice': (5,),
									'access': 'R',
									'description': '''Request status for RR[5] register
0 RR[5] register is not enabled, or are already requesting reload
1 RR[5] register is enabled, and are not yet requesting reload''',
								},
							'RR6': {
									'slice': (6,),
									'access': 'R',
									'description': '''Request status for RR[6] register
0 RR[6] register is not enabled, or are already requesting reload
1 RR[6] register is enabled, and are not yet requesting reload''',
								},
							'RR7': {
									'slice': (7,),
									'access': 'R',
									'description': '''Request status for RR[7] register
0 RR[7] register is not enabled, or are already requesting reload
1 RR[7] register is enabled, and are not yet requesting reload''',
								},
						},
				},
			'WDT_CRV': {
					'address': 0x4001504, 'module': 'WDT',
						'description': 'Counter reload value',
				},
			'WDT_RREN':  {
					'address': 0x40010508, 'module': 'WDT',
					'description': 'Reload request enable',
					'bitfields':  {
							'RR0': {
									'slice': (0,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[0] register
0 Disable RR[0] register
1 Enable RR[0] register''',
								},
							'RR1': {
									'slice': (1,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[1] register
0 Disable RR[1] register
1 Enable RR[1] register''',
								},
							'RR2': {
									'slice': (2,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[2] register
0 Disable RR[2] register
1 Enable RR[2] register''',
								},
							'RR3': {
									'slice': (3,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[3] register
0 Disable RR[3] register
1 Enable RR[3] register''',
								},
							'RR4': {
									'slice': (4,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[4] register
0 Disable RR[4] register
1 Enable RR[4] register''',
								},
							'RR5': {
									'slice': (5,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[5] register
0 Disable RR[5] register
1 Enable RR[5] register''',
								},
							'RR6': {
									'slice': (6,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[6] register
0 Disable RR[6] register
1 Enable RR[6] register''',
								},
							'RR7': {
									'slice': (7,),
									'acceess': 'R/W',
									'description': '''Enable or disable RR[7] register
0 Disable RR[7] register
1 Enable RR[7] register''',
								},
						},
				},
			'WDT_CONFIG': {
					'address': 0x4001050C, 'module': 'WDT',
					'description': 'Configuration register',
					'bitfields': {
							'SLEEP': {
									'slice': (0,),
									'access': 'R/W',
									'description': '''Configure the watchdog to either be paused, or kept running, while the CPU is sleeping.
0: Pause the watchdog while the CPU is sleeping
1: Keep the watchdog running while the CPU is sleeping.'''
								},
							'HALT': {
									'slice': (3,),
									'access': 'R/W',
									'description': '''Configure the watchdog to either be paused, or kept running, while the CPU is halted by the debugger.
0: Pause watchdog while the CPU is halted by the debugger.
1: Keep the watchdog running while the CPU is halted by the debugger''',
								},
						},
				},
			'WDT_RR0': {
					'address': 0x40010600, 'module': 'WDT',
					'description': 'Reload request 0',
					'access': 'W',
				},
			'WDT_RR1': {
					'address': 0x40010604, 'module': 'WDT',
					'description': 'Reload request 1',
					'access': 'W',
				},
			'WDT_RR2': {
					'address': 0x40010608, 'module': 'WDT',
					'description': 'Reload request 2',
					'access': 'W',
				},
			'WDT_RR3': {
					'address': 0x4001060C, 'module': 'WDT',
					'description': 'Reload request 3',
					'access': 'W',
				},
			'WDT_RR4': {
					'address': 0x40010610, 'module': 'WDT',
					'description': 'Reload request 4',
					'access': 'W',
				},
			'WDT_RR5': {
					'address': 0x40010614, 'module': 'WDT',
					'description': 'Reload request 5',
					'access': 'W',
				},
			'WDT_RR6': {
					'address': 0x40010618, 'module': 'WDT',
					'description': 'Reload request 6',
					'access': 'W',
				},
			'WDT_RR7': {
					'address': 0x4001061C, 'module': 'WDT',
					'description': 'Reload request 7',
					'access': 'W',
				},

			#### 11000: RTC1 ####
			# 'RTC1_TASK0': { 'address': 0x40011000, },
			'RTC1_START': {
					'address': 0x40011000, 'module': 'RTC1',
					'description': 'Start RTC COUNTER',
				},
			# 'RTC1_TASK1': { 'address': 0x40011004, },
			'RTC1_STOP': {
					'address': 0x40011004, 'module': 'RTC1',
					'description': 'Stop RTC COUNTER',
				},
			# 'RTC1_TASK2': { 'address': 0x40011008, },
			'RTC1_CLEAR': {
					'address': 0x40011008, 'module': 'RTC1',
					'description': 'Clear RTC COUNTER',
				},
			# 'RTC1_TASK3': { 'address': 0x4001100C, },
			'RTC1_TRIGOVRFLW': {
					'address': 0x4001100C, 'module': 'RTC1',
					'description': 'Set COUNTER to 0xFFFF0.',
				},
			# 'RTC1_EVENT0': { 'address': 0x40011100, },
			'RTC1_TICK': {
					'address': 0x40011100, 'module': 'RTC1',
					'description': 'Event on COUNTER increment',
				},
			'RTC1_OVRFLW': {
					'address': 0x40011104, 'module': 'RTC1',
					'description': 'Event on COUNTER overflow',
				},
			# 'RTC1_EVENT16': { 'address': 0x40011140, },
			'RTC1_COMPARE0': {
					'address': 0x40011140, 'module': 'RTC1',
					'description': 'Compare event on CC[0] match.',
				},
			# 'RTC1_EVENT17': { 'address': 0x40011144, },
			'RTC1_COMPARE1': {
					'address': 0x40011144, 'module': 'RTC1',
					'description': 'Compare event on CC[1] match.',
				},
			# 'RTC1_EVENT18': { 'address': 0x40011148, },
			'RTC1_COMPARE2': {
					'address': 0x40011148, 'module': 'RTC1',
					'description': 'Compare event on CC[2] match.',
				},
			# 'RTC1_EVENT19': { 'address': 0x4001114C, },
			'RTC1_COMPARE3': {
					'address': 0x4001114C, 'module': 'RTC1',
					'description': 'Compare event on CC[3] match.',
				},
			# 'RTC1_SHORTS':  { 'address': 0x40011200, 'module': 'RTC1', },
			'RTC1_INTENSET':{
					'address': 0x40011304, 'module': 'RTC1',
					'description': 'Configures which events shall generate an RTC interrupt',
				},
			'RTC1_INTENCLR':{
					'address': 0x40011308, 'module': 'RTC1',
					'description': 'Configures which events shall not generate an RTC interrupt',
				},
			'RTC1_EVTEN': {
					'address': 0x40011340, 'module': 'RTC1',
					'description': 'Enable or disable event routing to PPI',
					'bitfields': {
							'TICK': {
									'slice': (0,),
									'access': 'R/W',
									'description': '''Enable or disable routing of TICK event to PPI.
1: Enable
0: Disable''',
								},
							'OVERFLW': {
									'slice': (1,),
									'access': 'R/W',
									'description': '''Enable or disable routing of OVRFLW event to PPI.''',
								},
							'COMPARE0': {
									'slice': (16,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[0]event to PPI.''',
								},
							'COMPARE1': {
									'slice': (17,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[1]event to PPI.''',
								},
							'COMPARE2': {
									'slice': (18,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[2]event to PPI.''',
								},
							'COMPARE3': {
									'slice': (19,),
									'access': 'R/W',
									'description': '''Enable or disable routing of COMPARE[3]event to PPI.''',
								}
						},
				},
			'RTC1_EVTENSET': {
					'address': 0x40011344, 'module': 'RTC1',
					'description': 'Enable event routing to PPI',
					'bitfields': {
							'TICK': {
								'slice': (0,),
								'description': '''Enable routing of TICK event to PPI.
W1: Enable
R0: Disabled (readback bit0 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'OVRFLW': {
									'slice': (1,),
									'description': '''Enable routing of OVRFLW event to PPI.
W1: Enable
R0: Disabled (readback bit1 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'COMPARE0': {
									'slice': (16,),
									'description': '''Enable routing of COMPARE[0] event to PPI.
W1: Enable
R0: Disabled (readback bit 16 of EVTEN)
R1: Enabled (readback bit 16 of EVTEN)''',
								},
							'COMPARE1': {
									'slice': (17,),
									'description': '''Enable routing of COMPARE[1] event to PPI.
W1: Enable
R0: Disabled (readback bit 17 of EVTEN)
R1: Enabled (readback bit 17 of EVTEN)''',
								},
							'COMPARE2': {
									'slice': (18,),
									'description': '''Enable routing of COMPARE[2] event to PPI.
W1: Enable
R0: Disabled (readback bit 18 of EVTEN)
R1: Enabled (readback bit 18 of EVTEN)''',
								},
							'COMPARE3': {
									'slice': (19,),
									'description': '''Enable routing of COMPARE[3] event to PPI.
W1: Enable
R0: Disabled (readback bit 19 of EVTEN)
R1: Enabled (readback bit 19 of EVTEN)''',
								},
						},
				},
			'RTC1_EVTENCLR': {
					'address': 0x40011348, 'module': 'RTC1',
					'description': 'Disable event routing to PPI',
					'bitfields': {
							'TICK': {
								'slice': (0,),
								'description': '''Disable routing of TICK event to PPI.
W1: Disable
R0: Disabled (readback bit0 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'OVRFLW': {
									'slice': (1,),
									'description': '''Disable routing of OVRFLW event to PPI.
W1: Disable
R0: Disabled (readback bit1 of EVTEN)
R1: Enabled (readback bit0 of EVTEN)''',
								},
							'COMPARE0': {
									'slice': (16,),
									'description': '''Disable routing of COMPARE[0] event to PPI.
W1: Disable
R0: Disabled (readback bit 16 of EVTEN)
R1: Enabled (readback bit 16 of EVTEN)''',
								},
							'COMPARE1': {
									'slice': (17,),
									'description': '''Disable routing of COMPARE[1] event to PPI.
W1: Disable
R0: Disabled (readback bit 17 of EVTEN)
R1: Enabled (readback bit 17 of EVTEN)''',
								},
							'COMPARE2': {
									'slice': (18,),
									'description': '''Enable routing of COMPARE[2] event to PPI.
W1: Disable
R0: Disabled (readback bit 18 of EVTEN)
R1: Enabled (readback bit 18 of EVTEN)''',
								},
							'COMPARE3': {
									'slice': (19,),
									'description': '''Disable routing of COMPARE[3] event to PPI.
W1: Disable
R0: Disabled (readback bit 19 of EVTEN)
R1: Enabled (readback bit 19 of EVTEN)''',
								},
				},
			#### 12000: QDEC ####
			'QDEC_TASK0': { 'address': 0x40012000, },
			'QDEC_START': {
					'address': 0x40012000,
					'description': '''Task starting the quadrature decoder. When started, the SAMPLE register will be continuously updated at the rate given in the SAMPLEPER register.''',
				},
			'QDEC_TASK1': { 'address': 0x40012004, },
			'QDEC_STOP': {
					'address': 0x40012004,
					'description': '''Task stopping the quadrature decoder.''',
				},
			'QDEC_TASK2': {
					'address': 0x40012008,
					'description': '''Task transferring the content of ACC to ACCREAD and the content of ACCDBL to ACCDBLREAD, and then clearing the ACC and ACCDBL registers. These read-and-clear operations will be done automatically.''',
				},
			'QDEC_TASK3': { 'address': 0x4001200C, },
			'QDEC_TASK4': { 'address': 0x40012010, },
			'QDEC_TASK5': { 'address': 0x40012014, },
			'QDEC_TASK6': { 'address': 0x40012018, },
			'QDEC_TASK7': { 'address': 0x4001201C, },
			'QDEC_TASK8': { 'address': 0x40012020, },
			'QDEC_TASK9': { 'address': 0x40012024, },
			'QDEC_TASK10': { 'address': 0x40012028, },
			'QDEC_TASK11': { 'address': 0x4001202C, },
			'QDEC_TASK12': { 'address': 0x40012030, },
			'QDEC_TASK13': { 'address': 0x40012034, },
			'QDEC_TASK14': { 'address': 0x40012038, },
			'QDEC_TASK15': { 'address': 0x4001203C, },
			'QDEC_TASK16': { 'address': 0x40012040, },
			'QDEC_TASK17': { 'address': 0x40012044, },
			'QDEC_TASK18': { 'address': 0x40012048, },
			'QDEC_TASK19': { 'address': 0x4001204C, },
			'QDEC_TASK20': { 'address': 0x40012050, },
			'QDEC_TASK21': { 'address': 0x40012054, },
			'QDEC_TASK22': { 'address': 0x40012058, },
			'QDEC_TASK23': { 'address': 0x4001205C, },
			'QDEC_TASK24': { 'address': 0x40012060, },
			'QDEC_TASK25': { 'address': 0x40012064, },
			'QDEC_TASK26': { 'address': 0x40012068, },
			'QDEC_TASK27': { 'address': 0x4001206C, },
			'QDEC_TASK28': { 'address': 0x40012070, },
			'QDEC_TASK29': { 'address': 0x40012074, },
			'QDEC_TASK30': { 'address': 0x40012078, },
			'QDEC_TASK31': { 'address': 0x4001207C, },
			'QDEC_EVENT0': { 'address': 0x40012100, },
			'QDEC_SAMPLERDY': {
					'address': 0x40012100,
					'description': '''Event being generated for every new sample value written to the SAMPLE register.''',
				},
			'QDEC_EVENT1': { 'address': 0x40012104, },
			'QDEC_REPORTRDY': {
					'address': 0x40012104,
					'description': '''Event being generated when REPORTPER number of samples has been accumulated in the ACC register and the content of the ACC register does not equal 0. (Thus, this event is only generated if a motion is detected since the previous clearing of the ACC register).''',
				},
			'QDEC_EVENT2': { 'address': 0x40012108, },
			'QDEC_ACCOF': {
					'address': 0x40012108,
					'description': '''ACC or ACCDBL register overflow.''',
				},
			'QDEC_EVENT3': { 'address': 0x4001210C, },
			'QDEC_EVENT4': { 'address': 0x40012110, },
			'QDEC_EVENT5': { 'address': 0x40012114, },
			'QDEC_EVENT6': { 'address': 0x40012118, },
			'QDEC_EVENT7': { 'address': 0x4001211C, },
			'QDEC_EVENT8': { 'address': 0x40012120, },
			'QDEC_EVENT9': { 'address': 0x40012124, },
			'QDEC_EVENT10': { 'address': 0x40012128, },
			'QDEC_EVENT11': { 'address': 0x4001212C, },
			'QDEC_EVENT12': { 'address': 0x40012130, },
			'QDEC_EVENT13': { 'address': 0x40012134, },
			'QDEC_EVENT14': { 'address': 0x40012138, },
			'QDEC_EVENT15': { 'address': 0x4001213C, },
			'QDEC_EVENT16': { 'address': 0x40012140, },
			'QDEC_EVENT17': { 'address': 0x40012144, },
			'QDEC_EVENT18': { 'address': 0x40012148, },
			'QDEC_EVENT19': { 'address': 0x4001214C, },
			'QDEC_EVENT20': { 'address': 0x40012150, },
			'QDEC_EVENT21': { 'address': 0x40012154, },
			'QDEC_EVENT22': { 'address': 0x40012158, },
			'QDEC_EVENT23': { 'address': 0x4001215C, },
			'QDEC_EVENT24': { 'address': 0x40012160, },
			'QDEC_EVENT25': { 'address': 0x40012164, },
			'QDEC_EVENT26': { 'address': 0x40012168, },
			'QDEC_EVENT27': { 'address': 0x4001216C, },
			'QDEC_EVENT28': { 'address': 0x40012170, },
			'QDEC_EVENT29': { 'address': 0x40012174, },
			'QDEC_EVENT30': { 'address': 0x40012178, },
			'QDEC_EVENT31': { 'address': 0x4001217C, },
			'QDEC_SHORTS':  {
					'address': 0x40012200,
					'description': '''Shortcut register.''',
					'bitfields': {
							'REPORTRDY_READCLRACC': {
									'slice': (0,),
									'description': '''Short REPORTRDY event to READCLRACC task.
0: Disable
1: Enable''',
									'access': 'R/W',
									'default': 0,
								},
							'SAMPLERDY_STOP': {
									'slice': (1,),
									'description': '''Short SAMPLERDY event to STOP task.
0: Disable
1: Enable''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'QDEC_INTENSET':{
					'address': 0x40012304,
					'description': '''Interrupt enable set register''',
				},
			'QDEC_INTENCLR':{
					'address': 0x40012308,
					'description': '''Interrupt enable clear register''',
				},
			'QDEC_REG0':    { 'address': 0x40012400, },
			'QDEC_REG1':    { 'address': 0x40012404, },
			'QDEC_REG2':    { 'address': 0x40012408, },
			'QDEC_REG3':    { 'address': 0x4001240C, },
			'QDEC_REG4':    { 'address': 0x40012410, },
			'QDEC_REG5':    { 'address': 0x40012414, },
			'QDEC_REG6':    { 'address': 0x40012418, },
			'QDEC_REG7':    { 'address': 0x4001241C, },
			'QDEC_REG8':    { 'address': 0x40012420, },
			'QDEC_REG9':    { 'address': 0x40012424, },
			'QDEC_REG10':   { 'address': 0x40012428, },
			'QDEC_REG11':   { 'address': 0x4001242C, },
			'QDEC_REG12':   { 'address': 0x40012430, },
			'QDEC_REG13':   { 'address': 0x40012434, },
			'QDEC_REG14':   { 'address': 0x40012438, },
			'QDEC_REG15':   { 'address': 0x4001243C, },
			'QDEC_REG16':   { 'address': 0x40012440, },
			'QDEC_REG17':   { 'address': 0x40012444, },
			'QDEC_REG18':   { 'address': 0x40012448, },
			'QDEC_REG19':   { 'address': 0x4001244C, },
			'QDEC_REG20':   { 'address': 0x40012450, },
			'QDEC_REG21':   { 'address': 0x40012454, },
			'QDEC_REG22':   { 'address': 0x40012458, },
			'QDEC_REG23':   { 'address': 0x4001245C, },
			'QDEC_REG24':   { 'address': 0x40012460, },
			'QDEC_REG25':   { 'address': 0x40012464, },
			'QDEC_REG26':   { 'address': 0x40012468, },
			'QDEC_REG27':   { 'address': 0x4001246C, },
			'QDEC_REG28':   { 'address': 0x40012470, },
			'QDEC_REG29':   { 'address': 0x40012474, },
			'QDEC_REG30':   { 'address': 0x40012478, },
			'QDEC_REG31':   { 'address': 0x4001247C, },
			'QDEC_ENABLE': {  ## Should this be ADC_ENABLE?? 
					'address': 0x40012500,
					'description': 'ADC enable',
					'bitfields': {
							'ENABLE': {
									'slice': (0,),
									'description': '''Enable the quadrature decoder. When enabled, the decoder pins will be active. When disabled, the quadrature decoder pins are not active and can be used as GPIO.
0: DISABLE
1: ENABLE''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'QDEC_LEDPOL': {
					'address': 0x40012504,
					'description': 'ADC configuration',
					'bitfields': {
							'LEDPOL': {
									'slice': (0,),
									'description': '''LED output polarity.
0 (ACTIVELOW): LED active on output pin low.
1 (ACTIVEHIGH): LED active on output pin high.''',
									'access': 'R/W',
									'default': 0,
								},
						},
				},
			'QDEC_SAMPLEPER': {
					'address': 0x40012508,
					'description': 'ADC conversion result',
					'bitfields': {
							'VAL': {
									'slice': (2,0),
									'description': '''Sample period. The SAMPLE register will be updated
									for every new sample.
0 (128_US):     128 us
1 (256_US):     256 us
2 (512_US):     512 us
3 (1024_US):   1024 us
4 (2048_US):   2048 us
5 (4096_US):   4096 us
6 (8192_US):   8192 us
7 (16384_US): 16384 us''',
								},
						},
				},
			'QDEC_SAMPLE': {
					'address': 0x4001250C,
					'access': 'R',
					'default': 0,
					'description': '''Motion sample value.
(--1..2) Last motion sample.
The value is a 2's complement value, and the sign gives the direction of the motion.
The value '2' indicates a double transition.''',
				},
			'QDEC_REPORTPER': {
					'address': 0x40012510,
					'description': 'Number of samples to be taken before a REPORTRDY event is generated',
					'bitfields': {
							'VAL': {
									'slice': (2,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Specifies the number of samples to be accumulated in the ACC register before the REPORTRDY event can be generated.  The report period in us is given as:
RPUS = SP * RP, Where
RPUS is the report period in [us/report]
SP is the sample period in [us/sample] specified in SAMPLEPER
RP is the report period in [samples/report] specified in REPORTPER
0: (10_SMPL):   10 samples/report
1: (40_SMPL):   40 samples/report
2: (80_SMPL):   80 samples/report
3: (120_SMPL): 120 samples/report
4: (160_SMPL): 160 samples/report
5: (200_SMPL): 200 samples/report
6: (240_SMPL): 240 samples/report
7: (280_SMPL): 280 samples/report''',
								},
						},
				},
			'QDEC_ACC': {
					'address': 0x40012514,
					'description': '''Register accumulating the valid transitions.
Register accumulating all valid samples (not double transition) read from the RENC (in the SAMPLE register). Double transitions (SAMPLE = 2) will not be accumulated in this register.
The value is a 32-bit 2's complement value, -1024..1023.
If a sample that would cause this register to overflow or underflow is received, the sample will be ignored and an overflow event (ACCOF) will be generated.
The ACC register is cleared by triggering the READCLRACC task.''',
					'access': 'R',
					'default': 0,
				},
			'QDEC_ACCREAD': {
					'address': 0x40012518,
					'description': '''Snapshot of the ACC register updated by the READCLRACC task.
Snapshot of the ACC register. Value -1024..1023.
The ACCREAD register is updated when the READCLRACC task is triggered.''',
					'access': 'R',
					'default': 0,
				},
			'QDEC_PSELLED': {
					'address': 0x4001251C,
					'description': '''GPIO pin number to be used as LED output.
0..31: GPIO pin number to be used as LED output.
0xFFFFFFFF: disable this output.''',
					'access': 'R/W',
					'default': 0xFFFFFFFF,
				},
			'QDEC_PSELA': {
					'address': 0x40012520,
					'description': '''GPIO pin number to be used as Phase A input.
0..31: GPIO pin number to be used as Phase A input.
0xFFFFFFFF: disable this input.''',
					'access': 'R/W',
					'default': 0xFFFFFFFF,
				},
			'QDEC_PSELB': {
					'address': 0x40012524,
					'description': '''GPIO pin number to be used as Phase B input.
0..31: GPIO pin number to be used as Phase B input.
0xFFFFFFFF: disable this input.''',
					'access': 'R/W',
					'default': 0xFFFFFFFF,
				},
			'QDEC_DBFEN': {
					'address': 0x40012528,
					'description': 'Enable input debounce filters',
					'bitfields': {
							'DBFEN': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable input debounce filters.
0: Disable
1: Enable''',
								},
						},
				},
			'QDEC_LEDPRE': {
					'address': 0x40012540,
					'description': 'Time period the LED is switched ON prior to sampling.',
					'bitfields': {
						'LEDPRE': {
								'slice': (8,0),
								'access': 'R/W',
								'default': 0,
								'description': '''0..511: Period in us the LED is switched on prior to sampling.''',
							},
						},
				},
			'QDEC_ACCDBL': {
					'address': 0x40012544,
					'description': 'Register accumulating the number of detected double transitions.',
					'bitfields': {
							'ACCDBL': {
									'slice': (3,0),
									'access': 'R',
									'default': 0,
									'description': '''0..15: Register accumulating the number of detected double or illegal transitions. (SAMPLE = 2).
When this register has reached its maximum value the accumulation of double / illegal transitions will stop.
An overflow event (ACCOF) will be generated if any double or illegal transitions are detected after the maximum or minimum value was reached.
This field is cleared by triggering the READCLRACC task.''',
								},
						},
				},
			'QDEC_ACCDBLREAD': {
					'address': 0x40012548,
					'description': 'Snapshot of the ACCDBL.',
					'bitfields': {
							'ACCDBLREAD': {
									'slice': (3,0),
									'access': 'R',
									'default': 0,
									'description': '''0..15: Snapshot of the ACCDBL register.
This field is updated when the READCLRACC task is triggered.''',
								},
						},
				},

			#### 13000: LPCOMP (low-power comparator) ####
			'LPCOMP_TASK0': { 'address': 0x40013000, },
			'LPCOMP_START': {
					'address': 0x40013000,
					'description': 'Start comparator',
				},
			'LPCOMP_TASK1': { 'address': 0x40013004, },
			'LPCOMP_STOP': {
					'address': 0x40013004,
					'description': 'Stop comparator',
				},
			'LPCOMP_TASK2': { 'address': 0x40013008, },
			'LPCOMP_SAMPLE': {
					'address': 0x40013008,
					'description': 'Sample comparator value',
				},
			'LPCOMP_TASK3': { 'address': 0x4001300C, },
			'LPCOMP_TASK4': { 'address': 0x40013010, },
			'LPCOMP_TASK5': { 'address': 0x40013014, },
			'LPCOMP_TASK6': { 'address': 0x40013018, },
			'LPCOMP_TASK7': { 'address': 0x4001301C, },
			'LPCOMP_TASK8': { 'address': 0x40013020, },
			'LPCOMP_TASK9': { 'address': 0x40013024, },
			'LPCOMP_TASK10': { 'address': 0x40013028, },
			'LPCOMP_TASK11': { 'address': 0x4001302C, },
			'LPCOMP_TASK12': { 'address': 0x40013030, },
			'LPCOMP_TASK13': { 'address': 0x40013034, },
			'LPCOMP_TASK14': { 'address': 0x40013038, },
			'LPCOMP_TASK15': { 'address': 0x4001303C, },
			'LPCOMP_TASK16': { 'address': 0x40013040, },
			'LPCOMP_TASK17': { 'address': 0x40013044, },
			'LPCOMP_TASK18': { 'address': 0x40013048, },
			'LPCOMP_TASK19': { 'address': 0x4001304C, },
			'LPCOMP_TASK20': { 'address': 0x40013050, },
			'LPCOMP_TASK21': { 'address': 0x40013054, },
			'LPCOMP_TASK22': { 'address': 0x40013058, },
			'LPCOMP_TASK23': { 'address': 0x4001305C, },
			'LPCOMP_TASK24': { 'address': 0x40013060, },
			'LPCOMP_TASK25': { 'address': 0x40013064, },
			'LPCOMP_TASK26': { 'address': 0x40013068, },
			'LPCOMP_TASK27': { 'address': 0x4001306C, },
			'LPCOMP_TASK28': { 'address': 0x40013070, },
			'LPCOMP_TASK29': { 'address': 0x40013074, },
			'LPCOMP_TASK30': { 'address': 0x40013078, },
			'LPCOMP_TASK31': { 'address': 0x4001307C, },
			'LPCOMP_EVENT0': { 'address': 0x40013100, },
			'LPCOMP_READY': {
					'address': 0x40013100,
					'description': 'LPCOMP is ready and output is valid.',
				},
			'LPCOMP_EVENT1': { 'address': 0x40013104, },
			'LPCOMP_DOWN': {
					'address': 0x40013104,
					'description': 'Downward crossing',
				},
			'LPCOMP_EVENT2': { 'address': 0x40013108, },
			'LPCOMP_UP': {
					'address': 0x40013108,
					'description': 'Upward crossing',
				},
			'LPCOMP_EVENT3': { 'address': 0x4001310C, },
			'LPCOMP_CROSS': {
					'address': 0x4001310C,
					'description': 'Downward or upward crossing',
				},
			'LPCOMP_EVENT4': { 'address': 0x40013110, },
			'LPCOMP_EVENT5': { 'address': 0x40013114, },
			'LPCOMP_EVENT6': { 'address': 0x40013118, },
			'LPCOMP_EVENT7': { 'address': 0x4001311C, },
			'LPCOMP_EVENT8': { 'address': 0x40013120, },
			'LPCOMP_EVENT9': { 'address': 0x40013124, },
			'LPCOMP_EVENT10': { 'address': 0x40013128, },
			'LPCOMP_EVENT11': { 'address': 0x4001312C, },
			'LPCOMP_EVENT12': { 'address': 0x40013130, },
			'LPCOMP_EVENT13': { 'address': 0x40013134, },
			'LPCOMP_EVENT14': { 'address': 0x40013138, },
			'LPCOMP_EVENT15': { 'address': 0x4001313C, },
			'LPCOMP_EVENT16': { 'address': 0x40013140, },
			'LPCOMP_EVENT17': { 'address': 0x40013144, },
			'LPCOMP_EVENT18': { 'address': 0x40013148, },
			'LPCOMP_EVENT19': { 'address': 0x4001314C, },
			'LPCOMP_EVENT20': { 'address': 0x40013150, },
			'LPCOMP_EVENT21': { 'address': 0x40013154, },
			'LPCOMP_EVENT22': { 'address': 0x40013158, },
			'LPCOMP_EVENT23': { 'address': 0x4001315C, },
			'LPCOMP_EVENT24': { 'address': 0x40013160, },
			'LPCOMP_EVENT25': { 'address': 0x40013164, },
			'LPCOMP_EVENT26': { 'address': 0x40013168, },
			'LPCOMP_EVENT27': { 'address': 0x4001316C, },
			'LPCOMP_EVENT28': { 'address': 0x40013170, },
			'LPCOMP_EVENT29': { 'address': 0x40013174, },
			'LPCOMP_EVENT30': { 'address': 0x40013178, },
			'LPCOMP_EVENT31': { 'address': 0x4001317C, },
			'LPCOMP_SHORTS':  {
					'address': 0x40013200,
					'description': 'Shortcuts for LPCOMP',
					'bitfields': {
							'READY_SAMPLE': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between READY event and SAMPLE task.
0: Disable shortcut.
1: Enable shortcut.''',
								},
							'READY_STOP': {
								'slice': (1,),
								'access': 'R/W',
								'default': 0,
								'description': '''Enable or disable shortcut between READY event and STOP task.
0: Disable shortcut.
1: Enable shortcut.''',
								},
							'DOWN_STOP': {
									'slice': (2,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between DOWN event and STOP task.
0: Disable shortcut.
1: Enable shortcut.''',
								},
							'UP_STOP': {
									'slice': (3,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between UP event and STOP task.
0: Disable shortcut.
1: Enable shortcut.''',
								},
							'CROSS_STOP': {
									'slice': (4,),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable shortcut between CROSS event and STOP task.
0: Disable shortcut.
1: Enable shortcut.''',
								},
						},
				},
			'LPCOMP_INTENSET':{
					'address': 0x40013304,
					'description': 'Interrupt enable set register',
				},
			'LPCOMP_INTENCLR':{
					'address': 0x40013308,
					'description': 'Interrupt enable clear register',
				},
			'LPCOMP_REG0':    { 'address': 0x40013400, },
			'LPCOMP_RESULT':    {
					'address': 0x40013400,
					'description': 'Compare result',
					'bitfields': {
							'RESULT': {
									'slice': (0,),
									'access': 'R',
									'default': 0,
									'description': '''Result of last compare. Decision point SAMPLE task.
0 (BELOW): Input voltage is below the reference threshold. (VIN+ < VIN-)
1 (ABOVE): Input voltage is above the reference threshold. (VIN+ > VIN-)''',
								},
						},
				},
			'LPCOMP_REG1':    { 'address': 0x40013404, },
			'LPCOMP_REG2':    { 'address': 0x40013408, },
			'LPCOMP_REG3':    { 'address': 0x4001340C, },
			'LPCOMP_REG4':    { 'address': 0x40013410, },
			'LPCOMP_REG5':    { 'address': 0x40013414, },
			'LPCOMP_REG6':    { 'address': 0x40013418, },
			'LPCOMP_REG7':    { 'address': 0x4001341C, },
			'LPCOMP_REG8':    { 'address': 0x40013420, },
			'LPCOMP_REG9':    { 'address': 0x40013424, },
			'LPCOMP_REG10':   { 'address': 0x40013428, },
			'LPCOMP_REG11':   { 'address': 0x4001342C, },
			'LPCOMP_REG12':   { 'address': 0x40013430, },
			'LPCOMP_REG13':   { 'address': 0x40013434, },
			'LPCOMP_REG14':   { 'address': 0x40013438, },
			'LPCOMP_REG15':   { 'address': 0x4001343C, },
			'LPCOMP_REG16':   { 'address': 0x40013440, },
			'LPCOMP_REG17':   { 'address': 0x40013444, },
			'LPCOMP_REG18':   { 'address': 0x40013448, },
			'LPCOMP_REG19':   { 'address': 0x4001344C, },
			'LPCOMP_REG20':   { 'address': 0x40013450, },
			'LPCOMP_REG21':   { 'address': 0x40013454, },
			'LPCOMP_REG22':   { 'address': 0x40013458, },
			'LPCOMP_REG23':   { 'address': 0x4001345C, },
			'LPCOMP_REG24':   { 'address': 0x40013460, },
			'LPCOMP_REG25':   { 'address': 0x40013464, },
			'LPCOMP_REG26':   { 'address': 0x40013468, },
			'LPCOMP_REG27':   { 'address': 0x4001346C, },
			'LPCOMP_REG28':   { 'address': 0x40013470, },
			'LPCOMP_REG29':   { 'address': 0x40013474, },
			'LPCOMP_REG30':   { 'address': 0x40013478, },
			'LPCOMP_REG31':   { 'address': 0x4001347C, },
			'LPCOMP_ENABLE': {
					'address': 0x40013500,
					'description': 'Enable LPCOMP',
					'bitfields': {
							'ENABLE': {
									'slice': (1,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Enable or disable LPCOMP.
0: Disable LPCOMP.
1: Enable LPCOMP.''',
								},
						},
				},
			'LPCOMP_PSEL': {
					'address': 0x40013504,
					'description': 'Input pin select',
					'bitfields': {
							'PSEL': {
									'slice': (2,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Analog pin select.
0 (AIN0): AIN0 selected as analog input.
1 (AIN1): AIN1 selected as analog input.
2 (AIN2): AIN2 selected as analog input.
3 (AIN3): AIN3 selected as analog input.
4 (AIN4): AIN4 selected as analog input.
5 (AIN5): AIN5 selected as analog input.
6 (AIN6): AIN6 selected as analog input.
7 (AIN7): AIN7 selected as analog input.''',
								},
						},
				},
			'LPCOMP_REFSEL': {
					'address': 0x40013508,
					'description': 'Reference select',
					'bitfields': {
							'REFSEL': {
									'slice': (2,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Reference select.
0 (VDD_1_8): VDD * 1/8 selected as reference.
1 (VDD_2_8): VDD * 2/8 selected as reference.
2 (VDD_3_8): VDD * 3/8 selected as reference.
3 (VDD_4_8): VDD * 4/8 selected as reference.
4 (VDD_5_8): VDD * 5/8 selected as reference.
5 (VDD_6_8): VDD * 6/8 selected as reference.
6 (VDD_7_8): VDD * 7/8 selected as reference.
7 (AREF):    External analog reference selected.''',
								},
						},
				},
			'LPCOMP_EXTREFSEL': {
					'address': 0x4001350C,
					'description': 'External reference select',
					'bitfields': {
							'EXTREFSEL': {
									'slice': (0,),
									'access': 'R/W',
									'default': 0,
									'description': '''External analog reference select.
0 (AREF0): Use AREF0 as external analog reference.
1 (AREF1): Use AREF1 as external analog reference.''',
								},
						},
				},
			'LPCOMP_ANADETECT': {
					'address': 0x40013520,
					'description': 'Analog detect configuration',
					'bitfields': {
							'ANADETECT': {
									'slice': (1,0),
									'access': 'R/W',
									'default': 0,
									'description': '''Analog detect configuration.
0 (CROSS): Generate ANADETECT on crossing, both upward crossing and downward crossing.
1 (UP):    Generate ANADETECT on upward crossing only.
2 (DOWN):  Generate ANADETECT on downward crossing only.''',
								},
						},
				},

			#### 1E000: NVMC (nonvolatile memory controller) ####
			'NVMC_TASK0': {
					'address': 0x4001E000,
				},
			'NVMC_TASK0': { 'address': 0x4001E000, },
			'NVMC_TASK1': { 'address': 0x4001E004, },
			'NVMC_TASK2': { 'address': 0x4001E008, },
			'NVMC_TASK3': { 'address': 0x4001E00C, },
			'NVMC_TASK4': { 'address': 0x4001E010, },
			'NVMC_TASK5': { 'address': 0x4001E014, },
			'NVMC_TASK6': { 'address': 0x4001E018, },
			'NVMC_TASK7': { 'address': 0x4001E01C, },
			'NVMC_TASK8': { 'address': 0x4001E020, },
			'NVMC_TASK9': { 'address': 0x4001E024, },
			'NVMC_TASK10': { 'address': 0x4001E028, },
			'NVMC_TASK11': { 'address': 0x4001E02C, },
			'NVMC_TASK12': { 'address': 0x4001E030, },
			'NVMC_TASK13': { 'address': 0x4001E034, },
			'NVMC_TASK14': { 'address': 0x4001E038, },
			'NVMC_TASK15': { 'address': 0x4001E03C, },
			'NVMC_TASK16': { 'address': 0x4001E040, },
			'NVMC_TASK17': { 'address': 0x4001E044, },
			'NVMC_TASK18': { 'address': 0x4001E048, },
			'NVMC_TASK19': { 'address': 0x4001E04C, },
			'NVMC_TASK20': { 'address': 0x4001E050, },
			'NVMC_TASK21': { 'address': 0x4001E054, },
			'NVMC_TASK22': { 'address': 0x4001E058, },
			'NVMC_TASK23': { 'address': 0x4001E05C, },
			'NVMC_TASK24': { 'address': 0x4001E060, },
			'NVMC_TASK25': { 'address': 0x4001E064, },
			'NVMC_TASK26': { 'address': 0x4001E068, },
			'NVMC_TASK27': { 'address': 0x4001E06C, },
			'NVMC_TASK28': { 'address': 0x4001E070, },
			'NVMC_TASK29': { 'address': 0x4001E074, },
			'NVMC_TASK30': { 'address': 0x4001E078, },
			'NVMC_TASK31': { 'address': 0x4001E07C, },
			'NVMC_EVENT0': { 'address': 0x4001E100, },
			'NVMC_EVENT1': { 'address': 0x4001E104, },
			'NVMC_EVENT2': { 'address': 0x4001E108, },
			'NVMC_EVENT3': { 'address': 0x4001E10C, },
			'NVMC_EVENT4': { 'address': 0x4001E110, },
			'NVMC_EVENT5': { 'address': 0x4001E114, },
			'NVMC_EVENT6': { 'address': 0x4001E118, },
			'NVMC_EVENT7': { 'address': 0x4001E11C, },
			'NVMC_EVENT8': { 'address': 0x4001E120, },
			'NVMC_EVENT9': { 'address': 0x4001E124, },
			'NVMC_EVENT10': { 'address': 0x4001E128, },
			'NVMC_EVENT11': { 'address': 0x4001E12C, },
			'NVMC_EVENT12': { 'address': 0x4001E130, },
			'NVMC_EVENT13': { 'address': 0x4001E134, },
			'NVMC_EVENT14': { 'address': 0x4001E138, },
			'NVMC_EVENT15': { 'address': 0x4001E13C, },
			'NVMC_EVENT16': { 'address': 0x4001E140, },
			'NVMC_EVENT17': { 'address': 0x4001E144, },
			'NVMC_EVENT18': { 'address': 0x4001E148, },
			'NVMC_EVENT19': { 'address': 0x4001E14C, },
			'NVMC_EVENT20': { 'address': 0x4001E150, },
			'NVMC_EVENT21': { 'address': 0x4001E154, },
			'NVMC_EVENT22': { 'address': 0x4001E158, },
			'NVMC_EVENT23': { 'address': 0x4001E15C, },
			'NVMC_EVENT24': { 'address': 0x4001E160, },
			'NVMC_EVENT25': { 'address': 0x4001E164, },
			'NVMC_EVENT26': { 'address': 0x4001E168, },
			'NVMC_EVENT27': { 'address': 0x4001E16C, },
			'NVMC_EVENT28': { 'address': 0x4001E170, },
			'NVMC_EVENT29': { 'address': 0x4001E174, },
			'NVMC_EVENT30': { 'address': 0x4001E178, },
			'NVMC_EVENT31': { 'address': 0x4001E17C, },
			'NVMC_SHORTS':  { 'address': 0x4001E200, },
			'NVMC_INTENSET':{ 'address': 0x4001E304, },
			'NVMC_INTENCLR':{ 'address': 0x4001E308, },
			'NVMC_REG0':    { 'address': 0x4001E400, },
			'NVMC_REG1':    { 'address': 0x4001E404, },
			'NVMC_REG2':    { 'address': 0x4001E408, },
			'NVMC_REG3':    { 'address': 0x4001E40C, },
			'NVMC_REG4':    { 'address': 0x4001E410, },
			'NVMC_REG5':    { 'address': 0x4001E414, },
			'NVMC_REG6':    { 'address': 0x4001E418, },
			'NVMC_REG7':    { 'address': 0x4001E41C, },
			'NVMC_REG8':    { 'address': 0x4001E420, },
			'NVMC_REG9':    { 'address': 0x4001E424, },
			'NVMC_REG10':   { 'address': 0x4001E428, },
			'NVMC_REG11':   { 'address': 0x4001E42C, },
			'NVMC_REG12':   { 'address': 0x4001E430, },
			'NVMC_REG13':   { 'address': 0x4001E434, },
			'NVMC_REG14':   { 'address': 0x4001E438, },
			'NVMC_REG15':   { 'address': 0x4001E43C, },
			'NVMC_REG16':   { 'address': 0x4001E440, },
			'NVMC_REG17':   { 'address': 0x4001E444, },
			'NVMC_REG18':   { 'address': 0x4001E448, },
			'NVMC_REG19':   { 'address': 0x4001E44C, },
			'NVMC_REG20':   { 'address': 0x4001E450, },
			'NVMC_REG21':   { 'address': 0x4001E454, },
			'NVMC_REG22':   { 'address': 0x4001E458, },
			'NVMC_REG23':   { 'address': 0x4001E45C, },
			'NVMC_REG24':   { 'address': 0x4001E460, },
			'NVMC_REG25':   { 'address': 0x4001E464, },
			'NVMC_REG26':   { 'address': 0x4001E468, },
			'NVMC_REG27':   { 'address': 0x4001E46C, },
			'NVMC_REG28':   { 'address': 0x4001E470, },
			'NVMC_REG29':   { 'address': 0x4001E474, },
			'NVMC_REG30':   { 'address': 0x4001E478, },
			'NVMC_REG31':   { 'address': 0x4001E47C, },

			#### 1F000: PPI (programmable peripheral interconnect) ####
			'PPI_TASK0': { 'address': 0x4001F000, },
			'PPI_CHG0EN': {
					'address': 0x4001F000,
					'description': 'Enable channel group 0',
				},
			'PPI_TASK1': { 'address': 0x4001F004, },
			'PPI_CHG0DS': {
					'address': 0x4001F004,
					'description': 'Disable channel group 0',
				},
			'PPI_TASK2': { 'address': 0x4001F008, },
			'PPI_CHG1EN': {
					'address': 0x4001F008,
					'description': 'Enable channel group 1',
				},
			'PPI_TASK3': { 'address': 0x4001F00C, },
			'PPI_CHG1DIS': {
					'address': 0x4001F00C,
					'description': 'Disable channel group 1',
				},
			'PPI_TASK4': { 'address': 0x4001F010, },
			'PPI_CHG2EN': {
					'address': 0x4001F010,
					'description': 'Enable channel group 2',
				},
			'PPI_TASK5': { 'address': 0x4001F014, },
			'PPI_CHG2DIS': {
					'address': 0x4001F014,
					'description': 'Disable channel group 2',
				},
			'PPI_TASK6': { 'address': 0x4001F018, },
			'PPI_CHG3EN': {
					'address': 0x4001F018,
					'description': 'Enable channel group 3',
				},
			'PPI_TASK7': { 'address': 0x4001F01C, },
			'PPI_CHG3DIS': {
					'address': 0x4001F01C,
					'description': 'Disable channel group 3',
				},
			'PPI_TASK8': { 'address': 0x4001F020, },
			'PPI_TASK9': { 'address': 0x4001F024, },
			'PPI_TASK10': { 'address': 0x4001F028, },
			'PPI_TASK11': { 'address': 0x4001F02C, },
			'PPI_TASK12': { 'address': 0x4001F030, },
			'PPI_TASK13': { 'address': 0x4001F034, },
			'PPI_TASK14': { 'address': 0x4001F038, },
			'PPI_TASK15': { 'address': 0x4001F03C, },
			'PPI_TASK16': { 'address': 0x4001F040, },
			'PPI_TASK17': { 'address': 0x4001F044, },
			'PPI_TASK18': { 'address': 0x4001F048, },
			'PPI_TASK19': { 'address': 0x4001F04C, },
			'PPI_TASK20': { 'address': 0x4001F050, },
			'PPI_TASK21': { 'address': 0x4001F054, },
			'PPI_TASK22': { 'address': 0x4001F058, },
			'PPI_TASK23': { 'address': 0x4001F05C, },
			'PPI_TASK24': { 'address': 0x4001F060, },
			'PPI_TASK25': { 'address': 0x4001F064, },
			'PPI_TASK26': { 'address': 0x4001F068, },
			'PPI_TASK27': { 'address': 0x4001F06C, },
			'PPI_TASK28': { 'address': 0x4001F070, },
			'PPI_TASK29': { 'address': 0x4001F074, },
			'PPI_TASK30': { 'address': 0x4001F078, },
			'PPI_TASK31': { 'address': 0x4001F07C, },
			'PPI_EVENT0': { 'address': 0x4001F100, },
			'PPI_EVENT1': { 'address': 0x4001F104, },
			'PPI_EVENT2': { 'address': 0x4001F108, },
			'PPI_EVENT3': { 'address': 0x4001F10C, },
			'PPI_EVENT4': { 'address': 0x4001F110, },
			'PPI_EVENT5': { 'address': 0x4001F114, },
			'PPI_EVENT6': { 'address': 0x4001F118, },
			'PPI_EVENT7': { 'address': 0x4001F11C, },
			'PPI_EVENT8': { 'address': 0x4001F120, },
			'PPI_EVENT9': { 'address': 0x4001F124, },
			'PPI_EVENT10': { 'address': 0x4001F128, },
			'PPI_EVENT11': { 'address': 0x4001F12C, },
			'PPI_EVENT12': { 'address': 0x4001F130, },
			'PPI_EVENT13': { 'address': 0x4001F134, },
			'PPI_EVENT14': { 'address': 0x4001F138, },
			'PPI_EVENT15': { 'address': 0x4001F13C, },
			'PPI_EVENT16': { 'address': 0x4001F140, },
			'PPI_EVENT17': { 'address': 0x4001F144, },
			'PPI_EVENT18': { 'address': 0x4001F148, },
			'PPI_EVENT19': { 'address': 0x4001F14C, },
			'PPI_EVENT20': { 'address': 0x4001F150, },
			'PPI_EVENT21': { 'address': 0x4001F154, },
			'PPI_EVENT22': { 'address': 0x4001F158, },
			'PPI_EVENT23': { 'address': 0x4001F15C, },
			'PPI_EVENT24': { 'address': 0x4001F160, },
			'PPI_EVENT25': { 'address': 0x4001F164, },
			'PPI_EVENT26': { 'address': 0x4001F168, },
			'PPI_EVENT27': { 'address': 0x4001F16C, },
			'PPI_EVENT28': { 'address': 0x4001F170, },
			'PPI_EVENT29': { 'address': 0x4001F174, },
			'PPI_EVENT30': { 'address': 0x4001F178, },
			'PPI_EVENT31': { 'address': 0x4001F17C, },
			'PPI_SHORTS':  { 'address': 0x4001F200, },
			'PPI_INTENSET':{ 'address': 0x4001F304, },
			'PPI_INTENCLR':{ 'address': 0x4001F308, },
			'PPI_REG0':    { 'address': 0x4001F400, },
			'PPI_REG1':    { 'address': 0x4001F404, },
			'PPI_REG2':    { 'address': 0x4001F408, },
			'PPI_REG3':    { 'address': 0x4001F40C, },
			'PPI_REG4':    { 'address': 0x4001F410, },
			'PPI_REG5':    { 'address': 0x4001F414, },
			'PPI_REG6':    { 'address': 0x4001F418, },
			'PPI_REG7':    { 'address': 0x4001F41C, },
			'PPI_REG8':    { 'address': 0x4001F420, },
			'PPI_REG9':    { 'address': 0x4001F424, },
			'PPI_REG10':   { 'address': 0x4001F428, },
			'PPI_REG11':   { 'address': 0x4001F42C, },
			'PPI_REG12':   { 'address': 0x4001F430, },
			'PPI_REG13':   { 'address': 0x4001F434, },
			'PPI_REG14':   { 'address': 0x4001F438, },
			'PPI_REG15':   { 'address': 0x4001F43C, },
			'PPI_REG16':   { 'address': 0x4001F440, },
			'PPI_REG17':   { 'address': 0x4001F444, },
			'PPI_REG18':   { 'address': 0x4001F448, },
			'PPI_REG19':   { 'address': 0x4001F44C, },
			'PPI_REG20':   { 'address': 0x4001F450, },
			'PPI_REG21':   { 'address': 0x4001F454, },
			'PPI_REG22':   { 'address': 0x4001F458, },
			'PPI_REG23':   { 'address': 0x4001F45C, },
			'PPI_REG24':   { 'address': 0x4001F460, },
			'PPI_REG25':   { 'address': 0x4001F464, },
			'PPI_REG26':   { 'address': 0x4001F468, },
			'PPI_REG27':   { 'address': 0x4001F46C, },
			'PPI_REG28':   { 'address': 0x4001F470, },
			'PPI_REG29':   { 'address': 0x4001F474, },
			'PPI_REG30':   { 'address': 0x4001F478, },
			'PPI_REG31':   { 'address': 0x4001F47C, },
			'PPI_CHEN': {
					'address': 0x4001F500,
					'description': 'Channel enable',
					'bitfields': {
						'CH0': { 'slice': (0,), 'description': '''0: Disable
1: Enable''',
								'access': 'R/W' },
						'CH1': { 'slice': (1,), 'access': 'R/W' },
						'CH2': { 'slice': (2,), 'access': 'R/W' },
						'CH3': { 'slice': (3,), 'access': 'R/W' },
						'CH4': { 'slice': (4,), 'access': 'R/W' },
						'CH5': { 'slice': (5,), 'access': 'R/W' },
						'CH6': { 'slice': (6,), 'access': 'R/W' },
						'CH7': { 'slice': (7,), 'access': 'R/W' },
						'CH8': { 'slice': (8,), 'access': 'R/W' },
						'CH9': { 'slice': (9,), 'access': 'R/W' },
						'CH10': { 'slice': (10,), 'access': 'R/W' },
						'CH11': { 'slice': (11,), 'access': 'R/W' },
						'CH12': { 'slice': (12,), 'access': 'R/W' },
						'CH13': { 'slice': (13,), 'access': 'R/W' },
						'CH14': { 'slice': (14,), 'access': 'R/W' },
						'CH15': { 'slice': (15,), 'access': 'R/W' },
						'CH16': { 'slice': (16,), 'access': 'R/W' },
						'CH17': { 'slice': (17,), 'access': 'R/W' },
						'CH18': { 'slice': (18,), 'access': 'R/W' },
						'CH19': { 'slice': (19,), 'access': 'R/W' },
						'CH20': { 'slice': (20,), 'access': 'R/W' },
						'CH21': { 'slice': (21,), 'access': 'R/W' },
						'CH22': { 'slice': (22,), 'access': 'R/W' },
						'CH23': { 'slice': (23,), 'access': 'R/W' },
						'CH24': { 'slice': (24,), 'access': 'R/W' },
						'CH25': { 'slice': (25,), 'access': 'R/W' },
						'CH26': { 'slice': (26,), 'access': 'R/W' },
						'CH27': { 'slice': (27,), 'access': 'R/W' },
						'CH28': { 'slice': (28,), 'access': 'R/W' },
						'CH29': { 'slice': (29,), 'access': 'R/W' },
						'CH30': { 'slice': (30,), 'access': 'R/W' },
						'CH31': { 'slice': (31,), 'access': 'R/W' },
						},
				},
			############ @@@@@@@@@@@ ############
			'PPI_CHENSET': {
					'address': 0x4001F504,
					'description': 'Channel enable set',
					'bitfields': {
						'CH0': { 'slice': (0,), 'description': '''Enable channel 0.
W1: Enable
R1: Enabled
R0: Disabled''',
								'access': 'R/W' },
						'CH1': { 'slice': (1,), 'access': 'R/W' },
						'CH2': { 'slice': (2,), 'access': 'R/W' },
						'CH3': { 'slice': (3,), 'access': 'R/W' },
						'CH4': { 'slice': (4,), 'access': 'R/W' },
						'CH5': { 'slice': (5,), 'access': 'R/W' },
						'CH6': { 'slice': (6,), 'access': 'R/W' },
						'CH7': { 'slice': (7,), 'access': 'R/W' },
						'CH8': { 'slice': (8,), 'access': 'R/W' },
						'CH9': { 'slice': (9,), 'access': 'R/W' },
						'CH10': { 'slice': (10,), 'access': 'R/W' },
						'CH11': { 'slice': (11,), 'access': 'R/W' },
						'CH12': { 'slice': (12,), 'access': 'R/W' },
						'CH13': { 'slice': (13,), 'access': 'R/W' },
						'CH14': { 'slice': (14,), 'access': 'R/W' },
						'CH15': { 'slice': (15,), 'access': 'R/W' },
						'CH16': { 'slice': (16,), 'access': 'R/W' },
						'CH17': { 'slice': (17,), 'access': 'R/W' },
						'CH18': { 'slice': (18,), 'access': 'R/W' },
						'CH19': { 'slice': (19,), 'access': 'R/W' },
						'CH20': { 'slice': (20,), 'access': 'R/W' },
						'CH21': { 'slice': (21,), 'access': 'R/W' },
						'CH22': { 'slice': (22,), 'access': 'R/W' },
						'CH23': { 'slice': (23,), 'access': 'R/W' },
						'CH24': { 'slice': (24,), 'access': 'R/W' },
						'CH25': { 'slice': (25,), 'access': 'R/W' },
						'CH26': { 'slice': (26,), 'access': 'R/W' },
						'CH27': { 'slice': (27,), 'access': 'R/W' },
						'CH28': { 'slice': (28,), 'access': 'R/W' },
						'CH29': { 'slice': (29,), 'access': 'R/W' },
						'CH30': { 'slice': (30,), 'access': 'R/W' },
						'CH31': { 'slice': (31,), 'access': 'R/W' },
						},
				},
			'PPI_CHENCLR': {
					'address': 0x4001F508,
					'description': 'Channel enable clear',
					### I think there is a bug in the documentation!  Section 15.2.3
						'CH0': { 'slice': (0,), 'access': 'R/W' },
						'CH1': { 'slice': (1,), 'access': 'R/W' },
						'CH2': { 'slice': (2,), 'access': 'R/W' },
						'CH3': { 'slice': (3,), 'access': 'R/W' },
						'CH4': { 'slice': (4,), 'access': 'R/W' },
						'CH5': { 'slice': (5,), 'access': 'R/W' },
						'CH6': { 'slice': (6,), 'access': 'R/W' },
						'CH7': { 'slice': (7,), 'access': 'R/W' },
						'CH8': { 'slice': (8,), 'access': 'R/W' },
						'CH9': { 'slice': (9,), 'access': 'R/W' },
						'CH10': { 'slice': (10,), 'access': 'R/W' },
						'CH11': { 'slice': (11,), 'access': 'R/W' },
						'CH12': { 'slice': (12,), 'access': 'R/W' },
						'CH13': { 'slice': (13,), 'access': 'R/W' },
						'CH14': { 'slice': (14,), 'access': 'R/W' },
						'CH15': { 'slice': (15,), 'access': 'R/W' },
						'CH16': { 'slice': (16,), 'access': 'R/W' },
						'CH17': { 'slice': (17,), 'access': 'R/W' },
						'CH18': { 'slice': (18,), 'access': 'R/W' },
						'CH19': { 'slice': (19,), 'access': 'R/W' },
						'CH20': { 'slice': (20,), 'access': 'R/W' },
						'CH21': { 'slice': (21,), 'access': 'R/W' },
						'CH22': { 'slice': (22,), 'access': 'R/W' },
						'CH23': { 'slice': (23,), 'access': 'R/W' },
						'CH24': { 'slice': (24,), 'access': 'R/W' },
						'CH25': { 'slice': (25,), 'access': 'R/W' },
						'CH26': { 'slice': (26,), 'access': 'R/W' },
						'CH27': { 'slice': (27,), 'access': 'R/W' },
						'CH28': { 'slice': (28,), 'access': 'R/W' },
						'CH29': { 'slice': (29,), 'access': 'R/W' },
						'CH30': { 'slice': (30,), 'access': 'R/W' },
						'CH31': { 'slice': (31,), 'access': 'R/W' },
				},
			'PPI_CH0EEP': {
					'address': 0x4001F510,
					'description': 'Channel 0 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH0TEP': {
					'address': 0x4001F514,
					'description': 'Channel 0 task endpoint. Pointer to task register. Accepts only addresses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH1EEP': {
					'address': 0x4001F518,
					'description': 'Channel 1 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH1TEP': {
					'address': 0x4001F51C,
					'description': 'Channel 1 task endpoint. Pointer to task register. Accepts only addresses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH2EEP': {
					'address': 0x4001F520,
					'description': 'Channel 2 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH2TEP': {
					'address': 0x4001F524,
					'description': 'Channel 2 task endpoint. Pointer to task register. Accepts only addresses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH3EEP': {
					'address': 0x4001F528,
					'description': 'Channel 3 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH3TEP': {
					'address': 0x4001F52C,
					'description': 'Channel 3 task endpoint. Pointer to task register. Accepts only addresses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH4EEP': {
					'address': 0x4001F530,
					'description': 'Channel 4 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH4TEP': {
					'address': 0x4001F534,
					'description': 'Channel 4 task endpoint. Pointer to task register. Accepts only addresses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH5EEP': {
					'address': 0x4001F538,
					'description': 'Channel 5 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH5TEP': {
					'address': 0x4001F53C,
					'description': 'Channel 5 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH6EEP': {
					'address': 0x4001F540,
					'description': 'Channel 6 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH6TEP': {
					'address': 0x4001F544,
					'description': 'Channel 6 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH7EEP': {
					'address': 0x4001F548,
					'description': 'Channel 7 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH7TEP': {
					'address': 0x4001F54C,
					'description': 'Channel 7 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH8EEP': {
					'address': 0x4001F550,
					'description': 'Channel 8 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH8TEP': {
					'address': 0x4001F554,
					'description': 'Channel 8 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH9EEP': {
					'address': 0x4001F558,
					'description': 'Channel 9 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH9TEP': {
					'address': 0x4001F55C,
					'description': 'Channel 9 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH10EEP': {
					'address': 0x4001F560,
					'description': 'Channel 10 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH10TEP': {
					'address': 0x4001F564,
					'description': 'Channel 10 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH11EEP': {
					'address': 0x4001F568,
					'description': 'Channel 11 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH11TEP': {
					'address': 0x4001F56C,
					'description': 'Channel 11 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH12EEP': {
					'address': 0x4001F570,
					'description': 'Channel 12 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH12TEP': {
					'address': 0x4001F574,
					'description': 'Channel 12 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH13EEP': {
					'address': 0x4001F578,
					'description': 'Channel 13 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH13TEP': {
					'address': 0x4001F57C,
					'description': 'Channel 13 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH14EEP': {
					'address': 0x4001F580,
					'description': 'Channel 14 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH14TEP': {
					'address': 0x4001F584,
					'description': 'Channel 14 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CH15EEP': {
					'address': 0x4001F588,
					'description': 'Channel 15 event endpoint. Pointer to event register. Accepts only addresses to registers from the event group.',
					'access': 'R/W',
				},
			'PPI_CH15TEP': {
					'address': 0x4001F58C,
					'description': 'Channel 15 task endpoint. Pointer to task register. Accepts only addreses to registers from the task group.',
					'access': 'R/W',
				},
			'PPI_CHG0': {
					'address': 0x4001F800,
					'description': '''Channel group 0. Include or exclude channel in group 0.
0: Exclude
1: Include''',
					'access': 'R/W',
							'CH0': {
								'slice': (0,),
								'description': '''Include or exclude channel 0 in group 0.
0: Exclude
1: Include''',
								'access': 'R/W',
							},
							'CH1': { 'slice': (1,), 'description': 'Include or exclude channel 1 in group 0.'},
							'CH2': { 'slice': (2,), 'description': 'Include or exclude channel 2 in group 0.'},
							'CH3': { 'slice': (3,), 'description': 'Include or exclude channel 3 in group 0.'},
							'CH4': { 'slice': (4,), 'description': 'Include or exclude channel 4 in group 0.'},
							'CH5': { 'slice': (5,), 'description': 'Include or exclude channel 5 in group 0.'},
							'CH6': { 'slice': (6,), 'description': 'Include or exclude channel 6 in group 0.'},
							'CH7': { 'slice': (7,), 'description': 'Include or exclude channel 7 in group 0.'},
							'CH8': { 'slice': (8,), 'description': 'Include or exclude channel 8 in group 0.'},
							'CH9': { 'slice': (9,), 'description': 'Include or exclude channel 9 in group 0.'},
							'CH10': { 'slice': (10,), 'description': 'Include or exclude channel 10 in group 0.'},
							'CH11': { 'slice': (11,), 'description': 'Include or exclude channel 11 in group 0.'},
							'CH12': { 'slice': (12,), 'description': 'Include or exclude channel 12 in group 0.'},
							'CH13': { 'slice': (13,), 'description': 'Include or exclude channel 13 in group 0.'},
							'CH14': { 'slice': (14,), 'description': 'Include or exclude channel 14 in group 0.'},
							'CH15': { 'slice': (15,), 'description': 'Include or exclude channel 15 in group 0.'},
							'CH20': { 'slice': (20,), 'description': 'Include or exclude channel 20 in group 0.'},
							'CH21': { 'slice': (21,), 'description': 'Include or exclude channel 21 in group 0.'},
							'CH22': { 'slice': (22,), 'description': 'Include or exclude channel 22 in group 0.'},
							'CH23': { 'slice': (23,), 'description': 'Include or exclude channel 23 in group 0.'},
							'CH24': { 'slice': (24,), 'description': 'Include or exclude channel 24 in group 0.'},
							'CH25': { 'slice': (25,), 'description': 'Include or exclude channel 25 in group 0.'},
							'CH26': { 'slice': (26,), 'description': 'Include or exclude channel 26 in group 0.'},
							'CH27': { 'slice': (27,), 'description': 'Include or exclude channel 27 in group 0.'},
							'CH28': { 'slice': (28,), 'description': 'Include or exclude channel 28 in group 0.'},
							'CH29': { 'slice': (29,), 'description': 'Include or exclude channel 29 in group 0.'},
							'CH30': { 'slice': (30,), 'description': 'Include or exclude channel 30 in group 0.'},
							'CH31': { 'slice': (31,), 'description': 'Include or exclude channel 31 in group 0.'},
				},
			'PPI_CHG1': {
					'address': 0x4001F804,
					'description': '''Channel group 1. Include or exclude channel in group 1.
0: Exclude
1: Include''',
					'access': 'R/W',
					'bitfields': {
							'CH0': {
								'slice': (0,),
								'description': '''Include or exclude channel 0 in group 1.
0: Exclude
1: Include''',
								'access': 'R/W',
							},
							'CH1': { 'slice': (1,), 'description': 'Include or exclude channel 1 in group 1.'},
							'CH2': { 'slice': (2,), 'description': 'Include or exclude channel 2 in group 1.'},
							'CH3': { 'slice': (3,), 'description': 'Include or exclude channel 3 in group 1.'},
							'CH4': { 'slice': (4,), 'description': 'Include or exclude channel 4 in group 1.'},
							'CH5': { 'slice': (5,), 'description': 'Include or exclude channel 5 in group 1.'},
							'CH6': { 'slice': (6,), 'description': 'Include or exclude channel 6 in group 1.'},
							'CH7': { 'slice': (7,), 'description': 'Include or exclude channel 7 in group 1.'},
							'CH8': { 'slice': (8,), 'description': 'Include or exclude channel 8 in group 1.'},
							'CH9': { 'slice': (9,), 'description': 'Include or exclude channel 9 in group 1.'},
							'CH10': { 'slice': (10,), 'description': 'Include or exclude channel 10 in group 1.'},
							'CH11': { 'slice': (11,), 'description': 'Include or exclude channel 11 in group 1.'},
							'CH12': { 'slice': (12,), 'description': 'Include or exclude channel 12 in group 1.'},
							'CH13': { 'slice': (13,), 'description': 'Include or exclude channel 13 in group 1.'},
							'CH14': { 'slice': (14,), 'description': 'Include or exclude channel 14 in group 1.'},
							'CH15': { 'slice': (15,), 'description': 'Include or exclude channel 15 in group 1.'},
							'CH20': { 'slice': (20,), 'description': 'Include or exclude channel 20 in group 1.'},
							'CH21': { 'slice': (21,), 'description': 'Include or exclude channel 21 in group 1.'},
							'CH22': { 'slice': (22,), 'description': 'Include or exclude channel 22 in group 1.'},
							'CH23': { 'slice': (23,), 'description': 'Include or exclude channel 23 in group 1.'},
							'CH24': { 'slice': (24,), 'description': 'Include or exclude channel 24 in group 1.'},
							'CH25': { 'slice': (25,), 'description': 'Include or exclude channel 25 in group 1.'},
							'CH26': { 'slice': (26,), 'description': 'Include or exclude channel 26 in group 1.'},
							'CH27': { 'slice': (27,), 'description': 'Include or exclude channel 27 in group 1.'},
							'CH28': { 'slice': (28,), 'description': 'Include or exclude channel 28 in group 1.'},
							'CH29': { 'slice': (29,), 'description': 'Include or exclude channel 29 in group 1.'},
							'CH30': { 'slice': (30,), 'description': 'Include or exclude channel 30 in group 1.'},
							'CH31': { 'slice': (31,), 'description': 'Include or exclude channel 31 in group 1.'},
						},
				},
			'PPI_CHG2': {
					'address': 0x4001F808,
					'description': '''Channel group 2. Include or exclude channel in group 2.
0: Exclude
1: Include''',
					'access': 'R/W',
					'bitfields': {
							'CH0': {
								'slice': (0,),
								'description': '''Include or exclude channel 0 in group 2.
0: Exclude
1: Include''',
								'access': 'R/W',
							},
							'CH1': { 'slice': (1,), 'description': 'Include or exclude channel 1 in group 2.'},
							'CH2': { 'slice': (2,), 'description': 'Include or exclude channel 2 in group 2.'},
							'CH3': { 'slice': (3,), 'description': 'Include or exclude channel 3 in group 2.'},
							'CH4': { 'slice': (4,), 'description': 'Include or exclude channel 4 in group 2.'},
							'CH5': { 'slice': (5,), 'description': 'Include or exclude channel 5 in group 2.'},
							'CH6': { 'slice': (6,), 'description': 'Include or exclude channel 6 in group 2.'},
							'CH7': { 'slice': (7,), 'description': 'Include or exclude channel 7 in group 2.'},
							'CH8': { 'slice': (8,), 'description': 'Include or exclude channel 8 in group 2.'},
							'CH9': { 'slice': (9,), 'description': 'Include or exclude channel 9 in group 2.'},
							'CH10': { 'slice': (10,), 'description': 'Include or exclude channel 10 in group 2.'},
							'CH11': { 'slice': (11,), 'description': 'Include or exclude channel 11 in group 2.'},
							'CH12': { 'slice': (12,), 'description': 'Include or exclude channel 12 in group 2.'},
							'CH13': { 'slice': (13,), 'description': 'Include or exclude channel 13 in group 2.'},
							'CH14': { 'slice': (14,), 'description': 'Include or exclude channel 14 in group 2.'},
							'CH15': { 'slice': (15,), 'description': 'Include or exclude channel 15 in group 2.'},
							'CH20': { 'slice': (20,), 'description': 'Include or exclude channel 20 in group 2.'},
							'CH21': { 'slice': (21,), 'description': 'Include or exclude channel 21 in group 2.'},
							'CH22': { 'slice': (22,), 'description': 'Include or exclude channel 22 in group 2.'},
							'CH23': { 'slice': (23,), 'description': 'Include or exclude channel 23 in group 2.'},
							'CH24': { 'slice': (24,), 'description': 'Include or exclude channel 24 in group 2.'},
							'CH25': { 'slice': (25,), 'description': 'Include or exclude channel 25 in group 2.'},
							'CH26': { 'slice': (26,), 'description': 'Include or exclude channel 26 in group 2.'},
							'CH27': { 'slice': (27,), 'description': 'Include or exclude channel 27 in group 2.'},
							'CH28': { 'slice': (28,), 'description': 'Include or exclude channel 28 in group 2.'},
							'CH29': { 'slice': (29,), 'description': 'Include or exclude channel 29 in group 2.'},
							'CH30': { 'slice': (30,), 'description': 'Include or exclude channel 30 in group 2.'},
							'CH31': { 'slice': (31,), 'description': 'Include or exclude channel 31 in group 2.'},
							},
				},
			'PPI_CHG3': {
					'address': 0x4001F80C,
					'description': '''Channel group 3. Include or exclude channel in group 3.
0: Exclude
1: Include''',
					'access': 'R/W',
					'bitfields': {
							'CH0': {
								'slice': (0,),
								'description': '''Include or exclude channel 0 in group 3.
0: Exclude
1: Include''',
								'access': 'R/W',
							},
							'CH1': { 'slice': (1,), 'description': 'Include or exclude channel 1 in group 3.'},
							'CH2': { 'slice': (2,), 'description': 'Include or exclude channel 2 in group 3.'},
							'CH3': { 'slice': (3,), 'description': 'Include or exclude channel 3 in group 3.'},
							'CH4': { 'slice': (4,), 'description': 'Include or exclude channel 4 in group 3.'},
							'CH5': { 'slice': (5,), 'description': 'Include or exclude channel 5 in group 3.'},
							'CH6': { 'slice': (6,), 'description': 'Include or exclude channel 6 in group 3.'},
							'CH7': { 'slice': (7,), 'description': 'Include or exclude channel 7 in group 3.'},
							'CH8': { 'slice': (8,), 'description': 'Include or exclude channel 8 in group 3.'},
							'CH9': { 'slice': (9,), 'description': 'Include or exclude channel 9 in group 3.'},
							'CH10': { 'slice': (10,), 'description': 'Include or exclude channel 10 in group 3.'},
							'CH11': { 'slice': (11,), 'description': 'Include or exclude channel 11 in group 3.'},
							'CH12': { 'slice': (12,), 'description': 'Include or exclude channel 12 in group 3.'},
							'CH13': { 'slice': (13,), 'description': 'Include or exclude channel 13 in group 3.'},
							'CH14': { 'slice': (14,), 'description': 'Include or exclude channel 14 in group 3.'},
							'CH15': { 'slice': (15,), 'description': 'Include or exclude channel 15 in group 3.'},
							'CH20': { 'slice': (20,), 'description': 'Include or exclude channel 20 in group 3.'},
							'CH21': { 'slice': (21,), 'description': 'Include or exclude channel 21 in group 3.'},
							'CH22': { 'slice': (22,), 'description': 'Include or exclude channel 22 in group 3.'},
							'CH23': { 'slice': (23,), 'description': 'Include or exclude channel 23 in group 3.'},
							'CH24': { 'slice': (24,), 'description': 'Include or exclude channel 24 in group 3.'},
							'CH25': { 'slice': (25,), 'description': 'Include or exclude channel 25 in group 3.'},
							'CH26': { 'slice': (26,), 'description': 'Include or exclude channel 26 in group 3.'},
							'CH27': { 'slice': (27,), 'description': 'Include or exclude channel 27 in group 3.'},
							'CH28': { 'slice': (28,), 'description': 'Include or exclude channel 28 in group 3.'},
							'CH29': { 'slice': (29,), 'description': 'Include or exclude channel 29 in group 3.'},
							'CH30': { 'slice': (30,), 'description': 'Include or exclude channel 30 in group 3.'},
							'CH31': { 'slice': (31,), 'description': 'Include or exclude channel 31 in group 3.'},
						},
				},

			############## GPIO ##################
			'GPIO_OUT': {
					'address': 0x50000504,
					'description': 'Write GPIO port. Register to write to the whole GPIO port.  Bit position in register relates to pin number in GPIO port, e.g., bit 0 relates to GPIO pin number 0.',
					'access': 'R/W',
					'default': 0,
				},
			'GPIO_OUTSET': {
					'address': 0x50000508,
					'description': '''Set individual bits in GPIO port. Register to set pins in the GPIO port high ('1'). Bit position in register relates to pin number in GPIO port, e.g., bit 0 relates to GPIO pin number 0. Setting a '1' in one of the bits in the register will set the corresponding bint in the GPIO port high.''',
					'access': 'R/W',
					'default': 0,
				},
			'GPIO_OUTCLR': {
					'address': 0x5000050C,
					'description': '''Clear individual bits in GPIO port. Register to clear pins in the GPIO port low ('0'). Bit position in register relates to pin number in GPIO port, e.g., bit 0 relates to GPIO pin number 0. Setting a '1' in one of the bits in the register will set the corresponding bit in the GPIO port low.''',
					'access': 'R/W',
					'default': 0,
				},
			'GPIO_IN': {
					'address': 0x50000510,
					'description': 'Read GPIO port. Register to read the whole GPIO port. Bit position in register relates to pin number in GPIO port, e.g., bit 0 relates to GPIO pin number 0',
					'access': 'R',
					'default': 0,
				},
			'GPIO_DIR': {
					'address': 0x50000514,
					'description': '''Direction of GPIO pins. Register to set direction of pins in the GPIO. Bit position in register relates to pin number in GPIO port, e.g., bit 0 relates to GPIO pin number 0. Setting a '1' in one of the bits in the register will configure the corresponding GPOI pin as an output pin.  Setting the same bit to '0' will configure GPIO pin as an input.''',
					'access': 'R/W',
					'default': 0,
				},
			'GPIO_DIRSET': {
					'address': 0x50000518,
					'description': '''Setting DIR register. Register to set individual bits in the DIR register, which subsequently sets individual GPIO pins as outputs.  Setting a '1' in one or more bits in this register will set the corresponding bits in the DIR register.''',
					'access': 'R/W',
					'default': 0,
				},
			'GPIO_DIRCLR': {
					'address': 0x5000051C,
					'description': '''Clearing DIR register. Register to clear individual bits in the DIR register, which subsequently sets individual GPIO pins as input.  Setting a '1' in one or more bits in this register will clear the corresponding bits in the DIR register.''',
					'access': 'R/W',
					'default': 0,
				},
			'GPIO_CNF0': {
					'address': 0x50000700,
					'description': 'Configuration of pin 0.',
					'bitfields': {
							'DIR': {
									'slice': (0,),
									'description': '''Pin direction.
0: input
1: output''',
									'default': 0,
									'access': 'R/W',
								},
							'INPUT': {
									'slice': (1,),
									'description': '''Connect or disconnect input buffer.
0: connect
1: disconnect''',
									'access': 'R/W',
									'default': 0,
								},
							'PULL': {
									'slice': (3,2),
									'description': '''0: Disabled (No pull)
1: Pulldown
3: Pullup''',
									'access': 'R/W',
									'default': 0,
								},
							'DRIVE': {
									'slice': (10,8),
									'description': '''0: Standard 0, standard 1
1: High drive 0, standard 1
2: Standard 0, high drive 1
3: High drive 0, high drive 1
4: Disconnect 0, standard 1
5: Disconnect 0, high drive 1
6: Standard 0, disconnect 1
7: High drive 0, disconnect 1''',
									'access': 'R/W',
									'default': 0,
								},
							'SENSE': {
									'slice': (17,16),
									'description': '''0: Disabled
2: Sense for high level
3: Sense for low level''',
									'default': 0,
									'access': 'R/W',
								},
						},
				},
			'GPIO_CNF1': { 'address': 0x50000704, 'description': 'Configuration of pin 1', },
			'GPIO_CNF2': { 'address': 0x50000708, 'description': 'Configuration of pin 2', },
			'GPIO_CNF3': { 'address': 0x5000070C, 'description': 'Configuration of pin 3', },
			'GPIO_CNF4': { 'address': 0x50000710, 'description': 'Configuration of pin 4', },
			'GPIO_CNF5': { 'address': 0x50000714, 'description': 'Configuration of pin 5', },
			'GPIO_CNF6': { 'address': 0x50000718, 'description': 'Configuration of pin 6', },
			'GPIO_CNF7': { 'address': 0x5000071C, 'description': 'Configuration of pin 7', },
			'GPIO_CNF8': { 'address': 0x50000720, 'description': 'Configuration of pin 8', },
			'GPIO_CNF9': { 'address': 0x50000724, 'description': 'Configuration of pin 9', },
			'GPIO_CNF10': { 'address': 0x50000728, 'description': 'Configuration of pin 10', },
			'GPIO_CNF11': { 'address': 0x5000072C, 'description': 'Configuration of pin 11', },
			'GPIO_CNF12': { 'address': 0x50000730, 'description': 'Configuration of pin 12', },
			'GPIO_CNF13': { 'address': 0x50000734, 'description': 'Configuration of pin 13', },
			'GPIO_CNF14': { 'address': 0x50000738, 'description': 'Configuration of pin 14', },
			'GPIO_CNF15': { 'address': 0x5000073C, 'description': 'Configuration of pin 15', },
			'GPIO_CNF16': { 'address': 0x50000740, 'description': 'Configuration of pin 16', },
			'GPIO_CNF17': { 'address': 0x50000744, 'description': 'Configuration of pin 17', },
			'GPIO_CNF18': { 'address': 0x50000748, 'description': 'Configuration of pin 18', },
			'GPIO_CNF19': { 'address': 0x5000074C, 'description': 'Configuration of pin 19', },
			'GPIO_CNF20': { 'address': 0x50000750, 'description': 'Configuration of pin 20', },
			'GPIO_CNF21': { 'address': 0x50000754, 'description': 'Configuration of pin 21', },
			'GPIO_CNF22': { 'address': 0x50000758, 'description': 'Configuration of pin 22', },
			'GPIO_CNF23': { 'address': 0x5000075C, 'description': 'Configuration of pin 23', },
			'GPIO_CNF24': { 'address': 0x50000760, 'description': 'Configuration of pin 24', },
			'GPIO_CNF25': { 'address': 0x50000764, 'description': 'Configuration of pin 25', },
			'GPIO_CNF26': { 'address': 0x50000768, 'description': 'Configuration of pin 26', },
			'GPIO_CNF27': { 'address': 0x5000076C, 'description': 'Configuration of pin 27', },
			'GPIO_CNF28': { 'address': 0x50000770, 'description': 'Configuration of pin 28', },
			'GPIO_CNF29': { 'address': 0x50000774, 'description': 'Configuration of pin 29', },
			'GPIO_CNF30': { 'address': 0x50000778, 'description': 'Configuration of pin 30', },
			'GPIO_CNF31': { 'address': 0x5000077C, 'description': 'Configuration of pin 31', },
		},

		############### RADIO:  0x40001000 ################
		##### RADIO tasks #######
		'RADIO_TXEN': {
				'address': 0x40001000, 'module': 'RADIO',
				'description': 'Enable radio in TX mode',
			},
		'RADIO_RXEN': {
				'address': 0x40001004, 'module': 'RADIO',
				'description': 'Enable radio in RX mode',
			},
		'RADIO_START': {
				'address': 0x40001008, 'module': 'RADIO',
				'description': 'Start radio',
			},
		'RADIO_STOP': {
				'address': 0x4000100C, 'module': 'RADIO',
				'description': 'Stop radio',
			},
		'RADIO_DISABLE': {
				'address': 0x40001010, 'module': 'RADIO',
				'description': 'Disable radio',
			},
		'RADIO_RSSISTART': {
				'address': 0x40001014, 'module': 'RADIO',
				'description': 'Task for starting the RSSI and take one single sample of the receive signal strength',
			},
		'RADIO_RSSISTOT': {
				'address': 0x40001018, 'module': 'RADIO',
				'description': 'Task for stopping the RSSI and take one single sample of the receive signal strength',
			},
		'RADIO_BCSTART': {
				'address': 0x4000101C, 'module': 'RADIO',
				'description': 'Start bit counter',
			},
		'RADIO_BCSTOP': {
				'address': 0x40001020, 'module': 'RADIO',
				'description': 'Stop bit counter',
			},
		#### RADIO events ######
		'RADIO_READY': {
				'address': 0x40001100, 'module': 'RADIO',
				'description': 'Ready event',
			},
		'RADIO_ADDRESS': {
				'address': 0x40001104, 'module': 'RADIO',
				'description': 'Address event',
			},
		'RADIO_PAYLOAD': {
				'address': 0x40001108, 'module': 'RADIO',
				'description': 'Payload event',
			},
		'RADIO_END': {
				'address': 0x4000110C, 'module': 'RADIO',
				'description': 'End event',
			},
		'RADIO_DISABLED': {
				'address': 0x40001110, 'module': 'RADIO',
				'description': 'Disabled event',
			},
		'RADIO_DEVMATCH': {
				'address': 0x40001114, 'module': 'RADIO',
				'description': 'A device address match occurred on the last received packet',
			},
		'RADIO_DEVMISS': {
				'address': 0x4001118, 'module': 'RADIO',
				'description': 'No device address match occurred on the last received packet',
			},
		'RADIO_RSSIEND': {
				'address': 0x4000111C, 'module': 'RADIO',
				'description': 'Sampling of received signal strength complete. A new RSSI sample is ready for readout from the RSSISAMPLE register',
			},
		'RADIO_BCMATCH': {
				'address': 0x40001128, 'module': 'RADIO',
				'description': 'Bit counter reached bit count value specified in BCC',
			},
		'RADIO_SHORTS': {
				'address': 0x40001200, 'module': 'RADIO',
				'description': 'Shortcuts for the radio',
				'bitfields': {
						'READY_START': {
								'slice': (0,),
								'description': 'Enable or disable shortcut between READY event and START task',
								'access': 'R/W',
								'default': 0,
							},
						'END_DISABLE': {
								'slice': (1,),
								'description': 'Enable or disable shortcut between END event and DISABLE task',
								'access': 'R/W',
								'default': 0,
							},
						'DISABLED_TXEN': {
								'slice': (2,),
								'description': 'Enable or disable shortcut between DISABLED event and TXEN task',
								'access': 'R/W',
								'default': 0,
							},
						'DISABLED_RXEN': {
								'slice': (3,),
								'description': 'Enable or disable shortcut between DISABLED event and RXEN task',
								'access': 'R/W',
								'default': 0,
							},
						'ADDRESS_RSSISTART': {
								'slice': (4,),
								'description': 'Enable or disable shortcut between ADDRESS event and RSSISTART task',
								'access': 'R/W',
								'default': 0,
							},
						'END_START': {
								'slice': (5,),
								'description': 'Enable or disable shortcut between END event and START task',
								'access': 'R/W',
								'default': 0,
							},
						'ADDRESS_BCSTART': {
								'slice': (6,),
								'description': 'Enable or disable shortcut between ADDRESS event and BCSTART task',
								'access': 'R/W',
								'default': 0,
							},
						'DISABLED_RSSISTOP': {
								'slice': (8,),
								'description': 'Enable or disable shortcut between DISABLED event and RSSISTOP task',
								'access': 'R/W',
								'default': 0,
							},
					},
			},
		'RADIO_INTENSET': {
				'address': 0x40001304, 'module': 'RADIO',
				'description': 'Interrupt enable set register',
			},
		'RADIO_INTENCLR': {
				'address': 0x40001308, 'module': 'RADIO',
				'description': 'Interrupt enable clear register',
			},
		'RADIO_CRCSTATUS': {
				'address': 0x40001400, 'module': 'RADIO',
				'description': '''CRC status''',
				'default': 0,
				'bitfields': {
						'CRCSTATUS': {
								'slice': (0,),
								'description': '''CRC status of packet received.
0: Packet received with CRC error
1: Packet received with CRC OK''',
								'access': 'R',
							},
					},
			},
		'RADIO_RXMATCH': {
				'address': 0x40001408, 'module': 'RADIO',
				'description': 'Received address',
				'bitfields': {
						'RXMATCH': {
								'slice': (2,0),
								'description': '''Logical address on which previous packet was received''',
								'access': 'R',
							},
					},
			},
		'RADIO_RXCRC': {
				'address': 0x4000140C, 'module': 'RADIO',
				'description': 'Received CRC',
				'bitfields': {
						'RXCRC': {
								'slice': (23,0),
								'description': '''CRC field of previously received packet''',
								'default': 0,
								'access': 'R',
							},
					},
			},
		'RADIO_DAI': {
				'address': 0x40001410, 'module': 'RADIO',
				'description': '''Device address match index. Packet address to be used for the next transmission or reception. When transmitting, the packet pointed to by this address will be transmitted and when receiving, the received packet will be written to this address.

This address is byte aligned RAM address.

Decision point: START task.
''',
				'bitfields': {
					'DAI': {
							'slice': (2,0),
							'access': 'R',
							'default': 0,
							'description': '''Index(n) of device address, see DAB[n] and DAP[n], that got an address match.''',
						},
					},
			},
		'RADIO_PACKETPTR': {
				'address': 0x40001504, 'module': 'RADIO',
				'description': 'Packet pointer',
			},
		'RADIO_FREQUENCY': {
				'address': 0x40001508, 'module': 'RADIO',
				'description': 'frequency',
				'bitfields': {
						'FREQUENCY': {
								'slice': (6,0),
								'description': '''Radio channel frequency offset in MHz: RF frequency = 2400 + A (MHz). Decision point: TXEN or RXEN.''',
								'access': 'R/W',
								'default': 0,
							},
					},
			},
		'RADIO_TXPOWER': {
				'address': 0x4000150C, 'module': 'RADIO',
				'description': 'Output power',
				'bitfields': {
						'TXPOWER': {
								'slice': (7,0),
								'access': 'R/W',
								'description': '''Radio output power. Decision point: TXEN task.

0x04 (POS_4_DBM): +4 dBm
0    (0_DBM):      0 dBm
0xFC (NEG_4_DBM): -4 dBm
0xF8 (NEG_8_DBM): -8 dBm
0xF4 (NEG_12_DBM):-12 dBm
0xF0 (NEG_16_DBM):-16 dBm
0xEC (NEG_20_DBM):-20 dBm
0xD8 (NEG_30_DBM):-30 dBm''',
								'default': 0,
							},
					},
			},
		'RADIO_MODE': {
				'address': 0x40001510, 'module': 'RADIO',
				'description': 'Data rate and modulation',
				'bitfields': {
						'MODE': {
							'slice': (1,0),
							'access': 'R/W',
							'default': 0,
							'description': '''Radio data rate and modulation setting.  The radio supports Frequency-shift Keying (FSK) modulation, which depending on setting are compatible with either Nordic Semiconductor's proprietary radios, or Bluetooth low energy.

0 (NRF_1MBIT): 1 Mbit/s Nordic proprietary radio mode
1 (NRF_2MBIT): 2 Mbit/s Nordic proprietary radio mode
2 (NRF_250_KBIT) 250 kbit/s Nordic proprietary radio mode
3 (BLE_1MBIT) 1 Mbit/s Bluetooth Low Energy.''',
							},
					},
			},
		'RADIO_PCNF0': {
				'address': 0x40001514, 'module': 'RADIO',
				'description': 'Packet configuration 0',
				'bitfields': {
					'LFLEN': {
							'slice': (3,0),
							'description': '''Length of length field in number of bits. Value 0..8.  Decision point: START task.''',
							'access': 'R/W',
							'default': 0,
						},
					'S0LEN': {
							'slice': (8,),
							'description': '''Length of S0 field in number of bytes. Value 0..1.  Decision point: START task''',
							'access': 'R/W',
							'default': 0,
						},
					'S1LEN': {
							'slice': (19,16),
							'description': '''Length of S1 field in number of bits. Value 0..8.  Decision point: START task.''',
							'access': 'R/W',
							'default': 0,
						},
					},
			},
		'RADIO_PCNF1': {
				'address': 0x40001518, 'module': 'RADIO',
				'description': 'Packet configuration 1',
				'bitfields': {
						'MAXLEN': {
								'slice': (7,0),
								'description': '''Maximum length of packet payload. If the payload of a packet is larger than MAXLEN the radio will only receive MAXLEN number of bytes.

Value 0..255''',
								'access': 'R/W',
								'default': 0,
							},
						'STATLEN': {
								'slice': (15,8),
								'description': '''Static length in number of bytes. The radio will send and receive N bytes more than what is defined in the Length field of the packet. Usually the RADIO will send/receive the number of bytes defined by the Length field in the RADIO packet. If you want to send more than that, you do so by adding a static length of N bytes to the packet.

Decision point: START task.  Value: 0..255.''',
								'access': 'R/W',
								'default': 0,
							},
						'BALEN': {
								'slice': (18,16),
								'description': '''Base address length in number of bytes. The address field is composed of the base address and the one byte long address prefix, e.g. set BALEN=2 to get a total address of 3 bytes.

Decision point: START task. Value: 2..4.''',
								'access': 'R/W',
								'default': 0,
							},
						'ENDIAN': {
								'slice': (24,),
								'description': '''On air endianness of packet length field.

Decision point: START task.
0: Little endian - least-significant bit on air first
1: Big endian - most-significant bit on air first''',
								'access': 'R/W',
								'default': 0,
							},
						'WHITEEN': {
								'slice': (25,),
								'description': '''Packet whitening enabled.
0: Disabled
1: Enabled''',
								'access': 'R/W',
								'default': 0,
							},
					},
			},
		'RADIO_BASE0': {
				'address': 0x4000151C, 'module': 'RADIO',
				'description': 'Base address 0. Decision point: START task.',
				'access': 'R/W',
				'default': 0,
			},
		'RADIO_BASE1': {
				'address': 0x40001520, 'module': 'RADIO',
				'description': 'BASE address 1. Decision point: START task.',
				'access': 'R/W',
				'default': 0,
			},
		'RADIO_PREFIX0': {
				'address': 0x40001524, 'module': 'RADIO',
				'description': 'Prefix bytes for logical addresses 0-3',
				'bitfields': {
					'AP0': {
							'slice': (7,0),
							'description': 'Address prefix 0. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					'AP1': {
							'slice': (15,8),
							'description': 'Address prefix 1. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					'AP2': {
							'slice': (23,16),
							'description': 'Address prefix 2. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					'AP3': {
							'slice': (31,24),
							'description': 'Address prefix 3. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					},
			},
		'RADIO_PREFIX1':  {
				'address': 0x40001528, 'module': 'RADIO',
				'description': 'Prefix bytes for logical addresses 4-7',
					'AP4': {
							'slice': (7,0),
							'description': 'Address prefix 4. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					'AP5': {
							'slice': (15,8),
							'description': 'Address prefix 5. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					'AP6': {
							'slice': (23,16),
							'description': 'Address prefix 6. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
					'AP7': {
							'slice': (31,24),
							'description': 'Address prefix 7. Decision point: START task.',
							'access': 'R/W',
							'default': 0,
						},
			},
		'RADIO_TXADDRESS':  {
				'address': 0x4000152C, 'module': 'RADIO',
				'description': 'Transmit address select',
				'bitfields': {
						'TXADDRESS': {
								'slice': (2, 0),
								'description': '''Logical address to be used when transmitting a packet. Decision point: START task.''',
								'default': 0,
								'access': 'R/W',
							},
					},
			},
		'RADIO_RXADDRESSES': {
				'address': 0x40001530, 'module': 'RADIO',
				'description': 'Receive address select',
				'bitfields': {
						'ADR0': {
								'slice': (0,),
								'description': '''Enable reception on logical address 0. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
								'default': 0,
							},
						'ADR1': {
								'slice': (1,),
								'description': '''Enable reception on logical address 1. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
								'default': 0,
							},
						'ADR2': {
								'slice': (2,),
								'description': '''Enable reception on logical address 2. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
								'default': 0,
							},
						'ADR3': {
								'slice': (3,),
								'description': '''Enable reception on logical address 3. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
							},
						'ADR4': {
								'slice': (4,),
								'description': '''Enable reception on logical address 4. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
							},
						'ADR5': {
								'slice': (5,),
								'description': '''Enable reception on logical address 5. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
							},
						'ADR6': {
								'slice': (6,),
								'description': '''Enable reception on logical address 6. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
							},
						'ADR7': {
								'slice': (7,),
								'description': '''Enable reception on logical address 7. Decision point: START task.
0: Disable
1: Enable''',
								'access': 'R/W',
							},
					},
			},
		'RADIO_CRCCNF': {
				'address': 0x40001534, 'module': 'RADIO',
				'description': 'CRC configuration',
				'bitfields': {
						'LEN': {
								'slice': (1,0),
								'description': '''1..3: CRC length in number of bytes. Decision point: START task.
0: CRC length is zero, and CRC calculation is disabled.''',
								'access': 'R/W',
								'default': 0,
							},
						'SKIP_ADR': {
								'slice': (8,),
								'description': '''Leave packet address field out of CRC calculation.  Decision point: START task.
0: CRC calculation includes address field.
1: CRC calculation does not include address field. The CRC calculation will start at the first byte after the address.''',
								'access': 'R/W',
								'default': 0,
							},
					},
			},
		'RADIO_CRCPOLY': {
				'address': 0x40001538, 'module': 'RADIO',
				'description': 'CRC polynomial',
				'bitfields': {
						'CRCPOLY': {
								'slice': (23,1),
								'description': '''CRC polynomial.
Each term in the CRC polynomial is mapped to a bit in this register whose index corredsponds to the term's exponent. The last significant term/bit is hardwired to 1.
The following example is for an 8-bit CRC polynomial:
x^8 + x^7 + x^3 + x^2 + 1 = 1 1000 1101 
Decision point: START task.''',
								'access': 'R/W',
								'default': 0,
							},
					},
			},
		'RADIO_CRCINIT': {
				'address': 0x4000153C, 'module': 'RADIO',
				'description': 'CRC initial value',
				'bitfields': {
						'CRCINIT': {
								'slice': (23,0),
								'description': '''Initial value for CRC calculation. Decision point: START task.''',
								'default': 0,
								'access': 'R/W',
							},
					},
			},
		'RADIO_TEST': {
				'address': 0x40001540, 'module': 'RADIO',
				'description': 'Test features enable register',
				'bitfields': {
						'CONST_CARRIER': {
								'slice': (0,),
								'descripton': '''Constant carrier. Decision point: TXEN task.
0: Disable
1: Enable''',
								'access': 'R/W',
								'default': 0,
							},
						'PLL_LOCK': {
								'slice': (1,),
								'description': '''PLL lock. Decision point: TXEN or RXEN task.
0: Disable
1: Enable''',
								'access': 'R/W',
								'default': 0,
						},
					},
			},
		'RADIO_TIFS': {
				'address': 0x40001544, 'module': 'RADIO',
				'description': 'Interframe Spacing in us',
				'bitfields': {
						'TIFS': {
								'slice': (7,0),
								'access': 'R/W',
								'default': 0x40,
								'description': '''Interframe spacing.
Interframe space is the time interval between two consecutive packets.  It is defined as the time, in micro seconds, from the end of the last bit of the previous packet to the start of the first bit of the subsequent packet.
Decision point: START task.''',
							},
					},
			},
		'RADIO_RSSISAMPLE': {
				'address': 0x40001548, 'module': 'RADIO',
				'description': 'RSSI sample',
				'bitfields': {
						'RSSISAMPLE': {
								'slice': (6,0),
								'description': '''RSSI sample result. The value of this register is read as a positive value while the actual received signal strength is a negative value. Actual received signal strength is as follows:
Received signal strength = -A[dBm].''',
								'access': 'R/W',
								'default': 0,
							},
					},
			},
		'RADIO_STATE': {
				'address': 0x40001550, 'module': 'RADIO',
				'description': 'Current radio state',
				'bitfields': {
						'STATE': {
								'slice': (3,0),
								'description': '''Current radio state.
0: DISABLED
1: RXRU
2: RXIDLE
3: RX
4: RXDISABLE
9: TXRU
10: TXIDLE
11: TX
12: TXDISABLE''',
								'access': 'R',
								'default': 0,
							},
					},
			},
		'RADIO_DATAWHITEIV': {
				'address': 0x40001554, 'module': 'RADIO',
				'description': 'Data whitening initial value',
				'bitfields': {
						'DATAWHITEIV': {
								'slice': (5,0),
								'default': 0x40,
								'access': 'R/W',
								'description': '''Data whitening initial value. Bit 0 corresponds to Position 6 of the LSFR, Bit 1 to Position 5. etc. Decision point: TXEN and RXEN.''',
							},
					},
			},
		'RADIO_BCC': {
				'address': 0x40001560, 'module': 'RADIO',
				'description': 'Bit counter compare',
				'access': 'R/W',
				'default': 0,
			},
		'RADIO_DAB0': {
				'address': 0x40001600, 'module': 'RADIO',
				'description': 'Device address 0 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB1': {
				'address': 0x40001604, 'module': 'RADIO',
				'description': 'Device address 1 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB2': {
				'address': 0x40001608, 'module': 'RADIO',
				'description': 'Device address 2 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB3': {
				'address': 0x4000160C, 'module': 'RADIO',
				'description': 'Device address 3 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB4': {
				'address': 0x40001610, 'module': 'RADIO',
				'description': 'Device address 4 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB5': {
				'address': 0x40001614, 'module': 'RADIO',
				'description': 'Device address 5 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB6': {
				'address': 0x40001618, 'module': 'RADIO',
				'description': 'Device address 6 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAB7': {
				'address': 0x4000161C, 'module': 'RADIO',
				'description': 'Device address 7 base segment',
				'access': 'R/W',
				'default': 0x40,
			},
		'RADIO_DAP0': {
				'address': 0x40001620, 'module': 'RADIO',
				'description': 'Device address 0 prefix',
				'bitfields': {
					'DAP0': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP1': {
				'address': 0x40001624, 'module': 'RADIO',
				'description': 'Device address 1 prefix',
				'bitfields': {
					'DAP1': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP2': {
				'address': 0x40001628, 'module': 'RADIO',
				'description': 'Device address 2 prefix',
				'bitfields': {
					'DAP2': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP3': {
				'address': 0x4000162C, 'module': 'RADIO',
				'description': 'Device address 3 prefix',
				'bitfields': {
					'DAP3': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP4': {
				'address': 0x40001630, 'module': 'RADIO',
				'description': 'Device address 4 prefix',
				'bitfields': {
					'DAP4': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP5': {
				'address': 0x40001634, 'module': 'RADIO',
				'description': 'Device address 5 prefix',
				'bitfields': {
					'DAP5': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP6': {
				'address': 0x40001638, 'module': 'RADIO',
				'description': 'Device address 6 prefix',
				'bitfields': {
					'DAP6': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DAP7': {
				'address': 0x4000163C, 'module': 'RADIO',
				'description': 'Device address 7 prefix',
				'bitfields': {
					'DAP7': {
						'slice': (15,0),
						'access': 'R/W',
						'default': 0x0040,
					},
				},
			},
		'RADIO_DACNF': {
				'address': 0x40001640, 'module': 'RADIO',
				'description': 'Device address match configuration',
				'bitfields': {
						'ENA0': {
							'slice': (0,),
							'description': '''Enable or disable device address matching using device address 0.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'ENA1': {
							'slice': (1,),
							'description': '''Enable or disable device address matching using device address 1.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'ENA2': {
							'slice': (2,),
							'description': '''Enable or disable device address matching using device address 2.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'ENA3': {
							'slice': (3,),
							'description': '''Enable or disable device address matching using device address 3.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'ENA4': {
							'slice': (4,),
							'description': '''Enable or disable device address matching using device address 4.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'ENA5': {
							'slice': (5,),
							'description': '''Enable or disable device address matching using device address 5.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'ENA6': {
							'slice': (6,),
							'description': '''Enable or disable device address matching using device address 6.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 1,
							},
						'ENA7': {
							'slice': (7,),
							'description': '''Enable or disable device address matching using device address 7.
0: Disable
1: Enable''',
							'access': 'R/W',
							'default': 0
							},
						'TXADD0': {
							'slice': (8,),
							'description': '''TxAdd for device address 0''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD1': {
							'slice': (9,),
							'description': '''TxAdd for device address 1''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD2': {
							'slice': (10,),
							'description': '''TxAdd for device address 2''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD3': {
							'slice': (11,),
							'description': '''TxAdd for device address 3''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD4': {
							'slice': (12,),
							'description': '''TxAdd for device address 4''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD5': {
							'slice': (13,),
							'description': '''TxAdd for device address 5''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD6': {
							'slice': (14,),
							'description': '''TxAdd for device address 6''',
							'access': 'R/W',
							'default': 0,
							},
						'TXADD7': {
							'slice': (15,),
							'description': '''TxAdd for device address 7''',
							'access': 'R/W',
							'default': 0,
							},
					},
			},
		'RADIO_OVERRIDE0': {
				'address': 0x40001724, 'module': 'RADIO',
				'description': 'Override0 - Radio configuration configuration parameters',
				'access': 'R',
				'default': 0,
			},
		'RADIO_OVERRIDE1': {
				'address': 0x40001728, 'module': 'RADIO',
				'description': 'Override1 - Radio configuration configuration parameters',
				'access': 'R',
				'default': 0,
			},
		'RADIO_OVERRIDE2': {
				'address': 0x4000172C, 'module': 'RADIO',
				'description': 'Override2 - Radio configuration configuration parameters',
				'access': 'R',
				'default': 0,
			},
		'RADIO_OVERRIDE3': {
				'address': 0x40001730, 'module': 'RADIO',
				'description': 'Override3 - Radio configuration configuration parameters',
				'access': 'R',
				'default': 0,
			},
		'RADIO_OVERRIDE4': {
				'address': 0x40001734, 'module': 'RADIO',
				'description': 'Override4 - Radio configuration configuration parameters',
				'bitfields': {
						'OVERRIDE': {
								'slice': (30,0),
								'description': 'Radio override',
								'default': 0,
							},
						'OREN': {
								'slice': (31,),
								'description': '''Override control.
0: Disable use of OVERRIDE[n] (n=0..4) registers.
1: Enable use of OVERRIDE[n] (n=0..4) registers.''',
								'default': 0,
							},
					},
			},
		'RADIO_POWER': {
				'address': 0x40001FFC, 'module': 'RADIO',
				'description': 'Peripheral power control',
				'bitfields': {
						'POWER': {
								'slice': (0,),
								'description': '''Peripheral power control. The peripheral and its registers are reset to its initial state by switching the peripheral off and then back on again.
0: Peripheral is powered off
1: Peripheral is powered on''',
								'access': 'R/W',
								'default': 1,
							},
					},
			},
		}



	def sanityCheck(self):
		# do a sanity check
		# extract all field names and sort and list them.
		SFRNames = self._SFR.keys()

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
		if nRF51822SFR._SFR.has_key(sfrName):
			defn = copy.deepcopy(nRF51822SFR._SFR[sfrName])
		else:
			raise NameError(sfrName)
		self.__dict__['_name']        = sfrName
		self.__dict__['_defn']        = defn
		self.__dict__['_address']     = defn['address']
		try:
			self.__dict__['_module']      = defn['module']
		except Exception:
			print 'SFR %s has no module' % sfrName
		try:
			self.__dict__['_description'] = defn['description']
		except Exception:
			print 'SFR %s has no description' % sfrName
		self.__dict__['_value']       = 0
		# self.__dict__['_C'] = 0
		# self.__dict__['_A'] = 0
		self.__dict__['_code'] = None
		self.__dict__['_mcu'] = mcu
		# initialize the value to the power-up default, if any.
		self.powerUpInit()

	def getVarType(self):
		return 'uint32'

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
			try:
				s = field['slice']
			except Exception:
				print 'malformed SFR definition %s' % self._name
				continue
			val = field.get('default',0)
			if not isinstance(val, int):  # (type(val) != type(0)):
				raise TypeError("type of val of %s is %s", self._name, type(val))
			if not isinstance(s, tuple):
				raise TypeError('slice of %s is not tuple: %s' % (self._name, s))
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
			# RHS is an expression, already a code capsule
			self._code = value
		else:
			# RHS is most likely a constant, so we start fresh
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
		# now construct negative of mask
		# use R2 for maskN
		maskN = 0xffffffff ^ mask  # complement the whole word
		# use R2 for maskN
		self._loadImm(maskN, 2) # R2 = maskN (negative mask, for clearing)
		self._loadWord(self._address, 1)  # old SFR value in R1, address in R3
		# first clear the bits in the slice
		self._emit('AND R%d, R%d', 1, 2)  # old SFR (R1) &= maskN (R2)
		if (isinstance(value, int)):
			valMask = (value << p) & mask
			self._loadImm(valMask, 0) # R0 = valMask
		elif (isinstance(value, CodeCapsule)):
			# R0 already contains the value, but we AND the mask
			# construct mask from maskN (currently in R2)
			self._emit('NEG R%d, R%d', 2, 2)
			self._emit('SUB R%d, #0x%x', 2, 1)  # R2 = mask
			self._emit('AND R%d, R%d', 0, 2)    # R0 &= mask
		# in either case, R0 contains the value to OR into masked SFR
		self._emit('ORR R%d, R%d', 0, 1)
		# now write new SFR value (R0) back into SFR, reusing R3 as address
		# (because it was last loaded - don't recompute address).
		self._storeWord(self._address, False)
		return self._code


	def writeSFR(self, value):
		'''This is to write the SFR (by MOV instruction) 
		   Option: check write permission?
		'''
		if value is None:
			return
		if isinstance(value, CodeCapsule):
			self._code = value
		else:
			self._code = CodeCapsule(self._mcu, dest=self,
					src=self)
		if (isinstance(value, int)):
			self._loadImm(value, 0) # R0 = value
		elif (isinstance(value, SFR)) or (isinstance(value, nrf51822var.VAR)) \
				or isinstance(value, CodeCapsule):
					# nothing to do - R0 was already loaded by previous code
			pass
		else:
			raise Exception('writeSFR unsupported value %s' % value)
			# either case the runtime already called value.readSFR() or
			# value.readVar() and put result into R0.
			# now is time to write R0 back into SFR.
		self._storeWord(self._address) # mem[address] = R0
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
					dest=self._mcu.lookupVar('R0'))  # outlet is assumed to be accumulator?
			# special handling: as bit index
			bitindex = int(name[1])
			# If the SFR is bit addressable (i.e., modulo 8) then access
			# using a bit instruction. Otherwise, access as word and return
			# value.
			return self._readBit(self._address, bitindex)
		else:
			self._code = CodeCapsule(self._mcu, src=self,
					dest=self._mcu.lookupVar('R0'))  # outlet is assumed to be accumulator?

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
		self._loadWord(self._address)  # R0 = SFR, R3 = address
		# mask out extra bits and shift
		self._loadImm(mask, 1)  # R1 = mask
		self._emit('AND R%d, R%d', 0, 1) # R0 &= mask
		# now shift right logical
		p = s[1]   # make the code shorter
		if (p != 0):
			self._emit('LSR R%d, R%d, #0x%x', 0, 0, p)
		# otherwise, nothing to do
		return self._code

	def _emit (self, formatStr, *operands):
		self._code.emit(formatStr, *operands)

	def _loadBit(self, bitAddress):
		'''
		This does not apply to ARM/THUMB because there is no bit addressable memory
		'''
		self._emit('MOV C, 0x%x', bitAddress)
		# self._C = (self._value >> (bitAddress & 0x7) ) & 1
		return self._code

	def _writeBit(self, address, bitindex, value):
		'''
			SFR.bitindex = value
			This is done by loading the SFR, OR in the bit, and write back
		'''
		mask = (1 << bitindex)
		# should we worry about alignment?
		if (isinstance(value, int)): # maybe also allow string of '0''1'
			self._loadWord(self._address, 0) # old SFR value
			if (value == 0): # AND in the maskN
				self._emit('MOV R%d, #0x%x', 2, 2) # R2 = 2
				self._emit('NEG R%d, R%d', 2, 2)  # R2 = -2 = 0b111..10
				if (bitindex > 0):  # use rotate instead of shift
					self._emit('MOV R%d, #0x%x', 1, (32 - bitindex)) # R1 = 32-bitIndex
					self._emit('ROR R%d, R%d', 2, 1) # R2 = R2 rotateR (32-bitIndex)
					# same as R2 = ~(1 << bitindex)
				# otherwise, R2 is ready to use (0 is at least-significant bit)
				self._emit('AND R%d, R%d', 0, 2) # clear bit
			elif (value == 1):
				# OR with the bit
				self._emit('MOV R%d, #0x%x', 2, 1) # R2 = 1
				if (bitindex > 0):
					self._emit('LSL R%d, R%d, #%d', 2, 2, bitindex) # R2 = 1 << bitindex
				self._emit('ORR R%d, R%d', 0, 2) # set bit
			else:
				# value too large
				raise ValueError('value %d overflow for bit assignment' % value)
			return self._code
		elif isinstance(value, codecapsule):
			# value is in R0. 
			self._loadWord(self._address, 1) # old SFR value
			self._emit('CMP R%d, #0x%x', 0, 0) # test R0 == 0?
			self._emit('BEQ 0x%x', 6)  # if 0 then jump to clear. 
			# now do the setting (OR in the bit)
			self._emit('MOV R%d, #0x%x', 0, 1) # R0 = 1 [PC+2]
			self._emit('LSL R%d, R%d, #%d', 0, 0, bitindex) # R0 = 1 << bitindex [PC+4]
			self._emit('ORR R%d, R%d', 0, 1) # R0 |= R1 [PC+4]+2
			self._emit('B 0x%x', 8) # unconditionally skip the clear part [PC+4]+4
			# [PC+4] + 6 => the "else" part
			self._emit('MOV R%d, #0x%x', 2, 2) # R2 = 2
			self._emit('NEG R%d, R%d', 2, 2)  # R2 = -2 = 0b111..10
			self._emit('MOV R%d, #0x%x', 1, (32 - bitindex)) # R1 = 32-bitIndex
			self._emit('ROR R%d, R%d', 2, 1) # R2 = R2 rotateR (32-bitIndex)
			# clear this 
			self._emit('AND R%d, R%d', 0, 2) # R1 &= R2
			self._storeWord(self._address, False) # store back into SFR
			# using same address as in R3
		return self._code

	def _readBit(self, address, bitindex):
		'''load byte and extract bit 
		'''
		self._loadByte(self._address) # this does it to memory with MOV
		return self._extractBit(bitindex)  # save in bit accumulator C

	def _loadImm(self, imm, targetReg = 0):
		self._code.loadImm(imm, targetReg)

	def _loadWord(self, address, targetReg = 0):
		'''This generates the MOV instruction to move the SFR into R0 by default,
		   (or to targetReg as specified)
		   leave the effective address in R3.
			 perhaps this method should be moved to code capsule??
			 assumption: this starts at a word boundary, so that
			 data is aligned at word boundary.
		'''
		self._loadImm(address, 3) # load address (as imm) into register R3
		# address is now in R3. so we use R3 to load it into R0.
		self._emit('LDR R%d, [R%d, #%d]', 0, 3, 0)

		# self._A = self._value 
		return self._code


	def _extractBit(self, bitindex):
		'''the byte is in R0, turn it into either 0 or 1. just shift it
		   to the left (all the way to MSB) and then right.
		'''
		self._emit('LSL R%d, R%d, #%d', 0, 0, (31-bitindex))
		self._emit('LSR R%d, R%d, #%d', 0, 0, 31)
		# self._C = (self._A >> bitindex) & 1
		return self._code

	def readSFR(self, dest=None):
		'''This is called by the mcu.SFR to generate instructions to
		   load from SFR as a byte.
		'''
		if dest is None: dest = self._mcu.lookupVar('R0')
		self._code = CodeCapsule(self._mcu, src=self,
				dest=dest)
		self._code.setResultType('uint32')
		return self._loadWord(self._address)

	def _storeWord(self, address, calcAddress = True):
		'''
			this method stores the word (in R0) to the address specified.
			if calcAddress is False, then we just use the address already in R3.
			Otherwise, generate code to calculate the address and leave it in R3.
			Note that in the case of calculating address, the instruction 
			should start on a word boundary, or else PC-relative load (LDR) 
			will not work correctly.

			Should this method be moved to codecapsule?
		'''
		if (calcAddress):
			self._emit('LDR R%d, [PC, #%d]', 3, 0) # from (PC+4) + 0
			self._emit('B 0x%x', 0) # target PC is offset from PC+4
			self._emit('.word 0x%x', address) # this is the actual address literal
		# now R3 has the address. use it to store from R0.
		self._emit('STR R%d, [R%d, #0x%x]', 0, 3, 0)
		return self._code # this seems useless?

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
	c = nRF51822SFR()
	c.sanityCheck()
	U1CSR = SFR('U1CSR')
	U1CSR.MODE
	WDCTL = SFR('WDCTL')
	WDCTL.INT
	WDCTL.CLR
	WDCTL.CLR = 3
