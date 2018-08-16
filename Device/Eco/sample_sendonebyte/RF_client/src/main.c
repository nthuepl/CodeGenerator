/*
 * main.c
 *
 *  Created on: 2014/1/21
 *      Author: EPL
 */

#include <eco/reg24e1.h>
#include <eco/eco_sys.h>
#include <rf/rf.h>
#include <spi/spi.h>
#include <serial/serial.h>

/* code generator status define */
#define IDLE		  0x00
#define HEADERPACKET  0x01
#define CODEPACKET    0x02
#define RUNCODE       0x04

#define RF_LENGTH 32
#define MESSAGE_LENGTH 41

void store_cpu_rate(unsigned long hz);
void mdelay(unsigned int msec);
void interrupt_rf() interrupt 10;

struct rf_config rf_data = {
{ 0x00 }, /* data2 width */
{ 0x08 }, /* data1 width */
{ 0x00, 0x00, 0x00, 0x00, 0x00 }, /* addr2 */
{ 0x00, 0x00, 0x0f, 0x01, 0x01 }, /* addr1, host addr */
{ 0x61 }, /* 24-bit address, 8-bit CRC */
{ 0x6f, 0x15 } };
struct rf_config *cfg = &rf_data;
char dst_addr[3] = { 0x02, 0x02, 0x02 };
extern char rf_buf[RF_BUF_LEN];
unsigned char codegenerator_status;
unsigned char HeaderFile[4];
unsigned char Meassage[MESSAGE_LENGTH];

void main()
{
	int i;
	store_cpu_rate(16);
	/* init serial */
	serial_init(19200);
	/* init led */
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;
	/* init rf */
	rf_init();
	rf_configure(cfg);

	/* code generator status initial */
	codegenerator_status = IDLE;

	EA = 1;
	EX4 = 1;
	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(500);
	}

	puts("Slave startup.\n\r");
	while(1) {
		CE = 1;
		//rf_wait_msg();
		//led_status = rf_buf[0];
/*		if(led_status == 'f') {
			blink_led();
			mdelay(200);
		}
		else if(led_status == 's') {
			blink_led();
			mdelay(500);
		}
		else
			blink_led();*/
	}
}

void interrupt_rf() interrupt 10
{

	char counter=0, led_status;
	blink_led();
	mdelay(500);

	counter=0;
	while (DR1) {
		rf_buf[counter++] = spi_write_then_read(0);	/* clock in data */
	} // DR1, data ready from receiver 1

	led_status = rf_buf[0];
	putc(led_status);
	puts("\n\r");

	/* clean up rf interrupt */
	CE = 0;
	EXIF &= ~0x40;
}
