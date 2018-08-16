/**************************************************************************************************
  Filename:       i2s_accelerometer.h
  Revised:        $Date: 2011-11-11 15:13:08 -0800 (Fri, 11 Nov 2011) $
  Revision:       $Revision: 28319 $

  Description:    This file contains Accelerometer Profile header file.

**************************************************************************************************/

#include "sdcc2iar.h"
#include "accelerometer.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif


/*********************************************************************
 * API FUNCTIONS 
 */

/*
 * Accel_AddService- Initializes the Accelerometer service by registering 
 *          GATT attributes with the GATT server. Only call this function once.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 */
bStatus_t Accel_AddService( uint32 services ) {
	s2i_call_u32(MAP_Accel_AddService); // was 0x773 | 0x90A
	s2i_ret_u8();
}

/*
 * Accel_RegisterAppCBs - Registers the application callback function.
 *                    Only call this function once.
 *
 *    appCallbacks - pointer to application callbacks.
 */
bStatus_t Accel_RegisterAppCBs(__xdata accelCBs_t *appCallbacks ) {
	s2i_call_p(MAP_Accel_RegisterAppCBs); // was 0x779 | 0x910
	s2i_ret_u8();
}


/*
 * Accel_SetParameter - Set an Accelerometer Profile parameter.
 *
 *    param - Profile parameter ID
 *    len - length of data to right
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 */
bStatus_t Accel_SetParameter( uint8 param, uint8 len, __xdata void *value ) {
	s2i_call_u8_u8_p(MAP_Accel_SetParameter); // was 0x77F | 0x916
	s2i_ret_u8();
}
  
/*
 * Accel_GetParameter - Get an Accelerometer Profile parameter.
 *
 *    param - Profile parameter ID
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 */
bStatus_t Accel_GetParameter( uint8 param, __xdata void *value ) {
	s2i_call_u8_p(MAP_Accel_GetParameter); // was 0x785 | 0x91C
	s2i_ret_u8();
}


