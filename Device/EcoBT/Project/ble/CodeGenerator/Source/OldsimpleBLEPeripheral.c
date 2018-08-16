/**************************************************************************************************
  Filename:       simpleBLEPeripheral.c
  Revised:        $Date: 2010-08-06 08:56:11 -0700 (Fri, 06 Aug 2010) $
  Revision:       $Revision: 23333 $

  Description:    This file contains the Simple BLE Peripheral sample application
                  for use with the CC2540 Bluetooth Low Energy Protocol Stack.
**************************************************************************************************/

/*********************************************************************
 * INCLUDES
 */

#include "bcomdef.h"
#include "OSAL.h"
#include "OSAL_PwrMgr.h"
#include "OSAL_Memory.h"

#include "OnBoard.h"
#include "hal_adc.h"
#include "hal_led.h"
#include "hal_key.h"
#include "hal_lcd.h"

#include "gatt.h"

#include "hci.h"

#include "gapgattserver.h"
#include "gattservapp.h"
#include "devinfoservice.h"
#include "simpleGATTprofile.h"

#if defined( CC2540_MINIDK )
  #include "simplekeys.h"
#endif

#if defined ( PLUS_BROADCASTER )
  #include "peripheralBroadcaster.h"
#else
  #include "peripheral.h"
#endif

#include "gapbondmgr.h"

#include "simpleBLEPeripheral.h"

#if defined FEATURE_OAD
  #include "oad.h"
  #include "oad_target.h"
#endif

//#define ECOEXEC_DEBUG
#ifdef ECOEXEC_DEBUG
#include "epl_hal_uart.h"
#endif
//#include "accelerometer.h"
//#include "EcoExecGATTprofile.h"
//#include "timeservice.h"
//#include "epl_hal_spi.h"
//#include "epl_acc_lis331dl.h"
#include "2541\epl_rtc_m41t62.h"
/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * CONSTANTS
 */

// How often to perform periodic event
#define SBP_PERIODIC_EVT_PERIOD                   5000

// What is the advertising interval when device is discoverable (units of 625us, 160=100ms)
#define DEFAULT_ADVERTISING_INTERVAL          160

// Whether to enable automatic parameter update request when a connection is formed
#define DEFAULT_ENABLE_UPDATE_REQUEST         FALSE

// Limited discoverable mode advertises for 30.72s, and then stops
// General discoverable mode advertises indefinitely

#if defined ( CC2540_MINIDK )
#define DEFAULT_DISCOVERABLE_MODE             GAP_ADTYPE_FLAGS_LIMITED
#else
#define DEFAULT_DISCOVERABLE_MODE             GAP_ADTYPE_FLAGS_GENERAL
#endif  // defined ( CC2540_MINIDK )

// Minimum connection interval (units of 1.25ms, 80=100ms) if automatic parameter update request is enabled
#define DEFAULT_DESIRED_MIN_CONN_INTERVAL     80

// Maximum connection interval (units of 1.25ms, 800=1000ms) if automatic parameter update request is enabled
#define DEFAULT_DESIRED_MAX_CONN_INTERVAL     800

// Slave latency to use if automatic parameter update request is enabled
#define DEFAULT_DESIRED_SLAVE_LATENCY         0

// Supervision timeout value (units of 10ms, 1000=10s) if automatic parameter update request is enabled
#define DEFAULT_DESIRED_CONN_TIMEOUT          1000

// Company Identifier: Texas Instruments Inc. (13)
#define TI_COMPANY_ID                         0x000D

#define INVALID_CONNHANDLE                    0xFFFF

// Length of bd addr as a string
#define B_ADDR_STR_LEN                        15

#if defined ( PLUS_BROADCASTER )
  #define ADV_IN_CONN_WAIT                    500 // delay 500 ms
#endif

// How often (in ms) to read the accelerometer
#define ACCEL_READ_PERIOD             500
// Minimum change in accelerometer before sending a notification
#define ACCEL_CHANGE_THRESHOLD        15
// How often (in ms) to read the time
#define TIME_READ_PERIOD 2000

// Accelerometer Profile Parameters
static uint8 accelEnabler = FALSE;

// Time service Profile Parameters
static uint8 timeEnabler = FALSE;
   
/*********************************************************************
 * TYPEDEFS
 */

/*********************************************************************
 * GLOBAL VARIABLES
 */

uint8 Message[512];
uint8 HeaderPacket[4];
uint8 i;
attHandleValueNoti_t notify;
extern uint16 EcoExecProfileConnHandle;

/*********************************************************************
 * EXTERNAL VARIABLES
 */

/*********************************************************************
 * EXTERNAL FUNCTIONS
 */

/*********************************************************************
 * LOCAL VARIABLES
 */
static uint8 simpleBLEPeripheral_TaskID;   // Task ID for internal task/event processing

static gaprole_States_t gapProfileState = GAPROLE_INIT;

// GAP - SCAN RSP data (max size = 31 bytes)
static uint8 scanRspData[] =
{
  // complete name
  0x0B,   // length of this data
  GAP_ADTYPE_LOCAL_NAME_COMPLETE,
  0x4E,   // 'N'
  0x65,   // 'e'
  0x6F,   // 'o'
  0x27,   // '''
  0x73,   // 's'
  0x20,   // ' '
  0x6E,   // 'n'
  0x6F,   // 'o'
  0x64,   // 'd'
  0x65,   // 'e'

  // connection interval range
  0x05,   // length of this data
  GAP_ADTYPE_SLAVE_CONN_INTERVAL_RANGE,
  LO_UINT16( DEFAULT_DESIRED_MIN_CONN_INTERVAL ),   // 100ms
  HI_UINT16( DEFAULT_DESIRED_MIN_CONN_INTERVAL ),
  LO_UINT16( DEFAULT_DESIRED_MAX_CONN_INTERVAL ),   // 1s
  HI_UINT16( DEFAULT_DESIRED_MAX_CONN_INTERVAL ),

  // Tx power level
  0x02,   // length of this data
  GAP_ADTYPE_POWER_LEVEL,
  0       // 0dBm
};

// GAP - Advertisement data (max size = 31 bytes, though this is
// best kept short to conserve power while advertisting)
static uint8 advertData[] =
{
  // Flags; this sets the device to use limited discoverable
  // mode (advertises for 30 seconds at a time) instead of general
  // discoverable mode (advertises indefinitely)
  0x02,   // length of this data
  GAP_ADTYPE_FLAGS,
  DEFAULT_DISCOVERABLE_MODE | GAP_ADTYPE_FLAGS_BREDR_NOT_SUPPORTED,

  // service UUID, to notify central devices what services are included
  // in this peripheral
  0x03,   // length of this data
  GAP_ADTYPE_16BIT_MORE,      // some of the UUID's, but not all
  LO_UINT16( SIMPLEPROFILE_SERV_UUID ),
  HI_UINT16( SIMPLEPROFILE_SERV_UUID ),

};

// GAP GATT Attributes
static uint8 attDeviceName[GAP_DEVICE_NAME_LEN] = "Neo's BLE Node";

/*********************************************************************
 * LOCAL FUNCTIONS
 */
static void simpleBLEPeripheral_ProcessOSALMsg( osal_event_hdr_t *pMsg );
static void peripheralStateNotificationCB( gaprole_States_t newState );
static void performPeriodicTask( void );
static void simpleProfileChangeCB( uint8 paramID );
static void EcoExecProfileChangeCB( uint8 paramID );
static void accelEnablerChangeCB( void );
static void accelRead( void );
static void timeserviceChangeCB( uint8 paramID );
static void timeRead( void );

#if defined( CC2540_MINIDK )
static void simpleBLEPeripheral_HandleKeys( uint8 shift, uint8 keys );
#endif

#if (defined HAL_LCD) && (HAL_LCD == TRUE)
static char *bdAddr2Str ( uint8 *pAddr );
#endif // (defined HAL_LCD) && (HAL_LCD == TRUE)



/*********************************************************************
 * PROFILE CALLBACKS
 */

// GAP Role Callbacks
static gapRolesCBs_t simpleBLEPeripheral_PeripheralCBs =
{
  peripheralStateNotificationCB,  // Profile State Change Callbacks
  NULL                            // When a valid RSSI is read from controller (not used by application)
};

// GAP Bond Manager Callbacks
static gapBondCBs_t simpleBLEPeripheral_BondMgrCBs =
{
  NULL,                     // Passcode callback (not used by application)
  NULL                      // Pairing / Bonding state Callback (not used by application)
};

// Simple GATT Profile Callbacks
static simpleProfileCBs_t simpleBLEPeripheral_SimpleProfileCBs =
{
  simpleProfileChangeCB    // Charactersitic value change callback
};

// EcoExec GATT Profile Callbacks
static EcoExecProfileCBs_t EcoExecProfileCBs =
{
  EcoExecProfileChangeCB    // Charactersitic value change callback
};

// Accelerometer Profile Callbacks
static accelCBs_t accelerometerProfileCBs =
{
  accelEnablerChangeCB     // Called when Enabler attribute changes
};

// RTC Profile Callbacks
static timeserviceCBs_t timeserviceProfileCBs = 
{
  timeserviceChangeCB       //  Called when Enabler attirbute chanes
};

/*********************************************************************
 * PUBLIC FUNCTIONS
 */

/*********************************************************************
 * @fn      SimpleBLEPeripheral_Init
 *
 * @brief   Initialization function for the Simple BLE Peripheral App Task.
 *          This is called during initialization and should contain
 *          any application specific initialization (ie. hardware
 *          initialization/setup, table initialization, power up
 *          notificaiton ... ).
 *
 * @param   task_id - the ID assigned by OSAL.  This ID should be
 *                    used to send messages and set timers.
 *
 * @return  none
 */
void SimpleBLEPeripheral_Init( uint8 task_id )
{
  simpleBLEPeripheral_TaskID = task_id;
  
  //static uint8 bdAddress[6] = {0x12,0x34,0x56,0x78,0x90,0xAA};
  //HCI_EXT_SetBDADDRCmd(bdAddress);
  
  // Setup the GAP Peripheral Role Profile
  {

    #if defined( CC2540_MINIDK )
      // For the CC2540DK-MINI keyfob, device doesn't start advertising until button is pressed
      uint8 initial_advertising_enable = FALSE;
    #else
      // For other hardware platforms, device starts advertising upon initialization
      uint8 initial_advertising_enable = TRUE;
    #endif

    // By setting this to zero, the device will go into the waiting state after
    // being discoverable for 30.72 second, and will not being advertising again
    // until the enabler is set back to TRUE
    uint16 gapRole_AdvertOffTime = 0;

    uint8 enable_update_request = DEFAULT_ENABLE_UPDATE_REQUEST;
    uint16 desired_min_interval = DEFAULT_DESIRED_MIN_CONN_INTERVAL;
    uint16 desired_max_interval = DEFAULT_DESIRED_MAX_CONN_INTERVAL;
    uint16 desired_slave_latency = DEFAULT_DESIRED_SLAVE_LATENCY;
    uint16 desired_conn_timeout = DEFAULT_DESIRED_CONN_TIMEOUT;

    // Set the GAP Role Parameters
    GAPRole_SetParameter( GAPROLE_ADVERT_ENABLED, sizeof( uint8 ), &initial_advertising_enable );
    GAPRole_SetParameter( GAPROLE_ADVERT_OFF_TIME, sizeof( uint16 ), &gapRole_AdvertOffTime );

    GAPRole_SetParameter( GAPROLE_SCAN_RSP_DATA, sizeof ( scanRspData ), scanRspData );
    GAPRole_SetParameter( GAPROLE_ADVERT_DATA, sizeof( advertData ), advertData );

    GAPRole_SetParameter( GAPROLE_PARAM_UPDATE_ENABLE, sizeof( uint8 ), &enable_update_request );
    GAPRole_SetParameter( GAPROLE_MIN_CONN_INTERVAL, sizeof( uint16 ), &desired_min_interval );
    GAPRole_SetParameter( GAPROLE_MAX_CONN_INTERVAL, sizeof( uint16 ), &desired_max_interval );
    GAPRole_SetParameter( GAPROLE_SLAVE_LATENCY, sizeof( uint16 ), &desired_slave_latency );
    GAPRole_SetParameter( GAPROLE_TIMEOUT_MULTIPLIER, sizeof( uint16 ), &desired_conn_timeout );
  }

  // Set the GAP Characteristics
  GGS_SetParameter( GGS_DEVICE_NAME_ATT, GAP_DEVICE_NAME_LEN, attDeviceName );

  // Set advertising interval
  {
    uint16 advInt = DEFAULT_ADVERTISING_INTERVAL;

    GAP_SetParamValue( TGAP_LIM_DISC_ADV_INT_MIN, advInt );
    GAP_SetParamValue( TGAP_LIM_DISC_ADV_INT_MAX, advInt );
    GAP_SetParamValue( TGAP_GEN_DISC_ADV_INT_MIN, advInt );
    GAP_SetParamValue( TGAP_GEN_DISC_ADV_INT_MAX, advInt );
  }

  // Setup the GAP Bond Manager
  {
    uint32 passkey = 0; // passkey "000000"
    uint8 pairMode = GAPBOND_PAIRING_MODE_WAIT_FOR_REQ;
    uint8 mitm = TRUE;
    uint8 ioCap = GAPBOND_IO_CAP_DISPLAY_ONLY;
    uint8 bonding = TRUE;
    GAPBondMgr_SetParameter( GAPBOND_DEFAULT_PASSCODE, sizeof ( uint32 ), &passkey );
    GAPBondMgr_SetParameter( GAPBOND_PAIRING_MODE, sizeof ( uint8 ), &pairMode );
    GAPBondMgr_SetParameter( GAPBOND_MITM_PROTECTION, sizeof ( uint8 ), &mitm );
    GAPBondMgr_SetParameter( GAPBOND_IO_CAPABILITIES, sizeof ( uint8 ), &ioCap );
    GAPBondMgr_SetParameter( GAPBOND_BONDING_ENABLED, sizeof ( uint8 ), &bonding );
  }

  // Initialize GATT attributes
  GGS_AddService( GATT_ALL_SERVICES );            // GAP
  GATTServApp_AddService( GATT_ALL_SERVICES );    // GATT attributes
  DevInfo_AddService();                           // Device Information Service
  SimpleProfile_AddService( GATT_ALL_SERVICES );  // Simple GATT Profile
  
//  Accel_AddService( GATT_ALL_SERVICES );          // Accel GATT Profile
//  EcoExecProfile_AddService( GATT_ALL_SERVICES ); // EcoExec GATT Profile
//  timeservice_AddService( GATT_ALL_SERVICES );   // Time GATT Profile
  
#if defined FEATURE_OAD
  VOID OADTarget_AddService();                    // OAD Profile
#endif

#if defined( CC2540_MINIDK )

  SK_AddService( GATT_ALL_SERVICES ); // Simple Keys Profile

  // Register for all key events - This app will handle all key events
  RegisterForKeys( simpleBLEPeripheral_TaskID );

  // makes sure LEDs are off
  HalLedSet( (HAL_LED_1 | HAL_LED_2), HAL_LED_MODE_OFF );

#endif // #if defined( CC2540_MINIDK )

#if (defined HAL_LCD) && (HAL_LCD == TRUE)

#if defined FEATURE_OAD
  #if defined (HAL_IMAGE_A)
    HalLcdWriteStringValue( "BLE Peri-A", OAD_VER_NUM( _imgHdr.ver ), 16, HAL_LCD_LINE_1 );
  #else
    HalLcdWriteStringValue( "BLE Peri-B", OAD_VER_NUM( _imgHdr.ver ), 16, HAL_LCD_LINE_1 );
  #endif // HAL_IMAGE_A
#else
  HalLcdWriteString( "BLE Peripheral", HAL_LCD_LINE_1 );
#endif // FEATURE_OAD

#endif // (defined HAL_LCD) && (HAL_LCD == TRUE)

  // Register callback with SimpleGATTprofile
  VOID SimpleProfile_RegisterAppCBs( &simpleBLEPeripheral_SimpleProfileCBs );
  
  // Register callback with EcoExecGATTprofile
//  VOID EcoExecProfile_RegisterAppCBs( &EcoExecProfileCBs );
  
  // Register callback with accelerometerprofile
//  VOID Accel_RegisterAppCBs( &accelerometerProfileCBs );
  
  // Register callback withe timeservice profile
//  VOID timeservice_RegisterAppCBs( &timeserviceProfileCBs );
  
  // Enable clock divide on halt
  // This reduces active current while radio is active and CC254x MCU
  // is halted
  HCI_EXT_ClkDivOnHaltCmd( HCI_EXT_ENABLE_CLK_DIVIDE_ON_HALT );

#if defined ( DC_DC_P0_7 )

  // Enable stack to toggle bypass control on TPS62730 (DC/DC converter)
  HCI_EXT_MapPmIoPortCmd( HCI_EXT_PM_IO_PORT_P0, HCI_EXT_PM_IO_PORT_PIN7 );

#endif // defined ( DC_DC_P0_7 )

  // Setup a delayed profile startup
  osal_set_event( simpleBLEPeripheral_TaskID, SBP_START_DEVICE_EVT );
}

/*********************************************************************
 * @fn      SimpleBLEPeripheral_ProcessEvent
 *
 * @brief   Simple BLE Peripheral Application Task event processor.  This function
 *          is called to process all events for the task.  Events
 *          include timers, messages and any other user defined events.
 *
 * @param   task_id  - The OSAL assigned task ID.
 * @param   events - events to process.  This is a bit map and can
 *                   contain more than one event.
 *
 * @return  events not processed
 */
uint16 SimpleBLEPeripheral_ProcessEvent( uint8 task_id, uint16 events )
{

  VOID task_id; // OSAL required parameter that isn't used in this function

  if ( events & SYS_EVENT_MSG )
  {
    uint8 *pMsg;

    if ( (pMsg = osal_msg_receive( simpleBLEPeripheral_TaskID )) != NULL )
    {
      simpleBLEPeripheral_ProcessOSALMsg( (osal_event_hdr_t *)pMsg );

      // Release the OSAL message
      VOID osal_msg_deallocate( pMsg );
    }

    // return unprocessed events
    return (events ^ SYS_EVENT_MSG);
  }

  if ( events & SBP_START_DEVICE_EVT )
  {
    // Start the Device
    VOID GAPRole_StartDevice( &simpleBLEPeripheral_PeripheralCBs );

    // Start Bond Manager
    VOID GAPBondMgr_Register( &simpleBLEPeripheral_BondMgrCBs );
#ifdef ECOEXEC_DEBUG
    uartInit(HAL_UART_BR_57600);
#endif
    rtcInit();
    // Set timer for first periodic event
    osal_start_timerEx( simpleBLEPeripheral_TaskID, SBP_PERIODIC_EVT, SBP_PERIODIC_EVT_PERIOD );
    
//    uint8 memAddress[2] = {HI_UINT16(((uint16)Message)+21), LO_UINT16(((uint16)Message)+21)};
//    EcoExecProfile_SetParameter( ECOEXECPROFILE_CHAR3, ECOEXECPROFILE_CHAR3_LEN, &memAddress );

    return ( events ^ SBP_START_DEVICE_EVT );
  }

  if( events & WIRELESS_EVT )
  { 
    P0SEL &= ~0x30;    /* Configure Port 0.4 0.5 as GPIO */
    P0DIR |= 0x30;   /* set direction to 1 as output */
   
    MEMCTR |= 0x08;
    __asm("LCALL Message"); /* 8000 + 0479 */
    MEMCTR &= ~0x08;
    
//    /**
//    * Handle Value Notification format.
//    */
//    typedef struct
//    {
//      uint16 handle;               //!< Handle of the attribute that has been changed (must be first field)
//      uint8 len;                   //!< Length of value
//      uint8 value[ATT_MTU_SIZE-3]; //!< New value of the attribute
//    } attHandleValueNoti_t;
    
    notify.handle = 0x0039;
    notify.len    = 20;
    ATT_HandleValueNoti( EcoExecProfileConnHandle , &notify );
    
    return ( events ^ WIRELESS_EVT );
  }
  
  if ( events & ACCEL_READ_EVT )
  {
//    bStatus_t status = Accel_GetParameter( ACCEL_ENABLER, &accelEnabler );
//    
//    if (status == SUCCESS)
//    {
//      if (accelEnabler)
//      {
//        // Restart timer
//        if (ACCEL_READ_PERIOD)
//          osal_start_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT, ACCEL_READ_PERIOD );
//        
//        // Read accelerometer data
//        accelRead();
//      }
//      else
//      {
//        // Stop the acceleromter
//        osal_stop_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT);
//      }
//    }
//    else
//    {
//      //??
//    }
    return (events ^ ACCEL_READ_EVT);
  }
  
  if ( events & TIME_READ_EVT )
  {
//    bStatus_t status = timeservice_GetParameter( TIME_ENABLER, &timeEnabler );
//    
//    if (status == SUCCESS)
//    {
//      if (timeEnabler)
//      {
//        // Restart timer
//        if (TIME_READ_PERIOD)
//          osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
//        
//        // Read accelerometer data
//        timeRead();
//      }
//      else
//      {
//        // Stop the acceleromter
//        osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
//      }
//    }
//    else
//    {
//      //??
//    }
    return (events ^ TIME_READ_EVT);
  }
  
  if ( events & SBP_PERIODIC_EVT )
  {
    
    // Restart timer
    if ( SBP_PERIODIC_EVT_PERIOD )
    {
      osal_start_timerEx( simpleBLEPeripheral_TaskID, SBP_PERIODIC_EVT, SBP_PERIODIC_EVT_PERIOD );
    }

    // Perform periodic application task
    performPeriodicTask();

    return (events ^ SBP_PERIODIC_EVT);
  }

#if defined ( PLUS_BROADCASTER )
  if ( events & SBP_ADV_IN_CONNECTION_EVT )
  {
    uint8 turnOnAdv = TRUE;
    // Turn on advertising while in a connection
    GAPRole_SetParameter( GAPROLE_ADVERT_ENABLED, sizeof( uint8 ), &turnOnAdv );

    return (events ^ SBP_ADV_IN_CONNECTION_EVT);
  }
#endif // PLUS_BROADCASTER
  
  

  // Discard unknown events
  return 0;
}

/*********************************************************************
 * @fn      simpleBLEPeripheral_ProcessOSALMsg
 *
 * @brief   Process an incoming task message.
 *
 * @param   pMsg - message to process
 *
 * @return  none
 */
static void simpleBLEPeripheral_ProcessOSALMsg( osal_event_hdr_t *pMsg )
{
  switch ( pMsg->event )
  {
  #if defined( CC2540_MINIDK )
    case KEY_CHANGE:
      simpleBLEPeripheral_HandleKeys( ((keyChange_t *)pMsg)->state, ((keyChange_t *)pMsg)->keys );
      break;
  #endif // #if defined( CC2540_MINIDK )

  default:
    // do nothing
    break;
  }
}

#if defined( CC2540_MINIDK )
/*********************************************************************
 * @fn      simpleBLEPeripheral_HandleKeys
 *
 * @brief   Handles all key events for this device.
 *
 * @param   shift - true if in shift/alt.
 * @param   keys - bit field for key events. Valid entries:
 *                 HAL_KEY_SW_2
 *                 HAL_KEY_SW_1
 *
 * @return  none
 */
static void simpleBLEPeripheral_HandleKeys( uint8 shift, uint8 keys )
{
  uint8 SK_Keys = 0;

  VOID shift;  // Intentionally unreferenced parameter

  if ( keys & HAL_KEY_SW_1 )
  {
    SK_Keys |= SK_KEY_LEFT;
  }

  if ( keys & HAL_KEY_SW_2 )
  {

    SK_Keys |= SK_KEY_RIGHT;

    // if device is not in a connection, pressing the right key should toggle
    // advertising on and off
    if( gapProfileState != GAPROLE_CONNECTED )
    {
      uint8 current_adv_enabled_status;
      uint8 new_adv_enabled_status;

      //Find the current GAP advertisement status
      GAPRole_GetParameter( GAPROLE_ADVERT_ENABLED, &current_adv_enabled_status );

      if( current_adv_enabled_status == FALSE )
      {
        new_adv_enabled_status = TRUE;
      }
      else
      {
        new_adv_enabled_status = FALSE;
      }

      //change the GAP advertisement status to opposite of current status
      GAPRole_SetParameter( GAPROLE_ADVERT_ENABLED, sizeof( uint8 ), &new_adv_enabled_status );
    }

  }

  // Set the value of the keys state to the Simple Keys Profile;
  // This will send out a notification of the keys state if enabled
  SK_SetParameter( SK_KEY_ATTR, sizeof ( uint8 ), &SK_Keys );
}
#endif // #if defined( CC2540_MINIDK )

/*********************************************************************
 * @fn      peripheralStateNotificationCB
 *
 * @brief   Notification from the profile of a state change.
 *
 * @param   newState - new state
 *
 * @return  none
 */
static void peripheralStateNotificationCB( gaprole_States_t newState )
{
  switch ( newState )
  {
    case GAPROLE_STARTED:
      {
        uint8 ownAddress[B_ADDR_LEN];
        uint8 systemId[DEVINFO_SYSTEM_ID_LEN];

        GAPRole_GetParameter(GAPROLE_BD_ADDR, ownAddress);

        // use 6 bytes of device address for 8 bytes of system ID value
        systemId[0] = ownAddress[0];
        systemId[1] = ownAddress[1];
        systemId[2] = ownAddress[2];

        // set middle bytes to zero
        systemId[4] = 0x00;
        systemId[3] = 0x00;

        // shift three bytes up
        systemId[7] = ownAddress[5];
        systemId[6] = ownAddress[4];
        systemId[5] = ownAddress[3];

        DevInfo_SetParameter(DEVINFO_SYSTEM_ID, DEVINFO_SYSTEM_ID_LEN, systemId);

        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          // Display device address
          HalLcdWriteString( bdAddr2Str( ownAddress ),  HAL_LCD_LINE_2 );
          HalLcdWriteString( "Initialized",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
      }
      break;

    case GAPROLE_ADVERTISING:
      {
        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          HalLcdWriteString( "Advertising",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
      }
      break;

    case GAPROLE_CONNECTED:
      {
        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          HalLcdWriteString( "Connected",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
          
      }
      break;

    case GAPROLE_WAITING:
      {
        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          HalLcdWriteString( "Disconnected",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
      }
      break;

    case GAPROLE_WAITING_AFTER_TIMEOUT:
      {
        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          HalLcdWriteString( "Timed Out",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
      }
      break;

    case GAPROLE_ERROR:
      {
        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          HalLcdWriteString( "Error",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
      }
      break;

    default:
      {
        #if (defined HAL_LCD) && (HAL_LCD == TRUE)
          HalLcdWriteString( "",  HAL_LCD_LINE_3 );
        #endif // (defined HAL_LCD) && (HAL_LCD == TRUE)
      }
      break;

  }

  gapProfileState = newState;

#if !defined( CC2540_MINIDK )
  VOID gapProfileState;     // added to prevent compiler warning with
                            // "CC2540 Slave" configurations
#endif


}

/*********************************************************************
 * @fn      performPeriodicTask
 *
 * @brief   Perform a periodic application task. This function gets
 *          called every five seconds as a result of the SBP_PERIODIC_EVT
 *          OSAL event. In this example, the value of the third
 *          characteristic in the SimpleGATTProfile service is retrieved
 *          from the profile, and then copied into the value of the
 *          the fourth characteristic.
 *
 * @param   none
 *
 * @return  none
 */
static void performPeriodicTask( void )
{
  uint8 valueToCopy;
  uint8 stat;

  // Call to retrieve the value of the third characteristic in the profile
  stat = SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR3, &valueToCopy);

  if( stat == SUCCESS )
  {
    /*
     * Call to set that value of the fourth characteristic in the profile. Note
     * that if notifications of the fourth characteristic have been enabled by
     * a GATT client device, then a notification will be sent every time this
     * function is called.
     */
    SimpleProfile_SetParameter( SIMPLEPROFILE_CHAR4, sizeof(uint8), &valueToCopy);
  }
}

/*********************************************************************
 * @fn      simpleProfileChangeCB
 *
 * @brief   Callback from SimpleBLEProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
static void simpleProfileChangeCB( uint8 paramID )
{
  uint8 newValue;

  switch( paramID )
  {
    case SIMPLEPROFILE_CHAR1:
      SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR1, &newValue );
      //osal_start_timerEx( simpleBLEPeripheral_TaskID, WIRELESS_EVT, 1000);
   
      break;

    case SIMPLEPROFILE_CHAR3:
      SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR3, &newValue );


      break;

    default:
      // should not reach here!
      break;
  }
}

/*********************************************************************
 * @fn      EcoExecProfileChangeCB
 *
 * @brief   Callback from EcoExecProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
//static void EcoExecProfileChangeCB( uint8 paramID )
//{
//  static int cnt;
//  switch( paramID ){
//  case ECOEXECPROFILE_CHAR1:
//    /* reload the packet counter to zero */
//    cnt = 0;
//    
//    EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR1, &HeaderPacket[0] );      /* 2 1 1 */
//
//#ifdef ECOEXEC_DEBUG
//    for(i=0; i < ECOEXECPROFILE_CHAR1_LEN; i++){
//      uartWriteHex( &HeaderPacket[i] );
//    }
//    uartWriteString("\r\n");
//#endif   
//    break;
//    
//  case ECOEXECPROFILE_CHAR2:
//    /* Write code to xdata-SRAM */
//    EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR2, &Message[cnt*19+23] );      /* Get code data  */
//    
//#ifdef ECOEXEC_DEBUG
//    for(i=0; i < ECOEXECPROFILE_CHAR2_LEN; i++){
//      uartWriteHex( &Message[cnt*19+23] );
//    }
//    uartWriteString("\r\n");
//#endif
//
//    cnt++;
//    if( HeaderPacket[3]<19 )
//    {
//        osal_start_timerEx( simpleBLEPeripheral_TaskID, WIRELESS_EVT, 300);
//    }
//    else 
//    { 
//      if( (cnt*19) >= HeaderPacket[3] )
//        osal_start_timerEx( simpleBLEPeripheral_TaskID, WIRELESS_EVT, 300);
//    }
//      
//    break;
//  default:
//    // should not reach here!
//    break;
//  }  /* end switch case */
//}

#if (defined HAL_LCD) && (HAL_LCD == TRUE)
/*********************************************************************
 * @fn      bdAddr2Str
 *
 * @brief   Convert Bluetooth address to string. Only needed when
 *          LCD display is used.
 *
 * @return  none
 */
char *bdAddr2Str( uint8 *pAddr )
{
  uint8       i;
  char        hex[] = "0123456789ABCDEF";
  static char str[B_ADDR_STR_LEN];
  char        *pStr = str;

  *pStr++ = '0';
  *pStr++ = 'x';

  // Start from end of addr
  pAddr += B_ADDR_LEN;

  for ( i = B_ADDR_LEN; i > 0; i-- )
  {
    *pStr++ = hex[*--pAddr >> 4];
    *pStr++ = hex[*pAddr & 0x0F];
  }

  *pStr = 0;

  return str;
}
#endif // (defined HAL_LCD) && (HAL_LCD == TRUE)

/*********************************************************************
*********************************************************************/

/*********************************************************************
 * @fn      accelEnablerChangeCB
 *
 * @brief   Called by the Accelerometer Profile when the Enabler Attribute
 *          is changed.
 *
 * @param   none
 *
 * @return  none
 */
//static void accelEnablerChangeCB( void )
//{
//  bStatus_t status = Accel_GetParameter( ACCEL_ENABLER, &accelEnabler );
//
//  if (status == SUCCESS){
//    if (accelEnabler){
//      
//      spiInit(SPI_MASTER);
//      // Initialize accelerometer
//      accInit();
//
//      // Setup timer for accelerometer task
//      osal_start_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT, ACCEL_READ_PERIOD );
//    } else {
//      // Stop the acceleromter
//      osal_stop_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT);
//    }
//  } else {
//      //??
//  }
//}

/*********************************************************************
 * @fn      accelRead
 *
 * @brief   Called by the application to read accelerometer data
 *          and put data in accelerometer profile
 *
 * @param   none
 *
 * @return  none
 */
//static void accelRead( void )
//{
//
//  static int16 x, y, z;
//  int16 new_x, new_y, new_z;
//
//  // Read data for each axis of the accelerometer
//  accReadAcc(&new_x, &new_y, &new_z);
//
//  // Check if x-axis value has changed by more than the threshold value and
//  // set profile parameter if it has (this will send a notification if enabled)
//  if( (x < (new_x-ACCEL_CHANGE_THRESHOLD)) || (x > (new_x+ACCEL_CHANGE_THRESHOLD)) )
//  {
//    x = new_x;
//    //Accel_SetParameter(ACCEL_X_ATTR, sizeof ( uint16 ), &x);
//    Accel_SetParameter(ACCEL_X_ATTR, sizeof ( int8 ), &x);
//  }
//  
//  // Check if y-axis value has changed by more than the threshold value and
//  // set profile parameter if it has (this will send a notification if enabled)
//  if( (y < (new_y-ACCEL_CHANGE_THRESHOLD)) || (y > (new_y+ACCEL_CHANGE_THRESHOLD)) )
//  {
//    y = new_y;
//    //Accel_SetParameter(ACCEL_Y_ATTR, sizeof ( uint16 ), &y);
//    Accel_SetParameter(ACCEL_Y_ATTR, sizeof ( int8 ), &y);
//  }
//  
//  // Check if z-axis value has changed by more than the threshold value and
//  // set profile parameter if it has (this will send a notification if enabled)
//  if( (z < (new_z-ACCEL_CHANGE_THRESHOLD)) || (z > (new_z+ACCEL_CHANGE_THRESHOLD)) )
//  {
//    z = new_z;  
//    //Accel_SetParameter(ACCEL_Z_ATTR, sizeof ( uint16 ), &z);
//    Accel_SetParameter(ACCEL_Z_ATTR, sizeof ( int8 ), &z);
//  }
//  
//}

/*********************************************************************
 * @fn      timeserviceChangeCB
 *
 * @brief   Callback from timeserviceProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
//static void timeserviceChangeCB( uint8 paramID )
//{
//  bStatus_t status;
//  static uint8 hour, minute, second, year, month
//    , date, day, century, alarmMonth, alarmDate
//      , alarmHour, alarmMinute, alarmSecond, alarmRepeatmode;
//  switch( paramID ){
//  case TIME_ENABLER:
//    status = timeservice_GetParameter( TIME_ENABLER, &timeEnabler );
//    if (status == SUCCESS){
//      if (timeEnabler){
//        // Initialize RTC
//        rtcInit();
//        // Setup timer for accelerometer task
//        osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
//      } else {
//        // Stop the acceleromter
//        osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
//      }
//    } else {
//      //??
//    }
//    break;
//  case HOUR:
//  case MINUTE:
//  case SECOND:
//    timeservice_GetParameter( HOUR, &hour );
//    timeservice_GetParameter( MINUTE, &minute );
//    timeservice_GetParameter( SECOND, &second );
//    rtcSetTime(hour, minute, second );
//    break;
//  case YEAR:
//  case MONTH:
//  case DATE:
//  case DAY:
//  case CENTURY:
//    timeservice_GetParameter( DAY, &day);
//    timeservice_GetParameter( DATE, &date );
//    timeservice_GetParameter( YEAR, &year );
//    timeservice_GetParameter( MONTH, &month );
//    //timeservice_GetParameter( CENTURY, &century );
//    //rtcSetDate(day, date, month, year, century );
//    rtcSetDate(day, date, month, year);
//    break;
//  case ALARM_MONTH:
//  case ALARM_DATE:
//  case ALARM_HOUR:
//  case ALARM_MINUTE:
//  case ALARM_SECOND:
//  case ALARM_REPEATMODE:
//    timeservice_GetParameter( ALARM_MONTH, &alarmMonth);
//    timeservice_GetParameter( ALARM_DATE, &alarmDate );
//    timeservice_GetParameter( ALARM_HOUR, &alarmHour );
//    timeservice_GetParameter( ALARM_MINUTE, &alarmMinute );
//    timeservice_GetParameter( ALARM_SECOND, &alarmSecond );
//    timeservice_GetParameter( ALARM_REPEATMODE, &alarmRepeatmode );
//    rtcSetAlarm( alarmMonth, alarmDate, alarmHour
//                , alarmMinute, alarmSecond, alarmRepeatmode );
//    break;
//  }
//}

/*********************************************************************
 * @fn      timeRead
 *
 * @brief   Called by the application to read time data
 *          and put data in timeservice profile
 *
 * @param   none
 *
 * @return  none
 */
//static void timeRead( void )
//{
//
//  static unsigned char hour, minute, second;
//  notify.handle = 0xFF00;
//  notify.len = 3 * sizeof( unsigned char );
//  
//  // Read time data of the time service
//  rtcGetTime( &hour, &minute, &second );
//  
//  timeservice_SetParameter(HOUR,   sizeof ( unsigned char ), &hour);
//  timeservice_SetParameter(MINUTE, sizeof ( unsigned char ), &minute);
//  timeservice_SetParameter(SECOND, sizeof ( unsigned char ), &second);
//  
//  notify.value[0] = hour;
//  notify.value[1] = minute;
//  notify.value[2] = second;
//  
//  ATT_HandleValueNoti( GAPROLE_CONNHANDLE, &notify );
//}