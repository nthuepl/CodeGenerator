/*
 * CodeGeneratorJumpTable.c
 * This is a jump table with relay, this table will forward program counter to user's callback function
 * that generate code by SDCC.
 */

#include "iar2sdcc.h"
#include "CodeGeneratorJumpTable.h"

void CodeGeneratorJumpTable( void )
{  
	// simpleProfileChangeCB(uint8):\n
	i2s_jumptable_call_u8( SDCCMAP_cg_simpleProfileChangeCB );
	
	// accelEnablerChangeCB(void):\n
	i2s_jumptable_call_void( SDCCMAP_cg_accelEnablerChangeCB );
	
	// battProfileChangeCB(uint8):\n
	i2s_jumptable_call_u8( SDCCMAP_cg_battProfileChangeCB );
	
	// CodeGenerator_EVT_1_CB(void):\n
	i2s_jumptable_call_void( SDCCMAP_cg_EVT_1_CB ); 
	
	// CodeGenerator_EVT_2_CB(void):\n
	i2s_jumptable_call_void( SDCCMAP_cg_EVT_2_CB ); 
	
	// CodeGenerator_EVT_3_CB(void): \n
	i2s_jumptable_call_void( SDCCMAP_cg_EVT_3_CB ); 
	
	// CodeGenerator_EVT_4_CB(void):\n
	i2s_jumptable_call_void( SDCCMAP_cg_EVT_4_CB );
	
	#ifdef CC2541
	// timeserviceChangeCB(uint8):\n
	i2s_jumptable_call_u8( SDCCMAP_cg_timeserviceChangeCB ); 
	#endif
}

