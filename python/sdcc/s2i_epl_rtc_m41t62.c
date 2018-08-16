/*
 * edited for SDCC.
 *
	This is the binding file that enables SDCC caller to call IAR API.
	binding for epl_epl_rtc_m41t62.c
	Compile this using
	sdcc -c --stack-auto s2i_epl_acc_lis331dl.c
	You can ignore the warning about parameter not used.
 */
#include "epl_rtc_m41t62.h"
#include "sdcc2iar.h"
#ifdef CC2540
#error "rtc not supported on CC2540 yet"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif


void rtcInit(void)
{  
	s2i_call_void(MAP_rtcInit); // was 0x9AC
	// based on
	// EcoKit/EcoCast/Device/EcoBT/Project/ble/CodeGenerator/CC2541DB/CC2541/List
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
	s2i_call_u8_u8_u8(MAP_rtcSetTime); // was 0x9B2
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
void rtcGetTime(__xdata  uint8* hour, __xdata uint8* minute, __xdata uint8* second )
{
	s2i_call_p_p_p(MAP_rtcGetTime); // was 0x9B8
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
	s2i_call_u8_u8_u8_u8_u8(MAP_rtcSetDate); // was 0x9BE
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
void rtcGetDate(__xdata uint8* day, __xdata uint8* date, __xdata uint8* month, __xdata uint8* year, __xdata uint8* century )
{
	s2i_call_p_p_p_p_p(MAP_rtcGetDate); // was 0x9C4
} // end function rtcGetDate

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

void rtcGetAlarm(__xdata uint8* alarmMonth, __xdata uint8* alarmDate,
		__xdata uint8* alarmHour , __xdata uint8* alarmMinutes, __xdata
		uint8* alarmSeconds, __xdata uint8* alarmReMode )
{
	s2i_call_p_p_pn(MAP_rtcGetAlarm, 4); // was 0x9D0
} // end function rtcGetAlarm

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
	s2i_call_u8_u8_u8_u8_u8_u8_u8(MAP_rtcSetAlarm); // was 0x9CA
	
  //uint8 rpt1 = repeatMode;
  //uint8 rpt2 = repeatMode;
  //uint8 rpt3 = repeatMode;
  //uint8 rpt4 = repeatMode;
  //uint8 rpt5 = repeatMode;
  //uint8 set_alarm[6];
  //rpt5 = ( rpt5&0x10 ) << 2;  // 0001 0000 >> 0100 0000
  //rpt4 = ( rpt4&0x08 ) << 4;  // 0000 1000 >> 1000 0000
  //rpt3 = ( rpt3&0x04 ) << 5;  // 0000 0100 >> 1000 0000
  //rpt2 = ( rpt2&0x02 ) << 6;  // 0000 0010 >> 1000 0000
  //rpt1 = ( rpt1&0x01 ) << 7;  // 0000 0001 >> 1000 0000
  
  //set_alarm[0] = RTC_M41T62_ALARM_MONTH;
	//set_alarm[1] = (0x80 | alarmMonth) ;
	//set_alarm[2] = rpt4 + rpt5 + ( 0x3F & alarmDate ) ;
	//set_alarm[3] = rpt3 + ( 0x3F & alarmHour )  ;
	//set_alarm[4] = rpt2 + ( 0x7F & alarmMinutes ) ;
	//set_alarm[5] = rpt1 + ( 0x7F & alarmSeconds );
  
  //HalI2CWrite(6,set_alarm);
  
//  rtcGetAlarmStatus();
} // end function rtcSetAlarm


#ifdef adafdfadfadfadfadfad
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
  //uint8 date_and_time[7] = {0,0,0,0,0,0,0};
  //uint8 reg_addr = RTC_M41T62_SECONDS;
  
  //HalI2CWrite(1,&reg_addr); 
  //HalI2CRead(7,date_and_time);
   
  //*second = date_and_time[0];
  //*minute = date_and_time[1];
  //*hour = date_and_time[2];
  //*day = date_and_time[3];
  //*date = date_and_time[4];
  //*month = date_and_time[5];
  //*year = date_and_time[6];
  
} // end rtcReadDateAndTime function

uint8 rtcGetAlarmStatus( void )
{
	// u8_call_void(codeAddress);   
	// ret_u8();   
  // uint8 get_alstatus = 0xFF;
  // uint8 reg_addr = RTC_M41T62_FLAGS;
  
  // HalI2CWrite(1,&reg_addr); 
  // HalI2CRead(1,&get_alstatus);
   
  return 0;
  
} // end function rtcGetAlarmStatus

#endif
