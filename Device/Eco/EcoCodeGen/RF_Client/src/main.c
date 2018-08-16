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

#define RF_LENGTH 28
#define MESSAGE_LENGTH 64

void puts(char *s);

void store_cpu_rate(unsigned long hz);
void mdelay(unsigned int msec);
void send_ack_feedback( unsigned char *buf, unsigned char event );
void interrupt_rf() __interrupt 10;
/*NOTE:
		The total number of bits in a ShockBurst RF package may not exceed 256!
		Maximum length of payload section is hence given by:
				DATAx_W(bits) = 256 - ADDR_W - CRC
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
{ 0x00, 0x00, 0x0f, 0x01, 0x01 }, /* addr1, host addr */
{ 0x61 }, /* 24-bit address, 8-bit CRC */
{ 0x6f, 0x15 } };
struct rf_config *cfg = &rf_data;
//char dst_addr[3] = { 0xf2, 0xf2, 0xf2 };
char dst_addr[3] = { 0x02, 0x02, 0x02 };
//extern char rf_buf[RF_BUF_LEN];
unsigned char codegenerator_status;
unsigned char HeaderFile[4];
unsigned char __xdata Message[MESSAGE_LENGTH];
//unsigned char Message[MESSAGE_LENGTH];
int i;

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

	/* enable channel 1 receive data interrupt */
	EX4 = 1;
	/* sample LEB blink */
	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(500);
	}

	puts("\n----------------------------");
	/* code generator status initial */
	codegenerator_status = IDLE;
	puts( "\n>Idle\n" );

	while(1) {
		CE = 1; /* Activate RX or TX mode */

		if( codegenerator_status == RUNCODE ){
			/* P0 ^= 0x20 */
			puts("Exec\n");
			__asm
				lcall #_Message
			__endasm ;
			puts("ret\n");

			send_ack_feedback( Message, 1);
//			/* chang to transmiter mode */
//			cfg->rf_prog[1] = 0x14;
//			rf_configure( cfg );
//
//			/* send feedback packet */
//			mdelay(700);
//			rf_send(dst_addr, 3, Message, RF_LENGTH );
//			puts("send result: \n");
//			for( i = 0; i < RF_LENGTH; i++ ){
//				putc( ( (Message[i]>>4) & 0x0f ) > 9 ? ( (Message[i]>>4) & 0xff )+ 55 :( (Message[i]>>4) & 0xff )+ 48 );
//				putc( ( Message[i] & 0x0f ) > 9 ? ( Message[i] & 0x0f ) + 55  : ( Message[i] & 0x0f ) + 48 );
//				putc( ' ' );
//			}
//
//			/* chang to receiver mode */
//			cfg->rf_prog[1] = 0x15;
//			rf_configure( cfg );

			codegenerator_status = IDLE;
			puts("\n----------------------------");
			puts( "\n>Idle\n" );
		}
	}
}

void send_ack_feedback( unsigned char *buf, unsigned char event )
{
	/* chang to transmiter mode */
	cfg->rf_prog[1] = 0x14;
	rf_configure( cfg );

	/* send ack packet */
	mdelay(700);	/* wait for dongle */
	rf_send(dst_addr, 3, buf, RF_LENGTH );
	if( event == 0 )
		puts("send ack: \n");
	else
		puts("send result: \n");

	for( i = 0; i < RF_LENGTH; i++ ){
		putc( ( (buf[i]>>4) & 0x0f ) > 9 ? ( (buf[i]>>4) & 0xff )+ 55 :( (buf[i]>>4) & 0xff )+ 48 );
		putc( ( buf[i] & 0x0f ) > 9 ? ( buf[i] & 0x0f ) + 55  : ( buf[i] & 0x0f ) + 48 );
		putc( ' ' );
	}
	/* chang to receiver mode */
	cfg->rf_prog[1] = 0x15;
	rf_configure( cfg );

} // end send_ack_feedback function

void interrupt_rf() __interrupt 10
{
	static unsigned char counter;

	while (DR1) {
		switch( codegenerator_status ){
		case IDLE:
			counter=0;
			codegenerator_status = HEADERPACKET;
			puts("\n>Header Packet\n");
		case HEADERPACKET:
			if( counter < 4 ){ 		/* header buffer length 4 bytes */
				HeaderFile[counter++] = spi_write_then_read(0);
				putc( ( (HeaderFile[counter-1]>>4) & 0x0f ) > 9 ? ( (HeaderFile[counter-1]>>4) & 0xff )+ 55 :( (HeaderFile[counter-1]>>4) & 0xff )+ 48 );
				putc( ( HeaderFile[counter-1] & 0x0f ) > 9 ? ( HeaderFile[counter-1] & 0x0f ) + 55  : ( HeaderFile[counter-1] & 0x0f ) + 48 );
				putc( ' ' );
			}
			else if( counter < RF_LENGTH ){
				spi_write_then_read(0);
				counter++;
			}
			else{
				counter = 0;
				send_ack_feedback( HeaderFile, 0 );
				codegenerator_status = CODEPACKET;
				puts("\n\r>Code Packet\n");
			}
			break;
		case CODEPACKET:
			if( counter < HeaderFile[3] ){
				Message[counter++] = spi_write_then_read(0);
				putc( ( (Message[counter-1]>>4) & 0x0f ) > 9 ? ( (Message[counter-1]>>4) & 0xff )+ 55 :( (Message[counter-1]>>4) & 0xff )+ 48 );
				putc( ( Message[counter-1] & 0x0f ) > 9 ? ( Message[counter-1] & 0x0f ) + 55  : ( Message[counter-1] & 0x0f ) + 48 );
				putc( ' ' );

				if( ( counter % RF_LENGTH == 0) ){
					if( (counter / RF_LENGTH) != HeaderFile[2] ){
						send_ack_feedback( Message, 0 );
//						/* chang to transmiter mode */
//						cfg->rf_prog[1] = 0x14;
//						rf_configure( cfg );
//						/* send ack packet */
//						mdelay(700);
//						rf_send(dst_addr, 3, Message, RF_LENGTH );
//						puts("send ack: \n");
//						for( i = 0; i < RF_LENGTH; i++ ){
//							putc( ( (Message[i]>>4) & 0x0f ) > 9 ? ( (Message[i]>>4) & 0xff )+ 55 :( (Message[i]>>4) & 0xff )+ 48 );
//							putc( ( Message[i] & 0x0f ) > 9 ? ( Message[i] & 0x0f ) + 55  : ( Message[i] & 0x0f ) + 48 );
//							putc( ' ' );
//						}
//						/* chang to receiver mode */
//						cfg->rf_prog[1] = 0x15;
//						rf_configure( cfg );

					}
					else{
						codegenerator_status = RUNCODE;
						puts("\n\r>Run Code\n");
					}
				}
			}
			break;
		} /* end switch case */
	} // DR1, data ready from receiver 1

	/* clean up rf interrupt */
	CE = 0;
	EXIF &= ~0x40;
}
