#if defined( CC2541) || defined( CC2541S )
#include <ioCC2541.h>
#else // CC2540
#include <ioCC2540.h>
#endif // CC2541 || CC2541S

#include "epl_hal_uart.h"

void uartInit(int BaudRate)
{
  PERCFG &= ~0x01;
  P0SEL |=0x0C;
  U0CSR |=0xC0;
  switch(BaudRate)
  {
  case HAL_UART_BR_9600:
    U0GCR |=0x08;
    U0BAUD = 0x3B;
    break;
  case HAL_UART_BR_19200:
    U0GCR |=0x09;
    U0BAUD = 0x3B;
    break;
  case HAL_UART_BR_38400:
    U0GCR |=0x0A;
    U0BAUD = 0x3B;
    break;
  case HAL_UART_BR_57600:
    U0GCR |=0x0A;
    U0BAUD = 0xD8;
    break;
  case HAL_UART_BR_115200:
    U0GCR |=0x0B;
    U0BAUD = 0xD8;
    break;
  default:
    break;
  }

  
}
void uartWriteByte(char write)
{
  U0DBUF = write;
  while((U0CSR&0x01) || !(U0CSR&0x02));
  U0CSR&=~0x02;
}
void uartReadByte(char *read)
{
  while((U0CSR&0x01) || !(U0CSR&0x04));
  *read=U0DBUF;
}
void uartWriteString(char *str)
{
  while(*str != 0)
  {
    uartWriteByte(*str++);
  }
}
void uartReadString(char *str)
{
  do{
    uartReadByte(str);
  }while(*str++ != '\r');
}

  
void uartWriteHex(uint8 *ptr)
{
  if( HI_UINT8(*ptr) < 10 )
    uartWriteByte(48+HI_UINT8(*ptr));
  else
    uartWriteByte(55+HI_UINT8(*ptr));
  
  if( LO_UINT8(*ptr) < 10 )
  {
    uartWriteByte(48+LO_UINT8(*ptr));
    //uartWriteString("small than 10.");
  }
  else
    uartWriteByte(55+LO_UINT8(*ptr));
  
  uartWriteByte(' ');  
}