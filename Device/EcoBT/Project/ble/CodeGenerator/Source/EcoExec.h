
#ifndef ECOEXEC_H
#define ECOEXEC_H

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
#define HAL_RTC_ALARM_BIT    0x01 // 0000 0001
   
  
/* display setup */
/* P0_3 TXD pin4*/
#define sendInstruction (P0_3=0)
#define sendData (P0_3=1)

/* P0_2 RXD pin5*/	
#define writesignal P0_2=0
#define readsignal P0_2=1

/* P0_0 AN0 pin6 */
#define enableSignal P0_0 

#define setDisplayData( value ){ \
	P1_3 = value&0x01;\
	P1_4 = (value>>1)&0x01;\
	P1_5 = (value>>2)&0x01;\
	P1_6 = (value>>3)&0x01;\
	P1_7 = (value>>4)&0x01;\
	P0_4 = (value>>5)&0x01;\
	P0_5 = (value>>6)&0x01;\
	P0_1 = (value>>7)&0x01;\
}

/*********************************************************************
 * GLOBAL VARIABLES
 */



/*********************************************************************
 * MACROS
 */

   
/*********************************************************************
 * FUNCTIONS
 */
void halProcessAlarmInterrupt( void );
void halProcessFreeFallInterrupt( void );

/*********************************************************************
*********************************************************************/

#ifdef __cplusplus
}
#endif

#endif /* ECOEXEC_H */
