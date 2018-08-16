/**************************************************************************************************
  Filename:       s2i_OSAL_Tasks.h
  Revised:        $Date: 2007-10-28 18:41:49 -0700 (Sun, 28 Oct 2007) $
  Revision:       $Revision: 15799 $

  Description:    This file contains the binding for OSAL Task definition and manipulation functions.


**************************************************************************************************/



/*********************************************************************
 * INCLUDES
 */
#include "hal_types.h"
#include "OSAL_Tasks.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#endif

/*********************************************************************
 * MACROS
 */



/*********************************************************************
 * FUNCTIONS
 */

/*
 * Call each of the tasks initailization functions.
 */
void osalInitTasks( void ) {
		s2i_call_void(MAP_osalInitTasks);
}

/*********************************************************************
*********************************************************************/
