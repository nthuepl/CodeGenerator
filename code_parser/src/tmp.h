/*	@file 	I2C.h
 *	@brief 	create sofeware I2C to write or read
 *	
 *	@author	zeroping.tw@gmail.com
 *	@date	2012.11.19
 */
#ifndef EPL_HAL_I2C_H
#define EPL_HAL_I2C_H

#ifdef __cplusplus
extern "C"
{
#endif
  
/***************************************************************************
***************************************************************************/
// <ioCC2540.h>
// <hal_types.h>
// <hal_defs.h>

#define W2SCL                     P0_6
#define W2SDA                     P0_7
  
#define HIGH                      1  
#define LOW                       0 

/*	@brief	Wait for some time to get proper I2C timing
 *	
 *	@param	none	
 *	@return	none
 */ 
void I2CWait(void);

/*	@brief	Initial I2C	
 *	
 *	@param	none	
 *	@return	none
 */
void I2CInit(void);

/*	@brief	Generates a START(S) condition on the bus.
 *	
 *	@param	none	
 *	@return	none
 */
void I2CStart(void);

/*	@brief	Generates a STOP(P) condition on the bus.
 *	
 *	@param	none	
 *	@return	none
 */
void I2CStop(void);

/*	@brief	Send a Byte to the slave
 *
 *	@param uint8 byte - 8 bit date to the slave
 *	@return ack - receive from the slave
 */
unsigned char I2CSentByte(uint8 bytedata);
  
/*	@brief	Receive a Byte from the slave
 *
 *	@param bool ack - 0 or 1 to do ack
 *	@return data - read from the slave
 */
unsigned char I2CReceiveByte( uint8 ack);
/***************************************************************************
***************************************************************************/
  
#ifdef __cplusplus
}
#endif

#endif