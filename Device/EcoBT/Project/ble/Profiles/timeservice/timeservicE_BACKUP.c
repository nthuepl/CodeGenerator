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

// HOUR UUID: 0xFDF2
CONST uint8 HOURUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(HOUR_UUID), HI_UINT16(HOUR_UUID)
};

// MINUTE UUID: 0xFDF3
CONST uint8 MINUTEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(MINUTE_UUID), HI_UINT16(MINUTE_UUID)
};

// SECOND UUID: 0xFDF4
CONST uint8 SECONDUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(SECOND_UUID), HI_UINT16(SECOND_UUID)
};

// CENTURY UUID: 0xFDF5
CONST uint8 CENTURYUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(CENTURY_UUID), HI_UINT16(CENTURY_UUID)
};

// YEAR UUID: 0xFDF6
CONST uint8 YEARUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(YEAR_UUID), HI_UINT16(YEAR_UUID)
};

// MONTH UUID: 0xFDF7
CONST uint8 MONTHUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(MONTH_UUID), HI_UINT16(MONTH_UUID)
};

// DATE UUID: 0xFDF8
CONST uint8 DATEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(DATE_UUID), HI_UINT16(DATE_UUID)
};

// DAY UUID: 0xFDF9
CONST uint8 DAYUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(DAY_UUID), HI_UINT16(DAY_UUID)
};

// ALARM_MONTH UUID: 0xFDFA
CONST uint8 ALARM_MONTHUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_MONTH_UUID), HI_UINT16(ALARM_MONTH_UUID)
};

// ALARM_DATE UUID: 0xFDFB
CONST uint8 ALARM_DATEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_DATE_UUID), HI_UINT16(ALARM_DATE_UUID)
};

// ALARM_HOUR UUID: 0xFDFC
CONST uint8 ALARM_HOURUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_HOUR_UUID), HI_UINT16(ALARM_HOUR_UUID)
};

// ALARM_MINUTE UUID: 0xFDFD
CONST uint8 ALARM_MINUTEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_MINUTE_UUID), HI_UINT16(ALARM_MINUTE_UUID)
};

// ALARM_SECOND UUID: 0xFDFE
CONST uint8 ALARM_SECONDUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_SECOND_UUID), HI_UINT16(ALARM_SECOND_UUID)
};

// ALARM_REPEATMODE UUID: 0xFDFF
CONST uint8 ALARM_REPEATMODEUUID[ATT_BT_UUID_SIZE] =
{
  LO_UINT16(ALARM_REPEATMODE_UUID), HI_UINT16(ALARM_REPEATMODE_UUID)
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

// Profile HOUR Properties
static uint8 HOURProps = GATT_PROP_READ | GATT_PROP_WRITE;

// HOUR Value
static uint8 HOURValue = 0;// Profile HOUR User Description
static uint8 HOURUserDesp[5] = "hour\0";

// Profile MINUTE Properties
static uint8 MINUTEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// MINUTE Value
static uint8 MINUTEValue = 0;// Profile MINUTE User Description
static uint8 MINUTEUserDesp[7] = "minute\0";

// Profile SECOND Properties
static uint8 SECONDProps = GATT_PROP_READ | GATT_PROP_WRITE;

// SECOND Value
static uint8 SECONDValue = 0;// Profile SECOND User Description
static uint8 SECONDUserDesp[7] = "second\0";

// Profile CENTURY Properties
static uint8 CENTURYProps = GATT_PROP_READ | GATT_PROP_WRITE;

// CENTURY Value
static uint8 CENTURYValue = 0;// Profile CENTURY User Description
static uint8 CENTURYUserDesp[8] = "century\0";

// Profile YEAR Properties
static uint8 YEARProps = GATT_PROP_READ | GATT_PROP_WRITE;

// YEAR Value
static uint8 YEARValue = 0;// Profile YEAR User Description
static uint8 YEARUserDesp[5] = "year\0";

// Profile MONTH Properties
static uint8 MONTHProps = GATT_PROP_READ | GATT_PROP_WRITE;

// MONTH Value
static uint8 MONTHValue = 0;// Profile MONTH User Description
static uint8 MONTHUserDesp[6] = "month\0";

// Profile DATE Properties
static uint8 DATEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// DATE Value
static uint8 DATEValue = 0;// Profile DATE User Description
static uint8 DATEUserDesp[5] = "date\0";

// Profile DAY Properties
static uint8 DAYProps = GATT_PROP_READ | GATT_PROP_WRITE;

// DAY Value
static uint8 DAYValue = 0;// Profile DAY User Description
static uint8 DAYUserDesp[4] = "day\0";

// Profile ALARM_MONTH Properties
static uint8 ALARM_MONTHProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM_MONTH Value
static uint8 ALARM_MONTHValue = 0;// Profile ALARM_MONTH User Description
static uint8 ALARM_MONTHUserDesp[12] = "alarm_month\0";

// Profile ALARM_DATE Properties
static uint8 ALARM_DATEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM_DATE Value
static uint8 ALARM_DATEValue = 0;// Profile ALARM_DATE User Description
static uint8 ALARM_DATEUserDesp[11] = "alarm_date\0";

// Profile ALARM_HOUR Properties
static uint8 ALARM_HOURProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM_HOUR Value
static uint8 ALARM_HOURValue = 0;// Profile ALARM_HOUR User Description
static uint8 ALARM_HOURUserDesp[11] = "alarm_hour\0";

// Profile ALARM_MINUTE Properties
static uint8 ALARM_MINUTEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM_MINUTE Value
static uint8 ALARM_MINUTEValue = 0;// Profile ALARM_MINUTE User Description
static uint8 ALARM_MINUTEUserDesp[13] = "alarm_minute\0";

// Profile ALARM_SECOND Properties
static uint8 ALARM_SECONDProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM_SECOND Value
static uint8 ALARM_SECONDValue = 0;// Profile ALARM_SECOND User Description
static uint8 ALARM_SECONDUserDesp[13] = "alarm_second\0";

// Profile ALARM_REPEATMODE Properties
static uint8 ALARM_REPEATMODEProps = GATT_PROP_READ | GATT_PROP_WRITE;

// ALARM_REPEATMODE Value
static uint8 ALARM_REPEATMODEValue = 0;// Profile ALARM_REPEATMODE User Description
static uint8 ALARM_REPEATMODEUserDesp[17] = "alarm_repeatmode\0";

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

    // HOUR Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &HOURProps
    },

      // HOUR Value
      {
        { ATT_BT_UUID_SIZE, HOURUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &HOURValue
      },

      // HOUR User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        HOURUserDesp
      },

    // MINUTE Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &MINUTEProps
    },

      // MINUTE Value
      {
        { ATT_BT_UUID_SIZE, MINUTEUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &MINUTEValue
      },

      // MINUTE User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        MINUTEUserDesp
      },

    // SECOND Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &SECONDProps
    },

      // SECOND Value
      {
        { ATT_BT_UUID_SIZE, SECONDUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &SECONDValue
      },

      // SECOND User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        SECONDUserDesp
      },

    // CENTURY Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &CENTURYProps
    },

      // CENTURY Value
      {
        { ATT_BT_UUID_SIZE, CENTURYUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &CENTURYValue
      },

      // CENTURY User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        CENTURYUserDesp
      },

    // YEAR Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &YEARProps
    },

      // YEAR Value
      {
        { ATT_BT_UUID_SIZE, YEARUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &YEARValue
      },

      // YEAR User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        YEARUserDesp
      },

    // MONTH Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &MONTHProps
    },

      // MONTH Value
      {
        { ATT_BT_UUID_SIZE, MONTHUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &MONTHValue
      },

      // MONTH User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        MONTHUserDesp
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
        &DATEValue
      },

      // DATE User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        DATEUserDesp
      },

    // DAY Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &DAYProps
    },

      // DAY Value
      {
        { ATT_BT_UUID_SIZE, DAYUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &DAYValue
      },

      // DAY User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        DAYUserDesp
      },

    // ALARM_MONTH Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARM_MONTHProps
    },

      // ALARM_MONTH Value
      {
        { ATT_BT_UUID_SIZE, ALARM_MONTHUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &ALARM_MONTHValue
      },

      // ALARM_MONTH User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARM_MONTHUserDesp
      },

    // ALARM_DATE Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARM_DATEProps
    },

      // ALARM_DATE Value
      {
        { ATT_BT_UUID_SIZE, ALARM_DATEUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &ALARM_DATEValue
      },

      // ALARM_DATE User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARM_DATEUserDesp
      },

    // ALARM_HOUR Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARM_HOURProps
    },

      // ALARM_HOUR Value
      {
        { ATT_BT_UUID_SIZE, ALARM_HOURUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &ALARM_HOURValue
      },

      // ALARM_HOUR User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARM_HOURUserDesp
      },

    // ALARM_MINUTE Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARM_MINUTEProps
    },

      // ALARM_MINUTE Value
      {
        { ATT_BT_UUID_SIZE, ALARM_MINUTEUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &ALARM_MINUTEValue
      },

      // ALARM_MINUTE User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARM_MINUTEUserDesp
      },

    // ALARM_SECOND Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARM_SECONDProps
    },

      // ALARM_SECOND Value
      {
        { ATT_BT_UUID_SIZE, ALARM_SECONDUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &ALARM_SECONDValue
      },

      // ALARM_SECOND User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARM_SECONDUserDesp
      },

    // ALARM_REPEATMODE Declaration
    {
      { ATT_BT_UUID_SIZE, characterUUID },
      GATT_PERMIT_READ,
      0,
      &ALARM_REPEATMODEProps
    },

      // ALARM_REPEATMODE Value
      {
        { ATT_BT_UUID_SIZE, ALARM_REPEATMODEUUID },
        GATT_PERMIT_READ | GATT_PERMIT_WRITE,
        0,
        &ALARM_REPEATMODEValue
      },

      // ALARM_REPEATMODE User Description
      {
        { ATT_BT_UUID_SIZE, charUserDescUUID },
        GATT_PERMIT_READ, 
        0,
        ALARM_REPEATMODEUserDesp
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

    case HOUR:
      if ( len == HOUR_LEN )
      {
        VOID osal_memcpy( &HOURValue, value, HOUR_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case MINUTE:
      if ( len == MINUTE_LEN )
      {
        VOID osal_memcpy( &MINUTEValue, value, MINUTE_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case SECOND:
      if ( len == SECOND_LEN )
      {
        VOID osal_memcpy( &SECONDValue, value, SECOND_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case CENTURY:
      if ( len == CENTURY_LEN )
      {
        VOID osal_memcpy( &CENTURYValue, value, CENTURY_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case YEAR:
      if ( len == YEAR_LEN )
      {
        VOID osal_memcpy( &YEARValue, value, YEAR_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case MONTH:
      if ( len == MONTH_LEN )
      {
        VOID osal_memcpy( &MONTHValue, value, MONTH_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case DATE:
      if ( len == DATE_LEN )
      {
        VOID osal_memcpy( &DATEValue, value, DATE_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case DAY:
      if ( len == DAY_LEN )
      {
        VOID osal_memcpy( &DAYValue, value, DAY_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM_MONTH:
      if ( len == ALARM_MONTH_LEN )
      {
        VOID osal_memcpy( &ALARM_MONTHValue, value, ALARM_MONTH_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM_DATE:
      if ( len == ALARM_DATE_LEN )
      {
        VOID osal_memcpy( &ALARM_DATEValue, value, ALARM_DATE_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM_HOUR:
      if ( len == ALARM_HOUR_LEN )
      {
        VOID osal_memcpy( &ALARM_HOURValue, value, ALARM_HOUR_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM_MINUTE:
      if ( len == ALARM_MINUTE_LEN )
      {
        VOID osal_memcpy( &ALARM_MINUTEValue, value, ALARM_MINUTE_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM_SECOND:
      if ( len == ALARM_SECOND_LEN )
      {
        VOID osal_memcpy( &ALARM_SECONDValue, value, ALARM_SECOND_LEN );
      }
      else
      {
        ret = bleInvalidRange;
      }
      break;

    case ALARM_REPEATMODE:
      if ( len == ALARM_REPEATMODE_LEN )
      {
        VOID osal_memcpy( &ALARM_REPEATMODEValue, value, ALARM_REPEATMODE_LEN );
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

    case HOUR:
      VOID osal_memcpy( value, &HOURValue, HOUR_LEN );
      break;

    case MINUTE:
      VOID osal_memcpy( value, &MINUTEValue, MINUTE_LEN );
      break;

    case SECOND:
      VOID osal_memcpy( value, &SECONDValue, SECOND_LEN );
      break;

    case CENTURY:
      VOID osal_memcpy( value, &CENTURYValue, CENTURY_LEN );
      break;

    case YEAR:
      VOID osal_memcpy( value, &YEARValue, YEAR_LEN );
      break;

    case MONTH:
      VOID osal_memcpy( value, &MONTHValue, MONTH_LEN );
      break;

    case DATE:
      VOID osal_memcpy( value, &DATEValue, DATE_LEN );
      break;

    case DAY:
      VOID osal_memcpy( value, &DAYValue, DAY_LEN );
      break;

    case ALARM_MONTH:
      VOID osal_memcpy( value, &ALARM_MONTHValue, ALARM_MONTH_LEN );
      break;

    case ALARM_DATE:
      VOID osal_memcpy( value, &ALARM_DATEValue, ALARM_DATE_LEN );
      break;

    case ALARM_HOUR:
      VOID osal_memcpy( value, &ALARM_HOURValue, ALARM_HOUR_LEN );
      break;

    case ALARM_MINUTE:
      VOID osal_memcpy( value, &ALARM_MINUTEValue, ALARM_MINUTE_LEN );
      break;

    case ALARM_SECOND:
      VOID osal_memcpy( value, &ALARM_SECONDValue, ALARM_SECOND_LEN );
      break;

    case ALARM_REPEATMODE:
      VOID osal_memcpy( value, &ALARM_REPEATMODEValue, ALARM_REPEATMODE_LEN );
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

      case HOUR_UUID:
        *pLen = HOUR_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, HOUR_LEN );
        break;

      case MINUTE_UUID:
        *pLen = MINUTE_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, MINUTE_LEN );
        break;

      case SECOND_UUID:
        *pLen = SECOND_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, SECOND_LEN );
        break;

      case CENTURY_UUID:
        *pLen = CENTURY_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, CENTURY_LEN );
        break;

      case YEAR_UUID:
        *pLen = YEAR_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, YEAR_LEN );
        break;

      case MONTH_UUID:
        *pLen = MONTH_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, MONTH_LEN );
        break;

      case DATE_UUID:
        *pLen = DATE_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, DATE_LEN );
        break;

      case DAY_UUID:
        *pLen = DAY_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, DAY_LEN );
        break;

      case ALARM_MONTH_UUID:
        *pLen = ALARM_MONTH_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_MONTH_LEN );
        break;

      case ALARM_DATE_UUID:
        *pLen = ALARM_DATE_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_DATE_LEN );
        break;

      case ALARM_HOUR_UUID:
        *pLen = ALARM_HOUR_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_HOUR_LEN );
        break;

      case ALARM_MINUTE_UUID:
        *pLen = ALARM_MINUTE_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_MINUTE_LEN );
        break;

      case ALARM_SECOND_UUID:
        *pLen = ALARM_SECOND_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_SECOND_LEN );
        break;

      case ALARM_REPEATMODE_UUID:
        *pLen = ALARM_REPEATMODE_LEN;
        VOID osal_memcpy( pValue, pAttr->pValue, ALARM_REPEATMODE_LEN );
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

      case HOUR_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != HOUR_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, HOUR_LEN );
          notifyApp = HOUR;
        }
        break;

      case MINUTE_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != MINUTE_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, MINUTE_LEN );
          notifyApp = MINUTE;
        }
        break;

      case SECOND_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != SECOND_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, SECOND_LEN );
          notifyApp = SECOND;
        }
        break;

      case CENTURY_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != CENTURY_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, CENTURY_LEN );
          notifyApp = CENTURY;
        }
        break;

      case YEAR_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != YEAR_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, YEAR_LEN );
          notifyApp = YEAR;
        }
        break;

      case MONTH_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != MONTH_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, MONTH_LEN );
          notifyApp = MONTH;
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

      case DAY_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != DAY_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, DAY_LEN );
          notifyApp = DAY;
        }
        break;

      case ALARM_MONTH_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_MONTH_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_MONTH_LEN );
          notifyApp = ALARM_MONTH;
        }
        break;

      case ALARM_DATE_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_DATE_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_DATE_LEN );
          notifyApp = ALARM_DATE;
        }
        break;

      case ALARM_HOUR_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_HOUR_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_HOUR_LEN );
          notifyApp = ALARM_HOUR;
        }
        break;

      case ALARM_MINUTE_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_MINUTE_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_MINUTE_LEN );
          notifyApp = ALARM_MINUTE;
        }
        break;

      case ALARM_SECOND_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_SECOND_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_SECOND_LEN );
          notifyApp = ALARM_SECOND;
        }
        break;

      case ALARM_REPEATMODE_UUID:
        //Validate the value
        // Make sure it's not a blob oper
        if ( offset == 0 )
        {
          if ( len != ALARM_REPEATMODE_LEN )
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
          VOID osal_memcpy( pAttr->pValue, pValue, ALARM_REPEATMODE_LEN );
          notifyApp = ALARM_REPEATMODE;
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
