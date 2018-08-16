

#ifndef EcoExecGATTprofile_H
#define EcoExecGATTprofile_H

#ifdef __cplusplus
extern "C"
{
#endif

/*********************************************************************
 * INCLUDES
 */

/*********************************************************************
 * CONSTANTS
 */

// Profile Parameters
#define ECOEXECPROFILE_CHAR1                   0  // RW uint8 - Profile Characteristic 1 value 
#define ECOEXECPROFILE_CHAR2                   1  // RW uint8 - Profile Characteristic 2 value
#define ECOEXECPROFILE_CHAR3                   2  // RW uint8 - Profile Characteristic 3 value
#define ECOEXECPROFILE_CHAR4                   3  // RW uint8 - Profile Characteristic 4 value
#define ECOEXECPROFILE_CHAR5                   4  // RW uint8 - Profile Characteristic 4 value
  
// Service UUID
#define ECOEXECPROFILE_SERV_UUID               0xFCF0
    
// UUID
#define ECOEXECPROFILE_CHAR1_UUID              0xFCF1 /* four bytes Header file - two bytes for sequence number, 
                                                        two byte for segment number (segment = code_length/20 ) */
#define ECOEXECPROFILE_CHAR2_UUID              0xFCF2 /* Code data package */
#define ECOEXECPROFILE_CHAR3_UUID              0xFCF3 /* uint16 FirstCodeMemoryAddress; */ 
#define ECOEXECPROFILE_CHAR4_UUID              0xFCF4 /* Flash Code Flag */
#define ECOEXECPROFILE_CHAR5_UUID              0xFCF5 /* Flash Code Section */
  
// EcoExec Profile Services bit fields
#define ECOEXECPROFILE_SERVICE             0x00000001

// Length of Header File in bytes
#define ECOEXECPROFILE_CHAR1_LEN	   4

// Length of Code Data in bytes
#define ECOEXECPROFILE_CHAR2_LEN           20 
  
// Length of FirstCodeMemory Address in bytes
#define ECOEXECPROFILE_CHAR3_LEN           2 
   
// Length of Flash Code Flag in bytes
#define ECOEXECPROFILE_CHAR4_LEN           1 
  
// Length of Flash Code Section in bytes
#define ECOEXECPROFILE_CHAR5_LEN           1
/*********************************************************************
 * TYPEDEFS
 */
extern uint16 EcoExecProfileConnHandle;
  
/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * Profile Callbacks
 */

// Callback when a characteristic value has changed
typedef NULL_OK void (*EcoExecProfileChange_t)( uint8 paramID );

typedef struct
{
  EcoExecProfileChange_t        pfnEcoExecProfileChange;  // Called when characteristic value changes
} EcoExecProfileCBs_t;

    

/*********************************************************************
 * API FUNCTIONS 
 */


/*
 * EcoExecProfile_AddService- Initializes the EcoExec GATT Profile service by registering
 *          GATT attributes with the GATT server.
 *
 * @param   services - services to add. This is a bit map and can
 *                     contain more than one service.
 */

extern bStatus_t EcoExecProfile_AddService( uint32 services );

/*
 * EcoExecProfile_RegisterAppCBs - Registers the application callback function.
 *                    Only call this function once.
 *
 *    appCallbacks - pointer to application callbacks.
 */
extern bStatus_t EcoExecProfile_RegisterAppCBs( EcoExecProfileCBs_t *appCallbacks );

/*
 * EcoExecProfile_SetParameter - Set a EcoExec GATT Profile parameter.
 *
 *    param - Profile parameter ID
 *    len - length of data to right
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 */
extern bStatus_t EcoExecProfile_SetParameter( uint8 param, uint8 len, void *value );
  
/*
 * EcoExecProfile_GetParameter - Get a EcoExec GATT Profile parameter.
 *
 *    param - Profile parameter ID
 *    value - pointer to data to write.  This is dependent on
 *          the parameter ID and WILL be cast to the appropriate 
 *          data type (example: data type of uint16 will be cast to 
 *          uint16 pointer).
 */
extern bStatus_t EcoExecProfile_GetParameter( uint8 param, void *value );

/*********************************************************************
*********************************************************************/

#ifdef __cplusplus

}
#endif

#endif /* ECOEXECGATTPROFILE_H */
