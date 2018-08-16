#
# isa_8051.py
#
# this is the instruction-set definition for 8051
# (actually 8052)
# shared by cc2540, nrf24e1, etc.
#
from isa import ISA
class ISA8051(ISA):
	'''
		this is the data structure for generating code (assembly or machine)
		for 8051.  It is a "factory".  we define these formatting strings
		and formatting functions as either constant list or lambda to a
		list of expressions.  One can do code-gen and pattern match - but
		they should match exactly...  This also means we can't really do
		labels, but probably that could be solved later?
	'''
	_isa_name = "8051"
	_instr = {
			'NOP':             [0x00],
			'ACALL 0x%x':      lambda x:    [0x11+((x>>3)&0xe0), x & 0xff],
			'AJMP 0x%x':       lambda x:    [0x01+((x>>3)&0xe0), x & 0xff],
			'LJMP 0x%x':       lambda x:    [0x02, (x >> 8) & 0xff, x & 0xff],
			'RR A':            [0x03],
			'INC A':           [0x04],
			'INC 0x%x':        lambda x:    [0x05, x],
			'INC @R%d':        lambda x:    [0x06 + x],
			'INC R%d':         lambda x:    [0x08 + x],
			'JBC 0x%x, 0x%x':  lambda x, y: [0x10, x, y & 0xff],
			'LCALL 0x%x':      lambda x:    [0x12, ((x>>8) & 0xff), (x & 0xff)],
			'RRC A':                        [0x13],        # RRC A
			'DEC A':                        [0x14],        # DEC A
			'DEC 0x%x':        lambda x:    [0x15, x],     # DEC iram
			'DEC @R%d':        lambda x:    [0x16 + x],    # DEC @R[01]
			'DEC @R0':                      [0x16],        # DEC @R0
			'DEC @R1':                      [0x17],        # DEC @R1
			'DEC R%d':         lambda x:    [0x18 + x],    # DEC R[0-7]
			'JB 0x%x, 0x%x':   lambda x, y: [0x20, x, y],  # JB bitAddr, codeAddr
			'RET':                          [0x22],        # RET
			'RL A':                         [0x23],        # RL A
			'ADD A, #0x%x':    lambda x:    [0x24, x],     # ADD A, #data
			'ADD A, 0x%x':     lambda x:    [0x25, x],     # ADD A, iram
			'ADD A, DPL':                   [0x25, 0x82],  # ADD A, DPL=0x82
			'ADD A, DPH':                   [0x25, 0x83],  # ADD A, DPL=0x83
			'ADD A, @R%d':     lambda x:    [0x26 + x],    # ADD A, @R[01]
			'ADD A, @R0':                   [0x26],        # ADD A, @R0
			'ADD A, @R1':                   [0x27],        # ADD A, @R1
			'ADD A, R%d':      lambda x:    [0x28 + x],    # ADD A, R[0-7]
			'JNB 0x%x, 0x%x':  lambda x, y: [0x30, x, y],  # JNB bitAddr, codeAddr
			'JNB ACC.%d, 0x%x':lambda x, y: [0x30, 0xE0+x, y],  # JNB ACC.bit, codeAddr
			'RETI':                         [0x32],        # RETI
			'RLC A':                        [0x33],        # RLC A
			'ADDC A, #0x%x':   lambda x:    [0x34, x],     # ADDC A, #data
			'ADDC A, 0x%x':    lambda x:    [0x35, x],     # ADDC A, data
			'ADDC A, @R%d':    lambda x:    [0x36 + x],    # ADDC A, @R[01]
			'ADDC A, @R0':                  [0x36],        # ADDC A, @R0
			'ADDC A, @R1':                  [0x37],        # ADDC A, @R1
			'ADDC A, R%d':     lambda x:    [0x38 + x],    # ADDC A, R[0-7]
			'JC 0x%x':         lambda x:    [0x40, x],     # JC codeAddr
			'ORL 0x%x, A':     lambda x:    [0x42, x],     # ORL dataAddr, A
			'ORL 0x%x, #0x%x': lambda x, y: [0x43, x, y],  # ORL dataAddr, #data
			'ORL A, #0x%x':    lambda x:    [0x44, x],     # ORL A, #data
			'ORL A, 0x%x':     lambda x:    [0x45, x],     # ORL A, dataAddr
			'ORL A, @R%d':     lambda x:    [0x46 + x],    # ORL A, @R[01]
			'ORL A, @R0':                   [0x46],        # ORL A, @R0
			'ORL A, @R1':                   [0x47],        # ORL A, @R1
			'ORL A, R%d':      lambda x:    [0x48 + x],    # ORL A, R[0-7]
			'JNC 0x%x':        lambda x:    [0x50, x],     # JNC codeAddr
			'ANL 0x%x, A':     lambda x:    [0x52, x],     # ANL dataAddr, A
			'ANL 0x%x, #0x%x': lambda x, y: [0x53, x, y],  # ANL iram, #data
			'ANL A, #0x%x':    lambda x:    [0x54, x],     # ANL A, #data
			'ANL A, 0x%x':     lambda x:    [0x55, x],     # ANL A, #data
			'ANL A, @R%d':     lambda x:    [0x56 + x],    # ANL A, @R[01]
			'ANL A, @R0':                   [0x56],        # ANL A, @R0
			'ANL A, @R1':                   [0x57],        # ANL A, @R1
			'ANL A, R%d':      lambda x:    [0x58 + x],    # ANL A, R[0-7]
			'JZ 0x%x':         lambda x:    [0x60, x],     # JZ codeAddr
			'XRL 0x%x, A':     lambda x:    [0x62, x],     # XRL iram, A
			'XRL 0x%x, #0x%x': lambda x, y: [0x63, x, y],  # XRL iram, #data
			'XRL A, #0x%x':    lambda x:    [0x64, x],     # XRL A, #data
			'XRL A, 0x%x':     lambda x:    [0x65, x],     # XRL A, iram
			'XRL A, @R%d':     lambda x:    [0x66 + x],    # XRL A, @R[01]
			'XRL A, @R0':                   [0x66],        # XRL A, @R0
			'XRL A, @R1':                   [0x67],        # XRL A, @R1
			'XRL A, R%d':      lambda x:    [0x68 + x],    # XRL A, R[0-7]
			'JNZ 0x%x':        lambda x:    [0x70, x],     # JNZ codeAddr
			'ORL C, 0x%x':     lambda x:    [0x72, x],     # ORL C, bitAddr
			'JMP @A+DPTR':                  [0x73],        # JMP @A+DPTR
			'MOV A, #0x%x':    lambda x:    [0x74, x],     # MOV A, #data
			'MOV 0x%x, #0x%x': lambda x, y: [0x75, x, y],  # MOV iram, #data
			'MOV B, #0x%x':    lambda y:    [0x75, 0xF0, y],  # MOV B=0xF0, #data
			'MOV DPL, #0x%x':  lambda y:    [0x75, 0x82, y],  # MOV DPL=0x82, #data
			'MOV DPH, #0x%x':  lambda y:    [0x75, 0x83, y],  # MOV DPL=0x83, #data
			'MOV @R%d, #0x%x': lambda x, y: [0x76 + x, y], # MOV @R[01], #data
			'MOV @R0, #0x%x':  lambda x:    [0x76, x],     # MOV @R0, #data
			'MOV @R1, #0x%x':  lambda x:    [0x77, x],     # MOV @R1, #data
			'MOV R%d, #0x%x':  lambda x, y: [0x78+ x, y],  # MOV R[0-7], #data
			'MOV R0, #0x%x':   lambda x:    [0x78, x],     # MOV R0, #data
			'MOV R1, #0x%x':   lambda x:    [0x79, x],     # MOV R1, #data
			'MOV R2, #0x%x':   lambda x:    [0x7A, x],     # MOV R2, #data
			'MOV R3, #0x%x':   lambda x:    [0x7B, x],     # MOV R3, #data
			'MOV R4, #0x%x':   lambda x:    [0x7C, x],     # MOV R4, #data
			'MOV R5, #0x%x':   lambda x:    [0x7D, x],     # MOV R5, #data
			'MOV R6, #0x%x':   lambda x:    [0x7E, x],     # MOV R6, #data
			'MOV R7, #0x%x':   lambda x:    [0x7F, x],     # MOV R7, #data
			'SJMP 0x%x':       lambda x:    [0x80, x],     # SJMP codeAddr
			'ANL C, 0x%x':     lambda x:    [0x82, x],     # ANL C, bitAddr
			'MOVC A, @A+PC':                [0x83],        # MOVC
			'DIV AB':                       [0x84],        # DIV AB
			'MOV 0x%x, 0x%x':  lambda x, y: [0x85, y, x],  # MOV iram, iram
			'MOV 0x%x, @R%d':  lambda x, y: [0x86+y, x],   # MOV iram, @R[0-1]
			'MOV 0x%x, @R0':   lambda x:    [0x86, x],     # MOV iram, @R0
			'MOV 0x%x, @R1':   lambda x:    [0x87, x],     # MOV iram, @R1
			'MOV 0x%x, R%d':   lambda x, y: [0x88+y, x],   # MOV iram, R[0-7]
			'MOV B, R%d':      lambda y:    [0x88+y, 0xF0], # MOV B=0xF0, R[0-7]
			'MOV SP, R%d':     lambda y:    [0x88+y, 0x81], # MOV iram, R[0-7]
			'MOV SP, R0':                   [0x88, 0x81],  # MOV iram, R[0-7]
			'MOV DPTR, #0x%x': lambda x:    [0x90, (x>>8)&0xff, x&0xff ],
			'MOV 0x%x, C':     lambda x:    [0x92, x],     # MOV bit, C
			'MOV ACC.%d, C':   lambda x:    [0x92, 0xE0+x], # MOV ACC.bit, C
			'MOV B.%d, C':     lambda x:    [0x92, 0xF0+x], # MOV B.bit, C
			'MOVC A, @A+DPTR':              [0x93],        # MOVC A, @A+DPTR
			'SUBB A, #0x%x':   lambda x:    [0x94, x],     # SUBB A, #data
			'SUBB A, 0x%x':    lambda x:    [0x95, x],     # SUBB A, iram
			'SUBB A, @R%d':    lambda x:    [0x96 + x],    # SUBB A, @R[01]
			'SUBB A, @R0':                  [0x96],        # SUBB A, @R0
			'SUBB A, @R1':                  [0x97],        # SUBB A, @R1
			'SUBB A, R%d':     lambda x:    [0x98 + x],    # SUBB A, R[0-7]
			'ORL C, 0x%x':     lambda x:    [0xA0, x],     # ORL C, bitAddr
			'MOV C, 0x%x':     lambda x:    [0xA2, x],     # MOV C, bitAddr
			'MOV C, ACC.%d':   lambda x:    [0xA2, 0xe0+x], # MOV C, ACC.bit
			'INC DPTR':                     [0xA3],        # INC DPTR
			'MUL AB':                       [0xA4],        # MUL AB
			# opcode 0xA5 is reserved
			'MOV @R%d, 0x%x':  lambda x, y: [0xA6+x, y],   # MOV @R[01], iram
			'MOV @R0, 0x%x':   lambda x:    [0xA6, x],     # MOV @R0, iram
			'MOV @R1, 0x%x':   lambda x:    [0xA7, x],     # MOV @R1, iram
			'MOV R%d, 0x%x':   lambda x, y: [0xA8+x, y],   # MOV R[0-7], iram
			'MOV R%d, B':      lambda x:    [0xA8+x, 0xF0],# MOV R[0-7], B=0xF0
			'MOV R%d, SP':     lambda x:    [0xA8+x, 0x81],# MOV R[0-7], SP
			'ANL C, 0x%x':     lambda x:    [0xB0, x],     # ANL C, bitAddr
			'CPL 0x%x':        lambda x:    [0xB2, x],     # CPL bitAddr
			'CPL C':                        [0xB3],        # CPL C
			'CJNE A, #0x%x, 0x%x': lambda x, y: [0xB4, x, y], # CJNE A, #data, code
			'CJNE A, 0x%x, 0x%x': lambda x, y: [0xB5, x, y], # CJNE A, iram, code
			'CJNE @R%d, #0x%x, 0x%x': lambda x, y, z: [0xB6+x, y, z], # CJNE @R[01], #data, code
			'CJNE @R0, #0x%x, 0x%x': lambda y, z: [0xB6, y, z], # CJNE @R0, #data, code
			'CJNE @R1, #0x%x, 0x%x': lambda y, z: [0xB7, y, z], # CJNE @R1, #data, code
			'CJNE R%d, #0x%x, 0x%x': lambda x, y, z: [0xB8+x, y, z], # CJNE R[0-7], #data, code
			'PUSH 0x%x':       lambda x:    [0xC0, x],     # PUSH iram
			'PUSH ACC':                     [0xC0, 0xE0],  # PUSH accumulator
			'PUSH B':                       [0xC0, 0xF0],  # PUSH B register
			'PUSH DPL':                     [0xC0, 0x82],  # PUSH DPL
			'PUSH DPH':                     [0xC0, 0x83],  # PUSH DPH
			'PUSH PSW':                     [0xC0, 0xD0],  # PUSH PSW (for CY)
			'CLR 0x%x':        lambda x:    [0xC2, x],     # CLR bitAddr
			'CLR C':                        [0xC3],        # CLR C
			'SWAP A':                       [0xC4],        # SWAP A
			'XCH A, 0x%x':     lambda x:    [0xC5, x],     # XCH A, iram
			'XCH A, DPL':                   [0xC5, 0x82],  # XCH A, DPL=0x82
			'XCH A, DPH':                   [0xC5, 0x83],  # XCH A, DPH=0x83
			'XCH A, @R%d':     lambda x:    [0xC6 + x],    # XCH A, @R[01]
			'XCH A, @R0':                   [0xC6],        # XCH A, @R0
			'XCH A, @R1':                   [0xC7],        # XCH A, @R1
			'XCH A, R%d':      lambda x:    [0xC8 + x],    # XCH A, R[0-7]
			'POP 0x%x':        lambda x:    [0xD0, x],     # POP iram
			'POP DPL':                      [0xD0, 0x82],  # POP DPL=0x82
			'POP DPH':                      [0xD0, 0x83],  # POP DPL=0x83
			'POP ACC':                      [0xD0, 0xE0],  # POP to accumulator
			'POP B':                        [0xD0, 0xF0],  # POP to B register
			'SETB 0x%x':       lambda x:    [0xD2, x],     # SETB bitAddr
			'SETB C':                       [0xD3],        # SETB C
			'DA A':                         [0xD4],        # DA A
			'DJNZ 0x%x, 0x%x': lambda x, y: [0xD5, x, y],  # DJNZ iram, code
			'XCHD A, @R%d':    lambda x:    [0xD6+x],      # XCHD A, @R[01]
			'XCHD A, @R0':                  [0xD6],        # XCHD A, @R0
			'XCHD A, @R1':                  [0xD7],        # XCHD A, @R1
			'DJNZ R%d, 0x%x':  lambda x, y: [0xD8+x, y],   # DJNZ R[0-7], code
			'MOVX A, @DPTR':                [0xE0],
			'MOVX A, @R%d':    lambda x:    [0xE2 + x],    # MOVX A, @R[01]
			'MOVX A, @R0':                  [0xE2],        # MOVX A, @R0
			'MOVX A, @R1':                  [0xE3],        # MOVX A, @R1
			'CLR A':                        [0xE4],        # CLR A
			'MOV A, 0x%x':     lambda x:    [0xE5, x],     # MOV A, iram
			'MOV A, B':                     [0xE5, 0xF0],  # MOV A, B=0xF0
			'MOV A, DPL':                   [0xE5, 0x82],  # MOV A, DPL=0x82
			'MOV A, DPH':                   [0xE5, 0x83],  # MOV A, DPL=0x83
			'MOV A, @R%d':     lambda x:    [0xE6 + x],    # MOV A, @R[01]
			'MOV A, @R0':                   [0xE6],        # MOV A, @R0
			'MOV A, @R1':                   [0xE7],        # MOV A, @R1
			'MOV A, R%d':      lambda x:    [0xE8 + x],    # MOV A, R[0-7]
			'MOV A, R0':                    [0xE8],        # MOV A, R0
			'MOV A, R1':                    [0xE9],        # MOV A, R1
			'MOV A, R2':                    [0xEA],        # MOV A, R2
			'MOV A, R3':                    [0xEB],        # MOV A, R3
			'MOV A, R4':                    [0xEC],        # MOV A, R4
			'MOV A, R5':                    [0xED],        # MOV A, R5
			'MOV A, R6':                    [0xEE],        # MOV A, R6
			'MOV A, R7':                    [0xEF],        # MOV A, R7
			'MOVX @DPTR, A':                [0xF0],
			'MOVX @R%d, A':    lambda x:    [0xF2 + x],    # MOVX @R[01], A
			'MOVX @R0, A':                  [0xF2],        # MOVX @R0, A
			'MOVX @R1, A':                  [0xF3],        # MOVX @R1, A
			'CPL A':                        [0xF4],
			'MOV 0x%x, A':     lambda x:    [0xF5, x],     # MOV iram, A
			'MOV DPL, A':                   [0xF5, 0x82],  # MOV DPL=0x82, A
			'MOV DPH, A':                   [0xF5, 0x83],  # MOV DPL=0x83, A
			'MOV B, A':                     [0xF5, 0xF0],  # MOV B=0xF0, A
			'MOV @R%d, A':     lambda x:    [0xF6 + x],    # MOV @R[01], A
			'MOV @R0, A':                   [0xF6],        # MOV @R0, A
			'MOV @R1, A':                   [0xF7],        # MOV @R1, A
			'MOV R%d, A':      lambda x:    [0xf8 + x],    # MOV R[0-7], A
			'MOV R0, A':                    [0xf8],        # MOV R0, A
			'MOV R1, A':                    [0xf9],        # MOV R1, A
			'MOV R2, A':                    [0xfA],        # MOV R2, A
			'MOV R3, A':                    [0xfB],        # MOV R3, A
			'MOV R4, A':                    [0xfC],        # MOV R4, A
			'MOV R5, A':                    [0xfD],        # MOV R5, A
			'MOV R6, A':                    [0xfE],        # MOV R6, A
			'MOV R7, A':                    [0xfF],        # MOV R7, A
	}
	# the __init__ and all other methods are all inherited

	disasm = {
		0x00: (1,                 'NOP'),
		0x01: (2, lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x02: (3, lambda x, y, z: 'LJMP 0x%x' % (((y & 0xff) << 8) + (z & 0xff))),
		0x03: (1,                  'RR A'),
		0x04: (1,                  'INC A'),
		0x05: (2, lambda x, y:     'INC 0x%x' % y),
		0x06: (1,                  'INC @R0'),
		0x07: (1,                  'INC @R1'),
		0x08: (1,                  'INC R0'),
		0x09: (1,                  'INC R1'),
		0x0a: (1,                  'INC R2'),
		0x0b: (1,                  'INC R3'),
		0x0c: (1,                  'INC R4'),
		0x0d: (1,                  'INC R5'),
		0x0e: (1,                  'INC R6'),
		0x0f: (1,                  'INC R7'),
		0x10: (3,  lambda x, y, z: 'JBC 0x%x, 0x%x' %  (y, z)),
		0x11: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x12: (3,  lambda x, y, z: 'LCALL 0x%x' % (((y & 0xff) << 8) + (x & 0xff))),
		0x13: (1,                  'RRC A'),
		0x14: (1,                  'DEC A'),
		0x15: (2,  lambda x, y:    'DEC 0x%x' % y),
		0x16: (1,                  'DEC @R0'),
		0x17: (1,                  'DEC @R1'),
		0x18: (1,                  'DEC R0'),
		0x19: (1,                  'DEC R1'),
		0x1a: (1,                  'DEC R2'),
		0x1b: (1,                  'DEC R3'),
		0x1c: (1,                  'DEC R4'),
		0x1d: (1,                  'DEC R5'),
		0x1e: (1,                  'DEC R6'),
		0x1f: (1,                  'DEC R7'),
		0x20: (3,  lambda x, y, z: 'JB 0x%x, 0x%x' % (((y & 0xff) << 8) + (z & 0xff))),
		0x21: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x22: (1,                  'RET'),
		0x23: (1,                  'RL A'),
		0x24: (2,  lambda x, y:    'ADD A, #0x%x' % y),
		0x25: (2,  lambda x, y:    'ADD A, 0x%x' % y),
		0x26: (1,                  'ADD A, @R0'),
		0x27: (1,                  'ADD A, @R1'),
		0x28: (1,                  'ADD A, R0'),
		0x29: (1,                  'ADD A, R1'),
		0x2a: (1,                  'ADD A, R2'),
		0x2b: (1,                  'ADD A, R3'),
		0x2c: (1,                  'ADD A, R4'),
		0x2d: (1,                  'ADD A, R5'),
		0x2e: (1,                  'ADD A, R6'),
		0x2f: (1,                  'ADD A, R7'),
		0x30: (3,  lambda x, y, z: 'JNB 0x%x, 0x%x' % (y, z)),
		0x31: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x32: (1,                  'RETI'),
		0x33: (1,                  'RLC A'),
		0x34: (2,  lambda x, y:    'ADDC A, #0x%x' % y),
		0x35: (2,  lambda x, y:    'ADDC A, 0x%x' % y),
		0x36: (1,                  'ADDC A, @R0'),
		0x37: (1,                  'ADDC A, @R1'),
		0x38: (1,                  'ADDC A, R0'),
		0x39: (1,                  'ADDC A, R1'),
		0x3a: (1,                  'ADDC A, R2'),
		0x3b: (1,                  'ADDC A, R3'),
		0x3c: (1,                  'ADDC A, R4'),
		0x3d: (1,                  'ADDC A, R5'),
		0x3e: (1,                  'ADDC A, R6'),
		0x3f: (1,                  'ADDC A, R7'),
		0x40: (2,  lambda x, y:    'JC 0x%x' % y),

		0x41: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x42: (2,  lambda x, y:    'ORL 0x%x, A' % y),
		0x43: (3,  lambda x, y, z: 'ORL 0x%x, #0x%x' % (y, z)),
		0x44: (2,  lambda x, y:    'ORL A, #0x%x' % y),
		0x45: (2,  lambda x, y:    'ORL A, 0x%x' % y),
		0x46: (1,                  'ORL A, @R0'),
		0x47: (1,                  'ORL A, @R1'),
		0x48: (1,                  'ORL A, R0'),
		0x49: (1,                  'ORL A, R1'),
		0x4a: (1,                  'ORL A, R2'),
		0x4b: (1,                  'ORL A, R3'),
		0x4c: (1,                  'ORL A, R4'),
		0x4d: (1,                  'ORL A, R5'),
		0x4e: (1,                  'ORL A, R6'),
		0x4f: (1,                  'ORL A, R7'),
		0x50: (2,  lambda x, y:    'JNC 0x%x' % y),
		0x51: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x52: (2,  lambda x, y:    'ANL 0x%x, A' % y),
		0x53: (3,  lambda x, y, z: 'ANL 0x%x, #0x%x' % (y, z)),
		0x54: (2,  lambda x, y:    'ANL A, #0x%x' % y),
		0x55: (2,  lambda x, y:    'ANL A, 0x%x' % y),
		0x56: (1,                  'ANL A, @R0'),
		0x57: (1,                  'ANL A, @R1'),
		0x58: (1,                  'ANL A, R0'),
		0x59: (1,                  'ANL A, R1'),
		0x5a: (1,                  'ANL A, R2'),
		0x5b: (1,                  'ANL A, R3'),
		0x5c: (1,                  'ANL A, R4'),
		0x5d: (1,                  'ANL A, R5'),
		0x5e: (1,                  'ANL A, R6'),
		0x5f: (1,                  'ANL A, R7'),
		0x60: (1,  lambda x, y:    'JZ 0x%x' % y),
		0x61: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x62: (2,  lambda x, y:    'XRL 0x%x, A' % y),
		0x63: (3,  lambda x, y, z: 'XRL 0x%x, #0x%x' % (y, z)),
		0x64: (2,  lambda x, y:    'XRL A, #0x%x' % y),
		0x65: (2,  lambda x, y:    'XRL A, 0x%x' % y),
		0x66: (1,                  'XRL A, @R0'),
		0x67: (1,                  'XRL A, @R1'),
		0x68: (1,                  'XRL A, R0'),
		0x69: (1,                  'XRL A, R1'),
		0x6a: (1,                  'XRL A, R2'),
		0x6b: (1,                  'XRL A, R3'),
		0x6c: (1,                  'XRL A, R4'),
		0x6d: (1,                  'XRL A, R5'),
		0x6e: (1,                  'XRL A, R6'),
		0x6f: (1,                  'XRL A, R7'),
		0x70: (2,  lambda x, y:    'JNZ 0x%x' % y),
		0x71: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x72: (2,  lambda x, y:    'ORL C, 0x%x' % y),
		0x73: (1,                  'JMP @A+DPTR'),
		0x74: (2,  lambda x, y:    'MOV A, #0x%x' % y),
		0x75: (3,  lambda x, y, z: 'MOV 0x%x, #0x%x' % (y, z)),
		0x76: (2,  lambda x, y:    'MOV @R0, #0x%x' % y),
		0x77: (2,  lambda x, y:    'MOV @R1, #0x%x' % y),
		0x78: (2,  lambda x, y:    'MOV R0, #0x%x' % y),
		0x79: (2,  lambda x, y:    'MOV R1, #0x%x' % y),
		0x7a: (2,  lambda x, y:    'MOV R2, #0x%x' % y),
		0x7b: (2,  lambda x, y:    'MOV R3, #0x%x' % y),
		0x7c: (2,  lambda x, y:    'MOV R4, #0x%x' % y),
		0x7d: (2,  lambda x, y:    'MOV R5, #0x%x' % y),
		0x7e: (2,  lambda x, y:    'MOV R6, #0x%x' % y),
		0x7f: (2,  lambda x, y:    'MOV R7, #0x%x' % y),
		0x80: (2,  lambda x, y:    'SJMP 0x%x' % y),
		0x81: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x82: (2,  lambda x, y:    'ANL C, 0x%x' % y),
		0x83: (1,                  'MOVC A, @A+PC'),
		0x84: (1,                  'DIV AB'),
		0x85: (3,  lambda x, y, z: 'MOV 0x%x, 0x%x' % (y, z)),
		0x86: (2,  lambda x, y:    'MOV 0x%x, @R0' % y),
		0x87: (2,  lambda x, y:    'MOV 0x%x, @R1' % y),
		0x88: (2,  lambda x, y:    'MOV 0x%x, R0' % y),
		0x89: (2,  lambda x, y:    'MOV 0x%x, R1' % y),
		0x8a: (2,  lambda x, y:    'MOV 0x%x, R2' % y),
		0x8b: (2,  lambda x, y:    'MOV 0x%x, R3' % y),
		0x8c: (2,  lambda x, y:    'MOV 0x%x, R4' % y),
		0x8d: (2,  lambda x, y:    'MOV 0x%x, R5' % y),
		0x8e: (2,  lambda x, y:    'MOV 0x%x, R6' % y),
		0x8f: (2,  lambda x, y:    'MOV 0x%x, R7' % y),
		0x90: (3,  lambda x, y, z: 'MOV DPTR, #0x%x' % (((y & 0xff) << 8) + (z & 0xff))),
		0x91: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0x92: (2,  lambda x, y:    'MOV 0x%x, C' % y),
		0x93: (1,                  'MOVC A, @A+DPTR'),
		0x94: (2,  lambda x, y:    'SUBB A, #0x%x' % y),
		0x95: (2,  lambda x, y:    'SUBB A, 0x%x' % y),
		0x96: (1,                  'SUBB A, @R0'),
		0x97: (1,                  'SUBB A, @R1'),
		0x98: (1,                  'SUBB A, R0'),
		0x99: (1,                  'SUBB A, R1'),
		0x9a: (1,                  'SUBB A, R2'),
		0x9b: (1,                  'SUBB A, R3'),
		0x9c: (1,                  'SUBB A, R4'),
		0x9d: (1,                  'SUBB A, R5'),
		0x9e: (1,                  'SUBB A, R6'),
		0x9f: (1,                  'SUBB A, R7'),
		0xa0: (1,  lambda x, y:    'ORL C, 0x%x' % y),
		0xa1: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0xa2: (2,  lambda x, y:    'MOV C, 0x%x' % y),
		0xa3: (1,                  'INC DPTR'),
		0xa4: (1,                  'MUL AB'),
		0xa5: (1,                  'reserved'),
		0xa6: (2,  lambda x, y:    'MOV @R0, 0x%x' % y),
		0xa7: (2,  lambda x, y:    'MOV @R1, 0x%x' % y),
		0xa8: (2,  lambda x, y:    'MOV R0, 0x%x' % y),
		0xa9: (2,  lambda x, y:    'MOV R1, 0x%x' % y),
		0xaa: (2,  lambda x, y:    'MOV R2, 0x%x' % y),
		0xab: (2,  lambda x, y:    'MOV R3, 0x%x' % y),
		0xac: (2,  lambda x, y:    'MOV R4, 0x%x' % y),
		0xad: (2,  lambda x, y:    'MOV R5, 0x%x' % y),
		0xae: (2,  lambda x, y:    'MOV R6, 0x%x' % y),
		0xaf: (2,  lambda x, y:    'MOV R7, 0x%x' % y),
		0xb0: (2,  lambda x, y:    'ANL C, 0x%x' % y),
		0xb1: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0xb2: (2,  lambda x, y:    'CPL 0x%x' % y),
		0xb3: (1,                  'CPL C'),
		0xb4: (3,  lambda x, y, z: 'CJNE A, #0x%x, 0x%x' % (y, z)),
		0xb5: (3,  lambda x, y, z: 'CJNE A, 0x%x, 0x%x' % (y, z)),
		0xb6: (3,  lambda x, y, z: 'CJNE @R0, #0x%x, 0x%x' % (y, z)),
		0xb7: (3,  lambda x, y, z: 'CJNE @R1, #0x%x, 0x%x' % (y, z)),
		0xb8: (3,  lambda x, y, z: 'CJNE R0, #0x%x, 0x%x' % (y, z)),
		0xb9: (3,  lambda x, y, z: 'CJNE R1, #0x%x, 0x%x' % (y, z)),
		0xba: (3,  lambda x, y, z: 'CJNE R2, #0x%x, 0x%x' % (y, z)),
		0xbb: (3,  lambda x, y, z: 'CJNE R3, #0x%x, 0x%x' % (y, z)),
		0xbc: (3,  lambda x, y, z: 'CJNE R4, #0x%x, 0x%x' % (y, z)),
		0xbd: (3,  lambda x, y, z: 'CJNE R5, #0x%x, 0x%x' % (y, z)),
		0xbe: (3,  lambda x, y, z: 'CJNE R6, #0x%x, 0x%x' % (y, z)),
		0xbf: (3,  lambda x, y, z: 'CJNE R7, #0x%x, 0x%x' % (y, z)),
		0xc0: (2,  lambda x, y:    'PUSH 0x%x' % y),
		0xc1: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0xc2: (2,  lambda x, y:    'CLR 0x%x' % y),
		0xc3: (1,                  'CLR C'),
		0xc4: (1,                  'SWAP A'),
		0xc5: (2,  lambda x, y:    'XCH A, 0x%x' % y),
		0xc6: (1,                  'XCH A, @R0'),
		0xc7: (1,                  'XCH A, @R1'),
		0xc8: (1,                  'XCH A, R0'),
		0xc9: (1,                  'XCH A, R1'),
		0xca: (1,                  'XCH A, R2'),
		0xcb: (1,                  'XCH A, R3'),
		0xcc: (1,                  'XCH A, R4'),
		0xcd: (1,                  'XCH A, R5'),
		0xce: (1,                  'XCH A, R6'),
		0xcf: (1,                  'XCH A, R7'),
		0xd0: (2,  lambda x, y:    'POP 0x%x' % y),
		0xd1: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0xd2: (2,  lambda x, y:    'SETB 0x%x' % y),
		0xd3: (1,                  'SETB C'),
		0xd4: (1,                  'DA A'),
		0xd5: (3,  lambda x, y, z: 'DJNZ 0x%x, 0x%x' % (y, z)),
		0xd6: (1,                  'XCHD A, @R0'),
		0xd7: (1,                  'XCHD A, @R1'),
		0xd8: (2,  lambda x, y:    'DJNZ R0, 0x%x' % y),
		0xd9: (2,  lambda x, y:    'DJNZ R1, 0x%x' % y),
		0xda: (2,  lambda x, y:    'DJNZ R2, 0x%x' % y),
		0xdb: (2,  lambda x, y:    'DJNZ R3, 0x%x' % y),
		0xdc: (2,  lambda x, y:    'DJNZ R4, 0x%x' % y),
		0xdd: (2,  lambda x, y:    'DJNZ R5, 0x%x' % y),
		0xde: (2,  lambda x, y:    'DJNZ R6, 0x%x' % y),
		0xdf: (2,  lambda x, y:    'DJNZ R7, 0x%x' % y),
		0xe0: (1,                  'MOVX A, @DPTR'),
		0xe1: (2,  lambda x, y:    'AJMP 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0xe2: (1,                  'MOVX A, @R0'),
		0xe3: (1,                  'MOVX A, @R1'),
		0xe4: (1,                  'CLR A'),
		0xe5: (2,  lambda x, y:    'MOV A, 0x%x' % y),
		0xe6: (1,                  'MOV A, @R0'),
		0xe7: (1,                  'MOV A, @R1'),
		0xe8: (1,                  'MOV A, R0'),
		0xe9: (1,                  'MOV A, R1'),
		0xea: (1,                  'MOV A, R2'),
		0xeb: (1,                  'MOV A, R3'),
		0xec: (1,                  'MOV A, R4'),
		0xed: (1,                  'MOV A, R5'),
		0xee: (1,                  'MOV A, R6'),
		0xef: (1,                  'MOV A, R7'),
		0xf0: (1,                  'MOVX @DPTR, A'),
		0xf1: (2,  lambda x, y:    'ACALL 0x%x' % (((x & 0xe0) << 3) + (y & 0xff))),
		0xf2: (1,                  'MOVX @R0, A'),
		0xf3: (1,                  'MOVX @R1, A'),
		0xf4: (1,                  'CPL A'),
		0xf5: (2,  lambda x, y:    'MOV 0x%x, A' % y),
		0xf6: (1,                  'MOV @R0, A'),
		0xf7: (1,                  'MOV @R1, A'),
		0xf8: (1,                  'MOV R0, A'),
		0xf9: (1,                  'MOV R1, A'),
		0xfa: (1,                  'MOV R2, A'),
		0xfb: (1,                  'MOV R3, A'),
		0xfc: (1,                  'MOV R4, A'),
		0xfd: (1,                  'MOV R5, A'),
		0xfe: (1,                  'MOV R6, A'),
		0xff: (1,                  'MOV R7, A'),
	}

def disasm(array):
	out = [ ]
	while array:
		(length, defn) = ISA8051.disasm[array[0]]
		if not isinstance(defn, str): # it's a lambda
			defn = apply(defn, tuple(array[:length]))
		out.append(defn)
		del array[:length]
	return str(out)
		
