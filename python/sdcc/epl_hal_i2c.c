/*	@file 	I2C.h
 *	@brief 	create sofeware I2C to write or read
 *	
 *	@author	zeroping.tw@gmail.com
 *	@date	2012.11.19
 */    
#include "cc2540sfr.h"
#include "hal_types.h"
#include "epl_hal_i2c.h"

/*	@brief	Wait for some time to get proper I2C timing
 *	
 *	@param	none	
 *	@return	none
 */
void I2CWait()
{
  int i;
  for(i=0; i<2000; i++);
}

/*	@brief	Initial I2C	
 *	
 *	@param	none	
 *	@return	none
 */
void I2CInit()
{
  // 0x04 0000 0100
  // 0x08 0000 1000
  P0DIR |= (0x40 | 0x80);
  W2SDA = HIGH;
  W2SCL = HIGH;
}

/*	@brief	Generates a START(S) condition on the bus.
 *	
 *	@param	none	
 *	@return	none
 */
void I2CStart()
{
  // SDA high->low while SCL=high
  W2SDA = HIGH;
  W2SCL = HIGH;
  I2CWait();
  W2SDA = LOW;
  I2CWait();
  W2SCL = LOW;
  I2CWait();
}

/*	@brief	Generates a STOP(P) condition on the bus.
 *	
 *	@param	none	
 *	@return	none
 */
void I2CStop()
{
  //SDA low->high while SCL=high
  W2SDA = LOW;
  I2CWait();
  W2SCL = HIGH;
  I2CWait();
  W2SDA = HIGH;
}

/*	@brief	Send a Byte to the slave
 *
 *	@param uint8 byte - 8 bit date to the slave
 *	@return ack - receive from the slave
 */
unsigned char I2CSentByte(uint8 bytedata)
{
  unsigned char i;
  unsigned char ack;
  uint8 tempdata;
  
  W2SDA = HIGH;;
  for(i=0; i<8; i++)
  {
    tempdata = bytedata << i;
    if(tempdata & 0x80)
        W2SDA = HIGH;
    else
        W2SDA = LOW;
    
    W2SCL = HIGH;
    I2CWait();
    W2SCL = LOW;
    I2CWait();  
  }
  W2SDA = HIGH;
  I2CWait();
  W2SCL = HIGH;
  I2CWait();

  // receive acknowledge
  ack = W2SDA;
  W2SCL = LOW;
  I2CWait();
  
  return ack;  
}

/*	@brief	Receive a Byte from the slave
 *
 *	@param bool ack - 0 or 1 to do ack
 *	@return data - read from the slave
 */
unsigned char I2CReceiveByte( uint8 ack)
{
  unsigned char i;
  uint8 bytedata = 0;
  
  for(i=0; i<8; i++)
  {
    W2SCL = HIGH;
    I2CWait();

    bytedata = bytedata << 1;
    if(W2SDA == HIGH)
      bytedata |= 0x01;
    
    W2SCL = LOW;
    I2CWait();
  }
  // send acknowledge
  

  W2SDA = ack;
  I2CWait();
  W2SCL = HIGH;
  I2CWait();
  W2SCL = LOW; 
  W2SDA = HIGH;   // after an ack clock, the data output by master receiver must
                  // pull up the SDA!!!
  return bytedata;
}