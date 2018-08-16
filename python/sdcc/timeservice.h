/**************************************************************************************************
	Filename:       timeservice.h
	Revised:        $Date:2014-03-13 16:50:14 $

	Description:    This file contains the GATT profile definitions and prototypes..

	Copyright 2013 EPLAB National Tsing Hua University. All rights reserved.
	The information contained herein is confidential property of NTHU. 	The material may be used for a personal and non-commercial use only in connection with 	a legitimate academic research purpose. Any attempt to copy, modify, and distribute any portion of this source code or derivative thereof for commercial, political, or propaganda purposes is strictly prohibited. All other uses require explicit written permission from the authors and copyright holders. This copyright statement must be retained in its entirety and displayed in the copyright statement of derived source code or systems.
**************************************************************************************************/

#ifndef TIMESERVICE_H
#define TIMESERVICE_H

#ifdef __cplusplus
extern "C"
{
#endif

/*********************************************************************
 * INCLUDES
 */
#include "hal_types.h"
#include "bcomdef.h"
/*********************************************************************
 * CONSTANTS
 */

// Profile Parameters
#define TIME_ENABLER		0
#define TIME                    1
#define DATE                    2
#define ALARM                   3
  
//#define HOUR			1
//#define MINUTE			2
//#define SECOND			3
//#define CENTURY			4
//#define YEAR			5
//#define MONTH			6	
//#define DATE			7
//#define DAY			8
//#define ALARM_MONTH		9
//#define ALARM_DATE		10
//#define ALARM_HOUR		11
//#define ALARM_MINUTE		12
//#define ALARM_SECOND		13
//#define ALARM_REPEATMODE	14

// timeservice Profile Service UUID
#define TIMESERVICE_SERV_UUID	0xFDF0

// timeservice UUID
#define TIME_ENABLER_UUID		0xFDF1
#define TIME_UUID			0xFDF2
#define DATE_UUID			0xFDF3
#define ALARM_UUID			0xFDF4
  
//#define HOUR_UUID			0xFDF2
//#define MINUTE_UUID			0xFDF3
//#define SECOND_UUID			0xFDF4
//#define CENTURY_UUID			0xFDF5
//#define YEAR_UUID			0xFDF6
//#define MONTH_UUID			0xFDF7
//#define DATE_UUID			0xFDF8
//#define DAY_UUID			0xFDF9
//#define ALARM_MONTH_UUID		0xFDFA
//#define ALARM_DATE_UUID			0xFDFB
//#define ALARM_HOUR_UUID			0xFDFC
//#define ALARM_MINUTE_UUID		0xFDFD
//#define ALARM_SECOND_UUID		0xFDFE
//#define ALARM_REPEATMODE_UUID	0xFDFF

// timeservice Profile Services bit fields
#define TIMESERVICE_SERVICE		0x00000001

  // Length of Characteristics
#define TIME_ENABLER_LEN		1
#define TIME_LEN                        3
#define DATE_LEN                        5
#define ALARM_LEN                       6
  
//#define HOUR_LEN			1
//#define MINUTE_LEN			1
//#define SECOND_LEN			1
//#define CENTURY_LEN			1
//#define YEAR_LEN			1
//#define MONTH_LEN			1
//#define DATE_LEN			1
//#define DAY_LEN				1
//#define ALARM_MONTH_LEN			1
//#define ALARM_DATE_LEN			1
//#define ALARM_HOUR_LEN			1
//#define ALARM_MINUTE_LEN		1
//#define ALARM_SECOND_LEN		1
//#define ALARM_REPEATMODE_LEN	        1

/*********************************************************************
 * TYPEDEFS
 */

/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * Profile Callbacks
 */

// Callback when a characteristic value has changed
typedef void (*timeserviceChange_t)( uint8 paramID );

typedef struct
{
  timeserviceChange_t		pfntimeserviceChange; // Called when characteristic value changes
} timeserviceCBs_t;



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

extern bStatus_t timeservice_AddService( uint32 services );

/*
 * timeservice_RegisterAppCBs - Registers the application callback function.
 *                    Only call this function once.
 *
 *    appCallbacks - pointer to application callbacks.
 */
extern bStatus_t timeservice_RegisterAppCBs(__xdata timeserviceCBs_t *appCallbacks );

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
extern bStatus_t timeservice_SetParameter( uint8 param, uint8 len, __xdata void *value );

/*
 * timeservice_GetParameter - Get a GATT Profile parameter.
 *
 *    param - Profile parameter ID
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 */
extern bStatus_t timeservice_GetParameter( uint8 param, __xdata void *value );


/*********************************************************************
*********************************************************************/

#ifdef __cplusplus
}
#endif

#endif /* TIMESERVICE_H */	
