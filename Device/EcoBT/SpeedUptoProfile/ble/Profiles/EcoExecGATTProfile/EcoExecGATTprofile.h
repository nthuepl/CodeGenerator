

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
  
// Service UUID
#define ECOEXECPROFILE_SERV_UUID               0xFCF0
    
// UUID
#define ECOEXECPROFILE_CHAR1_UUID              0xFCF1 
  
// EcoExec Profile Services bit fields
#define ECOEXECPROFILE_SERVICE             0x00000001

// Length of Header File in bytes
#define ECOEXECPROFILE_CHAR1_LEN	   1


/* six bytes Header file - 
two bytes sequence number, 
two bytes segment number, 
one bytes Flash Code Flag,
one bytes Flash Code Section*/
   
/* Code data package 20 bytes*/
   
#define HEADER_LEN              8
#define MAIN_SECTIOIN           4
#define CODEDATA_LEN            20  
#define RAMCODE_CALL            0xaa
#define FLASHCODE_CALL          0xbb
#define STOP_CALLBACKS          0xcc


/*********************************************************************
 * TYPEDEFS
 */
extern uint16 EcoExecProfileConnHandle;
extern uint8 Message[500];  
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


/*********************************************************************
*********************************************************************/

#ifdef __cplusplus

}
#endif

#endif /* ECOEXECGATTPROFILE_H */
