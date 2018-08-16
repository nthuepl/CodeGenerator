/**************************************************************************************************
  Filename:       EcoExecGATTprofile.c
  Revised:        
  Revision:       $Revision: 23333 $

  Description:    This file contains the Simple GATT profile sample GATT service 
                  profile for use with the BLE sample application.

  Copyright 2013 Lai Tong Kun, EPL, NTHU. All rights reserved.
**************************************************************************************************/

/*********************************************************************
 * INCLUDES
 */
#include "bcomdef.h"
#include "OSAL.h"
#include "linkdb.h"
#include "att.h"
#include "gatt.h"
#include "gatt_uuid.h"
#include "gattservapp.h"
#include "gapbondmgr.h"
#include "hal_led.h"
#include "EcoExecGATTprofile.h"

/* include for the ROM code reprogramming */
#include "hal_flash.h"

/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * CONSTANTS
 */

#define CODEGENERATOR_FIRSTPAGE 0x30000/HAL_FLASH_PAGE_SIZE
#define CODEGENERATOR_WRITING_FLASH_SIZE CODEDATA_LEN/HAL_FLASH_WORD_SIZE

#define SERVAPP_NUM_ATTR_SUPPORTED        17

/*********************************************************************
 * TYPEDEFS
 */

/*********************************************************************
 * GLOBAL VARIABLES
 */

uint16 EcoExecProfileConnHandle = 0xFFFF;
   
// EcoExec GATT Profile Service UUID: 0xFCF0
CONST uint8 EcoExecProfileServUUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_SERV_UUID), HI_UINT16(ECOEXECPROFILE_SERV_UUID)
};

// Place holders for the GATT Server App to be able to lookup handles.
// EcoExec GATT Profile Characteristic 1 UUID: 0xFCF1 - 1 bytes
CONST uint8 EcoExecProfilechar1UUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_CHAR1_UUID), HI_UINT16(ECOEXECPROFILE_CHAR1_UUID)
};


/*********************************************************************
 * EXTERNAL VARIABLES
 */

/*********************************************************************
 * EXTERNAL FUNCTIONS
 */

/*********************************************************************
 * LOCAL VARIABLES
 */

static unsigned short codeSegmentCnt;
static unsigned char pg;
static unsigned char isFlashCode;
static unsigned char codeSection;
static unsigned char sequenceNum[2];
static unsigned char codeSegmentNum[2];
static unsigned short offset = 0x0000;
static unsigned short pgoffset_boundary = 0x0000;
static unsigned short addr;

unsigned char Message[500];
unsigned char xDataSeg[256];

//#define FLASH_DEBUG
//#define ECOEXEC_DEBUG
static EcoExecProfileCBs_t *EcoExecProfile_AppCBs = NULL;

/*********************************************************************
 * Profile Attributes - variables
 */

// EcoExec Profile Service attribute
static CONST gattAttrType_t EcoExecProfileService = { ATT_BT_UUID_SIZE, EcoExecProfileServUUID };


// EcoExec Profile Characteristic 1 Properties
static uint8 EcoExecProfileChar1Props = GATT_PROP_READ | GATT_PROP_WRITE;

// Characteristic 1 Value
static uint8 EcoExecProfileChar1 = 0;

// EcoExec Profile Characteristic 1 User Description
static uint8 EcoExecProfileChar1UserDesp[17] = "Data\0";

/*********************************************************************
 * Profile Attributes - Table
 */

static gattAttribute_t EcoExecProfileAttrTbl[SERVAPP_NUM_ATTR_SUPPORTED] = 
{
  // EcoExec Profile Service
  { 
    { ATT_BT_UUID_SIZE, primaryServiceUUID }, /* type */
    GATT_PERMIT_READ,                         /* permissions */
    0,                                        /* handle */
    (uint8 *)&EcoExecProfileService            /* pValue */
  },
  
  // Characteristic 1 Declaration
  { 
    { ATT_BT_UUID_SIZE, characterUUID },
    GATT_PERMIT_READ, 
    0,
    &EcoExecProfileChar1Props 
  },
  
  // Characteristic Value 1
  { 
    { ATT_BT_UUID_SIZE, EcoExecProfilechar1UUID },
    GATT_PERMIT_READ | GATT_PERMIT_WRITE, 
    0, 
    &EcoExecProfileChar1 
  },
  
  // Characteristic 1 User Description
  { 
    { ATT_BT_UUID_SIZE, charUserDescUUID },
    GATT_PERMIT_READ, 
    0, 
    EcoExecProfileChar1UserDesp 
  },  
  
};


/*********************************************************************
 * LOCAL FUNCTIONS
 */
static uint8 EcoExecProfile_ReadAttrCB( uint16 connHandle, gattAttribute_t *pAttr, 
                            uint8 *pValue, uint8 *pLen, uint16 offset, uint8 maxLen );
static bStatus_t EcoExecProfile_WriteAttrCB( uint16 connHandle, gattAttribute_t *pAttr,
                                 uint8 *pValue, uint8 len, uint16 offset );

static void EcoExecProfile_HandleConnStatusCB( uint16 connHandle, uint8 changeType );

static void SetHeader(uint8* pValue);
static void SetCodeData( uint8* pValue );


/*********************************************************************
 * PROFILE CALLBACKS
 */
// EcoExec Profile Service Callbacks
CONST gattServiceCBs_t EcoExecProfileCBs =
{
  EcoExecProfile_ReadAttrCB,  // Read callback function pointer
  EcoExecProfile_WriteAttrCB, // Write callback function pointer
  NULL                       // Authorization callback function pointer
};

/*********************************************************************
 * PUBLIC FUNCTIONS
 */

/*********************************************************************
 * @fn      EcoExecProfile_AddService
 *
 * @brief   Initializes the EcoExec Profile service by registering
 *          GATT attributes with the GATT server.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  Success or Failure
 */
bStatus_t EcoExecProfile_AddService( uint32 services )
{
  uint8 status = SUCCESS;

  // Initialize Client Characteristic Configuration attributes

  // Register with Link DB to receive link status change callback
  VOID linkDB_Register( EcoExecProfile_HandleConnStatusCB );  
  
  if ( services & ECOEXECPROFILE_SERVICE )
  {
    // Register GATT attribute list and CBs with GATT Server App
    status = GATTServApp_RegisterService( EcoExecProfileAttrTbl, 
                                          GATT_NUM_ATTRS( EcoExecProfileAttrTbl ),
                                          &EcoExecProfileCBs );
  }

  return ( status );
}


/*********************************************************************
 * @fn      EcoExecProfile_RegisterAppCBs
 *
 * @brief   Registers the application callback function. Only call 
 *          this function once.
 *
 * @param   callbacks - pointer to application callbacks.
 *
 * @return  SUCCESS or bleAlreadyInRequestedMode
 */
bStatus_t EcoExecProfile_RegisterAppCBs( EcoExecProfileCBs_t *appCallbacks )
{
  if ( appCallbacks )
  {
    EcoExecProfile_AppCBs = appCallbacks;
    
    return ( SUCCESS );
  }
  else
  {
    return ( bleAlreadyInRequestedMode );
  }
}

/*********************************************************************
 * @fn          EcoExecProfile_ReadAttrCB
 *
 * @brief       Read an attribute.
 *
 * @param       connHandle - connection message was received on
 * @param       pAttr - pointer to attribute
 * @param       pValue - pointer to data to be read
 * @param       pLen - length of data to be read
 * @param       offset - offset of the first octet to be read
 * @param       maxLen - maximum length of data to be read
 *
 * @return      Success or Failure
 */
static uint8 EcoExecProfile_ReadAttrCB( uint16 connHandle, gattAttribute_t *pAttr, 
                            uint8 *pValue, uint8 *pLen, uint16 offset, uint8 maxLen )
{
  bStatus_t status = SUCCESS;
  // TBD: is there any use for supporting reads
  *pLen = 0;
  return ( status );
}

/*********************************************************************
 * @fn      EcoExecProfile_WriteAttrCB
 *
 * @brief   Validate attribute data prior to a write operation
 *
 * @param   connHandle - connection message was received on
 * @param   pAttr - pointer to attribute
 * @param   pValue - pointer to data to be written
 * @param   len - length of data
 * @param   offset - offset of the first octet to be written
 * @param   complete - whether this is the last packet
 * @param   oper - whether to validate and/or write attribute value  
 *
 * @return  Success or Failure
 */
static bStatus_t EcoExecProfile_WriteAttrCB( uint16 connHandle, gattAttribute_t *pAttr,
                                 uint8 *pValue, uint8 len, uint16 offset )
{
  bStatus_t status = SUCCESS;
  
  // If attribute permissions require authorization to write, return error
  if ( gattPermitAuthorWrite( pAttr->permissions ) )
  {
    // Insufficient authorization
    return ( ATT_ERR_INSUFFICIENT_AUTHOR );
  }
  
  if ( pAttr->type.len == ATT_BT_UUID_SIZE )
  {
    // 16-bit UUID
    uint16 uuid = BUILD_UINT16( pAttr->type.uuid[0], pAttr->type.uuid[1]);
    switch ( uuid )
    {
      case ECOEXECPROFILE_CHAR1_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != HEADER_LEN || len != CODEDATA_LEN )
          {
            status = ATT_ERR_INVALID_VALUE_SIZE;
          }
        }
        else
        {
          status = ATT_ERR_ATTR_NOT_LONG;
        }
        
        //Write the value
        if ( status == SUCCESS )
        {
          if ( len == HEADER_LEN )
          {
            SetHeader(pValue);
          }
          
          if( len == CODEDATA_LEN )
          {
            SetCodeData(pValue);
          }
        }
        EcoExecProfileConnHandle = connHandle;
        break;
        
      default:
        status = ATT_ERR_ATTR_NOT_FOUND;
        break;
    }
  }
  else
  {
    // 128-bit UUID
    status = ATT_ERR_INVALID_HANDLE;
  }
  
  return ( status );
}

/*one bytes pValue[0] Code type Flag 0:RAM Code 1:Flash Code,
* one bytes pValue[1] Flash Code Section
* two bytes pValue[2,3] sequence number, 
* two bytes pValue[4,5] segment number, */
static void SetHeader( uint8* pValue )
{
  /* revser the xdata segment for sdcc code */
  if( xDataSeg[0] == 0x00 )
    xDataSeg[3] = 1;
  
  
  isFlashCode = pValue[0];
  codeSection = pValue[1];
  sequenceNum[0] = pValue[2];
  sequenceNum[1] = pValue[3];
  codeSegmentNum[0] = pValue[4];
  codeSegmentNum[1] = pValue[5];
  
  /* reload the Code Segment counter to zero */
  codeSegmentCnt = 0x0000;
  
  /* reload the Flash Code offset counter to zero */
  offset = 0x0000;
  
  if( pValue[0] == TRUE ){
    /* the value of flash section of the following code data will be place */
    pg = ( CODEGENERATOR_FIRSTPAGE + pValue[1] ); /* codeSecton: 0 ~ 15 */
    // stop all call functions before flash writting
    if( EcoExecProfile_AppCBs && EcoExecProfile_AppCBs->pfnEcoExecProfileChange )
    {
      EcoExecProfile_AppCBs->pfnEcoExecProfileChange( STOP_CALLBACKS );  
    }
  }
#ifdef ECOEXEC_DEBUG
  uartWriteString("> Code type: " );
  if(pValue[0]=TRUE){
    uartWriteString( "Flash Code." );
    
    uartWriteString("> Code section: " );
    uartWriteHex( pValue+1 );
    
    uartWriteString( "> pg: " );
    uartWriteHex( &pg );
    uartWriteString( "\n\r" );
  }
  else{
    uartWriteString( "RAM Code" );
    uartWriteString( "\n\r" );
  }
  
  uartWriteString("> sequence: " );
  uartWriteHex( pValue+2 );
  uartWriteHex( pValue+3 );
  uartWriteString( "\n\r" );
  
  uartWriteString("> segment: " );
  uartWriteHex( pValue+4 );
  uartWriteHex( pValue+5 );
  uartWriteString( "\n\r" );
#endif  
}

/*one bytes pValue[0] Code type Flag,
* one bytes pValue[1] Flash Code Section
* two bytes pValue[2,3] sequence number, 
* two bytes pValue[4,5] segment number, */
static void SetCodeData( uint8* pValue )
{
  uint8 notifyApp = 0xFF;
  
  if( codeSegmentNum[1] != 0x00 || codeSegmentNum[0] != 0x00 ){ /* code segment len is not 0x0000 */
    if( isFlashCode == FALSE ){ 
      /* Copy code to xdata-SRAM */
      (void)osal_memcpy( &Message[codeSegmentCnt*CODEDATA_LEN], pValue+4, CODEDATA_LEN );   
    }else{
    /* Write code to Flash Memory */
#ifdef FLASH_DEBUG
    int i;
    static unsigned char FlashCode[HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE];
    /********************** read flash **********************/
    HalFlashRead( pg, offset, FlashCode, HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE);
    for(i=0; i < HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE; i++){
      uartWriteHex( &FlashCode[i] );
    }
    uartWriteString("\r\n");
#endif
    
    /********************** recaculate flash address **********************/
    addr = (offset >> 2) + ((uint16)pg << 9);
    
    /********************** Erase flash **********************/
    if( offset == 0x0000 ){
        pgoffset_boundary = (HAL_FLASH_PAGE_SIZE-1);
        HalFlashErase( pg );
    }else if( (offset+20) > pgoffset_boundary ){
        HalFlashErase( pg+(pgoffset_boundary/(HAL_FLASH_PAGE_SIZE-1)) );
        pgoffset_boundary+=(HAL_FLASH_PAGE_SIZE-1);
    }
#ifdef FLASH_DEBUG
    /********************** read flash **********************/
    HalFlashRead( pg, offset, FlashCode, HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE);
    for(i=0; i < HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE; i++){
      uartWriteHex( &FlashCode[i] );
    }
    uartWriteString("\r\n");
#endif
    
    /********************** write flash **********************/
    HalFlashWrite( addr, pValue, CODEGENERATOR_WRITING_FLASH_SIZE ); 
#ifdef FLASH_DEBUG
    HalFlashRead( pg, offset, FlashCode, HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE);
    for(i=0; i < HAL_FLASH_WORD_SIZE*CODEGENERATOR_WRITING_FLASH_SIZE; i++){
      uartWriteHex( &FlashCode[i] );
    }
    uartWriteString("\r\n----------------------\r\n");
#endif

#if defined( CC2541 ) || defined( CC2541S )
    P2_1 ^= 1;
#else
    P0_4 ^= 1;
#endif
    offset += CODEDATA_LEN;
    }   
    
    /* update code segment counter */
    codeSegmentCnt++;
    
    if( codeSegmentCnt == BUILD_UINT16(pValue[5], pValue[4]) ) /* code data loading is finish */
      if( isFlashCode == FALSE ) 
        notifyApp = RAMCODE_CALL;   /* Run RAM Code */
      else{
        if( codeSection == MAIN_SECTIOIN )
          notifyApp = FLASHCODE_CALL; /* Run Flash Code */
#ifdef ECOEXEC_DEBUG
        uartWriteString( "Finished flash code loading.\n\r" );
#endif
      }
    
      // set ram code call or flash code call by event call back
      if ( (notifyApp != 0xFF ) && EcoExecProfile_AppCBs && EcoExecProfile_AppCBs->pfnEcoExecProfileChange )
      {
        EcoExecProfile_AppCBs->pfnEcoExecProfileChange( notifyApp );  
      }

  }
}
/*********************************************************************
 * @fn          EcoExecProfile_HandleConnStatusCB
 *
 * @brief       EcoExec Profile link status change handler function.
 *
 * @param       connHandle - connection handle
 * @param       changeType - type of change
 *
 * @return      none
 */
static void EcoExecProfile_HandleConnStatusCB( uint16 connHandle, uint8 changeType )
{ 
  // Make sure this is not loopback connection
  if ( connHandle != LOOPBACK_CONNHANDLE )
  {
    // Reset Client Char Config if connection has dropped
    if ( ( changeType == LINKDB_STATUS_UPDATE_REMOVED )      ||
         ( ( changeType == LINKDB_STATUS_UPDATE_STATEFLAGS ) && 
           ( !linkDB_Up( connHandle ) ) ) )
    { 
      
    }
  }
}
/*********************************************************************
*********************************************************************/

