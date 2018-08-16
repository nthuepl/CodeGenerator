/*
 * mainBase.c
 *
 *  Created on: 2014/1/22
 *      Author: NeoLai
 */

#include <eco/reg24e1.h>
#include <eco/eco_sys.h>
#include <serial/serial.h>
#include <rf/rf.h>

#define RF_LENGTH 32
#define MESSAGE_LENGTH 41

void store_cpu_rate(unsigned long hz);
void mdelay(unsigned int msec);
void serial_init(unsigned int baud);
char getc();
void puts(char *s);
void putc(char c);
void interrupt_serial() interrupt 4;

struct rf_config rf_data = {
{ 0x00 }, /* data2 width */
{ 0x08 }, /* data1 width */
//{ 0xff }, /* 32 bytes - code generator data1 width in bits */
{ 0x00, 0x00, 0x00, 0x00, 0x00 }, /* addr2 */
{ 0x00, 0x00, 0x02, 0x02, 0x02 }, /* addr1, host addr */
{ 0x61 }, /* 24-bit address, 8-bit CRC */
{ 0x6f, 0x14 } };

struct rf_config *cfg = &rf_data;
char dst_addr[3] = { 0x0f, 0x01, 0x01 };

char led_status;

unsigned char MessageBUF[MESSAGE_LENGTH];
unsigned char i = 0, index = 0;

void main()
{

	store_cpu_rate(16);
	/* init serial */
	serial_init(19200);
	/* init led */
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;
	/* init rf */
	rf_init();
	rf_configure(cfg);

	led_status = 'f';
	EA = 1;
	ES = 1;
	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(500);
	}
	//rf_send(dst_addr, 3, &led_status, 1);
	puts("Master startup.\n\r");
	while(1) {
		/*if(led_status == 'f') {
			blink_led();
			mdelay(500);
			rf_send(dst_addr, 3, &led_status, 1);
		}
		else if(led_status == 's') {
			blink_led();
			mdelay(500);
			rf_send(dst_addr, 3, &led_status, 1);
		}
		else*/
//			blink_led();
//			mdelay(500);
	}
}

void interrupt_serial() interrupt 4
{
	char cmd;

	blink_led();
//	mdelay(1000);
//	blink_led();

	if(RI) {
		RI = 0; /* software clear serial receive interrupt*/
		cmd = SBUF; /* SBUF serial port data buffer */

		//if(cmd == 'f') {
			led_status = cmd;
			rf_send(dst_addr, 3, &led_status, 1);
		//}
		//else if(cmd == 's') {
		//	led_status = cmd;
		//	rf_send(dst_addr, 3, &led_status, 1);
		//}

	}

}
