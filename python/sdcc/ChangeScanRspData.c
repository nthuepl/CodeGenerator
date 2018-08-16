#include "sdcc2iar.h"
#include "bcomdef.h"
#include "OSAL.h"
#include "OSAL_PwrMgr.h"

#include "OnBoard.h"
#include "hal_adc.h"
#include "hal_led.h"

#include "gatt.h"
#include "gap.h"
#include "hci.h"

#include "peripheral.h"
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

__xdata __at (MAP_notify+3) uint8 buf[20];
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
void Main()
{
	scanRspData[0] = 0x0B;   // length of this data
	scanRspData[1] = GAP_ADTYPE_LOCAL_NAME_COMPLETE;
	scanRspData[2] = 'E';   // 'E'
	scanRspData[3] = 'P';   // 'P'
	scanRspData[4] = 'L';   // 'L'
	scanRspData[5] = 0x27;   // '''
	scanRspData[6] = 0x73;   // 's'
	scanRspData[7] = 0x20;   // ' '
	scanRspData[8] = 0x6E;   // 'n'
	scanRspData[9] = 0x6F;   // 'o'
	scanRspData[10] = 0x64;   // 'd'
	scanRspData[11] = 0x65;   // 'e'
	scanRspData[12] = 0x05;   // length of this data
	scanRspData[13] = GAP_ADTYPE_SLAVE_CONN_INTERVAL_RANGE,
	scanRspData[14] = LO_UINT16( 80 );   // 100ms
	scanRspData[15] = HI_UINT16( 80 );
	scanRspData[16] = LO_UINT16( 800 );   // 1s
	scanRspData[17] = HI_UINT16( 800 );
	scanRspData[18] = 0x02;   // length of this data
	scanRspData[19] = GAP_ADTYPE_POWER_LEVEL;
	scanRspData[20] = 0;       // 0dBm

    GAPRole_SetParameter( GAPROLE_SCAN_RSP_DATA, sizeof ( scanRspData ), scanRspData );

	sdcc_main_return; /* return macro, which is same as assembly below */
}