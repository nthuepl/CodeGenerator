/**	
 *  @ingroup HAL
 *	@defgroup UART
 *	@{
 *	@file 	epl_hal_uart.h
 *	@brief 	create software uart to write or read
 *	
 *	@author	
 *	@date	
 *  @copyright Copyright 2013 EPLAB National Tsing Hua University. All rights reserved.\n
 *  The information contained herein is confidential property of NTHU. 
 *      The material may be used for a personal and non-commercial use only in connection with 
 *      a legitimate academic research purpose.  
 *      Any attempt to copy, modify, and distribute any portion of this source code or derivative thereof for commercial, 
 *      political, or propaganda purposes is strictly prohibited.  
 *      All other uses require explicit written permission from the authors and copyright holders. 
 *      This copyright statement must be retained in its entirety and displayed 
 *      in the copyright statement of derived source code or systems.
 */


#ifndef EPL_UATR_H
#define EPL_UATR_H

#include "hal_types.h"

/** @cond */
#define HAL_UART_BR_9600   0x00
#define HAL_UART_BR_19200  0x01
#define HAL_UART_BR_38400  0x02
#define HAL_UART_BR_57600  0x03
#define HAL_UART_BR_115200 0x04
#define HI_UINT8(a) (((a) >> 4) & 0x0F)
#define LO_UINT8(a) ((a) & 0x0F)
/** @endcond */

// Function prototypes

/** @brief	Init Uart interface
* 	@return none
*/
void uartInit(int BaudRate);

/** @brief	Write one byte to Uart interface
*
*  @param [in]       write
*     Value to write
*/
void uartWriteByte(char write);

/** @brief	Read one byte from Uart interface
*
* @param [in]       *read
*		Pointer to store the data to write to ADC
*/
void uartReadByte(char *read);

/** @brief	Read one byte from Uart interface
*
* @param [in]       *str
*		Pointer to store the string to write to ADC
*/
void uartWriteString(char *str);

/** @brief	Read one byte from Uart interface
*
* @param [in]       *str
*		Pointer to store the string read from ADC
*/
void uartReadString(char *str);

/** @brief	convert one byte from Hex to String then write to Uart interface
*
* @param [in]       *ptr
*		Pointer to store the string read from User
*/
void uartWriteHex(uint8 *ptr);
#endif

/**
* @}
*/