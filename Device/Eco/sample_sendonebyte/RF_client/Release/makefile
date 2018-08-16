################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: LED_BLINK_RF.ihex

# Tool invocations
LED_BLINK_RF.ihex: $(RELS) $(USER_RELS)
	@echo 'Building target: $@'
	@echo 'Invoking: SDCC Linker'
	sdcc -L"C:\Program Files\EPL_LIB/E1_LIB/lib" -o"LED_BLINK_RF.ihex" $(RELS) $(USER_RELS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(C_DEPS)$(RELS)$(EXECUTABLES) LED_BLINK_RF.ihex
	-@echo ' '

post-build:
	-python "C:\Program Files\EPL_LIB/E1_LIB/utils/eeprep.py"   "LED_BLINK_RF.ihex"  "RF_client.hex"
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets
