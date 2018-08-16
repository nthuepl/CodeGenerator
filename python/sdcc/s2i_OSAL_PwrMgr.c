/**************************************************************************************************
  Filename:       s2i_OSAL_PwrMgr.h
  Revised:        $Date: 2007-10-28 18:41:49 -0700 (Sun, 28 Oct 2007) $
  Revision:       $Revision: 15799 $

  Description:    This file contains the binding for OSAL Power Management API.

**************************************************************************************************/

/*********************************************************************
 * INCLUDES
 */
#include "hal_types.h"
#include  "OSAL_PwrMgr.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#endif


/*********************************************************************
 * FUNCTIONS
 */

  /*
   * Initialize the power management system.
   *   This function is called from OSAL.
   *  So, there is really no reason to call this function
	 *  from SDCC, but we include it anyway.
   */
  void osal_pwrmgr_init( void ) {
		s2i_call_void(MAP_osal_pwrmgr_init);
	}

  /*
   * This function is called by each task to state whether or not this
   * task wants to conserve power. The task will call this function to
   * vote whether it wants the OSAL to conserve power or it wants to
   * hold off on the power savings. By default, when a task is created,
   * its own power state is set to conserve. If the task always wants
   * to converse power, it doesn't need to call this function at all.
   * It is important for the task that changed the power manager task
   * state to PWRMGR_HOLD to switch back to PWRMGR_CONSERVE when the
   * hold period ends.
   */
  uint8 osal_pwrmgr_task_state( uint8 task_id, uint8 state ) {
		s2i_call_u8_u8(MAP_osal_pwrmgr_task_state);
		s2i_ret_u8();
	}

  /*
   * This function is called on power-up, whenever the device characteristic
   * change (ex. Battery backed coordinator). This function works with the timer
   * to set HAL's power manager sleep state when power saving is entered.
   * This function should be called form HAL initialization. After power up
   * initialization, it should only be called from NWK or ZDO.
   */
  // void osal_pwrmgr_device( uint8 pwrmgr_device );

  /*
   * This function is called from the main OSAL loop when there are
   * no events scheduled and shouldn't be called from anywhere else.
	 *
	 * So, we shouldn't need to call this function from SDCC.
   */
  // void osal_pwrmgr_powerconserve( void );

/*********************************************************************
*********************************************************************/
