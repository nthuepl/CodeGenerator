/**************************************************************************************************
  Filename:       s2i_epl_acc_lis331dl.c

	This is the binding file that enables SDCC caller to call IAR API.
	binding for epl_acc_lis331dl.c.

	Compile this using
	sdcc -c --stack-auto s2i_epl_acc_lis331dl.c
	actually, also with either -DCC2540 or 
	You can ignore the warning about parameter not used.
**************************************************************************************************/

#include "epl_acc_lis331dl.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif

/** \brief	Initialize SPI interface and LIS331DL-H accelerometer
*
* This will initialize the SPI interface and LIS331DL-H accelerometer
*
*/
void accInit(void)
{
	s2i_call_void(MAP_accInit); // was 0x7CD | 0x964
}

/** \brief	Write one byte to a sensor register
*
* Write one byte to a sensor register
*
* \param[in]       reg
*     Register address
* \param[in]       val
*     Value to write
*/
void accWriteReg(uint8 reg, uint8 val)
{
	s2i_call_u8_u8(MAP_accWriteReg); // was 0x7D3 | 0x96A
}


/** \brief	Read one byte from a sensor register
*
* Read one byte from a sensor register
*
* \param[in]       reg
*     Register address
* \param[in]       *pVal
*     Pointer to variable to put read out value
*/
void accReadReg(uint8 reg, __xdata uint8 *pVal)
{
	s2i_call_u8_p(MAP_accReadReg); // was 0x7D9 | 0x970
}

/** \brief	Read multi byte from a sensor register
*
* Read multi byte from a sensor register
*
* \param[in]       reg
*     Register address
* \param[in]       *pVal
*     Pointer to variable to put read out value
* \param[in]       count
*     read bytes count
*/
void accReadMultiReg(uint8 reg, __xdata uint8 *pVal, uint8 count)
{
		// PC140502 This function is not in the map file!
}

/** \brief	Read x, y and z acceleration data
*
* Read x, y and z acceleration data in one operation.
* NOTE: No sensor access must be made immidiately folloing this operation
* without enabling the last Wait call.
*
* \param[in]       *pXVal
*     Pointer to variable to put read out X acceleration
* \param[in]       *pYVal
*     Pointer to variable to put read out Y acceleration
* \param[in]       *pZVal
*     Pointer to variable to put read out Z acceleration
*/

void accReadAcc(__xdata int16 *pXVal, __xdata int16 *pYVal, __xdata int16 *pZVal)
{
	s2i_call_p_p_p(MAP_accReadAcc); // was 0x7DF | 0x976
}

/** \brief	Read x, y and z acceleration data
*
* Read x, y and z acceleration data in one operation.
* NOTE: No sensor access must be made immidiately folloing this operation
* without enabling the last Wait call.
*
* \param[in]       *pXVal
*     Pointer to variable to put read out X,Y and Z acceleration
*/

void accReadAllAcc(__xdata uint8 *pVal)
{
		// PC140502 this function is not in mapfile!
    // accReadMultiReg(ACC_LIS331DL_OUT_XL, (uint8*)pVal, 6);
}

void accSetFreeFallEvent( void )
{
	s2i_call_void(MAP_accSetFreeFallEvent); // was 0x97C
}
