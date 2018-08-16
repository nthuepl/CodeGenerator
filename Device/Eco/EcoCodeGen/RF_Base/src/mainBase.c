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
#include <spi/spi.h>

#define RF_LENGTH 28
#define MESSAGE_LENGTH RF_LENGTH
#define CODE_BUF 64

void store_cpu_rate(unsigned long hz);
void mdelay(unsigned int msec);
void serial_init(unsigned int baud);
char getc();
void puts(char *s);
void putc(char c);
void interrupt_serial() __interrupt 4;
void interrupt_rf() __interrupt 10;

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
//char dst_addr[3] = { 0xf2, 0xf2, 0xf2 };
char MessageBUF[MESSAGE_LENGTH];
unsigned char code_segment = 0;
unsigned char i = 0, counter = 0;

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

	/* enable all interrupt */
	EA = 1;
	/* enable serial port interrupt */
	ES = 1;
	/* enable channel 1 receive data interrupt */
	EX4 = 1;

	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(500);
	}
	puts("\n----------------------------");
	puts( "\nStartup.\n" );
	while(1)
	{

	}
} //  end main

void interrupt_rf() __interrupt 10
{
	static unsigned char fb_counter;

//	if( code_segment > 1 )
//		puts("Ack: " );
//	else
//		puts("Feedback: ");

	while (DR1) {
		MessageBUF[fb_counter++] = spi_write_then_read(0);
		putc( MessageBUF[fb_counter-1]);
		//putc( ( (MessageBUF[fb_counter-1]>>4) & 0x0f ) > 9 ? ( (MessageBUF[fb_counter-1]>>4) & 0x0f )+ 55 :( (MessageBUF[fb_counter-1]>>4) & 0x0f )+ 48 );
		//putc( ( MessageBUF[fb_counter-1] & 0x0f ) > 9 ? ( MessageBUF[fb_counter-1] & 0x0f ) + 55  : ( MessageBUF[fb_counter-1] & 0x0f ) + 48 );
		//putc( ' ' );

		if( fb_counter == RF_LENGTH ){
			/* chang to transmiter mode */
			cfg->rf_prog[1] = 0x14;
			rf_configure( cfg );
			fb_counter = 0;
//			code_segment--;
//			puts("\n----------------------------\n");
		}
	} // DR1, data ready from receiver 1

	/* clean up rf interrupt */
	CE = 0;
	EXIF &= ~0x40;
}

void interrupt_serial() __interrupt 4
{
	static unsigned char header_counter;
	static unsigned char code_counter;

	if(RI) {
		/* software clear serial receive interrupt*/
		RI = 0;

		/* recevice header */
		if( header_counter < (RF_LENGTH-1) ){
			if( header_counter == 3 ){
				code_counter = SBUF;
				code_segment = code_counter/RF_LENGTH;
				MessageBUF[header_counter++] = code_counter;
			}
			else{
				MessageBUF[header_counter++] = SBUF;
			}
		}
		else if( header_counter == (RF_LENGTH-1) ){
			MessageBUF[header_counter++] = SBUF;
			rf_send( dst_addr, 3, MessageBUF, RF_LENGTH );

			/* chang to receiver mode */
			cfg->rf_prog[1] = 0x15;
			rf_configure( cfg );
			CE = 1; /* Activate RX or TX mode */


//			puts("Send header: \n\r");
//			for( i = 0; i < MESSAGE_LENGTH; i++ ){
//				putc( ( (MessageBUF[i]>>4) & 0x0f ) > 9 ? ( (MessageBUF[i]>>4) & 0x0f )+ 55 :( (MessageBUF[i]>>4) & 0x0f )+ 48 );
//				putc( ( MessageBUF[i] & 0x0f ) > 9 ? ( MessageBUF[i] & 0x0f ) + 55  : ( MessageBUF[i] & 0x0f ) + 48 );
//				putc( ' ' );
//			}
//			puts("\n\r");

		}
		else{
				/* recevice code */
				if( code_counter % RF_LENGTH == 0 ){
					MessageBUF[0] = SBUF;
					code_counter--;
				}
				else{
					MessageBUF[RF_LENGTH-(code_counter%RF_LENGTH)] = SBUF;
					code_counter--;
					/* send code */
					if( code_counter % RF_LENGTH == 0 ){
						rf_send(dst_addr, 3, MessageBUF, RF_LENGTH );
						code_segment--;
//						puts("Send code: \n\r");
//						for( i = 0; i < MESSAGE_LENGTH; i++ ){
//							putc( ( (MessageBUF[i]>>4) & 0x0f ) > 9 ? ( (MessageBUF[i]>>4) & 0x0f )+ 55 :( (MessageBUF[i]>>4) & 0x0f )+ 48 );
//							putc( ( MessageBUF[i] & 0x0f ) > 9 ? ( MessageBUF[i] & 0x0f ) + 55  : ( MessageBUF[i] & 0x0f ) + 48 );
//							putc( ' ' );
//						}
//						puts("\n\r");

//						if( code_segment > 1 )
//							puts("wait ack.\n" );
//						else
//							puts("wait FB.\n" );

						/* chang to receiver mode */
						cfg->rf_prog[1] = 0x15;
						rf_configure( cfg );
						CE = 1; /* Activate RX or TX mode */
					}

					/* reset header counter */
					if( code_counter == 0 )
						header_counter = 0;
				}

		}
	}

}
