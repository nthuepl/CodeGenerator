
/**************************************************************************************************
 *                                           Includes
 **************************************************************************************************/

#include "EcoExec.h"
#include "epl_hal_uart.h"

#if defined( CC2541) || defined( CC2541S )
#include <ioCC2541.h>
#else // CC2540
#include <ioCC2540.h>
#endif // CC2541 || CC2541S



/**************************************************************************************************
 * FUNCTIONS
 **************************************************************************************************/


//unsigned char Test( unsigned char event )
//{
//  P2_1 ^= 1;
//  return event;
//}



//#pragma location="CODEGENERATOR_1"
void halProcessAlarmInterrupt( void )
{   
  P2_1 ^= 1;
}

//#pragma location="CODEGENERATOR_2"
void halProcessFreeFallInterrupt( void )
{
  uartWriteString("FreeFall\n\r");
  P2_2 ^= 1;
}




/**************************************************************************************************
                                           CALL-BACKS
**************************************************************************************************/


 

/***************************************************************************************************
 *                                    INTERRUPT SERVICE ROUTINE
 ***************************************************************************************************/



/*************************************************************************************************
**************************************************************************************************/