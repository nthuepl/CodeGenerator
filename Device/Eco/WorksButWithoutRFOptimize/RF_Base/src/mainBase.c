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

#define RF_LENGTH 28
#define MESSAGE_LENGTH 41

void store_cpu_rate(unsigned long hz);
void mdelay(unsigned int msec);
void serial_init(unsigned int baud);
char getc();
void puts(char *s);
void putc(char c);
void interrupt_serial() interrupt 4;
/*NOTE:
		The total number of bits in a ShockBurst RF package may not exceed 256!
		Maximum length of payload section is hence given by:
				DATAx _W(bits) = 256 - ADDR _W - CRC
Where:
	ADDR_W: length of RX address set in configuration word bit [23:18]
	CRC: check sum, 8 or 16 bits set in configuration word bit [17]
	PRE: preamble, 8 bits are automatically included
*/
struct rf_config rf_data = {
{ 0x00 }, /* data2 width */
//{ 0x08 }, /* data1 width */
{ 0xE0 }, /* 256 - 24 - 8 = 224 - code generator data1 width in bits */
{ 0x00, 0x00, 0x00, 0x00, 0x00 }, /* addr2 */
{ 0x00, 0x00, 0x02, 0x02, 0x02 }, /* addr1, host addr */
{ 0x61 }, /* 24-bit address, 8-bit CRC */
{ 0x6f, 0x14 } };

struct rf_config *cfg = &rf_data;
char dst_addr[3] = { 0x0f, 0x01, 0x01 };

char MessageBUF[MESSAGE_LENGTH];
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

	EA = 1;
	ES = 1;
	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(500);
	}
	//rf_send(dst_addr, 3, &led_status, 1);
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

//	blink_led();
//	mdelay(1000);
//	blink_led();



	if(RI) {
		RI = 0; /* software clear serial receive interrupt*/
		cmd = SBUF; /* SBUF serial port data buffer */

		if( cmd == 'h' ){

			MessageBUF[0] = 0x00;
			MessageBUF[1] = 0x01;
			MessageBUF[2] = 0x01;
			MessageBUF[3] = 0x08;

			for( i = 4; i < MESSAGE_LENGTH; i++ )
				MessageBUF[i] = 0;
		}

		if( cmd == 'c' ){
/*			blink_led();
			P0 ^= 0x20
			63 80 20 22 iram address*/
			MessageBUF[0] = 0x63;
			MessageBUF[1] = 0x80;
			MessageBUF[2] = 0x20;
			MessageBUF[3] = 0x22;
			for( i = 4; i < MESSAGE_LENGTH; i++ )
				MessageBUF[i] = 0;
		}

		if( cmd == 's' ){
			rf_send(dst_addr, 3, MessageBUF, RF_LENGTH );
			puts("Send: \n\r");
			for( i = 0; i < RF_LENGTH; i++ ){
				putc(MessageBUF[i]+48);
				putc(' ');
			}
			puts("\n\r");
		}
//		if(cmd == 'f') {
//			led_status = cmd;
//			rf_send(dst_addr, 3, &led_status, 1);
//		}
//		else if(cmd == 's') {
//			led_status = cmd;
//			rf_send(dst_addr, 3, &led_status, 1);
//		}

	}

}
