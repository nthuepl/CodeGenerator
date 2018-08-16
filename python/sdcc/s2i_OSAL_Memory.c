/**************************************************************************************************
  Filename:       s2i_OSAL_Memory.c
  Revised:        $Date: 2010-07-28 08:42:48 -0700 (Wed, 28 Jul 2010) $
  Revision:       $Revision: 23160 $
    
  Description:    This is the binding for OSAL memory control functions. 
    
**************************************************************************************************/

#include "OSAL_Memory.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif

  void osal_mem_init( void ) {
		s2i_call_void(MAP_osal_mem_init);
	}

 /*
  * Setup efficient search for the first free block of heap.
  */
  void osal_mem_kick( void ) {
		s2i_call_void(MAP_osal_mem_kick);
	}

 /*
  * Allocate a block of memory.
  */
#ifdef DPRINTF_OSALHEAPTRACE
  void *osal_mem_alloc_dbg( uint16 size, const char *fname, unsigned lnum );
#define osal_mem_alloc(_size ) osal_mem_alloc_dbg(_size, __FILE__, __LINE__)
#else /* DPRINTF_OSALHEAPTRACE */
  void *osal_mem_alloc( uint16 size );
#endif /* DPRINTF_OSALHEAPTRACE */

 /*
  * Free a block of memory.
  */
#ifdef DPRINTF_OSALHEAPTRACE
  void osal_mem_free_dbg( void *ptr, const char *fname, unsigned lnum );
#define osal_mem_free(_ptr ) osal_mem_free_dbg(_ptr, __FILE__, __LINE__)
#else /* DPRINTF_OSALHEAPTRACE */
  void osal_mem_free(__xdata void *ptr ) {
		s2i_call_p(MAP_osal_mem_free);
	}
#endif /* DPRINTF_OSALHEAPTRACE */

#if ( OSALMEM_METRICS )
 /*
  * Return the maximum number of blocks ever allocated at once.
  */
  uint16 osal_heap_block_max( void ) {
		s2i_call_void(MAP_osal_heap_block_max);
		s2i_ret_u16();
	}

 /*
  * Return the current number of blocks now allocated.
  */
  uint16 osal_heap_block_cnt( void ) {
		s2i_call_void(MAP_osal_heap_block_cnt);
		s2i_ret_u16();
	}
 /*
  * Return the current number of free blocks.
  */
  uint16 osal_heap_block_free( void ) {
		s2i_call_void(MAP_osal_heap_block_free);
		s2i_ret_u16();
	}
 /*
  * Return the current number of bytes allocated.
  */
  uint16 osal_heap_mem_used( void ) {
		s2i_call_void(MAP_osal_heap_mem_used);
		s2i_ret_u16();
	}
#endif

#if defined (ZTOOL_P1) || defined (ZTOOL_P2)
 /*
  * Return the highest number of bytes ever used in the heap.
  */
  uint16 osal_heap_high_water( void ) {
		s2i_call_void(MAP_osal_heap_high_water);
		s2i_ret_u16();
	}
#endif
