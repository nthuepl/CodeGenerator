;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.4.0/*rc1*/ #8960 (Mar 15 2014) (MINGW32)
; This file was generated Wed Mar 26 21:02:59 2014
;--------------------------------------------------------
	.module mainBase
	.optsdcc -mmcs51 --model-small
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _main
	.globl _putc
	.globl _puts
	.globl _serial_init
	.globl _mdelay
	.globl _store_cpu_rate
	.globl _spi_write_then_read
	.globl _poll_rf_send
	.globl _poll_rf_configure
	.globl _poll_rf_init
	.globl _PWDI
	.globl _PX5
	.globl _PX4
	.globl _PX3
	.globl _PX2
	.globl _EWDI
	.globl _EX5
	.globl _EX4
	.globl _EX3
	.globl _EX2
	.globl _WDTI
	.globl _CY
	.globl _AC
	.globl _F0
	.globl _RS1
	.globl _RS0
	.globl _OV
	.globl _F1
	.globl _P
	.globl _TF2
	.globl _EXF2
	.globl _RCLK
	.globl _TCLK
	.globl _EXEN2
	.globl _TR2
	.globl _CT2
	.globl _C_T2
	.globl _CPRL2
	.globl _CP_RL2
	.globl _PT2
	.globl _PS
	.globl _PT1
	.globl _PX1
	.globl _PT0
	.globl _PX0
	.globl _EA
	.globl _ET2
	.globl _ES
	.globl _ET1
	.globl _EX1
	.globl _ET0
	.globl _EX0
	.globl _PWR_UP
	.globl _CE
	.globl _DR2
	.globl _DR2_CE
	.globl _CLK2
	.globl _DOUT2
	.globl _CS
	.globl _DR1
	.globl _CLK1
	.globl _DATA
	.globl _SM0
	.globl _SM1
	.globl _SM2
	.globl _REN
	.globl _TB8
	.globl _RB8
	.globl _TI
	.globl _RI
	.globl _DIN0
	.globl _P1_2
	.globl _DIO1
	.globl _P1_1
	.globl _DIO0
	.globl _T2
	.globl _P1_0
	.globl _TF1
	.globl _TR1
	.globl _TF0
	.globl _TR0
	.globl _IE1
	.globl _IT1
	.globl _IE0
	.globl _IT0
	.globl _DIO9
	.globl _PWM
	.globl _P0_7
	.globl _DIO8
	.globl _T1
	.globl _P0_6
	.globl _DIO7
	.globl _T0
	.globl _P0_5
	.globl _DIO6
	.globl _INT1_N
	.globl _P0_4
	.globl _DIO5
	.globl _INT0_N
	.globl _P0_3
	.globl _DIO4
	.globl _TXD
	.globl _P0_2
	.globl _DIO3
	.globl _RXD
	.globl _P0_1
	.globl _DIO2
	.globl _P0_0
	.globl _EIP
	.globl _B
	.globl _EIE
	.globl _ACC
	.globl _EICON
	.globl _PSW
	.globl _TH2
	.globl _TL2
	.globl _RCAP2H
	.globl _RCAP2L
	.globl _T2CON
	.globl _DEV_OFFSET
	.globl _T2_1V2
	.globl _T1_1V2
	.globl _IP
	.globl _TEST_MODE
	.globl _CK_CTRL
	.globl _TICK_DV
	.globl _SPICLK
	.globl _SPI_CTRL
	.globl _SPI_DATA
	.globl _RSTREAS
	.globl _REGX_CTRL
	.globl _REGX_LSB
	.globl _REGX_MSB
	.globl _PWMDUTY
	.globl _PWMCON
	.globl _IE
	.globl _ADCSTATIC
	.globl _ADCDATAL
	.globl _ADCDATAH
	.globl _ADCCON
	.globl _RADIO
	.globl _SBUF
	.globl _SCON
	.globl _P1_ALT
	.globl _P1_DIR
	.globl _P0_ALT
	.globl _P0_DIR
	.globl _MPAGE
	.globl _EXIF
	.globl _P1
	.globl _SPC_FNC
	.globl _CKCON
	.globl _TH1
	.globl _TH0
	.globl _TL1
	.globl _TL0
	.globl _TMOD
	.globl _TCON
	.globl _PCON
	.globl _DPS
	.globl _DPH1
	.globl _DPL1
	.globl _DPH0
	.globl _DPH
	.globl _DPL0
	.globl _DPL
	.globl _SP
	.globl _P0
	.globl _counter
	.globl _i
	.globl _code_segment
	.globl _MessageBUF
	.globl _dst_addr
	.globl _cfg
	.globl _rf_data
	.globl _interrupt_rf
	.globl _interrupt_serial
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
	.area RSEG    (ABS,DATA)
	.org 0x0000
_P0	=	0x0080
_SP	=	0x0081
_DPL	=	0x0082
_DPL0	=	0x0082
_DPH	=	0x0083
_DPH0	=	0x0083
_DPL1	=	0x0084
_DPH1	=	0x0085
_DPS	=	0x0086
_PCON	=	0x0087
_TCON	=	0x0088
_TMOD	=	0x0089
_TL0	=	0x008a
_TL1	=	0x008b
_TH0	=	0x008c
_TH1	=	0x008d
_CKCON	=	0x008e
_SPC_FNC	=	0x008f
_P1	=	0x0090
_EXIF	=	0x0091
_MPAGE	=	0x0092
_P0_DIR	=	0x0094
_P0_ALT	=	0x0095
_P1_DIR	=	0x0096
_P1_ALT	=	0x0097
_SCON	=	0x0098
_SBUF	=	0x0099
_RADIO	=	0x00a0
_ADCCON	=	0x00a1
_ADCDATAH	=	0x00a2
_ADCDATAL	=	0x00a3
_ADCSTATIC	=	0x00a4
_IE	=	0x00a8
_PWMCON	=	0x00a9
_PWMDUTY	=	0x00aa
_REGX_MSB	=	0x00ab
_REGX_LSB	=	0x00ac
_REGX_CTRL	=	0x00ad
_RSTREAS	=	0x00b1
_SPI_DATA	=	0x00b2
_SPI_CTRL	=	0x00b3
_SPICLK	=	0x00b4
_TICK_DV	=	0x00b5
_CK_CTRL	=	0x00b6
_TEST_MODE	=	0x00b7
_IP	=	0x00b8
_T1_1V2	=	0x00bc
_T2_1V2	=	0x00bd
_DEV_OFFSET	=	0x00be
_T2CON	=	0x00c8
_RCAP2L	=	0x00ca
_RCAP2H	=	0x00cb
_TL2	=	0x00cc
_TH2	=	0x00cd
_PSW	=	0x00d0
_EICON	=	0x00d8
_ACC	=	0x00e0
_EIE	=	0x00e8
_B	=	0x00f0
_EIP	=	0x00f8
;--------------------------------------------------------
; special function bits
;--------------------------------------------------------
	.area RSEG    (ABS,DATA)
	.org 0x0000
_P0_0	=	0x0080
_DIO2	=	0x0080
_P0_1	=	0x0081
_RXD	=	0x0081
_DIO3	=	0x0081
_P0_2	=	0x0082
_TXD	=	0x0082
_DIO4	=	0x0082
_P0_3	=	0x0083
_INT0_N	=	0x0083
_DIO5	=	0x0083
_P0_4	=	0x0084
_INT1_N	=	0x0084
_DIO6	=	0x0084
_P0_5	=	0x0085
_T0	=	0x0085
_DIO7	=	0x0085
_P0_6	=	0x0086
_T1	=	0x0086
_DIO8	=	0x0086
_P0_7	=	0x0087
_PWM	=	0x0087
_DIO9	=	0x0087
_IT0	=	0x0088
_IE0	=	0x0089
_IT1	=	0x008a
_IE1	=	0x008b
_TR0	=	0x008c
_TF0	=	0x008d
_TR1	=	0x008e
_TF1	=	0x008f
_P1_0	=	0x0090
_T2	=	0x0090
_DIO0	=	0x0090
_P1_1	=	0x0091
_DIO1	=	0x0091
_P1_2	=	0x0092
_DIN0	=	0x0092
_RI	=	0x0098
_TI	=	0x0099
_RB8	=	0x009a
_TB8	=	0x009b
_REN	=	0x009c
_SM2	=	0x009d
_SM1	=	0x009e
_SM0	=	0x009f
_DATA	=	0x00a0
_CLK1	=	0x00a1
_DR1	=	0x00a2
_CS	=	0x00a3
_DOUT2	=	0x00a4
_CLK2	=	0x00a5
_DR2_CE	=	0x00a6
_DR2	=	0x00a6
_CE	=	0x00a6
_PWR_UP	=	0x00a7
_EX0	=	0x00a8
_ET0	=	0x00a9
_EX1	=	0x00aa
_ET1	=	0x00ab
_ES	=	0x00ac
_ET2	=	0x00ad
_EA	=	0x00af
_PX0	=	0x00b8
_PT0	=	0x00b9
_PX1	=	0x00ba
_PT1	=	0x00bb
_PS	=	0x00bc
_PT2	=	0x00bd
_CP_RL2	=	0x00c8
_CPRL2	=	0x00c8
_C_T2	=	0x00c9
_CT2	=	0x00c9
_TR2	=	0x00ca
_EXEN2	=	0x00cb
_TCLK	=	0x00cc
_RCLK	=	0x00cd
_EXF2	=	0x00ce
_TF2	=	0x00cf
_P	=	0x00d0
_F1	=	0x00d1
_OV	=	0x00d2
_RS0	=	0x00d3
_RS1	=	0x00d4
_F0	=	0x00d5
_AC	=	0x00d6
_CY	=	0x00d7
_WDTI	=	0x00db
_EX2	=	0x00e8
_EX3	=	0x00e9
_EX4	=	0x00ea
_EX5	=	0x00eb
_EWDI	=	0x00ec
_PX2	=	0x00f8
_PX3	=	0x00f9
_PX4	=	0x00fa
_PX5	=	0x00fb
_PWDI	=	0x00fc
;--------------------------------------------------------
; overlayable register banks
;--------------------------------------------------------
	.area REG_BANK_0	(REL,OVR,DATA)
	.ds 8
;--------------------------------------------------------
; overlayable bit register bank
;--------------------------------------------------------
	.area BIT_BANK	(REL,OVR,DATA)
bits:
	.ds 1
	b0 = bits[0]
	b1 = bits[1]
	b2 = bits[2]
	b3 = bits[3]
	b4 = bits[4]
	b5 = bits[5]
	b6 = bits[6]
	b7 = bits[7]
;--------------------------------------------------------
; internal ram data
;--------------------------------------------------------
	.area DSEG    (DATA)
_rf_data::
	.ds 15
_cfg::
	.ds 3
_dst_addr::
	.ds 3
_MessageBUF::
	.ds 28
_code_segment::
	.ds 1
_i::
	.ds 1
_counter::
	.ds 1
_interrupt_rf_fb_counter_1_17:
	.ds 1
_interrupt_serial_header_counter_1_20:
	.ds 1
_interrupt_serial_code_counter_1_20:
	.ds 1
;--------------------------------------------------------
; overlayable items in internal ram 
;--------------------------------------------------------
;--------------------------------------------------------
; Stack segment in internal ram 
;--------------------------------------------------------
	.area	SSEG
__start__stack:
	.ds	1

;--------------------------------------------------------
; indirectly addressable internal ram data
;--------------------------------------------------------
	.area ISEG    (DATA)
;--------------------------------------------------------
; absolute internal ram data
;--------------------------------------------------------
	.area IABS    (ABS,DATA)
	.area IABS    (ABS,DATA)
;--------------------------------------------------------
; bit data
;--------------------------------------------------------
	.area BSEG    (BIT)
;--------------------------------------------------------
; paged external ram data
;--------------------------------------------------------
	.area PSEG    (PAG,XDATA)
;--------------------------------------------------------
; external ram data
;--------------------------------------------------------
	.area XSEG    (XDATA)
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area XABS    (ABS,XDATA)
;--------------------------------------------------------
; external initialized ram data
;--------------------------------------------------------
	.area XISEG   (XDATA)
	.area HOME    (CODE)
	.area GSINIT0 (CODE)
	.area GSINIT1 (CODE)
	.area GSINIT2 (CODE)
	.area GSINIT3 (CODE)
	.area GSINIT4 (CODE)
	.area GSINIT5 (CODE)
	.area GSINIT  (CODE)
	.area GSFINAL (CODE)
	.area CSEG    (CODE)
;--------------------------------------------------------
; interrupt vector 
;--------------------------------------------------------
	.area HOME    (CODE)
__interrupt_vect:
	ljmp	__sdcc_gsinit_startup
	reti
	.ds	7
	reti
	.ds	7
	reti
	.ds	7
	reti
	.ds	7
	ljmp	_interrupt_serial
	.ds	5
	reti
	.ds	7
	reti
	.ds	7
	reti
	.ds	7
	reti
	.ds	7
	reti
	.ds	7
	ljmp	_interrupt_rf
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area HOME    (CODE)
	.area GSINIT  (CODE)
	.area GSFINAL (CODE)
	.area GSINIT  (CODE)
	.globl __sdcc_gsinit_startup
	.globl __sdcc_program_startup
	.globl __start__stack
	.globl __mcs51_genXINIT
	.globl __mcs51_genXRAMCLEAR
	.globl __mcs51_genRAMCLEAR
;	../src/mainBase.c:36: struct rf_config rf_data = {
	mov	_rf_data,#0x00
	mov	(_rf_data + 0x0001),#0xE0
	mov	(_rf_data + 0x0002),#0x00
	mov	(_rf_data + 0x0003),#0x00
	mov	(_rf_data + 0x0004),#0x00
	mov	(_rf_data + 0x0005),#0x00
	mov	(_rf_data + 0x0006),#0x00
	mov	(_rf_data + 0x0007),#0x00
	mov	(_rf_data + 0x0008),#0x00
	mov	(_rf_data + 0x0009),#0x02
	mov	(_rf_data + 0x000a),#0x02
	mov	(_rf_data + 0x000b),#0x02
	mov	(_rf_data + 0x000c),#0x61
	mov	(_rf_data + 0x000d),#0x6F
	mov	(_rf_data + 0x000e),#0x14
;	../src/mainBase.c:45: struct rf_config *cfg = &rf_data;
	mov	_cfg,#_rf_data
	mov	(_cfg + 1),#0x00
	mov	(_cfg + 2),#0x40
;	../src/mainBase.c:46: char dst_addr[3] = { 0x0f, 0x01, 0x01 };
	mov	_dst_addr,#0x0F
	mov	(_dst_addr + 0x0001),#0x01
	mov	(_dst_addr + 0x0002),#0x01
;	../src/mainBase.c:49: unsigned char code_segment = 0;
	mov	_code_segment,#0x00
;	../src/mainBase.c:50: unsigned char i = 0, counter = 0;
	mov	_i,#0x00
;	../src/mainBase.c:50: 
	mov	_counter,#0x00
	.area GSFINAL (CODE)
	ljmp	__sdcc_program_startup
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area HOME    (CODE)
	.area HOME    (CODE)
__sdcc_program_startup:
	ljmp	_main
;	return from main will return to caller
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area CSEG    (CODE)
;------------------------------------------------------------
;Allocation info for local variables in function 'main'
;------------------------------------------------------------
;	../src/mainBase.c:52: void main()
;	-----------------------------------------
;	 function main
;	-----------------------------------------
_main:
	ar7 = 0x07
	ar6 = 0x06
	ar5 = 0x05
	ar4 = 0x04
	ar3 = 0x03
	ar2 = 0x02
	ar1 = 0x01
	ar0 = 0x00
;	../src/mainBase.c:54: store_cpu_rate(16);
	mov	dptr,#(0x10&0x00ff)
	clr	a
	mov	b,a
	lcall	_store_cpu_rate
;	../src/mainBase.c:56: serial_init(19200);
	mov	dptr,#0x4B00
	lcall	_serial_init
;	../src/mainBase.c:58: P0_DIR &= ~0x28;
	mov	r7,_P0_DIR
	mov	a,#0xD7
	anl	a,r7
	mov	_P0_DIR,a
;	../src/mainBase.c:59: P0_ALT &= ~0x28;
	mov	r7,_P0_ALT
	mov	a,#0xD7
	anl	a,r7
	mov	_P0_ALT,a
;	../src/mainBase.c:61: rf_init();
	lcall	_poll_rf_init
;	../src/mainBase.c:62: rf_configure(cfg);
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	lcall	_poll_rf_configure
;	../src/mainBase.c:65: EA = 1;
	setb	_EA
;	../src/mainBase.c:67: ES = 1;
	setb	_ES
;	../src/mainBase.c:69: EX4 = 1;
	setb	_EX4
;	../src/mainBase.c:71: for(i=0;i<6;i++)
	mov	_i,#0x00
00105$:
;	../src/mainBase.c:73: blink_led();
	xrl	_P0,#0x20
;	../src/mainBase.c:74: mdelay(500);
	mov	dptr,#0x01F4
	lcall	_mdelay
;	../src/mainBase.c:71: for(i=0;i<6;i++)
	inc	_i
	mov	a,#0x100 - 0x06
	add	a,_i
	jnc	00105$
;	../src/mainBase.c:76: puts("\n----------------------------");
	mov	dptr,#___str_0
	mov	b,#0x80
	lcall	_puts
;	../src/mainBase.c:77: puts( "\nStartup.\n" );
	mov	dptr,#___str_1
	mov	b,#0x80
	lcall	_puts
;	../src/mainBase.c:78: while(1)
00103$:
	sjmp	00103$
;------------------------------------------------------------
;Allocation info for local variables in function 'interrupt_rf'
;------------------------------------------------------------
;fb_counter                Allocated with name '_interrupt_rf_fb_counter_1_17'
;------------------------------------------------------------
;	../src/mainBase.c:84: void interrupt_rf() __interrupt 10
;	-----------------------------------------
;	 function interrupt_rf
;	-----------------------------------------
_interrupt_rf:
	push	bits
	push	acc
	push	b
	push	dpl
	push	dph
	push	(0+7)
	push	(0+6)
	push	(0+5)
	push	(0+4)
	push	(0+3)
	push	(0+2)
	push	(0+1)
	push	(0+0)
	push	psw
	mov	psw,#0x00
;	../src/mainBase.c:93: while (DR1) {
00103$:
	jnb	_DR1,00105$
;	../src/mainBase.c:94: MessageBUF[fb_counter++] = spi_write_then_read(0);
	mov	r7,_interrupt_rf_fb_counter_1_17
	inc	_interrupt_rf_fb_counter_1_17
	mov	a,r7
	add	a,#_MessageBUF
	mov	r1,a
	mov	dpl,#0x00
	push	ar1
	lcall	_spi_write_then_read
	mov	a,dpl
	pop	ar1
	mov	@r1,a
;	../src/mainBase.c:95: putc( MessageBUF[fb_counter-1]);
	mov	a,_interrupt_rf_fb_counter_1_17
	dec	a
	add	a,#_MessageBUF
	mov	r1,a
	mov	dpl,@r1
	lcall	_putc
;	../src/mainBase.c:100: if( fb_counter == RF_LENGTH ){
	mov	a,#0x1C
	cjne	a,_interrupt_rf_fb_counter_1_17,00103$
;	../src/mainBase.c:102: cfg->rf_prog[1] = 0x14;
	mov	a,#0x0E
	add	a,_cfg
	mov	r5,a
	clr	a
	addc	a,(_cfg + 1)
	mov	r6,a
	mov	r7,(_cfg + 2)
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,#0x14
	lcall	__gptrput
;	../src/mainBase.c:103: rf_configure( cfg );
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	lcall	_poll_rf_configure
;	../src/mainBase.c:104: fb_counter = 0;
	mov	_interrupt_rf_fb_counter_1_17,#0x00
	sjmp	00103$
00105$:
;	../src/mainBase.c:111: CE = 0;
	clr	_CE
;	../src/mainBase.c:112: EXIF &= ~0x40;
	mov	r7,_EXIF
	mov	a,#0xBF
	anl	a,r7
	mov	_EXIF,a
	pop	psw
	pop	(0+0)
	pop	(0+1)
	pop	(0+2)
	pop	(0+3)
	pop	(0+4)
	pop	(0+5)
	pop	(0+6)
	pop	(0+7)
	pop	dph
	pop	dpl
	pop	b
	pop	acc
	pop	bits
	reti
;------------------------------------------------------------
;Allocation info for local variables in function 'interrupt_serial'
;------------------------------------------------------------
;header_counter            Allocated with name '_interrupt_serial_header_counter_1_20'
;code_counter              Allocated with name '_interrupt_serial_code_counter_1_20'
;------------------------------------------------------------
;	../src/mainBase.c:115: void interrupt_serial() __interrupt 4
;	-----------------------------------------
;	 function interrupt_serial
;	-----------------------------------------
_interrupt_serial:
	push	bits
	push	acc
	push	b
	push	dpl
	push	dph
	push	(0+7)
	push	(0+6)
	push	(0+5)
	push	(0+4)
	push	(0+3)
	push	(0+2)
	push	(0+1)
	push	(0+0)
	push	psw
	mov	psw,#0x00
;	../src/mainBase.c:120: if(RI) {
;	../src/mainBase.c:122: RI = 0;
	jbc	_RI,00142$
	ljmp	00119$
00142$:
;	../src/mainBase.c:125: if( header_counter < (RF_LENGTH-1) ){
	mov	a,#0x100 - 0x1B
	add	a,_interrupt_serial_header_counter_1_20
	jc	00115$
;	../src/mainBase.c:126: if( header_counter == 3 ){
	mov	a,#0x03
	cjne	a,_interrupt_serial_header_counter_1_20,00102$
;	../src/mainBase.c:127: code_counter = SBUF;
	mov	_interrupt_serial_code_counter_1_20,_SBUF
;	../src/mainBase.c:128: code_segment = code_counter/RF_LENGTH;
	mov	b,#0x1C
	mov	a,_interrupt_serial_code_counter_1_20
	div	ab
	mov	_code_segment,a
;	../src/mainBase.c:129: MessageBUF[header_counter++] = code_counter;
	mov	r7,_interrupt_serial_header_counter_1_20
	inc	_interrupt_serial_header_counter_1_20
	mov	a,r7
	add	a,#_MessageBUF
	mov	r0,a
	mov	@r0,_interrupt_serial_code_counter_1_20
	ljmp	00119$
00102$:
;	../src/mainBase.c:132: MessageBUF[header_counter++] = SBUF;
	mov	r7,_interrupt_serial_header_counter_1_20
	inc	_interrupt_serial_header_counter_1_20
	mov	a,r7
	add	a,#_MessageBUF
	mov	r0,a
	mov	@r0,_SBUF
	ljmp	00119$
00115$:
;	../src/mainBase.c:135: else if( header_counter == (RF_LENGTH-1) ){
	mov	a,#0x1B
	cjne	a,_interrupt_serial_header_counter_1_20,00112$
;	../src/mainBase.c:136: MessageBUF[header_counter++] = SBUF;
	mov	r7,_interrupt_serial_header_counter_1_20
	inc	_interrupt_serial_header_counter_1_20
	mov	a,r7
	add	a,#_MessageBUF
	mov	r0,a
	mov	@r0,_SBUF
;	../src/mainBase.c:137: rf_send( dst_addr, 3, MessageBUF, RF_LENGTH );
	mov	_poll_rf_send_PARM_3,#_MessageBUF
	mov	(_poll_rf_send_PARM_3 + 1),#0x00
	mov	(_poll_rf_send_PARM_3 + 2),#0x40
	mov	_poll_rf_send_PARM_2,#0x03
	mov	_poll_rf_send_PARM_4,#0x1C
	mov	dptr,#_dst_addr
	mov	b,#0x40
	lcall	_poll_rf_send
;	../src/mainBase.c:140: cfg->rf_prog[1] = 0x15;
	mov	a,#0x0E
	add	a,_cfg
	mov	r5,a
	clr	a
	addc	a,(_cfg + 1)
	mov	r6,a
	mov	r7,(_cfg + 2)
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,#0x15
	lcall	__gptrput
;	../src/mainBase.c:141: rf_configure( cfg );
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	lcall	_poll_rf_configure
;	../src/mainBase.c:142: CE = 1; /* Activate RX or TX mode */
	setb	_CE
	sjmp	00119$
00112$:
;	../src/mainBase.c:156: if( code_counter % RF_LENGTH == 0 ){
	mov	b,#0x1C
	mov	a,_interrupt_serial_code_counter_1_20
	div	ab
	mov	a,b
	mov	r7,a
	jnz	00109$
;	../src/mainBase.c:157: MessageBUF[0] = SBUF;
	mov	_MessageBUF,_SBUF
;	../src/mainBase.c:158: code_counter--;
	dec	_interrupt_serial_code_counter_1_20
	sjmp	00119$
00109$:
;	../src/mainBase.c:161: MessageBUF[RF_LENGTH-(code_counter%RF_LENGTH)] = SBUF;
	mov	a,#0x1C
	clr	c
	subb	a,r7
	add	a,#_MessageBUF
	mov	r0,a
	mov	@r0,_SBUF
;	../src/mainBase.c:162: code_counter--;
	dec	_interrupt_serial_code_counter_1_20
;	../src/mainBase.c:164: if( code_counter % RF_LENGTH == 0 ){
	mov	b,#0x1C
	mov	a,_interrupt_serial_code_counter_1_20
	div	ab
	mov	a,b
;	../src/mainBase.c:165: rf_send(dst_addr, 3, MessageBUF, RF_LENGTH );
	jnz	00105$
	mov	_poll_rf_send_PARM_3,#_MessageBUF
	mov	(_poll_rf_send_PARM_3 + 1),a
	mov	(_poll_rf_send_PARM_3 + 2),#0x40
	mov	_poll_rf_send_PARM_2,#0x03
	mov	_poll_rf_send_PARM_4,#0x1C
	mov	dptr,#_dst_addr
	mov	b,#0x40
	lcall	_poll_rf_send
;	../src/mainBase.c:166: code_segment--;
	dec	_code_segment
;	../src/mainBase.c:181: cfg->rf_prog[1] = 0x15;
	mov	a,#0x0E
	add	a,_cfg
	mov	r5,a
	clr	a
	addc	a,(_cfg + 1)
	mov	r6,a
	mov	r7,(_cfg + 2)
	mov	dpl,r5
	mov	dph,r6
	mov	b,r7
	mov	a,#0x15
	lcall	__gptrput
;	../src/mainBase.c:182: rf_configure( cfg );
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	lcall	_poll_rf_configure
;	../src/mainBase.c:183: CE = 1; /* Activate RX or TX mode */
	setb	_CE
00105$:
;	../src/mainBase.c:187: if( code_counter == 0 )
	mov	a,_interrupt_serial_code_counter_1_20
;	../src/mainBase.c:188: header_counter = 0;
	jnz	00119$
	mov	_interrupt_serial_header_counter_1_20,a
00119$:
	pop	psw
	pop	(0+0)
	pop	(0+1)
	pop	(0+2)
	pop	(0+3)
	pop	(0+4)
	pop	(0+5)
	pop	(0+6)
	pop	(0+7)
	pop	dph
	pop	dpl
	pop	b
	pop	acc
	pop	bits
	reti
	.area CSEG    (CODE)
	.area CONST   (CODE)
___str_0:
	.db 0x0A
	.ascii "----------------------------"
	.db 0x00
___str_1:
	.db 0x0A
	.ascii "Startup."
	.db 0x0A
	.db 0x00
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
