                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 2.9.0 #5416 (Mar 22 2009) (MINGW32)
                              4 ; This file was generated Sat Feb 15 21:01:14 2014
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
                            171 	.globl _Meassage
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
   003B                     377 _Meassage::
   003B                     378 	.ds 41
                            379 ;--------------------------------------------------------
                            380 ; overlayable items in internal ram 
                            381 ;--------------------------------------------------------
                            382 	.area OSEG    (OVR,DATA)
                            383 ;--------------------------------------------------------
                            384 ; Stack segment in internal ram 
                            385 ;--------------------------------------------------------
                            386 	.area	SSEG	(DATA)
   0080                     387 __start__stack:
   0080                     388 	.ds	1
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
                            411 ;--------------------------------------------------------
                            412 ; absolute external ram data
                            413 ;--------------------------------------------------------
                            414 	.area XABS    (ABS,XDATA)
                            415 ;--------------------------------------------------------
                            416 ; external initialized ram data
                            417 ;--------------------------------------------------------
                            418 	.area XISEG   (XDATA)
                            419 	.area HOME    (CODE)
                            420 	.area GSINIT0 (CODE)
                            421 	.area GSINIT1 (CODE)
                            422 	.area GSINIT2 (CODE)
                            423 	.area GSINIT3 (CODE)
                            424 	.area GSINIT4 (CODE)
                            425 	.area GSINIT5 (CODE)
                            426 	.area GSINIT  (CODE)
                            427 	.area GSFINAL (CODE)
                            428 	.area CSEG    (CODE)
                            429 ;--------------------------------------------------------
                            430 ; interrupt vector 
                            431 ;--------------------------------------------------------
                            432 	.area HOME    (CODE)
   0000                     433 __interrupt_vect:
   0000 02 00 5B            434 	ljmp	__sdcc_gsinit_startup
   0003 32                  435 	reti
   0004                     436 	.ds	7
   000B 32                  437 	reti
   000C                     438 	.ds	7
   0013 32                  439 	reti
   0014                     440 	.ds	7
   001B 32                  441 	reti
   001C                     442 	.ds	7
   0023 32                  443 	reti
   0024                     444 	.ds	7
   002B 32                  445 	reti
   002C                     446 	.ds	7
   0033 32                  447 	reti
   0034                     448 	.ds	7
   003B 32                  449 	reti
   003C                     450 	.ds	7
   0043 32                  451 	reti
   0044                     452 	.ds	7
   004B 32                  453 	reti
   004C                     454 	.ds	7
   0053 02 01 55            455 	ljmp	_interrupt_rf
                            456 ;--------------------------------------------------------
                            457 ; global & static initialisations
                            458 ;--------------------------------------------------------
                            459 	.area HOME    (CODE)
                            460 	.area GSINIT  (CODE)
                            461 	.area GSFINAL (CODE)
                            462 	.area GSINIT  (CODE)
                            463 	.globl __sdcc_gsinit_startup
                            464 	.globl __sdcc_program_startup
                            465 	.globl __start__stack
                            466 	.globl __mcs51_genXINIT
                            467 	.globl __mcs51_genXRAMCLEAR
                            468 	.globl __mcs51_genRAMCLEAR
                            469 ;	../src/main.c:27: struct rf_config rf_data = {
   00B4 75 21 00            470 	mov	_rf_data,#0x00
   00B7 75 22 08            471 	mov	(_rf_data + 0x0001),#0x08
   00BA 75 23 00            472 	mov	(_rf_data + 0x0002),#0x00
   00BD 75 24 00            473 	mov	(_rf_data + 0x0003),#0x00
   00C0 75 25 00            474 	mov	(_rf_data + 0x0004),#0x00
   00C3 75 26 00            475 	mov	(_rf_data + 0x0005),#0x00
   00C6 75 27 00            476 	mov	(_rf_data + 0x0006),#0x00
   00C9 75 28 00            477 	mov	(_rf_data + 0x0007),#0x00
   00CC 75 29 00            478 	mov	(_rf_data + 0x0008),#0x00
   00CF 75 2A 0F            479 	mov	(_rf_data + 0x0009),#0x0F
   00D2 75 2B 01            480 	mov	(_rf_data + 0x000a),#0x01
   00D5 75 2C 01            481 	mov	(_rf_data + 0x000b),#0x01
   00D8 75 2D 61            482 	mov	(_rf_data + 0x000c),#0x61
   00DB 75 2E 6F            483 	mov	(_rf_data + 0x000d),#0x6F
   00DE 75 2F 15            484 	mov	(_rf_data + 0x000e),#0x15
                            485 ;	../src/main.c:34: struct rf_config *cfg = &rf_data;
   00E1 75 30 21            486 	mov	_cfg,#_rf_data
   00E4 75 31 00            487 	mov	(_cfg + 1),#0x00
   00E7 75 32 40            488 	mov	(_cfg + 2),#0x40
                            489 ;	../src/main.c:35: char dst_addr[3] = { 0x02, 0x02, 0x02 };
   00EA 75 33 02            490 	mov	_dst_addr,#0x02
   00ED 75 34 02            491 	mov	(_dst_addr + 0x0001),#0x02
   00F0 75 35 02            492 	mov	(_dst_addr + 0x0002),#0x02
                            493 	.area GSFINAL (CODE)
   00F3 02 00 56            494 	ljmp	__sdcc_program_startup
                            495 ;--------------------------------------------------------
                            496 ; Home
                            497 ;--------------------------------------------------------
                            498 	.area HOME    (CODE)
                            499 	.area HOME    (CODE)
   0056                     500 __sdcc_program_startup:
   0056 12 00 F6            501 	lcall	_main
                            502 ;	return from main will lock up
   0059 80 FE               503 	sjmp .
                            504 ;--------------------------------------------------------
                            505 ; code
                            506 ;--------------------------------------------------------
                            507 	.area CSEG    (CODE)
                            508 ;------------------------------------------------------------
                            509 ;Allocation info for local variables in function 'main'
                            510 ;------------------------------------------------------------
                            511 ;i                         Allocated to registers r2 r3 
                            512 ;------------------------------------------------------------
                            513 ;	../src/main.c:41: void main()
                            514 ;	-----------------------------------------
                            515 ;	 function main
                            516 ;	-----------------------------------------
   00F6                     517 _main:
                    0002    518 	ar2 = 0x02
                    0003    519 	ar3 = 0x03
                    0004    520 	ar4 = 0x04
                    0005    521 	ar5 = 0x05
                    0006    522 	ar6 = 0x06
                    0007    523 	ar7 = 0x07
                    0000    524 	ar0 = 0x00
                    0001    525 	ar1 = 0x01
                            526 ;	../src/main.c:44: store_cpu_rate(16);
   00F6 90 00 10            527 	mov	dptr,#(0x10&0x00ff)
   00F9 E4                  528 	clr	a
   00FA F5 F0               529 	mov	b,a
   00FC 12 02 AD            530 	lcall	_store_cpu_rate
                            531 ;	../src/main.c:46: serial_init(19200);
   00FF 90 4B 00            532 	mov	dptr,#0x4B00
   0102 12 03 D9            533 	lcall	_serial_init
                            534 ;	../src/main.c:48: P0_DIR &= ~0x28;
   0105 53 94 D7            535 	anl	_P0_DIR,#0xD7
                            536 ;	../src/main.c:49: P0_ALT &= ~0x28;
   0108 53 95 D7            537 	anl	_P0_ALT,#0xD7
                            538 ;	../src/main.c:51: rf_init();
   010B 12 01 CD            539 	lcall	_poll_rf_init
                            540 ;	../src/main.c:52: rf_configure(cfg);
   010E 85 30 82            541 	mov	dpl,_cfg
   0111 85 31 83            542 	mov	dph,(_cfg + 1)
   0114 85 32 F0            543 	mov	b,(_cfg + 2)
   0117 12 01 D8            544 	lcall	_poll_rf_configure
                            545 ;	../src/main.c:55: codegenerator_status = IDLE;
   011A 75 36 00            546 	mov	_codegenerator_status,#0x00
                            547 ;	../src/main.c:57: EA = 1;
   011D D2 AF               548 	setb	_EA
                            549 ;	../src/main.c:58: EX4 = 1;
   011F D2 EA               550 	setb	_EX4
                            551 ;	../src/main.c:59: for(i=0;i<6;i++)
   0121 7A 00               552 	mov	r2,#0x00
   0123 7B 00               553 	mov	r3,#0x00
   0125                     554 00104$:
   0125 C3                  555 	clr	c
   0126 EA                  556 	mov	a,r2
   0127 94 06               557 	subb	a,#0x06
   0129 EB                  558 	mov	a,r3
   012A 64 80               559 	xrl	a,#0x80
   012C 94 80               560 	subb	a,#0x80
   012E 50 18               561 	jnc	00107$
                            562 ;	../src/main.c:61: blink_led();
   0130 63 80 20            563 	xrl	_P0,#0x20
                            564 ;	../src/main.c:62: mdelay(500);
   0133 90 01 F4            565 	mov	dptr,#0x01F4
   0136 C0 02               566 	push	ar2
   0138 C0 03               567 	push	ar3
   013A 12 02 BE            568 	lcall	_mdelay
   013D D0 03               569 	pop	ar3
   013F D0 02               570 	pop	ar2
                            571 ;	../src/main.c:59: for(i=0;i<6;i++)
   0141 0A                  572 	inc	r2
   0142 BA 00 E0            573 	cjne	r2,#0x00,00104$
   0145 0B                  574 	inc	r3
   0146 80 DD               575 	sjmp	00104$
   0148                     576 00107$:
                            577 ;	../src/main.c:65: puts("Slave startup.\n\r");
   0148 90 05 A1            578 	mov	dptr,#__str_0
   014B 75 F0 80            579 	mov	b,#0x80
   014E 12 03 F8            580 	lcall	_puts
                            581 ;	../src/main.c:66: while(1) {
   0151                     582 00102$:
                            583 ;	../src/main.c:67: CE = 1;
   0151 D2 A6               584 	setb	_CE
   0153 80 FC               585 	sjmp	00102$
                            586 ;------------------------------------------------------------
                            587 ;Allocation info for local variables in function 'interrupt_rf'
                            588 ;------------------------------------------------------------
                            589 ;counter                   Allocated to registers r2 
                            590 ;led_status                Allocated to registers 
                            591 ;------------------------------------------------------------
                            592 ;	../src/main.c:83: void interrupt_rf() interrupt 10
                            593 ;	-----------------------------------------
                            594 ;	 function interrupt_rf
                            595 ;	-----------------------------------------
   0155                     596 _interrupt_rf:
   0155 C0 20               597 	push	bits
   0157 C0 E0               598 	push	acc
   0159 C0 F0               599 	push	b
   015B C0 82               600 	push	dpl
   015D C0 83               601 	push	dph
   015F C0 02               602 	push	(0+2)
   0161 C0 03               603 	push	(0+3)
   0163 C0 04               604 	push	(0+4)
   0165 C0 05               605 	push	(0+5)
   0167 C0 06               606 	push	(0+6)
   0169 C0 07               607 	push	(0+7)
   016B C0 00               608 	push	(0+0)
   016D C0 01               609 	push	(0+1)
   016F C0 D0               610 	push	psw
   0171 75 D0 00            611 	mov	psw,#0x00
                            612 ;	../src/main.c:87: blink_led();
   0174 63 80 20            613 	xrl	_P0,#0x20
                            614 ;	../src/main.c:88: mdelay(500);
   0177 90 01 F4            615 	mov	dptr,#0x01F4
   017A 12 02 BE            616 	lcall	_mdelay
                            617 ;	../src/main.c:91: while (DR1) {
   017D 7A 00               618 	mov	r2,#0x00
   017F                     619 00101$:
   017F 30 A2 1A            620 	jnb	_DR1,00103$
                            621 ;	../src/main.c:92: rf_buf[counter++] = spi_write_then_read(0);	/* clock in data */
   0182 8A 03               622 	mov	ar3,r2
   0184 0A                  623 	inc	r2
   0185 EB                  624 	mov	a,r3
   0186 24 64               625 	add	a,#_rf_buf
   0188 F8                  626 	mov	r0,a
   0189 75 82 00            627 	mov	dpl,#0x00
   018C C0 02               628 	push	ar2
   018E C0 00               629 	push	ar0
   0190 12 05 2F            630 	lcall	_spi_write_then_read
   0193 E5 82               631 	mov	a,dpl
   0195 D0 00               632 	pop	ar0
   0197 D0 02               633 	pop	ar2
   0199 F6                  634 	mov	@r0,a
   019A 80 E3               635 	sjmp	00101$
   019C                     636 00103$:
                            637 ;	../src/main.c:95: led_status = rf_buf[0];
   019C 85 64 82            638 	mov	dpl,_rf_buf
                            639 ;	../src/main.c:96: putc(led_status);
   019F 12 03 F5            640 	lcall	_putc
                            641 ;	../src/main.c:97: puts("\n\r");
   01A2 90 05 B2            642 	mov	dptr,#__str_1
   01A5 75 F0 80            643 	mov	b,#0x80
   01A8 12 03 F8            644 	lcall	_puts
                            645 ;	../src/main.c:100: CE = 0;
   01AB C2 A6               646 	clr	_CE
                            647 ;	../src/main.c:101: EXIF &= ~0x40;
   01AD 53 91 BF            648 	anl	_EXIF,#0xBF
   01B0 D0 D0               649 	pop	psw
   01B2 D0 01               650 	pop	(0+1)
   01B4 D0 00               651 	pop	(0+0)
   01B6 D0 07               652 	pop	(0+7)
   01B8 D0 06               653 	pop	(0+6)
   01BA D0 05               654 	pop	(0+5)
   01BC D0 04               655 	pop	(0+4)
   01BE D0 03               656 	pop	(0+3)
   01C0 D0 02               657 	pop	(0+2)
   01C2 D0 83               658 	pop	dph
   01C4 D0 82               659 	pop	dpl
   01C6 D0 F0               660 	pop	b
   01C8 D0 E0               661 	pop	acc
   01CA D0 20               662 	pop	bits
   01CC 32                  663 	reti
                            664 	.area CSEG    (CODE)
                            665 	.area CONST   (CODE)
   05A1                     666 __str_0:
   05A1 53 6C 61 76 65 20   667 	.ascii "Slave startup."
        73 74 61 72 74 75
        70 2E
   05AF 0A                  668 	.db 0x0A
   05B0 0D                  669 	.db 0x0D
   05B1 00                  670 	.db 0x00
   05B2                     671 __str_1:
   05B2 0A                  672 	.db 0x0A
   05B3 0D                  673 	.db 0x0D
   05B4 00                  674 	.db 0x00
                            675 	.area XINIT   (CODE)
                            676 	.area CABS    (ABS,CODE)
