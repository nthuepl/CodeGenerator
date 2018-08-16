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
all: RF_Base.ihex

# Tool invocations
RF_Base.ihex: $(RELS) $(USER_RELS)
	@echo 'Building target: $@'
	@echo 'Invoking: SDCC Linker'
	sdcc -L"C:\Program Files\EPL_LIB/E1_LIB/lib" -o"RF_Base.ihex" $(RELS) $(USER_RELS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(C_DEPS)$(RELS)$(EXECUTABLES) RF_Base.ihex
	-@echo ' '

post-build:
	-python "C:\Program Files\EPL_LIB/E1_LIB/utils/eeprep.py"   "RF_Base.ihex"  "RF_Base.hex"
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets
