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


#define RF_LENGTH 28
#define MESSAGE_LENGTH 41

void store_cpu_rate(unsigned long hz);
void mdelay(unsigned int msec);
void interrupt_rf() __interrupt 10;
void puts(char *s);
void putc(char c);

struct rf_config rf_data = {
{ 0x00 }, /* data2 width */
//{ 0x08 }, /* data1 width */
{ 0xE0 }, /* 256 - 24 - 8 = 224 - code generator data1 width in bits */
{ 0x00, 0x00, 0x00, 0x00, 0x00 }, /* addr2 */
{ 0x00, 0x00, 0xf2, 0xf2, 0xf2 }, /* addr1, host addr */
{ 0x61 }, /* 24-bit address, 8-bit CRC */
{ 0x6f, 0x15 } };
struct rf_config *cfg = &rf_data;
//char dst_addr[3] = { 0xf2, 0x02, 0x02 };
unsigned char counter = 1;

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

	EA = 1;
	EX4 = 1;
	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(500);
	}

	puts("Listener startup.\n\r");
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

void interrupt_rf() __interrupt 10
{
	while (DR1) {
		if( counter  < RF_LENGTH ){
			if( counter == 0 )
				puts( "FeedBack: \n" );
			Meassage[counter++] = spi_write_then_read(0);
			putc( ( (Meassage[counter-1]>>4) & 0xff ) + 48 );
			putc( ( Meassage[counter-1] & 0x0f ) + 48 );
			putc( ' ' );
		}
		else{
			counter = 1;
			puts("\n");
		}
	} // DR1, data ready from receiver 1

	/* clean up rf interrupt */
	CE = 0;
	EXIF &= ~0x40;
}
