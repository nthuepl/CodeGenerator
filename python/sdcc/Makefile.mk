# This is the common makefile definition to be included into each 
# architecture for CC2540 or CC2541
# the including Makefile will define ARCH := CC2540  or CC2541.
# it will be executed as if we are in that subdirectory already

CC := sdcc
CFLAGS := --model-small
CFLAGS += --stack-auto
CFLAGS += -DHOST_CONFIG=PERIPHERAL_CFG
LDFLAGS := --code-loc 0xA000
LDFLAGS += --stack-loc 0x80
LDFLAGS += $(CFLAGS)
SRCDIR := ..
INCLUDEFLAGS := -I$(SRCDIR)

CBLDFLAGS := --code-loc 0x8800
CBLDFLAGS += --stack-loc 0x80
CBLDFLAGS += $(CFLAGS)

BINFLAGS := --input-target=ihex
BINFLAGS += --output-target=binary

CFLAGS += -D$(ARCH)
WARNFLAGS := --disable-warning 59 --disable-warning 85

LIB := s2i_OSAL.rel s2i_OSAL_PwrMgr.rel s2i_OSAL_Tasks.rel \
				s2i_OSAL_Timers.rel s2i_accelerometer.rel s2i_devinfoservice.rel\
				s2i_epl_acc_lis331dl.rel s2i_epl_hal_spi.rel s2i_epl_hal_uart.rel\
				s2i_gap.rel s2i_gapbondmgr.rel s2i_gapgattserver.rel s2i_peripheral.rel\
				s2i_gattservapp.rel s2i_simpleBLEPeripheral.rel \
				s2i_simpleGATTprofile.rel

ifeq ($(ARCH), CC2541)
LIB += s2i_timeservice.rel s2i_epl_rtc_m41t62.rel
XRAMLOC := 0xEBD
XRAMSIZE := 0x100
else
XRAMLOC := 0x6AD
XRAMSIZE := 0x100
endif

all:	testacc.bin testhello.bin testrtc.bin testuart.bin testspi.bin testsimpleGATTprofile.bin

sdcc2iar.lib:	$(LIB)
	sdar -rc $@ $^

s2i_%.rel:		$(SRCDIR)/s2i_%.c  $(SRCDIR)/sdcc2iar.h $(SRCDIR)/iar2sdcc.h $(SRCDIR)/bcomdef.h \
		$(SRCDIR)/OSAL.h $(SRCDIR)/linkdb.h $(SRCDIR)/att.h $(SRCDIR)/gatt.h $(SRCDIR)/gatt_uuid.h $(SRCDIR)/peripheral.h\
		$(SRCDIR)/gattservapp.h $(SRCDIR)/gapbondmgr.h
	$(CC) $(INCLUDEFLAGS) $(CFLAGS) $(WARNFLAGS) -c $<

$(SRCDIR)/cc%relay.h:  ../../../code_parser/result_%/dic.py
	python ../genmapdef.py $< "MAP" $@

%.bin:	%.hex
	sdobjcopy --input-target=ihex --output-target=binary $< $@
	
test%.hex:		test%.rel s2i_epl_acc_lis331dl.rel 
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC)--xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@

testrtc.hex:		testrtc.rel s2i_epl_rtc_m41t62.rel 
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@

testhello.hex:	testhello.rel s2i_epl_acc_lis331dl.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@
	
testuart.hex:	testuart.rel s2i_epl_hal_uart.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@

testspi.hex:	testspi.rel s2i_epl_hal_spi.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@
	
testsimpleGATTprofile.hex:	testsimpleGATTprofile.rel s2i_simpleGATTprofile.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@

CodeGeneratorJumpTable.hex:	 CodeGeneratorJumpTable.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@

CodeGeneratorMain.hex: CodeGeneratorMain.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^  sdcc2iar.lib -o $@
	
CodeGeneratorCallBacks.hex: CodeGeneratorCallBacks.rel
	$(CC) $(CBLDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@
	python $(SRCDIR)/sdccmapparser.py CodeGeneratorCallBacks.map "SDCCMAP" $(SRCDIR)/CodeGeneratorJumpTable.h
	make CodeGeneratorJumpTable.bin
	
ChangeDeviceName.hex: ChangeDeviceName.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@

ChangeAdvertData.hex: ChangeAdvertData.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@
	
ChangeScanRspData.hex: ChangeScanRspData.rel
	$(CC) $(LDFLAGS) --xram-loc $(XRAMLOC) --xram-size $(XRAMSIZE) $^ sdcc2iar.lib -o $@
	
%.rel:	$(SRCDIR)/%.c $(SRCDIR)/epl_acc_lis331dl.h $(SRCDIR)/epl_rtc_m41t62.h $(SRCDIR)/epl_hal_uart.h $(SRCDIR)/epl_hal_spi.h \
		$(SRCDIR)/simpleGATTprofile.h $(SRCDIR)/OSAL_Timers.h $(SRCDIR)/bcomdef.h $(SRCDIR)/OSAL.h $(SRCDIR)/linkdb.h \
		$(SRCDIR)/att.h $(SRCDIR)/gatt.h $(SRCDIR)/gatt_uuid.h $(SRCDIR)/gattservapp.h $(SRCDIR)/gapbondmgr.h $(SRCDIR)/peripheral.h \
		$(SRCDIR)/sdcc2iar.h $(SRCDIR)/iar2sdcc.h $(SRCDIR)/cc2540relay.h $(SRCDIR)/cc2541relay.h $(SRCDIR)/cc2540int.h
	$(CC) $(CFLAGS) $(WARNFLAGS) -c $<

clean:
	rm *.asm *.bin *.hex *.lk *.map *.mem *.rel *.rst *.sym *.lst
	
