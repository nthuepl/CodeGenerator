################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/mainBase.c 

C_DEPS += \
./src/mainBase.d 

RELS += \
./src/mainBase.rel 


# Each subdirectory must supply rules for building sources it contributes
src/%.rel: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: SDCC Compiler'
	sdcc -c -I"C:\Program Files\EPL_LIB/E1_LIB/include" --model-small -o"$@" "$<" && \
	echo -n $(@:%.rel=%.d) $(dir $@) > $(@:%.rel=%.d) && \
	sdcc -c -MM -I"C:\Program Files\EPL_LIB/E1_LIB/include" --model-small  "$<" >> $(@:%.rel=%.d)
	@echo 'Finished building: $<'
	@echo ' '


