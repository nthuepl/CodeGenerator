/**************************************************************************************************
  Filename:       s2i_gapgattserver.c
  Revised:        $Date: 2009-10-21 07:25:22 -0700 (Wed, 21 Oct 2009) $
  Revision:       $Revision: 20946 $

  Description:    This file contains GAP GATT attribute definitions
                  and prototypes.


**************************************************************************************************/


/*********************************************************************
 * INCLUDES
 */
#include "sdcc2iar.h"
#include "gapgattserver.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro for either CC2540 or CC2541"
#endif
  
  

/*********************************************************************
 * CONSTANTS
 */



/*********************************************************************
 * API FUNCTIONS
 */

/**
 * @brief   Set a GAP GATT Server parameter.
 *
 * @param   param - Profile parameter ID<BR>
 * @param   len - length of data to right
 * @param   value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).<BR>
 *
 * @return  bStatus_t
 */
bStatus_t GGS_SetParameter( uint8 param, uint8 len, __xdata void *value ) {
	s2i_call_u8_u8_p(MAP_GGS_SetParameter); // was 0xCBF | 0xECE
	s2i_ret_u8();
}

/**
 * @brief   Get a GAP GATT Server parameter.
 *
 * @param   param - Profile parameter ID<BR>
 * @param   value - pointer to data to put.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).<BR>
 *
 * @return  bStatus_t
 */
bStatus_t GGS_GetParameter( uint8 param, __xdata void *value ) {
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
 * @brief   Add function for the GAP GATT Service.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  SUCCESS: Service added successfully.<BR>
 *          INVALIDPARAMETER: Invalid service field.<BR>
 *          FAILURE: Not enough attribute handles available.<BR>
 *          bleMemAllocError: Memory allocation error occurred.<BR>
 */
bStatus_t GGS_AddService( uint32 services ) {
	s2i_call_u32(MAP_GGS_AddService); // was 0xCC5 | 0xED4
	s2i_ret_u8();
}

/**
 * @brief   Delete function for the GAP GATT Service.
 *
 * @param   services - services to delete. This is a bit map and can
 *                     contain more than one service.
 *
 * @return  SUCCESS: Service deleted successfully.<BR>
 *          FAILURE: Service not found.<BR>
 */
bStatus_t GGS_DelService( uint32 services ) {
#ifdef MAP_GGS_DelService
	s2i_call_u32(MAP_GGS_DelService);
#endif
	s2i_ret_u8();
}

/**
 * @brief   Registers the application callback function.
 *
 *          Note: Callback registration is needed only when the
 *                Device Name is made writable. The application
 *                will be notified when the Device Name is changed
 *                over the air.
 *
 * @param   appCallbacks - pointer to application callbacks.
 *
 * @return  none
 */
void GGS_RegisterAppCBs(__xdata ggsAppCBs_t *appCallbacks ) {
#ifdef MAP_GGS_RegisterAppCBs
	s2i_call_u32(MAP_GGS_RegisterAppCBs);
#endif
}

/**
 * @brief   Set a GGS Parameter value. Use this function to change
 *          the default GGS parameter values.
 *
 * @param   value - new GGS param value
 *
 * @return  void
 */
void GGS_SetParamValue( uint16 value ) {
#ifdef MAP_GGS_SetParamValue
	s2i_call_u16(MAP_GGS_SetParamValue);
#endif
}

/**
 * @brief   Get a GGS Parameter value.
 *
 * @param   none
 *
 * @return  GGS Parameter value
 */
uint16 GGS_GetParamValue( void ) {
#ifdef MAP_GGS_GetParamValue
	 s2i_call_void(MAP_GGS_GetParamValue);
#endif
	s2i_ret_u16();
}

