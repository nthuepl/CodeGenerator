/**************************************************************************************************
	Filename:       timeservice.h
	Revised:        $Date:2014-03-13 16:50:14 $

	Description:    This file contains the GATT profile definitions and prototypes..

	Copyright 2013 EPLAB National Tsing Hua University. All rights reserved.
	The information contained herein is confidential property of NTHU. 	The material may be used for a personal and non-commercial use only in connection with 	a legitimate academic research purpose. Any attempt to copy, modify, and distribute any portion of this source code or derivative thereof for commercial, political, or propaganda purposes is strictly prohibited. All other uses require explicit written permission from the authors and copyright holders. This copyright statement must be retained in its entirety and displayed in the copyright statement of derived source code or systems.
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

#include "timeservice.h"

/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * CONSTANTS
 */

#define SERVAPP_NUM_ATTR_SUPPORTED        46

/*********************************************************************
 * TYPEDEFS
 */

/*********************************************************************
 * GLOBAL VARIABLES
 */

// GATT Profile Service UUID: 0xFDF0
CONST uint8 timeserviceServUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(TIMESERVICE_SERV_UUID), HI_UINT16(TIMESERVICE_SERV_UUID)
};

// TIME_ENABLER UUID: 0xFDF1
CONST uint8 TIME_ENABLERUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(TIME_ENABLER_UUID), HI_UINT16(TIME_ENABLER_UUID)
};

// TIME UUID: 0xFDF2
CONST uint8 TIMEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(TIME_UUID), HI_UINT16(TIME_UUID)
};

// DATE UUID: 0xFDF3
CONST uint8 DATEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(DATE_UUID), HI_UINT16(DATE_UUID)
};

// ALARM UUID: 0xFDF4
CONST uint8 ALARMUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_UUID), HI_UINT16(ALARM_UUID)
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

static timeserviceCBs_t *timeservice_AppCBs = NULL;

/*********************************************************************
 * Profile Attributes - variables
 */

// Profile Service attribute
static CONST gattAttrType_t timeserviceService = { ATT_BT_UUID_SIZE, timeserviceServUUID };

// Profile TIME_ENABLER Properties
static uint8 TIME_ENABLERProps = GATT_PROP_READ | GATT_PROP_WRITE;

// TIME_ENABLER Value
static uint8 TIME_ENABLERValue = 0;// Profile TIME_ENABLER User Description
static uint8 TIME_ENABLERUserDesp[13] = "time_enabler\0";

// Profile TIME Properties
static uint8 TIMEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// TIME Value
static uint8 TIMEValue[TIME_LEN] = { 0, 0, 0 };// Profile HOUR User Description
static uint8 TIMEUserDesp[5] = "time\0";

// Profile DATE Properties
static uint8 DATEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// DATE Value
static uint8 DATEValue[DATE_LEN] = {0, 0, 0, 0, 0 };// Profile MINUTE User Description
static uint8 DATEUserDesp[7] = "date\0";

// Profile ALARM Properties
static uint8 ALARMProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM Value
static uint8 ALARMValue[ALARM_LEN] = { 0, 0, 0, 0, 0, 0 };// Profile SECOND User Description
static uint8 ALARMUserDesp[7] = "alarm\0";


/*********************************************************************
 * Profile Attributes - Table
 */

static gattAttribute_t timeserviceAttrTbl[SERVAPP_NUM_ATTR_SUPPORTED] = 
{
  // Simple Profile Service
  {
    { ATT_BT_UUID_SIZE, primaryServiceUUID }, /* type */
    GATT_PERMIT_READ,                         /* permissions */
    0,                                        /* handle */
    (uint8 *)&timeserviceService           /* pValue */
  },

    // TIME_ENABLER Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &TIME_ENABLERProps
    },

      // TIME_ENABLER Value
      {
        { ATT_BT_UUID_SIZE, TIME_ENABLERUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &TIME_ENABLERValue
      },

      // TIME_ENABLER User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        TIME_ENABLERUserDesp
      },

    // TIME Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &TIMEProps
    },

      // TIME Value
      {
        { ATT_BT_UUID_SIZE, TIMEUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        TIMEValue
      },

      // TIME User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        TIMEUserDesp
      },

    // DATE Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &DATEProps
    },

      // DATE Value
      {
        { ATT_BT_UUID_SIZE, DATEUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        DATEValue
      },

      // DATE User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        DATEUserDesp
      },

    // ALARM Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARMProps
    },

      // ALARM Value
      {
        { ATT_BT_UUID_SIZE, ALARMUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        ALARMValue
      },

      // ALARM User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARMUserDesp
      },
};


/*********************************************************************
 * LOCAL FUNCTIONS
 */
static uint8 timeservice_ReadAttrCB( uint16 connHandle, gattAttribute_t *pAttr, 
                            uint8 *pValue, uint8 *pLen, uint16 offset, uint8 maxLen );
static bStatus_t timeservice_WriteAttrCB( uint16 connHandle, gattAttribute_t *pAttr,
                                 uint8 *pValue, uint8 len, uint16 offset );

static void timeservice_HandleConnStatusCB( uint16 connHandle, uint8 changeType );


/*********************************************************************
 * PROFILE CALLBACKS
 */
// timeserviceService Callbacks
CONST gattServiceCBs_t timeserviceCBs =
{
  timeservice_ReadAttrCB,  // Read callback function pointer
  timeservice_WriteAttrCB, // Write callback function pointer
  NULL                       // Authorization callback function pointer
};

/*********************************************************************
 * PUBLIC FUNCTIONS
 */

/*********************************************************************
 * @fn      timeservice_AddService
 *
 * @brief   Initializes the timeservice service by registering
 *          GATT attributes with the GATT server.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  Success or Failure
 */
bStatus_t timeservice_AddService( uint32 services )
{
  uint8 status = SUCCESS;

  // Register with Link DB to receive link status change callback
  VOID linkDB_Register( timeservice_HandleConnStatusCB );

  if ( services & TIMESERVICE_SERVICE )
  {
    // Register GATT attribute list and CBs with GATT Server App
    status = GATTServApp_RegisterService( timeserviceAttrTbl, 
                                          GATT_NUM_ATTRS( timeserviceAttrTbl ),
                                          &timeserviceCBs );
  }

  return ( status );
}


/*********************************************************************
 * @fn      timeservice_RegisterAppCBs
 *
 * @brief   Registers the application callback function. Only call
 *          this function once.
 *
 * @param   callbacks - pointer to application callbacks.
 *
 * @return  SUCCESS or bleAlreadyInRequestedMode
 */
bStatus_t timeservice_RegisterAppCBs( timeserviceCBs_t *appCallbacks )
{
  if ( appCallbacks )
  {
    timeservice_AppCBs = appCallbacks;

    return ( SUCCESS );
  }
  else
  {
    return ( bleAlreadyInRequestedMode );
  }
}


/*********************************************************************
 * @fn      timeservice_SetParameter
 *
 * @brief   Set a timeservice parameter.
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
bStatus_t timeservice_SetParameter( uint8 param, uint8 len, void *value )
{
  bStatus_t ret = SUCCESS;
  switch ( param )
  {
    case TIME_ENABLER:
      if ( len == TIME_ENABLER_LEN )
      {
        VOID osal_memcpy( &TIME_ENABLERValue, value, TIME_ENABLER_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case TIME:
      if ( len == TIME_LEN )
      {
        VOID osal_memcpy( TIMEValue, value, TIME_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case DATE:
      if ( len == DATE_LEN )
      {
        VOID osal_memcpy( DATEValue, value, DATE_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM:
      if ( len == ALARM_LEN )
      {
        VOID osal_memcpy( ALARMValue, value, ALARM_LEN );
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
 * @fn      timeservice_GetParameter
 *
 * @brief   Get a timeservice parameter.
 *
 * @param   param - Profile parameter ID
 * @param   value - pointer to data to put.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).
 *
 * @return  bStatus_t
 */
bStatus_t timeservice_GetParameter( uint8 param, void *value )
{
  bStatus_t ret = SUCCESS;
  switch ( param )
  {
    case TIME_ENABLER:
      VOID osal_memcpy( value, &TIME_ENABLERValue, TIME_ENABLER_LEN );
      break;

    case TIME:
      VOID osal_memcpy( value, TIMEValue, TIME_LEN );
      break;

    case DATE:
      VOID osal_memcpy( value, DATEValue, DATE_LEN );
      break;

    case ALARM:
      VOID osal_memcpy( value, ALARMValue, ALARM_LEN );
      break;

    default:
      ret = INVALIDPARAMETER;
      break;
  }

  return ( ret );
}

/*********************************************************************
 * @fn          timeservice_ReadAttrCB
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
static uint8 timeservice_ReadAttrCB( uint16 connHandle, gattAttribute_t *pAttr, 
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

      case TIME_ENABLER_UUID:
        *pLen = TIME_ENABLER_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, TIME_ENABLER_LEN );
        break;

      case TIME_UUID:
        *pLen = TIME_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, TIME_LEN );
        break;

      case DATE_UUID:
        *pLen = DATE_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, DATE_LEN );
        break;

      case ALARM_UUID:
        *pLen = ALARM_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_LEN );
        break;

      default:
        // Should never get here!
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
 * @fn      timeservice_WriteAttrCB
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
static bStatus_t timeservice_WriteAttrCB( uint16 connHandle, gattAttribute_t *pAttr,
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
      case TIME_ENABLER_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != TIME_ENABLER_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, TIME_ENABLER_LEN );
          notifyApp = TIME_ENABLER;
        }
        break;

      case TIME_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != TIME_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, TIME_LEN );
          notifyApp = TIME;
        }
        break;

      case DATE_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != DATE_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, DATE_LEN );
          notifyApp = DATE;
        }
        break;

      case ALARM_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_LEN );
          notifyApp = ALARM;
        }
        break;

      case GATT_CLIENT_CHAR_CFG_UUID:
        status = GATTServApp_ProcessCCCWriteReq( connHandle, pAttr, pValue, len,
                                                 offset, GATT_CLIENT_CFG_NOTIFY );
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

  // If a charactersitic value changed then callback function to notify application of change
  if ( (notifyApp != 0xFF ) && timeservice_AppCBs && timeservice_AppCBs->pfntimeserviceChange )
  {
    timeservice_AppCBs->pfntimeserviceChange( notifyApp );  
  }

  return ( status );
}

/*********************************************************************
 * @fn          timeservice_HandleConnStatusCB
 *
 * @brief       timeservice link status change handler function.
 *
 * @param       connHandle - connection handle
 * @param       changeType - type of change
 *
 * @return      none
 */
static void timeservice_HandleConnStatusCB( uint16 connHandle, uint8 changeType )
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
