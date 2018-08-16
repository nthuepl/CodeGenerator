/*********************************************************************
 * INCLUDES
 */
#include "bcomdef.h"
#include "OSAL.h"
#include "OSAL_PwrMgr.h"

#include "OnBoard.h"
#include "hal_adc.h"
#include "hal_led.h"
#include "hal_key.h"
#include "hal_lcd.h"

#include "gatt.h"

#include "hci.h"

#if defined ( PLUS_BROADCASTER )
  #include "peripheralBroadcaster.h"
#else
  #include "peripheral.h"
#endif

#include "gapbondmgr.h"

#include "simpleBLEPeripheral.h"

#include "gapgattserver.h"
#include "gattservapp.h"
#include "devinfoservice.h"
#include "simpleGATTprofile.h"
#include "accelerometer.h"
#include "epl_hal_uart.h"
#include "epl_hal_spi.h"
#include "epl_acc_lis331dl.h"
#include "battservice.h"

#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#include "epl_rtc_m41t62.h"
#include "timeservice.h"
#endif

// How often (in ms) to read the accelerometer
#define ACCEL_READ_PERIOD             500

// Minimum change in accelerometer before sending a notification
#define ACCEL_CHANGE_THRESHOLD        15

__xdata __at (MAP_notify+3) uint8 buf[4];
__xdata __at (MAP_notify+3+4) uint16 fer[4];

// Accelerometer Profile Parameters
__xdata __at (MAP_accelEnabler) uint8 accelEnabler;
// Task ID for internal task/event processing
__xdata __at (MAP_simpleBLEPeripheral_TaskID) uint8 simpleBLEPeripheral_TaskID;
// GAP GATT Attributes
__xdata __at (MAP_attDeviceName)  uint8 attDeviceName[GAP_DEVICE_NAME_LEN];

#if defined(CC2541)
// Time service Profile Parameters
__xdata __at (MAP_timeEnabler) uint8 timeEnabler;
// How often (in ms) to read the time
#define TIME_READ_PERIOD              1000
#endif



/*********************************************************************
 * @fn      cg_simpleProfileChangeCB
 *
 * @brief   Callback from SimpleBLEProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
void cg_simpleProfileChangeCB( uint8 paramID )
{
	switch( paramID )
	{
	case SIMPLEPROFILE_CHAR1:
		SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR1, buf );
		break;
    
	case SIMPLEPROFILE_CHAR3:
		SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR3, buf );
		break;
    
	default:
		// should not reach here!
		break;
	}
}

/*********************************************************************
 * @fn      cg_accelEnablerChangeCB
 *
 * @brief   Called by the Accelerometer Profile when the Enabler Attribute
 *          is changed.
 *
 * @param   none
 *
 * @return  none
 */
void cg_accelEnablerChangeCB( void )
{
	bStatus_t status;
	status = Accel_GetParameter( ACCEL_ENABLER, &accelEnabler );

	if (status == SUCCESS){
		if (accelEnabler){
		// Initialize accelerometer
		accInit();

		// Setup timer for accelerometer task
		osal_start_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT, ACCEL_READ_PERIOD );
		} else {
		// Stop the acceleromter
		osal_stop_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT);
		}
	} else {
		//??
	}
}

/*********************************************************************
 * @fn      cg_battProfileChangeCB
 *
 * @brief   Callback from battserviceProfile indicating a value change
 *
 * @param   event - event of the value that was changed.
 *
 * @return  none
 */
void cg_battProfileChangeCB( uint8 event )
{
	switch( event ){
	case BATT_LEVEL_NOTI_DISABLED:
		break;
	case BATT_LEVEL_NOTI_ENABLED:
		break;
	default:
		break;
	}
}

void cg_EVT_1_CB( void )
{
	P0_5 ^= 1;
	osal_start_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_EVT_1, 100 );
}

void cg_EVT_2_CB( void )
{

}

void cg_EVT_3_CB( void )
{

}

void cg_EVT_4_CB( void )
{

}

#if defined(CC2541)
/*********************************************************************
 * @fn      cg_timeserviceChangeCB
 *
 * @brief   Callback from timeserviceProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
void cg_timeserviceChangeCB( uint8 paramID )
{
	bStatus_t status;
	
	switch( paramID ){
	case TIME_ENABLER:
		status = timeservice_GetParameter( TIME_ENABLER, &timeEnabler );
		if (status == SUCCESS){
			if (timeEnabler){
				// Initialize RTC
				rtcInit();
        
				/* uint8 alarmMonth, uint8 alarmDate, uint8 alarmHour , uint8 alarmMinutes, uint8 alarmSeconds, uint8 repeatMode */
				rtcSetAlarm( 0x03, 0x17, 0x16, 0x23, 0x03, 0x01 );
				rtcSetTime(0x00, 0x23, 0x16 ); /* uint8 second,uint8 minute, uint8 hour */
				rtcSetDate(0x01, 0x17, 0x03, 0x14, 0x03); /* uint8 day, uint8 date, uint8 month, uint8 year, uint8 century */
				// Setup timer for time servicetask
				osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
			} else {
				// Stop the time service
				osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
			}
		} else {
			//??
		}
		break;
        
	case TIME:
		osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
		osal_start_timerEx( simpleBLEPeripheral_TaskID, SET_TIME_EVT, 500 );
		break;
    
	case DATE:
		osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
		osal_start_timerEx( simpleBLEPeripheral_TaskID, SET_DATE_EVT, 500 );
		break;
    
	case ALARM:
		osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
		osal_start_timerEx( simpleBLEPeripheral_TaskID, SET_ALARM_EVT, 500 );
		break;
	}
}
#endif