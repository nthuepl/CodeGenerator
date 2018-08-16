/*
 * testacc.c
 *
 * This is the main test program for the accelerometer code, which was
 * compiled by and linked by IAR into the base firmware image,
 * and we are calling the API from SDCC (which this file should be
 * compiled with), and linked with the binding code (s2i_
 *
 * This test code should be placed at location 0x(6)A000,
 * and it should write to the RAM buffer before returning.
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
	accReadReg(ACC_LIS331DL_WHO_AM_I	, buf + 0);
	accReadReg(ACC_LIS331DL_CTRL_REG1 , buf + 1);
	accReadAcc(fer, fer+1, fer+2);
	
	sdcc_main_return; /* return macro, which is same as assembly below */
	
	// accWriteReg(ACC_LIS331DL_CTRL_REG1, 
	//		0x00 /* data rate 100 Hz */
	//		| 0x40 /* active mode */
	//		| 0x00 /* +/- 2g */
	//		| 0x00 /* normal mode, P not self test */
	//		| 0x00 /* normal mode, M not enabled */
	// ACC_LIS331DL_STATUS_REG
	// ACC_LIS331DL_CTRL_REG1
}