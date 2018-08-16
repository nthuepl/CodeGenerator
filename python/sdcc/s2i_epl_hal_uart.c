/***********************
 * s2i_epl_hal_uart.c
 *
 * This is the binding file that enables SDCC caller to call IAR API.
 * binding for epl_hal_spi.c
 *
 * Strictly speaking, we could actually just compile epl_hal_uart.c
 * directly using sdcc and it should work. but this is done as an
 * exercise.
	Compile this using
	sdcc -c --stack-auto s2i_epl_hal_uart.c
	You can ignore the warning about parameter not used.
 */

#include "cc2540sfr.h"
#include "epl_hal_uart.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif


void uartInit(int BaudRate)
{
	s2i_call_u16(MAP_uartInit);
}
void uartWriteByte(char write)
{
	s2i_call_u8(MAP_uartWriteByte); // was 0x803 | 0x99A
}
void uartReadByte(__xdata char *read)
{
  while((U0CSR&0x01) || !(U0CSR&0x04));
  *read=U0DBUF;
}
void uartWriteString(const char *str)
{
	s2i_call_p(MAP_uartWriteString); // was 0x809 | 0x9A0
}
void uartReadString(__xdata char *str)
{
  do{
    uartReadByte(str);
  }while(*str++ != '\r');
}

  
void uartWriteHex(__xdata uint8 *ptr)
{
	s2i_call_p(MAP_uartWriteHex); // was 0x80F | 0x9A6
}