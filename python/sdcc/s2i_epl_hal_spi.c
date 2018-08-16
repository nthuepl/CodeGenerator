/***********************
 * s2i_epl_hal_spi.c
 * This is the binding file that enables SDCC caller to call IAR API.
 * binding for epl_hal_spi.c
 *
 * Strictly speaking, we could actually just compile epl_hal_spi.c
 * directly using sdcc and it should work. but this is done as an
 * exercise.
* Compile this using
* sdcc -c --stack-auto s2i_epl_acc_lis331dl.c
* actually need to provide macro for -DCC2540 or -DCC2541 from 
* command line to extract this from 
* You can ignore the warning about parameter not used.
 */

#include "epl_hal_spi.h"
#include "sdcc2iar.h"
#ifdef CC2540
#include "cc2540relay.h"
#elif defined(CC2541)
#include "cc2541relay.h"
#else
#error "Need to define macro either CC2540 or CC2541"
#endif


void spiWriteByte(uint8 write)
{
	s2i_call_u8(MAP_spiWriteByte); // was 0x7EB | 0x982
}



/** \brief	Read one byte from SPI interface
*
* Read one byte from SPI interface
*
* \param[in]       read
*     Read out value
* \param[in]       write
*     Value to write
*/
void spiReadByte(__xdata uint8 *read, uint8 write)
{
	s2i_call_p_u8(MAP_spiReadByte); // was 0x7F1 | 0x988
}

/**
*
*       @brief Init SPI interface
*
*/
void spiInit(uint8 MODE){
	s2i_call_u8(MAP_spiInit); // was 0x7F7 | 0x98E
}

/***************************************************************************************************
*                                    INTERRUPT SERVICE ROUTINE
***************************************************************************************************/
/**
* @brief   SPI 1 slave RX sevice route
*
* @param	None
*
* @return 	None
*/
//HAL_ISR_FUNCTION( halSPI1RxIsr, URX1_VECTOR )
//{
//  static uint8 read = 0x00;
//  
//  spiReadByte( &read[read_idx], 0xF0);
//  
//}

