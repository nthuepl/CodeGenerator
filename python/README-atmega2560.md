This is the README for ATmega2560 

It is under development, using a lot of the same code from cc2540 code.

Test case:

		% python -i atmega2560mcu.py
		>>> mcu.PORTA
		>>> mcu.PORTA + 1
		>>> mcu.PORTA + 78
		>>> mcu.PORTA + mcu.PORTB
		>>> mcu.PORTA + 1 + mcu.PORTB
		>>> mcu.PORTA - 1
		>>> mcu.PORTA - mcu.PORTB
		>>> mcu.PORTA + mcu.PORTB - 1
		>>> 1 - mcu.PORTA
		>>> mcu.PORTA & mcu.PORTB
		>>> mcu.PORTA | mcu.PORTB
		>>> mcu.PORTA & 0xff
		>>> mcu.PORTA & 0x0
		>>> mcu.PORTA | 0xff
		>>> mcu.PORTA | 0x00
		>>> mcu.PORTA & 0x12
		>>> mcu.PORTA | 0x12
		>>> mcu.PORTA == 23
		>>> mcu.PORTA == mcu.PORTB
