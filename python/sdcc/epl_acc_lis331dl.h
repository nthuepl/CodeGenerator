/**
 * 
 * @ingroup Module
 * @defgroup Acc
 * @{
 * @file epl_acc_lis331dl.h
 * 
 *
 * @author AnPing
 * @date 2012/3/12
 * @copyright 
 * Copyright (c) 2013 EPLAB National Tsing Hua University . All rights reserved.\n
 * The information contained herein is confidential property of NTHU. 
 * The material may be used for a personal and non-commercial use only in connection with 
 * a legitimate academic research purpose.  
 * Any attempt to copy, modify, and distribute any portion of this source code or derivative thereof for commercial, 
 * political, or propaganda purposes is strictly prohibited.  
 * All other uses require explicit written permission from the authors and copyright holders. 
 * This copyright statement must be retained in its entirety and displayed 
 * in the copyright statement of derived source code or systems.
 */

#ifndef EPL_ACC_LIS331DL_H
#define EPL_ACC_LIS331DL_H

#include "hal_types.h"

#include "epl_hal_spi.h"


//***********************************************************************************
// Defines
/** @cond */  
#define SCK          P1_5
#define MISO         P1_7
#define MOSI         P1_6
#define CS           P1_1
#define CS_DISABLED     1
#define CS_ENABLED      0

// Data ready pin
#define ACC_DATA_READY  (P1_2 == 1)
/** @endcond */  

/** An enum describing register map in LIS331DL.
 */
typedef enum {
	ACC_LIS331DL_WHO_AM_I		= 0x0F,	/**< Device identification register                                                                    */
	ACC_LIS331DL_CTRL_REG1		= 0x20,	/**< LIS331DL control register 1                                                                       */
	ACC_LIS331DL_CTRL_REG2		= 0x21,	/**< LIS331DL control register 2                                                                       */
	ACC_LIS331DL_CTRL_REG3		= 0x22,	/**< LIS331DL control register 3                                                                       */
	ACC_LIS331DL_HP_FILTER_RESET    = 0x23,	/**< Dummy register. High pass-filter                                                                  */
	ACC_LIS331DL_STATUS_REG		= 0x27,	/**< Status register                                                                                   */
	ACC_LIS331DL_OUT_XL		= 0x28, /**< X axis data (L)                                                                                   */
	ACC_LIS331DL_OUT_XH		= 0x29,	/**< X axis data (H)(2's complement number)                                                            */
	ACC_LIS331DL_OUT_YL		= 0x2A, /**< Y axis data (L)                                                                                   */
	ACC_LIS331DL_OUT_YH		= 0x2B,	/**< Y axis data (2's complement number)                                                               */
	ACC_LIS331DL_OUT_ZL		= 0x2C, /**< Z axis data (L)                                                                                   */
	ACC_LIS331DL_OUT_ZH	        = 0x2D,	/**< Z axis data (2's complement number)                                                               */
	ACC_LIS331DL_FF_WU_CFG_1	= 0x30,	/**< And/Or combination of interrupt event. Enable interrupt generation on X, Y, Z Low and High event. */
	ACC_LIS331DL_FF_WU_CFG_1_ACK1   = 0x31,	/**< Free-fall and wake-up source register.                                                            */
	ACC_LIS331DL_FF_WU_THS_1	= 0x32,	/**< Resetting mode selection and Free-fall/Wake-up threshold.                                         */
	ACC_LIS331DL_FF_WU_DURATION_1	= 0x33,	/**< Duration register for Free-Fall/Wake-Up interrupt 1.                                              */
	ACC_LIS331DL_FF_WU_CFG_2	= 0x34,	/**< And/Or combination of interrupt event. Enable interrupt generation on X, Y, Z Low and High event. */
	ACC_LIS331DL_FF_WU_CFG_2_ACK2	= 0x35,	/**< Interrupt Active on high and low of X, Y, Z axis.                                                 */
	ACC_LIS331DL_FF_WU_THS_2	= 0x36, /**< Resetting mode selection and Free-fall/Wake-up threshold.                                         */
	ACC_LIS331DL_FF_WU_DURATION_2	= 0x37,	/**< Duration register for Free-Fall/Wake-up interrupt 2.                                              */
        ACC_LIS331DL_CLICK_CFG          = 0x38,	/**< Enable interrupt generation on double or single click event of X, Y, Z axis.                      */                                                                           
        ACC_LIS331DL_CLICK_SRC_ACK	= 0x39,	/**< Interrupt Active, Double or Single click on X, Y, Z axis event.                                   */
        ACC_LIS331DL_CLICK_THSY_X	= 0x3B,	/**< Click Threshold on X and Y axis. From 0.5g(0001) to 7.5g(1111) with step of 0.5g.                 */
        ACC_LIS331DL_CLICK_THSZ         = 0x3C,	/**< Click Threshold on Z axis. From 0.5g(0001) to 7.5g(1111) with step of 0.5g.                       */
        ACC_LIS331DL_CLICK_TIME_LIMIT	= 0x3D, /**< From 0 to 127.5 msec with step of 0.5 msec.                                                       */
        ACC_LIS331DL_CLICK_LATENCY	= 0x3E, /**< From 0 to 255 msec with step of 1 msec.                                                           */
        ACC_LIS331DL_CLICK_WINDOW	= 0x3F  /**< From 0 to 255 msec with step of 1 msec.                                                           */
} epl_acc_lis331dlH_reg;


/** An enum describing full measurement scale.
 */
typedef enum {
	ACC_LIS331DL_2G_SCALE = 0x00,		/**< +-2G mode */
	ACC_LIS331DL_8G_SCALE = 0x01		/**< +-8G mode */
} epl_acc_lis331dl_scale;

/** An enum describing full measurement scale.
 */
typedef enum {
	ACC_LIS331DL_DATA_RATE_100HZ = 0x00,	/**< 100Hz output data rate */
	ACC_LIS331DL_DATA_RATE_400HZ = 0x01		/**< 400Hz output data rate */
} epl_acc_lis331dl_data_rate;


/** @cond */  
// CMA3000 addressing space
#define WHO_AM_I        (0x00<<2)	
#define REVID           (0x01<<2)	
#define CTRL            (0x02<<2)   
#define STATUS          (0x03<<2)   
#define RSTR            (0x04<<2)   
#define INT_STATUS      (0x05<<2)   
#define DOUTX           (0x06<<2)   
#define DOUTY           (0x07<<2)   
#define DOUTZ           (0x08<<2)   
#define MDTHR           (0x09<<2)   
#define MDFFTMR         (0x0A<<2)   
#define FFTHR           (0x0B<<2)   

// CTRL register definitions
#define RANGE_2G        0x80
#define RANGE_8G        0x00

#define INT_ACTIVE_LOW  0x40
#define INT_ACTIVE_HIGH 0x00

#define MODE_PD         0x00
#define MODE_100HZ_MEAS 0x02
#define MODE_400HZ_MEAS 0x04
#define MODE_40HZ_MEAS  0x06
#define MODE_10HZ_MD    0x08
#define MODE_100HZ_FALL 0x0A
#define MODE_400HZ_FALL 0x0C

#define INT_DIS         0x01
#define INT_EN          0x00

/** @endcond */  





//***********************************************************************************
// Macros

// Wait 1+1/3*t [us]
/** @def WAIT_1_3US(t)
*		Delay for t CPU circle
*/
#define WAIT_1_3US(t)                   \
    do{ uint8 i;                        \
        for (i = 0; i<t; i++)     \
            __asm__("NOP");                 \
    }while(0)



//***********************************************************************************
// Function prototypes

/** @brief	Initialize SPI interface and LIS331DL-H accelerometer
*
*/
void accInit(void);

/** @brief	Write one byte to a sensor register
*
* @param [in]       reg
*     Register address
* @param [in]       val
*     Value to write
*/
void accWriteReg(uint8 reg, uint8 val);

/** @brief	Read one byte from a sensor register
*
* @param [in]       reg
*     Register address
* @param [in]       *pVal
*     Pointer to variable to put read out value
*/

void accReadReg(uint8 reg, __xdata uint8 *pVal);

/** @brief	Read multi byte from a sensor register
*
* @param [in]       reg
*     Register address
* @param [in]       *pVal
*     Pointer to variable to put read out value
* @param [in]       count
*     read bytes count
*/

void accReadMultiReg(uint8 reg, __xdata uint8 *pVal, uint8 count);


/** @brief	Read x, y and z acceleration data
*
* Read x, y and z acceleration data in one operation.
* NOTE: No sensor access must be made immidiately folloing this operation
* without enabling the last Wait call.
*
* @param [in]       *pXVal
*     Pointer to variable to put read out X acceleration
* @param [in]       *pYVal
*     Pointer to variable to put read out Y acceleration
* @param [in]       *pZVal
*     Pointer to variable to put read out Z acceleration
*/

void accReadAcc(__xdata int16 *pXVal, __xdata int16 *pYVal, __xdata
		int16 *pZVal);

/** @brief	Read x, y and z acceleration data
*
* Read x, y and z acceleration data in one operation.
* NOTE: No sensor access must be made immidiately folloing this operation
* without enabling the last Wait call.
*
* @param [in]       *pXVal
*     Pointer to variable to put read out X,Y and Z acceleration
*/
void accReadAllAcc(__xdata uint8 *pVal);

void accSetFreeFallEvent( void );


#endif
