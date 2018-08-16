/**************************************************************************************************
  Filename:       s2i_devinfoservice.c
  Revised:        $Date $
  Revision:       $Revision $

  Description:    This file contains the binding file for
	Device Information service definitions and
                  prototypes.
**************************************************************************************************/


/*********************************************************************
 * INCLUDES
 */
#include "sdcc2iar.h"
#include "devinfoservice.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif

/*********************************************************************
 * CONSTANTS
 */

/*
 * DevInfo_AddService- Initializes the Device Information service by registering
 *          GATT attributes with the GATT server.
 *
 */

bStatus_t DevInfo_AddService( void ) {
	s2i_call_void(MAP_DevInfo_AddService); // was 0x7BB | 0x952
	s2i_ret_u8();
}

/*********************************************************************
 * @fn      DevInfo_SetParameter
 *
 * @brief   Set a Device Information parameter.
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
bStatus_t DevInfo_SetParameter( uint8 param, uint8 len, __xdata void *value ) {
	s2i_call_u8_u8_p(MAP_DevInfo_SetParameter); // was 0x7C1 | 0x958
	s2i_ret_u8();
}


/*
 * DevInfo_GetParameter - Get a Device Information parameter.
 *
 *    param - Profile parameter ID
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).
 */
bStatus_t DevInfo_GetParameter( uint8 param, __xdata void *value ) {
#ifdef CC2540
	// s2i_call_u8_p(address);
#elif defined(CC2541)
	// s2i_call_u8_p(address);
#else
#error "Need to define macro either CC2540 or CC2541"
#endif
	s2i_ret_u8();
}
