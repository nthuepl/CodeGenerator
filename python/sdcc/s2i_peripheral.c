/**
  @headerfile:    peripheral.c
  $Date: 2012-10-01 12:57:40 -0700 (Mon, 01 Oct 2012) $
  $Revision: 31663 $

  @mainpage TI BLE GAP Peripheral Role

  This GAP profile advertises and allows connections.

*/

#include "peripheral.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
/*-------------------------------------------------------------------
 * INCLUDES
 */

/*-------------------------------------------------------------------
 * CONSTANTS
 */

/*-------------------------------------------------------------------
 * TYPEDEFS
 */


/*-------------------------------------------------------------------
 * API FUNCTIONS
 */

/**
 * @defgroup GAPROLES_PERIPHERAL_API GAP Peripheral Role API Functions
 *
 * @{
 */

/**
 * @brief       Set a GAP Role parameter.
 *
 *  NOTE: You can call this function with a GAP Parameter ID and it will set the
 *        GAP Parameter.  GAP Parameters are defined in (gap.h).  Also,
 *        the "len" field must be set to the size of a "uint16" and the
 *        "pValue" field must point to a "uint16".
 *
 * @param       param - Profile parameter ID: @ref GAPROLE_PROFILE_PARAMETERS
 * @param       len - length of data to write
 * @param       pValue - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).
 *
 * @return      SUCCESS or INVALIDPARAMETER (invalid paramID)
 */
bStatus_t GAPRole_SetParameter( uint16 param, uint8 len, __xdata void *pValue ) {
	s2i_call_u16_u8_p(MAP_GAPRole_SetParameter);
	s2i_ret_u8();
}

/**
 * @brief       Get a GAP Role parameter.
 *
 *  NOTE: You can call this function with a GAP Parameter ID and it will get a
 *        GAP Parameter.  GAP Parameters are defined in (gap.h).  Also, the
 *        "pValue" field must point to a "uint16".
 *
 * @param       param - Profile parameter ID: @ref GAPROLE_PROFILE_PARAMETERS
 * @param       pValue - pointer to location to get the value.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).
 *
 * @return      SUCCESS or INVALIDPARAMETER (invalid paramID)
 */
bStatus_t GAPRole_GetParameter( uint16 param, __xdata void *pValue ) {
		s2i_call_u16_p(MAP_GAPRole_GetParameter);
		s2i_ret_u8();
}

/**
 * @brief       Does the device initialization.  Only call this function once.
 *
 * @param       pAppCallbacks - pointer to application callbacks.
 *
 * @return      SUCCESS or bleAlreadyInRequestedMode
 */
bStatus_t GAPRole_StartDevice(__xdata gapRolesCBs_t *pAppCallbacks ) {
	s2i_call_p(MAP_GAPRole_StartDevice);
	s2i_ret_u8();
}

/**
 * @brief       Terminates the existing connection.
 *
 * @return      SUCCESS or bleIncorrectMode
 */
bStatus_t GAPRole_TerminateConnection( void ) {
	s2i_call_void(MAP_GAPRole_TerminateConnection);
	s2i_ret_u8();
}

/**
 * @brief       Update the parameters of an existing connection
 *
 * @param       connInterval - the new connection interval
 * @param       latency - the new slave latency
 * @param       connTimeout - the new timeout value
 * @param       handleFailure - what to do if the update does not occur.
 *              Method may choose to terminate connection, try again, or take no action
 *
 * @return      SUCCESS, bleNotConnected or bleInvalidRange
 */

bStatus_t GAPRole_SendUpdateParam( uint16 minConnInterval, uint16
		maxConnInterval, uint16 latency, uint16 connTimeout, uint8
		handleFailure ) {
	s2i_call_u16_u16_u16_u16_u8(MAP_GAPRole_SendUpdateParam);
	s2i_ret_u8();
}

/**
 * @} End GAPROLES_PERIPHERAL_API
 */


/*-------------------------------------------------------------------
 * TASK FUNCTIONS - Don't call these. These are system functions.
 */

/**
 * @internal
 *
 * @brief       Initialization function for the GAP Role Task.
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
void GAPRole_Init( uint8 task_id ) {
	s2i_call_u8(MAP_GAPRole_Init);
}

/**
 * @internal
 *
 * @brief       GAP Role Task event processor.
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
uint16 GAPRole_ProcessEvent( uint8 task_id, uint16 events ) {
	s2i_call_u8_u16(MAP_GAPRole_ProcessEvent);
	s2i_ret_u16();
}

/*-------------------------------------------------------------------
-------------------------------------------------------------------*/
