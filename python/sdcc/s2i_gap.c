/**
  file:    s2i_gap.c

  binding for BLE GAP API

*/


/*-------------------------------------------------------------------
 * INCLUDES
 */
#include "gap.h"
#include "sdcc2iar.h"

/*-------------------------------------------------------------------
 * FUNCTIONS - Initialization and Configuation
 */

  /**
   * @brief       Called to setup the device.  Call just once on initialization.
   *
   *   NOTE: When initialization is complete, the calling app will be
   *         sent the GAP_DEVICE_INIT_DONE_EVENT
   *
   * @param       taskID - Default task ID to send events.
   * @param       profileRole - GAP Profile Roles: @ref GAP_PROFILE_ROLE_DEFINES
   * @param       maxScanResponses - maximum number to scan responses
   *                we can receive during a device discovery.
   * @param       pIRK - pointer to Identity Root Key, NULLKEY (all zeroes) if the app
   *                wants the GAP to generate the key.
   * @param       pSRK - pointer to Sign Resolving Key, NULLKEY if the app
   *                wants the GAP to generate the key.
   * @param       pSignCounter - 32 bit value used in the SM Signing
   *                algorithm that shall be initialized to zero and incremented
   *                with every new signing. This variable must also be maintained
   *                by the application.
   *
   * @return      SUCCESS - Processing, expect GAP_DEVICE_INIT_DONE_EVENT, <BR>
   *              INVALIDPARAMETER - for invalid profile role or role combination, <BR>
   *              bleIncorrectMode - trouble communicating with HCI
   */
  bStatus_t GAP_DeviceInit(  uint8 taskID,
                           uint8 profileRole,
                           uint8 maxScanResponses,
                           __xdata uint8 *pIRK,
                           __xdata uint8 *pSRK,
                           __xdata uint32 *pSignCounter ) {
		s2i_call_u8_u8_u8_p_p_p(MAP_GAP_DeviceInit);
		s2i_ret_u8();
	}

  /**
   * @brief       Called to setup a GAP Advertisement/Scan Response data token.
   *
   * NOTE:        The data in these items are stored as low byte first (OTA format).
   *              The passed in structure "token" should be allocated by the calling app/profile
   *              and not released until after calling GAP_RemoveAdvToken().
   *
   * @param       pToken - Advertisement/Scan response token to write.
   *
   * @return      SUCCESS - advertisement token added to the GAP list <BR>
   *              INVALIDPARAMETER - Invalid Advertisement Type or pAttrData is NULL <BR>
   *              INVALID_MEM_SIZE - The tokens take up too much space and don't fit into Advertisment data and Scan Response Data<BR>
   *              bleInvalidRange - token ID already exists.<BR>
   *              bleIncorrectMode - not a peripheral device<BR>
   *              bleMemAllocError - memory allocation failure,
   */
  bStatus_t GAP_SetAdvToken(__xdata  gapAdvDataToken_t *pToken ) {
		s2i_call_p(MAP_GAP_SetAdvToken);
		s2i_ret_u8();
	}

  /**
   * @brief       Called to read a GAP Advertisement/Scan Response data token.
   *
   * @param       adType - Advertisement type to get
   *
   * @return      pointer to the advertisement data token structure, NULL if not found.
   */
  __xdata gapAdvDataToken_t *GAP_GetAdvToken( uint8 adType ) {
		s2i_call_u8(MAP_GAP_GetAdvToken);
		s2i_ret_u16();
	}

  /**
   * @brief       Called to remove a GAP Advertisement/Scan Response data token.
   *
   * @param       adType - Advertisement type to remove
   *
   * @return      pointer to the token structure removed from the GAP ADType list
   *              NULL if the requested adType wasn't found.
   */
  __xdata gapAdvDataToken_t *GAP_RemoveAdvToken( uint8 adType ) {
		s2i_call_u8(MAP_GAP_RemoveAdvToken);
		s2i_ret_u16();
	}

  /**
   * @brief       Called to rebuild and load Advertisement and Scan Response data from existing
   *              GAP Advertisement Tokens.
   *
   * @return      SUCCESS or bleIncorrectMode
   */
  bStatus_t GAP_UpdateAdvTokens( void ) {
		s2i_call_void(MAP_GAP_UpdateAdvTokens);
		s2i_ret_u8();
	}

 /**
   * @brief       Set a GAP Parameter value.  Use this function to change
   *              the default GAP parameter values.
   *
   * @param       paramID - parameter ID: @ref GAP_PARAMETER_ID_DEFINES
   * @param       paramValue - new param value
   *
   * @return      SUCCESS or INVALIDPARAMETER (invalid paramID)
   */
  bStatus_t GAP_SetParamValue( gapParamIDs_t paramID, uint16 paramValue ) {
		s2i_call_u16_u16(MAP_GAP_SetParamValue);
		s2i_ret_u8();
	}

  /**
   * @brief       Get a GAP Parameter value.
   *
   * @param       paramID - parameter ID: @ref GAP_PARAMETER_ID_DEFINES
   *
   * @return      GAP Parameter value or 0xFFFF if invalid
   */
  uint16 GAP_GetParamValue( gapParamIDs_t paramID ) {
		s2i_call_u16(MAP_GAP_GetParamValue);
		s2i_ret_u16();
	}

  /**
   * @brief       Setup the device's address type.  If ADDRTYPE_PRIVATE_RESOLVE
   *              is selected, the address will change periodically.
   *
   * @param       addrType - @ref GAP_ADDR_TYPE_DEFINES
   * @param       pStaticAddr - Only used with ADDRTYPE_STATIC
   *                       or ADDRTYPE_PRIVATE_NONRESOLVE type.<BR>
   *                   NULL to auto generate otherwise the application
   *                   can specify the address value
   *
   * @return      SUCCESS: address type updated,<BR>
   *              bleNotReady: Can't be called until GAP_DeviceInit() is called
   *                   and the init process is completed,<BR>
   *              bleIncorrectMode: can't change with an active connection,<BR>
   *               or INVALIDPARAMETER.<BR>
   *
   *              If return value isn't SUCCESS, the address type remains
   *              the same as before this call.
   */
  bStatus_t GAP_ConfigDeviceAddr( uint8 addrType, __xdata uint8 *pStaticAddr ) {
		s2i_call_u8_p(MAP_GAP_ConfigDeviceAddr);
		s2i_ret_u8();
	}

  /**
   * @brief       Register your task ID to receive extra (unwanted)
   *              HCI status and complete events.
   *
   * @param       taskID - Default task ID to send events.
   *
   * @return      none
   */
  void GAP_RegisterForHCIMsgs( uint8 taskID ) {
			s2i_call_u8(MAP_GAP_RegisterForHCIMsgs);
	}

/*-------------------------------------------------------------------
 * FUNCTIONS - Device Discovery
 */

  /**
   * @brief       Start a device discovery scan.
   *
   * @param       pParams - Device Discovery parameters
   *
   * @return      SUCCESS: scan started,<BR>
   *              bleIncorrectMode: invalid profile role,<BR>
   *              bleAlreadyInRequestedMode: not available<BR>
   */
  bStatus_t GAP_DeviceDiscoveryRequest(__xdata gapDevDiscReq_t *pParams ){
		s2i_call_p(MAP_GAP_DeviceDiscoveryRequest);
		s2i_ret_u8();
	}

  /**
   * @brief       Cancel an existing device discovery request.
   *
   * @param       taskID - used to return GAP_DEVICE_DISCOVERY_EVENT
   *
   * @return      SUCCESS: cancel started,<BR>
   *              bleInvalidTaskID: Not the task that started discovery,<BR>
   *              bleIncorrectMode: not in discovery mode<BR>
   */
  bStatus_t GAP_DeviceDiscoveryCancel( uint8 taskID ) {
		s2i_call_u8(MAP_GAP_DeviceDiscoveryCancel);
		s2i_ret_u8();
	}

  /**
   * @brief       Setup or change advertising.  Also starts advertising.
   *
   * @param       taskID - used to return GAP_DISCOVERABLE_RESPONSE_EVENT
   * @param       pParams - advertising parameters
   *
   * @return      SUCCESS: advertising started,<BR>
   *              bleIncorrectMode: invalid profile role,<BR>
   *              bleAlreadyInRequestedMode: not available at this time,<BR>
   *              bleNotReady: advertising data isn't set up yet.<BR>
   */
  bStatus_t GAP_MakeDiscoverable( uint8 taskID, __xdata gapAdvertisingParams_t *pParams ) {
		s2i_call_u8_p(MAP_GAP_MakeDiscoverable);
		s2i_ret_u8();
	}

  /**
   * @brief       Setup or change advertising and scan response data.
   *
   *    NOTE:  if the return status from this function is SUCCESS,
   *           the task isn't complete until the GAP_ADV_DATA_UPDATE_DONE_EVENT
   *           is sent to the calling application task.
   *
   * @param       taskID - task ID of the app requesting the change
   * @param       adType - TRUE - advertisement data, FALSE  - scan response data
   * @param       dataLen - Octet length of advertData
   * @param       pAdvertData - advertising or scan response data
   *
   * @return      SUCCESS: data accepted,<BR>
   *              bleIncorrectMode: invalid profile role,<BR>
   */
  bStatus_t GAP_UpdateAdvertisingData( uint8 taskID, uint8 adType,
                                      uint8 dataLen, __xdata uint8 *pAdvertData ) {
		s2i_call_u8_u8_u8_p(MAP_GAP_UpdateAdvertisingData);
		s2i_ret_u8();
	}

  /**
   * @brief       Stops advertising.
   *
   * @param       taskID - of task that called GAP_MakeDiscoverable
   *
   * @return      SUCCESS: stopping discoverable mode,<BR>
   *              bleIncorrectMode: not in discoverable mode,<BR>
   *              bleInvalidTaskID: not correct task<BR>
   */
  bStatus_t GAP_EndDiscoverable( uint8 taskID ) {
		s2i_call_u8(MAP_GAP_EndDiscoverable);
		s2i_ret_u8();
	}

  /**
   * @brief       Resolves a private address against an IRK.
   *
   * @param       pIRK - pointer to the IRK
   * @param       pAddr - pointer to the Resovable Private address
   *
   * @return      SUCCESS: match,<BR>
   *              FAILURE: don't match,<BR>
   *              INVALIDPARAMETER: parameters invalid<BR>
   */
  bStatus_t GAP_ResolvePrivateAddr(__xdata uint8 *pIRK, __xdata uint8 *pAddr ) {
		s2i_call_p_p(MAP_GAP_ResolvePrivateAddr);
		s2i_ret_u8();
	}

/*-------------------------------------------------------------------
 * FUNCTIONS - Link Establishment
 */

  /**
   * @brief       Establish a link to a slave device.
   *
   * @param       pParams - link establishment parameters
   *
   * @return      SUCCESS: started establish link process,<BR>
   *              bleIncorrectMode: invalid profile role,<BR>
   *              bleNotReady: a scan is in progress,<BR>
   *              bleAlreadyInRequestedMode: can’t process now,<BR>
   *              bleNoResources: Too many links<BR>
   */
  bStatus_t GAP_EstablishLinkReq(__xdata gapEstLinkReq_t *pParams ) {
		s2i_call_p(MAP_GAP_EstablishLinkReq);
		s2i_ret_u8();
	}

  /**
   * @brief       Terminate a link connection.
   *
   * @param       taskID - requesting app's task id.
   * @param       connectionHandle - connection handle of link to terminate
   *                  or @ref GAP_CONN_HANDLE_DEFINES
   *
   * @return      SUCCESS: Terminate started,<BR>
   *              bleIncorrectMode: No Link to terminate,<BR>
   *              bleInvalidTaskID: not app that established link<BR>
   */
  bStatus_t GAP_TerminateLinkReq( uint8 taskID, uint16 connectionHandle ) {
		s2i_call_u8_u16(MAP_GAP_TerminateLinkReq);
		s2i_ret_u8();
	}

  /**
   * @brief       Update the link parameters to a slave device.
   *
   * @param       pParams - link update parameters
   *
   * @return      SUCCESS: started update link process,<BR
   *              INVALIDPARAMETER: one of the parameters were invalid,<BR>
   *              bleIncorrectMode: invalid profile role,<BR>
   *              bleNotConnected: not in a connection<BR>
   */
  bStatus_t GAP_UpdateLinkParamReq(__xdata gapUpdateLinkParamReq_t *pParams ) {
		s2i_call_p(MAP_GAP_UpdateLinkParamReq);
		s2i_ret_u8();
	}

  /**
   * @brief       Returns the number of active connections.
   *
   * @return      Number of active connections.
   */
  uint8 GAP_NumActiveConnections( void ) {
		s2i_call_void(MAP_GAP_NumActiveConnections);
		s2i_ret_u8();
	}

/*-------------------------------------------------------------------
 * FUNCTIONS - Pairing
 */

  /**
   * @brief       Start the Authentication process with the requested device.
   *              This function is used to Initiate/Allow pairing.
   *              Called by both master and slave device (Central and Peripheral).
   *
   * NOTE:        This function is called after the link is established.
   *
   * @param       pParams - Authentication parameters
   * @param       pPairReq - Enter these parameters if the Pairing Request was already received.
   *              NULL, if waiting for Pairing Request or if initiating.
   *
   * @return      SUCCESS,<BR>
   *              bleIncorrectMode: Not correct profile role,<BR>
   *              INVALIDPARAMETER, <BR>
   *              bleNotConnected,<BR>
   *              bleAlreadyInRequestedMode,<BR>
   *              FAILURE - not workable.<BR>
   */
  bStatus_t GAP_Authenticate(__xdata gapAuthParams_t *pParams,
			__xdata gapPairingReq_t *pPairReq ) {
		s2i_call_p_p(MAP_GAP_Authenticate);
		s2i_ret_u8();
	}

  /**
   * @brief       Send a Pairing Failed message and end any existing pairing.
   *
   * @param       connectionHandle - connection handle.
   * @param       reason - Pairing Failed reason code.
   *
   * @return      SUCCESS - function was successful,<BR>
   *              bleMemAllocError - memory allocation error,<BR>
   *              INVALIDPARAMETER - one of the parameters were invalid,<BR>
   *              bleNotConnected - link not found,<BR>
   *              bleInvalidRange - one of the parameters were not within range.
   */
  bStatus_t GAP_TerminateAuth( uint16 connectionHandle, uint8 reason ) {
		s2i_call_u16_u8(MAP_GAP_TerminateAuth);
		s2i_ret_u8();
	}

  /**
   * @brief       Update the passkey in string format.  This function is called by the
   *              application/profile in response to receiving the
   *              GAP_PASSKEY_NEEDED_EVENT message.
   *
   * NOTE:        This function is the same as GAP_PasscodeUpdate(), except that
   *              the passkey is passed in as a string format.
   *
   * @param       pPasskey - new passkey - pointer to numeric string (ie. "019655" ).
   *              This string's range is "000000" to "999999".
   * @param       connectionHandle - connection handle.
   *
   * @return      SUCCESS: will start pairing with this entry,<BR>
   *              bleIncorrectMode: Link not found,<BR>
   *              INVALIDPARAMETER: passkey == NULL or passkey isn't formatted properly.<BR>
   */
  bStatus_t GAP_PasskeyUpdate(__xdata uint8 *pPasskey, uint16 connectionHandle ) {
		s2i_call_p_u16(MAP_GAP_PasskeyUpdate);
		s2i_ret_u8();
	}

  /**
   * @brief       Update the passkey in a numeric value (not string).
   *              This function is called by the application/profile in response
   *              to receiving the GAP_PASSKEY_NEEDED_EVENT message.
   *
   * NOTE:        This function is the same as GAP_PasskeyUpdate(), except that
   *              the passkey is passed in as a non-string format.
   *
   * @param       passcode - not string - range: 0 - 999,999.
   * @param       connectionHandle - connection handle.
   *
   * @return      SUCCESS: will start pairing with this entry,<BR>
   *              bleIncorrectMode: Link not found,<BR>
   *              INVALIDPARAMETER: passkey == NULL or passkey isn't formatted properly.<BR>
   */
  bStatus_t GAP_PasscodeUpdate( uint32 passcode, uint16 connectionHandle ) {
		s2i_call_u32_u16(MAP_GAP_PasscodeUpdate);
		s2i_ret_u8();
	}

  /**
   * @brief       Generate a Slave Requested Security message to the master.
   *
   * @param       connectionHandle - connection handle.
   * @param       authReq - Authentication Requirements: Bit 2: MITM, Bits 0-1: bonding (0 - no bonding, 1 - bonding)
   *
   * @return      SUCCESS: will send,<BR>
   *              bleNotConnected: Link not found,<BR>
   *              bleIncorrectMode: wrong GAP role, must be a Peripheral Role<BR>
   */
  bStatus_t GAP_SendSlaveSecurityRequest( uint16 connectionHandle, uint8 authReq ) {
		s2i_call_u16_u8(MAP_GAP_SendSlaveSecurityRequest);
		s2i_ret_u8();
	}

  /**
   * @brief       Set up the connection to accept signed data.
   *
   * NOTE:        This function is called after the link is established.
   *
   * @param       connectionHandle - connection handle of the signing information
   * @param       authenticated - TRUE if the signing information is authenticated, FALSE otherwise
   * @param       pParams - signing parameters
   *
   * @return      SUCCESS, <BR>
   *              bleIncorrectMode: Not correct profile role,<BR>
   *              INVALIDPARAMETER, <BR>
   *              bleNotConnected,<BR>
   *              FAILURE: not workable.<BR>
   */
  bStatus_t GAP_Signable( uint16 connectionHandle, uint8 authenticated,
			__xdata smSigningInfo_t *pParams ) {
		s2i_call_u16_u8_p(MAP_GAP_Signable);
		s2i_ret_u8();
	}

  /**
   * @brief       Set up the connection's bound paramaters.
   *
   * NOTE:        This function is called after the link is established.
   *
   * @param       connectionHandle - connection handle of the signing information
   * @param       authenticated - this connection was previously authenticated
   * @param       pParams - the connected device's security parameters
   * @param       startEncryption - whether or not to start encryption
   *
   * @return      SUCCESS, <BR>
   *              bleIncorrectMode: Not correct profile role,<BR>
   *              INVALIDPARAMETER, <BR>
   *              bleNotConnected,<BR>
   *              FAILURE: not workable.<BR>
   */
  bStatus_t GAP_Bond( uint16 connectionHandle, uint8 authenticated,
              __xdata smSecurityInfo_t *pParams, uint8 startEncryption ) {
		s2i_call_u16_u8_p_u8(MAP_GAP_Bond);
		s2i_ret_u8();
	}

/**
 * @} End GAP_API
 */

/*-------------------------------------------------------------------
 * Internal API - These functions are only called from gap.c module.
 */

  /**
   * @internal
   *
   * @brief       Setup the device configuration parameters.
   *
   * @param       taskID - Default task ID to send events.
   * @param       profileRole - GAP Profile Roles
   *
   * @return      SUCCESS or bleIncorrectMode
   */
  bStatus_t GAP_ParamsInit( uint8 taskID, uint8 profileRole ) {
		s2i_call_u8_u8(MAP_GAP_ParamsInit);
		s2i_ret_u8();
	}

  /**
   * @internal
   *
   * @brief       Setup the device security configuration parameters.
   *
   * @param       pIRK - pointer to Identity Root Key, NULLKEY (all zeroes) if the app
   *                wants the GAP to generate the key.
   * @param       pSRK - pointer to Sign Resolving Key, NULLKEY if the app
   *                wants the GAP to generate the key.
   * @param       pSignCounter - 32 bit value used in the SM Signing
   *                algorithm that shall be initialized to zero and incremented
   *                with every new signing. This variable must also be maintained
   *                by the application.
   *
   * @return      none
   */
  void GAP_SecParamsInit( __xdata uint8 *pIRK, __xdata uint8 *pSRK, __xdata uint32 *pSignCounter ) {
		s2i_call_p_p_p(MAP_GAP_SecParamsInit);
	}

  /**
   * @internal
   *
   * @brief       Initialize the GAP Peripheral Dev Manager.
   *
   * @param       none
   *
   * @return      SUCCESS or bleMemAllocError
   */
  bStatus_t GAP_PeriDevMgrInit( void ) {
		s2i_call_void(MAP_GAP_PeriDevMgrInit);
		s2i_ret_u8();
	}

  /**
   * @internal
   *
   * @brief       Initialize the GAP Central Dev Manager.
   *
   * @param       maxScanResponses - maximum number to scan responses
   *                we can receive during a device discovery.
   *
   * @return      SUCCESS or bleMemAllocError
   */
  bStatus_t GAP_CentDevMgrInit( uint8 maxScanResponses ) {
		s2i_call_u8(MAP_GAP_CentDevMgrInit);
		s2i_ret_u8();
	}

  /**
   * @internal
   *
   * @brief       Register the GAP Central Connection processing functions.
   *
   * @param       none
   *
   * @return      none
   */
  void GAP_CentConnRegister( void ) {
		s2i_call_void(MAP_GAP_CentConnRegister);
	}


/*-------------------------------------------------------------------
 * TASK API - These functions must only be called OSAL.
 */

  /**
   * @internal
   *
   * @brief       GAP Task initialization function.
   *
   * @param       taskID - GAP task ID.
   *
   * @return      void
   */
  void GAP_Init( uint8 task_id ) {
		s2i_call_u8(MAP_GAP_Init);
	}

  /**
   * @internal
   *
   * @brief       GAP Task event processing function.
   *
   * @param       taskID - GAP task ID
   * @param       events - GAP events.
   *
   * @return      events not processed
   */
  uint16 GAP_ProcessEvent( uint8 task_id, uint16 events ) {
		s2i_call_u8_u16(MAP_GAP_ProcessEvent);
		s2i_ret_u16();
	}


/*-------------------------------------------------------------------
-------------------------------------------------------------------*/
