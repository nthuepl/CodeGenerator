/**************************************************************************************************
	Filename:       s2i_timeservice.h
	Revised:        $Date:2014-03-13 16:50:14 $

	Description:    This file contains the SDCC-to-IAR binding for
	GATT profile definitions and prototypes..

	Copyright 2013 EPLAB National Tsing Hua University. All rights reserved.
	The information contained herein is confidential property of NTHU. 	The material may be used for a personal and non-commercial use only in connection with 	a legitimate academic research purpose. Any attempt to copy, modify, and distribute any portion of this source code or derivative thereof for commercial, political, or propaganda purposes is strictly prohibited. All other uses require explicit written permission from the authors and copyright holders. This copyright statement must be retained in its entirety and displayed in the copyright statement of derived source code or systems.
**************************************************************************************************/



/*********************************************************************
 * INCLUDES
 */
#include "timeservice.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif


/*********************************************************************
 * Profile Callbacks
 */


/*********************************************************************
 * API FUNCTIONS 
 */

/*
 * timeservice_AddService- Initializes the GATT Profile service by registering
 *          GATT attributes with the GATT server.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 */

bStatus_t timeservice_AddService( uint32 services ) {
	s2i_call_u32(MAP_timeservice_AddService);
	s2i_ret_u8();
}

/*
 * timeservice_RegisterAppCBs - Registers the application callback function.
 *                    Only call this function once.
 *
 *    appCallbacks - pointer to application callbacks.
 */
bStatus_t timeservice_RegisterAppCBs(__xdata timeserviceCBs_t *appCallbacks ) {
	s2i_call_p(MAP_timeservice_RegisterAppCBs);
	s2i_ret_u8();
}

/*
 * timeservice_SetParameter - Set a GATT Profile parameter.
 *
 *    param - Profile parameter ID
 *    len - length of data to right
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate
 *          data type (example: data type of uint16 will be cast to
 *          uint16 pointer).
 */
bStatus_t timeservice_SetParameter( uint8 param, uint8 len, __xdata void *value ) {
	s2i_call_u8_u8_p(MAP_timeservice_SetParameter);
	s2i_ret_u8();
}

/*
 * timeservice_GetParameter - Get a GATT Profile parameter.
 *
 *    param - Profile parameter ID
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 */
bStatus_t timeservice_GetParameter( uint8 param, __xdata void *value ) {
	s2i_call_u8_p(MAP_timeservice_GetParameter);
	s2i_ret_u8();
}


/*********************************************************************
*********************************************************************/

