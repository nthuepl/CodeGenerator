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
#include "epl_rtc_m41t62.h"

#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro for either CC2540 or CC2541"
#endif

__xdata __at (MAP_notify+3) uint8 buf[4];
__xdata __at (MAP_notify+3+4) uint16 fer[4];

__xdata static uint8 * second;
__xdata static uint8 * hour;
__xdata static uint8 * minute;

void Main() {
	rtcInit();
	//rtcGetTime(buf /*hour*/, buf+1 /*min*/, buf+2/*second*/);
	rtcSetDate( 0x04, 0x08, 0x05, 0x14, 0x10 );
	rtcGetDate( buf + 0, buf + 1, buf + 2, buf + 3, buf + 4 );
	rtcGetTime( hour, minute, second );
	rtcSetAlarm( 0x05/*month*/, 0x08/*date*/, 0x19/*hour*/, 
			0x55/*minute*/, 0x00/*second*/, 0x02/*repeatmode*/ );
	rtcGetAlarm( buf + 5 /*alarmMonth*/, buf + 6 /*alarmDate*/, buf + 7 /*alarmHour*/
            , buf + 8 /*alarmMinutes*/, buf + 9 /*alarmSeconds*/, buf + 10 /*alarmReMode*/ );
	sdcc_main_return; /* return macro, which is same as assembly below */
}