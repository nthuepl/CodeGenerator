# Makefile for a bunch of tests
# define architecture for CC2540 or CC2541
# most of the real content is now moved to each $(ARCH)/Makefile, which
# includes the Makefile.mk at this level for the real definition.
#

all:
	@echo "	do not make at this directory (though you can still make clean). instead, "
	@echo "	cd CC2540; make; cd .."
	@echo "	cd CC2541; make; cd .."
	@echo "	python runflash.py CC2540/testacc.bin '' (for example)"


clean:
	rm *.asm *.bin *.hex *.ihx *.lk *.lnk *.lst *.map *.mem *.rel *.rst *.sym
