/*
 * testrtc.c
 *
 * This is the main test program for the RTC code.  It is to be compiled
 * by SDCC, and it calls the API function for RTC that has been
 * compiled by and linked by IAR into the base firmware image.
 * SDCC links the binding file (s2i_epl_rtc*) to enable the call to
 * happen correctly.
 *
 * This test code should be placed at location 0x(6)A000,
 * and it should write to the RAM buffer before returning.
 */
#include "sdcc2iar.h" // not needed except for MAIN program for return
#include "simpleGATTprofile.h"

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
	buf[1] = 'p';
	SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR1, buf );
	SimpleProfile_SetParameter( SIMPLEPROFILE_CHAR1, sizeof(uint8), buf+1 );
	SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR1, buf+2 );

	sdcc_main_return; /* return macro, which is same as assembly below */
}