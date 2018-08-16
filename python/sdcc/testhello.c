/*
 * testhello.c
 *
 * make testhello.bin
 * python runflash.py testhello.bin ''
 *
 * You should be able to see it connect and print out the string hello.
 *
 * This is the basic test for the return buffer. 
 * It calls the accelerometer function to initialize it and then`
 * It puts a "hello" * string into the return buffer and that's it.
 * It assumes firmware image has been compiled by and linked by IAR,
 * and we are calling the API from SDCC (which this file should be
 * compiled with), and linked with the binding code (s2i_
 *
 * This test code should be placed at location 0x(6)A000,
 * and it should write to the RAM buffer before returning.
 * It is meant to be compiled using Makefile (make testhello.bin)
 * and use runflash.py to load the binary image and print it.
 */
#include "sdcc2iar.h" // not needed except for MAIN program for return
#include "epl_acc_lis331dl.h"

#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro for either CC2540 or CC2541"
#endif

__xdata __at (MAP_notify+3) uint8 buf[4];
__xdata __at (MAP_notify+3+4) uint16 fer[4];

void Main() {
	accInit();
	buf[0] = 'h';
	buf[1] = 'e';
	buf[2] = 'l';
	buf[3] = 'l';
	buf[4] = 'o';
	buf[5] = 0;
	
	sdcc_main_return; /* return macro, which is same as assembly below */
	//__asm
	//LJMP 0x0122 ; ?BRET_FF
	//__endasm;
	
	// accReadReg(ACC_LIS331DL_CTRL_REG1 , buf);
	// accWriteReg(ACC_LIS331DL_CTRL_REG1, 
	//		0x00 /* data rate 100 Hz */
	//		| 0x40 /* active mode */
	//		| 0x00 /* +/- 2g */
	//		| 0x00 /* normal mode, P not self test */
	//		| 0x00 /* normal mode, M not enabled */
	//		| 0x07 /* enable x, y, z */
	//		);
	// ACC_LIS331DL_STATUS_REG
	// ACC_LIS331DL_CTRL_REG1
}