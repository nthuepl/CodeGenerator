
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

void GeneratorStartPoint( void );
void blinkLED(void);

unsigned char Test( unsigned char event );
/*********************************************************************
*********************************************************************/

#ifdef __cplusplus
}
#endif

#endif /* ECOEXEC_H */
