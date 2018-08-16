                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ANSI-C Compiler
                                      3 ; Version 3.4.0/*rc1*/ #8960 (Mar 15 2014) (MINGW32)
                                      4 ; This file was generated Wed Mar 26 21:02:59 2014
                                      5 ;--------------------------------------------------------
                                      6 	.module mainBase
                                      7 	.optsdcc -mmcs51 --model-small
                                      8 	
                                      9 ;--------------------------------------------------------
                                     10 ; Public variables in this module
                                     11 ;--------------------------------------------------------
                                     12 	.globl _main
                                     13 	.globl _putc
                                     14 	.globl _puts
                                     15 	.globl _serial_init
                                     16 	.globl _mdelay
                                     17 	.globl _store_cpu_rate
                                     18 	.globl _spi_write_then_read
                                     19 	.globl _poll_rf_send
                                     20 	.globl _poll_rf_configure
                                     21 	.globl _poll_rf_init
                                     22 	.globl _PWDI
                                     23 	.globl _PX5
                                     24 	.globl _PX4
                                     25 	.globl _PX3
                                     26 	.globl _PX2
                                     27 	.globl _EWDI
                                     28 	.globl _EX5
                                     29 	.globl _EX4
                                     30 	.globl _EX3
                                     31 	.globl _EX2
                                     32 	.globl _WDTI
                                     33 	.globl _CY
                                     34 	.globl _AC
                                     35 	.globl _F0
                                     36 	.globl _RS1
                                     37 	.globl _RS0
                                     38 	.globl _OV
                                     39 	.globl _F1
                                     40 	.globl _P
                                     41 	.globl _TF2
                                     42 	.globl _EXF2
                                     43 	.globl _RCLK
                                     44 	.globl _TCLK
                                     45 	.globl _EXEN2
                                     46 	.globl _TR2
                                     47 	.globl _CT2
                                     48 	.globl _C_T2
                                     49 	.globl _CPRL2
                                     50 	.globl _CP_RL2
                                     51 	.globl _PT2
                                     52 	.globl _PS
                                     53 	.globl _PT1
                                     54 	.globl _PX1
                                     55 	.globl _PT0
                                     56 	.globl _PX0
                                     57 	.globl _EA
                                     58 	.globl _ET2
                                     59 	.globl _ES
                                     60 	.globl _ET1
                                     61 	.globl _EX1
                                     62 	.globl _ET0
                                     63 	.globl _EX0
                                     64 	.globl _PWR_UP
                                     65 	.globl _CE
                                     66 	.globl _DR2
                                     67 	.globl _DR2_CE
                                     68 	.globl _CLK2
                                     69 	.globl _DOUT2
                                     70 	.globl _CS
                                     71 	.globl _DR1
                                     72 	.globl _CLK1
                                     73 	.globl _DATA
                                     74 	.globl _SM0
                                     75 	.globl _SM1
                                     76 	.globl _SM2
                                     77 	.globl _REN
                                     78 	.globl _TB8
                                     79 	.globl _RB8
                                     80 	.globl _TI
                                     81 	.globl _RI
                                     82 	.globl _DIN0
                                     83 	.globl _P1_2
                                     84 	.globl _DIO1
                                     85 	.globl _P1_1
                                     86 	.globl _DIO0
                                     87 	.globl _T2
                                     88 	.globl _P1_0
                                     89 	.globl _TF1
                                     90 	.globl _TR1
                                     91 	.globl _TF0
                                     92 	.globl _TR0
                                     93 	.globl _IE1
                                     94 	.globl _IT1
                                     95 	.globl _IE0
                                     96 	.globl _IT0
                                     97 	.globl _DIO9
                                     98 	.globl _PWM
                                     99 	.globl _P0_7
                                    100 	.globl _DIO8
                                    101 	.globl _T1
                                    102 	.globl _P0_6
                                    103 	.globl _DIO7
                                    104 	.globl _T0
                                    105 	.globl _P0_5
                                    106 	.globl _DIO6
                                    107 	.globl _INT1_N
                                    108 	.globl _P0_4
                                    109 	.globl _DIO5
                                    110 	.globl _INT0_N
                                    111 	.globl _P0_3
                                    112 	.globl _DIO4
                                    113 	.globl _TXD
                                    114 	.globl _P0_2
                                    115 	.globl _DIO3
                                    116 	.globl _RXD
                                    117 	.globl _P0_1
                                    118 	.globl _DIO2
                                    119 	.globl _P0_0
                                    120 	.globl _EIP
                                    121 	.globl _B
                                    122 	.globl _EIE
                                    123 	.globl _ACC
                                    124 	.globl _EICON
                                    125 	.globl _PSW
                                    126 	.globl _TH2
                                    127 	.globl _TL2
                                    128 	.globl _RCAP2H
                                    129 	.globl _RCAP2L
                                    130 	.globl _T2CON
                                    131 	.globl _DEV_OFFSET
                                    132 	.globl _T2_1V2
                                    133 	.globl _T1_1V2
                                    134 	.globl _IP
                                    135 	.globl _TEST_MODE
                                    136 	.globl _CK_CTRL
                                    137 	.globl _TICK_DV
                                    138 	.globl _SPICLK
                                    139 	.globl _SPI_CTRL
                                    140 	.globl _SPI_DATA
                                    141 	.globl _RSTREAS
                                    142 	.globl _REGX_CTRL
                                    143 	.globl _REGX_LSB
                                    144 	.globl _REGX_MSB
                                    145 	.globl _PWMDUTY
                                    146 	.globl _PWMCON
                                    147 	.globl _IE
                                    148 	.globl _ADCSTATIC
                                    149 	.globl _ADCDATAL
                                    150 	.globl _ADCDATAH
                                    151 	.globl _ADCCON
                                    152 	.globl _RADIO
                                    153 	.globl _SBUF
                                    154 	.globl _SCON
                                    155 	.globl _P1_ALT
                                    156 	.globl _P1_DIR
                                    157 	.globl _P0_ALT
                                    158 	.globl _P0_DIR
                                    159 	.globl _MPAGE
                                    160 	.globl _EXIF
                                    161 	.globl _P1
                                    162 	.globl _SPC_FNC
                                    163 	.globl _CKCON
                                    164 	.globl _TH1
                                    165 	.globl _TH0
                                    166 	.globl _TL1
                                    167 	.globl _TL0
                                    168 	.globl _TMOD
                                    169 	.globl _TCON
                                    170 	.globl _PCON
                                    171 	.globl _DPS
                                    172 	.globl _DPH1
                                    173 	.globl _DPL1
                                    174 	.globl _DPH0
                                    175 	.globl _DPH
                                    176 	.globl _DPL0
                                    177 	.globl _DPL
                                    178 	.globl _SP
                                    179 	.globl _P0
                                    180 	.globl _counter
                                    181 	.globl _i
                                    182 	.globl _code_segment
                                    183 	.globl _MessageBUF
                                    184 	.globl _dst_addr
                                    185 	.globl _cfg
                                    186 	.globl _rf_data
                                    187 	.globl _interrupt_rf
                                    188 	.globl _interrupt_serial
                                    189 ;--------------------------------------------------------
                                    190 ; special function registers
                                    191 ;--------------------------------------------------------
                                    192 	.area RSEG    (ABS,DATA)
      000000                        193 	.org 0x0000
                           000080   194 _P0	=	0x0080
                           000081   195 _SP	=	0x0081
                           000082   196 _DPL	=	0x0082
                           000082   197 _DPL0	=	0x0082
                           000083   198 _DPH	=	0x0083
                           000083   199 _DPH0	=	0x0083
                           000084   200 _DPL1	=	0x0084
                           000085   201 _DPH1	=	0x0085
                           000086   202 _DPS	=	0x0086
                           000087   203 _PCON	=	0x0087
                           000088   204 _TCON	=	0x0088
                           000089   205 _TMOD	=	0x0089
                           00008A   206 _TL0	=	0x008a
                           00008B   207 _TL1	=	0x008b
                           00008C   208 _TH0	=	0x008c
                           00008D   209 _TH1	=	0x008d
                           00008E   210 _CKCON	=	0x008e
                           00008F   211 _SPC_FNC	=	0x008f
                           000090   212 _P1	=	0x0090
                           000091   213 _EXIF	=	0x0091
                           000092   214 _MPAGE	=	0x0092
                           000094   215 _P0_DIR	=	0x0094
                           000095   216 _P0_ALT	=	0x0095
                           000096   217 _P1_DIR	=	0x0096
                           000097   218 _P1_ALT	=	0x0097
                           000098   219 _SCON	=	0x0098
                           000099   220 _SBUF	=	0x0099
                           0000A0   221 _RADIO	=	0x00a0
                           0000A1   222 _ADCCON	=	0x00a1
                           0000A2   223 _ADCDATAH	=	0x00a2
                           0000A3   224 _ADCDATAL	=	0x00a3
                           0000A4   225 _ADCSTATIC	=	0x00a4
                           0000A8   226 _IE	=	0x00a8
                           0000A9   227 _PWMCON	=	0x00a9
                           0000AA   228 _PWMDUTY	=	0x00aa
                           0000AB   229 _REGX_MSB	=	0x00ab
                           0000AC   230 _REGX_LSB	=	0x00ac
                           0000AD   231 _REGX_CTRL	=	0x00ad
                           0000B1   232 _RSTREAS	=	0x00b1
                           0000B2   233 _SPI_DATA	=	0x00b2
                           0000B3   234 _SPI_CTRL	=	0x00b3
                           0000B4   235 _SPICLK	=	0x00b4
                           0000B5   236 _TICK_DV	=	0x00b5
                           0000B6   237 _CK_CTRL	=	0x00b6
                           0000B7   238 _TEST_MODE	=	0x00b7
                           0000B8   239 _IP	=	0x00b8
                           0000BC   240 _T1_1V2	=	0x00bc
                           0000BD   241 _T2_1V2	=	0x00bd
                           0000BE   242 _DEV_OFFSET	=	0x00be
                           0000C8   243 _T2CON	=	0x00c8
                           0000CA   244 _RCAP2L	=	0x00ca
                           0000CB   245 _RCAP2H	=	0x00cb
                           0000CC   246 _TL2	=	0x00cc
                           0000CD   247 _TH2	=	0x00cd
                           0000D0   248 _PSW	=	0x00d0
                           0000D8   249 _EICON	=	0x00d8
                           0000E0   250 _ACC	=	0x00e0
                           0000E8   251 _EIE	=	0x00e8
                           0000F0   252 _B	=	0x00f0
                           0000F8   253 _EIP	=	0x00f8
                                    254 ;--------------------------------------------------------
                                    255 ; special function bits
                                    256 ;--------------------------------------------------------
                                    257 	.area RSEG    (ABS,DATA)
      000000                        258 	.org 0x0000
                           000080   259 _P0_0	=	0x0080
                           000080   260 _DIO2	=	0x0080
                           000081   261 _P0_1	=	0x0081
                           000081   262 _RXD	=	0x0081
                           000081   263 _DIO3	=	0x0081
                           000082   264 _P0_2	=	0x0082
                           000082   265 _TXD	=	0x0082
                           000082   266 _DIO4	=	0x0082
                           000083   267 _P0_3	=	0x0083
                           000083   268 _INT0_N	=	0x0083
                           000083   269 _DIO5	=	0x0083
                           000084   270 _P0_4	=	0x0084
                           000084   271 _INT1_N	=	0x0084
                           000084   272 _DIO6	=	0x0084
                           000085   273 _P0_5	=	0x0085
                           000085   274 _T0	=	0x0085
                           000085   275 _DIO7	=	0x0085
                           000086   276 _P0_6	=	0x0086
                           000086   277 _T1	=	0x0086
                           000086   278 _DIO8	=	0x0086
                           000087   279 _P0_7	=	0x0087
                           000087   280 _PWM	=	0x0087
                           000087   281 _DIO9	=	0x0087
                           000088   282 _IT0	=	0x0088
                           000089   283 _IE0	=	0x0089
                           00008A   284 _IT1	=	0x008a
                           00008B   285 _IE1	=	0x008b
                           00008C   286 _TR0	=	0x008c
                           00008D   287 _TF0	=	0x008d
                           00008E   288 _TR1	=	0x008e
                           00008F   289 _TF1	=	0x008f
                           000090   290 _P1_0	=	0x0090
                           000090   291 _T2	=	0x0090
                           000090   292 _DIO0	=	0x0090
                           000091   293 _P1_1	=	0x0091
                           000091   294 _DIO1	=	0x0091
                           000092   295 _P1_2	=	0x0092
                           000092   296 _DIN0	=	0x0092
                           000098   297 _RI	=	0x0098
                           000099   298 _TI	=	0x0099
                           00009A   299 _RB8	=	0x009a
                           00009B   300 _TB8	=	0x009b
                           00009C   301 _REN	=	0x009c
                           00009D   302 _SM2	=	0x009d
                           00009E   303 _SM1	=	0x009e
                           00009F   304 _SM0	=	0x009f
                           0000A0   305 _DATA	=	0x00a0
                           0000A1   306 _CLK1	=	0x00a1
                           0000A2   307 _DR1	=	0x00a2
                           0000A3   308 _CS	=	0x00a3
                           0000A4   309 _DOUT2	=	0x00a4
                           0000A5   310 _CLK2	=	0x00a5
                           0000A6   311 _DR2_CE	=	0x00a6
                           0000A6   312 _DR2	=	0x00a6
                           0000A6   313 _CE	=	0x00a6
                           0000A7   314 _PWR_UP	=	0x00a7
                           0000A8   315 _EX0	=	0x00a8
                           0000A9   316 _ET0	=	0x00a9
                           0000AA   317 _EX1	=	0x00aa
                           0000AB   318 _ET1	=	0x00ab
                           0000AC   319 _ES	=	0x00ac
                           0000AD   320 _ET2	=	0x00ad
                           0000AF   321 _EA	=	0x00af
                           0000B8   322 _PX0	=	0x00b8
                           0000B9   323 _PT0	=	0x00b9
                           0000BA   324 _PX1	=	0x00ba
                           0000BB   325 _PT1	=	0x00bb
                           0000BC   326 _PS	=	0x00bc
                           0000BD   327 _PT2	=	0x00bd
                           0000C8   328 _CP_RL2	=	0x00c8
                           0000C8   329 _CPRL2	=	0x00c8
                           0000C9   330 _C_T2	=	0x00c9
                           0000C9   331 _CT2	=	0x00c9
                           0000CA   332 _TR2	=	0x00ca
                           0000CB   333 _EXEN2	=	0x00cb
                           0000CC   334 _TCLK	=	0x00cc
                           0000CD   335 _RCLK	=	0x00cd
                           0000CE   336 _EXF2	=	0x00ce
                           0000CF   337 _TF2	=	0x00cf
                           0000D0   338 _P	=	0x00d0
                           0000D1   339 _F1	=	0x00d1
                           0000D2   340 _OV	=	0x00d2
                           0000D3   341 _RS0	=	0x00d3
                           0000D4   342 _RS1	=	0x00d4
                           0000D5   343 _F0	=	0x00d5
                           0000D6   344 _AC	=	0x00d6
                           0000D7   345 _CY	=	0x00d7
                           0000DB   346 _WDTI	=	0x00db
                           0000E8   347 _EX2	=	0x00e8
                           0000E9   348 _EX3	=	0x00e9
                           0000EA   349 _EX4	=	0x00ea
                           0000EB   350 _EX5	=	0x00eb
                           0000EC   351 _EWDI	=	0x00ec
                           0000F8   352 _PX2	=	0x00f8
                           0000F9   353 _PX3	=	0x00f9
                           0000FA   354 _PX4	=	0x00fa
                           0000FB   355 _PX5	=	0x00fb
                           0000FC   356 _PWDI	=	0x00fc
                                    357 ;--------------------------------------------------------
                                    358 ; overlayable register banks
                                    359 ;--------------------------------------------------------
                                    360 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        361 	.ds 8
                                    362 ;--------------------------------------------------------
                                    363 ; overlayable bit register bank
                                    364 ;--------------------------------------------------------
                                    365 	.area BIT_BANK	(REL,OVR,DATA)
      000020                        366 bits:
      000020                        367 	.ds 1
                           008000   368 	b0 = bits[0]
                           008100   369 	b1 = bits[1]
                           008200   370 	b2 = bits[2]
                           008300   371 	b3 = bits[3]
                           008400   372 	b4 = bits[4]
                           008500   373 	b5 = bits[5]
                           008600   374 	b6 = bits[6]
                           008700   375 	b7 = bits[7]
                                    376 ;--------------------------------------------------------
                                    377 ; internal ram data
                                    378 ;--------------------------------------------------------
                                    379 	.area DSEG    (DATA)
      000021                        380 _rf_data::
      000021                        381 	.ds 15
      000030                        382 _cfg::
      000030                        383 	.ds 3
      000033                        384 _dst_addr::
      000033                        385 	.ds 3
      000036                        386 _MessageBUF::
      000036                        387 	.ds 28
      000052                        388 _code_segment::
      000052                        389 	.ds 1
      000053                        390 _i::
      000053                        391 	.ds 1
      000054                        392 _counter::
      000054                        393 	.ds 1
      000055                        394 _interrupt_rf_fb_counter_1_17:
      000055                        395 	.ds 1
      000056                        396 _interrupt_serial_header_counter_1_20:
      000056                        397 	.ds 1
      000057                        398 _interrupt_serial_code_counter_1_20:
      000057                        399 	.ds 1
                                    400 ;--------------------------------------------------------
                                    401 ; overlayable items in internal ram 
                                    402 ;--------------------------------------------------------
                                    403 ;--------------------------------------------------------
                                    404 ; Stack segment in internal ram 
                                    405 ;--------------------------------------------------------
                                    406 	.area	SSEG
      000074                        407 __start__stack:
      000074                        408 	.ds	1
                                    409 
                                    410 ;--------------------------------------------------------
                                    411 ; indirectly addressable internal ram data
                                    412 ;--------------------------------------------------------
                                    413 	.area ISEG    (DATA)
                                    414 ;--------------------------------------------------------
                                    415 ; absolute internal ram data
                                    416 ;--------------------------------------------------------
                                    417 	.area IABS    (ABS,DATA)
                                    418 	.area IABS    (ABS,DATA)
                                    419 ;--------------------------------------------------------
                                    420 ; bit data
                                    421 ;--------------------------------------------------------
                                    422 	.area BSEG    (BIT)
                                    423 ;--------------------------------------------------------
                                    424 ; paged external ram data
                                    425 ;--------------------------------------------------------
                                    426 	.area PSEG    (PAG,XDATA)
                                    427 ;--------------------------------------------------------
                                    428 ; external ram data
                                    429 ;--------------------------------------------------------
                                    430 	.area XSEG    (XDATA)
                                    431 ;--------------------------------------------------------
                                    432 ; absolute external ram data
                                    433 ;--------------------------------------------------------
                                    434 	.area XABS    (ABS,XDATA)
                                    435 ;--------------------------------------------------------
                                    436 ; external initialized ram data
                                    437 ;--------------------------------------------------------
                                    438 	.area XISEG   (XDATA)
                                    439 	.area HOME    (CODE)
                                    440 	.area GSINIT0 (CODE)
                                    441 	.area GSINIT1 (CODE)
                                    442 	.area GSINIT2 (CODE)
                                    443 	.area GSINIT3 (CODE)
                                    444 	.area GSINIT4 (CODE)
                                    445 	.area GSINIT5 (CODE)
                                    446 	.area GSINIT  (CODE)
                                    447 	.area GSFINAL (CODE)
                                    448 	.area CSEG    (CODE)
                                    449 ;--------------------------------------------------------
                                    450 ; interrupt vector 
                                    451 ;--------------------------------------------------------
                                    452 	.area HOME    (CODE)
      000000                        453 __interrupt_vect:
      000000 02 00 59         [24]  454 	ljmp	__sdcc_gsinit_startup
      000003 32               [24]  455 	reti
      000004                        456 	.ds	7
      00000B 32               [24]  457 	reti
      00000C                        458 	.ds	7
      000013 32               [24]  459 	reti
      000014                        460 	.ds	7
      00001B 32               [24]  461 	reti
      00001C                        462 	.ds	7
      000023 02 01 EB         [24]  463 	ljmp	_interrupt_serial
      000026                        464 	.ds	5
      00002B 32               [24]  465 	reti
      00002C                        466 	.ds	7
      000033 32               [24]  467 	reti
      000034                        468 	.ds	7
      00003B 32               [24]  469 	reti
      00003C                        470 	.ds	7
      000043 32               [24]  471 	reti
      000044                        472 	.ds	7
      00004B 32               [24]  473 	reti
      00004C                        474 	.ds	7
      000053 02 01 57         [24]  475 	ljmp	_interrupt_rf
                                    476 ;--------------------------------------------------------
                                    477 ; global & static initialisations
                                    478 ;--------------------------------------------------------
                                    479 	.area HOME    (CODE)
                                    480 	.area GSINIT  (CODE)
                                    481 	.area GSFINAL (CODE)
                                    482 	.area GSINIT  (CODE)
                                    483 	.globl __sdcc_gsinit_startup
                                    484 	.globl __sdcc_program_startup
                                    485 	.globl __start__stack
                                    486 	.globl __mcs51_genXINIT
                                    487 	.globl __mcs51_genXRAMCLEAR
                                    488 	.globl __mcs51_genRAMCLEAR
                                    489 ;	../src/mainBase.c:36: struct rf_config rf_data = {
      0000B2 75 21 00         [24]  490 	mov	_rf_data,#0x00
      0000B5 75 22 E0         [24]  491 	mov	(_rf_data + 0x0001),#0xE0
      0000B8 75 23 00         [24]  492 	mov	(_rf_data + 0x0002),#0x00
      0000BB 75 24 00         [24]  493 	mov	(_rf_data + 0x0003),#0x00
      0000BE 75 25 00         [24]  494 	mov	(_rf_data + 0x0004),#0x00
      0000C1 75 26 00         [24]  495 	mov	(_rf_data + 0x0005),#0x00
      0000C4 75 27 00         [24]  496 	mov	(_rf_data + 0x0006),#0x00
      0000C7 75 28 00         [24]  497 	mov	(_rf_data + 0x0007),#0x00
      0000CA 75 29 00         [24]  498 	mov	(_rf_data + 0x0008),#0x00
      0000CD 75 2A 02         [24]  499 	mov	(_rf_data + 0x0009),#0x02
      0000D0 75 2B 02         [24]  500 	mov	(_rf_data + 0x000a),#0x02
      0000D3 75 2C 02         [24]  501 	mov	(_rf_data + 0x000b),#0x02
      0000D6 75 2D 61         [24]  502 	mov	(_rf_data + 0x000c),#0x61
      0000D9 75 2E 6F         [24]  503 	mov	(_rf_data + 0x000d),#0x6F
      0000DC 75 2F 14         [24]  504 	mov	(_rf_data + 0x000e),#0x14
                                    505 ;	../src/mainBase.c:45: struct rf_config *cfg = &rf_data;
      0000DF 75 30 21         [24]  506 	mov	_cfg,#_rf_data
      0000E2 75 31 00         [24]  507 	mov	(_cfg + 1),#0x00
      0000E5 75 32 40         [24]  508 	mov	(_cfg + 2),#0x40
                                    509 ;	../src/mainBase.c:46: char dst_addr[3] = { 0x0f, 0x01, 0x01 };
      0000E8 75 33 0F         [24]  510 	mov	_dst_addr,#0x0F
      0000EB 75 34 01         [24]  511 	mov	(_dst_addr + 0x0001),#0x01
      0000EE 75 35 01         [24]  512 	mov	(_dst_addr + 0x0002),#0x01
                                    513 ;	../src/mainBase.c:49: unsigned char code_segment = 0;
      0000F1 75 52 00         [24]  514 	mov	_code_segment,#0x00
                                    515 ;	../src/mainBase.c:50: unsigned char i = 0, counter = 0;
      0000F4 75 53 00         [24]  516 	mov	_i,#0x00
                                    517 ;	../src/mainBase.c:50: 
      0000F7 75 54 00         [24]  518 	mov	_counter,#0x00
                                    519 	.area GSFINAL (CODE)
      0000FA 02 00 56         [24]  520 	ljmp	__sdcc_program_startup
                                    521 ;--------------------------------------------------------
                                    522 ; Home
                                    523 ;--------------------------------------------------------
                                    524 	.area HOME    (CODE)
                                    525 	.area HOME    (CODE)
      000056                        526 __sdcc_program_startup:
      000056 02 00 FD         [24]  527 	ljmp	_main
                                    528 ;	return from main will return to caller
                                    529 ;--------------------------------------------------------
                                    530 ; code
                                    531 ;--------------------------------------------------------
                                    532 	.area CSEG    (CODE)
                                    533 ;------------------------------------------------------------
                                    534 ;Allocation info for local variables in function 'main'
                                    535 ;------------------------------------------------------------
                                    536 ;	../src/mainBase.c:52: void main()
                                    537 ;	-----------------------------------------
                                    538 ;	 function main
                                    539 ;	-----------------------------------------
      0000FD                        540 _main:
                           000007   541 	ar7 = 0x07
                           000006   542 	ar6 = 0x06
                           000005   543 	ar5 = 0x05
                           000004   544 	ar4 = 0x04
                           000003   545 	ar3 = 0x03
                           000002   546 	ar2 = 0x02
                           000001   547 	ar1 = 0x01
                           000000   548 	ar0 = 0x00
                                    549 ;	../src/mainBase.c:54: store_cpu_rate(16);
      0000FD 90 00 10         [24]  550 	mov	dptr,#(0x10&0x00ff)
      000100 E4               [12]  551 	clr	a
      000101 F5 F0            [12]  552 	mov	b,a
      000103 12 04 EF         [24]  553 	lcall	_store_cpu_rate
                                    554 ;	../src/mainBase.c:56: serial_init(19200);
      000106 90 4B 00         [24]  555 	mov	dptr,#0x4B00
      000109 12 04 5B         [24]  556 	lcall	_serial_init
                                    557 ;	../src/mainBase.c:58: P0_DIR &= ~0x28;
      00010C AF 94            [24]  558 	mov	r7,_P0_DIR
      00010E 74 D7            [12]  559 	mov	a,#0xD7
      000110 5F               [12]  560 	anl	a,r7
      000111 F5 94            [12]  561 	mov	_P0_DIR,a
                                    562 ;	../src/mainBase.c:59: P0_ALT &= ~0x28;
      000113 AF 95            [24]  563 	mov	r7,_P0_ALT
      000115 74 D7            [12]  564 	mov	a,#0xD7
      000117 5F               [12]  565 	anl	a,r7
      000118 F5 95            [12]  566 	mov	_P0_ALT,a
                                    567 ;	../src/mainBase.c:61: rf_init();
      00011A 12 03 2F         [24]  568 	lcall	_poll_rf_init
                                    569 ;	../src/mainBase.c:62: rf_configure(cfg);
      00011D 85 30 82         [24]  570 	mov	dpl,_cfg
      000120 85 31 83         [24]  571 	mov	dph,(_cfg + 1)
      000123 85 32 F0         [24]  572 	mov	b,(_cfg + 2)
      000126 12 03 3A         [24]  573 	lcall	_poll_rf_configure
                                    574 ;	../src/mainBase.c:65: EA = 1;
      000129 D2 AF            [12]  575 	setb	_EA
                                    576 ;	../src/mainBase.c:67: ES = 1;
      00012B D2 AC            [12]  577 	setb	_ES
                                    578 ;	../src/mainBase.c:69: EX4 = 1;
      00012D D2 EA            [12]  579 	setb	_EX4
                                    580 ;	../src/mainBase.c:71: for(i=0;i<6;i++)
      00012F 75 53 00         [24]  581 	mov	_i,#0x00
      000132                        582 00105$:
                                    583 ;	../src/mainBase.c:73: blink_led();
      000132 63 80 20         [24]  584 	xrl	_P0,#0x20
                                    585 ;	../src/mainBase.c:74: mdelay(500);
      000135 90 01 F4         [24]  586 	mov	dptr,#0x01F4
      000138 12 05 00         [24]  587 	lcall	_mdelay
                                    588 ;	../src/mainBase.c:71: for(i=0;i<6;i++)
      00013B 05 53            [12]  589 	inc	_i
      00013D 74 FA            [12]  590 	mov	a,#0x100 - 0x06
      00013F 25 53            [12]  591 	add	a,_i
      000141 50 EF            [24]  592 	jnc	00105$
                                    593 ;	../src/mainBase.c:76: puts("\n----------------------------");
      000143 90 06 EA         [24]  594 	mov	dptr,#___str_0
      000146 75 F0 80         [24]  595 	mov	b,#0x80
      000149 12 04 7A         [24]  596 	lcall	_puts
                                    597 ;	../src/mainBase.c:77: puts( "\nStartup.\n" );
      00014C 90 07 08         [24]  598 	mov	dptr,#___str_1
      00014F 75 F0 80         [24]  599 	mov	b,#0x80
      000152 12 04 7A         [24]  600 	lcall	_puts
                                    601 ;	../src/mainBase.c:78: while(1)
      000155                        602 00103$:
      000155 80 FE            [24]  603 	sjmp	00103$
                                    604 ;------------------------------------------------------------
                                    605 ;Allocation info for local variables in function 'interrupt_rf'
                                    606 ;------------------------------------------------------------
                                    607 ;fb_counter                Allocated with name '_interrupt_rf_fb_counter_1_17'
                                    608 ;------------------------------------------------------------
                                    609 ;	../src/mainBase.c:84: void interrupt_rf() __interrupt 10
                                    610 ;	-----------------------------------------
                                    611 ;	 function interrupt_rf
                                    612 ;	-----------------------------------------
      000157                        613 _interrupt_rf:
      000157 C0 20            [24]  614 	push	bits
      000159 C0 E0            [24]  615 	push	acc
      00015B C0 F0            [24]  616 	push	b
      00015D C0 82            [24]  617 	push	dpl
      00015F C0 83            [24]  618 	push	dph
      000161 C0 07            [24]  619 	push	(0+7)
      000163 C0 06            [24]  620 	push	(0+6)
      000165 C0 05            [24]  621 	push	(0+5)
      000167 C0 04            [24]  622 	push	(0+4)
      000169 C0 03            [24]  623 	push	(0+3)
      00016B C0 02            [24]  624 	push	(0+2)
      00016D C0 01            [24]  625 	push	(0+1)
      00016F C0 00            [24]  626 	push	(0+0)
      000171 C0 D0            [24]  627 	push	psw
      000173 75 D0 00         [24]  628 	mov	psw,#0x00
                                    629 ;	../src/mainBase.c:93: while (DR1) {
      000176                        630 00103$:
      000176 30 A2 4C         [24]  631 	jnb	_DR1,00105$
                                    632 ;	../src/mainBase.c:94: MessageBUF[fb_counter++] = spi_write_then_read(0);
      000179 AF 55            [24]  633 	mov	r7,_interrupt_rf_fb_counter_1_17
      00017B 05 55            [12]  634 	inc	_interrupt_rf_fb_counter_1_17
      00017D EF               [12]  635 	mov	a,r7
      00017E 24 36            [12]  636 	add	a,#_MessageBUF
      000180 F9               [12]  637 	mov	r1,a
      000181 75 82 00         [24]  638 	mov	dpl,#0x00
      000184 C0 01            [24]  639 	push	ar1
      000186 12 06 91         [24]  640 	lcall	_spi_write_then_read
      000189 E5 82            [12]  641 	mov	a,dpl
      00018B D0 01            [24]  642 	pop	ar1
      00018D F7               [12]  643 	mov	@r1,a
                                    644 ;	../src/mainBase.c:95: putc( MessageBUF[fb_counter-1]);
      00018E E5 55            [12]  645 	mov	a,_interrupt_rf_fb_counter_1_17
      000190 14               [12]  646 	dec	a
      000191 24 36            [12]  647 	add	a,#_MessageBUF
      000193 F9               [12]  648 	mov	r1,a
      000194 87 82            [24]  649 	mov	dpl,@r1
      000196 12 04 77         [24]  650 	lcall	_putc
                                    651 ;	../src/mainBase.c:100: if( fb_counter == RF_LENGTH ){
      000199 74 1C            [12]  652 	mov	a,#0x1C
      00019B B5 55 D8         [24]  653 	cjne	a,_interrupt_rf_fb_counter_1_17,00103$
                                    654 ;	../src/mainBase.c:102: cfg->rf_prog[1] = 0x14;
      00019E 74 0E            [12]  655 	mov	a,#0x0E
      0001A0 25 30            [12]  656 	add	a,_cfg
      0001A2 FD               [12]  657 	mov	r5,a
      0001A3 E4               [12]  658 	clr	a
      0001A4 35 31            [12]  659 	addc	a,(_cfg + 1)
      0001A6 FE               [12]  660 	mov	r6,a
      0001A7 AF 32            [24]  661 	mov	r7,(_cfg + 2)
      0001A9 8D 82            [24]  662 	mov	dpl,r5
      0001AB 8E 83            [24]  663 	mov	dph,r6
      0001AD 8F F0            [24]  664 	mov	b,r7
      0001AF 74 14            [12]  665 	mov	a,#0x14
      0001B1 12 03 14         [24]  666 	lcall	__gptrput
                                    667 ;	../src/mainBase.c:103: rf_configure( cfg );
      0001B4 85 30 82         [24]  668 	mov	dpl,_cfg
      0001B7 85 31 83         [24]  669 	mov	dph,(_cfg + 1)
      0001BA 85 32 F0         [24]  670 	mov	b,(_cfg + 2)
      0001BD 12 03 3A         [24]  671 	lcall	_poll_rf_configure
                                    672 ;	../src/mainBase.c:104: fb_counter = 0;
      0001C0 75 55 00         [24]  673 	mov	_interrupt_rf_fb_counter_1_17,#0x00
      0001C3 80 B1            [24]  674 	sjmp	00103$
      0001C5                        675 00105$:
                                    676 ;	../src/mainBase.c:111: CE = 0;
      0001C5 C2 A6            [12]  677 	clr	_CE
                                    678 ;	../src/mainBase.c:112: EXIF &= ~0x40;
      0001C7 AF 91            [24]  679 	mov	r7,_EXIF
      0001C9 74 BF            [12]  680 	mov	a,#0xBF
      0001CB 5F               [12]  681 	anl	a,r7
      0001CC F5 91            [12]  682 	mov	_EXIF,a
      0001CE D0 D0            [24]  683 	pop	psw
      0001D0 D0 00            [24]  684 	pop	(0+0)
      0001D2 D0 01            [24]  685 	pop	(0+1)
      0001D4 D0 02            [24]  686 	pop	(0+2)
      0001D6 D0 03            [24]  687 	pop	(0+3)
      0001D8 D0 04            [24]  688 	pop	(0+4)
      0001DA D0 05            [24]  689 	pop	(0+5)
      0001DC D0 06            [24]  690 	pop	(0+6)
      0001DE D0 07            [24]  691 	pop	(0+7)
      0001E0 D0 83            [24]  692 	pop	dph
      0001E2 D0 82            [24]  693 	pop	dpl
      0001E4 D0 F0            [24]  694 	pop	b
      0001E6 D0 E0            [24]  695 	pop	acc
      0001E8 D0 20            [24]  696 	pop	bits
      0001EA 32               [24]  697 	reti
                                    698 ;------------------------------------------------------------
                                    699 ;Allocation info for local variables in function 'interrupt_serial'
                                    700 ;------------------------------------------------------------
                                    701 ;header_counter            Allocated with name '_interrupt_serial_header_counter_1_20'
                                    702 ;code_counter              Allocated with name '_interrupt_serial_code_counter_1_20'
                                    703 ;------------------------------------------------------------
                                    704 ;	../src/mainBase.c:115: void interrupt_serial() __interrupt 4
                                    705 ;	-----------------------------------------
                                    706 ;	 function interrupt_serial
                                    707 ;	-----------------------------------------
      0001EB                        708 _interrupt_serial:
      0001EB C0 20            [24]  709 	push	bits
      0001ED C0 E0            [24]  710 	push	acc
      0001EF C0 F0            [24]  711 	push	b
      0001F1 C0 82            [24]  712 	push	dpl
      0001F3 C0 83            [24]  713 	push	dph
      0001F5 C0 07            [24]  714 	push	(0+7)
      0001F7 C0 06            [24]  715 	push	(0+6)
      0001F9 C0 05            [24]  716 	push	(0+5)
      0001FB C0 04            [24]  717 	push	(0+4)
      0001FD C0 03            [24]  718 	push	(0+3)
      0001FF C0 02            [24]  719 	push	(0+2)
      000201 C0 01            [24]  720 	push	(0+1)
      000203 C0 00            [24]  721 	push	(0+0)
      000205 C0 D0            [24]  722 	push	psw
      000207 75 D0 00         [24]  723 	mov	psw,#0x00
                                    724 ;	../src/mainBase.c:120: if(RI) {
                                    725 ;	../src/mainBase.c:122: RI = 0;
      00020A 10 98 03         [24]  726 	jbc	_RI,00142$
      00020D 02 02 F7         [24]  727 	ljmp	00119$
      000210                        728 00142$:
                                    729 ;	../src/mainBase.c:125: if( header_counter < (RF_LENGTH-1) ){
      000210 74 E5            [12]  730 	mov	a,#0x100 - 0x1B
      000212 25 56            [12]  731 	add	a,_interrupt_serial_header_counter_1_20
      000214 40 2A            [24]  732 	jc	00115$
                                    733 ;	../src/mainBase.c:126: if( header_counter == 3 ){
      000216 74 03            [12]  734 	mov	a,#0x03
      000218 B5 56 18         [24]  735 	cjne	a,_interrupt_serial_header_counter_1_20,00102$
                                    736 ;	../src/mainBase.c:127: code_counter = SBUF;
      00021B 85 99 57         [24]  737 	mov	_interrupt_serial_code_counter_1_20,_SBUF
                                    738 ;	../src/mainBase.c:128: code_segment = code_counter/RF_LENGTH;
      00021E 75 F0 1C         [24]  739 	mov	b,#0x1C
      000221 E5 57            [12]  740 	mov	a,_interrupt_serial_code_counter_1_20
      000223 84               [48]  741 	div	ab
      000224 F5 52            [12]  742 	mov	_code_segment,a
                                    743 ;	../src/mainBase.c:129: MessageBUF[header_counter++] = code_counter;
      000226 AF 56            [24]  744 	mov	r7,_interrupt_serial_header_counter_1_20
      000228 05 56            [12]  745 	inc	_interrupt_serial_header_counter_1_20
      00022A EF               [12]  746 	mov	a,r7
      00022B 24 36            [12]  747 	add	a,#_MessageBUF
      00022D F8               [12]  748 	mov	r0,a
      00022E A6 57            [24]  749 	mov	@r0,_interrupt_serial_code_counter_1_20
      000230 02 02 F7         [24]  750 	ljmp	00119$
      000233                        751 00102$:
                                    752 ;	../src/mainBase.c:132: MessageBUF[header_counter++] = SBUF;
      000233 AF 56            [24]  753 	mov	r7,_interrupt_serial_header_counter_1_20
      000235 05 56            [12]  754 	inc	_interrupt_serial_header_counter_1_20
      000237 EF               [12]  755 	mov	a,r7
      000238 24 36            [12]  756 	add	a,#_MessageBUF
      00023A F8               [12]  757 	mov	r0,a
      00023B A6 99            [24]  758 	mov	@r0,_SBUF
      00023D 02 02 F7         [24]  759 	ljmp	00119$
      000240                        760 00115$:
                                    761 ;	../src/mainBase.c:135: else if( header_counter == (RF_LENGTH-1) ){
      000240 74 1B            [12]  762 	mov	a,#0x1B
      000242 B5 56 48         [24]  763 	cjne	a,_interrupt_serial_header_counter_1_20,00112$
                                    764 ;	../src/mainBase.c:136: MessageBUF[header_counter++] = SBUF;
      000245 AF 56            [24]  765 	mov	r7,_interrupt_serial_header_counter_1_20
      000247 05 56            [12]  766 	inc	_interrupt_serial_header_counter_1_20
      000249 EF               [12]  767 	mov	a,r7
      00024A 24 36            [12]  768 	add	a,#_MessageBUF
      00024C F8               [12]  769 	mov	r0,a
      00024D A6 99            [24]  770 	mov	@r0,_SBUF
                                    771 ;	../src/mainBase.c:137: rf_send( dst_addr, 3, MessageBUF, RF_LENGTH );
      00024F 75 70 36         [24]  772 	mov	_poll_rf_send_PARM_3,#_MessageBUF
      000252 75 71 00         [24]  773 	mov	(_poll_rf_send_PARM_3 + 1),#0x00
      000255 75 72 40         [24]  774 	mov	(_poll_rf_send_PARM_3 + 2),#0x40
      000258 75 6F 03         [24]  775 	mov	_poll_rf_send_PARM_2,#0x03
      00025B 75 73 1C         [24]  776 	mov	_poll_rf_send_PARM_4,#0x1C
      00025E 90 00 33         [24]  777 	mov	dptr,#_dst_addr
      000261 75 F0 40         [24]  778 	mov	b,#0x40
      000264 12 03 85         [24]  779 	lcall	_poll_rf_send
                                    780 ;	../src/mainBase.c:140: cfg->rf_prog[1] = 0x15;
      000267 74 0E            [12]  781 	mov	a,#0x0E
      000269 25 30            [12]  782 	add	a,_cfg
      00026B FD               [12]  783 	mov	r5,a
      00026C E4               [12]  784 	clr	a
      00026D 35 31            [12]  785 	addc	a,(_cfg + 1)
      00026F FE               [12]  786 	mov	r6,a
      000270 AF 32            [24]  787 	mov	r7,(_cfg + 2)
      000272 8D 82            [24]  788 	mov	dpl,r5
      000274 8E 83            [24]  789 	mov	dph,r6
      000276 8F F0            [24]  790 	mov	b,r7
      000278 74 15            [12]  791 	mov	a,#0x15
      00027A 12 03 14         [24]  792 	lcall	__gptrput
                                    793 ;	../src/mainBase.c:141: rf_configure( cfg );
      00027D 85 30 82         [24]  794 	mov	dpl,_cfg
      000280 85 31 83         [24]  795 	mov	dph,(_cfg + 1)
      000283 85 32 F0         [24]  796 	mov	b,(_cfg + 2)
      000286 12 03 3A         [24]  797 	lcall	_poll_rf_configure
                                    798 ;	../src/mainBase.c:142: CE = 1; /* Activate RX or TX mode */
      000289 D2 A6            [12]  799 	setb	_CE
      00028B 80 6A            [24]  800 	sjmp	00119$
      00028D                        801 00112$:
                                    802 ;	../src/mainBase.c:156: if( code_counter % RF_LENGTH == 0 ){
      00028D 75 F0 1C         [24]  803 	mov	b,#0x1C
      000290 E5 57            [12]  804 	mov	a,_interrupt_serial_code_counter_1_20
      000292 84               [48]  805 	div	ab
      000293 E5 F0            [12]  806 	mov	a,b
      000295 FF               [12]  807 	mov	r7,a
      000296 70 07            [24]  808 	jnz	00109$
                                    809 ;	../src/mainBase.c:157: MessageBUF[0] = SBUF;
      000298 85 99 36         [24]  810 	mov	_MessageBUF,_SBUF
                                    811 ;	../src/mainBase.c:158: code_counter--;
      00029B 15 57            [12]  812 	dec	_interrupt_serial_code_counter_1_20
      00029D 80 58            [24]  813 	sjmp	00119$
      00029F                        814 00109$:
                                    815 ;	../src/mainBase.c:161: MessageBUF[RF_LENGTH-(code_counter%RF_LENGTH)] = SBUF;
      00029F 74 1C            [12]  816 	mov	a,#0x1C
      0002A1 C3               [12]  817 	clr	c
      0002A2 9F               [12]  818 	subb	a,r7
      0002A3 24 36            [12]  819 	add	a,#_MessageBUF
      0002A5 F8               [12]  820 	mov	r0,a
      0002A6 A6 99            [24]  821 	mov	@r0,_SBUF
                                    822 ;	../src/mainBase.c:162: code_counter--;
      0002A8 15 57            [12]  823 	dec	_interrupt_serial_code_counter_1_20
                                    824 ;	../src/mainBase.c:164: if( code_counter % RF_LENGTH == 0 ){
      0002AA 75 F0 1C         [24]  825 	mov	b,#0x1C
      0002AD E5 57            [12]  826 	mov	a,_interrupt_serial_code_counter_1_20
      0002AF 84               [48]  827 	div	ab
      0002B0 E5 F0            [12]  828 	mov	a,b
                                    829 ;	../src/mainBase.c:165: rf_send(dst_addr, 3, MessageBUF, RF_LENGTH );
      0002B2 70 3D            [24]  830 	jnz	00105$
      0002B4 75 70 36         [24]  831 	mov	_poll_rf_send_PARM_3,#_MessageBUF
      0002B7 F5 71            [12]  832 	mov	(_poll_rf_send_PARM_3 + 1),a
      0002B9 75 72 40         [24]  833 	mov	(_poll_rf_send_PARM_3 + 2),#0x40
      0002BC 75 6F 03         [24]  834 	mov	_poll_rf_send_PARM_2,#0x03
      0002BF 75 73 1C         [24]  835 	mov	_poll_rf_send_PARM_4,#0x1C
      0002C2 90 00 33         [24]  836 	mov	dptr,#_dst_addr
      0002C5 75 F0 40         [24]  837 	mov	b,#0x40
      0002C8 12 03 85         [24]  838 	lcall	_poll_rf_send
                                    839 ;	../src/mainBase.c:166: code_segment--;
      0002CB 15 52            [12]  840 	dec	_code_segment
                                    841 ;	../src/mainBase.c:181: cfg->rf_prog[1] = 0x15;
      0002CD 74 0E            [12]  842 	mov	a,#0x0E
      0002CF 25 30            [12]  843 	add	a,_cfg
      0002D1 FD               [12]  844 	mov	r5,a
      0002D2 E4               [12]  845 	clr	a
      0002D3 35 31            [12]  846 	addc	a,(_cfg + 1)
      0002D5 FE               [12]  847 	mov	r6,a
      0002D6 AF 32            [24]  848 	mov	r7,(_cfg + 2)
      0002D8 8D 82            [24]  849 	mov	dpl,r5
      0002DA 8E 83            [24]  850 	mov	dph,r6
      0002DC 8F F0            [24]  851 	mov	b,r7
      0002DE 74 15            [12]  852 	mov	a,#0x15
      0002E0 12 03 14         [24]  853 	lcall	__gptrput
                                    854 ;	../src/mainBase.c:182: rf_configure( cfg );
      0002E3 85 30 82         [24]  855 	mov	dpl,_cfg
      0002E6 85 31 83         [24]  856 	mov	dph,(_cfg + 1)
      0002E9 85 32 F0         [24]  857 	mov	b,(_cfg + 2)
      0002EC 12 03 3A         [24]  858 	lcall	_poll_rf_configure
                                    859 ;	../src/mainBase.c:183: CE = 1; /* Activate RX or TX mode */
      0002EF D2 A6            [12]  860 	setb	_CE
      0002F1                        861 00105$:
                                    862 ;	../src/mainBase.c:187: if( code_counter == 0 )
      0002F1 E5 57            [12]  863 	mov	a,_interrupt_serial_code_counter_1_20
                                    864 ;	../src/mainBase.c:188: header_counter = 0;
      0002F3 70 02            [24]  865 	jnz	00119$
      0002F5 F5 56            [12]  866 	mov	_interrupt_serial_header_counter_1_20,a
      0002F7                        867 00119$:
      0002F7 D0 D0            [24]  868 	pop	psw
      0002F9 D0 00            [24]  869 	pop	(0+0)
      0002FB D0 01            [24]  870 	pop	(0+1)
      0002FD D0 02            [24]  871 	pop	(0+2)
      0002FF D0 03            [24]  872 	pop	(0+3)
      000301 D0 04            [24]  873 	pop	(0+4)
      000303 D0 05            [24]  874 	pop	(0+5)
      000305 D0 06            [24]  875 	pop	(0+6)
      000307 D0 07            [24]  876 	pop	(0+7)
      000309 D0 83            [24]  877 	pop	dph
      00030B D0 82            [24]  878 	pop	dpl
      00030D D0 F0            [24]  879 	pop	b
      00030F D0 E0            [24]  880 	pop	acc
      000311 D0 20            [24]  881 	pop	bits
      000313 32               [24]  882 	reti
                                    883 	.area CSEG    (CODE)
                                    884 	.area CONST   (CODE)
      0006EA                        885 ___str_0:
      0006EA 0A                     886 	.db 0x0A
      0006EB 2D 2D 2D 2D 2D 2D 2D   887 	.ascii "----------------------------"
             2D 2D 2D 2D 2D 2D 2D
             2D 2D 2D 2D 2D 2D 2D
             2D 2D 2D 2D 2D 2D 2D
      000707 00                     888 	.db 0x00
      000708                        889 ___str_1:
      000708 0A                     890 	.db 0x0A
      000709 53 74 61 72 74 75 70   891 	.ascii "Startup."
             2E
      000711 0A                     892 	.db 0x0A
      000712 00                     893 	.db 0x00
                                    894 	.area XINIT   (CODE)
                                    895 	.area CABS    (ABS,CODE)
