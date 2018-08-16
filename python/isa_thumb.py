#
# isa_thumb.py
#
# this is for the THUMB ISA
from isa import ISA
class ISAThumb(ISA):
	'''
		this is the data structure for generating code (assembly or machine)
		for the ARM Thumb instruction set.
		It is a "factory".  we define these formatting strings
		and formatting functions as either constant list or lambda to a
		list of expressions.  One can do code-gen and pattern match - but
		they should match exactly...  This also means we can't really do
		labels, but probably that could be solved later?
	'''
	_isa_name = "THUMB"
	_instr = {
			'ADC R%d, R%d': # add with carry. opcode = 0100 0001 01
							lambda Rd, Rs: [0x4140 | (Rs << 3) | Rd],
			'ADD R%d, R%d, R%d': # add reg. Opcode = 0001100
							lambda Rd, Rs, Rn: [0x1800 | (Rn << 6) | (Rs << 3) | Rd],
			'ADD R%d, R%s, #0x%x': # add imm. Opcode = 0001101
							lambda Rd, Rs, Offset: [0x1A00 | ((Offset & 0x7) << 6) | (Rs << 3) | Rd],
			'ADD Rd, #0x%x':  # ADD 8-bit imm.  opcode 00110
							lambda Rd, Offset: [0x3000 | (Rd << 8) | (Offset & 0xFF)],
			'ADD R%d, H%d':   # ADD register in range 8-15 to register in 0-7. op=0100 0100 01
							lambda Rd, Hs: [0x4440 | (Hs << 3) | Rd],
			'ADD H%d, R%d':   # Add register in range 0-7 to one in range 8-15. op=0100 0100 10
							lambda Hd, Rs: [0x4480 | (Rs << 3) | Hd],
			'ADD H%d, H%d':   # Add two registers in range 8-15. op = 0100 0100 11
							lambda Hd, Hs: [0x44C0 | (Hs << 3) | Hd],
			'ADD R%d, PC, #0x%x': # opcode 1010 0
							lambda Rd, imm: [0xA000 | (Rd << 8) | ((imm >> 2) & 0xff)],
			'ADD R%d, SP, #0x%x': # opcode 1010 1
							lambda Rd, imm: [0xA800 | (Rd << 8) | ((imm >> 2) & 0xff)],
			'ADD SP, #%d':  # opcode 1011 0000 0
							lambda imm: [0xB000 | ((imm >> 2)  & 0x7F)],
			'ADD SP, #-%d':  # opcode 1011 0000 1
							lambda imm: [0xB080 | ((imm >> 2)  & 0x7F)],
			'AND R%d, R%d':  # and. Opcode = 0100 0000 00
							lambda Rd, Rs: [0x4000 | (Rs << 3) | Rd],
			'ASR R%d, R%d, #0x%x':  # arithmetic shift right: opcode 00010. Rd=Rs << 5bit
							lambda Rd, Rs, Offset: [0x1000 | ((Offset & 0x1F) << 6) | (Rs << 3) | Rd],
			'ASR R%d, R%d':  # arithmetic right shift, opcode 0100 0001 00
							lambda Rd, Rs: [0x4100 | (Rs << 3) | Rd],
			'B 0x%x':   # unconditional branch. opcode 1110 0
							lambda offset: [0xE000 | ((offset >> 1) & 0x7ff)],
			'BEQ 0x%x': # opcode 1011 0000
							lambda offset: [0xB000 | ((offset >> 1) & 0xff)],
			'BNE 0x%x': # opcode 1011 0001
							lambda offset: [0xB100 | ((offset >> 1) & 0xff)],
			'BCS 0x%x': # opcode 1011 0010
							lambda offset: [0xB200 | ((offset >> 1) & 0xff)],
			'BCC 0x%x': # opcode 1011 0011
							lambda offset: [0xB300 | ((offset >> 1) & 0xff)],
			'BMI 0x%x': # opcode 1011 0100
							lambda offset: [0xB400 | ((offset >> 1) & 0xff)],
			'BPL 0x%x': # opcode 1011 0101
							lambda offset: [0xB500 | ((offset >> 1) & 0xff)],
			'BVS 0x%x': # opcode 1011 0110
							lambda offset: [0xB600 | ((offset >> 1) & 0xff)],
			'BVC 0x%x': # opcode 1011 0111
							lambda offset: [0xB700 | ((offset >> 1) & 0xff)],
			'BHI 0x%x': # opcode 1011 1000
							lambda offset: [0xB800 | ((offset >> 1) & 0xff)],
			'BLS 0x%x': # opcode 1011 1001
							lambda offset: [0xB900 | ((offset >> 1) & 0xff)],
			'BGE 0x%x': # opcode 1011 1010
							lambda offset: [0xBA00 | ((offset >> 1) & 0xff)],
			'BLT 0x%x': # opcode 1011 1011
							lambda offset: [0xBB00 | ((offset >> 1) & 0xff)],
			'BGT 0x%x': # opcode 1011 1100
							lambda offset: [0xBC00 | ((offset >> 1) & 0xff)],
			'BLE 0x%x': # opcode 1011 1101
							lambda offset: [0xBD00 | ((offset >> 1) & 0xff)],
			'BIC R%d, R%d': # bit clear. opcode =0100 0011 10
							lambda Rd, Rs: [0x4380 | (Rs << 3) | Rd],
			'BL 0x%x':  # branch and link. this is a two-instruction sequence.
							lambda offset: [0xF000 | ((offset >> 12) & 0x7FF),
														0xF800 | ((offset >> 1) & 0x7FF)],
			'BX R%d':  # branch and exchange. opcode =0100 0111 00
							lambda Rs: [0x4700 | (Rs << 3)],
			'BX H%d':  # branch and exchange. opcode =0100 0111 01
							lambda Rs: [0x4740 | (Rs << 3)],
			'CMN R%d, R%d': # compare negative. opcode = 0100 0010 11
							lambda Rd, Rs: [0x42C0 | (Rs << 3) | Rd],
			'CMP R%d, #0x%x': # compare. opcode = 00101
									lambda Rd, Offset: [0x2800 | (Rd << 8) | (Offset & 0xFF)],
			'CMP R%d, R%d': # compare . opcode = 0100 0010 10
							lambda Rd, Rs: [0x4280 | (Rs << 3) | Rd],
			'CMP R%d, H%d': # compare . opcode = 0100 0101 01
							lambda Rd, Hs: [0x4540 | (Hs << 3) | Rd],
			'CMP H%d, R%d': # compare . opcode = 0100 0101 10
							lambda Hd, Rs: [0x4580 | (Rs << 3) | Hd],
			'CMP H%d, H%d': # compare . opcode = 0100 0101 11
							lambda Hd, Hs: [0x45C0 | (Hs << 3) | Hd],
			'EOR R%d, R%d': # exclusive or. opcode = 0100 0000 01
							lambda Rd, Rs: [0x4040 | (Rs << 3) | Rd],
			'LDMIA R%d!, {R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, R: [0xC800 | (Rb_ << 8) | (1 << R)],
			'LDMIA R%d!, {R%d, R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, Ra, Rb: [0xC800 | (Rb_ << 8) | (1 << Ra) | (1 << Rb)],
			'LDMIA R%d!, {R%d, R%d, R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, Ra, Rb, Rc: [0xC800 | (Rb_ << 8) | (1 << Ra) | (1 << Rb) | \
									(1 << Rc)],
			'LDMIA R%d!, {R%d, R%d, R%d, R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, Ra, Rb, Rc, Rd: [0xC800 | (Rb_ << 8) | (1 << Ra) | (1 << Rb) | \
									(1 << Rc) | (1 << Rd)],
			'LDMIA R%d!, {R%d, R%d, R%d, R%d, R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, Ra, Rb, Rc, Rd, Re: [0xC800 | (Rb_ << 8) | (1 << Ra) | \
									(1 << Rb) | (1 << Rc) | (1 << Rd) | (1 << Re)],
			'LDMIA R%d!, {R%d, R%d, R%d, R%d, R%d, R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, Ra, Rb, Rc, Rd, Re, Rf: [0xC800 | (Rb_ << 8) | (1 << Ra) | \
									(1 << Rb) | (1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf)],
			'LDMIA R%d!, {R%d, R%d, R%d, R%d, R%d, R%d, R%d}': # load multiple. opcode 1100 1 
							lambda Rb_, Ra, Rb, Rc, Rd, Re, Rf, Rg: [0xC800 | (Rb_ << 8) | (1 << Ra) | \
									(1 << Rb) | (1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf) | (1 << Rg)],
			'LDMIA R%d!, {R0-R7}': # load multiple. opcode 1100 1 
							lambda Rb_: [0xC8FF | (Rb_ << 8)],
			'LDR R%d, [PC, #%d]':  # load word. opcode = 0100 1. imm is concatenated with 00 for addr
							lambda Rd, imm: [0x4800 | (Rd << 8) | ((imm >> 2)& 0xff)],
			'LDR R%d, [R%d, R%d]': # opcode = 0101 100.
							lambda Rd, Rb, Ro: [0x5800 | (Ro << 6) | (Rb << 3) | Rd],
			'LDR R%d, [R%d, #%d]': # opcode = 0110 1
							lambda Rd, Rb, imm: [0x6800 | (((imm >> 2) & 0x1F) << 6) | (Rb << 3) | Rd],
			'LDR R%d, [SP, #%d]': # opcode = 1001 1
							lambda Rd, imm: [0x9800 | (Rd << 8) | ((imm >> 2) & 0x1F)],
			'LDRB R%d, [R%d, R%d]': # load byte. opcode = 0101 110
							lambda Rd, Rb, Ro: [0x5C00 | (Ro << 6) | (Rb << 3) | Rd],
			'LDRB R%d, [R%d, #%d]': # opcode = 0111 1
							lambda Rd, Rb, imm: [0x7800 | (((imm) & 0x1F) << 6) | (Rb << 3) | Rd],
			'LDRH R%d, [R%d, R%d]': # load halfword. opcode = 0101 101
							lambda Rd, Rb, Ro: [0x5A00 | (Ro << 6) | (Rb << 3) | Rd],
			'LDRH R%d, [R%d, #%d]': # opcode = 1000 1
							lambda Rd, Rb, imm: [0x8802 | (((imm >> 1) & 0x1F) << 6) | (Rb << 3) | Rd],
			'LSL R%d, R%d, #%d':  # logical shift left. opcode = 00000
							lambda Rd, Rs, Offset: [((Offset & 0x1F) << 6) | (Rs << 3) | Rd ],
			'LSL R%d, R%d':  # left shift, opcode 0100 0000 10
							lambda Rd, Rs: [0x4080 | (Rs << 3) | Rd],
			'LDSB R%d, [R%d, R%d]': # load sign-extended byte. opcode = 0101 011
							lambda Rd, Rb, Ro: [0x5600 | (Ro << 6) | (Rb << 3) | Rd],
			'LDSH R%d, [R%d, R%d]': # load sign-extended halfword. opcode = 0101 111
							lambda Rd, Rb, Ro: [0x5E00 | (Ro << 6) | (Rb << 3) | Rd],
			'LSR R%d, R%d, #%d':  # logical shift right. opcode = 00001
							lambda Rd, Rs, Offset: [0x0800 | ((Offset & 0x1F)<< 6) | (Rs << 3) | Rd],
			'LSR R%d, R%d':  # right shift, opcode 0100 0000 11
							lambda Rd, Rs: [0x40C0 | (Rs << 3) | Rd],
			'MOV R%d, #0x%x':  # move imm. opcode 00100
							lambda Rd, Offset: [0x2000 | (Rd << 8) | (Offset&0xFF)],
			'MOV R%d, H%d': # move reg. opcode = 0100 0110 01
							lambda Rd, Hs: [0x4640 | (Hs << 3) | Rd],
			'MOV H%d, R%d': # move reg. opcode = 0100 0110 10
							lambda Hd, Rs: [0x4680 | (Rs << 3) | Hd],
			'MOV H%d, H%d': # move reg. opcode = 0100 0110 11
							lambda Hd, Hs: [0x4680 | (Hs << 3) | Hd],
			'MUL R%d, R%d':  # multiply. opcode = 0100 0011 01
							lambda Rd, Rs: [0x4340 | (Rs << 3) | Rd],
			'MVN R%d, R%d':  # move negative register. opcode = 0100 0011 11
							lambda Rd, Rs: [0x43C0 | (Rs << 3) | Rd],
			'NEG R%d, R%d':  # negate. opcode = 0100 0010 01
							lambda Rd, Rs: [0x4240 | (Rs << 3) | Rd],
			'ORR R%d, R%d':  # OR. opcode = 0100 0011 00
							lambda Rd, Rs: [0x4300 | (Rs << 3) | Rd],
			'ROR R%d, R%d':  # rotate right. opcode = 0100 0001 11
							lambda Rd, Rs: [0x41C0 | (Rs << 3) | Rd],
			'SBC R%d, R%d':  # subtract with carry. opcode 0100 0001 10
							lambda Rd, Rs: [0x4180 | (Rs << 3) | Rd],
			'STR R%d, [R%d, R%d]':   # store word.  opcode = 0101 000
							lambda Rd, Rb, Ro: [0x5000 | (Ro << 6) | (Rb << 3) | Rd],
			'STR R%d, [R%d, #%d]': # opcode = 0110 0
							lambda Rd, Rb, imm: [0x6000 | (((imm >> 2) & 0x1F) << 6) | (Rb << 3) | Rd],
			'STR R%d, [SP, #0%d]': # opcode = 1001 0
							lambda Rd, imm: [0x9000 | (Rd << 8) | ((imm >> 2) & 0x1F)],
			'STRB R%d, [R%d, R%d]':  # store byte. opcode = 0101 010
							lambda Rd, Rb, Ro: [0x5400 | (Ro << 6) | (Rb << 3) | Rd],
			'STRB R%d, [R%d, #%d]': # opcode = 0111 0
							lambda Rd, Rb, imm: [0x7000 | (((imm) & 0x1F) << 6) | (Rb << 3) | Rd],
			'STRH R%d, [R%d, R%d]':  # store halfword. opcode = 0101 001
							lambda Rd, Rb, Ro: [0x5200 | (Ro << 6) | (Rb << 3) | Rd],
			'STRH R%d, [R%d, #%d]': # opcode = 1000 0
							lambda Rd, Rb, imm: [0x8000 | (((imm >> 1) & 0x1F) << 6) | (Rb << 3) | Rd],
			'SWI 0x%x':   # software interrupt. opcode 1101 1111
							lambda value: [0xDF00 | (value & 0xff)],
			'SUB R%d, R%d, R%d':   # subtract register. Opcode 0001110
							lambda Rd, Rs, Rn: [0x1C00 | (Rn << 6) | (Rs << 3) | Rd],
			'SUB R%d, R%d, #0x%x':   # subtract imm. Opcode 0001111
							lambda Rd, Rs, offset: [0x1E00 | ((offset & 0x7)<< 6) | (Rs << 3) | Rd],
			'SUB R%d, #0x%x': # offset 00111
							lambda Rd, Offset: [0x3800 | (Rd << 8) | (Offset & 0xFF)],
			'TST R%d, R%d':   # test bits. Opcode 0100 0010 00
							lambda Rd, Rs: [0x4200 | (Rs << 3) | Rd],
			'MUL R%d, R%d':  # multiply. opcode = 0100 0011 01
							lambda Rd, Rs: [0x4340 | (Rs << 3) | Rd],
			'MVN R%d, R%d':  # move negative register. opcode = 0100 0011 11
							lambda Rd, Rs: [0x43C0 | (Rs << 3) | Rd],
			'NEG R%d, R%d':  # negate. opcode = 0100 0010 01
							lambda Rd, Rs: [0x4240 | (Rs << 3) | Rd],
			'ORR R%d, R%d':  # OR. opcode = 0100 0011 00
							lambda Rd, Rs: [0x4300 | (Rs << 3) | Rd],
			'POP {R%d}':  # pop registers. opcode = 1011 1100
							lambda R: [0xBC00 | (1 << R)],
			'POP {R%d, PC}':  # pop registers. opcode = 1011 1101
							lambda R: [0xBD00 | (1 << R)],
			'POP {R%d, R%d}':  # pop registers. opcode 1011 1100 
							lambda Ra, Rb: [0xBC00 | (1 << Ra) | (1 << Rb)],
			'POP {R%d, R%d, PC}': # pop registers. opcode 1011 1101 
							lambda Ra, Rb: [0xBD00 | (1 << Ra) | (1 << Rb)],
			'POP {R%d, R%d, R%d}':  # pop registers. opcode 1011 1100 
							lambda Ra, Rb, Rc: [0xBC00 | (1 << Ra) | (1 << Rb) | (1 << Rc)],
			'POP {R%d, R%d, R%d, PC}': # pop registers. opcode 1011 1101 
							lambda Ra, Rb, Rc: [0xBD00 | (1 << Ra) | (1 << Rb) | (1 << Rc)],
			'POP {R%d, R%d, R%d, R%d}':  # pop registers. opcode 1011 1100 
							lambda Ra, Rb, Rc, Rd: [0xBC00 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd)],
			'POP {R%d, R%d, R%d, R%d, PC}': # pop registers. opcode 1011 1101 
							lambda Ra, Rb, Rc, Rd: [0xBD00 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd)],
			'POP {R%d, R%d, R%d, R%d, R%d}':  # pop registers. opcode 1011 1100 
							lambda Ra, Rb, Rc, Rd, Re: [0xBC00 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re)],
			'POP {R%d, R%d, R%d, R%d, R%d, PC}': # pop registers. opcode 1011 1101 
							lambda Ra, Rb, Rc, Rd, Re: [0xBD00 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re)],
			'POP {R%d, R%d, R%d, R%d, R%d, R%d}':  # pop registers. opcode 1011 1100 
							lambda Ra, Rb, Rc, Rd, Re, Rf: [0xBC00 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re) | (1 << Rf)],
			'POP {R%d, R%d, R%d, R%d, R%d, R%d, PC}': # pop registers. opcode 1011 1101 
							lambda Ra, Rb, Rc, Rd, Re, Rf: [0xBD00 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re) | (1 << Rf)],
			'POP {R%d, R%d, R%d, R%d, R%d, R%d, R%d}':  # pop registers. opcode 1011 1100 
							lambda Ra, Rb, Rc, Rd, Re, Rf, Rg: [0xBC00 | (1 << Ra) | (1 << Rb) | \
									(1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf)],
			'POP {R%d, R%d, R%d, R%d, R%d, R%d, R%d, PC}': # pop registers. opcode 1011 1101 
							lambda Ra, Rb, Rc, Rd, Re, Rf, Rg: [0xBD00 | (1 << Ra) | (1 << Rb) | \
									(1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf)],
			'POP {R0-R7}':  # pop registers. opcode 1011 1100 
							[0xBCFF],
			'POP {R0-R7, PC}': # pop registers. opcode 1011 1101 
							[0xBDFF],
			'PUSH {R%d}':  # push registers. opcode 1011 0100 
							lambda R: [0xB400 | (1 << R)],
			'PUSH {R%d, LR}': # push registers. opcode 1011 0101 
							lambda R: [0xB500 | (1 << R)],
			'PUSH {R%d, R%d}':  # push registers. opcode 1011 0100 
							lambda Ra, Rb: [0xB400 | (1 << Ra) | (1 << Rb)],
			'PUSH {R%d, R%d, LR}': # push registers. opcode 1011 0101 
							lambda Ra, Rb: [0xB500 | (1 << Ra) | (1 << Rb)],
			'PUSH {R%d, R%d, R%d}':  # push registers. opcode 1011 0100 
							lambda Ra, Rb, Rc: [0xB400 | (1 << Ra) | (1 << Rb) | (1 << Rc)],
			'PUSH {R%d, R%d, R%d, LR}': # push registers. opcode 1011 0101 
							lambda Ra, Rb, Rc: [0xB500 | (1 << Ra) | (1 << Rb) | (1 << Rc)],
			'PUSH {R%d, R%d, R%d, R%d}':  # push registers. opcode 1011 0100 
							lambda Ra, Rb, Rc, Rd: [0xB400 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd)],
			'PUSH {R%d, R%d, R%d, R%d, LR}': # push registers. opcode 1011 0101 
							lambda Ra, Rb, Rc, Rd: [0xB500 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd)],
			'PUSH {R%d, R%d, R%d, R%d, R%d}':  # push registers. opcode 1011 0100 
							lambda Ra, Rb, Rc, Rd, Re: [0xB400 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re)],
			'PUSH {R%d, R%d, R%d, R%d, R%d, LR}': # push registers. opcode 1011 0101 
							lambda Ra, Rb, Rc, Rd, Re: [0xB500 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re)],
			'PUSH {R%d, R%d, R%d, R%d, R%d, R%d}':  # push registers. opcode 1011 0100 
							lambda Ra, Rb, Rc, Rd, Re, Rf: [0xB400 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re) | (1 << Rf)],
			'PUSH {R%d, R%d, R%d, R%d, R%d, R%d, LR}': # push registers. opcode 1011 0101 
							lambda Ra, Rb, Rc, Rd, Re, Rf: [0xB500 | (1 << Ra) | (1 << Rb) | (1 << Rc) | \
									(1 << Rd) | (1 << Re) | (1 << Rf)],
			'PUSH {R%d, R%d, R%d, R%d, R%d, R%d, R%d}':  # push registers. opcode 1011 0100 
							lambda Ra, Rb, Rc, Rd, Re, Rf, Rg: [0xB400 | (1 << Ra) | (1 << Rb) | \
									(1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf)],
			'PUSH {R%d, R%d, R%d, R%d, R%d, R%d, R%d, LR}': # push registers. opcode 1011 0101 
							lambda Ra, Rb, Rc, Rd, Re, Rf, Rg: [0xB500 | (1 << Ra) | (1 << Rb) | \
									(1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf)],
			'PUSH {R0-R7}':  # push registers. opcode 1011 0100 
							[0xB4FF],
			'PUSH {R0-R7, LR}': # push registers. opcode 1011 0101 
							[0xB5FF],
			'STMIA R%d!, {R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, R: [0xC000 | (Rb_ << 8) | (1 << R)],
			'STMIA R%d!, {R%d, R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, Ra, Rb: [0xC000 | (Rb_ << 8) | (1 << Ra) | (1 << Rb)],
			'STMIA R%d!, {R%d, R%d, R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, Ra, Rb, Rc: [0xC000 | (Rb_ << 8) | (1 << Ra) | (1 << Rb) | \
									(1 << Rc)],
			'STMIA R%d!, {R%d, R%d, R%d, R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, Ra, Rb, Rc, Rd: [0xC000 | (Rb_ << 8) | (1 << Ra) | (1 << Rb) | \
									(1 << Rc) | (1 << Rd)],
			'STMIA R%d!, {R%d, R%d, R%d, R%d, R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, Ra, Rb, Rc, Rd, Re: [0xC000 | (Rb_ << 8) | (1 << Ra) | \
									(1 << Rb) | (1 << Rc) | (1 << Rd) | (1 << Re)],
			'STMIA R%d!, {R%d, R%d, R%d, R%d, R%d, R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, Ra, Rb, Rc, Rd, Re, Rf: [0xC000 | (Rb_ << 8) | (1 << Ra) | \
									(1 << Rb) | (1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf)],
			'STMIA R%d!, {R%d, R%d, R%d, R%d, R%d, R%d, R%d}': # store multiple. opcode 1100 0 
							lambda Rb_, Ra, Rb, Rc, Rd, Re, Rf, Rg: [0xC000 | (Rb_ << 8) | (1 << Ra) | \
									(1 << Rb) | (1 << Rc) | (1 << Rd) | (1 << Re) | (1 << Rf) | (1 << Rg)],
			'STMIA R%d!, {R0-R7}': # store multiple. opcode 1100 0 
							lambda Rb_: [0xC0FF | (Rb_ << 8)],
			'.word 0x%x': 
							lambda data: [(data >> 16) & 0xffff, data & 0xffff],
	}
	# all methods are inherited from ISA, so no need to define more
