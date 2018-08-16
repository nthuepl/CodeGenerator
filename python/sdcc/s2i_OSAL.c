/******************************************************************************
  Filename:     s2i_OSAL.h
  Revised:      $Date: 2012-02-17 15:07:16 -0800 (Fri, 17 Feb 2012) $
  Revision:     $Revision: 29376 $

  Description:  This API allows the software components in the Z-Stack to be
                written independently of the specifics of the operating system,
                kernel, or tasking environment (including control loops or
                connect-to-interrupt systems).


  Copyright 2004-2011 Texas Instruments Incorporated. All rights reserved.

  IMPORTANT: Your use of this Software is limited to those specific rights
  granted under the terms of a software license agreement between the user
  who downloaded the software, his/her employer (which must be your employer)
  and Texas Instruments Incorporated (the "License").  You may not use this
  Software unless you agree to abide by the terms of the License. The License
  limits your use, and you acknowledge, that the Software may not be modified,
  copied or distributed unless embedded on a Texas Instruments microcontroller
  or used solely and exclusively in conjunction with a Texas Instruments radio
  frequency transceiver, which is integrated into your product. Other than for
  the foregoing purpose, you may not use, reproduce, copy, prepare derivative
  works of, modify, distribute, perform, display or sell this Software and/or
  its documentation for any purpose.

  YOU FURTHER ACKNOWLEDGE AND AGREE THAT THE SOFTWARE AND DOCUMENTATION ARE
  PROVIDED “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED,
  INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, TITLE,
  NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL
  TEXAS INSTRUMENTS OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER CONTRACT,
  NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR OTHER
  LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
  INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE
  OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT
  OF SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
  (INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.

  Should you have any questions regarding your right to use this Software,
  contact Texas Instruments Incorporated at www.TI.com.
******************************************************************************/
#include "sdcc2iar.h"
#include "OSAL.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#endif

/*********************************************************************
 * GLOBAL VARIABLES
 */

/*********************************************************************
 * FUNCTIONS
 */

/*** Message Management ***/

  /*
   * Task Message Allocation
   */
  __xdata uint8 * osal_msg_allocate(uint16 len ) {
		s2i_call_u16(MAP_osal_msg_allocate); // was 0x695 | 0x82C
		s2i_ret_u16();
	}

  /*
   * Task Message Deallocation
   */
  uint8 osal_msg_deallocate(__xdata uint8 *msg_ptr ) {
		s2i_call_p(MAP_osal_msg_deallocate); // was 0x69B | 0x832
		s2i_ret_u8();
	}

  /*
   * Send a Task Message
   */
  uint8 osal_msg_send( uint8 destination_task, __xdata uint8 *msg_ptr ) {
		s2i_call_u8_p(MAP_osal_msg_send); // was 0x6A1 | 0x838
		s2i_ret_u8();
	}

  /*
   * Push a Task Message to head of queue
   */
  uint8 osal_msg_push_front( uint8 destination_task, __xdata uint8 *msg_ptr ) {
#ifdef MAP_osal_msg_push_front
		s2i_call_u8_p(MAP_osal_msg_push_front);
#endif
		s2i_ret_u8();
	}

  /*
   * Receive a Task Message
   */
  __xdata uint8 *osal_msg_receive( uint8 task_id ) {
		s2i_call_u8(MAP_osal_msg_receive); // was 0x6AD | 0x844
		s2i_ret_u16();
	}

  /*
   * Find in place a matching Task Message / Event.
   */
  __xdata osal_event_hdr_t *osal_msg_find(uint8 task_id, uint8 event) {
#ifdef MAP_osal_event_hdr_t
		s2i_call_u8_u8(MAP_osal_event_hdr_t);
#endif
		s2i_ret_u16();
	}

  /*
   * Enqueue a Task Message
   */
  void osal_msg_enqueue( __xdata osal_msg_q_t *q_ptr, __xdata void *msg_ptr ) {
		s2i_call_p_p(MAP_osal_msg_enqueue); // was 0x6B3 | 0x84A
	}


  /*
   * Enqueue a Task Message Up to Max
   */
  uint8 osal_msg_enqueue_max(__xdata osal_msg_q_t *q_ptr, __xdata void *msg_ptr, uint8 max ) {
#ifdef MAP_osal_msg_enqueue_max
		s2i_call_p_p_u8(MAP_osal_msg_enqueue_max);
#endif
	}

  /*
   * Dequeue a Task Message
   */
  __xdata void *osal_msg_dequeue(__xdata osal_msg_q_t *q_ptr ) {
#ifdef MAP_osal_msg_dequeue
		s2i_call_p(MAP_osal_msg_dequeue);
#endif
		s2i_ret_u16();
	}

  /*
   * Push a Task Message to head of queue
   */
  void osal_msg_push(__xdata osal_msg_q_t *q_ptr, __xdata void *msg_ptr ) {
		s2i_call_p_p(MAP_osal_msg_push); // was 0x6B9 | 0x850
	}

  /*
   * Extract and remove a Task Message from queue
   */
  void osal_msg_extract(__xdata osal_msg_q_t *q_ptr, __xdata void *msg_ptr, __xdata void *prev_ptr ) {
		s2i_call_p_p_p(MAP_osal_msg_extract); // was 0x6BF | 0x856
	}


/*** Task Synchronization  ***/

  /*
   * Set a Task Event
   */
  uint8 osal_set_event( uint8 task_id, uint16 event_flag ) {
		s2i_call_u8_u16(MAP_osal_set_event); // was 0x6C5 | 0x85C
		s2i_ret_u8();
	}


  /*
   * Clear a Task Event
   */
  uint8 osal_clear_event( uint8 task_id, uint16 event_flag ) {
		s2i_call_u8_u16(MAP_osal_clear_event); // was 0x6CB | 0x862
		s2i_ret_u8();
	}


/*** Interrupt Management  ***/

  /*
   * Register Interrupt Service Routine (ISR)
   */
  uint8 osal_isr_register( uint8 interrupt_id, void (*isr_ptr)(__xdata uint8* ) ) {
#ifdef MAP_osal_isr_register
		s2i_u8_p(MAP_osal_isr_register);
#endif
		s2i_ret_u8();
	}

  /*
   * Enable Interrupt
   */
  uint8 osal_int_enable( uint8 interrupt_id ) {
#ifdef MAP_osal_int_enable
		s2i_call_u8(MAP_osal_int_enable);
#endif
		s2i_ret_u8();
	}

  /*
   * Disable Interrupt
   */
  uint8 osal_int_disable( uint8 interrupt_id ) {
		s2i_call_u8(MAP_osal_int_disable); // was 0x6D1 | 0x868
		s2i_ret_u8();
	}


/*** Task Management  ***/

  /*
   * Initialize the Task System
   */
  uint8 osal_init_system( void ) {
		s2i_call_void(MAP_osal_init_system); // was 0x6D7 | 0x86E
		s2i_ret_u8();
	}

  /*
   * System Processing Loop
   */
#if defined (ZBIT)
  extern __declspec(dllexport)  void osal_start_system( void );
#else
  void osal_start_system( void ) {
		s2i_call_void(MAP_osal_start_system); // was 0x6DD | 0x874
	}
#endif

  /*
   * One Pass Throu the OSAL Processing Loop
   */
  void osal_run_system( void ) {
		s2i_call_void(MAP_osal_run_system); // was 0x6E3 | 0x87A
	}

  /*
   * Get the active task ID
   */
  uint8 osal_self( void ) {
#ifdef MAP_osal_self
		s2i_call_void(MAP_osal_self);
#endif
		s2i_ret_u8();
	}


/*** Helper Functions ***/

  /*
   * String Length
   */
  int osal_strlen(__xdata char *pString ) {
		s2i_call_p(MAP_osal_strlen); // was 0x66B | 0x802
		s2i_ret_u16();
	}

  /*
   * Memory copy
   */
  __xdata void *osal_memcpy(__xdata void* dest, __xdata const void GENERIC * src, unsigned int len) {
		s2i_call_p_p_u16(MAP_osal_memcpy); // was 0x671 | 0x808
		s2i_ret_u16();
	}

  /*
   * Memory Duplicate - allocates and copies
   */
  __xdata void *osal_memdup(__xdata const void GENERIC *src, unsigned int len ) {
		s2i_call_p_u16(MAP_osal_memdup); // was 0x67D | 0x814
		s2i_ret_u16();
	}

  /*
   * Reverse Memory copy
   */
  __xdata void *osal_revmemcpy(__xdata  void* a, __xdata const void GENERIC * b, unsigned int c) {
		s2i_call_p_p_u16(MAP_osal_revmemcpy); // was 0x677 | 0x80E
		s2i_ret_u16();
	}

  /*
   * Memory compare
   */
  uint8 osal_memcmp(__xdata const void GENERIC *src1, __xdata const void GENERIC *src2, unsigned int len ) {
		s2i_call_p_p_u16(MAP_osal_memcmp); // was 0x683 | 0x81A
		s2i_ret_u8();
	}

  /*
   * Memory set
   */
  __xdata void *osal_memset(__xdata void *dest, uint8 value, int len ) {
		s2i_call_p_u8_u16(MAP_osal_memset); // was 0x689 | 0x820
		s2i_ret_u16();
	}

  /*
   * Build a uint16 out of 2 bytes (0 then 1).
   */
  uint16 osal_build_uint16(__xdata uint8 *swapped ) {
#ifdef MAP_osal_build_uint16
		s2i_call_p(MAP_osal_build_uint16);
#endif
		s2i_ret_u16();
	}

  /*
   * Build a uint32 out of sequential bytes.
   */
  uint32 osal_build_uint32(__xdata uint8 *swapped, uint8 len ) {
#ifdef MAP_osal_build_uint32
		s2i_call_p_u8(MAP_osal_build_uint32);
#endif
		s2i_ret_u32();
	}

  /*
   * Convert long to ascii string
   */
  #if !defined ( ZBIT ) && !defined ( ZBIT2 ) && !defined (UBIT)
    extern uint8 *_ltoa( uint32 l, uint8 * buf, uint8 radix );
  #endif

  /*
   * Random number generator
   */
  uint16 osal_rand( void ) {
		s2i_call_void(MAP_osal_rand); // was 0x68F | 0x826
		s2i_ret_u16();
	}

  /*
   * Buffer an uint32 value - LSB first.
   */
  __xdata uint8* osal_buffer_uint32(__xdata uint8 *buf, uint32 val ) {
#ifdef MAP_osal_buffer_uint32
		s2i_call_p_u32(MAP_osal_buffer_uint32);
#endif
		s2i_ret_u16();
	}

  /*
   * Buffer an uint24 value - LSB first
   */
  __xdata uint8* osal_buffer_uint24(__xdata uint8 *buf, uint24 val ) {
#ifdef MAP_osal_buffer_uint24
		s2i_call_p_u24(MAP_osal_buffer_uint24);
#endif
		s2i_ret_u16();
	}

  /*
   * Is all of the array elements set to a value?
   */
  uint8 osal_isbufset(__xdata uint8 *buf, uint8 val, uint8 len ) {
		s2i_call_p_u8_u8(MAP_osal_isbufset); // was 0x6E9 | 0x880
		s2i_ret_u8();
	}

