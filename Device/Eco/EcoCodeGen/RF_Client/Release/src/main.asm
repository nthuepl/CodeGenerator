;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.4.0/*rc1*/ #8960 (Mar 15 2014) (MINGW32)
; This file was generated Wed Mar 26 21:03:23 2014
;--------------------------------------------------------
	.module main
	.optsdcc -mmcs51 --model-small
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _main
	.globl _mdelay
	.globl _store_cpu_rate
	.globl _puts
	.globl _putc
	.globl _serial_init
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
	.globl _Message
	.globl _send_ack_feedback_PARM_2
	.globl _i
	.globl _HeaderFile
	.globl _codegenerator_status
	.globl _dst_addr
	.globl _cfg
	.globl _rf_data
	.globl _send_ack_feedback
	.globl _interrupt_rf
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
_codegenerator_status::
	.ds 1
_HeaderFile::
	.ds 4
_i::
	.ds 2
_send_ack_feedback_PARM_2:
	.ds 1
_interrupt_rf_counter_1_20:
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
_Message::
	.ds 64
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
;	../src/main.c:38: struct rf_config rf_data = {
	mov	_rf_data,#0x00
	mov	(_rf_data + 0x0001),#0xE0
	mov	(_rf_data + 0x0002),#0x00
	mov	(_rf_data + 0x0003),#0x00
	mov	(_rf_data + 0x0004),#0x00
	mov	(_rf_data + 0x0005),#0x00
	mov	(_rf_data + 0x0006),#0x00
	mov	(_rf_data + 0x0007),#0x00
	mov	(_rf_data + 0x0008),#0x00
	mov	(_rf_data + 0x0009),#0x0F
	mov	(_rf_data + 0x000a),#0x01
	mov	(_rf_data + 0x000b),#0x01
	mov	(_rf_data + 0x000c),#0x61
	mov	(_rf_data + 0x000d),#0x6F
	mov	(_rf_data + 0x000e),#0x15
;	../src/main.c:46: struct rf_config *cfg = &rf_data;
	mov	_cfg,#_rf_data
	mov	(_cfg + 1),#0x00
	mov	(_cfg + 2),#0x40
;	../src/main.c:48: char dst_addr[3] = { 0x02, 0x02, 0x02 };
	mov	_dst_addr,#0x02
	mov	(_dst_addr + 0x0001),#0x02
	mov	(_dst_addr + 0x0002),#0x02
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
;	../src/main.c:56: void main()
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
;	../src/main.c:60: store_cpu_rate(16);
	mov	dptr,#(0x10&0x00ff)
	clr	a
	mov	b,a
	lcall	_store_cpu_rate
;	../src/main.c:63: serial_init(19200);
	mov	dptr,#0x4B00
	lcall	_serial_init
;	../src/main.c:66: P0_DIR &= ~0x28;
	mov	r7,_P0_DIR
	mov	a,#0xD7
	anl	a,r7
	mov	_P0_DIR,a
;	../src/main.c:67: P0_ALT &= ~0x28;
	mov	r7,_P0_ALT
	mov	a,#0xD7
	anl	a,r7
	mov	_P0_ALT,a
;	../src/main.c:70: rf_init();
	lcall	_poll_rf_init
;	../src/main.c:71: rf_configure(cfg);
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	lcall	_poll_rf_configure
;	../src/main.c:74: EA = 1;
	setb	_EA
;	../src/main.c:77: EX4 = 1;
	setb	_EX4
;	../src/main.c:79: for(i=0;i<6;i++)
	clr	a
	mov	_i,a
	mov	(_i + 1),a
00107$:
;	../src/main.c:81: blink_led();
	xrl	_P0,#0x20
;	../src/main.c:82: mdelay(500);
	mov	dptr,#0x01F4
	lcall	_mdelay
;	../src/main.c:79: for(i=0;i<6;i++)
	inc	_i
	clr	a
	cjne	a,_i,00123$
	inc	(_i + 1)
00123$:
	clr	c
	mov	a,_i
	subb	a,#0x06
	mov	a,(_i + 1)
	xrl	a,#0x80
	subb	a,#0x80
	jc	00107$
;	../src/main.c:85: puts("\n----------------------------");
	mov	dptr,#___str_0
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:87: codegenerator_status = IDLE;
	mov	_codegenerator_status,#0x00
;	../src/main.c:88: puts( "\n>Idle\n" );
	mov	dptr,#___str_1
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:90: while(1) {
00105$:
;	../src/main.c:91: CE = 1; /* Activate RX or TX mode */
	setb	_CE
;	../src/main.c:93: if( codegenerator_status == RUNCODE ){
	mov	a,#0x04
	cjne	a,_codegenerator_status,00105$
;	../src/main.c:95: puts("Exec\n");
	mov	dptr,#___str_2
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:98: __endasm ;
	lcall #_Message
;	../src/main.c:99: puts("ret\n");
	mov	dptr,#___str_3
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:101: send_ack_feedback( Message, 1);
	mov	_send_ack_feedback_PARM_2,#0x01
	mov	dptr,#_Message
	mov	b,#0x00
	lcall	_send_ack_feedback
;	../src/main.c:120: codegenerator_status = IDLE;
	mov	_codegenerator_status,#0x00
;	../src/main.c:121: puts("\n----------------------------");
	mov	dptr,#___str_0
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:122: puts( "\n>Idle\n" );
	mov	dptr,#___str_1
	mov	b,#0x80
	lcall	_puts
	sjmp	00105$
;------------------------------------------------------------
;Allocation info for local variables in function 'send_ack_feedback'
;------------------------------------------------------------
;event                     Allocated with name '_send_ack_feedback_PARM_2'
;buf                       Allocated to registers r5 r6 r7 
;------------------------------------------------------------
;	../src/main.c:127: void send_ack_feedback( unsigned char *buf, unsigned char event )
;	-----------------------------------------
;	 function send_ack_feedback
;	-----------------------------------------
_send_ack_feedback:
	mov	r5,dpl
	mov	r6,dph
	mov	r7,b
;	../src/main.c:130: cfg->rf_prog[1] = 0x14;
	mov	a,#0x0E
	add	a,_cfg
	mov	r2,a
	clr	a
	addc	a,(_cfg + 1)
	mov	r3,a
	mov	r4,(_cfg + 2)
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	mov	a,#0x14
	lcall	__gptrput
;	../src/main.c:131: rf_configure( cfg );
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	push	ar7
	push	ar6
	push	ar5
	lcall	_poll_rf_configure
;	../src/main.c:134: mdelay(700);	/* wait for dongle */
	mov	dptr,#0x02BC
	lcall	_mdelay
	pop	ar5
	pop	ar6
	pop	ar7
;	../src/main.c:135: rf_send(dst_addr, 3, buf, RF_LENGTH );
	mov	_poll_rf_send_PARM_2,#0x03
	mov	_poll_rf_send_PARM_3,r5
	mov	(_poll_rf_send_PARM_3 + 1),r6
	mov	(_poll_rf_send_PARM_3 + 2),r7
	mov	_poll_rf_send_PARM_4,#0x1C
	mov	dptr,#_dst_addr
	mov	b,#0x40
	push	ar7
	push	ar6
	push	ar5
	lcall	_poll_rf_send
	pop	ar5
	pop	ar6
	pop	ar7
;	../src/main.c:136: if( event == 0 )
	mov	a,_send_ack_feedback_PARM_2
	jnz	00102$
;	../src/main.c:137: puts("send ack: \n");
	mov	dptr,#___str_4
	mov	b,#0x80
	push	ar7
	push	ar6
	push	ar5
	lcall	_puts
	pop	ar5
	pop	ar6
	pop	ar7
	sjmp	00103$
00102$:
;	../src/main.c:139: puts("send result: \n");
	mov	dptr,#___str_5
	mov	b,#0x80
	push	ar7
	push	ar6
	push	ar5
	lcall	_puts
	pop	ar5
	pop	ar6
	pop	ar7
00103$:
;	../src/main.c:141: for( i = 0; i < RF_LENGTH; i++ ){
	clr	a
	mov	_i,a
	mov	(_i + 1),a
00105$:
;	../src/main.c:142: putc( ( (buf[i]>>4) & 0x0f ) > 9 ? ( (buf[i]>>4) & 0xff )+ 55 :( (buf[i]>>4) & 0xff )+ 48 );
	mov	a,_i
	add	a,r5
	mov	r2,a
	mov	a,(_i + 1)
	addc	a,r6
	mov	r3,a
	mov	ar4,r7
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	lcall	__gptrget
	mov	r2,a
	swap	a
	anl	a,#0x0F
	mov	r4,a
	mov	a,#0x0F
	anl	a,r4
	mov  r3,a
	add	a,#0xff - 0x09
	jnc	00109$
	mov	a,#0x37
	add	a,r4
	mov	r3,a
	sjmp	00110$
00109$:
	mov	a,#0x30
	add	a,r4
	mov	r3,a
00110$:
	mov	dpl,r3
	push	ar7
	push	ar6
	push	ar5
	lcall	_putc
	pop	ar5
	pop	ar6
	pop	ar7
;	../src/main.c:143: putc( ( buf[i] & 0x0f ) > 9 ? ( buf[i] & 0x0f ) + 55  : ( buf[i] & 0x0f ) + 48 );
	mov	a,_i
	add	a,r5
	mov	r2,a
	mov	a,(_i + 1)
	addc	a,r6
	mov	r3,a
	mov	ar4,r7
	mov	dpl,r2
	mov	dph,r3
	mov	b,r4
	lcall	__gptrget
	mov	r4,a
	mov	a,#0x0F
	anl	a,r4
	mov  r3,a
	add	a,#0xff - 0x09
	jnc	00111$
	mov	a,#0x0F
	anl	a,r4
	add	a,#0x37
	mov	r3,a
	sjmp	00112$
00111$:
	mov	a,#0x0F
	anl	a,r4
	add	a,#0x30
	mov	r3,a
00112$:
	mov	dpl,r3
	push	ar7
	push	ar6
	push	ar5
	lcall	_putc
;	../src/main.c:144: putc( ' ' );
	mov	dpl,#0x20
	lcall	_putc
	pop	ar5
	pop	ar6
	pop	ar7
;	../src/main.c:141: for( i = 0; i < RF_LENGTH; i++ ){
	inc	_i
	clr	a
	cjne	a,_i,00131$
	inc	(_i + 1)
00131$:
	clr	c
	mov	a,_i
	subb	a,#0x1C
	mov	a,(_i + 1)
	xrl	a,#0x80
	subb	a,#0x80
	jnc	00132$
	ljmp	00105$
00132$:
;	../src/main.c:147: cfg->rf_prog[1] = 0x15;
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
;	../src/main.c:148: rf_configure( cfg );
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	ljmp	_poll_rf_configure
;------------------------------------------------------------
;Allocation info for local variables in function 'interrupt_rf'
;------------------------------------------------------------
;counter                   Allocated with name '_interrupt_rf_counter_1_20'
;------------------------------------------------------------
;	../src/main.c:152: void interrupt_rf() __interrupt 10
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
;	../src/main.c:156: while (DR1) {
00118$:
	jb	_DR1,00173$
	ljmp	00120$
00173$:
;	../src/main.c:157: switch( codegenerator_status ){
	clr	a
	cjne	a,_codegenerator_status,00174$
	sjmp	00101$
00174$:
	mov	a,#0x01
	cjne	a,_codegenerator_status,00175$
	sjmp	00102$
00175$:
	mov	a,#0x02
	cjne	a,_codegenerator_status,00176$
	ljmp	00109$
00176$:
;	../src/main.c:158: case IDLE:
	sjmp	00118$
00101$:
;	../src/main.c:159: counter=0;
	mov	_interrupt_rf_counter_1_20,#0x00
;	../src/main.c:160: codegenerator_status = HEADERPACKET;
	mov	_codegenerator_status,#0x01
;	../src/main.c:161: puts("\n>Header Packet\n");
	mov	dptr,#___str_6
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:162: case HEADERPACKET:
00102$:
;	../src/main.c:163: if( counter < 4 ){ 		/* header buffer length 4 bytes */
	mov	a,#0x100 - 0x04
	add	a,_interrupt_rf_counter_1_20
	jnc	00177$
	ljmp	00107$
00177$:
;	../src/main.c:164: HeaderFile[counter++] = spi_write_then_read(0);
	mov	r7,_interrupt_rf_counter_1_20
	inc	_interrupt_rf_counter_1_20
	mov	a,r7
	add	a,#_HeaderFile
	mov	r1,a
	mov	dpl,#0x00
	push	ar1
	lcall	_spi_write_then_read
	mov	a,dpl
	pop	ar1
	mov	@r1,a
;	../src/main.c:165: putc( ( (HeaderFile[counter-1]>>4) & 0x0f ) > 9 ? ( (HeaderFile[counter-1]>>4) & 0xff )+ 55 :( (HeaderFile[counter-1]>>4) & 0xff )+ 48 );
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_HeaderFile
	mov	r1,a
	mov	a,@r1
	swap	a
	anl	a,#(0x0F&0x0F)
	mov	r7,a
	add	a,#0xff - 0x09
	jnc	00123$
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_HeaderFile
	mov	r1,a
	mov	a,@r1
	swap	a
	anl	a,#0x0F
	add	a,#0x37
	mov	r7,a
	sjmp	00124$
00123$:
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_HeaderFile
	mov	r1,a
	mov	a,@r1
	swap	a
	anl	a,#0x0F
	mov	r6,a
	add	a,#0x30
	mov	r7,a
00124$:
	mov	dpl,r7
	lcall	_putc
;	../src/main.c:166: putc( ( HeaderFile[counter-1] & 0x0f ) > 9 ? ( HeaderFile[counter-1] & 0x0f ) + 55  : ( HeaderFile[counter-1] & 0x0f ) + 48 );
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_HeaderFile
	mov	r1,a
	mov	ar7,@r1
	anl	ar7,#0x0F
	mov	a,r7
	add	a,#0xff - 0x09
	jnc	00125$
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_HeaderFile
	mov	r1,a
	mov	ar7,@r1
	mov	a,#0x0F
	anl	a,r7
	add	a,#0x37
	mov	r7,a
	sjmp	00126$
00125$:
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_HeaderFile
	mov	r1,a
	mov	ar6,@r1
	mov	a,#0x0F
	anl	a,r6
	add	a,#0x30
	mov	r7,a
00126$:
	mov	dpl,r7
	lcall	_putc
;	../src/main.c:167: putc( ' ' );
	mov	dpl,#0x20
	lcall	_putc
	ljmp	00118$
00107$:
;	../src/main.c:169: else if( counter < RF_LENGTH ){
	mov	a,#0x100 - 0x1C
	add	a,_interrupt_rf_counter_1_20
	jc	00104$
;	../src/main.c:170: spi_write_then_read(0);
	mov	dpl,#0x00
	lcall	_spi_write_then_read
;	../src/main.c:171: counter++;
	inc	_interrupt_rf_counter_1_20
	ljmp	00118$
00104$:
;	../src/main.c:174: counter = 0;
	mov	_interrupt_rf_counter_1_20,#0x00
;	../src/main.c:175: send_ack_feedback( HeaderFile, 0 );
	mov	_send_ack_feedback_PARM_2,#0x00
	mov	dptr,#_HeaderFile
	mov	b,#0x40
	lcall	_send_ack_feedback
;	../src/main.c:176: codegenerator_status = CODEPACKET;
	mov	_codegenerator_status,#0x02
;	../src/main.c:177: puts("\n\r>Code Packet\n");
	mov	dptr,#___str_7
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:179: break;
	ljmp	00118$
;	../src/main.c:180: case CODEPACKET:
00109$:
;	../src/main.c:181: if( counter < HeaderFile[3] ){
	clr	c
	mov	a,_interrupt_rf_counter_1_20
	subb	a,(_HeaderFile + 0x0003)
	jc	00181$
	ljmp	00118$
00181$:
;	../src/main.c:182: Message[counter++] = spi_write_then_read(0);
	mov	r7,_interrupt_rf_counter_1_20
	inc	_interrupt_rf_counter_1_20
	mov	a,r7
	add	a,#_Message
	mov	r7,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	r6,a
	mov	dpl,#0x00
	push	ar7
	push	ar6
	lcall	_spi_write_then_read
	mov	r5,dpl
	pop	ar6
	pop	ar7
	mov	dpl,r7
	mov	dph,r6
	mov	a,r5
	movx	@dptr,a
;	../src/main.c:183: putc( ( (Message[counter-1]>>4) & 0x0f ) > 9 ? ( (Message[counter-1]>>4) & 0xff )+ 55 :( (Message[counter-1]>>4) & 0xff )+ 48 );
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_Message
	mov	dpl,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	dph,a
	movx	a,@dptr
	swap	a
	anl	a,#(0x0F&0x0F)
	mov	r7,a
	add	a,#0xff - 0x09
	jnc	00127$
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_Message
	mov	dpl,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	dph,a
	movx	a,@dptr
	swap	a
	anl	a,#0x0F
	add	a,#0x37
	mov	r7,a
	sjmp	00128$
00127$:
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_Message
	mov	dpl,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	dph,a
	movx	a,@dptr
	swap	a
	anl	a,#0x0F
	mov	r6,a
	add	a,#0x30
	mov	r7,a
00128$:
	mov	dpl,r7
	lcall	_putc
;	../src/main.c:184: putc( ( Message[counter-1] & 0x0f ) > 9 ? ( Message[counter-1] & 0x0f ) + 55  : ( Message[counter-1] & 0x0f ) + 48 );
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_Message
	mov	dpl,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	dph,a
	movx	a,@dptr
	anl	a,#0x0F
	mov	r7,a
	add	a,#0xff - 0x09
	jnc	00129$
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_Message
	mov	dpl,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	dph,a
	movx	a,@dptr
	mov	r7,a
	mov	a,#0x0F
	anl	a,r7
	add	a,#0x37
	mov	r7,a
	sjmp	00130$
00129$:
	mov	a,_interrupt_rf_counter_1_20
	dec	a
	add	a,#_Message
	mov	dpl,a
	clr	a
	addc	a,#(_Message >> 8)
	mov	dph,a
	movx	a,@dptr
	mov	r6,a
	mov	a,#0x0F
	anl	a,r6
	add	a,#0x30
	mov	r7,a
00130$:
	mov	dpl,r7
	lcall	_putc
;	../src/main.c:185: putc( ' ' );
	mov	dpl,#0x20
	lcall	_putc
;	../src/main.c:187: if( ( counter % RF_LENGTH == 0) ){
	mov	b,#0x1C
	mov	a,_interrupt_rf_counter_1_20
	div	ab
	mov	a,b
	jz	00184$
	ljmp	00118$
00184$:
;	../src/main.c:188: if( (counter / RF_LENGTH) != HeaderFile[2] ){
	mov	b,#0x1C
	mov	a,_interrupt_rf_counter_1_20
	div	ab
	mov	r7,a
	cjne	a,(_HeaderFile + 0x0002),00185$
	sjmp	00111$
00185$:
;	../src/main.c:189: send_ack_feedback( Message, 0 );
	mov	_send_ack_feedback_PARM_2,#0x00
	mov	dptr,#_Message
	mov	b,#0x00
	lcall	_send_ack_feedback
	ljmp	00118$
00111$:
;	../src/main.c:208: codegenerator_status = RUNCODE;
	mov	_codegenerator_status,#0x04
;	../src/main.c:209: puts("\n\r>Run Code\n");
	mov	dptr,#___str_8
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:214: } /* end switch case */
	ljmp	00118$
00120$:
;	../src/main.c:218: CE = 0;
	clr	_CE
;	../src/main.c:219: EXIF &= ~0x40;
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
	.area CSEG    (CODE)
	.area CONST   (CODE)
___str_0:
	.db 0x0A
	.ascii "----------------------------"
	.db 0x00
___str_1:
	.db 0x0A
	.ascii ">Idle"
	.db 0x0A
	.db 0x00
___str_2:
	.ascii "Exec"
	.db 0x0A
	.db 0x00
___str_3:
	.ascii "ret"
	.db 0x0A
	.db 0x00
___str_4:
	.ascii "send ack: "
	.db 0x0A
	.db 0x00
___str_5:
	.ascii "send result: "
	.db 0x0A
	.db 0x00
___str_6:
	.db 0x0A
	.ascii ">Header Packet"
	.db 0x0A
	.db 0x00
___str_7:
	.db 0x0A
	.db 0x0D
	.ascii ">Code Packet"
	.db 0x0A
	.db 0x00
___str_8:
	.db 0x0A
	.db 0x0D
	.ascii ">Run Code"
	.db 0x0A
	.db 0x00
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
