/**
  @headerfile:    s2i_gapbondmgr.c
  $Date: 2011-03-03 15:46:41 -0800 (Thu, 03 Mar 2011) $
  $Revision: 12 $

*/

#include "gapbondmgr.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro for either CC2540 or CC2541"
#endif
  
  


/*-------------------------------------------------------------------
 * API FUNCTIONS 
 */

/**
 * @defgroup GAPROLES_BONDMGR_API GAP Bond Manager API Functions
 * 
 * @{
 */
  
/**
 * @brief       Set a GAP Bond Manager parameter.
 *
 *  NOTE: You can call this function with a GAP Parameter ID and it will set the 
 *        GAP Parameter.  GAP Parameters are defined in (gap.h).  Also, 
 *        the "len" field must be set to the size of a "uint16" and the
 *        "pValue" field must point to a "uint16".
 *
 * @param       param - Profile parameter ID: @ref GAPBOND_PROFILE_PARAMETERS
 * @param       len - length of data to write
 * @param       pValue - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 *
 * @return      SUCCESS or INVALIDPARAMETER (invalid paramID)
 */
bStatus_t GAPBondMgr_SetParameter( uint16 param, uint8 len, __xdata void *pValue ) {
	s2i_call_u16_u8_p(MAP_GAPBondMgr_SetParameter); // was 0x81B | 0x9DC
	s2i_ret_u8();
}
  
/**
 * @brief       Get a GAP Bond Manager parameter.
 *
 *  NOTE: You can call this function with a GAP Parameter ID and it will get a 
 *        GAP Parameter.  GAP Parameters are defined in (gap.h).  Also, the
 *        "pValue" field must point to a "uint16".
 *
 * @param       param - Profile parameter ID: @ref GAPBOND_PROFILE_PARAMETERS
 * @param       pValue - pointer to location to get the value.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 *
 * @return      SUCCESS or INVALIDPARAMETER (invalid paramID)
 */
bStatus_t GAPBondMgr_GetParameter( uint16 param, __xdata void *pValue ) {
#ifdef CC2540
	// s2i_call_u16_p(address);
#elif defined(CC2541)
	// s2i_call_u16_p(address);
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
	s2i_ret_u8();
}

/**
 * @brief       Notify the Bond Manager that a connection has been made.
 *       
 *   NOTE:      The GAP Peripheral/Central Role profile will
 *              call this function, if they are included in the project.
 *
 * @param       addrType - device's address type. Reference GAP_ADDR_TYPE_DEFINES in gap.h
 * @param       pDevAddr - device's address
 * @param       connHandle - connection handle
 * @param       role - master or slave role.  Reference GAP_PROFILE_ROLE_DEFINES in gap.h
 *
 * @return      SUCCESS, otherwise failure
 */
bStatus_t GAPBondMgr_LinkEst( uint8 addrType, __xdata uint8 *pDevAddr, uint16 connHandle, uint8 role ) {
	s2i_call_u8_p_u16_u8(MAP_GAPBondMgr_LinkEst); // was 0x821 | 0x9E2
	s2i_ret_u8();
}

/**
 * @brief       Resolve an address from bonding information.
 *
 * @param       addrType - device's address type. Reference GAP_ADDR_TYPE_DEFINES in gap.h
 * @param       pDevAddr - device's address
 * @param       pResolvedAddr - pointer to buffer to put the resolved address
 *
 * @return      bonding index (0 - (GAP_BONDINGS_MAX-1) if found,
 *              GAP_BONDINGS_MAX if not found
 */
uint8 GAPBondMgr_ResolveAddr( uint8 addrType, __xdata uint8 *pDevAddr, __xdata uint8 *pResolvedAddr ) {
	s2i_call_u8_p_p(MAP_GAPBondMgr_ResolveAddress); // was 0x827 | 0x9E8
	s2i_ret_u8();
}

/**
 * @brief       Set/clear the service change indication in a bond record.
 * 
 * @param       connectionHandle - connection handle of the connected device or 0xFFFF
 *                                 if all devices in database.
 * @param       setParam - TRUE to set the service change indication, FALSE to clear it.
 *
 * @return      SUCCESS - bond record found and changed,<BR>
 *              bleNoResources - bond record not found (for 0xFFFF connectionHandle),<BR>
 *              bleNotConnected - connection not found - connectionHandle is invalid (for non-0xFFFF connectionHandle).
 */
bStatus_t GAPBondMgr_ServiceChangeInd( uint16 connectionHandle, uint8 setParam ) {
	s2i_call_u16_u8(MAP_GAPBondMgr_ServiceChangeInd); // was 0x82D | 0x9EE
	s2i_ret_u8();
}


/**
 * @brief       Update the Characteristic Configuration in a bond record.
 * 
 * @param       connectionHandle - connection handle of the connected device or 0xFFFF
 *                                 if all devices in database.
 * @param       attrHandle - attribute handle.
 * @param       value - characteristic configuration value.
 *
 * @return      SUCCESS - bond record found and changed,<BR>
 *              bleNoResources - bond record not found (for 0xFFFF connectionHandle),<BR>
 *              bleNotConnected - connection not found - connectionHandle is invalid (for non-0xFFFF connectionHandle).
 */
bStatus_t GAPBondMgr_UpdateCharCfg( uint16 connectionHandle, uint16 attrHandle, uint16 value ) {
	s2i_call_u16_u16_u16(MAP_GAPBondMgr_UpdateCharCfg); // was 0x833 | 0x9F4
	s2i_ret_u8();
}

/**
 * @brief       Register callback functions with the bond manager.
 * 
 *   NOTE:      There is no need to register a passcode callback function
 *              if the passcode will be handled with the GAPBOND_DEFAULT_PASSCODE parameter.
 *
 * @param       pCB - pointer to callback function structure.
 *
 * @return      none
 */
void GAPBondMgr_Register(__xdata gapBondCBs_t *pCB ) {
	s2i_call_p(MAP_GAPBondMgr_Register); // was 0x839 | 0x9FA
}

/**
 * @brief       Respond to a passcode request.
 * 
 * @param       connectionHandle - connection handle of the connected device or 0xFFFF
 *                                 if all devices in database.
 * @param       status - SUCCESS if passcode is available, otherwise see @ref SMP_PAIRING_FAILED_DEFINES.
 * @param       passcode - integer value containing the passcode.
 *
 * @return      SUCCESS - bond record found and changed,<BR>
 *              bleIncorrectMode - Link not found.
 */
bStatus_t GAPBondMgr_PasscodeRsp( uint16 connectionHandle, uint8 status, uint32 passcode ) {
#ifdef CC2540
//	s2i_call_u16_u8_u32(address);
#elif defined(CC2541)
//	s2i_call_u16_u8_u32(address);
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
	s2i_ret_u8();
}

/**
 * @brief       This is a bypass mechanism to allow the bond manager to process
 *              GAP messages.  
 * 
 *   NOTE:      This is an advanced feature and shouldn't be called unless
 *              the normal GAP Bond Manager task ID registration is overridden.
 *
 * @param       pMsg - GAP event message
 *
 * @return      none
 */
void GAPBondMgr_ProcessGAPMsg(__xdata gapEventHdr_t *pMsg ) {
	s2i_call_p(MAP_GAPBondMgr_ProcessGAPMsg); // was 0x83F | 0xA00
}

/**
 * @brief       This function will check the length of a Bond Manager NV Item.  
 * 
 * @param       id - NV ID.
 * @param       len - lengths in bytes of item.
 *
 * @return      SUCCESS or FAILURE
 */
uint8 GAPBondMgr_CheckNVLen( uint8 id, uint8 len ) {
#ifdef MAP_GAPBondMgr_CheckNVLen
	s2i_call_u8_u8(MAP_GAPBondMgr_CheckNVLen);
#endif
	s2i_ret_u8();
}

/**
 * @} End GAPROLES_BONDMGR_API
 */   



/*-------------------------------------------------------------------
 * TASK FUNCTIONS - Don't call these. These are system functions.
 */

/**
 * @internal
 *
 * @brief       Initialization function for the GAP Bond Manager Task.
 *          This is called during initialization and should contain
 *          any application specific initialization (ie. hardware
 *          initialization/setup, table initialization, power up
 *          notificaiton ... ).
 *
 * @param       the ID assigned by OSAL.  This ID should be
 *                    used to send messages and set timers.
 *
 * @return      void
 */
// extern void GAPBondMgr_Init( uint8 task_id );

/**
 * @internal
 *
 * @brief       GAP Bond Manager Task event processor.  
 *          This function is called to process all events for the task.
 *          Events include timers, messages and any other user defined 
 *          events.
 *
 * @param   task_id  - The OSAL assigned task ID.
 * @param   events - events to process.  This is a bit map and can
 *                   contain more than one event.
 *
 * @return      events not processed
 */
// extern uint16 GAPBondMgr_ProcessEvent( uint8 task_id, uint16 events );
