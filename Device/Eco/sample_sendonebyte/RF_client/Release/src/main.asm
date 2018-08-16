;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 2.9.0 #5416 (Mar 22 2009) (MINGW32)
; This file was generated Sat Feb 15 21:01:14 2014
;--------------------------------------------------------
	.module main
	.optsdcc -mmcs51 --model-small
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _main
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
	.globl _Meassage
	.globl _HeaderFile
	.globl _codegenerator_status
	.globl _dst_addr
	.globl _cfg
	.globl _rf_data
	.globl _interrupt_rf
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
	.area RSEG    (DATA)
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
	.area RSEG    (DATA)
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
_Meassage::
	.ds 41
;--------------------------------------------------------
; overlayable items in internal ram 
;--------------------------------------------------------
	.area OSEG    (OVR,DATA)
;--------------------------------------------------------
; Stack segment in internal ram 
;--------------------------------------------------------
	.area	SSEG	(DATA)
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
;	../src/main.c:27: struct rf_config rf_data = {
	mov	_rf_data,#0x00
	mov	(_rf_data + 0x0001),#0x08
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
;	../src/main.c:34: struct rf_config *cfg = &rf_data;
	mov	_cfg,#_rf_data
	mov	(_cfg + 1),#0x00
	mov	(_cfg + 2),#0x40
;	../src/main.c:35: char dst_addr[3] = { 0x02, 0x02, 0x02 };
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
	lcall	_main
;	return from main will lock up
	sjmp .
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area CSEG    (CODE)
;------------------------------------------------------------
;Allocation info for local variables in function 'main'
;------------------------------------------------------------
;i                         Allocated to registers r2 r3 
;------------------------------------------------------------
;	../src/main.c:41: void main()
;	-----------------------------------------
;	 function main
;	-----------------------------------------
_main:
	ar2 = 0x02
	ar3 = 0x03
	ar4 = 0x04
	ar5 = 0x05
	ar6 = 0x06
	ar7 = 0x07
	ar0 = 0x00
	ar1 = 0x01
;	../src/main.c:44: store_cpu_rate(16);
	mov	dptr,#(0x10&0x00ff)
	clr	a
	mov	b,a
	lcall	_store_cpu_rate
;	../src/main.c:46: serial_init(19200);
	mov	dptr,#0x4B00
	lcall	_serial_init
;	../src/main.c:48: P0_DIR &= ~0x28;
	anl	_P0_DIR,#0xD7
;	../src/main.c:49: P0_ALT &= ~0x28;
	anl	_P0_ALT,#0xD7
;	../src/main.c:51: rf_init();
	lcall	_poll_rf_init
;	../src/main.c:52: rf_configure(cfg);
	mov	dpl,_cfg
	mov	dph,(_cfg + 1)
	mov	b,(_cfg + 2)
	lcall	_poll_rf_configure
;	../src/main.c:55: codegenerator_status = IDLE;
	mov	_codegenerator_status,#0x00
;	../src/main.c:57: EA = 1;
	setb	_EA
;	../src/main.c:58: EX4 = 1;
	setb	_EX4
;	../src/main.c:59: for(i=0;i<6;i++)
	mov	r2,#0x00
	mov	r3,#0x00
00104$:
	clr	c
	mov	a,r2
	subb	a,#0x06
	mov	a,r3
	xrl	a,#0x80
	subb	a,#0x80
	jnc	00107$
;	../src/main.c:61: blink_led();
	xrl	_P0,#0x20
;	../src/main.c:62: mdelay(500);
	mov	dptr,#0x01F4
	push	ar2
	push	ar3
	lcall	_mdelay
	pop	ar3
	pop	ar2
;	../src/main.c:59: for(i=0;i<6;i++)
	inc	r2
	cjne	r2,#0x00,00104$
	inc	r3
	sjmp	00104$
00107$:
;	../src/main.c:65: puts("Slave startup.\n\r");
	mov	dptr,#__str_0
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:66: while(1) {
00102$:
;	../src/main.c:67: CE = 1;
	setb	_CE
	sjmp	00102$
;------------------------------------------------------------
;Allocation info for local variables in function 'interrupt_rf'
;------------------------------------------------------------
;counter                   Allocated to registers r2 
;led_status                Allocated to registers 
;------------------------------------------------------------
;	../src/main.c:83: void interrupt_rf() interrupt 10
;	-----------------------------------------
;	 function interrupt_rf
;	-----------------------------------------
_interrupt_rf:
	push	bits
	push	acc
	push	b
	push	dpl
	push	dph
	push	(0+2)
	push	(0+3)
	push	(0+4)
	push	(0+5)
	push	(0+6)
	push	(0+7)
	push	(0+0)
	push	(0+1)
	push	psw
	mov	psw,#0x00
;	../src/main.c:87: blink_led();
	xrl	_P0,#0x20
;	../src/main.c:88: mdelay(500);
	mov	dptr,#0x01F4
	lcall	_mdelay
;	../src/main.c:91: while (DR1) {
	mov	r2,#0x00
00101$:
	jnb	_DR1,00103$
;	../src/main.c:92: rf_buf[counter++] = spi_write_then_read(0);	/* clock in data */
	mov	ar3,r2
	inc	r2
	mov	a,r3
	add	a,#_rf_buf
	mov	r0,a
	mov	dpl,#0x00
	push	ar2
	push	ar0
	lcall	_spi_write_then_read
	mov	a,dpl
	pop	ar0
	pop	ar2
	mov	@r0,a
	sjmp	00101$
00103$:
;	../src/main.c:95: led_status = rf_buf[0];
	mov	dpl,_rf_buf
;	../src/main.c:96: putc(led_status);
	lcall	_putc
;	../src/main.c:97: puts("\n\r");
	mov	dptr,#__str_1
	mov	b,#0x80
	lcall	_puts
;	../src/main.c:100: CE = 0;
	clr	_CE
;	../src/main.c:101: EXIF &= ~0x40;
	anl	_EXIF,#0xBF
	pop	psw
	pop	(0+1)
	pop	(0+0)
	pop	(0+7)
	pop	(0+6)
	pop	(0+5)
	pop	(0+4)
	pop	(0+3)
	pop	(0+2)
	pop	dph
	pop	dpl
	pop	b
	pop	acc
	pop	bits
	reti
	.area CSEG    (CODE)
	.area CONST   (CODE)
__str_0:
	.ascii "Slave startup."
	.db 0x0A
	.db 0x0D
	.db 0x00
__str_1:
	.db 0x0A
	.db 0x0D
	.db 0x00
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
