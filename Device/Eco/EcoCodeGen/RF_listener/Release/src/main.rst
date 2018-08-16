                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ANSI-C Compiler
                                      3 ; Version 3.4.0/*rc1*/ #8960 (Mar 15 2014) (MINGW32)
                                      4 ; This file was generated Wed Mar 26 21:03:35 2014
                                      5 ;--------------------------------------------------------
                                      6 	.module main
                                      7 	.optsdcc -mmcs51 --model-small
                                      8 	
                                      9 ;--------------------------------------------------------
                                     10 ; Public variables in this module
                                     11 ;--------------------------------------------------------
                                     12 	.globl _main
                                     13 	.globl _putc
                                     14 	.globl _puts
                                     15 	.globl _mdelay
                                     16 	.globl _store_cpu_rate
                                     17 	.globl _serial_init
                                     18 	.globl _spi_write_then_read
                                     19 	.globl _poll_rf_configure
                                     20 	.globl _poll_rf_init
                                     21 	.globl _PWDI
                                     22 	.globl _PX5
                                     23 	.globl _PX4
                                     24 	.globl _PX3
                                     25 	.globl _PX2
                                     26 	.globl _EWDI
                                     27 	.globl _EX5
                                     28 	.globl _EX4
                                     29 	.globl _EX3
                                     30 	.globl _EX2
                                     31 	.globl _WDTI
                                     32 	.globl _CY
                                     33 	.globl _AC
                                     34 	.globl _F0
                                     35 	.globl _RS1
                                     36 	.globl _RS0
                                     37 	.globl _OV
                                     38 	.globl _F1
                                     39 	.globl _P
                                     40 	.globl _TF2
                                     41 	.globl _EXF2
                                     42 	.globl _RCLK
                                     43 	.globl _TCLK
                                     44 	.globl _EXEN2
                                     45 	.globl _TR2
                                     46 	.globl _CT2
                                     47 	.globl _C_T2
                                     48 	.globl _CPRL2
                                     49 	.globl _CP_RL2
                                     50 	.globl _PT2
                                     51 	.globl _PS
                                     52 	.globl _PT1
                                     53 	.globl _PX1
                                     54 	.globl _PT0
                                     55 	.globl _PX0
                                     56 	.globl _EA
                                     57 	.globl _ET2
                                     58 	.globl _ES
                                     59 	.globl _ET1
                                     60 	.globl _EX1
                                     61 	.globl _ET0
                                     62 	.globl _EX0
                                     63 	.globl _PWR_UP
                                     64 	.globl _CE
                                     65 	.globl _DR2
                                     66 	.globl _DR2_CE
                                     67 	.globl _CLK2
                                     68 	.globl _DOUT2
                                     69 	.globl _CS
                                     70 	.globl _DR1
                                     71 	.globl _CLK1
                                     72 	.globl _DATA
                                     73 	.globl _SM0
                                     74 	.globl _SM1
                                     75 	.globl _SM2
                                     76 	.globl _REN
                                     77 	.globl _TB8
                                     78 	.globl _RB8
                                     79 	.globl _TI
                                     80 	.globl _RI
                                     81 	.globl _DIN0
                                     82 	.globl _P1_2
                                     83 	.globl _DIO1
                                     84 	.globl _P1_1
                                     85 	.globl _DIO0
                                     86 	.globl _T2
                                     87 	.globl _P1_0
                                     88 	.globl _TF1
                                     89 	.globl _TR1
                                     90 	.globl _TF0
                                     91 	.globl _TR0
                                     92 	.globl _IE1
                                     93 	.globl _IT1
                                     94 	.globl _IE0
                                     95 	.globl _IT0
                                     96 	.globl _DIO9
                                     97 	.globl _PWM
                                     98 	.globl _P0_7
                                     99 	.globl _DIO8
                                    100 	.globl _T1
                                    101 	.globl _P0_6
                                    102 	.globl _DIO7
                                    103 	.globl _T0
                                    104 	.globl _P0_5
                                    105 	.globl _DIO6
                                    106 	.globl _INT1_N
                                    107 	.globl _P0_4
                                    108 	.globl _DIO5
                                    109 	.globl _INT0_N
                                    110 	.globl _P0_3
                                    111 	.globl _DIO4
                                    112 	.globl _TXD
                                    113 	.globl _P0_2
                                    114 	.globl _DIO3
                                    115 	.globl _RXD
                                    116 	.globl _P0_1
                                    117 	.globl _DIO2
                                    118 	.globl _P0_0
                                    119 	.globl _EIP
                                    120 	.globl _B
                                    121 	.globl _EIE
                                    122 	.globl _ACC
                                    123 	.globl _EICON
                                    124 	.globl _PSW
                                    125 	.globl _TH2
                                    126 	.globl _TL2
                                    127 	.globl _RCAP2H
                                    128 	.globl _RCAP2L
                                    129 	.globl _T2CON
                                    130 	.globl _DEV_OFFSET
                                    131 	.globl _T2_1V2
                                    132 	.globl _T1_1V2
                                    133 	.globl _IP
                                    134 	.globl _TEST_MODE
                                    135 	.globl _CK_CTRL
                                    136 	.globl _TICK_DV
                                    137 	.globl _SPICLK
                                    138 	.globl _SPI_CTRL
                                    139 	.globl _SPI_DATA
                                    140 	.globl _RSTREAS
                                    141 	.globl _REGX_CTRL
                                    142 	.globl _REGX_LSB
                                    143 	.globl _REGX_MSB
                                    144 	.globl _PWMDUTY
                                    145 	.globl _PWMCON
                                    146 	.globl _IE
                                    147 	.globl _ADCSTATIC
                                    148 	.globl _ADCDATAL
                                    149 	.globl _ADCDATAH
                                    150 	.globl _ADCCON
                                    151 	.globl _RADIO
                                    152 	.globl _SBUF
                                    153 	.globl _SCON
                                    154 	.globl _P1_ALT
                                    155 	.globl _P1_DIR
                                    156 	.globl _P0_ALT
                                    157 	.globl _P0_DIR
                                    158 	.globl _MPAGE
                                    159 	.globl _EXIF
                                    160 	.globl _P1
                                    161 	.globl _SPC_FNC
                                    162 	.globl _CKCON
                                    163 	.globl _TH1
                                    164 	.globl _TH0
                                    165 	.globl _TL1
                                    166 	.globl _TL0
                                    167 	.globl _TMOD
                                    168 	.globl _TCON
                                    169 	.globl _PCON
                                    170 	.globl _DPS
                                    171 	.globl _DPH1
                                    172 	.globl _DPL1
                                    173 	.globl _DPH0
                                    174 	.globl _DPH
                                    175 	.globl _DPL0
                                    176 	.globl _DPL
                                    177 	.globl _SP
                                    178 	.globl _P0
                                    179 	.globl _Meassage
                                    180 	.globl _counter
                                    181 	.globl _cfg
                                    182 	.globl _rf_data
                                    183 	.globl _interrupt_rf
                                    184 ;--------------------------------------------------------
                                    185 ; special function registers
                                    186 ;--------------------------------------------------------
                                    187 	.area RSEG    (ABS,DATA)
      000000                        188 	.org 0x0000
                           000080   189 _P0	=	0x0080
                           000081   190 _SP	=	0x0081
                           000082   191 _DPL	=	0x0082
                           000082   192 _DPL0	=	0x0082
                           000083   193 _DPH	=	0x0083
                           000083   194 _DPH0	=	0x0083
                           000084   195 _DPL1	=	0x0084
                           000085   196 _DPH1	=	0x0085
                           000086   197 _DPS	=	0x0086
                           000087   198 _PCON	=	0x0087
                           000088   199 _TCON	=	0x0088
                           000089   200 _TMOD	=	0x0089
                           00008A   201 _TL0	=	0x008a
                           00008B   202 _TL1	=	0x008b
                           00008C   203 _TH0	=	0x008c
                           00008D   204 _TH1	=	0x008d
                           00008E   205 _CKCON	=	0x008e
                           00008F   206 _SPC_FNC	=	0x008f
                           000090   207 _P1	=	0x0090
                           000091   208 _EXIF	=	0x0091
                           000092   209 _MPAGE	=	0x0092
                           000094   210 _P0_DIR	=	0x0094
                           000095   211 _P0_ALT	=	0x0095
                           000096   212 _P1_DIR	=	0x0096
                           000097   213 _P1_ALT	=	0x0097
                           000098   214 _SCON	=	0x0098
                           000099   215 _SBUF	=	0x0099
                           0000A0   216 _RADIO	=	0x00a0
                           0000A1   217 _ADCCON	=	0x00a1
                           0000A2   218 _ADCDATAH	=	0x00a2
                           0000A3   219 _ADCDATAL	=	0x00a3
                           0000A4   220 _ADCSTATIC	=	0x00a4
                           0000A8   221 _IE	=	0x00a8
                           0000A9   222 _PWMCON	=	0x00a9
                           0000AA   223 _PWMDUTY	=	0x00aa
                           0000AB   224 _REGX_MSB	=	0x00ab
                           0000AC   225 _REGX_LSB	=	0x00ac
                           0000AD   226 _REGX_CTRL	=	0x00ad
                           0000B1   227 _RSTREAS	=	0x00b1
                           0000B2   228 _SPI_DATA	=	0x00b2
                           0000B3   229 _SPI_CTRL	=	0x00b3
                           0000B4   230 _SPICLK	=	0x00b4
                           0000B5   231 _TICK_DV	=	0x00b5
                           0000B6   232 _CK_CTRL	=	0x00b6
                           0000B7   233 _TEST_MODE	=	0x00b7
                           0000B8   234 _IP	=	0x00b8
                           0000BC   235 _T1_1V2	=	0x00bc
                           0000BD   236 _T2_1V2	=	0x00bd
                           0000BE   237 _DEV_OFFSET	=	0x00be
                           0000C8   238 _T2CON	=	0x00c8
                           0000CA   239 _RCAP2L	=	0x00ca
                           0000CB   240 _RCAP2H	=	0x00cb
                           0000CC   241 _TL2	=	0x00cc
                           0000CD   242 _TH2	=	0x00cd
                           0000D0   243 _PSW	=	0x00d0
                           0000D8   244 _EICON	=	0x00d8
                           0000E0   245 _ACC	=	0x00e0
                           0000E8   246 _EIE	=	0x00e8
                           0000F0   247 _B	=	0x00f0
                           0000F8   248 _EIP	=	0x00f8
                                    249 ;--------------------------------------------------------
                                    250 ; special function bits
                                    251 ;--------------------------------------------------------
                                    252 	.area RSEG    (ABS,DATA)
      000000                        253 	.org 0x0000
                           000080   254 _P0_0	=	0x0080
                           000080   255 _DIO2	=	0x0080
                           000081   256 _P0_1	=	0x0081
                           000081   257 _RXD	=	0x0081
                           000081   258 _DIO3	=	0x0081
                           000082   259 _P0_2	=	0x0082
                           000082   260 _TXD	=	0x0082
                           000082   261 _DIO4	=	0x0082
                           000083   262 _P0_3	=	0x0083
                           000083   263 _INT0_N	=	0x0083
                           000083   264 _DIO5	=	0x0083
                           000084   265 _P0_4	=	0x0084
                           000084   266 _INT1_N	=	0x0084
                           000084   267 _DIO6	=	0x0084
                           000085   268 _P0_5	=	0x0085
                           000085   269 _T0	=	0x0085
                           000085   270 _DIO7	=	0x0085
                           000086   271 _P0_6	=	0x0086
                           000086   272 _T1	=	0x0086
                           000086   273 _DIO8	=	0x0086
                           000087   274 _P0_7	=	0x0087
                           000087   275 _PWM	=	0x0087
                           000087   276 _DIO9	=	0x0087
                           000088   277 _IT0	=	0x0088
                           000089   278 _IE0	=	0x0089
                           00008A   279 _IT1	=	0x008a
                           00008B   280 _IE1	=	0x008b
                           00008C   281 _TR0	=	0x008c
                           00008D   282 _TF0	=	0x008d
                           00008E   283 _TR1	=	0x008e
                           00008F   284 _TF1	=	0x008f
                           000090   285 _P1_0	=	0x0090
                           000090   286 _T2	=	0x0090
                           000090   287 _DIO0	=	0x0090
                           000091   288 _P1_1	=	0x0091
                           000091   289 _DIO1	=	0x0091
                           000092   290 _P1_2	=	0x0092
                           000092   291 _DIN0	=	0x0092
                           000098   292 _RI	=	0x0098
                           000099   293 _TI	=	0x0099
                           00009A   294 _RB8	=	0x009a
                           00009B   295 _TB8	=	0x009b
                           00009C   296 _REN	=	0x009c
                           00009D   297 _SM2	=	0x009d
                           00009E   298 _SM1	=	0x009e
                           00009F   299 _SM0	=	0x009f
                           0000A0   300 _DATA	=	0x00a0
                           0000A1   301 _CLK1	=	0x00a1
                           0000A2   302 _DR1	=	0x00a2
                           0000A3   303 _CS	=	0x00a3
                           0000A4   304 _DOUT2	=	0x00a4
                           0000A5   305 _CLK2	=	0x00a5
                           0000A6   306 _DR2_CE	=	0x00a6
                           0000A6   307 _DR2	=	0x00a6
                           0000A6   308 _CE	=	0x00a6
                           0000A7   309 _PWR_UP	=	0x00a7
                           0000A8   310 _EX0	=	0x00a8
                           0000A9   311 _ET0	=	0x00a9
                           0000AA   312 _EX1	=	0x00aa
                           0000AB   313 _ET1	=	0x00ab
                           0000AC   314 _ES	=	0x00ac
                           0000AD   315 _ET2	=	0x00ad
                           0000AF   316 _EA	=	0x00af
                           0000B8   317 _PX0	=	0x00b8
                           0000B9   318 _PT0	=	0x00b9
                           0000BA   319 _PX1	=	0x00ba
                           0000BB   320 _PT1	=	0x00bb
                           0000BC   321 _PS	=	0x00bc
                           0000BD   322 _PT2	=	0x00bd
                           0000C8   323 _CP_RL2	=	0x00c8
                           0000C8   324 _CPRL2	=	0x00c8
                           0000C9   325 _C_T2	=	0x00c9
                           0000C9   326 _CT2	=	0x00c9
                           0000CA   327 _TR2	=	0x00ca
                           0000CB   328 _EXEN2	=	0x00cb
                           0000CC   329 _TCLK	=	0x00cc
                           0000CD   330 _RCLK	=	0x00cd
                           0000CE   331 _EXF2	=	0x00ce
                           0000CF   332 _TF2	=	0x00cf
                           0000D0   333 _P	=	0x00d0
                           0000D1   334 _F1	=	0x00d1
                           0000D2   335 _OV	=	0x00d2
                           0000D3   336 _RS0	=	0x00d3
                           0000D4   337 _RS1	=	0x00d4
                           0000D5   338 _F0	=	0x00d5
                           0000D6   339 _AC	=	0x00d6
                           0000D7   340 _CY	=	0x00d7
                           0000DB   341 _WDTI	=	0x00db
                           0000E8   342 _EX2	=	0x00e8
                           0000E9   343 _EX3	=	0x00e9
                           0000EA   344 _EX4	=	0x00ea
                           0000EB   345 _EX5	=	0x00eb
                           0000EC   346 _EWDI	=	0x00ec
                           0000F8   347 _PX2	=	0x00f8
                           0000F9   348 _PX3	=	0x00f9
                           0000FA   349 _PX4	=	0x00fa
                           0000FB   350 _PX5	=	0x00fb
                           0000FC   351 _PWDI	=	0x00fc
                                    352 ;--------------------------------------------------------
                                    353 ; overlayable register banks
                                    354 ;--------------------------------------------------------
                                    355 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        356 	.ds 8
                                    357 ;--------------------------------------------------------
                                    358 ; overlayable bit register bank
                                    359 ;--------------------------------------------------------
                                    360 	.area BIT_BANK	(REL,OVR,DATA)
      000020                        361 bits:
      000020                        362 	.ds 1
                           008000   363 	b0 = bits[0]
                           008100   364 	b1 = bits[1]
                           008200   365 	b2 = bits[2]
                           008300   366 	b3 = bits[3]
                           008400   367 	b4 = bits[4]
                           008500   368 	b5 = bits[5]
                           008600   369 	b6 = bits[6]
                           008700   370 	b7 = bits[7]
                                    371 ;--------------------------------------------------------
                                    372 ; internal ram data
                                    373 ;--------------------------------------------------------
                                    374 	.area DSEG    (DATA)
      000021                        375 _rf_data::
      000021                        376 	.ds 15
      000030                        377 _cfg::
      000030                        378 	.ds 3
      000033                        379 _counter::
      000033                        380 	.ds 1
      000034                        381 _Meassage::
      000034                        382 	.ds 41
                                    383 ;--------------------------------------------------------
                                    384 ; overlayable items in internal ram 
                                    385 ;--------------------------------------------------------
                                    386 ;--------------------------------------------------------
                                    387 ; Stack segment in internal ram 
                                    388 ;--------------------------------------------------------
                                    389 	.area	SSEG
      000079                        390 __start__stack:
      000079                        391 	.ds	1
                                    392 
                                    393 ;--------------------------------------------------------
                                    394 ; indirectly addressable internal ram data
                                    395 ;--------------------------------------------------------
                                    396 	.area ISEG    (DATA)
                                    397 ;--------------------------------------------------------
                                    398 ; absolute internal ram data
                                    399 ;--------------------------------------------------------
                                    400 	.area IABS    (ABS,DATA)
                                    401 	.area IABS    (ABS,DATA)
                                    402 ;--------------------------------------------------------
                                    403 ; bit data
                                    404 ;--------------------------------------------------------
                                    405 	.area BSEG    (BIT)
                                    406 ;--------------------------------------------------------
                                    407 ; paged external ram data
                                    408 ;--------------------------------------------------------
                                    409 	.area PSEG    (PAG,XDATA)
                                    410 ;--------------------------------------------------------
                                    411 ; external ram data
                                    412 ;--------------------------------------------------------
                                    413 	.area XSEG    (XDATA)
                                    414 ;--------------------------------------------------------
                                    415 ; absolute external ram data
                                    416 ;--------------------------------------------------------
                                    417 	.area XABS    (ABS,XDATA)
                                    418 ;--------------------------------------------------------
                                    419 ; external initialized ram data
                                    420 ;--------------------------------------------------------
                                    421 	.area XISEG   (XDATA)
                                    422 	.area HOME    (CODE)
                                    423 	.area GSINIT0 (CODE)
                                    424 	.area GSINIT1 (CODE)
                                    425 	.area GSINIT2 (CODE)
                                    426 	.area GSINIT3 (CODE)
                                    427 	.area GSINIT4 (CODE)
                                    428 	.area GSINIT5 (CODE)
                                    429 	.area GSINIT  (CODE)
                                    430 	.area GSFINAL (CODE)
                                    431 	.area CSEG    (CODE)
                                    432 ;--------------------------------------------------------
                                    433 ; interrupt vector 
                                    434 ;--------------------------------------------------------
                                    435 	.area HOME    (CODE)
      000000                        436 __interrupt_vect:
      000000 02 00 59         [24]  437 	ljmp	__sdcc_gsinit_startup
      000003 32               [24]  438 	reti
      000004                        439 	.ds	7
      00000B 32               [24]  440 	reti
      00000C                        441 	.ds	7
      000013 32               [24]  442 	reti
      000014                        443 	.ds	7
      00001B 32               [24]  444 	reti
      00001C                        445 	.ds	7
      000023 32               [24]  446 	reti
      000024                        447 	.ds	7
      00002B 32               [24]  448 	reti
      00002C                        449 	.ds	7
      000033 32               [24]  450 	reti
      000034                        451 	.ds	7
      00003B 32               [24]  452 	reti
      00003C                        453 	.ds	7
      000043 32               [24]  454 	reti
      000044                        455 	.ds	7
      00004B 32               [24]  456 	reti
      00004C                        457 	.ds	7
      000053 02 01 50         [24]  458 	ljmp	_interrupt_rf
                                    459 ;--------------------------------------------------------
                                    460 ; global & static initialisations
                                    461 ;--------------------------------------------------------
                                    462 	.area HOME    (CODE)
                                    463 	.area GSINIT  (CODE)
                                    464 	.area GSFINAL (CODE)
                                    465 	.area GSINIT  (CODE)
                                    466 	.globl __sdcc_gsinit_startup
                                    467 	.globl __sdcc_program_startup
                                    468 	.globl __start__stack
                                    469 	.globl __mcs51_genXINIT
                                    470 	.globl __mcs51_genXRAMCLEAR
                                    471 	.globl __mcs51_genRAMCLEAR
                                    472 ;	../src/main.c:24: struct rf_config rf_data = {
      0000B2 75 21 00         [24]  473 	mov	_rf_data,#0x00
      0000B5 75 22 E0         [24]  474 	mov	(_rf_data + 0x0001),#0xE0
      0000B8 75 23 00         [24]  475 	mov	(_rf_data + 0x0002),#0x00
      0000BB 75 24 00         [24]  476 	mov	(_rf_data + 0x0003),#0x00
      0000BE 75 25 00         [24]  477 	mov	(_rf_data + 0x0004),#0x00
      0000C1 75 26 00         [24]  478 	mov	(_rf_data + 0x0005),#0x00
      0000C4 75 27 00         [24]  479 	mov	(_rf_data + 0x0006),#0x00
      0000C7 75 28 00         [24]  480 	mov	(_rf_data + 0x0007),#0x00
      0000CA 75 29 00         [24]  481 	mov	(_rf_data + 0x0008),#0x00
      0000CD 75 2A F2         [24]  482 	mov	(_rf_data + 0x0009),#0xF2
      0000D0 75 2B F2         [24]  483 	mov	(_rf_data + 0x000a),#0xF2
      0000D3 75 2C F2         [24]  484 	mov	(_rf_data + 0x000b),#0xF2
      0000D6 75 2D 61         [24]  485 	mov	(_rf_data + 0x000c),#0x61
      0000D9 75 2E 6F         [24]  486 	mov	(_rf_data + 0x000d),#0x6F
      0000DC 75 2F 15         [24]  487 	mov	(_rf_data + 0x000e),#0x15
                                    488 ;	../src/main.c:32: struct rf_config *cfg = &rf_data;
      0000DF 75 30 21         [24]  489 	mov	_cfg,#_rf_data
      0000E2 75 31 00         [24]  490 	mov	(_cfg + 1),#0x00
      0000E5 75 32 40         [24]  491 	mov	(_cfg + 2),#0x40
                                    492 ;	../src/main.c:34: unsigned char counter = 1;
      0000E8 75 33 01         [24]  493 	mov	_counter,#0x01
                                    494 	.area GSFINAL (CODE)
      0000EB 02 00 56         [24]  495 	ljmp	__sdcc_program_startup
                                    496 ;--------------------------------------------------------
                                    497 ; Home
                                    498 ;--------------------------------------------------------
                                    499 	.area HOME    (CODE)
                                    500 	.area HOME    (CODE)
      000056                        501 __sdcc_program_startup:
      000056 02 00 EE         [24]  502 	ljmp	_main
                                    503 ;	return from main will return to caller
                                    504 ;--------------------------------------------------------
                                    505 ; code
                                    506 ;--------------------------------------------------------
                                    507 	.area CSEG    (CODE)
                                    508 ;------------------------------------------------------------
                                    509 ;Allocation info for local variables in function 'main'
                                    510 ;------------------------------------------------------------
                                    511 ;i                         Allocated to registers r6 r7 
                                    512 ;------------------------------------------------------------
                                    513 ;	../src/main.c:38: void main()
                                    514 ;	-----------------------------------------
                                    515 ;	 function main
                                    516 ;	-----------------------------------------
      0000EE                        517 _main:
                           000007   518 	ar7 = 0x07
                           000006   519 	ar6 = 0x06
                           000005   520 	ar5 = 0x05
                           000004   521 	ar4 = 0x04
                           000003   522 	ar3 = 0x03
                           000002   523 	ar2 = 0x02
                           000001   524 	ar1 = 0x01
                           000000   525 	ar0 = 0x00
                                    526 ;	../src/main.c:41: store_cpu_rate(16);
      0000EE 90 00 10         [24]  527 	mov	dptr,#(0x10&0x00ff)
      0000F1 E4               [12]  528 	clr	a
      0000F2 F5 F0            [12]  529 	mov	b,a
      0000F4 12 02 D9         [24]  530 	lcall	_store_cpu_rate
                                    531 ;	../src/main.c:43: serial_init(19200);
      0000F7 90 4B 00         [24]  532 	mov	dptr,#0x4B00
      0000FA 12 02 45         [24]  533 	lcall	_serial_init
                                    534 ;	../src/main.c:45: P0_DIR &= ~0x28;
      0000FD AF 94            [24]  535 	mov	r7,_P0_DIR
      0000FF 74 D7            [12]  536 	mov	a,#0xD7
      000101 5F               [12]  537 	anl	a,r7
      000102 F5 94            [12]  538 	mov	_P0_DIR,a
                                    539 ;	../src/main.c:46: P0_ALT &= ~0x28;
      000104 AF 95            [24]  540 	mov	r7,_P0_ALT
      000106 74 D7            [12]  541 	mov	a,#0xD7
      000108 5F               [12]  542 	anl	a,r7
      000109 F5 95            [12]  543 	mov	_P0_ALT,a
                                    544 ;	../src/main.c:48: rf_init();
      00010B 12 04 74         [24]  545 	lcall	_poll_rf_init
                                    546 ;	../src/main.c:49: rf_configure(cfg);
      00010E 85 30 82         [24]  547 	mov	dpl,_cfg
      000111 85 31 83         [24]  548 	mov	dph,(_cfg + 1)
      000114 85 32 F0         [24]  549 	mov	b,(_cfg + 2)
      000117 12 04 7F         [24]  550 	lcall	_poll_rf_configure
                                    551 ;	../src/main.c:51: EA = 1;
      00011A D2 AF            [12]  552 	setb	_EA
                                    553 ;	../src/main.c:52: EX4 = 1;
      00011C D2 EA            [12]  554 	setb	_EX4
                                    555 ;	../src/main.c:53: for(i=0;i<6;i++)
      00011E 7E 00            [12]  556 	mov	r6,#0x00
      000120 7F 00            [12]  557 	mov	r7,#0x00
      000122                        558 00105$:
                                    559 ;	../src/main.c:55: blink_led();
      000122 63 80 20         [24]  560 	xrl	_P0,#0x20
                                    561 ;	../src/main.c:56: mdelay(500);
      000125 90 01 F4         [24]  562 	mov	dptr,#0x01F4
      000128 C0 07            [24]  563 	push	ar7
      00012A C0 06            [24]  564 	push	ar6
      00012C 12 02 EA         [24]  565 	lcall	_mdelay
      00012F D0 06            [24]  566 	pop	ar6
      000131 D0 07            [24]  567 	pop	ar7
                                    568 ;	../src/main.c:53: for(i=0;i<6;i++)
      000133 0E               [12]  569 	inc	r6
      000134 BE 00 01         [24]  570 	cjne	r6,#0x00,00119$
      000137 0F               [12]  571 	inc	r7
      000138                        572 00119$:
      000138 C3               [12]  573 	clr	c
      000139 EE               [12]  574 	mov	a,r6
      00013A 94 06            [12]  575 	subb	a,#0x06
      00013C EF               [12]  576 	mov	a,r7
      00013D 64 80            [12]  577 	xrl	a,#0x80
      00013F 94 80            [12]  578 	subb	a,#0x80
      000141 40 DF            [24]  579 	jc	00105$
                                    580 ;	../src/main.c:59: puts("Listener startup.\n\r");
      000143 90 05 CF         [24]  581 	mov	dptr,#___str_0
      000146 75 F0 80         [24]  582 	mov	b,#0x80
      000149 12 02 64         [24]  583 	lcall	_puts
                                    584 ;	../src/main.c:60: while(1) {
      00014C                        585 00103$:
                                    586 ;	../src/main.c:61: CE = 1;
      00014C D2 A6            [12]  587 	setb	_CE
      00014E 80 FC            [24]  588 	sjmp	00103$
                                    589 ;------------------------------------------------------------
                                    590 ;Allocation info for local variables in function 'interrupt_rf'
                                    591 ;------------------------------------------------------------
                                    592 ;	../src/main.c:77: void interrupt_rf() __interrupt 10
                                    593 ;	-----------------------------------------
                                    594 ;	 function interrupt_rf
                                    595 ;	-----------------------------------------
      000150                        596 _interrupt_rf:
      000150 C0 20            [24]  597 	push	bits
      000152 C0 E0            [24]  598 	push	acc
      000154 C0 F0            [24]  599 	push	b
      000156 C0 82            [24]  600 	push	dpl
      000158 C0 83            [24]  601 	push	dph
      00015A C0 07            [24]  602 	push	(0+7)
      00015C C0 06            [24]  603 	push	(0+6)
      00015E C0 05            [24]  604 	push	(0+5)
      000160 C0 04            [24]  605 	push	(0+4)
      000162 C0 03            [24]  606 	push	(0+3)
      000164 C0 02            [24]  607 	push	(0+2)
      000166 C0 01            [24]  608 	push	(0+1)
      000168 C0 00            [24]  609 	push	(0+0)
      00016A C0 D0            [24]  610 	push	psw
      00016C 75 D0 00         [24]  611 	mov	psw,#0x00
                                    612 ;	../src/main.c:79: while (DR1) {
      00016F                        613 00106$:
      00016F 30 A2 61         [24]  614 	jnb	_DR1,00108$
                                    615 ;	../src/main.c:80: if( counter  < RF_LENGTH ){
      000172 74 E4            [12]  616 	mov	a,#0x100 - 0x1C
      000174 25 33            [12]  617 	add	a,_counter
      000176 40 4D            [24]  618 	jc	00104$
                                    619 ;	../src/main.c:81: if( counter == 0 )
      000178 E5 33            [12]  620 	mov	a,_counter
      00017A 70 09            [24]  621 	jnz	00102$
                                    622 ;	../src/main.c:82: puts( "FeedBack: \n" );
      00017C 90 05 E3         [24]  623 	mov	dptr,#___str_1
      00017F 75 F0 80         [24]  624 	mov	b,#0x80
      000182 12 02 64         [24]  625 	lcall	_puts
      000185                        626 00102$:
                                    627 ;	../src/main.c:83: Meassage[counter++] = spi_write_then_read(0);
      000185 AF 33            [24]  628 	mov	r7,_counter
      000187 05 33            [12]  629 	inc	_counter
      000189 EF               [12]  630 	mov	a,r7
      00018A 24 34            [12]  631 	add	a,#_Meassage
      00018C F9               [12]  632 	mov	r1,a
      00018D 75 82 00         [24]  633 	mov	dpl,#0x00
      000190 C0 01            [24]  634 	push	ar1
      000192 12 05 A0         [24]  635 	lcall	_spi_write_then_read
      000195 E5 82            [12]  636 	mov	a,dpl
      000197 D0 01            [24]  637 	pop	ar1
      000199 F7               [12]  638 	mov	@r1,a
                                    639 ;	../src/main.c:84: putc( ( (Meassage[counter-1]>>4) & 0xff ) + 48 );
      00019A E5 33            [12]  640 	mov	a,_counter
      00019C 14               [12]  641 	dec	a
      00019D 24 34            [12]  642 	add	a,#_Meassage
      00019F F9               [12]  643 	mov	r1,a
      0001A0 E7               [12]  644 	mov	a,@r1
      0001A1 C4               [12]  645 	swap	a
      0001A2 54 0F            [12]  646 	anl	a,#0x0F
      0001A4 24 30            [12]  647 	add	a,#0x30
      0001A6 F5 82            [12]  648 	mov	dpl,a
      0001A8 12 02 61         [24]  649 	lcall	_putc
                                    650 ;	../src/main.c:85: putc( ( Meassage[counter-1] & 0x0f ) + 48 );
      0001AB E5 33            [12]  651 	mov	a,_counter
      0001AD 14               [12]  652 	dec	a
      0001AE 24 34            [12]  653 	add	a,#_Meassage
      0001B0 F9               [12]  654 	mov	r1,a
      0001B1 87 07            [24]  655 	mov	ar7,@r1
      0001B3 74 0F            [12]  656 	mov	a,#0x0F
      0001B5 5F               [12]  657 	anl	a,r7
      0001B6 24 30            [12]  658 	add	a,#0x30
      0001B8 F5 82            [12]  659 	mov	dpl,a
      0001BA 12 02 61         [24]  660 	lcall	_putc
                                    661 ;	../src/main.c:86: putc( ' ' );
      0001BD 75 82 20         [24]  662 	mov	dpl,#0x20
      0001C0 12 02 61         [24]  663 	lcall	_putc
      0001C3 80 AA            [24]  664 	sjmp	00106$
      0001C5                        665 00104$:
                                    666 ;	../src/main.c:89: counter = 1;
      0001C5 75 33 01         [24]  667 	mov	_counter,#0x01
                                    668 ;	../src/main.c:90: puts("\n");
      0001C8 90 05 EF         [24]  669 	mov	dptr,#___str_2
      0001CB 75 F0 80         [24]  670 	mov	b,#0x80
      0001CE 12 02 64         [24]  671 	lcall	_puts
      0001D1 80 9C            [24]  672 	sjmp	00106$
      0001D3                        673 00108$:
                                    674 ;	../src/main.c:95: CE = 0;
      0001D3 C2 A6            [12]  675 	clr	_CE
                                    676 ;	../src/main.c:96: EXIF &= ~0x40;
      0001D5 AF 91            [24]  677 	mov	r7,_EXIF
      0001D7 74 BF            [12]  678 	mov	a,#0xBF
      0001D9 5F               [12]  679 	anl	a,r7
      0001DA F5 91            [12]  680 	mov	_EXIF,a
      0001DC D0 D0            [24]  681 	pop	psw
      0001DE D0 00            [24]  682 	pop	(0+0)
      0001E0 D0 01            [24]  683 	pop	(0+1)
      0001E2 D0 02            [24]  684 	pop	(0+2)
      0001E4 D0 03            [24]  685 	pop	(0+3)
      0001E6 D0 04            [24]  686 	pop	(0+4)
      0001E8 D0 05            [24]  687 	pop	(0+5)
      0001EA D0 06            [24]  688 	pop	(0+6)
      0001EC D0 07            [24]  689 	pop	(0+7)
      0001EE D0 83            [24]  690 	pop	dph
      0001F0 D0 82            [24]  691 	pop	dpl
      0001F2 D0 F0            [24]  692 	pop	b
      0001F4 D0 E0            [24]  693 	pop	acc
      0001F6 D0 20            [24]  694 	pop	bits
      0001F8 32               [24]  695 	reti
                                    696 	.area CSEG    (CODE)
                                    697 	.area CONST   (CODE)
      0005CF                        698 ___str_0:
      0005CF 4C 69 73 74 65 6E 65   699 	.ascii "Listener startup."
             72 20 73 74 61 72 74
             75 70 2E
      0005E0 0A                     700 	.db 0x0A
      0005E1 0D                     701 	.db 0x0D
      0005E2 00                     702 	.db 0x00
      0005E3                        703 ___str_1:
      0005E3 46 65 65 64 42 61 63   704 	.ascii "FeedBack: "
             6B 3A 20
      0005ED 0A                     705 	.db 0x0A
      0005EE 00                     706 	.db 0x00
      0005EF                        707 ___str_2:
      0005EF 0A                     708 	.db 0x0A
      0005F0 00                     709 	.db 0x00
                                    710 	.area XINIT   (CODE)
                                    711 	.area CABS    (ABS,CODE)
