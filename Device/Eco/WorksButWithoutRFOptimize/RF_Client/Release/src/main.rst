                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 2.9.0 #5416 (Mar 22 2009) (MINGW32)
                              4 ; This file was generated Thu Feb 20 23:48:31 2014
                              5 ;--------------------------------------------------------
                              6 	.module main
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
                            171 	.globl _Message
                            172 	.globl _HeaderFile
                            173 	.globl _codegenerator_status
                            174 	.globl _dst_addr
                            175 	.globl _cfg
                            176 	.globl _rf_data
                            177 	.globl _interrupt_rf
                            178 ;--------------------------------------------------------
                            179 ; special function registers
                            180 ;--------------------------------------------------------
                            181 	.area RSEG    (DATA)
                    0080    182 _P0	=	0x0080
                    0081    183 _SP	=	0x0081
                    0082    184 _DPL	=	0x0082
                    0082    185 _DPL0	=	0x0082
                    0083    186 _DPH	=	0x0083
                    0083    187 _DPH0	=	0x0083
                    0084    188 _DPL1	=	0x0084
                    0085    189 _DPH1	=	0x0085
                    0086    190 _DPS	=	0x0086
                    0087    191 _PCON	=	0x0087
                    0088    192 _TCON	=	0x0088
                    0089    193 _TMOD	=	0x0089
                    008A    194 _TL0	=	0x008a
                    008B    195 _TL1	=	0x008b
                    008C    196 _TH0	=	0x008c
                    008D    197 _TH1	=	0x008d
                    008E    198 _CKCON	=	0x008e
                    008F    199 _SPC_FNC	=	0x008f
                    0090    200 _P1	=	0x0090
                    0091    201 _EXIF	=	0x0091
                    0092    202 _MPAGE	=	0x0092
                    0094    203 _P0_DIR	=	0x0094
                    0095    204 _P0_ALT	=	0x0095
                    0096    205 _P1_DIR	=	0x0096
                    0097    206 _P1_ALT	=	0x0097
                    0098    207 _SCON	=	0x0098
                    0099    208 _SBUF	=	0x0099
                    00A0    209 _RADIO	=	0x00a0
                    00A1    210 _ADCCON	=	0x00a1
                    00A2    211 _ADCDATAH	=	0x00a2
                    00A3    212 _ADCDATAL	=	0x00a3
                    00A4    213 _ADCSTATIC	=	0x00a4
                    00A8    214 _IE	=	0x00a8
                    00A9    215 _PWMCON	=	0x00a9
                    00AA    216 _PWMDUTY	=	0x00aa
                    00AB    217 _REGX_MSB	=	0x00ab
                    00AC    218 _REGX_LSB	=	0x00ac
                    00AD    219 _REGX_CTRL	=	0x00ad
                    00B1    220 _RSTREAS	=	0x00b1
                    00B2    221 _SPI_DATA	=	0x00b2
                    00B3    222 _SPI_CTRL	=	0x00b3
                    00B4    223 _SPICLK	=	0x00b4
                    00B5    224 _TICK_DV	=	0x00b5
                    00B6    225 _CK_CTRL	=	0x00b6
                    00B7    226 _TEST_MODE	=	0x00b7
                    00B8    227 _IP	=	0x00b8
                    00BC    228 _T1_1V2	=	0x00bc
                    00BD    229 _T2_1V2	=	0x00bd
                    00BE    230 _DEV_OFFSET	=	0x00be
                    00C8    231 _T2CON	=	0x00c8
                    00CA    232 _RCAP2L	=	0x00ca
                    00CB    233 _RCAP2H	=	0x00cb
                    00CC    234 _TL2	=	0x00cc
                    00CD    235 _TH2	=	0x00cd
                    00D0    236 _PSW	=	0x00d0
                    00D8    237 _EICON	=	0x00d8
                    00E0    238 _ACC	=	0x00e0
                    00E8    239 _EIE	=	0x00e8
                    00F0    240 _B	=	0x00f0
                    00F8    241 _EIP	=	0x00f8
                            242 ;--------------------------------------------------------
                            243 ; special function bits
                            244 ;--------------------------------------------------------
                            245 	.area RSEG    (DATA)
                    0080    246 _P0_0	=	0x0080
                    0080    247 _DIO2	=	0x0080
                    0081    248 _P0_1	=	0x0081
                    0081    249 _RXD	=	0x0081
                    0081    250 _DIO3	=	0x0081
                    0082    251 _P0_2	=	0x0082
                    0082    252 _TXD	=	0x0082
                    0082    253 _DIO4	=	0x0082
                    0083    254 _P0_3	=	0x0083
                    0083    255 _INT0_N	=	0x0083
                    0083    256 _DIO5	=	0x0083
                    0084    257 _P0_4	=	0x0084
                    0084    258 _INT1_N	=	0x0084
                    0084    259 _DIO6	=	0x0084
                    0085    260 _P0_5	=	0x0085
                    0085    261 _T0	=	0x0085
                    0085    262 _DIO7	=	0x0085
                    0086    263 _P0_6	=	0x0086
                    0086    264 _T1	=	0x0086
                    0086    265 _DIO8	=	0x0086
                    0087    266 _P0_7	=	0x0087
                    0087    267 _PWM	=	0x0087
                    0087    268 _DIO9	=	0x0087
                    0088    269 _IT0	=	0x0088
                    0089    270 _IE0	=	0x0089
                    008A    271 _IT1	=	0x008a
                    008B    272 _IE1	=	0x008b
                    008C    273 _TR0	=	0x008c
                    008D    274 _TF0	=	0x008d
                    008E    275 _TR1	=	0x008e
                    008F    276 _TF1	=	0x008f
                    0090    277 _P1_0	=	0x0090
                    0090    278 _T2	=	0x0090
                    0090    279 _DIO0	=	0x0090
                    0091    280 _P1_1	=	0x0091
                    0091    281 _DIO1	=	0x0091
                    0092    282 _P1_2	=	0x0092
                    0092    283 _DIN0	=	0x0092
                    0098    284 _RI	=	0x0098
                    0099    285 _TI	=	0x0099
                    009A    286 _RB8	=	0x009a
                    009B    287 _TB8	=	0x009b
                    009C    288 _REN	=	0x009c
                    009D    289 _SM2	=	0x009d
                    009E    290 _SM1	=	0x009e
                    009F    291 _SM0	=	0x009f
                    00A0    292 _DATA	=	0x00a0
                    00A1    293 _CLK1	=	0x00a1
                    00A2    294 _DR1	=	0x00a2
                    00A3    295 _CS	=	0x00a3
                    00A4    296 _DOUT2	=	0x00a4
                    00A5    297 _CLK2	=	0x00a5
                    00A6    298 _DR2_CE	=	0x00a6
                    00A6    299 _DR2	=	0x00a6
                    00A6    300 _CE	=	0x00a6
                    00A7    301 _PWR_UP	=	0x00a7
                    00A8    302 _EX0	=	0x00a8
                    00A9    303 _ET0	=	0x00a9
                    00AA    304 _EX1	=	0x00aa
                    00AB    305 _ET1	=	0x00ab
                    00AC    306 _ES	=	0x00ac
                    00AD    307 _ET2	=	0x00ad
                    00AF    308 _EA	=	0x00af
                    00B8    309 _PX0	=	0x00b8
                    00B9    310 _PT0	=	0x00b9
                    00BA    311 _PX1	=	0x00ba
                    00BB    312 _PT1	=	0x00bb
                    00BC    313 _PS	=	0x00bc
                    00BD    314 _PT2	=	0x00bd
                    00C8    315 _CP_RL2	=	0x00c8
                    00C8    316 _CPRL2	=	0x00c8
                    00C9    317 _C_T2	=	0x00c9
                    00C9    318 _CT2	=	0x00c9
                    00CA    319 _TR2	=	0x00ca
                    00CB    320 _EXEN2	=	0x00cb
                    00CC    321 _TCLK	=	0x00cc
                    00CD    322 _RCLK	=	0x00cd
                    00CE    323 _EXF2	=	0x00ce
                    00CF    324 _TF2	=	0x00cf
                    00D0    325 _P	=	0x00d0
                    00D1    326 _F1	=	0x00d1
                    00D2    327 _OV	=	0x00d2
                    00D3    328 _RS0	=	0x00d3
                    00D4    329 _RS1	=	0x00d4
                    00D5    330 _F0	=	0x00d5
                    00D6    331 _AC	=	0x00d6
                    00D7    332 _CY	=	0x00d7
                    00DB    333 _WDTI	=	0x00db
                    00E8    334 _EX2	=	0x00e8
                    00E9    335 _EX3	=	0x00e9
                    00EA    336 _EX4	=	0x00ea
                    00EB    337 _EX5	=	0x00eb
                    00EC    338 _EWDI	=	0x00ec
                    00F8    339 _PX2	=	0x00f8
                    00F9    340 _PX3	=	0x00f9
                    00FA    341 _PX4	=	0x00fa
                    00FB    342 _PX5	=	0x00fb
                    00FC    343 _PWDI	=	0x00fc
                            344 ;--------------------------------------------------------
                            345 ; overlayable register banks
                            346 ;--------------------------------------------------------
                            347 	.area REG_BANK_0	(REL,OVR,DATA)
   0000                     348 	.ds 8
                            349 ;--------------------------------------------------------
                            350 ; overlayable bit register bank
                            351 ;--------------------------------------------------------
                            352 	.area BIT_BANK	(REL,OVR,DATA)
   0020                     353 bits:
   0020                     354 	.ds 1
                    8000    355 	b0 = bits[0]
                    8100    356 	b1 = bits[1]
                    8200    357 	b2 = bits[2]
                    8300    358 	b3 = bits[3]
                    8400    359 	b4 = bits[4]
                    8500    360 	b5 = bits[5]
                    8600    361 	b6 = bits[6]
                    8700    362 	b7 = bits[7]
                            363 ;--------------------------------------------------------
                            364 ; internal ram data
                            365 ;--------------------------------------------------------
                            366 	.area DSEG    (DATA)
   0021                     367 _rf_data::
   0021                     368 	.ds 15
   0030                     369 _cfg::
   0030                     370 	.ds 3
   0033                     371 _dst_addr::
   0033                     372 	.ds 3
   0036                     373 _codegenerator_status::
   0036                     374 	.ds 1
   0037                     375 _HeaderFile::
   0037                     376 	.ds 4
   003B                     377 _interrupt_rf_counter_1_1:
   003B                     378 	.ds 1
                            379 ;--------------------------------------------------------
                            380 ; overlayable items in internal ram 
                            381 ;--------------------------------------------------------
                            382 	.area OSEG    (OVR,DATA)
                            383 ;--------------------------------------------------------
                            384 ; Stack segment in internal ram 
                            385 ;--------------------------------------------------------
                            386 	.area	SSEG	(DATA)
   0058                     387 __start__stack:
   0058                     388 	.ds	1
                            389 
                            390 ;--------------------------------------------------------
                            391 ; indirectly addressable internal ram data
                            392 ;--------------------------------------------------------
                            393 	.area ISEG    (DATA)
                            394 ;--------------------------------------------------------
                            395 ; absolute internal ram data
                            396 ;--------------------------------------------------------
                            397 	.area IABS    (ABS,DATA)
                            398 	.area IABS    (ABS,DATA)
                            399 ;--------------------------------------------------------
                            400 ; bit data
                            401 ;--------------------------------------------------------
                            402 	.area BSEG    (BIT)
                            403 ;--------------------------------------------------------
                            404 ; paged external ram data
                            405 ;--------------------------------------------------------
                            406 	.area PSEG    (PAG,XDATA)
                            407 ;--------------------------------------------------------
                            408 ; external ram data
                            409 ;--------------------------------------------------------
                            410 	.area XSEG    (XDATA)
   0000                     411 _Message::
   0000                     412 	.ds 40
                            413 ;--------------------------------------------------------
                            414 ; absolute external ram data
                            415 ;--------------------------------------------------------
                            416 	.area XABS    (ABS,XDATA)
                            417 ;--------------------------------------------------------
                            418 ; external initialized ram data
                            419 ;--------------------------------------------------------
                            420 	.area XISEG   (XDATA)
                            421 	.area HOME    (CODE)
                            422 	.area GSINIT0 (CODE)
                            423 	.area GSINIT1 (CODE)
                            424 	.area GSINIT2 (CODE)
                            425 	.area GSINIT3 (CODE)
                            426 	.area GSINIT4 (CODE)
                            427 	.area GSINIT5 (CODE)
                            428 	.area GSINIT  (CODE)
                            429 	.area GSFINAL (CODE)
                            430 	.area CSEG    (CODE)
                            431 ;--------------------------------------------------------
                            432 ; interrupt vector 
                            433 ;--------------------------------------------------------
                            434 	.area HOME    (CODE)
   0000                     435 __interrupt_vect:
   0000 02 00 5B            436 	ljmp	__sdcc_gsinit_startup
   0003 32                  437 	reti
   0004                     438 	.ds	7
   000B 32                  439 	reti
   000C                     440 	.ds	7
   0013 32                  441 	reti
   0014                     442 	.ds	7
   001B 32                  443 	reti
   001C                     444 	.ds	7
   0023 32                  445 	reti
   0024                     446 	.ds	7
   002B 32                  447 	reti
   002C                     448 	.ds	7
   0033 32                  449 	reti
   0034                     450 	.ds	7
   003B 32                  451 	reti
   003C                     452 	.ds	7
   0043 32                  453 	reti
   0044                     454 	.ds	7
   004B 32                  455 	reti
   004C                     456 	.ds	7
   0053 02 01 73            457 	ljmp	_interrupt_rf
                            458 ;--------------------------------------------------------
                            459 ; global & static initialisations
                            460 ;--------------------------------------------------------
                            461 	.area HOME    (CODE)
                            462 	.area GSINIT  (CODE)
                            463 	.area GSFINAL (CODE)
                            464 	.area GSINIT  (CODE)
                            465 	.globl __sdcc_gsinit_startup
                            466 	.globl __sdcc_program_startup
                            467 	.globl __start__stack
                            468 	.globl __mcs51_genXINIT
                            469 	.globl __mcs51_genXRAMCLEAR
                            470 	.globl __mcs51_genRAMCLEAR
                            471 ;	../src/main.c:37: struct rf_config rf_data = {
   00B4 75 21 00            472 	mov	_rf_data,#0x00
   00B7 75 22 E0            473 	mov	(_rf_data + 0x0001),#0xE0
   00BA 75 23 00            474 	mov	(_rf_data + 0x0002),#0x00
   00BD 75 24 00            475 	mov	(_rf_data + 0x0003),#0x00
   00C0 75 25 00            476 	mov	(_rf_data + 0x0004),#0x00
   00C3 75 26 00            477 	mov	(_rf_data + 0x0005),#0x00
   00C6 75 27 00            478 	mov	(_rf_data + 0x0006),#0x00
   00C9 75 28 00            479 	mov	(_rf_data + 0x0007),#0x00
   00CC 75 29 00            480 	mov	(_rf_data + 0x0008),#0x00
   00CF 75 2A 0F            481 	mov	(_rf_data + 0x0009),#0x0F
   00D2 75 2B 01            482 	mov	(_rf_data + 0x000a),#0x01
   00D5 75 2C 01            483 	mov	(_rf_data + 0x000b),#0x01
   00D8 75 2D 61            484 	mov	(_rf_data + 0x000c),#0x61
   00DB 75 2E 6F            485 	mov	(_rf_data + 0x000d),#0x6F
   00DE 75 2F 15            486 	mov	(_rf_data + 0x000e),#0x15
                            487 ;	../src/main.c:45: struct rf_config *cfg = &rf_data;
   00E1 75 30 21            488 	mov	_cfg,#_rf_data
   00E4 75 31 00            489 	mov	(_cfg + 1),#0x00
   00E7 75 32 40            490 	mov	(_cfg + 2),#0x40
                            491 ;	../src/main.c:46: char dst_addr[3] = { 0x02, 0x02, 0x02 };
   00EA 75 33 02            492 	mov	_dst_addr,#0x02
   00ED 75 34 02            493 	mov	(_dst_addr + 0x0001),#0x02
   00F0 75 35 02            494 	mov	(_dst_addr + 0x0002),#0x02
                            495 	.area GSFINAL (CODE)
   00F3 02 00 56            496 	ljmp	__sdcc_program_startup
                            497 ;--------------------------------------------------------
                            498 ; Home
                            499 ;--------------------------------------------------------
                            500 	.area HOME    (CODE)
                            501 	.area HOME    (CODE)
   0056                     502 __sdcc_program_startup:
   0056 12 00 F6            503 	lcall	_main
                            504 ;	return from main will lock up
   0059 80 FE               505 	sjmp .
                            506 ;--------------------------------------------------------
                            507 ; code
                            508 ;--------------------------------------------------------
                            509 	.area CSEG    (CODE)
                            510 ;------------------------------------------------------------
                            511 ;Allocation info for local variables in function 'main'
                            512 ;------------------------------------------------------------
                            513 ;i                         Allocated to registers r2 r3 
                            514 ;------------------------------------------------------------
                            515 ;	../src/main.c:53: void main()
                            516 ;	-----------------------------------------
                            517 ;	 function main
                            518 ;	-----------------------------------------
   00F6                     519 _main:
                    0002    520 	ar2 = 0x02
                    0003    521 	ar3 = 0x03
                    0004    522 	ar4 = 0x04
                    0005    523 	ar5 = 0x05
                    0006    524 	ar6 = 0x06
                    0007    525 	ar7 = 0x07
                    0000    526 	ar0 = 0x00
                    0001    527 	ar1 = 0x01
                            528 ;	../src/main.c:57: store_cpu_rate(16);
   00F6 90 00 10            529 	mov	dptr,#(0x10&0x00ff)
   00F9 E4                  530 	clr	a
   00FA F5 F0               531 	mov	b,a
   00FC 12 03 2B            532 	lcall	_store_cpu_rate
                            533 ;	../src/main.c:59: serial_init(19200);
   00FF 90 4B 00            534 	mov	dptr,#0x4B00
   0102 12 04 57            535 	lcall	_serial_init
                            536 ;	../src/main.c:61: P0_DIR &= ~0x28;
   0105 53 94 D7            537 	anl	_P0_DIR,#0xD7
                            538 ;	../src/main.c:62: P0_ALT &= ~0x28;
   0108 53 95 D7            539 	anl	_P0_ALT,#0xD7
                            540 ;	../src/main.c:64: rf_init();
   010B 12 05 A6            541 	lcall	_poll_rf_init
                            542 ;	../src/main.c:65: rf_configure(cfg);
   010E 85 30 82            543 	mov	dpl,_cfg
   0111 85 31 83            544 	mov	dph,(_cfg + 1)
   0114 85 32 F0            545 	mov	b,(_cfg + 2)
   0117 12 05 B1            546 	lcall	_poll_rf_configure
                            547 ;	../src/main.c:68: codegenerator_status = IDLE;
   011A 75 36 00            548 	mov	_codegenerator_status,#0x00
                            549 ;	../src/main.c:70: EA = 1;
   011D D2 AF               550 	setb	_EA
                            551 ;	../src/main.c:71: EX4 = 1;
   011F D2 EA               552 	setb	_EX4
                            553 ;	../src/main.c:72: for(i=0;i<6;i++)
   0121 7A 00               554 	mov	r2,#0x00
   0123 7B 00               555 	mov	r3,#0x00
   0125                     556 00106$:
   0125 C3                  557 	clr	c
   0126 EA                  558 	mov	a,r2
   0127 94 06               559 	subb	a,#0x06
   0129 EB                  560 	mov	a,r3
   012A 64 80               561 	xrl	a,#0x80
   012C 94 80               562 	subb	a,#0x80
   012E 50 18               563 	jnc	00109$
                            564 ;	../src/main.c:74: blink_led();
   0130 63 80 20            565 	xrl	_P0,#0x20
                            566 ;	../src/main.c:75: mdelay(500);
   0133 90 01 F4            567 	mov	dptr,#0x01F4
   0136 C0 02               568 	push	ar2
   0138 C0 03               569 	push	ar3
   013A 12 03 3C            570 	lcall	_mdelay
   013D D0 03               571 	pop	ar3
   013F D0 02               572 	pop	ar2
                            573 ;	../src/main.c:72: for(i=0;i<6;i++)
   0141 0A                  574 	inc	r2
   0142 BA 00 E0            575 	cjne	r2,#0x00,00106$
   0145 0B                  576 	inc	r3
   0146 80 DD               577 	sjmp	00106$
   0148                     578 00109$:
                            579 ;	../src/main.c:78: puts("wait for header packet\n");
   0148 90 06 FF            580 	mov	dptr,#__str_0
   014B 75 F0 80            581 	mov	b,#0x80
   014E 12 04 76            582 	lcall	_puts
                            583 ;	../src/main.c:79: while(1) {
   0151                     584 00104$:
                            585 ;	../src/main.c:80: CE = 1; /* Activate RX or TX mode */
   0151 D2 A6               586 	setb	_CE
                            587 ;	../src/main.c:82: if( codegenerator_status == RUNCODE )
   0153 74 04               588 	mov	a,#0x04
   0155 B5 36 F9            589 	cjne	a,_codegenerator_status,00104$
                            590 ;	../src/main.c:85: puts("Start\n\r");
   0158 90 07 17            591 	mov	dptr,#__str_1
   015B 75 F0 80            592 	mov	b,#0x80
   015E 12 04 76            593 	lcall	_puts
                            594 ;	../src/main.c:89: _endasm ;
                            595 	
                            596 	
   0161 12 00 00            597 	    lcall #_Message
                            598 	   
                            599 ;	../src/main.c:90: puts("ret\n\r");
   0164 90 07 1F            600 	mov	dptr,#__str_2
   0167 75 F0 80            601 	mov	b,#0x80
   016A 12 04 76            602 	lcall	_puts
                            603 ;	../src/main.c:91: codegenerator_status = IDLE;
   016D 75 36 00            604 	mov	_codegenerator_status,#0x00
   0170 02 01 51            605 	ljmp	00104$
                            606 ;------------------------------------------------------------
                            607 ;Allocation info for local variables in function 'interrupt_rf'
                            608 ;------------------------------------------------------------
                            609 ;counter                   Allocated with name '_interrupt_rf_counter_1_1'
                            610 ;------------------------------------------------------------
                            611 ;	../src/main.c:97: void interrupt_rf() interrupt 10
                            612 ;	-----------------------------------------
                            613 ;	 function interrupt_rf
                            614 ;	-----------------------------------------
   0173                     615 _interrupt_rf:
   0173 C0 20               616 	push	bits
   0175 C0 E0               617 	push	acc
   0177 C0 F0               618 	push	b
   0179 C0 82               619 	push	dpl
   017B C0 83               620 	push	dph
   017D C0 02               621 	push	(0+2)
   017F C0 03               622 	push	(0+3)
   0181 C0 04               623 	push	(0+4)
   0183 C0 05               624 	push	(0+5)
   0185 C0 06               625 	push	(0+6)
   0187 C0 07               626 	push	(0+7)
   0189 C0 00               627 	push	(0+0)
   018B C0 01               628 	push	(0+1)
   018D C0 D0               629 	push	psw
   018F 75 D0 00            630 	mov	psw,#0x00
                            631 ;	../src/main.c:102: while (DR1) {
   0192                     632 00114$:
   0192 20 A2 03            633 	jb	_DR1,00127$
   0195 02 03 09            634 	ljmp	00116$
   0198                     635 00127$:
                            636 ;	../src/main.c:103: switch( codegenerator_status )
   0198 E4                  637 	clr	a
   0199 B5 36 02            638 	cjne	a,_codegenerator_status,00128$
   019C 80 11               639 	sjmp	00101$
   019E                     640 00128$:
   019E 74 01               641 	mov	a,#0x01
   01A0 B5 36 02            642 	cjne	a,_codegenerator_status,00129$
   01A3 80 22               643 	sjmp	00102$
   01A5                     644 00129$:
   01A5 74 02               645 	mov	a,#0x02
   01A7 B5 36 03            646 	cjne	a,_codegenerator_status,00130$
   01AA 02 02 37            647 	ljmp	00109$
   01AD                     648 00130$:
                            649 ;	../src/main.c:105: case IDLE:
   01AD 80 E3               650 	sjmp	00114$
   01AF                     651 00101$:
                            652 ;	../src/main.c:106: puts("idle\n");
   01AF 90 07 25            653 	mov	dptr,#__str_3
   01B2 75 F0 80            654 	mov	b,#0x80
   01B5 12 04 76            655 	lcall	_puts
                            656 ;	../src/main.c:107: counter=0;
   01B8 75 3B 00            657 	mov	_interrupt_rf_counter_1_1,#0x00
                            658 ;	../src/main.c:108: codegenerator_status = HEADERPACKET;
   01BB 75 36 01            659 	mov	_codegenerator_status,#0x01
                            660 ;	../src/main.c:109: puts("header\n");
   01BE 90 07 2B            661 	mov	dptr,#__str_4
   01C1 75 F0 80            662 	mov	b,#0x80
   01C4 12 04 76            663 	lcall	_puts
                            664 ;	../src/main.c:110: case HEADERPACKET:
   01C7                     665 00102$:
                            666 ;	../src/main.c:111: if( counter < 4 ){ /* header buffer length 4 bytes */
   01C7 C3                  667 	clr	c
   01C8 E5 3B               668 	mov	a,_interrupt_rf_counter_1_1
   01CA 64 80               669 	xrl	a,#0x80
   01CC 94 84               670 	subb	a,#0x84
   01CE 50 41               671 	jnc	00107$
                            672 ;	../src/main.c:112: HeaderFile[counter++] = spi_write_then_read(0);
   01D0 AA 3B               673 	mov	r2,_interrupt_rf_counter_1_1
   01D2 05 3B               674 	inc	_interrupt_rf_counter_1_1
   01D4 EA                  675 	mov	a,r2
   01D5 24 37               676 	add	a,#_HeaderFile
   01D7 F8                  677 	mov	r0,a
   01D8 75 82 00            678 	mov	dpl,#0x00
   01DB C0 00               679 	push	ar0
   01DD 12 06 D2            680 	lcall	_spi_write_then_read
   01E0 E5 82               681 	mov	a,dpl
   01E2 D0 00               682 	pop	ar0
   01E4 F6                  683 	mov	@r0,a
                            684 ;	../src/main.c:113: putc( ( (HeaderFile[counter-1]>>4) & 0xff ) + 48 );
   01E5 E5 3B               685 	mov	a,_interrupt_rf_counter_1_1
   01E7 14                  686 	dec	a
   01E8 24 37               687 	add	a,#_HeaderFile
   01EA F8                  688 	mov	r0,a
   01EB E6                  689 	mov	a,@r0
   01EC C4                  690 	swap	a
   01ED 54 0F               691 	anl	a,#0x0f
   01EF 24 30               692 	add	a,#0x30
   01F1 F5 82               693 	mov	dpl,a
   01F3 12 04 73            694 	lcall	_putc
                            695 ;	../src/main.c:114: putc( ( HeaderFile[counter-1] & 0x0f ) + 48 );
   01F6 E5 3B               696 	mov	a,_interrupt_rf_counter_1_1
   01F8 14                  697 	dec	a
   01F9 24 37               698 	add	a,#_HeaderFile
   01FB F8                  699 	mov	r0,a
   01FC 86 02               700 	mov	ar2,@r0
   01FE 74 0F               701 	mov	a,#0x0F
   0200 5A                  702 	anl	a,r2
   0201 24 30               703 	add	a,#0x30
   0203 F5 82               704 	mov	dpl,a
   0205 12 04 73            705 	lcall	_putc
                            706 ;	../src/main.c:115: putc(' ' );
   0208 75 82 20            707 	mov	dpl,#0x20
   020B 12 04 73            708 	lcall	_putc
   020E 02 01 92            709 	ljmp	00114$
   0211                     710 00107$:
                            711 ;	../src/main.c:118: if( counter < RF_LENGTH ){
   0211 C3                  712 	clr	c
   0212 E5 3B               713 	mov	a,_interrupt_rf_counter_1_1
   0214 64 80               714 	xrl	a,#0x80
   0216 94 9C               715 	subb	a,#0x9c
   0218 50 0B               716 	jnc	00104$
                            717 ;	../src/main.c:119: spi_write_then_read(0);
   021A 75 82 00            718 	mov	dpl,#0x00
   021D 12 06 D2            719 	lcall	_spi_write_then_read
                            720 ;	../src/main.c:120: counter++;
   0220 05 3B               721 	inc	_interrupt_rf_counter_1_1
   0222 02 01 92            722 	ljmp	00114$
   0225                     723 00104$:
                            724 ;	../src/main.c:123: counter = 0;
   0225 75 3B 00            725 	mov	_interrupt_rf_counter_1_1,#0x00
                            726 ;	../src/main.c:124: codegenerator_status = CODEPACKET;
   0228 75 36 02            727 	mov	_codegenerator_status,#0x02
                            728 ;	../src/main.c:125: puts("\n\rcode\n");
   022B 90 07 33            729 	mov	dptr,#__str_5
   022E 75 F0 80            730 	mov	b,#0x80
   0231 12 04 76            731 	lcall	_puts
                            732 ;	../src/main.c:127: break;
   0234 02 01 92            733 	ljmp	00114$
                            734 ;	../src/main.c:128: case CODEPACKET:
   0237                     735 00109$:
                            736 ;	../src/main.c:129: if( counter < (RF_LENGTH-1) ){ /* code buffer length 41 bytes */
   0237 C3                  737 	clr	c
   0238 E5 3B               738 	mov	a,_interrupt_rf_counter_1_1
   023A 64 80               739 	xrl	a,#0x80
   023C 94 9B               740 	subb	a,#0x9b
   023E 50 5A               741 	jnc	00111$
                            742 ;	../src/main.c:130: Message[counter++] = spi_write_then_read(0);
   0240 AA 3B               743 	mov	r2,_interrupt_rf_counter_1_1
   0242 05 3B               744 	inc	_interrupt_rf_counter_1_1
   0244 EA                  745 	mov	a,r2
   0245 24 00               746 	add	a,#_Message
   0247 FA                  747 	mov	r2,a
   0248 E4                  748 	clr	a
   0249 34 00               749 	addc	a,#(_Message >> 8)
   024B FB                  750 	mov	r3,a
   024C 75 82 00            751 	mov	dpl,#0x00
   024F C0 02               752 	push	ar2
   0251 C0 03               753 	push	ar3
   0253 12 06 D2            754 	lcall	_spi_write_then_read
   0256 AC 82               755 	mov	r4,dpl
   0258 D0 03               756 	pop	ar3
   025A D0 02               757 	pop	ar2
   025C 8A 82               758 	mov	dpl,r2
   025E 8B 83               759 	mov	dph,r3
   0260 EC                  760 	mov	a,r4
   0261 F0                  761 	movx	@dptr,a
                            762 ;	../src/main.c:131: putc( ( (Message[counter-1]>>4) & 0xff ) + 48 );
   0262 E5 3B               763 	mov	a,_interrupt_rf_counter_1_1
   0264 14                  764 	dec	a
   0265 24 00               765 	add	a,#_Message
   0267 F5 82               766 	mov	dpl,a
   0269 E4                  767 	clr	a
   026A 34 00               768 	addc	a,#(_Message >> 8)
   026C F5 83               769 	mov	dph,a
   026E E0                  770 	movx	a,@dptr
   026F C4                  771 	swap	a
   0270 54 0F               772 	anl	a,#0x0f
   0272 24 30               773 	add	a,#0x30
   0274 F5 82               774 	mov	dpl,a
   0276 12 04 73            775 	lcall	_putc
                            776 ;	../src/main.c:132: putc( ( Message[counter-1] & 0x0f ) + 48 );
   0279 E5 3B               777 	mov	a,_interrupt_rf_counter_1_1
   027B 14                  778 	dec	a
   027C 24 00               779 	add	a,#_Message
   027E F5 82               780 	mov	dpl,a
   0280 E4                  781 	clr	a
   0281 34 00               782 	addc	a,#(_Message >> 8)
   0283 F5 83               783 	mov	dph,a
   0285 E0                  784 	movx	a,@dptr
   0286 FA                  785 	mov	r2,a
   0287 74 0F               786 	mov	a,#0x0F
   0289 5A                  787 	anl	a,r2
   028A 24 30               788 	add	a,#0x30
   028C F5 82               789 	mov	dpl,a
   028E 12 04 73            790 	lcall	_putc
                            791 ;	../src/main.c:133: putc(' ' );
   0291 75 82 20            792 	mov	dpl,#0x20
   0294 12 04 73            793 	lcall	_putc
   0297 02 01 92            794 	ljmp	00114$
   029A                     795 00111$:
                            796 ;	../src/main.c:136: spi_write_then_read(0);
   029A 75 82 00            797 	mov	dpl,#0x00
   029D 12 06 D2            798 	lcall	_spi_write_then_read
                            799 ;	../src/main.c:137: Message[counter++] = spi_write_then_read(0);
   02A0 AA 3B               800 	mov	r2,_interrupt_rf_counter_1_1
   02A2 05 3B               801 	inc	_interrupt_rf_counter_1_1
   02A4 EA                  802 	mov	a,r2
   02A5 24 00               803 	add	a,#_Message
   02A7 FA                  804 	mov	r2,a
   02A8 E4                  805 	clr	a
   02A9 34 00               806 	addc	a,#(_Message >> 8)
   02AB FB                  807 	mov	r3,a
   02AC 75 82 00            808 	mov	dpl,#0x00
   02AF C0 02               809 	push	ar2
   02B1 C0 03               810 	push	ar3
   02B3 12 06 D2            811 	lcall	_spi_write_then_read
   02B6 AC 82               812 	mov	r4,dpl
   02B8 D0 03               813 	pop	ar3
   02BA D0 02               814 	pop	ar2
   02BC 8A 82               815 	mov	dpl,r2
   02BE 8B 83               816 	mov	dph,r3
   02C0 EC                  817 	mov	a,r4
   02C1 F0                  818 	movx	@dptr,a
                            819 ;	../src/main.c:138: putc( ( (Message[counter-1]>>4) & 0xff ) + 48 );
   02C2 E5 3B               820 	mov	a,_interrupt_rf_counter_1_1
   02C4 14                  821 	dec	a
   02C5 24 00               822 	add	a,#_Message
   02C7 F5 82               823 	mov	dpl,a
   02C9 E4                  824 	clr	a
   02CA 34 00               825 	addc	a,#(_Message >> 8)
   02CC F5 83               826 	mov	dph,a
   02CE E0                  827 	movx	a,@dptr
   02CF C4                  828 	swap	a
   02D0 54 0F               829 	anl	a,#0x0f
   02D2 24 30               830 	add	a,#0x30
   02D4 F5 82               831 	mov	dpl,a
   02D6 12 04 73            832 	lcall	_putc
                            833 ;	../src/main.c:139: putc( ( Message[counter-1] & 0x0f ) + 48 );
   02D9 E5 3B               834 	mov	a,_interrupt_rf_counter_1_1
   02DB 14                  835 	dec	a
   02DC 24 00               836 	add	a,#_Message
   02DE F5 82               837 	mov	dpl,a
   02E0 E4                  838 	clr	a
   02E1 34 00               839 	addc	a,#(_Message >> 8)
   02E3 F5 83               840 	mov	dph,a
   02E5 E0                  841 	movx	a,@dptr
   02E6 FA                  842 	mov	r2,a
   02E7 74 0F               843 	mov	a,#0x0F
   02E9 5A                  844 	anl	a,r2
   02EA 24 30               845 	add	a,#0x30
   02EC F5 82               846 	mov	dpl,a
   02EE 12 04 73            847 	lcall	_putc
                            848 ;	../src/main.c:140: putc( ' ' );
   02F1 75 82 20            849 	mov	dpl,#0x20
   02F4 12 04 73            850 	lcall	_putc
                            851 ;	../src/main.c:141: counter = 0;
   02F7 75 3B 00            852 	mov	_interrupt_rf_counter_1_1,#0x00
                            853 ;	../src/main.c:142: codegenerator_status = RUNCODE;
   02FA 75 36 04            854 	mov	_codegenerator_status,#0x04
                            855 ;	../src/main.c:143: puts("\n\rRun\n");
   02FD 90 07 3B            856 	mov	dptr,#__str_6
   0300 75 F0 80            857 	mov	b,#0x80
   0303 12 04 76            858 	lcall	_puts
                            859 ;	../src/main.c:146: } /* end switch case */
   0306 02 01 92            860 	ljmp	00114$
   0309                     861 00116$:
                            862 ;	../src/main.c:151: CE = 0;
   0309 C2 A6               863 	clr	_CE
                            864 ;	../src/main.c:152: EXIF &= ~0x40;
   030B 53 91 BF            865 	anl	_EXIF,#0xBF
   030E D0 D0               866 	pop	psw
   0310 D0 01               867 	pop	(0+1)
   0312 D0 00               868 	pop	(0+0)
   0314 D0 07               869 	pop	(0+7)
   0316 D0 06               870 	pop	(0+6)
   0318 D0 05               871 	pop	(0+5)
   031A D0 04               872 	pop	(0+4)
   031C D0 03               873 	pop	(0+3)
   031E D0 02               874 	pop	(0+2)
   0320 D0 83               875 	pop	dph
   0322 D0 82               876 	pop	dpl
   0324 D0 F0               877 	pop	b
   0326 D0 E0               878 	pop	acc
   0328 D0 20               879 	pop	bits
   032A 32                  880 	reti
                            881 	.area CSEG    (CODE)
                            882 	.area CONST   (CODE)
   06FF                     883 __str_0:
   06FF 77 61 69 74 20 66   884 	.ascii "wait for header packet"
        6F 72 20 68 65 61
        64 65 72 20 70 61
        63 6B 65 74
   0715 0A                  885 	.db 0x0A
   0716 00                  886 	.db 0x00
   0717                     887 __str_1:
   0717 53 74 61 72 74      888 	.ascii "Start"
   071C 0A                  889 	.db 0x0A
   071D 0D                  890 	.db 0x0D
   071E 00                  891 	.db 0x00
   071F                     892 __str_2:
   071F 72 65 74            893 	.ascii "ret"
   0722 0A                  894 	.db 0x0A
   0723 0D                  895 	.db 0x0D
   0724 00                  896 	.db 0x00
   0725                     897 __str_3:
   0725 69 64 6C 65         898 	.ascii "idle"
   0729 0A                  899 	.db 0x0A
   072A 00                  900 	.db 0x00
   072B                     901 __str_4:
   072B 68 65 61 64 65 72   902 	.ascii "header"
   0731 0A                  903 	.db 0x0A
   0732 00                  904 	.db 0x00
   0733                     905 __str_5:
   0733 0A                  906 	.db 0x0A
   0734 0D                  907 	.db 0x0D
   0735 63 6F 64 65         908 	.ascii "code"
   0739 0A                  909 	.db 0x0A
   073A 00                  910 	.db 0x00
   073B                     911 __str_6:
   073B 0A                  912 	.db 0x0A
   073C 0D                  913 	.db 0x0D
   073D 52 75 6E            914 	.ascii "Run"
   0740 0A                  915 	.db 0x0A
   0741 00                  916 	.db 0x00
                            917 	.area XINIT   (CODE)
                            918 	.area CABS    (ABS,CODE)
