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

/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * CONSTANTS
 */

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

// Characteristic 1 UUID: 0xFCF1 - f4 bytes Head file 
CONST uint8 EcoExecProfilechar1UUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_CHAR1_UUID), HI_UINT16(ECOEXECPROFILE_CHAR1_UUID)
};

// Characteristic 2 UUID: 0xFCF2 - 20 bytes code data
CONST uint8 EcoExecProfilechar2UUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_CHAR2_UUID), HI_UINT16(ECOEXECPROFILE_CHAR2_UUID)
};

// Characteristic 3 UUID: 0xFCF3 - uint16 FirstCodeMemoryAddress
CONST uint8 EcoExecProfilechar3UUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_CHAR3_UUID), HI_UINT16(ECOEXECPROFILE_CHAR3_UUID)
};

// Characteristic 4 UUID: 0xFCF4
CONST uint8 EcoExecProfilechar4UUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_CHAR4_UUID), HI_UINT16(ECOEXECPROFILE_CHAR4_UUID)
};

// Characteristic 5 UUID: 0xFCF5
CONST uint8 EcoExecProfilechar5UUID[ATT_BT_UUID_SIZE] =
{ 
  LO_UINT16(ECOEXECPROFILE_CHAR5_UUID), HI_UINT16(ECOEXECPROFILE_CHAR5_UUID)
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

static EcoExecProfileCBs_t *EcoExecProfile_AppCBs = NULL;

/*********************************************************************
 * Profile Attributes - variables
 */

// EcoExec Profile Service attribute
static CONST gattAttrType_t EcoExecProfileService = { ATT_BT_UUID_SIZE, EcoExecProfileServUUID };


// EcoExec Profile Characteristic 1 Properties
static uint8 EcoExecProfileChar1Props = GATT_PROP_READ | GATT_PROP_WRITE;

// Characteristic 1 Value
static uint8 EcoExecProfileChar1[4] = {0,0,0,0};

// EcoExec Profile Characteristic 1 User Description
static uint8 EcoExecProfileChar1UserDesp[17] = "Head file\0";


// EcoExec Profile Characteristic 2 Properties
static uint8 EcoExecProfileChar2Props = GATT_PROP_READ | GATT_PROP_WRITE;

// Characteristic 2 Value
static uint8 EcoExecProfileChar2[ECOEXECPROFILE_CHAR2_LEN] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

// EcoExec Profile Characteristic 2 User Description
static uint8 EcoExecProfileChar2UserDesp[17] = "Code data\0";


// EcoExec Profile Characteristic 3 Properties
static uint8 EcoExecProfileChar3Props = GATT_PROP_WRITE;

// Characteristic 3 Value
static uint8 EcoExecProfileChar3[2] = {0x00, 0x00};

// EcoExec Profile Characteristic 3 User Description
static uint8 EcoExecProfileChar3UserDesp[17] = "FirstCodeLoc.\0";


// EcoExec Profile Flash Code Flag Properties
static uint8 EcoExecProfileChar4Props = GATT_PROP_READ | GATT_PROP_WRITE;

// Flash Code Flag Value
static uint8 EcoExecProfileChar4 = 0;
                                        
// EcoExec Profile Flash Code Flag User Description
static uint8 EcoExecProfileChar4UserDesp[17] = "Flash Code Flag\0";


// EcoExec Profile Flash Code Section Properties
static uint8 EcoExecProfileChar5Props = GATT_PROP_READ | GATT_PROP_WRITE;

// Flash Code Section Value
static uint8 EcoExecProfileChar5 = 0;

// EcoExec Profile Flash Code Section User Description
static uint8 EcoExecProfileChar5UserDesp[17] = "FlashCodeSection\0";


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
        EcoExecProfileChar1 
      },

      // Characteristic 1 User Description
      { 
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0, 
        EcoExecProfileChar1UserDesp 
      },      

    // Characteristic 2 Declaration
    { 
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ | GATT_PERMIT_WRITE, 
      0,
      &EcoExecProfileChar2Props 
    },

      // Characteristic Value 2
      { 
        { ATT_BT_UUID_SIZE, EcoExecProfilechar2UUID },
        GATT_PERMIT_READ|GATT_PERMIT_WRITE, 
        0, 
        EcoExecProfileChar2 
      },

      // Characteristic 2 User Description
      { 
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0, 
        EcoExecProfileChar2UserDesp 
      },           
      
    // Characteristic 3 Declaration
    { 
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ, 
      0,
      &EcoExecProfileChar3Props 
    },

      // Characteristic Value 3
      { 
        { ATT_BT_UUID_SIZE, EcoExecProfilechar3UUID },
        GATT_PERMIT_READ|GATT_PERMIT_WRITE, 
        0, 
        EcoExecProfileChar3 
      },

      // Characteristic 3 User Description
      { 
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0, 
        EcoExecProfileChar3UserDesp 
      },

    // Flash Code Flag Declaration
    { 
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ, 
      0,
      &EcoExecProfileChar4Props 
    },

      // Flash Code Flag value
      { 
        { ATT_BT_UUID_SIZE, EcoExecProfilechar4UUID },
        GATT_PERMIT_READ|GATT_PERMIT_WRITE, 
        0, 
        &EcoExecProfileChar4 
      },
     
      // Flash Code Flag Description
      { 
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0, 
        EcoExecProfileChar4UserDesp 
      },
      
    // Characteristic 5 Declaration
    { 
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ, 
      0,
      &EcoExecProfileChar5Props 
    },

      // Characteristic Value 5
      { 
        { ATT_BT_UUID_SIZE, EcoExecProfilechar5UUID },
        GATT_PERMIT_READ|GATT_PERMIT_WRITE, 
        0, 
        &EcoExecProfileChar5 
      },

      // Characteristic 5 User Description
      { 
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0, 
        EcoExecProfileChar5UserDesp 
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
 * @fn      EcoExecProfile_SetParameter
 *
 * @brief   Set a EcoExec Profile parameter.
 *
 * @param   param - Profile parameter ID
 * @param   len - length of data to right
 * @param   value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 *
 * @return  bStatus_t
 */
bStatus_t EcoExecProfile_SetParameter( uint8 param, uint8 len, void *value )
{
  bStatus_t ret = SUCCESS;
  switch ( param )
  {
    case ECOEXECPROFILE_CHAR1:
      if ( len == ECOEXECPROFILE_CHAR1_LEN ) 
      {
        VOID osal_memcpy( EcoExecProfileChar2, value, ECOEXECPROFILE_CHAR1_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ECOEXECPROFILE_CHAR2:
      if ( len == ECOEXECPROFILE_CHAR2_LEN ) 
      {
        VOID osal_memcpy( EcoExecProfileChar2, value, ECOEXECPROFILE_CHAR2_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ECOEXECPROFILE_CHAR3:
      if ( len == ECOEXECPROFILE_CHAR3_LEN ) 
      {
        VOID osal_memcpy( EcoExecProfileChar3, value, ECOEXECPROFILE_CHAR3_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ECOEXECPROFILE_CHAR4:
      if ( len == sizeof ( uint8 ) ) 
      {
        EcoExecProfileChar4 = *((uint8*)value);
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ECOEXECPROFILE_CHAR5:
      if ( len == ECOEXECPROFILE_CHAR5_LEN ) 
      {
        VOID osal_memcpy( &EcoExecProfileChar5, value, ECOEXECPROFILE_CHAR5_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;
      
    default:
      ret = INVALIDPARAMETER;
      break;
  }
  
  return ( ret );
}

/*********************************************************************
 * @fn      EcoExecProfile_GetParameter
 *
 * @brief   Get a EcoExec Profile parameter.
 *
 * @param   param - Profile parameter ID
 * @param   value - pointer to data to put.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 *
 * @return  bStatus_t
 */
bStatus_t EcoExecProfile_GetParameter( uint8 param, void *value )
{
  bStatus_t ret = SUCCESS;
  switch ( param )
  {
    case ECOEXECPROFILE_CHAR1:
      VOID osal_memcpy( value, EcoExecProfileChar1, ECOEXECPROFILE_CHAR1_LEN );
      //value = EcoExecProfileChar1;
      break;

    case ECOEXECPROFILE_CHAR2:
      VOID osal_memcpy( value, EcoExecProfileChar2, ECOEXECPROFILE_CHAR2_LEN );
      //value = EcoExecProfileChar2;
      break;      

    case ECOEXECPROFILE_CHAR3:
      VOID osal_memcpy( value, EcoExecProfileChar3, ECOEXECPROFILE_CHAR3_LEN );
      break;  

    case ECOEXECPROFILE_CHAR4:
      *((uint8*)value) = EcoExecProfileChar4;
      break;

    case ECOEXECPROFILE_CHAR5:
      VOID osal_memcpy( value, &EcoExecProfileChar5, ECOEXECPROFILE_CHAR5_LEN );
      break;      
      
    default:
      ret = INVALIDPARAMETER;
      break;
  }
  
  return ( ret );
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

  // If attribute permissions require authorization to read, return error
  if ( gattPermitAuthorRead( pAttr->permissions ) )
  {
    // Insufficient authorization
    return ( ATT_ERR_INSUFFICIENT_AUTHOR );
  }
  
  // Make sure it's not a blob operation (no attributes in the profile are long)
  if ( offset > 0 )
  {
    return ( ATT_ERR_ATTR_NOT_LONG );
  }
 
  if ( pAttr->type.len == ATT_BT_UUID_SIZE )
  {
    // 16-bit UUID
    uint16 uuid = BUILD_UINT16( pAttr->type.uuid[0], pAttr->type.uuid[1]);
    switch ( uuid )
    {
      // No need for "GATT_SERVICE_UUID" or "GATT_CLIENT_CHAR_CFG_UUID" cases;
      // gattserverapp handles those reads

      // characteritisc 3 does not have read permissions; therefore it is not
      //   included here
      // characteristic 4 does not have read permissions, but because it
      //   can be sent as a notification, it is included here
      case ECOEXECPROFILE_CHAR1_UUID:
        *pLen = ECOEXECPROFILE_CHAR1_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ECOEXECPROFILE_CHAR1_LEN );
        break;
        
      case ECOEXECPROFILE_CHAR2_UUID:
        *pLen = ECOEXECPROFILE_CHAR2_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ECOEXECPROFILE_CHAR2_LEN );
        break;
        
      case ECOEXECPROFILE_CHAR3_UUID:
        *pLen = ECOEXECPROFILE_CHAR3_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ECOEXECPROFILE_CHAR3_LEN );
        break;
        
      case ECOEXECPROFILE_CHAR4_UUID:
        *pLen = ECOEXECPROFILE_CHAR4_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ECOEXECPROFILE_CHAR4_LEN );
        break;
        
      case ECOEXECPROFILE_CHAR5_UUID:
        *pLen = ECOEXECPROFILE_CHAR5_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ECOEXECPROFILE_CHAR5_LEN );
        break;
        
      default:
        // Should never get here! (characteristics 3 and 4 do not have read permissions)
        *pLen = 0;
        status = ATT_ERR_ATTR_NOT_FOUND;
        break;
    }
  }
  else
  {
    // 128-bit UUID
    *pLen = 0;
    status = ATT_ERR_INVALID_HANDLE;
  }

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
  uint8 notifyApp = 0xFF;
  
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
          if ( len != ECOEXECPROFILE_CHAR1_LEN )
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
          uint8 *pCurValue = (uint8 *)pAttr->pValue;        
          VOID osal_memcpy( pCurValue, pValue, ECOEXECPROFILE_CHAR1_LEN );
          //if( pAttr->pValue == &EcoExecProfileChar1 )
          //{
            notifyApp = ECOEXECPROFILE_CHAR1;        
          //}
        }
        EcoExecProfileConnHandle = connHandle;  
        break;
        
      case ECOEXECPROFILE_CHAR2_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ECOEXECPROFILE_CHAR2_LEN )
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
          uint8 *pCurValue = (uint8 *)pAttr->pValue;        
          VOID osal_memcpy( pCurValue, pValue, ECOEXECPROFILE_CHAR2_LEN );
          //if( pAttr->pValue == &EcoExecProfileChar1 )
          //{
            notifyApp = ECOEXECPROFILE_CHAR2;        
          //}
          EcoExecProfileConnHandle = connHandle;      
         
        }
        break;
        
      case ECOEXECPROFILE_CHAR3_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ECOEXECPROFILE_CHAR3_LEN )
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
          uint8 *pCurValue = (uint8 *)pAttr->pValue;        
          VOID osal_memcpy( pCurValue, pValue, ECOEXECPROFILE_CHAR3_LEN );
          //if( pAttr->pValue == &EcoExecProfileChar1 )
          //{
            notifyApp = ECOEXECPROFILE_CHAR3;        
          //}
          EcoExecProfileConnHandle = connHandle;      
         
        }
        break;
        
       case ECOEXECPROFILE_CHAR4_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ECOEXECPROFILE_CHAR4_LEN )
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
          uint8 *pCurValue = (uint8 *)pAttr->pValue;        
          VOID osal_memcpy( pCurValue, pValue, ECOEXECPROFILE_CHAR4_LEN );
          //if( pAttr->pValue == &EcoExecProfileChar1 )
          //{
            notifyApp = ECOEXECPROFILE_CHAR4;        
          //}
          EcoExecProfileConnHandle = connHandle;      
         
        }
        break;
        
    case ECOEXECPROFILE_CHAR5_UUID:
      //Validate the value
      // Make sure it's not a blob oper
      if ( offset == 0 )
      {
        if ( len != ECOEXECPROFILE_CHAR5_LEN )
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
        uint8 *pCurValue = (uint8 *)pAttr->pValue;        
        VOID osal_memcpy( pCurValue, pValue, ECOEXECPROFILE_CHAR5_LEN );
        //if( pAttr->pValue == &EcoExecProfileChar1 )
        //{
        notifyApp = ECOEXECPROFILE_CHAR5;        
        //}
        EcoExecProfileConnHandle = connHandle;      
        
      }
      break;

      case GATT_CLIENT_CHAR_CFG_UUID:
        status = GATTServApp_ProcessCCCWriteReq( connHandle, pAttr, pValue, len,
                                                 offset, GATT_CLIENT_CFG_NOTIFY );
        break;
        
      default:
        // Should never get here! (characteristics 2 and 4 do not have write permissions)
        status = ATT_ERR_ATTR_NOT_FOUND;
        break;
    }
  }
  else
  {
    // 128-bit UUID
    status = ATT_ERR_INVALID_HANDLE;
  }

  // If a characteristic value changed then callback function to notify application of change
  if ( (notifyApp != 0xFF ) && EcoExecProfile_AppCBs && EcoExecProfile_AppCBs->pfnEcoExecProfileChange )
  {
    EcoExecProfile_AppCBs->pfnEcoExecProfileChange( notifyApp );  
  }
  
  return ( status );
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

