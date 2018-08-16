/**************************************************************************************************
  Filename:       s2i_OSAL_Timers.c
  Revised:        $Date: 2011-09-16 19:09:24 -0700 (Fri, 16 Sep 2011) $
  Revision:       $Revision: 27618 $

	Description:    This is the SDCC-toIAR binding file for the OSAL
	Timer definition and manipulation functions.
**************************************************************************************************/

#include "OSAL_Timers.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif

/*********************************************************************
 * FUNCTIONS
 */

  /*
   * Initialization for the OSAL Timer System.
   */
  void osalTimerInit( void ) {
		s2i_call_void(MAP_osalTimerInit);
	}

  /*
   * Set a Timer
   */
  uint8 osal_start_timerEx( uint8 task_id, uint16 event_id, uint32 timeout_value ) {
		s2i_call_u8_u16_u32(MAP_osal_start_timerEx);
		s2i_ret_u8();
	}
  
  /*
   * Set a timer that reloads itself.
   */
  uint8 osal_start_reload_timer( uint8 taskID, uint16 event_id, uint32 timeout_value ) {
		s2i_call_u8_u16_u32(MAP_osal_start_reload_timer);
		s2i_ret_u8();
	}

  /*
   * Stop a Timer
   */
  uint8 osal_stop_timerEx( uint8 task_id, uint16 event_id ) {
		s2i_call_u8_u16(MAP_osal_stop_timerEx);
		s2i_ret_u8();
	}

  /*
   * Get the tick count of a Timer.
   */
  uint32 osal_get_timeoutEx( uint8 task_id, uint16 event_id ) {
		s2i_call_u8_u16(MAP_osal_get_timeoutEx);
		s2i_ret_u32();
	}

  /*
   * Simulated Timer Interrupt Service Routine
   */

  void osal_timer_ISR( void ) {
		// s2i_call_void(MAP_osal_timer_ISR); Neo: not in the map file
	}

  /*
   * Adjust timer tables
   */
  void osal_adjust_timers( void ) {
	//	s2i_call_void(MAP_osal_adjust_timers); Neo: not in the map file
	}

  /*
   * Update timer tables
   */
  void osalTimerUpdate( uint32 updateTime ) {
		s2i_call_u32(MAP_osalTimerUpdate);
	}

  /*
   * Count active timers
   */
  uint8 osal_timer_num_active( void ) {
		// s2i_call_void(MAP_osal_timer_num_active); not in the map file
		// s2i_ret_u8();
	}

  /*
   * Set the hardware timer interrupts for sleep mode.
   * These functions should only be called in OSAL_PwrMgr.c
   */
  void osal_sleep_timers( void ) {
	//	s2i_call_void(MAP_osal_sleep_timers); Neo: not in the map file
	}
  void osal_unsleep_timers( void ) {
		// s2i_call_void(MAP_osal_unsleep_timers); Neo: not in the map file
	}

 /*
  * Read the system clock - returns milliseconds
  */
  uint32 osal_GetSystemClock( void ) {
		s2i_call_void(MAP_osal_GetSystemClock);
		s2i_ret_u32();
	}

  /*
   * Get the next OSAL timer expiration.
   * This function should only be called in OSAL_PwrMgr.c
   */
  uint32 osal_next_timeout( void ) {
		//s2i_call_void(MAP_osal_next_timeout); Neo: not in the map file
		//s2i_ret_u32();
	}
