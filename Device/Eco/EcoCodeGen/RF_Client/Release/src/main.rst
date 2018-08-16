                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ANSI-C Compiler
                                      3 ; Version 3.4.0/*rc1*/ #8960 (Mar 15 2014) (MINGW32)
                                      4 ; This file was generated Wed Mar 26 21:03:23 2014
                                      5 ;--------------------------------------------------------
                                      6 	.module main
                                      7 	.optsdcc -mmcs51 --model-small
                                      8 	
                                      9 ;--------------------------------------------------------
                                     10 ; Public variables in this module
                                     11 ;--------------------------------------------------------
                                     12 	.globl _main
                                     13 	.globl _mdelay
                                     14 	.globl _store_cpu_rate
                                     15 	.globl _puts
                                     16 	.globl _putc
                                     17 	.globl _serial_init
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
                                    180 	.globl _Message
                                    181 	.globl _send_ack_feedback_PARM_2
                                    182 	.globl _i
                                    183 	.globl _HeaderFile
                                    184 	.globl _codegenerator_status
                                    185 	.globl _dst_addr
                                    186 	.globl _cfg
                                    187 	.globl _rf_data
                                    188 	.globl _send_ack_feedback
                                    189 	.globl _interrupt_rf
                                    190 ;--------------------------------------------------------
                                    191 ; special function registers
                                    192 ;--------------------------------------------------------
                                    193 	.area RSEG    (ABS,DATA)
      000000                        194 	.org 0x0000
                           000080   195 _P0	=	0x0080
                           000081   196 _SP	=	0x0081
                           000082   197 _DPL	=	0x0082
                           000082   198 _DPL0	=	0x0082
                           000083   199 _DPH	=	0x0083
                           000083   200 _DPH0	=	0x0083
                           000084   201 _DPL1	=	0x0084
                           000085   202 _DPH1	=	0x0085
                           000086   203 _DPS	=	0x0086
                           000087   204 _PCON	=	0x0087
                           000088   205 _TCON	=	0x0088
                           000089   206 _TMOD	=	0x0089
                           00008A   207 _TL0	=	0x008a
                           00008B   208 _TL1	=	0x008b
                           00008C   209 _TH0	=	0x008c
                           00008D   210 _TH1	=	0x008d
                           00008E   211 _CKCON	=	0x008e
                           00008F   212 _SPC_FNC	=	0x008f
                           000090   213 _P1	=	0x0090
                           000091   214 _EXIF	=	0x0091
                           000092   215 _MPAGE	=	0x0092
                           000094   216 _P0_DIR	=	0x0094
                           000095   217 _P0_ALT	=	0x0095
                           000096   218 _P1_DIR	=	0x0096
                           000097   219 _P1_ALT	=	0x0097
                           000098   220 _SCON	=	0x0098
                           000099   221 _SBUF	=	0x0099
                           0000A0   222 _RADIO	=	0x00a0
                           0000A1   223 _ADCCON	=	0x00a1
                           0000A2   224 _ADCDATAH	=	0x00a2
                           0000A3   225 _ADCDATAL	=	0x00a3
                           0000A4   226 _ADCSTATIC	=	0x00a4
                           0000A8   227 _IE	=	0x00a8
                           0000A9   228 _PWMCON	=	0x00a9
                           0000AA   229 _PWMDUTY	=	0x00aa
                           0000AB   230 _REGX_MSB	=	0x00ab
                           0000AC   231 _REGX_LSB	=	0x00ac
                           0000AD   232 _REGX_CTRL	=	0x00ad
                           0000B1   233 _RSTREAS	=	0x00b1
                           0000B2   234 _SPI_DATA	=	0x00b2
                           0000B3   235 _SPI_CTRL	=	0x00b3
                           0000B4   236 _SPICLK	=	0x00b4
                           0000B5   237 _TICK_DV	=	0x00b5
                           0000B6   238 _CK_CTRL	=	0x00b6
                           0000B7   239 _TEST_MODE	=	0x00b7
                           0000B8   240 _IP	=	0x00b8
                           0000BC   241 _T1_1V2	=	0x00bc
                           0000BD   242 _T2_1V2	=	0x00bd
                           0000BE   243 _DEV_OFFSET	=	0x00be
                           0000C8   244 _T2CON	=	0x00c8
                           0000CA   245 _RCAP2L	=	0x00ca
                           0000CB   246 _RCAP2H	=	0x00cb
                           0000CC   247 _TL2	=	0x00cc
                           0000CD   248 _TH2	=	0x00cd
                           0000D0   249 _PSW	=	0x00d0
                           0000D8   250 _EICON	=	0x00d8
                           0000E0   251 _ACC	=	0x00e0
                           0000E8   252 _EIE	=	0x00e8
                           0000F0   253 _B	=	0x00f0
                           0000F8   254 _EIP	=	0x00f8
                                    255 ;--------------------------------------------------------
                                    256 ; special function bits
                                    257 ;--------------------------------------------------------
                                    258 	.area RSEG    (ABS,DATA)
      000000                        259 	.org 0x0000
                           000080   260 _P0_0	=	0x0080
                           000080   261 _DIO2	=	0x0080
                           000081   262 _P0_1	=	0x0081
                           000081   263 _RXD	=	0x0081
                           000081   264 _DIO3	=	0x0081
                           000082   265 _P0_2	=	0x0082
                           000082   266 _TXD	=	0x0082
                           000082   267 _DIO4	=	0x0082
                           000083   268 _P0_3	=	0x0083
                           000083   269 _INT0_N	=	0x0083
                           000083   270 _DIO5	=	0x0083
                           000084   271 _P0_4	=	0x0084
                           000084   272 _INT1_N	=	0x0084
                           000084   273 _DIO6	=	0x0084
                           000085   274 _P0_5	=	0x0085
                           000085   275 _T0	=	0x0085
                           000085   276 _DIO7	=	0x0085
                           000086   277 _P0_6	=	0x0086
                           000086   278 _T1	=	0x0086
                           000086   279 _DIO8	=	0x0086
                           000087   280 _P0_7	=	0x0087
                           000087   281 _PWM	=	0x0087
                           000087   282 _DIO9	=	0x0087
                           000088   283 _IT0	=	0x0088
                           000089   284 _IE0	=	0x0089
                           00008A   285 _IT1	=	0x008a
                           00008B   286 _IE1	=	0x008b
                           00008C   287 _TR0	=	0x008c
                           00008D   288 _TF0	=	0x008d
                           00008E   289 _TR1	=	0x008e
                           00008F   290 _TF1	=	0x008f
                           000090   291 _P1_0	=	0x0090
                           000090   292 _T2	=	0x0090
                           000090   293 _DIO0	=	0x0090
                           000091   294 _P1_1	=	0x0091
                           000091   295 _DIO1	=	0x0091
                           000092   296 _P1_2	=	0x0092
                           000092   297 _DIN0	=	0x0092
                           000098   298 _RI	=	0x0098
                           000099   299 _TI	=	0x0099
                           00009A   300 _RB8	=	0x009a
                           00009B   301 _TB8	=	0x009b
                           00009C   302 _REN	=	0x009c
                           00009D   303 _SM2	=	0x009d
                           00009E   304 _SM1	=	0x009e
                           00009F   305 _SM0	=	0x009f
                           0000A0   306 _DATA	=	0x00a0
                           0000A1   307 _CLK1	=	0x00a1
                           0000A2   308 _DR1	=	0x00a2
                           0000A3   309 _CS	=	0x00a3
                           0000A4   310 _DOUT2	=	0x00a4
                           0000A5   311 _CLK2	=	0x00a5
                           0000A6   312 _DR2_CE	=	0x00a6
                           0000A6   313 _DR2	=	0x00a6
                           0000A6   314 _CE	=	0x00a6
                           0000A7   315 _PWR_UP	=	0x00a7
                           0000A8   316 _EX0	=	0x00a8
                           0000A9   317 _ET0	=	0x00a9
                           0000AA   318 _EX1	=	0x00aa
                           0000AB   319 _ET1	=	0x00ab
                           0000AC   320 _ES	=	0x00ac
                           0000AD   321 _ET2	=	0x00ad
                           0000AF   322 _EA	=	0x00af
                           0000B8   323 _PX0	=	0x00b8
                           0000B9   324 _PT0	=	0x00b9
                           0000BA   325 _PX1	=	0x00ba
                           0000BB   326 _PT1	=	0x00bb
                           0000BC   327 _PS	=	0x00bc
                           0000BD   328 _PT2	=	0x00bd
                           0000C8   329 _CP_RL2	=	0x00c8
                           0000C8   330 _CPRL2	=	0x00c8
                           0000C9   331 _C_T2	=	0x00c9
                           0000C9   332 _CT2	=	0x00c9
                           0000CA   333 _TR2	=	0x00ca
                           0000CB   334 _EXEN2	=	0x00cb
                           0000CC   335 _TCLK	=	0x00cc
                           0000CD   336 _RCLK	=	0x00cd
                           0000CE   337 _EXF2	=	0x00ce
                           0000CF   338 _TF2	=	0x00cf
                           0000D0   339 _P	=	0x00d0
                           0000D1   340 _F1	=	0x00d1
                           0000D2   341 _OV	=	0x00d2
                           0000D3   342 _RS0	=	0x00d3
                           0000D4   343 _RS1	=	0x00d4
                           0000D5   344 _F0	=	0x00d5
                           0000D6   345 _AC	=	0x00d6
                           0000D7   346 _CY	=	0x00d7
                           0000DB   347 _WDTI	=	0x00db
                           0000E8   348 _EX2	=	0x00e8
                           0000E9   349 _EX3	=	0x00e9
                           0000EA   350 _EX4	=	0x00ea
                           0000EB   351 _EX5	=	0x00eb
                           0000EC   352 _EWDI	=	0x00ec
                           0000F8   353 _PX2	=	0x00f8
                           0000F9   354 _PX3	=	0x00f9
                           0000FA   355 _PX4	=	0x00fa
                           0000FB   356 _PX5	=	0x00fb
                           0000FC   357 _PWDI	=	0x00fc
                                    358 ;--------------------------------------------------------
                                    359 ; overlayable register banks
                                    360 ;--------------------------------------------------------
                                    361 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        362 	.ds 8
                                    363 ;--------------------------------------------------------
                                    364 ; overlayable bit register bank
                                    365 ;--------------------------------------------------------
                                    366 	.area BIT_BANK	(REL,OVR,DATA)
      000020                        367 bits:
      000020                        368 	.ds 1
                           008000   369 	b0 = bits[0]
                           008100   370 	b1 = bits[1]
                           008200   371 	b2 = bits[2]
                           008300   372 	b3 = bits[3]
                           008400   373 	b4 = bits[4]
                           008500   374 	b5 = bits[5]
                           008600   375 	b6 = bits[6]
                           008700   376 	b7 = bits[7]
                                    377 ;--------------------------------------------------------
                                    378 ; internal ram data
                                    379 ;--------------------------------------------------------
                                    380 	.area DSEG    (DATA)
      000021                        381 _rf_data::
      000021                        382 	.ds 15
      000030                        383 _cfg::
      000030                        384 	.ds 3
      000033                        385 _dst_addr::
      000033                        386 	.ds 3
      000036                        387 _codegenerator_status::
      000036                        388 	.ds 1
      000037                        389 _HeaderFile::
      000037                        390 	.ds 4
      00003B                        391 _i::
      00003B                        392 	.ds 2
      00003D                        393 _send_ack_feedback_PARM_2:
      00003D                        394 	.ds 1
      00003E                        395 _interrupt_rf_counter_1_20:
      00003E                        396 	.ds 1
                                    397 ;--------------------------------------------------------
                                    398 ; overlayable items in internal ram 
                                    399 ;--------------------------------------------------------
                                    400 ;--------------------------------------------------------
                                    401 ; Stack segment in internal ram 
                                    402 ;--------------------------------------------------------
                                    403 	.area	SSEG
      00005B                        404 __start__stack:
      00005B                        405 	.ds	1
                                    406 
                                    407 ;--------------------------------------------------------
                                    408 ; indirectly addressable internal ram data
                                    409 ;--------------------------------------------------------
                                    410 	.area ISEG    (DATA)
                                    411 ;--------------------------------------------------------
                                    412 ; absolute internal ram data
                                    413 ;--------------------------------------------------------
                                    414 	.area IABS    (ABS,DATA)
                                    415 	.area IABS    (ABS,DATA)
                                    416 ;--------------------------------------------------------
                                    417 ; bit data
                                    418 ;--------------------------------------------------------
                                    419 	.area BSEG    (BIT)
                                    420 ;--------------------------------------------------------
                                    421 ; paged external ram data
                                    422 ;--------------------------------------------------------
                                    423 	.area PSEG    (PAG,XDATA)
                                    424 ;--------------------------------------------------------
                                    425 ; external ram data
                                    426 ;--------------------------------------------------------
                                    427 	.area XSEG    (XDATA)
      000001                        428 _Message::
      000001                        429 	.ds 64
                                    430 ;--------------------------------------------------------
                                    431 ; absolute external ram data
                                    432 ;--------------------------------------------------------
                                    433 	.area XABS    (ABS,XDATA)
                                    434 ;--------------------------------------------------------
                                    435 ; external initialized ram data
                                    436 ;--------------------------------------------------------
                                    437 	.area XISEG   (XDATA)
                                    438 	.area HOME    (CODE)
                                    439 	.area GSINIT0 (CODE)
                                    440 	.area GSINIT1 (CODE)
                                    441 	.area GSINIT2 (CODE)
                                    442 	.area GSINIT3 (CODE)
                                    443 	.area GSINIT4 (CODE)
                                    444 	.area GSINIT5 (CODE)
                                    445 	.area GSINIT  (CODE)
                                    446 	.area GSFINAL (CODE)
                                    447 	.area CSEG    (CODE)
                                    448 ;--------------------------------------------------------
                                    449 ; interrupt vector 
                                    450 ;--------------------------------------------------------
                                    451 	.area HOME    (CODE)
      000000                        452 __interrupt_vect:
      000000 02 00 59         [24]  453 	ljmp	__sdcc_gsinit_startup
      000003 32               [24]  454 	reti
      000004                        455 	.ds	7
      00000B 32               [24]  456 	reti
      00000C                        457 	.ds	7
      000013 32               [24]  458 	reti
      000014                        459 	.ds	7
      00001B 32               [24]  460 	reti
      00001C                        461 	.ds	7
      000023 32               [24]  462 	reti
      000024                        463 	.ds	7
      00002B 32               [24]  464 	reti
      00002C                        465 	.ds	7
      000033 32               [24]  466 	reti
      000034                        467 	.ds	7
      00003B 32               [24]  468 	reti
      00003C                        469 	.ds	7
      000043 32               [24]  470 	reti
      000044                        471 	.ds	7
      00004B 32               [24]  472 	reti
      00004C                        473 	.ds	7
      000053 02 02 E1         [24]  474 	ljmp	_interrupt_rf
                                    475 ;--------------------------------------------------------
                                    476 ; global & static initialisations
                                    477 ;--------------------------------------------------------
                                    478 	.area HOME    (CODE)
                                    479 	.area GSINIT  (CODE)
                                    480 	.area GSFINAL (CODE)
                                    481 	.area GSINIT  (CODE)
                                    482 	.globl __sdcc_gsinit_startup
                                    483 	.globl __sdcc_program_startup
                                    484 	.globl __start__stack
                                    485 	.globl __mcs51_genXINIT
                                    486 	.globl __mcs51_genXRAMCLEAR
                                    487 	.globl __mcs51_genRAMCLEAR
                                    488 ;	../src/main.c:38: struct rf_config rf_data = {
      0000B2 75 21 00         [24]  489 	mov	_rf_data,#0x00
      0000B5 75 22 E0         [24]  490 	mov	(_rf_data + 0x0001),#0xE0
      0000B8 75 23 00         [24]  491 	mov	(_rf_data + 0x0002),#0x00
      0000BB 75 24 00         [24]  492 	mov	(_rf_data + 0x0003),#0x00
      0000BE 75 25 00         [24]  493 	mov	(_rf_data + 0x0004),#0x00
      0000C1 75 26 00         [24]  494 	mov	(_rf_data + 0x0005),#0x00
      0000C4 75 27 00         [24]  495 	mov	(_rf_data + 0x0006),#0x00
      0000C7 75 28 00         [24]  496 	mov	(_rf_data + 0x0007),#0x00
      0000CA 75 29 00         [24]  497 	mov	(_rf_data + 0x0008),#0x00
      0000CD 75 2A 0F         [24]  498 	mov	(_rf_data + 0x0009),#0x0F
      0000D0 75 2B 01         [24]  499 	mov	(_rf_data + 0x000a),#0x01
      0000D3 75 2C 01         [24]  500 	mov	(_rf_data + 0x000b),#0x01
      0000D6 75 2D 61         [24]  501 	mov	(_rf_data + 0x000c),#0x61
      0000D9 75 2E 6F         [24]  502 	mov	(_rf_data + 0x000d),#0x6F
      0000DC 75 2F 15         [24]  503 	mov	(_rf_data + 0x000e),#0x15
                                    504 ;	../src/main.c:46: struct rf_config *cfg = &rf_data;
      0000DF 75 30 21         [24]  505 	mov	_cfg,#_rf_data
      0000E2 75 31 00         [24]  506 	mov	(_cfg + 1),#0x00
      0000E5 75 32 40         [24]  507 	mov	(_cfg + 2),#0x40
                                    508 ;	../src/main.c:48: char dst_addr[3] = { 0x02, 0x02, 0x02 };
      0000E8 75 33 02         [24]  509 	mov	_dst_addr,#0x02
      0000EB 75 34 02         [24]  510 	mov	(_dst_addr + 0x0001),#0x02
      0000EE 75 35 02         [24]  511 	mov	(_dst_addr + 0x0002),#0x02
                                    512 	.area GSFINAL (CODE)
      0000F1 02 00 56         [24]  513 	ljmp	__sdcc_program_startup
                                    514 ;--------------------------------------------------------
                                    515 ; Home
                                    516 ;--------------------------------------------------------
                                    517 	.area HOME    (CODE)
                                    518 	.area HOME    (CODE)
      000056                        519 __sdcc_program_startup:
      000056 02 00 F4         [24]  520 	ljmp	_main
                                    521 ;	return from main will return to caller
                                    522 ;--------------------------------------------------------
                                    523 ; code
                                    524 ;--------------------------------------------------------
                                    525 	.area CSEG    (CODE)
                                    526 ;------------------------------------------------------------
                                    527 ;Allocation info for local variables in function 'main'
                                    528 ;------------------------------------------------------------
                                    529 ;	../src/main.c:56: void main()
                                    530 ;	-----------------------------------------
                                    531 ;	 function main
                                    532 ;	-----------------------------------------
      0000F4                        533 _main:
                           000007   534 	ar7 = 0x07
                           000006   535 	ar6 = 0x06
                           000005   536 	ar5 = 0x05
                           000004   537 	ar4 = 0x04
                           000003   538 	ar3 = 0x03
                           000002   539 	ar2 = 0x02
                           000001   540 	ar1 = 0x01
                           000000   541 	ar0 = 0x00
                                    542 ;	../src/main.c:60: store_cpu_rate(16);
      0000F4 90 00 10         [24]  543 	mov	dptr,#(0x10&0x00ff)
      0000F7 E4               [12]  544 	clr	a
      0000F8 F5 F0            [12]  545 	mov	b,a
      0000FA 12 05 F6         [24]  546 	lcall	_store_cpu_rate
                                    547 ;	../src/main.c:63: serial_init(19200);
      0000FD 90 4B 00         [24]  548 	mov	dptr,#0x4B00
      000100 12 07 22         [24]  549 	lcall	_serial_init
                                    550 ;	../src/main.c:66: P0_DIR &= ~0x28;
      000103 AF 94            [24]  551 	mov	r7,_P0_DIR
      000105 74 D7            [12]  552 	mov	a,#0xD7
      000107 5F               [12]  553 	anl	a,r7
      000108 F5 94            [12]  554 	mov	_P0_DIR,a
                                    555 ;	../src/main.c:67: P0_ALT &= ~0x28;
      00010A AF 95            [24]  556 	mov	r7,_P0_ALT
      00010C 74 D7            [12]  557 	mov	a,#0xD7
      00010E 5F               [12]  558 	anl	a,r7
      00010F F5 95            [12]  559 	mov	_P0_ALT,a
                                    560 ;	../src/main.c:70: rf_init();
      000111 12 05 16         [24]  561 	lcall	_poll_rf_init
                                    562 ;	../src/main.c:71: rf_configure(cfg);
      000114 85 30 82         [24]  563 	mov	dpl,_cfg
      000117 85 31 83         [24]  564 	mov	dph,(_cfg + 1)
      00011A 85 32 F0         [24]  565 	mov	b,(_cfg + 2)
      00011D 12 05 21         [24]  566 	lcall	_poll_rf_configure
                                    567 ;	../src/main.c:74: EA = 1;
      000120 D2 AF            [12]  568 	setb	_EA
                                    569 ;	../src/main.c:77: EX4 = 1;
      000122 D2 EA            [12]  570 	setb	_EX4
                                    571 ;	../src/main.c:79: for(i=0;i<6;i++)
      000124 E4               [12]  572 	clr	a
      000125 F5 3B            [12]  573 	mov	_i,a
      000127 F5 3C            [12]  574 	mov	(_i + 1),a
      000129                        575 00107$:
                                    576 ;	../src/main.c:81: blink_led();
      000129 63 80 20         [24]  577 	xrl	_P0,#0x20
                                    578 ;	../src/main.c:82: mdelay(500);
      00012C 90 01 F4         [24]  579 	mov	dptr,#0x01F4
      00012F 12 06 07         [24]  580 	lcall	_mdelay
                                    581 ;	../src/main.c:79: for(i=0;i<6;i++)
      000132 05 3B            [12]  582 	inc	_i
      000134 E4               [12]  583 	clr	a
      000135 B5 3B 02         [24]  584 	cjne	a,_i,00123$
      000138 05 3C            [12]  585 	inc	(_i + 1)
      00013A                        586 00123$:
      00013A C3               [12]  587 	clr	c
      00013B E5 3B            [12]  588 	mov	a,_i
      00013D 94 06            [12]  589 	subb	a,#0x06
      00013F E5 3C            [12]  590 	mov	a,(_i + 1)
      000141 64 80            [12]  591 	xrl	a,#0x80
      000143 94 80            [12]  592 	subb	a,#0x80
      000145 40 E2            [24]  593 	jc	00107$
                                    594 ;	../src/main.c:85: puts("\n----------------------------");
      000147 90 08 D1         [24]  595 	mov	dptr,#___str_0
      00014A 75 F0 80         [24]  596 	mov	b,#0x80
      00014D 12 07 41         [24]  597 	lcall	_puts
                                    598 ;	../src/main.c:87: codegenerator_status = IDLE;
      000150 75 36 00         [24]  599 	mov	_codegenerator_status,#0x00
                                    600 ;	../src/main.c:88: puts( "\n>Idle\n" );
      000153 90 08 EF         [24]  601 	mov	dptr,#___str_1
      000156 75 F0 80         [24]  602 	mov	b,#0x80
      000159 12 07 41         [24]  603 	lcall	_puts
                                    604 ;	../src/main.c:90: while(1) {
      00015C                        605 00105$:
                                    606 ;	../src/main.c:91: CE = 1; /* Activate RX or TX mode */
      00015C D2 A6            [12]  607 	setb	_CE
                                    608 ;	../src/main.c:93: if( codegenerator_status == RUNCODE ){
      00015E 74 04            [12]  609 	mov	a,#0x04
      000160 B5 36 F9         [24]  610 	cjne	a,_codegenerator_status,00105$
                                    611 ;	../src/main.c:95: puts("Exec\n");
      000163 90 08 F7         [24]  612 	mov	dptr,#___str_2
      000166 75 F0 80         [24]  613 	mov	b,#0x80
      000169 12 07 41         [24]  614 	lcall	_puts
                                    615 ;	../src/main.c:98: __endasm ;
      00016C 12 00 01         [24]  616 	lcall #_Message
                                    617 ;	../src/main.c:99: puts("ret\n");
      00016F 90 08 FD         [24]  618 	mov	dptr,#___str_3
      000172 75 F0 80         [24]  619 	mov	b,#0x80
      000175 12 07 41         [24]  620 	lcall	_puts
                                    621 ;	../src/main.c:101: send_ack_feedback( Message, 1);
      000178 75 3D 01         [24]  622 	mov	_send_ack_feedback_PARM_2,#0x01
      00017B 90 00 01         [24]  623 	mov	dptr,#_Message
      00017E 75 F0 00         [24]  624 	mov	b,#0x00
      000181 12 01 9B         [24]  625 	lcall	_send_ack_feedback
                                    626 ;	../src/main.c:120: codegenerator_status = IDLE;
      000184 75 36 00         [24]  627 	mov	_codegenerator_status,#0x00
                                    628 ;	../src/main.c:121: puts("\n----------------------------");
      000187 90 08 D1         [24]  629 	mov	dptr,#___str_0
      00018A 75 F0 80         [24]  630 	mov	b,#0x80
      00018D 12 07 41         [24]  631 	lcall	_puts
                                    632 ;	../src/main.c:122: puts( "\n>Idle\n" );
      000190 90 08 EF         [24]  633 	mov	dptr,#___str_1
      000193 75 F0 80         [24]  634 	mov	b,#0x80
      000196 12 07 41         [24]  635 	lcall	_puts
      000199 80 C1            [24]  636 	sjmp	00105$
                                    637 ;------------------------------------------------------------
                                    638 ;Allocation info for local variables in function 'send_ack_feedback'
                                    639 ;------------------------------------------------------------
                                    640 ;event                     Allocated with name '_send_ack_feedback_PARM_2'
                                    641 ;buf                       Allocated to registers r5 r6 r7 
                                    642 ;------------------------------------------------------------
                                    643 ;	../src/main.c:127: void send_ack_feedback( unsigned char *buf, unsigned char event )
                                    644 ;	-----------------------------------------
                                    645 ;	 function send_ack_feedback
                                    646 ;	-----------------------------------------
      00019B                        647 _send_ack_feedback:
      00019B AD 82            [24]  648 	mov	r5,dpl
      00019D AE 83            [24]  649 	mov	r6,dph
      00019F AF F0            [24]  650 	mov	r7,b
                                    651 ;	../src/main.c:130: cfg->rf_prog[1] = 0x14;
      0001A1 74 0E            [12]  652 	mov	a,#0x0E
      0001A3 25 30            [12]  653 	add	a,_cfg
      0001A5 FA               [12]  654 	mov	r2,a
      0001A6 E4               [12]  655 	clr	a
      0001A7 35 31            [12]  656 	addc	a,(_cfg + 1)
      0001A9 FB               [12]  657 	mov	r3,a
      0001AA AC 32            [24]  658 	mov	r4,(_cfg + 2)
      0001AC 8A 82            [24]  659 	mov	dpl,r2
      0001AE 8B 83            [24]  660 	mov	dph,r3
      0001B0 8C F0            [24]  661 	mov	b,r4
      0001B2 74 14            [12]  662 	mov	a,#0x14
      0001B4 12 04 FB         [24]  663 	lcall	__gptrput
                                    664 ;	../src/main.c:131: rf_configure( cfg );
      0001B7 85 30 82         [24]  665 	mov	dpl,_cfg
      0001BA 85 31 83         [24]  666 	mov	dph,(_cfg + 1)
      0001BD 85 32 F0         [24]  667 	mov	b,(_cfg + 2)
      0001C0 C0 07            [24]  668 	push	ar7
      0001C2 C0 06            [24]  669 	push	ar6
      0001C4 C0 05            [24]  670 	push	ar5
      0001C6 12 05 21         [24]  671 	lcall	_poll_rf_configure
                                    672 ;	../src/main.c:134: mdelay(700);	/* wait for dongle */
      0001C9 90 02 BC         [24]  673 	mov	dptr,#0x02BC
      0001CC 12 06 07         [24]  674 	lcall	_mdelay
      0001CF D0 05            [24]  675 	pop	ar5
      0001D1 D0 06            [24]  676 	pop	ar6
      0001D3 D0 07            [24]  677 	pop	ar7
                                    678 ;	../src/main.c:135: rf_send(dst_addr, 3, buf, RF_LENGTH );
      0001D5 75 56 03         [24]  679 	mov	_poll_rf_send_PARM_2,#0x03
      0001D8 8D 57            [24]  680 	mov	_poll_rf_send_PARM_3,r5
      0001DA 8E 58            [24]  681 	mov	(_poll_rf_send_PARM_3 + 1),r6
      0001DC 8F 59            [24]  682 	mov	(_poll_rf_send_PARM_3 + 2),r7
      0001DE 75 5A 1C         [24]  683 	mov	_poll_rf_send_PARM_4,#0x1C
      0001E1 90 00 33         [24]  684 	mov	dptr,#_dst_addr
      0001E4 75 F0 40         [24]  685 	mov	b,#0x40
      0001E7 C0 07            [24]  686 	push	ar7
      0001E9 C0 06            [24]  687 	push	ar6
      0001EB C0 05            [24]  688 	push	ar5
      0001ED 12 05 6C         [24]  689 	lcall	_poll_rf_send
      0001F0 D0 05            [24]  690 	pop	ar5
      0001F2 D0 06            [24]  691 	pop	ar6
      0001F4 D0 07            [24]  692 	pop	ar7
                                    693 ;	../src/main.c:136: if( event == 0 )
      0001F6 E5 3D            [12]  694 	mov	a,_send_ack_feedback_PARM_2
      0001F8 70 17            [24]  695 	jnz	00102$
                                    696 ;	../src/main.c:137: puts("send ack: \n");
      0001FA 90 09 02         [24]  697 	mov	dptr,#___str_4
      0001FD 75 F0 80         [24]  698 	mov	b,#0x80
      000200 C0 07            [24]  699 	push	ar7
      000202 C0 06            [24]  700 	push	ar6
      000204 C0 05            [24]  701 	push	ar5
      000206 12 07 41         [24]  702 	lcall	_puts
      000209 D0 05            [24]  703 	pop	ar5
      00020B D0 06            [24]  704 	pop	ar6
      00020D D0 07            [24]  705 	pop	ar7
      00020F 80 15            [24]  706 	sjmp	00103$
      000211                        707 00102$:
                                    708 ;	../src/main.c:139: puts("send result: \n");
      000211 90 09 0E         [24]  709 	mov	dptr,#___str_5
      000214 75 F0 80         [24]  710 	mov	b,#0x80
      000217 C0 07            [24]  711 	push	ar7
      000219 C0 06            [24]  712 	push	ar6
      00021B C0 05            [24]  713 	push	ar5
      00021D 12 07 41         [24]  714 	lcall	_puts
      000220 D0 05            [24]  715 	pop	ar5
      000222 D0 06            [24]  716 	pop	ar6
      000224 D0 07            [24]  717 	pop	ar7
      000226                        718 00103$:
                                    719 ;	../src/main.c:141: for( i = 0; i < RF_LENGTH; i++ ){
      000226 E4               [12]  720 	clr	a
      000227 F5 3B            [12]  721 	mov	_i,a
      000229 F5 3C            [12]  722 	mov	(_i + 1),a
      00022B                        723 00105$:
                                    724 ;	../src/main.c:142: putc( ( (buf[i]>>4) & 0x0f ) > 9 ? ( (buf[i]>>4) & 0xff )+ 55 :( (buf[i]>>4) & 0xff )+ 48 );
      00022B E5 3B            [12]  725 	mov	a,_i
      00022D 2D               [12]  726 	add	a,r5
      00022E FA               [12]  727 	mov	r2,a
      00022F E5 3C            [12]  728 	mov	a,(_i + 1)
      000231 3E               [12]  729 	addc	a,r6
      000232 FB               [12]  730 	mov	r3,a
      000233 8F 04            [24]  731 	mov	ar4,r7
      000235 8A 82            [24]  732 	mov	dpl,r2
      000237 8B 83            [24]  733 	mov	dph,r3
      000239 8C F0            [24]  734 	mov	b,r4
      00023B 12 08 B1         [24]  735 	lcall	__gptrget
      00023E FA               [12]  736 	mov	r2,a
      00023F C4               [12]  737 	swap	a
      000240 54 0F            [12]  738 	anl	a,#0x0F
      000242 FC               [12]  739 	mov	r4,a
      000243 74 0F            [12]  740 	mov	a,#0x0F
      000245 5C               [12]  741 	anl	a,r4
      000246 FB               [12]  742 	mov  r3,a
      000247 24 F6            [12]  743 	add	a,#0xff - 0x09
      000249 50 06            [24]  744 	jnc	00109$
      00024B 74 37            [12]  745 	mov	a,#0x37
      00024D 2C               [12]  746 	add	a,r4
      00024E FB               [12]  747 	mov	r3,a
      00024F 80 04            [24]  748 	sjmp	00110$
      000251                        749 00109$:
      000251 74 30            [12]  750 	mov	a,#0x30
      000253 2C               [12]  751 	add	a,r4
      000254 FB               [12]  752 	mov	r3,a
      000255                        753 00110$:
      000255 8B 82            [24]  754 	mov	dpl,r3
      000257 C0 07            [24]  755 	push	ar7
      000259 C0 06            [24]  756 	push	ar6
      00025B C0 05            [24]  757 	push	ar5
      00025D 12 07 3E         [24]  758 	lcall	_putc
      000260 D0 05            [24]  759 	pop	ar5
      000262 D0 06            [24]  760 	pop	ar6
      000264 D0 07            [24]  761 	pop	ar7
                                    762 ;	../src/main.c:143: putc( ( buf[i] & 0x0f ) > 9 ? ( buf[i] & 0x0f ) + 55  : ( buf[i] & 0x0f ) + 48 );
      000266 E5 3B            [12]  763 	mov	a,_i
      000268 2D               [12]  764 	add	a,r5
      000269 FA               [12]  765 	mov	r2,a
      00026A E5 3C            [12]  766 	mov	a,(_i + 1)
      00026C 3E               [12]  767 	addc	a,r6
      00026D FB               [12]  768 	mov	r3,a
      00026E 8F 04            [24]  769 	mov	ar4,r7
      000270 8A 82            [24]  770 	mov	dpl,r2
      000272 8B 83            [24]  771 	mov	dph,r3
      000274 8C F0            [24]  772 	mov	b,r4
      000276 12 08 B1         [24]  773 	lcall	__gptrget
      000279 FC               [12]  774 	mov	r4,a
      00027A 74 0F            [12]  775 	mov	a,#0x0F
      00027C 5C               [12]  776 	anl	a,r4
      00027D FB               [12]  777 	mov  r3,a
      00027E 24 F6            [12]  778 	add	a,#0xff - 0x09
      000280 50 08            [24]  779 	jnc	00111$
      000282 74 0F            [12]  780 	mov	a,#0x0F
      000284 5C               [12]  781 	anl	a,r4
      000285 24 37            [12]  782 	add	a,#0x37
      000287 FB               [12]  783 	mov	r3,a
      000288 80 06            [24]  784 	sjmp	00112$
      00028A                        785 00111$:
      00028A 74 0F            [12]  786 	mov	a,#0x0F
      00028C 5C               [12]  787 	anl	a,r4
      00028D 24 30            [12]  788 	add	a,#0x30
      00028F FB               [12]  789 	mov	r3,a
      000290                        790 00112$:
      000290 8B 82            [24]  791 	mov	dpl,r3
      000292 C0 07            [24]  792 	push	ar7
      000294 C0 06            [24]  793 	push	ar6
      000296 C0 05            [24]  794 	push	ar5
      000298 12 07 3E         [24]  795 	lcall	_putc
                                    796 ;	../src/main.c:144: putc( ' ' );
      00029B 75 82 20         [24]  797 	mov	dpl,#0x20
      00029E 12 07 3E         [24]  798 	lcall	_putc
      0002A1 D0 05            [24]  799 	pop	ar5
      0002A3 D0 06            [24]  800 	pop	ar6
      0002A5 D0 07            [24]  801 	pop	ar7
                                    802 ;	../src/main.c:141: for( i = 0; i < RF_LENGTH; i++ ){
      0002A7 05 3B            [12]  803 	inc	_i
      0002A9 E4               [12]  804 	clr	a
      0002AA B5 3B 02         [24]  805 	cjne	a,_i,00131$
      0002AD 05 3C            [12]  806 	inc	(_i + 1)
      0002AF                        807 00131$:
      0002AF C3               [12]  808 	clr	c
      0002B0 E5 3B            [12]  809 	mov	a,_i
      0002B2 94 1C            [12]  810 	subb	a,#0x1C
      0002B4 E5 3C            [12]  811 	mov	a,(_i + 1)
      0002B6 64 80            [12]  812 	xrl	a,#0x80
      0002B8 94 80            [12]  813 	subb	a,#0x80
      0002BA 50 03            [24]  814 	jnc	00132$
      0002BC 02 02 2B         [24]  815 	ljmp	00105$
      0002BF                        816 00132$:
                                    817 ;	../src/main.c:147: cfg->rf_prog[1] = 0x15;
      0002BF 74 0E            [12]  818 	mov	a,#0x0E
      0002C1 25 30            [12]  819 	add	a,_cfg
      0002C3 FD               [12]  820 	mov	r5,a
      0002C4 E4               [12]  821 	clr	a
      0002C5 35 31            [12]  822 	addc	a,(_cfg + 1)
      0002C7 FE               [12]  823 	mov	r6,a
      0002C8 AF 32            [24]  824 	mov	r7,(_cfg + 2)
      0002CA 8D 82            [24]  825 	mov	dpl,r5
      0002CC 8E 83            [24]  826 	mov	dph,r6
      0002CE 8F F0            [24]  827 	mov	b,r7
      0002D0 74 15            [12]  828 	mov	a,#0x15
      0002D2 12 04 FB         [24]  829 	lcall	__gptrput
                                    830 ;	../src/main.c:148: rf_configure( cfg );
      0002D5 85 30 82         [24]  831 	mov	dpl,_cfg
      0002D8 85 31 83         [24]  832 	mov	dph,(_cfg + 1)
      0002DB 85 32 F0         [24]  833 	mov	b,(_cfg + 2)
      0002DE 02 05 21         [24]  834 	ljmp	_poll_rf_configure
                                    835 ;------------------------------------------------------------
                                    836 ;Allocation info for local variables in function 'interrupt_rf'
                                    837 ;------------------------------------------------------------
                                    838 ;counter                   Allocated with name '_interrupt_rf_counter_1_20'
                                    839 ;------------------------------------------------------------
                                    840 ;	../src/main.c:152: void interrupt_rf() __interrupt 10
                                    841 ;	-----------------------------------------
                                    842 ;	 function interrupt_rf
                                    843 ;	-----------------------------------------
      0002E1                        844 _interrupt_rf:
      0002E1 C0 20            [24]  845 	push	bits
      0002E3 C0 E0            [24]  846 	push	acc
      0002E5 C0 F0            [24]  847 	push	b
      0002E7 C0 82            [24]  848 	push	dpl
      0002E9 C0 83            [24]  849 	push	dph
      0002EB C0 07            [24]  850 	push	(0+7)
      0002ED C0 06            [24]  851 	push	(0+6)
      0002EF C0 05            [24]  852 	push	(0+5)
      0002F1 C0 04            [24]  853 	push	(0+4)
      0002F3 C0 03            [24]  854 	push	(0+3)
      0002F5 C0 02            [24]  855 	push	(0+2)
      0002F7 C0 01            [24]  856 	push	(0+1)
      0002F9 C0 00            [24]  857 	push	(0+0)
      0002FB C0 D0            [24]  858 	push	psw
      0002FD 75 D0 00         [24]  859 	mov	psw,#0x00
                                    860 ;	../src/main.c:156: while (DR1) {
      000300                        861 00118$:
      000300 20 A2 03         [24]  862 	jb	_DR1,00173$
      000303 02 04 D5         [24]  863 	ljmp	00120$
      000306                        864 00173$:
                                    865 ;	../src/main.c:157: switch( codegenerator_status ){
      000306 E4               [12]  866 	clr	a
      000307 B5 36 02         [24]  867 	cjne	a,_codegenerator_status,00174$
      00030A 80 11            [24]  868 	sjmp	00101$
      00030C                        869 00174$:
      00030C 74 01            [12]  870 	mov	a,#0x01
      00030E B5 36 02         [24]  871 	cjne	a,_codegenerator_status,00175$
      000311 80 19            [24]  872 	sjmp	00102$
      000313                        873 00175$:
      000313 74 02            [12]  874 	mov	a,#0x02
      000315 B5 36 03         [24]  875 	cjne	a,_codegenerator_status,00176$
      000318 02 03 E6         [24]  876 	ljmp	00109$
      00031B                        877 00176$:
                                    878 ;	../src/main.c:158: case IDLE:
      00031B 80 E3            [24]  879 	sjmp	00118$
      00031D                        880 00101$:
                                    881 ;	../src/main.c:159: counter=0;
      00031D 75 3E 00         [24]  882 	mov	_interrupt_rf_counter_1_20,#0x00
                                    883 ;	../src/main.c:160: codegenerator_status = HEADERPACKET;
      000320 75 36 01         [24]  884 	mov	_codegenerator_status,#0x01
                                    885 ;	../src/main.c:161: puts("\n>Header Packet\n");
      000323 90 09 1D         [24]  886 	mov	dptr,#___str_6
      000326 75 F0 80         [24]  887 	mov	b,#0x80
      000329 12 07 41         [24]  888 	lcall	_puts
                                    889 ;	../src/main.c:162: case HEADERPACKET:
      00032C                        890 00102$:
                                    891 ;	../src/main.c:163: if( counter < 4 ){ 		/* header buffer length 4 bytes */
      00032C 74 FC            [12]  892 	mov	a,#0x100 - 0x04
      00032E 25 3E            [12]  893 	add	a,_interrupt_rf_counter_1_20
      000330 50 03            [24]  894 	jnc	00177$
      000332 02 03 B7         [24]  895 	ljmp	00107$
      000335                        896 00177$:
                                    897 ;	../src/main.c:164: HeaderFile[counter++] = spi_write_then_read(0);
      000335 AF 3E            [24]  898 	mov	r7,_interrupt_rf_counter_1_20
      000337 05 3E            [12]  899 	inc	_interrupt_rf_counter_1_20
      000339 EF               [12]  900 	mov	a,r7
      00033A 24 37            [12]  901 	add	a,#_HeaderFile
      00033C F9               [12]  902 	mov	r1,a
      00033D 75 82 00         [24]  903 	mov	dpl,#0x00
      000340 C0 01            [24]  904 	push	ar1
      000342 12 08 78         [24]  905 	lcall	_spi_write_then_read
      000345 E5 82            [12]  906 	mov	a,dpl
      000347 D0 01            [24]  907 	pop	ar1
      000349 F7               [12]  908 	mov	@r1,a
                                    909 ;	../src/main.c:165: putc( ( (HeaderFile[counter-1]>>4) & 0x0f ) > 9 ? ( (HeaderFile[counter-1]>>4) & 0xff )+ 55 :( (HeaderFile[counter-1]>>4) & 0xff )+ 48 );
      00034A E5 3E            [12]  910 	mov	a,_interrupt_rf_counter_1_20
      00034C 14               [12]  911 	dec	a
      00034D 24 37            [12]  912 	add	a,#_HeaderFile
      00034F F9               [12]  913 	mov	r1,a
      000350 E7               [12]  914 	mov	a,@r1
      000351 C4               [12]  915 	swap	a
      000352 54 0F            [12]  916 	anl	a,#(0x0F&0x0F)
      000354 FF               [12]  917 	mov	r7,a
      000355 24 F6            [12]  918 	add	a,#0xff - 0x09
      000357 50 0F            [24]  919 	jnc	00123$
      000359 E5 3E            [12]  920 	mov	a,_interrupt_rf_counter_1_20
      00035B 14               [12]  921 	dec	a
      00035C 24 37            [12]  922 	add	a,#_HeaderFile
      00035E F9               [12]  923 	mov	r1,a
      00035F E7               [12]  924 	mov	a,@r1
      000360 C4               [12]  925 	swap	a
      000361 54 0F            [12]  926 	anl	a,#0x0F
      000363 24 37            [12]  927 	add	a,#0x37
      000365 FF               [12]  928 	mov	r7,a
      000366 80 0E            [24]  929 	sjmp	00124$
      000368                        930 00123$:
      000368 E5 3E            [12]  931 	mov	a,_interrupt_rf_counter_1_20
      00036A 14               [12]  932 	dec	a
      00036B 24 37            [12]  933 	add	a,#_HeaderFile
      00036D F9               [12]  934 	mov	r1,a
      00036E E7               [12]  935 	mov	a,@r1
      00036F C4               [12]  936 	swap	a
      000370 54 0F            [12]  937 	anl	a,#0x0F
      000372 FE               [12]  938 	mov	r6,a
      000373 24 30            [12]  939 	add	a,#0x30
      000375 FF               [12]  940 	mov	r7,a
      000376                        941 00124$:
      000376 8F 82            [24]  942 	mov	dpl,r7
      000378 12 07 3E         [24]  943 	lcall	_putc
                                    944 ;	../src/main.c:166: putc( ( HeaderFile[counter-1] & 0x0f ) > 9 ? ( HeaderFile[counter-1] & 0x0f ) + 55  : ( HeaderFile[counter-1] & 0x0f ) + 48 );
      00037B E5 3E            [12]  945 	mov	a,_interrupt_rf_counter_1_20
      00037D 14               [12]  946 	dec	a
      00037E 24 37            [12]  947 	add	a,#_HeaderFile
      000380 F9               [12]  948 	mov	r1,a
      000381 87 07            [24]  949 	mov	ar7,@r1
      000383 53 07 0F         [24]  950 	anl	ar7,#0x0F
      000386 EF               [12]  951 	mov	a,r7
      000387 24 F6            [12]  952 	add	a,#0xff - 0x09
      000389 50 10            [24]  953 	jnc	00125$
      00038B E5 3E            [12]  954 	mov	a,_interrupt_rf_counter_1_20
      00038D 14               [12]  955 	dec	a
      00038E 24 37            [12]  956 	add	a,#_HeaderFile
      000390 F9               [12]  957 	mov	r1,a
      000391 87 07            [24]  958 	mov	ar7,@r1
      000393 74 0F            [12]  959 	mov	a,#0x0F
      000395 5F               [12]  960 	anl	a,r7
      000396 24 37            [12]  961 	add	a,#0x37
      000398 FF               [12]  962 	mov	r7,a
      000399 80 0E            [24]  963 	sjmp	00126$
      00039B                        964 00125$:
      00039B E5 3E            [12]  965 	mov	a,_interrupt_rf_counter_1_20
      00039D 14               [12]  966 	dec	a
      00039E 24 37            [12]  967 	add	a,#_HeaderFile
      0003A0 F9               [12]  968 	mov	r1,a
      0003A1 87 06            [24]  969 	mov	ar6,@r1
      0003A3 74 0F            [12]  970 	mov	a,#0x0F
      0003A5 5E               [12]  971 	anl	a,r6
      0003A6 24 30            [12]  972 	add	a,#0x30
      0003A8 FF               [12]  973 	mov	r7,a
      0003A9                        974 00126$:
      0003A9 8F 82            [24]  975 	mov	dpl,r7
      0003AB 12 07 3E         [24]  976 	lcall	_putc
                                    977 ;	../src/main.c:167: putc( ' ' );
      0003AE 75 82 20         [24]  978 	mov	dpl,#0x20
      0003B1 12 07 3E         [24]  979 	lcall	_putc
      0003B4 02 03 00         [24]  980 	ljmp	00118$
      0003B7                        981 00107$:
                                    982 ;	../src/main.c:169: else if( counter < RF_LENGTH ){
      0003B7 74 E4            [12]  983 	mov	a,#0x100 - 0x1C
      0003B9 25 3E            [12]  984 	add	a,_interrupt_rf_counter_1_20
      0003BB 40 0B            [24]  985 	jc	00104$
                                    986 ;	../src/main.c:170: spi_write_then_read(0);
      0003BD 75 82 00         [24]  987 	mov	dpl,#0x00
      0003C0 12 08 78         [24]  988 	lcall	_spi_write_then_read
                                    989 ;	../src/main.c:171: counter++;
      0003C3 05 3E            [12]  990 	inc	_interrupt_rf_counter_1_20
      0003C5 02 03 00         [24]  991 	ljmp	00118$
      0003C8                        992 00104$:
                                    993 ;	../src/main.c:174: counter = 0;
      0003C8 75 3E 00         [24]  994 	mov	_interrupt_rf_counter_1_20,#0x00
                                    995 ;	../src/main.c:175: send_ack_feedback( HeaderFile, 0 );
      0003CB 75 3D 00         [24]  996 	mov	_send_ack_feedback_PARM_2,#0x00
      0003CE 90 00 37         [24]  997 	mov	dptr,#_HeaderFile
      0003D1 75 F0 40         [24]  998 	mov	b,#0x40
      0003D4 12 01 9B         [24]  999 	lcall	_send_ack_feedback
                                   1000 ;	../src/main.c:176: codegenerator_status = CODEPACKET;
      0003D7 75 36 02         [24] 1001 	mov	_codegenerator_status,#0x02
                                   1002 ;	../src/main.c:177: puts("\n\r>Code Packet\n");
      0003DA 90 09 2E         [24] 1003 	mov	dptr,#___str_7
      0003DD 75 F0 80         [24] 1004 	mov	b,#0x80
      0003E0 12 07 41         [24] 1005 	lcall	_puts
                                   1006 ;	../src/main.c:179: break;
      0003E3 02 03 00         [24] 1007 	ljmp	00118$
                                   1008 ;	../src/main.c:180: case CODEPACKET:
      0003E6                       1009 00109$:
                                   1010 ;	../src/main.c:181: if( counter < HeaderFile[3] ){
      0003E6 C3               [12] 1011 	clr	c
      0003E7 E5 3E            [12] 1012 	mov	a,_interrupt_rf_counter_1_20
      0003E9 95 3A            [12] 1013 	subb	a,(_HeaderFile + 0x0003)
      0003EB 40 03            [24] 1014 	jc	00181$
      0003ED 02 03 00         [24] 1015 	ljmp	00118$
      0003F0                       1016 00181$:
                                   1017 ;	../src/main.c:182: Message[counter++] = spi_write_then_read(0);
      0003F0 AF 3E            [24] 1018 	mov	r7,_interrupt_rf_counter_1_20
      0003F2 05 3E            [12] 1019 	inc	_interrupt_rf_counter_1_20
      0003F4 EF               [12] 1020 	mov	a,r7
      0003F5 24 01            [12] 1021 	add	a,#_Message
      0003F7 FF               [12] 1022 	mov	r7,a
      0003F8 E4               [12] 1023 	clr	a
      0003F9 34 00            [12] 1024 	addc	a,#(_Message >> 8)
      0003FB FE               [12] 1025 	mov	r6,a
      0003FC 75 82 00         [24] 1026 	mov	dpl,#0x00
      0003FF C0 07            [24] 1027 	push	ar7
      000401 C0 06            [24] 1028 	push	ar6
      000403 12 08 78         [24] 1029 	lcall	_spi_write_then_read
      000406 AD 82            [24] 1030 	mov	r5,dpl
      000408 D0 06            [24] 1031 	pop	ar6
      00040A D0 07            [24] 1032 	pop	ar7
      00040C 8F 82            [24] 1033 	mov	dpl,r7
      00040E 8E 83            [24] 1034 	mov	dph,r6
      000410 ED               [12] 1035 	mov	a,r5
      000411 F0               [24] 1036 	movx	@dptr,a
                                   1037 ;	../src/main.c:183: putc( ( (Message[counter-1]>>4) & 0x0f ) > 9 ? ( (Message[counter-1]>>4) & 0xff )+ 55 :( (Message[counter-1]>>4) & 0xff )+ 48 );
      000412 E5 3E            [12] 1038 	mov	a,_interrupt_rf_counter_1_20
      000414 14               [12] 1039 	dec	a
      000415 24 01            [12] 1040 	add	a,#_Message
      000417 F5 82            [12] 1041 	mov	dpl,a
      000419 E4               [12] 1042 	clr	a
      00041A 34 00            [12] 1043 	addc	a,#(_Message >> 8)
      00041C F5 83            [12] 1044 	mov	dph,a
      00041E E0               [24] 1045 	movx	a,@dptr
      00041F C4               [12] 1046 	swap	a
      000420 54 0F            [12] 1047 	anl	a,#(0x0F&0x0F)
      000422 FF               [12] 1048 	mov	r7,a
      000423 24 F6            [12] 1049 	add	a,#0xff - 0x09
      000425 50 15            [24] 1050 	jnc	00127$
      000427 E5 3E            [12] 1051 	mov	a,_interrupt_rf_counter_1_20
      000429 14               [12] 1052 	dec	a
      00042A 24 01            [12] 1053 	add	a,#_Message
      00042C F5 82            [12] 1054 	mov	dpl,a
      00042E E4               [12] 1055 	clr	a
      00042F 34 00            [12] 1056 	addc	a,#(_Message >> 8)
      000431 F5 83            [12] 1057 	mov	dph,a
      000433 E0               [24] 1058 	movx	a,@dptr
      000434 C4               [12] 1059 	swap	a
      000435 54 0F            [12] 1060 	anl	a,#0x0F
      000437 24 37            [12] 1061 	add	a,#0x37
      000439 FF               [12] 1062 	mov	r7,a
      00043A 80 14            [24] 1063 	sjmp	00128$
      00043C                       1064 00127$:
      00043C E5 3E            [12] 1065 	mov	a,_interrupt_rf_counter_1_20
      00043E 14               [12] 1066 	dec	a
      00043F 24 01            [12] 1067 	add	a,#_Message
      000441 F5 82            [12] 1068 	mov	dpl,a
      000443 E4               [12] 1069 	clr	a
      000444 34 00            [12] 1070 	addc	a,#(_Message >> 8)
      000446 F5 83            [12] 1071 	mov	dph,a
      000448 E0               [24] 1072 	movx	a,@dptr
      000449 C4               [12] 1073 	swap	a
      00044A 54 0F            [12] 1074 	anl	a,#0x0F
      00044C FE               [12] 1075 	mov	r6,a
      00044D 24 30            [12] 1076 	add	a,#0x30
      00044F FF               [12] 1077 	mov	r7,a
      000450                       1078 00128$:
      000450 8F 82            [24] 1079 	mov	dpl,r7
      000452 12 07 3E         [24] 1080 	lcall	_putc
                                   1081 ;	../src/main.c:184: putc( ( Message[counter-1] & 0x0f ) > 9 ? ( Message[counter-1] & 0x0f ) + 55  : ( Message[counter-1] & 0x0f ) + 48 );
      000455 E5 3E            [12] 1082 	mov	a,_interrupt_rf_counter_1_20
      000457 14               [12] 1083 	dec	a
      000458 24 01            [12] 1084 	add	a,#_Message
      00045A F5 82            [12] 1085 	mov	dpl,a
      00045C E4               [12] 1086 	clr	a
      00045D 34 00            [12] 1087 	addc	a,#(_Message >> 8)
      00045F F5 83            [12] 1088 	mov	dph,a
      000461 E0               [24] 1089 	movx	a,@dptr
      000462 54 0F            [12] 1090 	anl	a,#0x0F
      000464 FF               [12] 1091 	mov	r7,a
      000465 24 F6            [12] 1092 	add	a,#0xff - 0x09
      000467 50 16            [24] 1093 	jnc	00129$
      000469 E5 3E            [12] 1094 	mov	a,_interrupt_rf_counter_1_20
      00046B 14               [12] 1095 	dec	a
      00046C 24 01            [12] 1096 	add	a,#_Message
      00046E F5 82            [12] 1097 	mov	dpl,a
      000470 E4               [12] 1098 	clr	a
      000471 34 00            [12] 1099 	addc	a,#(_Message >> 8)
      000473 F5 83            [12] 1100 	mov	dph,a
      000475 E0               [24] 1101 	movx	a,@dptr
      000476 FF               [12] 1102 	mov	r7,a
      000477 74 0F            [12] 1103 	mov	a,#0x0F
      000479 5F               [12] 1104 	anl	a,r7
      00047A 24 37            [12] 1105 	add	a,#0x37
      00047C FF               [12] 1106 	mov	r7,a
      00047D 80 14            [24] 1107 	sjmp	00130$
      00047F                       1108 00129$:
      00047F E5 3E            [12] 1109 	mov	a,_interrupt_rf_counter_1_20
      000481 14               [12] 1110 	dec	a
      000482 24 01            [12] 1111 	add	a,#_Message
      000484 F5 82            [12] 1112 	mov	dpl,a
      000486 E4               [12] 1113 	clr	a
      000487 34 00            [12] 1114 	addc	a,#(_Message >> 8)
      000489 F5 83            [12] 1115 	mov	dph,a
      00048B E0               [24] 1116 	movx	a,@dptr
      00048C FE               [12] 1117 	mov	r6,a
      00048D 74 0F            [12] 1118 	mov	a,#0x0F
      00048F 5E               [12] 1119 	anl	a,r6
      000490 24 30            [12] 1120 	add	a,#0x30
      000492 FF               [12] 1121 	mov	r7,a
      000493                       1122 00130$:
      000493 8F 82            [24] 1123 	mov	dpl,r7
      000495 12 07 3E         [24] 1124 	lcall	_putc
                                   1125 ;	../src/main.c:185: putc( ' ' );
      000498 75 82 20         [24] 1126 	mov	dpl,#0x20
      00049B 12 07 3E         [24] 1127 	lcall	_putc
                                   1128 ;	../src/main.c:187: if( ( counter % RF_LENGTH == 0) ){
      00049E 75 F0 1C         [24] 1129 	mov	b,#0x1C
      0004A1 E5 3E            [12] 1130 	mov	a,_interrupt_rf_counter_1_20
      0004A3 84               [48] 1131 	div	ab
      0004A4 E5 F0            [12] 1132 	mov	a,b
      0004A6 60 03            [24] 1133 	jz	00184$
      0004A8 02 03 00         [24] 1134 	ljmp	00118$
      0004AB                       1135 00184$:
                                   1136 ;	../src/main.c:188: if( (counter / RF_LENGTH) != HeaderFile[2] ){
      0004AB 75 F0 1C         [24] 1137 	mov	b,#0x1C
      0004AE E5 3E            [12] 1138 	mov	a,_interrupt_rf_counter_1_20
      0004B0 84               [48] 1139 	div	ab
      0004B1 FF               [12] 1140 	mov	r7,a
      0004B2 B5 39 02         [24] 1141 	cjne	a,(_HeaderFile + 0x0002),00185$
      0004B5 80 0F            [24] 1142 	sjmp	00111$
      0004B7                       1143 00185$:
                                   1144 ;	../src/main.c:189: send_ack_feedback( Message, 0 );
      0004B7 75 3D 00         [24] 1145 	mov	_send_ack_feedback_PARM_2,#0x00
      0004BA 90 00 01         [24] 1146 	mov	dptr,#_Message
      0004BD 75 F0 00         [24] 1147 	mov	b,#0x00
      0004C0 12 01 9B         [24] 1148 	lcall	_send_ack_feedback
      0004C3 02 03 00         [24] 1149 	ljmp	00118$
      0004C6                       1150 00111$:
                                   1151 ;	../src/main.c:208: codegenerator_status = RUNCODE;
      0004C6 75 36 04         [24] 1152 	mov	_codegenerator_status,#0x04
                                   1153 ;	../src/main.c:209: puts("\n\r>Run Code\n");
      0004C9 90 09 3E         [24] 1154 	mov	dptr,#___str_8
      0004CC 75 F0 80         [24] 1155 	mov	b,#0x80
      0004CF 12 07 41         [24] 1156 	lcall	_puts
                                   1157 ;	../src/main.c:214: } /* end switch case */
      0004D2 02 03 00         [24] 1158 	ljmp	00118$
      0004D5                       1159 00120$:
                                   1160 ;	../src/main.c:218: CE = 0;
      0004D5 C2 A6            [12] 1161 	clr	_CE
                                   1162 ;	../src/main.c:219: EXIF &= ~0x40;
      0004D7 AF 91            [24] 1163 	mov	r7,_EXIF
      0004D9 74 BF            [12] 1164 	mov	a,#0xBF
      0004DB 5F               [12] 1165 	anl	a,r7
      0004DC F5 91            [12] 1166 	mov	_EXIF,a
      0004DE D0 D0            [24] 1167 	pop	psw
      0004E0 D0 00            [24] 1168 	pop	(0+0)
      0004E2 D0 01            [24] 1169 	pop	(0+1)
      0004E4 D0 02            [24] 1170 	pop	(0+2)
      0004E6 D0 03            [24] 1171 	pop	(0+3)
      0004E8 D0 04            [24] 1172 	pop	(0+4)
      0004EA D0 05            [24] 1173 	pop	(0+5)
      0004EC D0 06            [24] 1174 	pop	(0+6)
      0004EE D0 07            [24] 1175 	pop	(0+7)
      0004F0 D0 83            [24] 1176 	pop	dph
      0004F2 D0 82            [24] 1177 	pop	dpl
      0004F4 D0 F0            [24] 1178 	pop	b
      0004F6 D0 E0            [24] 1179 	pop	acc
      0004F8 D0 20            [24] 1180 	pop	bits
      0004FA 32               [24] 1181 	reti
                                   1182 	.area CSEG    (CODE)
                                   1183 	.area CONST   (CODE)
      0008D1                       1184 ___str_0:
      0008D1 0A                    1185 	.db 0x0A
      0008D2 2D 2D 2D 2D 2D 2D 2D  1186 	.ascii "----------------------------"
             2D 2D 2D 2D 2D 2D 2D
             2D 2D 2D 2D 2D 2D 2D
             2D 2D 2D 2D 2D 2D 2D
      0008EE 00                    1187 	.db 0x00
      0008EF                       1188 ___str_1:
      0008EF 0A                    1189 	.db 0x0A
      0008F0 3E 49 64 6C 65        1190 	.ascii ">Idle"
      0008F5 0A                    1191 	.db 0x0A
      0008F6 00                    1192 	.db 0x00
      0008F7                       1193 ___str_2:
      0008F7 45 78 65 63           1194 	.ascii "Exec"
      0008FB 0A                    1195 	.db 0x0A
      0008FC 00                    1196 	.db 0x00
      0008FD                       1197 ___str_3:
      0008FD 72 65 74              1198 	.ascii "ret"
      000900 0A                    1199 	.db 0x0A
      000901 00                    1200 	.db 0x00
      000902                       1201 ___str_4:
      000902 73 65 6E 64 20 61 63  1202 	.ascii "send ack: "
             6B 3A 20
      00090C 0A                    1203 	.db 0x0A
      00090D 00                    1204 	.db 0x00
      00090E                       1205 ___str_5:
      00090E 73 65 6E 64 20 72 65  1206 	.ascii "send result: "
             73 75 6C 74 3A 20
      00091B 0A                    1207 	.db 0x0A
      00091C 00                    1208 	.db 0x00
      00091D                       1209 ___str_6:
      00091D 0A                    1210 	.db 0x0A
      00091E 3E 48 65 61 64 65 72  1211 	.ascii ">Header Packet"
             20 50 61 63 6B 65 74
      00092C 0A                    1212 	.db 0x0A
      00092D 00                    1213 	.db 0x00
      00092E                       1214 ___str_7:
      00092E 0A                    1215 	.db 0x0A
      00092F 0D                    1216 	.db 0x0D
      000930 3E 43 6F 64 65 20 50  1217 	.ascii ">Code Packet"
             61 63 6B 65 74
      00093C 0A                    1218 	.db 0x0A
      00093D 00                    1219 	.db 0x00
      00093E                       1220 ___str_8:
      00093E 0A                    1221 	.db 0x0A
      00093F 0D                    1222 	.db 0x0D
      000940 3E 52 75 6E 20 43 6F  1223 	.ascii ">Run Code"
             64 65
      000949 0A                    1224 	.db 0x0A
      00094A 00                    1225 	.db 0x00
                                   1226 	.area XINIT   (CODE)
                                   1227 	.area CABS    (ABS,CODE)
