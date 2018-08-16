                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 2.9.0 #5416 (Mar 22 2009) (MINGW32)
                              4 ; This file was generated Thu Jan 23 23:21:39 2014
                              5 ;--------------------------------------------------------
                              6 	.module CodeGenerator
                              7 	.optsdcc -mmcs51 --model-small
                              8 	
                              9 ;--------------------------------------------------------
                             10 ; Public variables in this module
                             11 ;--------------------------------------------------------
                             12 	.globl _stage
                             13 	.globl _stage_runcode
                             14 	.globl _stage_codepacket
                             15 	.globl _stage_headerpacket
                             16 	.globl _stage_idle
                             17 	.globl _CodeGeneratorInit
                             18 ;--------------------------------------------------------
                             19 ; special function registers
                             20 ;--------------------------------------------------------
                             21 	.area RSEG    (DATA)
                             22 ;--------------------------------------------------------
                             23 ; special function bits
                             24 ;--------------------------------------------------------
                             25 	.area RSEG    (DATA)
                             26 ;--------------------------------------------------------
                             27 ; overlayable register banks
                             28 ;--------------------------------------------------------
                             29 	.area REG_BANK_0	(REL,OVR,DATA)
   0000                      30 	.ds 8
                             31 ;--------------------------------------------------------
                             32 ; internal ram data
                             33 ;--------------------------------------------------------
                             34 	.area DSEG    (DATA)
   0008                      35 _stage_idle::
   0008                      36 	.ds 1
   0009                      37 _stage_headerpacket::
   0009                      38 	.ds 1
   000A                      39 _stage_codepacket::
   000A                      40 	.ds 1
   000B                      41 _stage_runcode::
   000B                      42 	.ds 1
   000C                      43 _stage::
   000C                      44 	.ds 1
                             45 ;--------------------------------------------------------
                             46 ; overlayable items in internal ram 
                             47 ;--------------------------------------------------------
                             48 	.area OSEG    (OVR,DATA)
                             49 ;--------------------------------------------------------
                             50 ; indirectly addressable internal ram data
                             51 ;--------------------------------------------------------
                             52 	.area ISEG    (DATA)
                             53 ;--------------------------------------------------------
                             54 ; absolute internal ram data
                             55 ;--------------------------------------------------------
                             56 	.area IABS    (ABS,DATA)
                             57 	.area IABS    (ABS,DATA)
                             58 ;--------------------------------------------------------
                             59 ; bit data
                             60 ;--------------------------------------------------------
                             61 	.area BSEG    (BIT)
                             62 ;--------------------------------------------------------
                             63 ; paged external ram data
                             64 ;--------------------------------------------------------
                             65 	.area PSEG    (PAG,XDATA)
                             66 ;--------------------------------------------------------
                             67 ; external ram data
                             68 ;--------------------------------------------------------
                             69 	.area XSEG    (XDATA)
                             70 ;--------------------------------------------------------
                             71 ; absolute external ram data
                             72 ;--------------------------------------------------------
                             73 	.area XABS    (ABS,XDATA)
                             74 ;--------------------------------------------------------
                             75 ; external initialized ram data
                             76 ;--------------------------------------------------------
                             77 	.area XISEG   (XDATA)
                             78 	.area HOME    (CODE)
                             79 	.area GSINIT0 (CODE)
                             80 	.area GSINIT1 (CODE)
                             81 	.area GSINIT2 (CODE)
                             82 	.area GSINIT3 (CODE)
                             83 	.area GSINIT4 (CODE)
                             84 	.area GSINIT5 (CODE)
                             85 	.area GSINIT  (CODE)
                             86 	.area GSFINAL (CODE)
                             87 	.area CSEG    (CODE)
                             88 ;--------------------------------------------------------
                             89 ; global & static initialisations
                             90 ;--------------------------------------------------------
                             91 	.area HOME    (CODE)
                             92 	.area GSINIT  (CODE)
                             93 	.area GSFINAL (CODE)
                             94 	.area GSINIT  (CODE)
                             95 ;	../src/CodeGenerator.c:10: unsigned char stage_idle         = 0x00;
   00B4 75 08 00             96 	mov	_stage_idle,#0x00
                             97 ;	../src/CodeGenerator.c:11: unsigned char stage_headerpacket = 0x01;
   00B7 75 09 01             98 	mov	_stage_headerpacket,#0x01
                             99 ;	../src/CodeGenerator.c:12: unsigned char stage_codepacket   = 0x02;
   00BA 75 0A 02            100 	mov	_stage_codepacket,#0x02
                            101 ;	../src/CodeGenerator.c:13: unsigned char stage_runcode      = 0x04;
   00BD 75 0B 04            102 	mov	_stage_runcode,#0x04
                            103 ;--------------------------------------------------------
                            104 ; Home
                            105 ;--------------------------------------------------------
                            106 	.area HOME    (CODE)
                            107 	.area HOME    (CODE)
                            108 ;--------------------------------------------------------
                            109 ; code
                            110 ;--------------------------------------------------------
                            111 	.area CSEG    (CODE)
                            112 ;------------------------------------------------------------
                            113 ;Allocation info for local variables in function 'CodeGeneratorInit'
                            114 ;------------------------------------------------------------
                            115 ;------------------------------------------------------------
                            116 ;	../src/CodeGenerator.c:18: void CodeGeneratorInit( void )
                            117 ;	-----------------------------------------
                            118 ;	 function CodeGeneratorInit
                            119 ;	-----------------------------------------
   0102                     120 _CodeGeneratorInit:
                    0002    121 	ar2 = 0x02
                    0003    122 	ar3 = 0x03
                    0004    123 	ar4 = 0x04
                    0005    124 	ar5 = 0x05
                    0006    125 	ar6 = 0x06
                    0007    126 	ar7 = 0x07
                    0000    127 	ar0 = 0x00
                    0001    128 	ar1 = 0x01
                            129 ;	../src/CodeGenerator.c:20: stage = stage_idle;
   0102 85 08 0C            130 	mov	_stage,_stage_idle
   0105 22                  131 	ret
                            132 	.area CSEG    (CODE)
                            133 	.area CONST   (CODE)
                            134 	.area XINIT   (CODE)
                            135 	.area CABS    (ABS,CODE)
