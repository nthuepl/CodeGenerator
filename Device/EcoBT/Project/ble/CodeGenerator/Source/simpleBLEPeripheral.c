/**************************************************************************************************
  Filename:       simpleBLEPeripheral.c
  Revised:        $Date: 2010-08-06 08:56:11 -0700 (Fri, 06 Aug 2010) $
  Revision:       $Revision: 23333 $

  Description:    This file contains the Simple BLE Peripheral sample application
                  for use with the CC2540 Bluetooth Low Energy Protocol Stack.

  Copyright 2010 - 2012 Texas Instruments Incorporated. All rights reserved.

  IMPORTANT: Your use of this Software is limited to those specific rights
  granted under the terms of a software license agreement between the user
  who downloaded the software, his/her employer (which must be your employer)
  and Texas Instruments Incorporated (the "License").  You may not use this
  Software unless you agree to abide by the terms of the License. The License
  limits your use, and you acknowledge, that the Software may not be modified,
  copied or distributed unless embedded on a Texas Instruments microcontroller
  or used solely and exclusively in conjunction with a Texas Instruments radio
  frequency transceiver, which is integrated into your product.  Other than for
  the foregoing purpose, you may not use, reproduce, copy, prepare derivative
  works of, modify, distribute, perform, display or sell this Software and/or
  its documentation for any purpose.

  YOU FURTHER ACKNOWLEDGE AND AGREE THAT THE SOFTWARE AND DOCUMENTATION ARE
  PROVIDED “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED,
  INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, TITLE,
  NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL
  TEXAS INSTRUMENTS OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER CONTRACT,
  NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR OTHER
  LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
  INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE
  OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT
  OF SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
  (INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.

  Should you have any questions regarding your right to use this Software,
  contact Texas Instruments Incorporated at www.TI.com.
**************************************************************************************************/

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

#if (defined CC2541)|| (defined CC2541S)
#include "epl_rtc_m41t62.h"
#include "timeservice.h"
#endif

#include "epl_hal_uart.h"
#include "accelerometer.h"

/* code generator's Profile */
#include "EcoExecGATTprofile.h"

/* include for acceleratormeter */
#include "epl_hal_spi.h"
#include "epl_acc_lis331dl.h"
#include "EcoExec.h"

/* is not ready on lighting board right now */
#include "battservice.h"

/* include for the ROM code reprogramming */
#include "hal_flash.h"

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

// Accelerometer Profile Parameters
static uint8 accelEnabler = FALSE;

#ifdef CC2541
// How often (in ms) to read the time
#define TIME_READ_PERIOD              1000

// Time service Profile Parameters
static uint8 timeEnabler = FALSE;

unsigned char newTime[TIME_LEN]={0};
unsigned char newDate[DATE_LEN]={0};
unsigned char newAlarm[ALARM_LEN]={0};
#endif

#define CODEGENERATOR_FIRSTPAGE 0x30000/HAL_FLASH_PAGE_SIZE
#define CODEGENERATOR_WRITING_FLASH_SIZE ECOEXECPROFILE_CHAR2_LEN/HAL_FLASH_WORD_SIZE

/*********************************************************************
 * TYPEDEFS
 */

/*********************************************************************
 * GLOBAL VARIABLES
 */

/* CBL RAM or Flash code flag */
static unsigned char isFlashCode = FALSE;

/* CBL code section, to record the incoming code data is a callback or main function */
static unsigned char codeSection = 0x00;

/* CBL code buffer for Interactive Execution */
unsigned char Message[500];

/* CBL a header packet contains the sequence, segment, code data length */
unsigned char HeaderPacket[4];

/* CBL EcoExec connection handle */
extern uint16 EcoExecProfileConnHandle;

/* CBL current flash page */
unsigned char pg;

/* CBL current flash offset */
uint16 offset = 0x0000;

/* CBL current flash boundary to decide if the next flash page needs to be earsed */
uint16 pgoffset_boundary = 0x0000;

/* CBL current flash address of the code data to be written to the flash */
uint16 addr;
unsigned char i;

/* CBL notify package */
attHandleValueNoti_t notify;

/* CBL external ram for CBL */
unsigned char xDataSeg[256];


/* debug flag */
//#define FLASH_DEBUG
//#define ECOEXEC_DEBUG

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
  'E',   // 'E'
  'P',   // 'P'
  'L',   // 'L'
  '\'',   // '''
  's',   // 's'
  ' ',   // ' '
  'n',   // 'n'
  'o',   // 'o'
  'd',   // 'd'
  'e',   // 'e'

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
  5,
  0xFF,
  '0',
  'e',
  'p',
  'l',
};

// GAP GATT Attributes
static uint8 attDeviceName[GAP_DEVICE_NAME_LEN] = "EPL's BLE Node";

/*********************************************************************
 * LOCAL FUNCTIONS
 */
static void simpleBLEPeripheral_ProcessOSALMsg( osal_event_hdr_t *pMsg );
static void peripheralStateNotificationCB( gaprole_States_t newState );
static void performPeriodicTask( void );

/* CBL Main function entrance point */
void CodeGeneratorStartPoint( void );

/* CBL callback function jumptable */
void CodeGenerator_EVT_1_CB(void);
void CodeGenerator_EVT_2_CB(void);
void CodeGenerator_EVT_3_CB(void);
void CodeGenerator_EVT_4_CB(void);
static void simpleProfileChangeCB( uint8 paramID );
static void EcoExecProfileChangeCB( uint8 paramID );
static void accelEnablerChangeCB( void );
static void accelRead( void );
#ifdef CC2541
void timeserviceChangeCB( uint8 paramID );
void timeRead( void );
#endif

/* CBL profile charactristic change callback*/
void cg_accelProfileChangeCB( void );
void cg_simpleProfileChangeCB( uint8 paramID );
void cg_battProfileChangeCB( uint8 event );

/* CBL callback function */
void cg_EVT_1_CB(void);
void cg_EVT_2_CB(void);
void cg_EVT_3_CB(void);
void cg_EVT_4_CB(void);

/* CBL Interactive Execution entrance point */
__near_func void execution_ram_code( void );

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

#ifdef CC2541
// RTC Profile Callbacks
static timeserviceCBs_t timeserviceProfileCBs = 
{
  timeserviceChangeCB       //  Called when Enabler attirbute chanes
};
#endif


// Batt Profile Callbacks
void battProfileChangeCB(uint8 event);

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

  /* revser the xdata segment for sdcc code xram space */
  if( xDataSeg[0] == 0x00 )
    xDataSeg[3] = 1;
  
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
  
  Accel_AddService( GATT_ALL_SERVICES );          // Accel GATT Profile
  EcoExecProfile_AddService( GATT_ALL_SERVICES ); // EcoExec GATT Profile
#ifdef CC2541
  timeservice_AddService( GATT_ALL_SERVICES );    // Time GATT Profile
#endif
  
  Batt_AddService( );                             // Battery GATT Profile
  
#if defined FEATURE_OAD
  VOID OADTarget_AddService();                    // OAD Profile
#endif

  // Register callback with SimpleGATTprofile
  VOID SimpleProfile_RegisterAppCBs( &simpleBLEPeripheral_SimpleProfileCBs );
  
  // Register callback with EcoExecGATTprofile
  VOID EcoExecProfile_RegisterAppCBs( &EcoExecProfileCBs );
  
  // Register callback with accelerometerprofile
  VOID Accel_RegisterAppCBs( &accelerometerProfileCBs );
  
#ifdef CC2541
  // Register callback withe timeservice profile
  VOID timeservice_RegisterAppCBs( &timeserviceProfileCBs );
#endif
  
  // Register callback withe timeservice profile
  VOID Batt_Register( battProfileChangeCB );
  

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

    // Set timer for first periodic event
    osal_start_timerEx( simpleBLEPeripheral_TaskID, SBP_PERIODIC_EVT, SBP_PERIODIC_EVT_PERIOD );
    
    /* run EcoExec Main */
    osal_start_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_MAIN_EVT, 100 );
    
#if defined( CC2541 ) || defined( CC2541S )
    P2SEL &= ~0x06;    /* Configure Port 2.1 2.2 as GPIO */
    P2DIR |= 0x06;   /* set direction to 1 s output */
#else
    P0SEL &= ~0x30;    /* Configure Port 0.4 0.5 as GPIO */
    P0DIR |= 0x30;   /* set direction to 1 s output */
#endif
    
/*****************************************************************************/ 
    uartInit(HAL_UART_BR_57600);
    
    /* init CG notify packet */
    notify.handle = 0x004C;
    notify.len    = 20;
/*****************************************************************************/ 
    return ( events ^ SBP_START_DEVICE_EVT );
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

  /* RAM Code event */
  if( events & RAM_CODE_EVT )
  { 

    execution_ram_code();
    
    /**
    * Notification
    */
    ATT_HandleValueNoti( EcoExecProfileConnHandle , &notify );
    
    return ( events ^ RAM_CODE_EVT );
  }/* End RAM Code event */
  
  /* Flash Code event */
  if( events & FLASH_CODE_EVT )
  { 
#ifdef FLASH_DEBUG
    unsigned char FlashCode[HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE]={0};
#endif
    addr = (offset >> 2) + ((uint16)pg << 9); /* reference from osal_snv.c ==> writeWord */
    
#ifdef FLASH_DEBUG
    /********************** read flash **********************/
    HalFlashRead( pg, offset, FlashCode, HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE);
    for(i=0; i < HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE; i++){
      uartWriteHex( &FlashCode[i] );
    }
    uartWriteString("\r\n");
#endif
    
    /********************** Erase flash **********************/
    if( offset == 0 ){
        pgoffset_boundary = (HAL_FLASH_PAGE_SIZE-1);
        HalFlashErase( pg );
      //if( BUILD_UINT16(HeaderPacket[3], HeaderPacket[2]) > 103 )
      //   HalFlashErase( pg+1 );
    }else if( (offset+20) > pgoffset_boundary ){
        HalFlashErase( pg+(pgoffset_boundary/(HAL_FLASH_PAGE_SIZE-1)) );
        pgoffset_boundary+=(HAL_FLASH_PAGE_SIZE-1);
    }
    
    /********************** Write flash **********************/
    HalFlashWrite( addr, Message, CODEGENERATOR_WRITING_FLASH_SIZE );
    
#ifdef FLASH_DEBUG
    HalFlashRead( pg, offset, FlashCode, HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE);
    for(i=0; i < HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE; i++){
      uartWriteHex( &Message[i] );
    }
    uartWriteString("\r\n----------------------\r\n");
#endif
    /********************** if the last code data is written to ROM, reset the header and code buffer **********************/
    if( isFlashCode == FALSE ){ 
      if( codeSection == 4)
        osal_set_event( simpleBLEPeripheral_TaskID, CODEGENERATOR_MAIN_EVT );
      else{
        ATT_HandleValueNoti( EcoExecProfileConnHandle , &notify );
      }
    }
#if defined( CC2541 ) || defined( CC2541S )
    P2_1 ^= 1;
#else
    P0_4 ^= 1;
#endif
    return ( events ^ FLASH_CODE_EVT );
  }/* End Flash Code event */
  
  if ( events & ACCEL_READ_EVT )
  {
    bStatus_t status = Accel_GetParameter( ACCEL_ENABLER, &accelEnabler );
    
    if (status == SUCCESS)
    {
      if (accelEnabler)
      {
        // Restart timer
        if (ACCEL_READ_PERIOD)
          osal_start_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT, ACCEL_READ_PERIOD );
        
        // Read accelerometer data
        accelRead();
      }
      else
      {
        // Stop the acceleromter
        osal_stop_timerEx( simpleBLEPeripheral_TaskID, ACCEL_READ_EVT);
      }
    }
    else
    {
      //??
    }
    return (events ^ ACCEL_READ_EVT);
  }
  
#ifdef CC2541  
  if ( events & TIME_READ_EVT )
  {

    bStatus_t status = timeservice_GetParameter( TIME_ENABLER, &timeEnabler );
    
    if (status == SUCCESS)
    {
      if (timeEnabler)
      {
        // Restart timer
        if (TIME_READ_PERIOD)
          osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
        
        // Read accelerometer data
        timeRead();
      }
      else
      {
        // Stop the acceleromter
        osal_stop_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT);
      }
    }
    else
    {
      //??
    }

    return (events ^ TIME_READ_EVT);
  }
#endif  
  
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
  
  #if (defined CC2541)|| (defined CC2541S)
  if( events & SET_TIME_EVT )
  {
    timeservice_GetParameter( TIME, newTime);
    //newsecond, newminute, newhour
    rtcSetTime( newTime[2], newTime[1], newTime[0] );
    osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
    return ( events ^ SET_TIME_EVT );
  }
  
  if( events & SET_DATE_EVT )
  {
    timeservice_GetParameter( DATE, newDate );
    rtcSetDate(newDate[0], newDate[1], newDate[2], newDate[3], newDate[4]);
    osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
    return ( events ^ SET_DATE_EVT );
  }
  
  if( events & SET_ALARM_EVT )
  {
    timeservice_GetParameter( ALARM, &newAlarm);
    rtcSetAlarm( newAlarm[0], newAlarm[1], newAlarm[2], newAlarm[3], newAlarm[4], newAlarm[5] );
    osal_start_timerEx( simpleBLEPeripheral_TaskID, TIME_READ_EVT, TIME_READ_PERIOD );
    return ( events ^ SET_ALARM_EVT );
  }
#endif
  if( events & CODEGENERATOR_MAIN_EVT )
  {
    asm("PUSH 6    \n" \
        "PUSH 7    \n" \
        "PUSH dpl  \n" \
        "PUSH dph  \n" );
    CodeGeneratorStartPoint();	
    asm("POP dph \n" \
        "POP dpl \n" \
        "POP 7   \n" \
        "POP 6     " );
    ATT_HandleValueNoti( EcoExecProfileConnHandle , &notify );
   
    return ( events ^ CODEGENERATOR_MAIN_EVT );
  }
  
  
  if( events & CODEGENERATOR_EVT_1 )
  {
    CodeGenerator_EVT_1_CB();
    return ( events ^ CODEGENERATOR_EVT_1 );
  }
  
  
  if( events & CODEGENERATOR_EVT_2 )
  {
    CodeGenerator_EVT_2_CB();
    return ( events ^ CODEGENERATOR_EVT_2 );
  }
  
  if( events & CODEGENERATOR_EVT_3 )
  {
    CodeGenerator_EVT_3_CB();
    return ( events ^ CODEGENERATOR_EVT_3 );
  }
  
  if( events & CODEGENERATOR_EVT_4 )
  {
    CodeGenerator_EVT_4_CB();
    return ( events ^ CODEGENERATOR_EVT_4 );
  }
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
#if defined( CC2540 )
Batt_MeasLevel();
#endif
}

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
 * @fn      EcoExecProfileChangeCB
 *
 * @brief   Callback from EcoExecProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
static void EcoExecProfileChangeCB( uint8 paramID )
{
  static uint16 cnt;
  switch( paramID ){
  case ECOEXECPROFILE_CHAR1:
    /* reload the packet counter to zero */
    cnt = 0x0000;
    
    EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR1, &HeaderPacket[0] );      /* Sequence: 2 Segment: 2 */

#ifdef ECOEXEC_DEBUG
    for(i=0; i < ECOEXECPROFILE_CHAR1_LEN; i++){
      uartWriteHex( &HeaderPacket[i] );
    }
    uartWriteString("\r\n");
#endif   
    break;
    
  case ECOEXECPROFILE_CHAR2:
    if( HeaderPacket[2] != 0 || HeaderPacket[3] != 0 ){ /* check code data length */
      /* Write code to xdata-SRAM */
      if( isFlashCode == FALSE ){
        EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR2, &Message[cnt*ECOEXECPROFILE_CHAR2_LEN] );     /* Get code data  */
#ifdef ECOEXEC_DEBUG
        for(i=0; i < ECOEXECPROFILE_CHAR2_LEN; i++){
          uartWriteHex( &Message[cnt*ECOEXECPROFILE_CHAR2_LEN+i] );
        }
        uartWriteString("\r\n");
#endif
      }else{
        /* if flash Code == FALSE, only use the element 0 ~ 19 of Message buffer for flash writing */
        EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR2, &Message[0] );          /* Get code data  */
#ifdef ECOEXEC_DEBUG
        for(i=0; i < ECOEXECPROFILE_CHAR2_LEN; i++){
          uartWriteHex( &Message[i] );
        }
        uartWriteString("\r\n");
#endif
      }   
      cnt++;
      
      /* Run Code From RAM */
      if( isFlashCode == FALSE ){    
        if( cnt == BUILD_UINT16(HeaderPacket[3], HeaderPacket[2]) ) /* HeaderPacket[2] : code data segment */
          osal_start_timerEx( simpleBLEPeripheral_TaskID, RAM_CODE_EVT, 100);
      }
      else{  
        /* Update ROM Code */
        if( cnt == 0x0001 )
          offset = 0x0000;
        else
          offset += ECOEXECPROFILE_CHAR2_LEN;
        
        if( cnt == BUILD_UINT16(HeaderPacket[3], HeaderPacket[2]) ){
          isFlashCode = FALSE;
#ifdef ECOEXEC_DEBUG
          uartWriteString( "Finished flash code loading.\n\r" );
#endif
        }
        osal_set_event( simpleBLEPeripheral_TaskID, FLASH_CODE_EVT );
        //osal_start_timerEx( simpleBLEPeripheral_TaskID, FLASH_CODE_EVT, 200);
      }
    }
    break;
    
  /* check this flag to determine the following code data will be place in RAM or ROM */
  case ECOEXECPROFILE_CHAR4:
    EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR4, &isFlashCode );
#ifdef ECOEXEC_DEBUG
    uartWriteString("isFlashCode: " );
    uartWriteHex( &isFlashCode );
    uartWriteString( "\n\r" );
#endif
    break;
    
  /* the value of flash section of the following code data will be place */
  case ECOEXECPROFILE_CHAR5:
    EcoExecProfile_GetParameter( ECOEXECPROFILE_CHAR5, &codeSection );

    /***** stop all the user event timers before write flash *****/
    osal_stop_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_EVT_1);
    osal_stop_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_EVT_2);
    osal_stop_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_EVT_3);
    osal_stop_timerEx( simpleBLEPeripheral_TaskID, CODEGENERATOR_EVT_4);

    pg = ( CODEGENERATOR_FIRSTPAGE + codeSection ); /* codeSecton: 0 ~ 15 */
#ifdef ECOEXEC_DEBUG
    uartWriteString("Code section: " );
    uartWriteHex( &codeSection );
    uartWriteString( "pg: " );
    uartWriteHex( &pg );
    uartWriteString( "\n\r" );
#endif
  default:
    // should not reach here!
    break;
  }  /* end switch case */
}


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
static void accelRead( void )
{

  static int16 x, y, z;
  int16 new_x, new_y, new_z;

  // Read data for each axis of the accelerometer
  accReadAcc(&new_x, &new_y, &new_z);

  // Check if x-axis value has changed by more than the threshold value and
  // set profile parameter if it has (this will send a notification if enabled)
  if( (x < (new_x-ACCEL_CHANGE_THRESHOLD)) || (x > (new_x+ACCEL_CHANGE_THRESHOLD)) )
  {
    x = new_x;
    Accel_SetParameter(ACCEL_X_ATTR, 2, &x);
  }
  
  // Check if y-axis value has changed by more than the threshold value and
  // set profile parameter if it has (this will send a notification if enabled)
  if( (y < (new_y-ACCEL_CHANGE_THRESHOLD)) || (y > (new_y+ACCEL_CHANGE_THRESHOLD)) )
  {
    y = new_y;
    Accel_SetParameter(ACCEL_Y_ATTR, 2, &y);
  }
  
  // Check if z-axis value has changed by more than the threshold value and
  // set profile parameter if it has (this will send a notification if enabled)
  if( (z < (new_z-ACCEL_CHANGE_THRESHOLD)) || (z > (new_z+ACCEL_CHANGE_THRESHOLD)) )
  {
    z = new_z;  
    Accel_SetParameter(ACCEL_Z_ATTR, 2, &z);
  }
}




#ifdef CC2541
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
void timeRead( void )
{  
  if (timeEnabler){
    // Read time data of the time service
    rtcGetTime( &newTime[0], &newTime[1], &newTime[2] );
    rtcGetDate( &newDate[0], &newDate[1], &newDate[2], &newDate[3], &newDate[4] );
    rtcGetAlarm( &newAlarm[0], &newAlarm[1], &newAlarm[2], &newAlarm[3], &newAlarm[4], &newAlarm[5] );
    
    timeservice_SetParameter(TIME, TIME_LEN, newTime);
    timeservice_SetParameter(DATE, DATE_LEN, newDate);
    timeservice_SetParameter(ALARM, ALARM_LEN, newAlarm);
  }
}
#endif

/**************************************************************************************************
 * @fn      timePort0Isr
 *
 * @brief   Port0 ISR
 *
 * @param
 *
 * @return
 **************************************************************************************************/
HAL_ISR_FUNCTION( halAlarmPort0Isr, P0INT_VECTOR )
{
  if ( P0IFG & HAL_RTC_ALARM_BIT )
  {
    halProcessAlarmInterrupt();
  }
  /*
    Clear the CPU interrupt flag for Port_0
    PxIFG has to be cleared before PxIF
  */
  P0IFG = 0;
  P0IF = 0;
}

/**************************************************************************************************
 * @fn      accPort1Isr
 *
 * @brief   Port0 ISR
 *
 * @param
 *
 * @return
 **************************************************************************************************/
HAL_ISR_FUNCTION( halaccPort1Isr, P1INT_VECTOR )
{
  if ( P1IFG & 0x04 )
  {
    halProcessFreeFallInterrupt();
  }
  /*
    Clear the CPU interrupt flag for Port_1
    PxIFG has to be cleared before PxIF
  */
  P1IFG = 0;
  P1IF = 0;
}

__near_func void execution_ram_code( void )
{
  MEMCTR |= 0x08;
  __asm("LCALL Message+8000h"); /* 0x8000 + Message */
  MEMCTR &= ~0x08;
}


/******************************************  CODE GENERATOR ******************************************/


/*********************************************************************
 * @fn      simpleProfileChangeCB
 *
 * @brief   Callback from SimpleBLEProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
#pragma location="CODEGENERATOR_0"
static void simpleProfileChangeCB( uint8 paramID )
{
  /* codegenerator_simpleProfileChangeCB( uint8 paramID ) */
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_simpleProfileChangeCB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  //codegenerator_simpleProfileChangeCB( paramID );
}

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
#pragma location="CODEGENERATOR_0"
static void accelEnablerChangeCB( void )
{
  /* cg_accelEnablerChangeCB( void ) */
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_accelEnablerChangeCB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" );
}

/*********************************************************************
 * @fn      battProfileChangeCB
 *
 * @brief   Callback from battserviceProfile indicating a value change
 *
 * @param   event - event of the value that was changed.
 *
 * @return  none
 */
#pragma location="CODEGENERATOR_0"
void battProfileChangeCB( uint8 event )
{
  /* codegenerator_simpleProfileChangeCB( uint8 event ) */
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_battProfileChangeCB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" );
}

#pragma location="CODEGENERATOR_0"
void CodeGenerator_EVT_1_CB(void)
{
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_EVT_1_CB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" );
}

#pragma location="CODEGENERATOR_0"
void CodeGenerator_EVT_2_CB(void)
{
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_EVT_2_CB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" );
}

#pragma location="CODEGENERATOR_0"
void CodeGenerator_EVT_3_CB(void)
{
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_EVT_3_CB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" );
}

#pragma location="CODEGENERATOR_0"
void CodeGenerator_EVT_4_CB(void)
{  
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_EVT_4_CB-0x60000" ); /* segment 1 */
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
}

#ifdef CC2541
/*********************************************************************
 * @fn      timeserviceChangeCB
 *
 * @brief   Callback from timeserviceProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
#pragma location="CODEGENERATOR_0"
void timeserviceChangeCB( uint8 paramID )
{
  /* cg_timeserviceChangeCB( uint8 paramID ) */
  asm("NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" \
      "NOP \n" );
  asm( "LJMP cg_timeserviceChangeCB-0x60000" ); /* segment 1*/
  asm("NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" \
    "NOP \n" );
}
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

#pragma location="CODEGENERATOR_1"
void cg_simpleProfileChangeCB( uint8 paramID )
{
  uint8 newValue;
  
  switch( paramID )
  {
  case SIMPLEPROFILE_CHAR1:
    //SimpleProfile_GetParameter( SIMPLEPROFILE_CHAR1, &newValue );
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
 * @fn      cg_accelEnablerChangeCB
 *
 * @brief   Called by the Accelerometer Profile when the Enabler Attribute
 *          is changed.
 *
 * @param   none
 *
 * @return  none
 */
#pragma location="CODEGENERATOR_1"
void cg_accelEnablerChangeCB( void )
{
  bStatus_t status = Accel_GetParameter( ACCEL_ENABLER, &accelEnabler );

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
#pragma location="CODEGENERATOR_1"
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

#pragma location="CODEGENERATOR_1"
void cg_EVT_1_CB( void )
{
  
}

#pragma location="CODEGENERATOR_1"
void cg_EVT_2_CB( void )
{
  
}

#pragma location="CODEGENERATOR_1"
void cg_EVT_3_CB( void )
{
  
}

#pragma location="CODEGENERATOR_1"
void cg_EVT_4_CB( void )
{
  
}

#ifdef CC2541
/*********************************************************************
 * @fn      cg_timeserviceChangeCB
 *
 * @brief   Callback from timeserviceProfile indicating a value change
 *
 * @param   paramID - parameter ID of the value that was changed.
 *
 * @return  none
 */
#pragma location="CODEGENERATOR_1"
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


/*********************************************************************
 * @fn      CodeGeneratorStartPoint
 *
 * @brief   Code Generator main function entrance point
 *
 * @param   None
 *
 * @return  none
 */
#pragma location="CODEGENERATOR_4"
void CodeGeneratorStartPoint( void )
{
// Setup Relay function
__asm("NOP");
}