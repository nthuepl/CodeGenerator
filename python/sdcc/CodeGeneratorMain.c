/*********************************************************************
 * INCLUDES
 */
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


__xdata static uint8 scanRspData[31];
__xdata static uint8 advertData[31];
__xdata static uint8 attDevicename[31];

void Main()
{	
	/* advert data */
	// advertData[0] = 0x02;	// length of this data
	// advertData[1] = GAP_ADTYPE_FLAGS;
	// advertData[2] = GAP_ADTYPE_FLAGS_GENERAL | GAP_ADTYPE_FLAGS_BREDR_NOT_SUPPORTED;
	// advertData[3] = 0x03;	// length of this data
	// advertData[4] = GAP_ADTYPE_16BIT_MORE;      // some of the UUID's, but not all
	// advertData[5] = LO_UINT16( SIMPLEPROFILE_SERV_UUID );
	// advertData[6] = HI_UINT16( SIMPLEPROFILE_SERV_UUID );
	// advertData[7] = 5;	// length of this data
	// advertData[8] = GAP_ADTYPE_MANUFACTURER_SPECIFIC;
	// advertData[9] = '0';
	// advertData[10] = 'e';
	// advertData[11] = 'p';
	// advertData[12] = 'l';
	
	/* iOS scan name */
	// attDeviceName[0] ='E';
	// attDeviceName[1] ='P';
	// attDeviceName[2] ='L';
	// attDeviceName[3] ='\'';
	// attDeviceName[4] ='s';
	// attDeviceName[5] =' ';
	// attDeviceName[6] ='B';
	// attDeviceName[7] ='L';
	// attDeviceName[8] ='E';
	// attDeviceName[9] =' ';
	// attDeviceName[10] ='N';
	// attDeviceName[11] ='o';
	// attDeviceName[12] ='d';
	// attDeviceName[13] ='e';
	
	/* Android scan name */
	// scanRspData[0] = 0x0B;   // length of this data
	// scanRspData[1] = GAP_ADTYPE_LOCAL_NAME_COMPLETE;
	// scanRspData[2] = 'E';   // 'E'
	// scanRspData[3] = 'P';   // 'P'
	// scanRspData[4] = 'L';   // 'L'
	// scanRspData[5] = '\'';  // '''
	// scanRspData[6] = 's';   // 's'
	// scanRspData[7] = ' ';   // ' '
	// scanRspData[8] = 'n';   // 'n'
	// scanRspData[9] = 'o';   // 'o'
	// scanRspData[10] = 'd';  // 'd'
	// scanRspData[11] = 'e';  // 'e'
	// scanRspData[12] = 0x05; // length of this data
	// scanRspData[13] = GAP_ADTYPE_SLAVE_CONN_INTERVAL_RANGE,
	// scanRspData[14] = LO_UINT16( 80 );   // 100ms
	// scanRspData[15] = HI_UINT16( 80 );
	// scanRspData[16] = LO_UINT16( 800 );   // 1s
	// scanRspData[17] = HI_UINT16( 800 );
	// scanRspData[18] = 0x02;   // length of this data
	// scanRspData[19] = GAP_ADTYPE_POWER_LEVEL;
	// scanRspData[20] = 0;       // 0dBm

    
	// Set attDeviceName
	// GGS_SetParameter( GGS_DEVICE_NAME_ATT, GAP_DEVICE_NAME_LEN, attDeviceName );
	// Set scan response data
	// GAPRole_SetParameter( GAPROLE_SCAN_RSP_DATA, sizeof ( scanRspData ), scanRspData );
	// Set advertising data
	// GAPRole_SetParameter( GAPROLE_ADVERT_DATA, sizeof( advertData ), advertData );
	
	osal_start_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_EVT_1, 500 );

	
	sdcc_main_return; /* return macro, which is same as assembly below */
}