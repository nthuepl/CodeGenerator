/*********************************************************************
 * INCLUDES
 */
#include "iar2sdcc.h"
#include "sdcc2iar.h"
#include "CodeGeneratorJumpTable.h"
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

void Main()
{	
	// int i = 0, j;

	attDeviceName[0] ='E';
	attDeviceName[1] ='c';
	attDeviceName[2] ='o';
	attDeviceName[3] ='G';
	attDeviceName[4] ='e';
	attDeviceName[5] ='n';
/*
	attDeviceName[0] ='N';
	attDeviceName[1] ='e';
	attDeviceName[2] ='o';
	attDeviceName[3] ='\'';
	attDeviceName[4] ='s';
	attDeviceName[5] =' ';
*/		
	// Set the GAP Characteristics
	buf[0] = GGS_SetParameter( GGS_DEVICE_NAME_ATT, GAP_DEVICE_NAME_LEN, attDeviceName );
		
	// for( i; i < GAP_DEVICE_NAME_LEN; i++ )
		// buf[i] = attDeviceName[i];

	sdcc_main_return; /* return macro, which is same as assembly below */
}