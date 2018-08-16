/**
 * s2i_gattservapp.c
 *
 * This is the binding file for gattservapp.h.
 * It is part of the BLE stack for 
 * - GATT service registration (attr list, call back functions)
 * - GATT service deregistration
 * - GATT service addition
 * - GATT service deletion
 *
 * The firmware is part of BLE stack provided in binary only, 
 * but it is not available in source form. But we can still
 * construct this binding layer to make calls -- but we need to make
 * sure that the calling conventions are matched in both ways.

**************************************************************************************************/

#include "gattservapp.h"
#include "sdcc2iar.h"
#include "iar2sdcc.h" // for converting callbacks
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro for either CC2540 or CC2541"
#endif

/**
 * @brief   Callback function prototype to read an attribute value.
 *
 * @param   connHandle - connection request was received on
 * @param   pAttr - pointer to attribute
 * @param   pValue - pointer to data to be read (to be returned)
 * @param   pLen - length of data (to be returned)
 * @param   offset - offset of the first octet to be read
 * @param   maxLen - maximum length of data to be read
 *
 * @return  SUCCESS: Read was successfully.<BR>
 *          Error, otherwise: ref ATT_ERR_CODE_DEFINES.<BR>
 */

// function of the following callback type are of type
// *pfnGATTReadAttrCB_t
// put here for illustration purpose, and maybe it should be
// pre-allocated for the purpose of generating the relay.

bStatus_t GattReadAttrCB( uint16 connHandle, gattAttribute_t *pAttr,
		uint8 *pValue, uint8 *pLen, uint16 offset, uint8 maxLen ) {
	/* need to convert type from iar2sdcc.  */
	i2s_call_u16_p_p_p_u16_u8();
	// the code here 
	i2s_exit_u16_p_p_p_u16_u8();
	i2s_ret_u8();
}

/**
 * @brief   Callback function prototype to write an attribute value.
 *
 * @param   connHandle - connection request was received on
 * @param   pAttr - pointer to attribute
 * @param   pValue - pointer to data to be written
 * @param   pLen - length of data
 * @param   offset - offset of the first octet to be written
 *
 * @return  SUCCESS: Write was successfully.<BR>
 *          Error, otherwise: ref ATT_ERR_CODE_DEFINES.<BR>
 */
// function of the following callback type are of type
// *pfnGATTWriteAttrCB_t
// put here for illustration purpose, and maybe it should be
// pre-allocated for the purpose of generating the relay.
bStatus_t GATTWriteAttrCB( uint16 connHandle, __xdata gattAttribute_t *pAttr,
                                           __xdata uint8 *pValue, uint8 len, uint16 offset ) {
		i2s_call_u16_p_p_u8_u16();
		// user code here
		i2s_exit_u16_p_p_u8_u16();
}
/**
 * @brief   Callback function prototype to authorize a Read or Write operation
 *          on a given attribute.
 *
 * @param   connHandle - connection request was received on
 * @param   pAttr - pointer to attribute
 * @param   opcode - request opcode (ATT_READ_REQ or ATT_WRITE_REQ)
 *
 * @return  SUCCESS: Operation authorized.<BR>
 *          ATT_ERR_INSUFFICIENT_AUTHOR: Authorization required.<BR>
 */
// function of the following callback type are of type
// *pfnGATTAuthorizeAttrCB_t
// put here for illustration purpose, and maybe it should be
// pre-allocated for the purpose of generating the relay.

bStatus_t GATTAuthorizeAttrCB( uint16 connHandle,
		__xdata gattAttribute_t *pAttr, uint8 opcode ) {
	i2s_call_u16_p_u8();
	i2s_exit_u16_p_u8();
}

/*************************************************************/


void GATTServApp_RegisterForMsg( uint8 taskID ) {
	s2i_call_u8(MAP_GATTServApp_RegisterForMsg); // was 0xDA9 | 0xFB8
}

/**
 * @brief   Register a service's attribute list and callback functions with
 *          the GATT Server Application.
 *
 * @param   pAttrs - Array of attribute records to be registered
 * @param   numAttrs - Number of attributes in array
 * @param   pServiceCBs - Service callback function pointers
 *
 * @return  SUCCESS: Service registered successfully.<BR>
 *          INVALIDPARAMETER: Invalid service field.<BR>
 *          FAILURE: Not enough attribute handles available.<BR>
 *          bleMemAllocError: Memory allocation error occurred.<BR>
 */

bStatus_t GATTServApp_RegisterService( __xdata gattAttribute_t *pAttrs,
		uint16 numAttrs, CONST gattServiceCBs_t *pServiceCBs ) {
	s2i_call_p_u16_p(MAP_GATTServApp_RegisterService); // was 0xDBB | 0xFCA
	s2i_ret_u8();
}

/**
 * @brief   Deregister a service's attribute list and callback functions from
 *          the GATT Server Application.
 *
 *          NOTE: It's the caller's responsibility to free the service attribute
 *          list returned from this API.
 *
 * @param   handle - handle of service to be deregistered
 * @param   p2pAttrs - pointer to array of attribute records (to be returned)
 *
 * @return  SUCCESS: Service deregistered successfully.
 *          FAILURE: Service not found.
 */
bStatus_t GATTServApp_DeregisterService( uint16 handle, __xdata gattAttribute_t **p2pAttrs ) {
	// No address available in map file so we can't do anything to it
	// here.
#ifdef CC2540
	// s2i_call_u16_p(address);
#elif defined(CC2541)
	// s2i_call_u16_p(address);
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
}

/**
 * @brief       Find the attribute record within a service attribute
 *              table for a given attribute value pointer.
 *
 * @param       pAttrTbl - pointer to attribute table
 * @param       numAttrs - number of attributes in attribute table
 * @param       pValue - pointer to attribute value
 *
 * @return      Pointer to attribute record. NULL, if not found.
 */

__xdata gattAttribute_t *GATTServApp_FindAttr( __xdata gattAttribute_t
		*pAttrTbl, uint16 numAttrs, __xdata uint8 *pValue ) {
	s2i_call_p_u16_p(MAP_GATTServApp_FindAttr); // was 0xDC7 | 0xFD6
	s2i_ret_p();
}
/**
 * @brief   Add function for the GATT Service.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  SUCCESS: Service added successfully.<BR>
 *          INVALIDPARAMETER: Invalid service field.<BR>
 *          FAILURE: Not enough attribute handles available.<BR>
 *          bleMemAllocError: Memory allocation error occurred.<BR>
 */
bStatus_t GATTServApp_AddService( uint32 services ) {
	s2i_call_u32(MAP_GATTServApp_AddService); // was 0xDCD | 0xFDC
	s2i_ret_u8();
}

/**
 * @brief   Delete function for the GATT Service.
 *
 * @param   services - services to delete. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  SUCCESS: Service deleted successfully.<BR>
 *          FAILURE: Service not found.<BR>
 */
bStatus_t GATTServApp_DelService( uint32 services ) {
	// this one is not included in the mapfile!
#ifdef CC2540
	// s2i_call_u32(address);
#elif defined(CC2541)
	// s2i_call_u32(address); 
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
	s2i_ret_u8();
}

/**
 * @brief   Set a GATT Server parameter.
 *
 * @param   param - Profile parameter ID
 * @param   len - length of data to right
 * @param   pValue - pointer to data to write. This is dependent on the
 *                   parameter ID and WILL be cast to the appropriate
 *                   data type (example: data type of uint16 will be cast
 *                   to uint16 pointer).
 *
 * @return  SUCCESS: Parameter set successful
 *          FAILURE: Parameter in use
 *          INVALIDPARAMETER: Invalid parameter
 *          bleInvalidRange: Invalid value
 *          bleMemAllocError: Memory allocation failed
 */

bStatus_t GATTServApp_SetParameter( uint8 param, uint8 len, __xdata void
		*pValue ) {
#ifdef CC2540
	// s2i_call_u8_u8_p(address);
#elif defined(CC2541)
	// s2i_call_u8_u8_p(address);
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
	s2i_ret_u8();
}


/**
 * @brief   Get a GATT Server parameter.
 *
 * @param   param - Profile parameter ID
 * @param   pValue - pointer to data to put. This is dependent on the
 *                   parameter ID and WILL be cast to the appropriate
 *                   data type (example: data type of uint16 will be
 *                   cast to uint16 pointer).
 *
 * @return  SUCCESS: Parameter get successful
 *          INVALIDPARAMETER: Invalid parameter
 */
bStatus_t GATTServApp_GetParameter( uint8 param, __xdata void *pValue ) {
#ifdef CC2540
	// s2i_call_u8_p(address); 
#elif defined(CC2541)
	// s2i_call_u8_p(address);
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
	s2i_ret_u8();
}

/**
 * @brief   Update the Client Characteristic Configuration for a given
 *          Client.
 *
 *          Note: This API should only be called from the Bond Manager.
 *
 * @param   connHandle - connection handle.
 * @param   attrHandle - attribute handle.
 * @param   value - characteristic configuration value.
 *
 * @return  SUCCESS: Parameter get successful
 *          INVALIDPARAMETER: Invalid parameter
 */
bStatus_t GATTServApp_UpdateCharCfg( uint16 connHandle, uint16 attrHandle, uint16 value ) {
	s2i_call_u16_u16_u16(MAP_GATTServApp_UpdateCharCfg); // was 0xE2D| 0x103C
	s2i_ret_u8();
}

/**
 * @brief   Initialize the client characteristic configuration table.
 *
 *          Note: Each client has its own instantiation of the Client
 *                Characteristic Configuration. Reads/Writes of the Client
 *                Characteristic Configuration only only affect the
 *                configuration of that client.
 *
 * @param   connHandle - connection handle (0xFFFF for all connections).
 * @param   charCfgTbl - client characteristic configuration table.
 *
 * @return  none
 */

void GATTServApp_InitCharCfg( uint16 connHandle, __xdata gattCharCfg_t
		*charCfgTbl ) {
	s2i_call_u16_p(MAP_GATTServApp_InitCharCfg); // was 0xE39 | 0x1048
}

/**
 * @brief   Read the client characteristic configuration for a given
 *          client.
 *
 *          Note: Each client has its own instantiation of the Client
 *                Characteristic Configuration. Reads of the Client
 *                Characteristic Configuration only shows the configuration
 *                for that client.
 *
 * @param   connHandle - connection handle.
 * @param   charCfgTbl - client characteristic configuration table.
 *
 * @return  attribute value
 */

uint16 GATTServApp_ReadCharCfg( uint16 connHandle, __xdata gattCharCfg_t
		*charCfgTbl ) {
	s2i_call_u16_p(MAP_GATTServApp_ReadCharCfg); // was 0xE3F | 0x104E
	s2i_ret_u16();
}
/**
 * @brief   Write the client characteristic configuration for a given
 *          client.
 *
 *          Note: Each client has its own instantiation of the Client
 *                Characteristic Configuration. Writes of the Client
 *                Characteristic Configuration only only affect the
 *                configuration of that client.
 *
 * @param   connHandle - connection handle.
 * @param   charCfgTbl - client characteristic configuration table.
 * @param   value - attribute new value.
 *
 * @return  Success or Failure
 */

uint8 GATTServApp_WriteCharCfg( uint16 connHandle, __xdata gattCharCfg_t
		*charCfgTbl, uint16 value ) {
	s2i_call_u16_p_u16(MAP_GATTServApp_WriteCharCfg); // was 0xE45 | 0x1054
	s2i_ret_u8();
}

/**
 * @brief   Process the client characteristic configuration
 *          write request for a given client.
 *
 * @param   connHandle - connection message was received on.
 * @param   pAttr - pointer to attribute.
 * @param   pValue - pointer to data to be written.
 * @param   len - length of data.
 * @param   offset - offset of the first octet to be written.
 * @param   validCfg - valid configuration.
 *
 * @return  Success or Failure
 */

bStatus_t GATTServApp_ProcessCCCWriteReq( uint16 connHandle, __xdata
		gattAttribute_t *pAttr, __xdata uint8 *pValue, uint8 len, uint16
		offset, uint16 validCfg ) {
	s2i_call_u16_p_p_u8_u16_u16(MAP_GATTServApp_ProcessCCCWriteReq); // was 0xE45| 0x1054
	s2i_ret_u8();
}

/**
 * @brief   Process Client Charateristic Configuration change.
 *
 * @param   charCfgTbl - characteristic configuration table.
 * @param   pValue - pointer to attribute value.
 * @param   authenticated - whether an authenticated link is required.
 * @param   attrTbl - attribute table.
 * @param   numAttrs - number of attributes in attribute table.
 * @param   taskId - task to be notified of confirmation.
 *
 * @return  Success or Failure
 */

bStatus_t GATTServApp_ProcessCharCfg( __xdata gattCharCfg_t *charCfgTbl,
		__xdata uint8 *pValue, uint8 authenticated, __xdata gattAttribute_t
		*attrTbl, uint16 numAttrs, uint8 taskId ) {
	s2i_call_p_p_u8_p_u16_u8(MAP_GATTServApp_ProcessCharCfg); // was 0xE51| 0x1060
	s2i_ret_u8();
}

/**
 * @brief   Build and send the GATT_CLIENT_CHAR_CFG_UPDATED_EVENT to
 *          the application.
 *
 * @param   connHandle - connection handle
 * @param   attrHandle - attribute handle
 * @param   value - attribute new value
 *
 * @return  none
 */

void GATTServApp_SendCCCUpdatedEvent( uint16 connHandle, uint16
		attrHandle, uint16 value ) {
	s2i_call_u16_u16_u16(MAP_GATTServApp_SendCCCUpdateEvent); // was 0xE5D| 0x4040
}


/**
 * @brief   Send out a Service Changed Indication.
 *
 * @param   connHandle - connection to use
 * @param   taskId - task to be notified of confirmation
 *
 * @return  SUCCESS: Indication was sent successfully.<BR>
 *          FAILURE: Service Changed attribute not found.<BR>
 *          INVALIDPARAMETER: Invalid connection handle or request field.<BR>
 *          MSG_BUFFER_NOT_AVAIL: No HCI buffer is available.<BR>
 *          bleNotConnected: Connection is down.<BR>
 *          blePending: A confirmation is pending with this client.<BR>
 */

bStatus_t GATTServApp_SendServiceChangedInd( uint16 connHandle, uint8
		taskId ) {
	s2i_call_u16_u8(MAP_GATTServApp_SendServiceChangedInd); // was 0xE33 | 0x1042
	s2i_ret_u8();
}

/**
 * @brief       Read an attribute. If the format of the attribute value
 *              is unknown to GATT Server, use the callback function
 *              provided by the Service.
 *
 * @param       connHandle - connection message was received on
 * @param       pAttr - pointer to attribute
 * @param       service - handle of owner service
 * @param       pValue - pointer to data to be read
 * @param       pLen - length of data to be read
 * @param       offset - offset of the first octet to be read
 * @param       maxLen - maximum length of data to be read
 *
 * @return      Success or Failure
 */

uint8 GATTServApp_ReadAttr( uint16 connHandle, __xdata gattAttribute_t
		*pAttr, uint16 service, __xdata uint8 *pValue, __xdata uint8 *pLen,
		uint16 offset, uint8 maxLen ) {
	s2i_call_u16_p_u16_p_p_u16_u8(MAP_GATTServApp_ReadAttr); // was 0xE33 | 0x1042
	s2i_ret_u8();
}

/**
 * @brief   Write attribute data
 *
 * @param   connHandle - connection message was received on
 * @param   handle - attribute handle
 * @param   pValue - pointer to data to be written
 * @param   len - length of data
 * @param   offset - offset of the first octet to be written
 *
 * @return  Success or Failure
 */

uint8 GATTServApp_WriteAttr( uint16 connHandle, uint16 handle, __xdata
		uint8 *pValue, uint16 len, uint16 offset ) {
	s2i_call_u16_u16_p_u16_u16(MAP_GATTServApp_WriteAttr); // was 0xE27 | 0x1036
	s2i_ret_u8();
}

/**
 * @}
 */

/**
 * @brief   Set a GATT Server Application Parameter value. Use this
 *          function to change the default GATT parameter values.
 *
 * @param   value - new param value
 *
 * @return  void
 */
void GATTServApp_SetParamValue( uint16 value ) {
#ifdef CC2540
//	s2i_call_u16(address);
#elif defined(CC2541)
//	s2i_call_u16(address);
#else
#error "Need to define macros CC2540 or CC2541"
#endif
}

/**
 * @brief   Get a GATT Server Application Parameter value.
 *
 * @param   none
 *
 * @return  GATT Parameter value
 */
uint16 GATTServApp_GetParamValue( void ) {
#ifdef CC2540
//	s2i_call_void(address);
#elif defined(CC2541)
//	s2i_call_void(address);
#else
#error "Need to define macros either CC2540 or CC2541"
#endif
	s2i_ret_u16();
}

/*-------------------------------------------------------------------
 * TASK API - These functions must only be called by OSAL.
 */

/**
 * @internal
 *
 * @brief   Initialize the GATT Server Test Application.
 *
 * @param   taskId - Task identifier for the desired task
 *
 * @return  void
 *
 */
void GATTServApp_Init( uint8 taskId ) {
	s2i_call_u8(MAP_GATTServApp_Init); // was 0xDAF | 0xFBF
}

/**
 * @internal
 *
 * @brief   GATT Server Application Task event processor. This function
 *          is called to process all events for the task. Events include
 *          timers, messages and any other user defined events.
 *
 * @param   task_id - The OSAL assigned task ID.
 * @param   events - events to process. This is a bit map and can
 *                   contain more than one event.
 *
 * @return  none
 */
uint16 GATTServApp_ProcessEvent( uint8 taskId, uint16 events ) {
	s2i_call_u8_u16(MAP_GATTServApp_ProcessEvent); //was 0xDB5 | 0xFC4
	s2i_ret_u16();
}

