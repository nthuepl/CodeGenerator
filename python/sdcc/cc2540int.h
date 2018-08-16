/*
 * cc2540int.h
 *
 * interrupt vector for CC2540 (and CC2541)
 */

#ifndef CC2540INT_H
#define CC2540INT_H
#define VECT(num,addr)   addr

/* ------------------------------------------------------------------------------------------------
 *                                        Interrupt Vectors
 * ------------------------------------------------------------------------------------------------
 */
#define  RFERR_VECTOR   VECT(  0, 0x03 )   /*  RF TX FIFO Underflow and RX FIFO Overflow   */
#define  ADC_VECTOR     VECT(  1, 0x0B )   /*  ADC End of Conversion                       */
#define  URX0_VECTOR    VECT(  2, 0x13 )   /*  USART0 RX Complete                          */
#define  URX1_VECTOR    VECT(  3, 0x1B )   /*  USART1 RX Complete                          */
#define  ENC_VECTOR     VECT(  4, 0x23 )   /*  AES Encryption/Decryption Complete          */
#define  ST_VECTOR      VECT(  5, 0x2B )   /*  Sleep Timer Compare                         */
#define  P2INT_VECTOR   VECT(  6, 0x33 )   /*  Port 2 Inputs and USB                       */
#define  UTX0_VECTOR    VECT(  7, 0x3B )   /*  USART0 TX Complete                          */
#define  DMA_VECTOR     VECT(  8, 0x43 )   /*  DMA Transfer Complete                       */
#define  T1_VECTOR      VECT(  9, 0x4B )   /*  Timer 1 (16-bit) Capture/Compare/Overflow   */
#define  T2_VECTOR      VECT( 10, 0x53 )   /*  Timer 2 (MAC Timer)                         */
#define  T3_VECTOR      VECT( 11, 0x5B )   /*  Timer 3 (8-bit) Capture/Compare/Overflow    */
#define  T4_VECTOR      VECT( 12, 0x63 )   /*  Timer 4 (8-bit) Capture/Compare/Overflow    */
#define  P0INT_VECTOR   VECT( 13, 0x6B )   /*  Port 0 Inputs                               */
#define  UTX1_VECTOR    VECT( 14, 0x73 )   /*  USART1 TX Complete                          */
#define  P1INT_VECTOR   VECT( 15, 0x7B )   /*  Port 1 Inputs                               */
#define  RF_VECTOR      VECT( 16, 0x83 )   /*  RF General Interrupts                       */
#define  WDT_VECTOR     VECT( 17, 0x8B )   /*  Watchdog Overflow in Timer Mode             */

// // Interrupt Vectors

// #define RFERR_VECTOR    0   // RF TX FIFO underflow and RX FIFO overflow.
// #define ADC_VECTOR      1   // ADC end of conversion
// #define URX0_VECTOR     2   // USART0 RX complete
// #define URX1_VECTOR     3   // USART1 RX complete
// #define ENC_VECTOR      4   // AES encryption/decryption complete
// #define ST_VECTOR       5   // Sleep Timer compare
// #define P2INT_VECTOR    6   // Port 2 inputs
// #define UTX0_VECTOR     7   // USART0 TX complete
// #define DMA_VECTOR      8   // DMA transfer complete
// #define T1_VECTOR       9   // Timer 1 (16-bit) capture/compare/overflow
// #define T2_VECTOR       10  // Timer 2 (MAC Timer)
// #define T3_VECTOR       11  // Timer 3 (8-bit) capture/compare/overflow
// #define T4_VECTOR       12  // Timer 4 (8-bit) capture/compare/overflow
// #define P0INT_VECTOR    13  // Port 0 inputs
// #define UTX1_VECTOR     14  // USART1 TX complete
// #define P1INT_VECTOR    15  // Port 1 inputs
// #define RF_VECTOR       16  // RF general interrupts
// #define WDT_VECTOR      17  // Watchdog overflow in timer mode

/* ------------------------------------------------------------------------------------------------
 *                                     Interrupt Alias
 * ------------------------------------------------------------------------------------------------
 */
#define  USB_VECTOR     P2INT_VECTOR /*  USB Interrupt vector, alias for P2INT_VECTOR        */


/* ------------------------------------------------------------------------------------------------
 *                                      SFR Bit Alias
 * ------------------------------------------------------------------------------------------------
 */
#define  USBIF     P2IF              /*  USB Interrupt Flag                                  */
/*       USBIE     P2IE              ,   not in a bit addressable register                   */

#endif
