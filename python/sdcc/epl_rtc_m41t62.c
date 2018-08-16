/*
 * edited for SDCC.
 * Compile with sdcc -DHOST_CONFIG=CENTRAL_CONFIG -c epl_rtc_m41t62.c
 */
/**************************************************************************************************
  Filename:       epl_rtc_m41t62.c
  Revised:        $Date: 2012-12-16$
  Revision:       $ TONG KUN LAI$

  Description:    Control of the RTC on the EcoBT board.

  Copyright 2012 EPL NTHU. All rights reserved.

**************************************************************************************************/
#if defined( CC2541) || defined( CC2541S )
#include "cc2540sfr.h"
#else // CC2540
#include "cc2540sfr.h"
#endif // CC2541 || CC2541S

#include "gatt.h"

//rtc
#include "hal_i2c.h"
#include "epl_rtc_m41t62.h"

/*****local variable*****/

uint8 slaveAddress = 0x68; // 1101000 0

/** \brief  This is will initialize I2C interface and M41T62 RTC
* \param[in]       void
*/

void rtcInit(void)
{  
  uint8 start_rtc[2] = {RTC_M41T62_FLAGS,0x00};
  HalI2CInit(slaveAddress,i2cClock_197KHZ); 
  
//  P2SEL &= 0xFD;
//  P2DIR |= 0x02;
//  P2_1 = 1;
  /*****Alarm interrupt setting*****/
  P0SEL &= 0xFE;        // port 0.0 as GPIO
  P0DIR &= 0xFE;        // port 0.0 as input
  PICTL |= 0x01;        // port interrupt control, 0 rising edge, 1 falling edge
  P0IEN |= 0x01;        // IOC module, prot 0 interrupt mask, 0 interrupts are disabled, 1 interrupt s are enabled.
  IEN1_P0IE   = 1;           // CPU module, prot 0 interrupt mask, 0 interrupts are disabled, 1 interrupt s are enabled.
  P0IFG  = 0x00;        // P0 interrupt Flag Status
  IRCON_P0IF   = 0;           // port 0 interrupt status flag
  IEN0_EA     = 1;           // enable interrupt
  


  HalI2CWrite(2,start_rtc);
  

} //  rtcInit function end

/** \brief	Write the Time data to M41T62 RTC
*
* Write the Time data to M41T62 RTC
*
* \param[in]       hour
*     hour data to write
* \param[in]       minute
*     minute data to write
* \param[in]       second
*     second data to write
*/
 

void rtcSetTime(uint8 second,uint8 minute,uint8 hour)
{
  uint8 set_time[4] = {RTC_M41T62_SECONDS,second,minute,hour};
  HalI2CWrite(4,set_time);

} // end function rtcSetTime

/** \brief	Read Time data to M41T62 RTC
*
* Read the Time data to M41T62 RTC
*
* \param[in]       hour
*     parameter for read  hour data of rtc
* \param[in]       minute
*     parameter for read  minute data of rtc 
* \param[in]       second
*     parameter for read  second data of rtc 
*/
void rtcGetTime( uint8* hour, uint8* minute, uint8* second )
{
  uint8 get_time[3] = {0,0,0};
  uint8 reg_addr = RTC_M41T62_SECONDS;
  
  HalI2CWrite(1,&reg_addr); 
  HalI2CRead(3,get_time);
   
  *hour = get_time[2];
  *minute = get_time[1];
  *second = get_time[0];
  
} // end function rtcGetTime


/** \brief	Write Date data to M41T62 RTC
*
* Write the Date data to M41T62 RTC
*
* \param[in]              day
*     dat data to write
* \param[in]              date
*     date data to write
* \param[in]              month
*     month data to write
* \param[in]              year
*     year data to write
* \param[in]              century
*     century data to write
*/
void rtcSetDate(uint8 day, uint8 date, uint8 month, uint8 year, uint8 century)
{
  uint8 set_date[5] = {RTC_M41T62_DAY, day, date, month, year};
  day = 0x07&day; 
  date = date&0x3F;
  month = (0x1F&month) + (century<<6);
  HalI2CWrite(5,set_date);
  
} // end function rtcSetDate


/** \brief	Read da data to M41T62 RTC
*
* Read the Time data to M41T62 RTC
*
* \param[in]       day
*     parameter for read  day data of rtc
* \param[in]       date
*     parameter for read  date data of rtc
* \param[in]       month
*     parameter for read  month data of rtc
* \param[in]       year
*     parameter for read  year data of rtc
* \param[in]       century
*     parameter for read  century data of rtc
*/
void rtcGetDate(uint8* day, uint8* date, uint8* month, uint8* year, uint8* century )
{
  uint8 get_date[4] = {0,0,0,0};
  uint8 reg_addr = RTC_M41T62_DAY;
  
  HalI2CWrite(1,&reg_addr); 
  HalI2CRead(4,get_date);
   
  *year = get_date[3];
  *month = (get_date[2]&0x1F);
  *date = get_date[1];
  *day = (get_date[0]&0x0F);
  *century = (get_date[2]>>6);
} // end function rtcGetDate


/** \brief	Read Time and Date data to M41T62 RTC
*
* Read the Time and Date data to M41T62 RTC
*
* \param[in]       hour
*     parameter for read  hour data of rtc
* \param[in]       minute
*     parameter for read  minute data of rtc 
* \param[in]       second
*     parameter for read  second data of rtc 
* \param[in]       day
*     parameter for read  day data of rtc
* \param[in]       date
*     parameter for read  date data of rtc
* \param[in]       month
*     parameter for read  month data of rtc
* \param[in]       year
*     parameter for read  year data of rtc
* \param[in]       century
*     parameter for read  century data of rtc
*/
void rtcReadDateAndTime(uint8* year, uint8* month, uint8* date, uint8* day
                        , uint8* hour, uint8* minute, uint8* second)
{
  uint8 date_and_time[7] = {0,0,0,0,0,0,0};
  uint8 reg_addr = RTC_M41T62_SECONDS;
  
  HalI2CWrite(1,&reg_addr); 
  HalI2CRead(7,date_and_time);
   
  *second = date_and_time[0];
  *minute = date_and_time[1];
  *hour = date_and_time[2];
  *day = date_and_time[3];
  *date = date_and_time[4];
  *month = date_and_time[5];
  *year = date_and_time[6];
  
} // end rtcReadDateAndTime function


/** \brief	Enable the alarm of M41T62 RTC
*
* write the Time and Date data to the alarm of M41T62 RTC
*
* \param[in]              alramMonth 01~12
*     alramMonth data to write
* \param[in]              alarmDate 01~31
*     alarmDate data to write
* \param[in]              alarmHour 00~23
*     alarmHour data to write
* \param[in]              alarmMinutes 00~59
*     alarmMinutes data to write
* \param[in]              alarmSeconds 00~59
*     alarmSeconds data to write
*/
void rtcSetAlarm( uint8 alarmMonth, uint8 alarmDate, uint8 alarmHour
                  , uint8 alarmMinutes, uint8 alarmSeconds, uint8 repeatMode )
{
  
  uint8 rpt1 = repeatMode;
  uint8 rpt2 = repeatMode;
  uint8 rpt3 = repeatMode;
  uint8 rpt4 = repeatMode;
  uint8 rpt5 = repeatMode;
  uint8 set_alarm[6];
  rpt5 = ( rpt5&0x10 ) << 2;  // 0001 0000 >> 0100 0000
  rpt4 = ( rpt4&0x08 ) << 4;  // 0000 1000 >> 1000 0000
  rpt3 = ( rpt3&0x04 ) << 5;  // 0000 0100 >> 1000 0000
  rpt2 = ( rpt2&0x02 ) << 6;  // 0000 0010 >> 1000 0000
  rpt1 = ( rpt1&0x01 ) << 7;  // 0000 0001 >> 1000 0000
  
  set_alarm[0] = RTC_M41T62_ALARM_MONTH;
	set_alarm[1] = (0x80 | alarmMonth) ;
	set_alarm[2] = rpt4 + rpt5 + ( 0x3F & alarmDate ) ;
	set_alarm[3] = rpt3 + ( 0x3F & alarmHour )  ;
	set_alarm[4] = rpt2 + ( 0x7F & alarmMinutes ) ;
	set_alarm[5] = rpt1 + ( 0x7F & alarmSeconds );
  
  HalI2CWrite(6,set_alarm);
  
//  rtcGetAlarmStatus();
} // end function rtcSetAlarm


/** \brief	read the alarm of M41T62 RTC
*
* read the Time and Date data to the alarm of M41T62 RTC
*
* \param[in]              alramMonth
*     alramMonth data to read
* \param[in]              alarmDate
*     alarmDate data to read
* \param[in]              alarmHour
*     alarmHour data to read
* \param[in]              alarmMinutes
*     alarmMinutes data to read
* \param[in]              alarmSeconds
*     alarmSeconds data to read
*/
void rtcGetAlarm( unsigned char* alarmMonth, unsigned char* alarmDate, unsigned char* alarmHour
                 , unsigned char* alarmMinutes, unsigned char* alarmSeconds, unsigned char* alarmReMode )
{
  uint8 get_alarm[5] = {0,0,0,0,0};
  uint8 reg_addr = RTC_M41T62_ALARM_MONTH;
  
  HalI2CWrite(1,&reg_addr); 
  HalI2CRead(5,get_alarm);
   
  *alarmMonth = get_alarm[0]&0x1F;
  *alarmDate = get_alarm[1]&0x3F;
  *alarmHour = get_alarm[2]&0x3F;
  *alarmMinutes = get_alarm[3]&0x7F;
  *alarmSeconds = get_alarm[4]&0x7F;
  
  *alarmReMode = 0x00;
  
  /* rpt bit 5 */
  *alarmReMode += ((get_alarm[1]&0x40)>>2);
    /* rpt bit 4 */
  *alarmReMode += ((get_alarm[1]&0x80)>>4);
    /* rpt bit 3 */
  *alarmReMode += ((get_alarm[2]&0x80)>>5);
    /* rpt bit 2 */
  *alarmReMode += ((get_alarm[3]&0x80)>>6);
    /* rpt bit 1 */
  *alarmReMode += ((get_alarm[4]&0x80)>>7);
    
    
} // end function rtcGetAlarm

uint8 rtcGetAlarmStatus( void )
{
  
  uint8 get_alstatus = 0xFF;
  uint8 reg_addr = RTC_M41T62_FLAGS;
  
  HalI2CWrite(1,&reg_addr); 
  HalI2CRead(1,&get_alstatus);
   
  return get_alstatus;
  
} // end function rtcGetAlarmStatus


