                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 2.9.0 #5416 (Mar 22 2009) (MINGW32)
                              4 ; This file was generated Sat Feb 15 20:54:43 2014
                              5 ;--------------------------------------------------------
                              6 	.module mainBase
                              7 	.optsdcc -mmcs51 --model-small
                              8 	
                              9 ;--------------------------------------------------------
                             10 ; Public variables in this module
                             11 ;--------------------------------------------------------
                             12 	.globl _main
                             13 	.globl _PWDI
                             14 	.globl _PX5
                             15 	.globl _PX4
                             16 	.globl _PX3
                             17 	.globl _PX2
                             18 	.globl _EWDI
                             19 	.globl _EX5
                             20 	.globl _EX4
                             21 	.globl _EX3
                             22 	.globl _EX2
                             23 	.globl _WDTI
                             24 	.globl _CY
                             25 	.globl _AC
                             26 	.globl _F0
                             27 	.globl _RS1
                             28 	.globl _RS0
                             29 	.globl _OV
                             30 	.globl _F1
                             31 	.globl _P
                             32 	.globl _TF2
                             33 	.globl _EXF2
                             34 	.globl _RCLK
                             35 	.globl _TCLK
                             36 	.globl _EXEN2
                             37 	.globl _TR2
                             38 	.globl _CT2
                             39 	.globl _C_T2
                             40 	.globl _CPRL2
                             41 	.globl _CP_RL2
                             42 	.globl _PT2
                             43 	.globl _PS
                             44 	.globl _PT1
                             45 	.globl _PX1
                             46 	.globl _PT0
                             47 	.globl _PX0
                             48 	.globl _EA
                             49 	.globl _ET2
                             50 	.globl _ES
                             51 	.globl _ET1
                             52 	.globl _EX1
                             53 	.globl _ET0
                             54 	.globl _EX0
                             55 	.globl _PWR_UP
                             56 	.globl _CE
                             57 	.globl _DR2
                             58 	.globl _DR2_CE
                             59 	.globl _CLK2
                             60 	.globl _DOUT2
                             61 	.globl _CS
                             62 	.globl _DR1
                             63 	.globl _CLK1
                             64 	.globl _DATA
                             65 	.globl _SM0
                             66 	.globl _SM1
                             67 	.globl _SM2
                             68 	.globl _REN
                             69 	.globl _TB8
                             70 	.globl _RB8
                             71 	.globl _TI
                             72 	.globl _RI
                             73 	.globl _DIN0
                             74 	.globl _P1_2
                             75 	.globl _DIO1
                             76 	.globl _P1_1
                             77 	.globl _DIO0
                             78 	.globl _T2
                             79 	.globl _P1_0
                             80 	.globl _TF1
                             81 	.globl _TR1
                             82 	.globl _TF0
                             83 	.globl _TR0
                             84 	.globl _IE1
                             85 	.globl _IT1
                             86 	.globl _IE0
                             87 	.globl _IT0
                             88 	.globl _DIO9
                             89 	.globl _PWM
                             90 	.globl _P0_7
                             91 	.globl _DIO8
                             92 	.globl _T1
                             93 	.globl _P0_6
                             94 	.globl _DIO7
                             95 	.globl _T0
                             96 	.globl _P0_5
                             97 	.globl _DIO6
                             98 	.globl _INT1_N
                             99 	.globl _P0_4
                            100 	.globl _DIO5
                            101 	.globl _INT0_N
                            102 	.globl _P0_3
                            103 	.globl _DIO4
                            104 	.globl _TXD
                            105 	.globl _P0_2
                            106 	.globl _DIO3
                            107 	.globl _RXD
                            108 	.globl _P0_1
                            109 	.globl _DIO2
                            110 	.globl _P0_0
                            111 	.globl _EIP
                            112 	.globl _B
                            113 	.globl _EIE
                            114 	.globl _ACC
                            115 	.globl _EICON
                            116 	.globl _PSW
                            117 	.globl _TH2
                            118 	.globl _TL2
                            119 	.globl _RCAP2H
                            120 	.globl _RCAP2L
                            121 	.globl _T2CON
                            122 	.globl _DEV_OFFSET
                            123 	.globl _T2_1V2
                            124 	.globl _T1_1V2
                            125 	.globl _IP
                            126 	.globl _TEST_MODE
                            127 	.globl _CK_CTRL
                            128 	.globl _TICK_DV
                            129 	.globl _SPICLK
                            130 	.globl _SPI_CTRL
                            131 	.globl _SPI_DATA
                            132 	.globl _RSTREAS
                            133 	.globl _REGX_CTRL
                            134 	.globl _REGX_LSB
                            135 	.globl _REGX_MSB
                            136 	.globl _PWMDUTY
                            137 	.globl _PWMCON
                            138 	.globl _IE
                            139 	.globl _ADCSTATIC
                            140 	.globl _ADCDATAL
                            141 	.globl _ADCDATAH
                            142 	.globl _ADCCON
                            143 	.globl _RADIO
                            144 	.globl _SBUF
                            145 	.globl _SCON
                            146 	.globl _P1_ALT
                            147 	.globl _P1_DIR
                            148 	.globl _P0_ALT
                            149 	.globl _P0_DIR
                            150 	.globl _MPAGE
                            151 	.globl _EXIF
                            152 	.globl _P1
                            153 	.globl _SPC_FNC
                            154 	.globl _CKCON
                            155 	.globl _TH1
                            156 	.globl _TH0
                            157 	.globl _TL1
                            158 	.globl _TL0
                            159 	.globl _TMOD
                            160 	.globl _TCON
                            161 	.globl _PCON
                            162 	.globl _DPS
                            163 	.globl _DPH1
                            164 	.globl _DPL1
                            165 	.globl _DPH0
                            166 	.globl _DPH
                            167 	.globl _DPL0
                            168 	.globl _DPL
                            169 	.globl _SP
                            170 	.globl _P0
                            171 	.globl _index
                            172 	.globl _i
                            173 	.globl _MessageBUF
                            174 	.globl _led_status
                            175 	.globl _dst_addr
                            176 	.globl _cfg
                            177 	.globl _rf_data
                            178 	.globl _interrupt_serial
                            179 ;--------------------------------------------------------
                            180 ; special function registers
                            181 ;--------------------------------------------------------
                            182 	.area RSEG    (DATA)
                    0080    183 _P0	=	0x0080
                    0081    184 _SP	=	0x0081
                    0082    185 _DPL	=	0x0082
                    0082    186 _DPL0	=	0x0082
                    0083    187 _DPH	=	0x0083
                    0083    188 _DPH0	=	0x0083
                    0084    189 _DPL1	=	0x0084
                    0085    190 _DPH1	=	0x0085
                    0086    191 _DPS	=	0x0086
                    0087    192 _PCON	=	0x0087
                    0088    193 _TCON	=	0x0088
                    0089    194 _TMOD	=	0x0089
                    008A    195 _TL0	=	0x008a
                    008B    196 _TL1	=	0x008b
                    008C    197 _TH0	=	0x008c
                    008D    198 _TH1	=	0x008d
                    008E    199 _CKCON	=	0x008e
                    008F    200 _SPC_FNC	=	0x008f
                    0090    201 _P1	=	0x0090
                    0091    202 _EXIF	=	0x0091
                    0092    203 _MPAGE	=	0x0092
                    0094    204 _P0_DIR	=	0x0094
                    0095    205 _P0_ALT	=	0x0095
                    0096    206 _P1_DIR	=	0x0096
                    0097    207 _P1_ALT	=	0x0097
                    0098    208 _SCON	=	0x0098
                    0099    209 _SBUF	=	0x0099
                    00A0    210 _RADIO	=	0x00a0
                    00A1    211 _ADCCON	=	0x00a1
                    00A2    212 _ADCDATAH	=	0x00a2
                    00A3    213 _ADCDATAL	=	0x00a3
                    00A4    214 _ADCSTATIC	=	0x00a4
                    00A8    215 _IE	=	0x00a8
                    00A9    216 _PWMCON	=	0x00a9
                    00AA    217 _PWMDUTY	=	0x00aa
                    00AB    218 _REGX_MSB	=	0x00ab
                    00AC    219 _REGX_LSB	=	0x00ac
                    00AD    220 _REGX_CTRL	=	0x00ad
                    00B1    221 _RSTREAS	=	0x00b1
                    00B2    222 _SPI_DATA	=	0x00b2
                    00B3    223 _SPI_CTRL	=	0x00b3
                    00B4    224 _SPICLK	=	0x00b4
                    00B5    225 _TICK_DV	=	0x00b5
                    00B6    226 _CK_CTRL	=	0x00b6
                    00B7    227 _TEST_MODE	=	0x00b7
                    00B8    228 _IP	=	0x00b8
                    00BC    229 _T1_1V2	=	0x00bc
                    00BD    230 _T2_1V2	=	0x00bd
                    00BE    231 _DEV_OFFSET	=	0x00be
                    00C8    232 _T2CON	=	0x00c8
                    00CA    233 _RCAP2L	=	0x00ca
                    00CB    234 _RCAP2H	=	0x00cb
                    00CC    235 _TL2	=	0x00cc
                    00CD    236 _TH2	=	0x00cd
                    00D0    237 _PSW	=	0x00d0
                    00D8    238 _EICON	=	0x00d8
                    00E0    239 _ACC	=	0x00e0
                    00E8    240 _EIE	=	0x00e8
                    00F0    241 _B	=	0x00f0
                    00F8    242 _EIP	=	0x00f8
                            243 ;--------------------------------------------------------
                            244 ; special function bits
                            245 ;--------------------------------------------------------
                            246 	.area RSEG    (DATA)
                    0080    247 _P0_0	=	0x0080
                    0080    248 _DIO2	=	0x0080
                    0081    249 _P0_1	=	0x0081
                    0081    250 _RXD	=	0x0081
                    0081    251 _DIO3	=	0x0081
                    0082    252 _P0_2	=	0x0082
                    0082    253 _TXD	=	0x0082
                    0082    254 _DIO4	=	0x0082
                    0083    255 _P0_3	=	0x0083
                    0083    256 _INT0_N	=	0x0083
                    0083    257 _DIO5	=	0x0083
                    0084    258 _P0_4	=	0x0084
                    0084    259 _INT1_N	=	0x0084
                    0084    260 _DIO6	=	0x0084
                    0085    261 _P0_5	=	0x0085
                    0085    262 _T0	=	0x0085
                    0085    263 _DIO7	=	0x0085
                    0086    264 _P0_6	=	0x0086
                    0086    265 _T1	=	0x0086
                    0086    266 _DIO8	=	0x0086
                    0087    267 _P0_7	=	0x0087
                    0087    268 _PWM	=	0x0087
                    0087    269 _DIO9	=	0x0087
                    0088    270 _IT0	=	0x0088
                    0089    271 _IE0	=	0x0089
                    008A    272 _IT1	=	0x008a
                    008B    273 _IE1	=	0x008b
                    008C    274 _TR0	=	0x008c
                    008D    275 _TF0	=	0x008d
                    008E    276 _TR1	=	0x008e
                    008F    277 _TF1	=	0x008f
                    0090    278 _P1_0	=	0x0090
                    0090    279 _T2	=	0x0090
                    0090    280 _DIO0	=	0x0090
                    0091    281 _P1_1	=	0x0091
                    0091    282 _DIO1	=	0x0091
                    0092    283 _P1_2	=	0x0092
                    0092    284 _DIN0	=	0x0092
                    0098    285 _RI	=	0x0098
                    0099    286 _TI	=	0x0099
                    009A    287 _RB8	=	0x009a
                    009B    288 _TB8	=	0x009b
                    009C    289 _REN	=	0x009c
                    009D    290 _SM2	=	0x009d
                    009E    291 _SM1	=	0x009e
                    009F    292 _SM0	=	0x009f
                    00A0    293 _DATA	=	0x00a0
                    00A1    294 _CLK1	=	0x00a1
                    00A2    295 _DR1	=	0x00a2
                    00A3    296 _CS	=	0x00a3
                    00A4    297 _DOUT2	=	0x00a4
                    00A5    298 _CLK2	=	0x00a5
                    00A6    299 _DR2_CE	=	0x00a6
                    00A6    300 _DR2	=	0x00a6
                    00A6    301 _CE	=	0x00a6
                    00A7    302 _PWR_UP	=	0x00a7
                    00A8    303 _EX0	=	0x00a8
                    00A9    304 _ET0	=	0x00a9
                    00AA    305 _EX1	=	0x00aa
                    00AB    306 _ET1	=	0x00ab
                    00AC    307 _ES	=	0x00ac
                    00AD    308 _ET2	=	0x00ad
                    00AF    309 _EA	=	0x00af
                    00B8    310 _PX0	=	0x00b8
                    00B9    311 _PT0	=	0x00b9
                    00BA    312 _PX1	=	0x00ba
                    00BB    313 _PT1	=	0x00bb
                    00BC    314 _PS	=	0x00bc
                    00BD    315 _PT2	=	0x00bd
                    00C8    316 _CP_RL2	=	0x00c8
                    00C8    317 _CPRL2	=	0x00c8
                    00C9    318 _C_T2	=	0x00c9
                    00C9    319 _CT2	=	0x00c9
                    00CA    320 _TR2	=	0x00ca
                    00CB    321 _EXEN2	=	0x00cb
                    00CC    322 _TCLK	=	0x00cc
                    00CD    323 _RCLK	=	0x00cd
                    00CE    324 _EXF2	=	0x00ce
                    00CF    325 _TF2	=	0x00cf
                    00D0    326 _P	=	0x00d0
                    00D1    327 _F1	=	0x00d1
                    00D2    328 _OV	=	0x00d2
                    00D3    329 _RS0	=	0x00d3
                    00D4    330 _RS1	=	0x00d4
                    00D5    331 _F0	=	0x00d5
                    00D6    332 _AC	=	0x00d6
                    00D7    333 _CY	=	0x00d7
                    00DB    334 _WDTI	=	0x00db
                    00E8    335 _EX2	=	0x00e8
                    00E9    336 _EX3	=	0x00e9
                    00EA    337 _EX4	=	0x00ea
                    00EB    338 _EX5	=	0x00eb
                    00EC    339 _EWDI	=	0x00ec
                    00F8    340 _PX2	=	0x00f8
                    00F9    341 _PX3	=	0x00f9
                    00FA    342 _PX4	=	0x00fa
                    00FB    343 _PX5	=	0x00fb
                    00FC    344 _PWDI	=	0x00fc
                            345 ;--------------------------------------------------------
                            346 ; overlayable register banks
                            347 ;--------------------------------------------------------
                            348 	.area REG_BANK_0	(REL,OVR,DATA)
   0000                     349 	.ds 8
                            350 ;--------------------------------------------------------
                            351 ; overlayable bit register bank
                            352 ;--------------------------------------------------------
                            353 	.area BIT_BANK	(REL,OVR,DATA)
   0020                     354 bits:
   0020                     355 	.ds 1
                    8000    356 	b0 = bits[0]
                    8100    357 	b1 = bits[1]
                    8200    358 	b2 = bits[2]
                    8300    359 	b3 = bits[3]
                    8400    360 	b4 = bits[4]
                    8500    361 	b5 = bits[5]
                    8600    362 	b6 = bits[6]
                    8700    363 	b7 = bits[7]
                            364 ;--------------------------------------------------------
                            365 ; internal ram data
                            366 ;--------------------------------------------------------
                            367 	.area DSEG    (DATA)
   0021                     368 _rf_data::
   0021                     369 	.ds 15
   0030                     370 _cfg::
   0030                     371 	.ds 3
   0033                     372 _dst_addr::
   0033                     373 	.ds 3
   0036                     374 _led_status::
   0036                     375 	.ds 1
   0037                     376 _MessageBUF::
   0037                     377 	.ds 41
   0060                     378 _i::
   0060                     379 	.ds 1
   0061                     380 _index::
   0061                     381 	.ds 1
                            382 ;--------------------------------------------------------
                            383 ; overlayable items in internal ram 
                            384 ;--------------------------------------------------------
                            385 	.area OSEG    (OVR,DATA)
                            386 ;--------------------------------------------------------
                            387 ; Stack segment in internal ram 
                            388 ;--------------------------------------------------------
                            389 	.area	SSEG	(DATA)
   007E                     390 __start__stack:
   007E                     391 	.ds	1
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
   0000                     436 __interrupt_vect:
   0000 02 00 2B            437 	ljmp	__sdcc_gsinit_startup
   0003 32                  438 	reti
   0004                     439 	.ds	7
   000B 32                  440 	reti
   000C                     441 	.ds	7
   0013 32                  442 	reti
   0014                     443 	.ds	7
   001B 32                  444 	reti
   001C                     445 	.ds	7
   0023 02 01 18            446 	ljmp	_interrupt_serial
                            447 ;--------------------------------------------------------
                            448 ; global & static initialisations
                            449 ;--------------------------------------------------------
                            450 	.area HOME    (CODE)
                            451 	.area GSINIT  (CODE)
                            452 	.area GSFINAL (CODE)
                            453 	.area GSINIT  (CODE)
                            454 	.globl __sdcc_gsinit_startup
                            455 	.globl __sdcc_program_startup
                            456 	.globl __start__stack
                            457 	.globl __mcs51_genXINIT
                            458 	.globl __mcs51_genXRAMCLEAR
                            459 	.globl __mcs51_genRAMCLEAR
                            460 ;	../src/mainBase.c:24: struct rf_config rf_data = {
   0084 75 21 00            461 	mov	_rf_data,#0x00
   0087 75 22 08            462 	mov	(_rf_data + 0x0001),#0x08
   008A 75 23 00            463 	mov	(_rf_data + 0x0002),#0x00
   008D 75 24 00            464 	mov	(_rf_data + 0x0003),#0x00
   0090 75 25 00            465 	mov	(_rf_data + 0x0004),#0x00
   0093 75 26 00            466 	mov	(_rf_data + 0x0005),#0x00
   0096 75 27 00            467 	mov	(_rf_data + 0x0006),#0x00
   0099 75 28 00            468 	mov	(_rf_data + 0x0007),#0x00
   009C 75 29 00            469 	mov	(_rf_data + 0x0008),#0x00
   009F 75 2A 02            470 	mov	(_rf_data + 0x0009),#0x02
   00A2 75 2B 02            471 	mov	(_rf_data + 0x000a),#0x02
   00A5 75 2C 02            472 	mov	(_rf_data + 0x000b),#0x02
   00A8 75 2D 61            473 	mov	(_rf_data + 0x000c),#0x61
   00AB 75 2E 6F            474 	mov	(_rf_data + 0x000d),#0x6F
   00AE 75 2F 14            475 	mov	(_rf_data + 0x000e),#0x14
                            476 ;	../src/mainBase.c:33: struct rf_config *cfg = &rf_data;
   00B1 75 30 21            477 	mov	_cfg,#_rf_data
   00B4 75 31 00            478 	mov	(_cfg + 1),#0x00
   00B7 75 32 40            479 	mov	(_cfg + 2),#0x40
                            480 ;	../src/mainBase.c:34: char dst_addr[3] = { 0x0f, 0x01, 0x01 };
   00BA 75 33 0F            481 	mov	_dst_addr,#0x0F
   00BD 75 34 01            482 	mov	(_dst_addr + 0x0001),#0x01
   00C0 75 35 01            483 	mov	(_dst_addr + 0x0002),#0x01
                            484 ;	../src/mainBase.c:39: unsigned char i = 0, index = 0;
   00C3 75 60 00            485 	mov	_i,#0x00
                            486 ;	../src/mainBase.c:39: 
   00C6 75 61 00            487 	mov	_index,#0x00
                            488 	.area GSFINAL (CODE)
   00C9 02 00 26            489 	ljmp	__sdcc_program_startup
                            490 ;--------------------------------------------------------
                            491 ; Home
                            492 ;--------------------------------------------------------
                            493 	.area HOME    (CODE)
                            494 	.area HOME    (CODE)
   0026                     495 __sdcc_program_startup:
   0026 12 00 CC            496 	lcall	_main
                            497 ;	return from main will lock up
   0029 80 FE               498 	sjmp .
                            499 ;--------------------------------------------------------
                            500 ; code
                            501 ;--------------------------------------------------------
                            502 	.area CSEG    (CODE)
                            503 ;------------------------------------------------------------
                            504 ;Allocation info for local variables in function 'main'
                            505 ;------------------------------------------------------------
                            506 ;------------------------------------------------------------
                            507 ;	../src/mainBase.c:41: void main()
                            508 ;	-----------------------------------------
                            509 ;	 function main
                            510 ;	-----------------------------------------
   00CC                     511 _main:
                    0002    512 	ar2 = 0x02
                    0003    513 	ar3 = 0x03
                    0004    514 	ar4 = 0x04
                    0005    515 	ar5 = 0x05
                    0006    516 	ar6 = 0x06
                    0007    517 	ar7 = 0x07
                    0000    518 	ar0 = 0x00
                    0001    519 	ar1 = 0x01
                            520 ;	../src/mainBase.c:44: store_cpu_rate(16);
   00CC 90 00 10            521 	mov	dptr,#(0x10&0x00ff)
   00CF E4                  522 	clr	a
   00D0 F5 F0               523 	mov	b,a
   00D2 12 02 57            524 	lcall	_store_cpu_rate
                            525 ;	../src/mainBase.c:46: serial_init(19200);
   00D5 90 4B 00            526 	mov	dptr,#0x4B00
   00D8 12 04 08            527 	lcall	_serial_init
                            528 ;	../src/mainBase.c:48: P0_DIR &= ~0x28;
   00DB 53 94 D7            529 	anl	_P0_DIR,#0xD7
                            530 ;	../src/mainBase.c:49: P0_ALT &= ~0x28;
   00DE 53 95 D7            531 	anl	_P0_ALT,#0xD7
                            532 ;	../src/mainBase.c:51: rf_init();
   00E1 12 01 77            533 	lcall	_poll_rf_init
                            534 ;	../src/mainBase.c:52: rf_configure(cfg);
   00E4 85 30 82            535 	mov	dpl,_cfg
   00E7 85 31 83            536 	mov	dph,(_cfg + 1)
   00EA 85 32 F0            537 	mov	b,(_cfg + 2)
   00ED 12 01 82            538 	lcall	_poll_rf_configure
                            539 ;	../src/mainBase.c:54: led_status = 'f';
   00F0 75 36 66            540 	mov	_led_status,#0x66
                            541 ;	../src/mainBase.c:55: EA = 1;
   00F3 D2 AF               542 	setb	_EA
                            543 ;	../src/mainBase.c:56: ES = 1;
   00F5 D2 AC               544 	setb	_ES
                            545 ;	../src/mainBase.c:57: for(i=0;i<6;i++)
   00F7 75 60 00            546 	mov	_i,#0x00
   00FA                     547 00104$:
   00FA 74 FA               548 	mov	a,#0x100 - 0x06
   00FC 25 60               549 	add	a,_i
   00FE 40 0D               550 	jc	00107$
                            551 ;	../src/mainBase.c:59: blink_led();
   0100 63 80 20            552 	xrl	_P0,#0x20
                            553 ;	../src/mainBase.c:60: mdelay(500);
   0103 90 01 F4            554 	mov	dptr,#0x01F4
   0106 12 02 68            555 	lcall	_mdelay
                            556 ;	../src/mainBase.c:57: for(i=0;i<6;i++)
   0109 05 60               557 	inc	_i
   010B 80 ED               558 	sjmp	00104$
   010D                     559 00107$:
                            560 ;	../src/mainBase.c:63: puts("Master startup.\n\r");
   010D 90 05 4B            561 	mov	dptr,#__str_0
   0110 75 F0 80            562 	mov	b,#0x80
   0113 12 04 27            563 	lcall	_puts
                            564 ;	../src/mainBase.c:64: while(1) {
   0116                     565 00102$:
   0116 80 FE               566 	sjmp	00102$
                            567 ;------------------------------------------------------------
                            568 ;Allocation info for local variables in function 'interrupt_serial'
                            569 ;------------------------------------------------------------
                            570 ;cmd                       Allocated to registers 
                            571 ;------------------------------------------------------------
                            572 ;	../src/mainBase.c:81: void interrupt_serial() interrupt 4
                            573 ;	-----------------------------------------
                            574 ;	 function interrupt_serial
                            575 ;	-----------------------------------------
   0118                     576 _interrupt_serial:
   0118 C0 20               577 	push	bits
   011A C0 E0               578 	push	acc
   011C C0 F0               579 	push	b
   011E C0 82               580 	push	dpl
   0120 C0 83               581 	push	dph
   0122 C0 02               582 	push	(0+2)
   0124 C0 03               583 	push	(0+3)
   0126 C0 04               584 	push	(0+4)
   0128 C0 05               585 	push	(0+5)
   012A C0 06               586 	push	(0+6)
   012C C0 07               587 	push	(0+7)
   012E C0 00               588 	push	(0+0)
   0130 C0 01               589 	push	(0+1)
   0132 C0 D0               590 	push	psw
   0134 75 D0 00            591 	mov	psw,#0x00
                            592 ;	../src/mainBase.c:85: blink_led();
   0137 63 80 20            593 	xrl	_P0,#0x20
                            594 ;	../src/mainBase.c:89: if(RI) {
                            595 ;	../src/mainBase.c:90: RI = 0; /* software clear serial receive interrupt*/
   013A 10 98 02            596 	jbc	_RI,00106$
   013D 80 1B               597 	sjmp	00103$
   013F                     598 00106$:
                            599 ;	../src/mainBase.c:91: cmd = SBUF; /* SBUF serial port data buffer */
   013F 85 99 36            600 	mov	_led_status,_SBUF
                            601 ;	../src/mainBase.c:95: rf_send(dst_addr, 3, &led_status, 1);
   0142 75 7A 36            602 	mov	_poll_rf_send_PARM_3,#_led_status
   0145 75 7B 00            603 	mov	(_poll_rf_send_PARM_3 + 1),#0x00
   0148 75 7C 40            604 	mov	(_poll_rf_send_PARM_3 + 2),#0x40
   014B 75 79 03            605 	mov	_poll_rf_send_PARM_2,#0x03
   014E 75 7D 01            606 	mov	_poll_rf_send_PARM_4,#0x01
   0151 90 00 33            607 	mov	dptr,#_dst_addr
   0154 75 F0 40            608 	mov	b,#0x40
   0157 12 01 CD            609 	lcall	_poll_rf_send
   015A                     610 00103$:
   015A D0 D0               611 	pop	psw
   015C D0 01               612 	pop	(0+1)
   015E D0 00               613 	pop	(0+0)
   0160 D0 07               614 	pop	(0+7)
   0162 D0 06               615 	pop	(0+6)
   0164 D0 05               616 	pop	(0+5)
   0166 D0 04               617 	pop	(0+4)
   0168 D0 03               618 	pop	(0+3)
   016A D0 02               619 	pop	(0+2)
   016C D0 83               620 	pop	dph
   016E D0 82               621 	pop	dpl
   0170 D0 F0               622 	pop	b
   0172 D0 E0               623 	pop	acc
   0174 D0 20               624 	pop	bits
   0176 32                  625 	reti
                            626 	.area CSEG    (CODE)
                            627 	.area CONST   (CODE)
   054B                     628 __str_0:
   054B 4D 61 73 74 65 72   629 	.ascii "Master startup."
        20 73 74 61 72 74
        75 70 2E
   055A 0A                  630 	.db 0x0A
   055B 0D                  631 	.db 0x0D
   055C 00                  632 	.db 0x00
                            633 	.area XINIT   (CODE)
                            634 	.area CABS    (ABS,CODE)
