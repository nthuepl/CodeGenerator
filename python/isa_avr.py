#
# isa_avr.py
#
# this is the instruction-set definition for AVR
# based on http://www.atmel.com/images/doc0856.pdf
#
from isa import ISA
class ISAAVR(ISA):
	'''
		this is the data structure for generating code (assembly or machine)
		for AVR.
	'''
	_isa_name = "AVR"
	_instr = {
			'ADD R%d, R%d':    lambda Rd, Rr: 
												[ 0x0C00 + ((Rr&0x10)<<5) + ((Rd & 0x1f)<< 4)
															+ (Rr & 0xf)],
			'ADC R%d, R%d':    lambda Rd, Rr:
												[ 0x1C00 + ((Rr&0x10)<<5) + ((Rd & 0x1f)<< 4)
															+ (Rr & 0xf)],
			'ADIW R%d, 0x%x':  lambda Rd, K:  [ 0x9600 + ((K & 0x30) << 2) + 
													{ 24: 0, 26: 0x10, 28: 0x20, 30: 0x30}[Rd] +
													(K & 0xf)],
			'ADIW R25:24, 0x%x':  lambda K:  [ 0x9600 + ((K & 0x30) << 2) + 
																		(K & 0xf)],
			'ADIW R27:26, 0x%x':  lambda K:  [ 0x9610 + ((K & 0x30) << 2) + 
																		(K & 0xf)],
			'ADIW R29:28, 0x%x':  lambda K:  [ 0x9620 + ((K & 0x30) << 2) + 
																		(K & 0xf)],
			'ADIW R31:30, 0x%x':  lambda K:  [ 0x9630 + ((K & 0x30) << 2) + 
																		(K & 0xf)],
			'SUB R%d, R%d':    lambda Rd, Rr: [ 0x1800 + ((Rr & 0x10) << 5)
													+ ((Rd & 0x1f) << 4) + (Rr & 0xf) ],
			'SUBI R%d, 0x%x':  lambda Rd, K:  [ 0x5000 + ((K & 0xf0) << 4) +
				((Rd & 0xf) << 4) + (K & 0xf) ],
			'SBC R%d, R%d':    lambda Rd, Rr: [ 0x0800 + ((Rr & 0x10) << 5)
				+ ((Rd & 0x1f) << 4) + (Rr & 0xf)  ],
			'SBCI R%d, 0x%x':  lambda Rd, K:  [ 0x4000 + ((K & 0xF0) << 4) +
				((Rd & 0xf) << 4) + (K & 0xf) ],
			'SBIW R%d, 0x%x':  lambda Rd, K:  [ 0x9700 + ((K & 0x30) <<  2) +
						{ 24: 0, 26: 0x10, 28: 0x20, 30: 0x30}[Rd] + (K & 0xf) ],
			'SBIW R25:24, 0x%x':  lambda K:  [ 0x9700 + ((K & 0x30) <<  2) +
						(K & 0xf) ],
			'AND R%d, R%d':    lambda Rd, Rr: [ 0x2000 + ((Rr&0x10)<<5) +
										((Rd&0x1f)<<4) + (Rr & 0xf) ],
			'AND R24, R%d':    lambda Rr: [ 0x2000 + ((Rr&0x10)<<5) +
										((24&0x1f)<<4) + (Rr & 0xf) ],
			'ANDI R%d, 0x%x':   lambda Rd, K:  [ 0x7000 + ((K & 0xf0)<<4) +
										((Rd & 0xf) << 4) + (K & 0xf)],
			'OR R%d, R%d':     lambda Rd, Rr: [ 0x2800 + ((Rr & 0x10) << 5)
											+ ((Rd & 0x1f) << 4)  + (Rr & 0xf) ],
			'ORI R%d, 0x%x':   lambda Rd, K:  [ 0x6000 + ((K & 0xf0) << 4) +
											((Rd & 0xf) << 4) + (K & 0xf) ],
			'EOR R%d, R%d':    lambda Rd, Rr: [ 0x2400 & ((Rr & 0x1f) << 5)
					+ ((Rd & 0x1f) << 4) + (Rr & 0xf) ],
			'COM R%d':         lambda Rd:     [ 0x9400 + ((Rd & 0x1f) << 4)],
			'NEG R%d':         lambda Rd:     [ 0x9401 + ((Rd & 0x1f) << 4) ],
			'SBR R%d, 0x%x':   lambda Rd, K:  [ 0x6000 + ((K & 0xf0) << 4) +
					((Rd & 0xf) << 4) + (K & 0xf) ],
			'CBR R%d, 0x%x':   lambda Rd, K:  [ 0x7000 + (((~K) & 0xf0)<<4) +
										((Rd & 0xf) << 4) + ((~K) & 0xf)],
			'INC R%d':         lambda Rd:     [ 0x9403 + ((Rd & 0x1f) << 4) ],
			'DEC R%d':         lambda Rd:     [ 0x940A + ((Rd&0x1f)<<4) ],
			'TST R%d':         lambda Rd:     [ 0x2000 + ((Rd&0x1f)<<5) +
					(Rd& 0x1f) ],
			'CLR R%d':         lambda Rd:     [ 0x2400 + ((Rd&0x1f)<<5) +
					(Rd & 0x1f)],
			'CLR R27':         [ 0x2400 + (27 << 5) + 27 ], # X high byte
			'SER R%d':         lambda Rd:     [ 0xEF0F + ((Rd&0xf) << 4) ],
			'MUL R%d, R%d':    lambda Rd, Rr: [ 0x9C00 + ((Rr & 0x10) << 5)
					+ ((Rd & 0x1f) << 4) + (Rr & 0xf) ],
			'MULS R%d, R%d':   lambda Rd, Rr: [ 0x0200 + ((Rd & 0xf) << 4) +
					(Rr & 0xf) ],
			'MULSU R%d, R%d':  lambda Rd, Rr: [ 0x0300 + ((Rd & 0x7)<< 4) +
					(Rr & 0x7) ],
			'FMUL R%d, R%d':   lambda Rd, Rr: [ 0x0308 + ((Rd&0x7) << 4) +
					(Rr&0x7)],
			'FMULS R%d, R%d':  lambda Rd, Rr: [ 0x0380 + ((Rd&0x7)<<4) +
					(Rr&0x7) ],
			'FMULSU R%d, R%d': lambda Rd, Rr: [ 0x0388 + ((Rd&0x7) << 4) +
					(Rr&0x7) ],
			'DES 0x%x':        lambda K: [ 0x940B + ((K & 0xf) << 4)],
			### branch
			'RJMP 0x%x':       lambda k: [ 0xC000 + (k & 0x0fff)],
			'IJMP':            [ 0x9409 ],
			'EIJMP':            [ 0x9419 ],
			'JMP 0x%x':        lambda k: [
					0x940C + ((k & 0x003E0000) >> 13) + ((k & 0x00010000) >> 16),
						(k & 0xffff) ],
			'RCALL 0x%x':      lambda k: [ 0xD000 + (k & 0x0fff) ],
			'ICALL':           [ 0x9509 ],
			'EICALL':          [ 0x9519 ],
			'CALL 0x%x':       lambda k: [ \
						0x940e + ((k & 0x003e0000) >> 13) + ((k & 0x00010000) >> 16), \
						(k & 0xffff)],
			'RET':             [ 0x9508 ],
			'RETI':            [ 0x9518 ],
			'CPSE R%d, R%d':   lambda Rd, Rr: [ 0x1000 + ((Rr&0x10)<<5) +
					((Rd&0x1f)<<4) + (Rr&0xf)],
			'CP R%d, R%d':     lambda Rd, Rr: [ 0x1400 + ((Rr&0x10)<<5) +
					((Rd&0x1f)<<4) + (Rr&0xf) ],
			'CPC R%d, R%d':    lambda Rd, Rr: [ 0x0400 + ((Rr&0x10)<<5) +
					((Rd&0x1f)<<4) + (Rr&0xf) ],
			'CPI R%d, 0x%x':   lambda Rd, K: [ 0x3000 + ((K&0xf0)<< 4) +
															((Rd&0xf)<<4) + (K&0xf)],
			'SBRC R%d, 0x%x':  lambda Rr, b: [ 0xFC00 + ((Rr & 0x1f) << 4) +
					(b & 0x7)],
			'SBRS R%d, 0x%x':  lambda Rr, b: [ 0xFE00 + ((Rr & 0x1f) << 4) +
					(b & 0x7) ],
			'SBIC 0x%x, 0x%x': lambda A, b: [ 0x9900 + ((A & 0x1f) << 3) +
					(b&0x7)],
			'SBIS 0x%x, 0x%x': lambda A, b: [ 0x9B00 + ((A & 0x1f) << 3) +
					(b&0x7)],
			'BRBS 0x%x, 0x%x': lambda s, k: [ 0xf000 + ((k&0x7f)<<3) + (s&0x7)],
			'BRBC 0x%x, 0x%x': lambda s, k: [ 0xf400 + ((k&0x7f)<<3) + (s&0x7)],
			'BREQ 0x%x':       lambda k: [ 0xf001 + ((k&0x7f)<<3) ],
			'BRNE 0x%x':       lambda k: [ 0xf401 + ((k&0x7f)<<3) ],
			'BRCS 0x%x':       lambda k: [ 0xf000 + ((k&0x7f)<<3) ],
			'BRCC 0x%x':       lambda k: [ 0xf400 + ((k&0x7f)<<3) ],
			'BRSH 0x%x':       lambda k: [ 0xf400 + ((k&0x7f)<<3) ],
			'BRLO 0x%x':       lambda k: [ 0xf000 + ((k&0x7f)<<3) ],
			'BRMI 0x%x':       lambda k: [ 0xf002 + ((k&0x7f)<<3) ],
			'BRPL 0x%x':       lambda k: [ 0xf402 + ((k&0x7f)<<3) ],
			'BRGE 0x%x':       lambda k: [ 0xf404 + ((k&0x7f)<<3) ],
			'BRLT 0x%x':       lambda k: [ 0xf004 + ((k&0x7f)<<3) ],
			'BRHS 0x%x':       lambda k: [ 0xf005 + ((k&0x7f)<<3) ],
			'BRHC 0x%x':       lambda k: [ 0xf405 + ((k&0x7f)<<3) ],
			'BRTS 0x%x':       lambda k: [ 0xf006 + ((k&0x7f)<<3) ],
			'BRTC 0x%x':       lambda k: [ 0xf406 + ((k&0x7f)<<3) ],
			'BRVS 0x%x':       lambda k: [ 0xf003 + ((k&0x7f)<<3) ],
			'BRVC 0x%x':       lambda k: [ 0xf403 + ((k&0x7f)<<3) ],
			'BRIE 0x%x':       lambda k: [ 0xf007 + ((k&0x7f)<<3) ],
			'BRID 0x%x':       lambda k: [ 0xf407 + ((k&0x7f)<<3) ],
			'MOV R%d, R%d':    lambda Rd, Rr: [ 0x2C00 + ((Rr & 0x10) << 5)
					+ ((Rd & 0x1f) << 4) + (Rr & 0xf)],
			'MOV R%d, R24':    lambda Rd: [ 0x2C00 + ((24 & 0x10) << 5)
					+ ((Rd & 0x1f) << 4) + (24 & 0xf)],
			'MOV R24, R%d':    lambda Rr: [ 0x2C00 + ((Rr & 0x10) << 5)
					+ ((24 & 0x1f) << 4) + (Rr & 0xf)],
			'MOVW R%d, R%d':   lambda Rd, Rr: [ 0x0100 + ((Rd & 0xf) << 4) +
					(Rr & 0xf) ],
			'LDI R%d, 0x%x':   lambda Rd, K: [ 0xE000 + ((K & 0xf0) << 4) +
					((Rd & 0xf) << 4) + (K & 0xf)],
			'LDI R24, 0x%x':   lambda K: [ 0xE000 + ((K & 0xf0) << 4) + 
					+ (24 << 4) + (K & 0x0f)],
			'LDI R26, 0x%x':   lambda K: [ 0xE000 + ((K & 0xf0) << 4) + 
					+ (26 << 4) + (K & 0x0f)],
			'LDI ZL, 0x%x':   lambda K: [ 0xE000 + ((K & 0xf0) << 4) + 
					+ (30 << 4) + (K & 0x0f)],
			'LDI ZH, 0x%x':   lambda K: [ 0xE000 + ((K & 0xf0) << 4) + 
					+ (31 << 4) + (K & 0x0f)],
			'LDS R%d, 0X%x':   lambda Rd, k: [ 0x9000 + ((Rd & 0x1f) << 4),
					(k & 0xffff)], # 32 bit version uses 0X
			'LDS R%d, 0x%x':   lambda Rd, k: [0xA000 + ((k & 0x70) << 4) +
					((Rd & 0xf) << 4) + (k & 0xf)], # 16-bit version uses 0x
			'LD R%d, X':       lambda Rd: [ 0x900C + ((Rd & 0x1f) << 4) ],
			'LD R%d, X+':      lambda Rd: [ 0x900D + ((Rd & 0x1f) << 4) ],
			'LD R%d, -X':      lambda Rd: [ 0x900E + ((Rd & 0x1f) << 4) ],
			'LD R%d, Y':       lambda Rd: [ 0x8008 + ((Rd & 0x1f) << 4) ],
			'LD R%d, Y+':      lambda Rd: [ 0x9009 + ((Rd & 0x1f) << 4) ],
			'LD R%d, -Y':      lambda Rd: [ 0x900A + ((Rd & 0x1f) << 4) ],
			'LDD R%d, Y+0x%x': lambda Rd, q: [ 0x8008 + ((q & 0x20) << 8) +
					((q & 0x18) << 7) + ((Rd & 0x1f) << 4) + (q & 0x7)],
			'LD R%d, Z':       lambda Rd: [ 0x8000 + ((Rd & 0x1f) << 4) ],
			'LD R%d, Z+':      lambda Rd: [ 0x9001 + ((Rd & 0x1f) << 4) ],
			'LD R%d, -Z':      lambda Rd: [ 0x9002 + ((Rd & 0x1f) << 4) ],
			'LDD R%d, Z+0x%x': lambda Rd, q: [ 0x8000 + ((q & 0x20) << 8) +
					((q & 0x18) << 7) + ((Rd & 0x1f) << 4) + (q & 0x7)],
			'STS 0X%x, R%d':   lambda k, Rr: [ 0x9200 + ((Rd&0x1f) << 4),
					(k & 0xffff) ],  # 32-bit version 
			'STS 0x%x, R%d':   lambda k, Rr: [0xA800 + ((k & 0x70) << 4),
					((Rr & 0x70) << 4) + (k & 0xf)],
			'ST X, R%d':       lambda Rr: [ 0x920C + ((Rr & 0x1f) << 4)],
			'ST X, R24':       [ 0x920C + (24 << 4)],
			'ST X+, R%d':      lambda Rr: [ 0x920D + ((Rr & 0x1f) << 4)],
			'ST -X, R%d':      lambda Rr: [ 0x920E + ((Rr & 0x1f) << 4)],
			'ST Y, R%d':       lambda Rr: [ 0x8208 + ((Rr & 0x1f) << 4)],
			'ST Y+, R%d':      lambda Rr: [ 0x9209 + ((Rr & 0x1f) << 4)],
			'ST -Y, R%d':      lambda Rr: [ 0x920A + ((Rr & 0x1f) << 4)],
			'STD Y+0x%x, R%d': lambda q, Rr: [ 0x8208 + ((q & 0x20) << 8) +
					((q & 0x18) << 7) + ((Rr & 0x1f) << 4) + (q & 0x7)],
			'ST Z, R%d':       lambda Rr: [ 0x8200 + ((Rr & 0x1f) << 4)],
			'ST Z+, R%d':      lambda Rr: [ 0x9201 + ((Rr & 0x1f) << 4)],
			'ST -Z, R%d':      lambda Rz: [ 0x9202 + ((Rr & 0x1f) << 4)],
			'STD Z+0x%x, R%d': lambda q, Rr: [ 0x8200 + ((q & 0x20) << 8) +
					((q & 0x18) << 7) + ((Rr & 0x1f) << 4) + (q & 0x7)],
			'LPM':             [ 0x95C8 ],
			'LPM R%d, Z':      lambda Rd: [ 0x9004 + ((Rd & 0x1f) << 4) ],
			'LPM R%d, Z+':     lambda Rd: [ 0x9005 + ((Rd & 0x1f) << 4) ],
			'ELPM':            [ 0x95D8 ],
			'ELPM R%d, Z':     lambda Rd: [ 0x9006 + ((Rd & 0x1f) << 4)],
			'ELPM R%d, Z+':    lambda Rd: [ 0x9007 + ((Rx & 0x1f) << 4)],
			'SPM':             [ 0x95E8 ],
			'SPM Z+':          [ 0x95F8 ],
			'IN R%d, 0x%x':    lambda Rd, A: [ 0xB000 + ((A & 0x30) << 5) +
					((Rd & 0x1f) << 4) + (A & 0xf) ],
			'OUT 0x%x, R%r':   lambda A, Rr: [ 0xB800 + ((A & 0x30) << 5) +
					((Rr & 0x1f) << 4) + (A & 0xf) ],
			'OUT 0x%x, R24':   lambda A: [ 0xB800 + ((A & 0x30) << 5) +
					(24 << 4) + (A & 0xf) ],
			'PUSH R%d':        lambda Rr: [ 0x920f + ((Rr & 0x1f) << 4) ],
			'POP R%d':         lambda Rd: [ 0x900f + ((Rd & 0x1f) << 4) ],
			'XCH Z, R%d':      lambda Rd: [ 0x9200 + ((Rd & 0x1f) << 4) ],
			'LAS Z, R%d':      lambda Rd: [ 0x9205 + ((Rd & 0x1f) << 4) ],
			'LAC Z, R%d':      lambda Rd: [ 0x9206 + ((Rd & 0x1f) << 4) ],
			'LAT Z, R%d':      lambda Rd: [ 0x9207 + ((Rd & 0x1f) << 4) ],
			'LSL R%d':         lambda Rd: [ 0x0C00 + ((Rd & 0x1f) << 5) +
					(Rd & 0x1f) ],
			'LSR R%d':         lambda Rd: [ 0x9406 + ((Rd & 0x1f) << 4)],
			'ROL R%d':         lambda Rd: [ 0x1C00 + ((Rd & 0x1f) << 5) +
					(Rd & 0x1f) ],
			'ROL R24':         [ 0x1C00 + (24 << 5) + 24 ],
			'ROR R%d':         lambda Rd: [ 0x9407 + ((Rd & 0x1f) << 4) ],
			'ROR R24':         [ 0x9407 + (24 << 4) ],
			'ASR R%d':         lambda Rd: [ 0x9405 + ((Rd & 0x1f) << 4) ],
			'SWAP R%d':        lambda Rd: [ 0x9402 + ((Rd & 0x1f) << 4) ],
			'SWAP R24':        [ 0x9402 + (24 << 4) ],
			'BSET 0x%x':       lambda s: [ 0x9408 + ((s & 0x7) << 4) ],
			'BCLR 0x%x':       lambda s: [ 0x9488 + ((s & 0x7) << 4) ],
			'SBI 0x%x, 0x%x':  lambda A, b: [ 0x9A00 + ((A & 0x1f)<<3) + (b&0x7)],
			'CBI 0x%x, 0x%x':  lambda A, b: [ 0x9800 + ((A & 0x1f)<<3) + (b&0x7)],
			'BST R%d, %d':   lambda Rr, b: [ 0xFA00 + ((Rd & 0x1f)<< 4) 
														+ (b & 0x7)],
			'BST R24, %d':   lambda Rr, b: [ 0xFA00 + (24<< 4) 
														+ (b & 0x7)],
			'BLD R%d, 0x%x':   lambda Rd, b: [ 0xf800 + ((Rd & 0x1f)<<4) +
					(b&0x7)],
			'SEC':             [ 0x9408 ],
			'CLC':             [ 0x9488 ],
			'SEN':             [ 0x9428 ],
			'CLN':             [ 0x94A8 ],
			'SEZ':             [ 0x9418 ],
			'CLZ':             [ 0x9498 ],
			'SEI':             [ 0x9478 ],
			'CLI':             [ 0x94F8 ],
			'SES':             [ 0x9448 ],
			'CLS':             [ 0x94C8 ],
			'SEV':             [ 0x9438 ],
			'CLV':             [ 0x94B8 ],
			'SET':             [ 0x9468 ],
			'CLT':             [ 0x94E8 ],
			'SEH':             [ 0x9458 ],
			'CLH':             [ 0x94D8 ],
			'BREAK':           [ 0x9598 ],
			'NOP':             [ 0x0000 ],
			'SLEEP':           [ 0x9588 ],
			'WDR':             [ 0x95A8 ],
	}
	# the __init__ and all other methods are all inherited
