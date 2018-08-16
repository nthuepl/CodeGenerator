/**************************************************************************************************
  Filename:       s2i_simpleGATTprofile.c
  Revised:        $Date: 2010-08-06 08:56:11 -0700 (Fri, 06 Aug 2010) $
  Revision:       $Revision: 23333 $

  Description:    This file contains the Simple GATT profile sample GATT service 
                  profile for use with the BLE sample application.

	PC140510: this is the binding version of the simpleGATTprofile in that
	it makes available the API calls provided by simpleGATTprofile, so
	that the user can write code in SDCC to register stuff.  This means
	there should be a version of the code (mostly based on the commented
	out parts, and mostly static functions and data structures) that can
	then make API calls to this file, so that the user can customize
	this simple GATT profile.  The callback should also be moved, except
	someone must generate a stub in IAR so that it can put in the relay,
	and the relay address is what should be registered.

**************************************************************************************************/

/*********************************************************************
 * INCLUDES
 */

#include "sdcc2iar.h"
#include "iar2sdcc.h"

#include "bcomdef.h"
#include "OSAL.h"
#include "linkdb.h"
#include "att.h"
#include "gatt.h"
#include "gatt_uuid.h"
#include "gattservapp.h"
#include "gapbondmgr.h"

#include "simpleGATTprofile.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro for either CC2540 or CC2541"
#endif
  
  

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
// Simple GATT Profile Service UUID: 0xFFF0
// CONST uint8 simpleProfileServUUID[ATT_BT_UUID_SIZE] =
// { 
//   LO_UINT16(SIMPLEPROFILE_SERV_UUID), HI_UINT16(SIMPLEPROFILE_SERV_UUID)
// };

// Characteristic 1 UUID: 0xFFF1
// CONST uint8 simpleProfilechar1UUID[ATT_BT_UUID_SIZE] =
// { 
//   LO_UINT16(SIMPLEPROFILE_CHAR1_UUID), HI_UINT16(SIMPLEPROFILE_CHAR1_UUID)
// };

// Characteristic 2 UUID: 0xFFF2
// CONST uint8 simpleProfilechar2UUID[ATT_BT_UUID_SIZE] =
// { 
//   LO_UINT16(SIMPLEPROFILE_CHAR2_UUID), HI_UINT16(SIMPLEPROFILE_CHAR2_UUID)
// };

// Characteristic 3 UUID: 0xFFF3
// CONST uint8 simpleProfilechar3UUID[ATT_BT_UUID_SIZE] =
// { 
//   LO_UINT16(SIMPLEPROFILE_CHAR3_UUID), HI_UINT16(SIMPLEPROFILE_CHAR3_UUID)
// };

// Characteristic 4 UUID: 0xFFF4
// CONST uint8 simpleProfilechar4UUID[ATT_BT_UUID_SIZE] =
// { 
//   LO_UINT16(SIMPLEPROFILE_CHAR4_UUID), HI_UINT16(SIMPLEPROFILE_CHAR4_UUID)
// };

// Characteristic 5 UUID: 0xFFF5
// extern CONST uint8 simpleProfilechar5UUID[ATT_BT_UUID_SIZE] =
// { 
//   LO_UINT16(SIMPLEPROFILE_CHAR5_UUID), HI_UINT16(SIMPLEPROFILE_CHAR5_UUID)
// };

/*********************************************************************
 * EXTERNAL VARIABLES
 */

/*********************************************************************
 * EXTERNAL FUNCTIONS
 */

/*********************************************************************
 * LOCAL VARIABLES
 */

// static simpleProfileCBs_t *simpleProfile_AppCBs = NULL;

/*********************************************************************
 * Profile Attributes - variables
 */

// Simple Profile Service attribute
// static CONST gattAttrType_t simpleProfileService = { ATT_BT_UUID_SIZE, simpleProfileServUUID };


// Simple Profile Characteristic 1 Properties
// static uint8 simpleProfileChar1Props = GATT_PROP_READ | GATT_PROP_WRITE;

// Characteristic 1 Value
// static uint8 simpleProfileChar1 = 0;

// Simple Profile Characteristic 1 User Description
// static uint8 simpleProfileChar1UserDesp[17] = "Characteristic 1\0";


// Simple Profile Characteristic 2 Properties
// static uint8 simpleProfileChar2Props = GATT_PROP_READ;

// Characteristic 2 Value
// static uint8 simpleProfileChar2 = 0;

// Simple Profile Characteristic 2 User Description
// static uint8 simpleProfileChar2UserDesp[17] = "Characteristic 2\0";


// Simple Profile Characteristic 3 Properties
// static uint8 simpleProfileChar3Props = GATT_PROP_WRITE;

// Characteristic 3 Value
// static uint8 simpleProfileChar3 = 0;

// Simple Profile Characteristic 3 User Description
// static uint8 simpleProfileChar3UserDesp[17] = "Characteristic 3\0";


// Simple Profile Characteristic 4 Properties
// static uint8 simpleProfileChar4Props = GATT_PROP_NOTIFY;

// Characteristic 4 Value
// static uint8 simpleProfileChar4 = 0;

// Simple Profile Characteristic 4 Configuration Each client has its own
// instantiation of the Client Characteristic Configuration. Reads of the
// Client Characteristic Configuration only shows the configuration for
// that client and writes only affect the configuration of that client.
// static gattCharCfg_t simpleProfileChar4Config[GATT_MAX_NUM_CONN];
                                        
// Simple Profile Characteristic 4 User Description
// static uint8 simpleProfileChar4UserDesp[17] = "Characteristic 4\0";


// Simple Profile Characteristic 5 Properties
// static uint8 simpleProfileChar5Props = GATT_PROP_READ;

// Characteristic 5 Value
// static uint8 simpleProfileChar5[SIMPLEPROFILE_CHAR5_LEN] = { 0, 0, 0, 0, 0 };

// Simple Profile Characteristic 5 User Description
// static uint8 simpleProfileChar5UserDesp[17] = "Characteristic 5\0";


/*********************************************************************
 * Profile Attributes - Table
 */

// static __xdata gattAttribute_t simpleProfileAttrTbl[SERVAPP_NUM_ATTR_SUPPORTED] = 
// {
//  // Simple Profile Service
//  { 
//    { ATT_BT_UUID_SIZE, primaryServiceUUID }, /* type */
//    GATT_PERMIT_READ,                         /* permissions */
//    0,                                        /* handle */
//    (__xdata uint8 *)&simpleProfileService            /* pValue */
//  },
//
//    // Characteristic 1 Declaration
//    { 
//      { ATT_BT_UUID_SIZE, characterUUID },
//      GATT_PERMIT_READ, 
//      0,
//      (__xdata uint8*)&simpleProfileChar1Props 
//    },
//
//      // Characteristic Value 1
//      { 
//        { ATT_BT_UUID_SIZE, simpleProfilechar1UUID },
//        GATT_PERMIT_READ | GATT_PERMIT_WRITE, 
//        0, 
//        (__xdata uint8*)&simpleProfileChar1 
//      },
//
//      // Characteristic 1 User Description
//      { 
//        { ATT_BT_UUID_SIZE, charUserDescUUID },
//        GATT_PERMIT_READ, 
//        0, 
//        simpleProfileChar1UserDesp 
//      },      
//
//    // Characteristic 2 Declaration
//    { 
//      { ATT_BT_UUID_SIZE, characterUUID },
//      GATT_PERMIT_READ, 
//      0,
//      &simpleProfileChar2Props 
//    },
//
//      // Characteristic Value 2
//      { 
//        { ATT_BT_UUID_SIZE, simpleProfilechar2UUID },
//        GATT_PERMIT_READ, 
//        0, 
//        &simpleProfileChar2 
//      },
//
//      // Characteristic 2 User Description
//      { 
//        { ATT_BT_UUID_SIZE, charUserDescUUID },
//        GATT_PERMIT_READ, 
//        0, 
//        simpleProfileChar2UserDesp 
//      },           
//      
//    // Characteristic 3 Declaration
//    { 
//      { ATT_BT_UUID_SIZE, characterUUID },
//      GATT_PERMIT_READ, 
//      0,
//      &simpleProfileChar3Props 
//    },
//
//      // Characteristic Value 3
//      { 
//        { ATT_BT_UUID_SIZE, simpleProfilechar3UUID },
//        GATT_PERMIT_WRITE, 
//        0, 
//        &simpleProfileChar3 
//      },
//
//      // Characteristic 3 User Description
//      { 
//        { ATT_BT_UUID_SIZE, charUserDescUUID },
//        GATT_PERMIT_READ, 
//        0, 
//        simpleProfileChar3UserDesp 
//      },
//
//    // Characteristic 4 Declaration
//    { 
//      { ATT_BT_UUID_SIZE, characterUUID },
//      GATT_PERMIT_READ, 
//      0,
//      &simpleProfileChar4Props 
//    },
//
//      // Characteristic Value 4
//      { 
//        { ATT_BT_UUID_SIZE, simpleProfilechar4UUID },
//        0, 
//        0, 
//        &simpleProfileChar4 
//      },
//
//      // Characteristic 4 configuration
//      { 
//        { ATT_BT_UUID_SIZE, clientCharCfgUUID },
//        GATT_PERMIT_READ | GATT_PERMIT_WRITE, 
//        0, 
//        (__xdata uint8 *)simpleProfileChar4Config 
//      },
//      
//      // Characteristic 4 User Description
//      { 
//        { ATT_BT_UUID_SIZE, charUserDescUUID },
//        GATT_PERMIT_READ, 
//        0, 
//        simpleProfileChar4UserDesp 
//      },
//      
//    // Characteristic 5 Declaration
//    { 
//      { ATT_BT_UUID_SIZE, characterUUID },
//      GATT_PERMIT_READ, 
//      0,
//      &simpleProfileChar5Props 
//    },
//
//      // Characteristic Value 5
//      { 
//        { ATT_BT_UUID_SIZE, simpleProfilechar5UUID },
//        GATT_PERMIT_AUTHEN_READ, 
//        0, 
//        simpleProfileChar5 
//      },
//
//      // Characteristic 5 User Description
//      { 
//        { ATT_BT_UUID_SIZE, charUserDescUUID },
//        GATT_PERMIT_READ, 
//        0, 
//        simpleProfileChar5UserDesp 
//      },
//
//
//};


/*********************************************************************
 * LOCAL FUNCTIONS
 */

static uint8 simpleProfile_ReadAttrCB( uint16 connHandle, __xdata
		gattAttribute_t *pAttr, __xdata uint8 *pValue, __xdata uint8 *pLen,
		uint16 offset, uint8 maxLen );

static bStatus_t simpleProfile_WriteAttrCB( uint16 connHandle, __xdata
		gattAttribute_t *pAttr, __xdata uint8 *pValue, uint8 len, uint16
		offset );

static void simpleProfile_HandleConnStatusCB( uint16 connHandle, uint8
		changeType );


/*********************************************************************
 * PROFILE CALLBACKS
 */
// Simple Profile Service Callbacks
// CONST gattServiceCBs_t simpleProfileCBs =
// {
//   simpleProfile_ReadAttrCB,  // Read callback function pointer
//   simpleProfile_WriteAttrCB, // Write callback function pointer
//   NULL                       // Authorization callback function pointer
// };

/*********************************************************************
 * PUBLIC FUNCTIONS
 */

/*********************************************************************
 * @fn      SimpleProfile_AddService
 *
 * @brief   Initializes the Simple Profile service by registering
 *          GATT attributes with the GATT server.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  Success or Failure
 */
bStatus_t SimpleProfile_AddService( uint32 services )
{
	s2i_call_u32(MAP_SimpleProfile_AddService); // was 0xA31 | 0xC16
	s2i_ret_u8();
}


/*********************************************************************
 * @fn      SimpleProfile_RegisterAppCBs
 *
 * @brief   Registers the application callback function. Only call 
 *          this function once.
 *
 * @param   callbacks - pointer to application callbacks.
 *
 * @return  SUCCESS or bleAlreadyInRequestedMode
 */
bStatus_t SimpleProfile_RegisterAppCBs(/*__xdata*/ simpleProfileCBs_t *appCallbacks )
{
	s2i_call_p(MAP_SimpleProfile_RegisterAppCBs); // was 0xA37 | 0xC1C
	s2i_ret_u8();
}
  

/*********************************************************************
 * @fn      SimpleProfile_SetParameter
 *
 * @brief   Set a Simple Profile parameter.
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

bStatus_t SimpleProfile_SetParameter( uint8 param, uint8 len, 
		__xdata void *value )
{
	s2i_call_u8_u8_p(MAP_SimpleProfile_SetParameter); // was 0xA3D | 0xC22
  s2i_ret_u8();
}

/*********************************************************************
 * @fn      SimpleProfile_GetParameter
 *
 * @brief   Get a Simple Profile parameter.
 *
 * @param   param - Profile parameter ID
 * @param   value - pointer to data to put.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 *
 * @return  bStatus_t
 */
bStatus_t SimpleProfile_GetParameter( uint8 param, __xdata void *value )
{
	s2i_call_u8_p(MAP_SimpleProfile_GetParameter); // was 0xA43 | 0xC28
  s2i_ret_u8();
}

/*********************************************************************
 * PC140508: this is a callback function to be registered.
 * It was declared static, it should have the type signature as here.
 *
 * This is invoked by IAR code, so it should be adapted using
 * iar2sdcc.h macros.
 *
 * @fn          simpleProfile_ReadAttrCB
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

static uint8 simpleProfile_ReadAttrCB( uint16 connHandle, __xdata
		gattAttribute_t *pAttr, __xdata uint8 *pValue, __xdata uint8 *pLen,
		uint16 offset, uint8 maxLen )
{

	i2s_call_u16_p_p_p_u16_u8();
	// user's own code here!!
	i2s_exit_u16_p_p_p_u16_u8();
  s2i_ret_u8();
}

/*********************************************************************
 * @fn      simpleProfile_WriteAttrCB
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

static bStatus_t simpleProfile_WriteAttrCB( uint16 connHandle, __xdata
		gattAttribute_t *pAttr, __xdata uint8 *pValue, uint8 len, uint16
		offset )
{
	i2s_call_u16_p_p_u8_u16();
	// user code here
	i2s_exit_u16_p_p_u8_u16();
	i2s_ret_u8();
}

static void simpleProfile_HandleConnStatusCB( uint16 connHandle, uint8
		changeType )
{ 
	i2s_call_u16_u8();

	// user code here
	i2s_exit_u16_u8();
}


/*********************************************************************
*********************************************************************/
