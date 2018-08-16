/*********************************************************************
 * INCLUDES
 */
#include "iar2sdcc.h"
#include "sdcc2iar.h"
#include "bcomdef.h"
#include "OSAL.h"
#include "OSAL_PwrMgr.h"

#include "OnBoard.h"
#include "hal_adc.h"
#include "hal_led.h"
#include "hal_key.h"
#include "hal_lcd.h"

#include "gatt.h"
#include "gap.h"
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
	__xdata static uint8 advertData[] =
	{
	// Flags; this sets the device to use limited discoverable
	// mode (advertises for 30 seconds at a time) instead of general
	// discoverable mode (advertises indefinitely)
	0x02,   // length of this data
	GAP_ADTYPE_FLAGS,
	GAP_ADTYPE_FLAGS_GENERAL | GAP_ADTYPE_FLAGS_BREDR_NOT_SUPPORTED,

	// service UUID, to notify central devices what services are included
	// in this peripheral
	0x03,   // length of this data
	GAP_ADTYPE_16BIT_MORE,      // some of the UUID's, but not all
	LO_UINT16( SIMPLEPROFILE_SERV_UUID ),
	HI_UINT16( SIMPLEPROFILE_SERV_UUID ),
	
	5,
	GAP_ADTYPE_MANUFACTURER_SPECIFIC,
	'0',
	'E',
	'P',
	'L',
	};
	GAPRole_SetParameter( GAPROLE_ADVERT_DATA, sizeof( advertData ), advertData );
	
	sdcc_main_return; /* return macro, which is same as assembly below */
}