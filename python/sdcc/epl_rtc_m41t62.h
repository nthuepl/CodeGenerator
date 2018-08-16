/**************************************************************************************************
  Filename:       epl_rtc_m41t62.h
  Revised:        $Date: 2010-09-29 11:12:58 -0700 (Wed, 29 Sep 2010) $
  Revision:       $Revision: 23938 $

  Description:    Header file for control of the accelerometer on the keyfob
                  board in the CC2540DK-mini kit.

  Copyright 2009 - 2010 Texas Instruments Incorporated. All rights reserved.
**************************************************************************************************/

#ifndef EPL_RTC_M41T62_H
#define EPL_RTC_M41T62_H


#include "hal_types.h"
#include "hal_mcu.h"
#include "hal_i2c.h"

/** An enum describing register map in M41T62.
 */
typedef enum {
	RTC_M41T62_10THS_100THS_OF_SECONDS = 0x00,
	RTC_M41T62_SECONDS = 0x01,
	RTC_M41T62_MINUTES = 0x02,
	RTC_M41T62_HOURS =   0x03,
	RTC_M41T62_DAY =     0x04,
	RTC_M41T62_DATE =    0x05,
	RTC_M41T62_CENTURY_MONTH =  0x06, /* Century = 0~3, Month = 1 ~ 12 */
	RTC_M41T62_YEAR =           0x07,
	RTC_M41T62_CALIBRATION =    0x08,
	RTC_M41T62_WATCHDOG =       0x09,
	RTC_M41T62_ALARM_MONTH =    0x0A,
	RTC_M41T62_ALARM_DATE =     0x0B,
	RTC_M41T62_ALARM_HOUR =     0x0C,
	RTC_M41T62_ALARM_MINUTES =  0x0D,
	RTC_M41T62_ALARM_SECONDS =  0x0E,
	RTC_M41T62_FLAGS =          0x0F,
        RTC_M41T62_ALARM_ONCEPERSECOND = 0x1F,
        RTC_M41T62_ALARM_ONCEPERMINUTE = 0x1E,
        RTC_M41T62_ALARM_ONCEPERHOUR =   0x3C,
        RTC_M41T62_ALARM_ONCEPERDAY =    0x18,
        RTC_M41T62_ALARM_ONCEPERYEAR =   0x00
} epl_rtc_m41t62_reg;






//***********************************************************************************
// Function prototypes
      
void rtcInit(void);
void rtcSetTime(uint8 second,uint8 minute, uint8 hour );

void rtcSetDate(uint8 day, uint8 date, uint8 month, uint8 year, uint8
		century);

void rtcGetTime(__xdata uint8* hour, __xdata uint8* minute, __xdata
		uint8* second );

void rtcGetDate(__xdata uint8* day, __xdata uint8* date, __xdata uint8*
		month, __xdata uint8* year, __xdata uint8* century);

void rtcReadDateAndTime(__xdata uint8* hour, __xdata uint8* minute,
		__xdata uint8* second, __xdata uint8* day , __xdata uint8* date,
		__xdata uint8* month, __xdata uint8* year);

void rtcSetAlarm( uint8 alarmMonth, uint8 alarmDate, uint8 alarmHour ,
		uint8 alarmMinutes, uint8 alarmSeconds, uint8 repeatMode );

void rtcGetAlarm(__xdata uint8* alarmMonth, __xdata uint8* alarmDate,
		__xdata uint8* alarmHour , __xdata uint8* alarmMinutes, __xdata
		uint8* alarmSeconds, __xdata uint8* alarmReMode );

uint8 rtcGetAlarmStatus( void );

void rtcSetWatchDog( void );


#endif
