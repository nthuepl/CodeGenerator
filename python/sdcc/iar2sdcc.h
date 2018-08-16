/*
 * iar2sdcc.h
 *
 * This is the macro definition for writing callbacks compiled in SDCC to be
 * called by IAR.  Note that unlike sdcc2iar, here we put these directly
 * into the function entry and exit to make the parameter values work
 * out. So, there is no callee involved in these cases.  But it must be
 * enveloped with the proper code; and in either case, we waste 3 bytes
 * on the istack for the frame pointer and return address anyway.
 */


#ifndef IAR2SDCC_H
#define IAR2SDCC_H

/* code pointer type -- assuming --small-model,
 * so code pointer is 16 bits,
 * and this pointer resides in xdata. hope it compiles.
 */
#define XSP_L  "0x18"
#define XSP_H  "(0x18+1)"


extern __xdata unsigned char * __data __at (XSP_L) XSP;

#define i2s_adjust_stack(offset) { \
	__asm \
		MOV A, SP \
	__endasm; \
	__asm__("ADD A, #" #offset "\n"); \
	__asm \
		MOV SP, A \
	__endasm; \
}

#define i2s_call_void() {\
	__asm \
		;; need to make room on stack for [ret H:L][bp], \
		;; so that the offset works correctly, even though we assume the \
		;; user code will not ever depend on it \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_void() { \
	i2s_adjust_stack(-3); \
}

/////////////////////////////////////////////////////////////

#define i2s_call_u8() { \
	__asm  \
		MOV DPL, R1  ;; arg1 coming from R1, goes to DPL \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u8() { \
	i2s_adjust_stack(-3); \
}

// (uint8 a1, uint8 a2)
// neo: sdcc-> arg1 DPL, arg2 iStack
#define i2s_call_u8_u8() {\
	__asm \
		MOV DPL, R1  ;; arg1 coming from R1, goes to DPL \
		PUSH 2       ;; arg2 coming from R2, goes to stack \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u8_u8() {\
	__asm \
		;; pop off what we pushed, including (fake) bp, ret addr \
	__endasm;\
	i2s_adjust_stack(-4); \
}

////////////////////////////////////////////////////////////
// (uinit8, uint8, uint8)
#define i2s_call_u8_u8_u8() {\
	__asm \
		MOV DPL, R1   ;; arg1 coming from R1, goes to DPL\
		;; remaining args are in R2 and R3. push R3 then R2. \
		PUSH 3 \
		PUSH 2 \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u8_u8_u8() {\
	i2s_adjust_stack(5); \
}

//////////////////////////////////////////////////////////////////
// (uint8, uint8, uint8, uint8, uint8)
#define i2s_call_u8_u8_u8_u8_u8() {\
	__asm \
		MOV DPL, R1 \
		PUSH 5 \
		PUSH 4 \
		PUSH 3 \
		PUSH 2 \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u8_u8_u8_u8_u8() {\
	i2s_adjust_stack(-7); \
}

//////////////////////////////////////////////////////
// (uint8 a1, uint8* a2)
#define i2s_call_u8_p() {\
	__asm \
		MOV R1, DPL ;; first param in DPL \
		PUSH 2 \
		PUSH 3 \
		;; no need for top empty byte \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u8_p() {\
	i2s_adjust_stack(-5); \
}

/////////////////////////////////////////////////////
//	(uint8 a1, uint8* a2, uint8 a3)
#define i2s_call_u8_p_u8() {\
	__asm \
		MOV DPL, R1  ;; first param in DPL \
		PUSH 4       ;; push arg3 first \
		PUSH 2       ;; push arg2 low byte \
		PUSH 3 	     ;; push arg2 high byte \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u8_p_u8() {\
	i2s_adjust_stack(-6); \
}


///////////////////////////////////////////////////
// (uint8* a1)
#define i2s_call_p() {\
	__asm \
		;; this one is simple: stara1 gets passed in on DPH:DPL, \
		;; then we pass it over to R2:R1 \
		MOV DPH, R2 \
		MOV DPL, R1 \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_p() {\
	i2s_adjust_stack(-3); \
}


#define i2s_call_u16_u8() {\
	__asm \
		;; the params are passed in as arg1=R3:R2, arg2=R1 \
		;; need to pass arg1 on DPH:DPL, arg2 on stack. \
		MOV DPL, R2 \
		MOV DPH, R3 \
		PUSH 1 \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u16_u8() {\
	i2s_adjust_stack(-4); \
}

/******************************************************************
// (int16* a1, int16* a2, int16* a3)
// #define call_p_p_p() {\
//
// (uint8* day, uint8* date, uint8* month, uint8* year, uint8* century )
// #define call_p_p_p_p_p(callee) { \

// this macro is for 3 pointers or more. if 3 then Nptrs = 1;
// #define call_p_p_pn(callee, Nptrs) { \

// #define call_u8_u8_u8_u8_u8_u8_u8(callee) { \
****************************************************************/

#define i2s_call_u16_p_p_p_u16_u8() { \
	__asm \
		;; incoming: arg1 in R3:R2, arg2 in R5:R4, arg3-5 on stack.  \
		;; question is what about arg6? in R1 or on stack? => my guess is R1. \
		;; set DPTR to XSTACK, where \
		;; (current top=lower) [arg3 p][arg4 p][arg5 16] \
		;; increment dptr, load in, and write to stack indirectly using @R1. \
		;; pre-allocated SP for [2][2][2][2][1] = 9 bytes,  \
		;; initialize R1 = SP, \
		;; and then copy from XSTACK. \
		MOV B, R1 ;; save arg6, assuming it is passed in as R1. \
		MOV  A, SP \
	__endasm; \
	__asm__("ADD  A, #9\n" \
					"MOV  DPL, " XSP_L "\n" \
					"MOV  DPH, " XSP_H "\n" \
					"MOV R1, A ;; use R1 to traverse the stack downward\n" \
					";; still need 3 more spaces on istack to fake bp and ret addr\n" \
					"ADD A, #3\n"); \
	__asm \
		MOV SP, A ;; this essentially does the adjust stack as in other macros \
		;; we will handle moving to DPTR last because it is first needed for XSP \
		MOV @R1, 5  ;; arg2 higher byte (new sp). 5 is R5 in this case.\
		DEC R1 \
		MOV @R1, 4  ;; arg2 lower byte (sp-1).  4 is R4 in this case.\
		DEC R1 \
		;; use R4 as a loop counter \
	__endasm; \
	__asm__("MOV R4, #3\n"); \
	__asm \
00001$: \
		MOVX A, @DPTR ;; arg3/4/5 lower byte \
		MOV R2, A    ;; save arg3/4/5 lower byte  \
		INC DPTR \
		MOVX A, @DPTR  ;; arg3/4/5 upper byte \
		INC DPTR \
		MOV @R1, A    ;; copy arg3/4/5 upper byte (sp-2/-4/-6)\
		DEC R1 \
		MOV @R1, 2   ;; copy arg3/4 lower byte (sp-3/-5/-7); 2 is R2.\
		DEC R1 \
		DJNZ R4, 00001$  ;; loop three times to pass arg3-5. \
		MOV @R1, B       ;; copy arg6 from saved B (sp-8) \
		MOV DPL, R2      ;; now pass arg1 in DPH:DPL \
		MOV DPH, R3 \
		;; no need to do another extra adjust stack in this case \
	__endasm; \
}
#define i2s_exit_u16_p_p_p_u16_u8() { \
	i2s_adjust_stack(-12); \
}

/////////////////////////////////////////////////////////////////

#define i2s_call_u16_p_u8() { \
	__asm \
		;; parameter comes on as [arg1] = R3:R2, [arg2] = R5:R4,  \
		;; [arg3] => R1 \
		;; istack is [arg2 H:L][arg3]\
		PUSH 1 ;; arg3 \
		PUSH 4 ;; arg2 low byte \
		PUSH 5 ;; arg3 high byte \
		MOV DPL, R2 \
		MOV DPH, R3 \
	__endasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_u16_p_u8() { \
	i2s_adjust_stack(-6); \
}

/////////////////////////////////////////////////////////////////
#define i2s_call_p_u16_p() { \
	__asm \
		;; arg3 on xstack +3:+2 => push \
		;; arg2 in R5:R4 => stack => push \
		;; arg1 in R3:R2 => DPH:DPL \
	__endsasm; \
	__asm__("MOV DPL, " XSP_L "\n" \
					"MOV DPH, " XSP_H "\n" );\
	__asm \
		MOVX A, @DPTR  ;; arg3 low byte  \
		PUSH ACC  \
		INC DPTR \
		MOVX A, @DPTR  ;; arg3 high byte \
		PUSH ACC \
		;; now handle arg2  \
		PUSH 4 \
		PUSH 5 \
		;; finally, handle arg1 \
		MOV DPL, 2 \
		MOV DPH, 3 \
	__endsasm; \
	i2s_adjust_stack(3); \
}
#define i2s_exit_p_u16_p() { \
	i2s_adjust_stack(-7); \
}


/////////////////////////////////////////////////////////////////
#define i2s_call_u16_p_p_u8_u16() { \
	__asm \
		;; parameter comes on as [arg1] = R3:R2, [arg2] = R5:R4,  \
		;; [arg4] => R1 \
		;; XSTACK [arg3 L:H][arg5 L:H] \
		;; arg1 => DPH:DPL \
		;; istack is [arg2 H:L][arg3 H:L][arg4][arg5 H:L] \
	__endasm; \
	__asm__("MOV DPL, " XSP_L "\n" \
					"MOV DPH, " XSP_H "\n" \
					"MOV A, SP \n" \
					"ADD A, #7\n" \
			); \
	__asm \
		MOV SP, A \
		MOV B, R1   ;; preserve R1 so we can use it as pointer \
		MOV @R1, 5 ;; arg2 high byte (sp); 5 is R5. \
		DEC R1 \
		MOV @R1, 4 ;; arg2 low byte (sp-1); 4 is R4. \
		DEC R1 \
		MOVX A, @DPTR  ;; arg3 low byte \
		MOV R5, A      ;; save arg3 low byte in R5 \
		INC DPTR \
		MOVX A, @DPTR  ;; arg3 high byte \
		MOV @R1, A     ;; write arg3 high byte (sp-2) \
		DEC R1 \
		MOV @R1, 5    ;; write arg3 low byte (sp-3); 5 is R5. \
		DEC R1 \
		MOV @R1, B     ;; write arg4 (saved in B) (sp-4) \
		DEC R1 \
		;; grab arg5 from xstack \
		INC DPTR \
		MOVX A, @DPTR  ;; arg5 low byte \
		MOV R5, A   ;; save arg5 low byte \
		INC DPTR \
		MOVX A, @DPTR  ;; arg5 high byte \
		MOV @R1, A     ;; write arg5 high byte (sp-5)\
		DEC R1 \
		MOV @R1, 5    ;; write arg5 low byte (sp-6); 5 is R5. \
		;; finally, pass arg1 from R3:R2 to DPH:DPL \
		MOV DPL, R2 \
		MOV DPH, R3 \
	__endasm; \
}
#define i2s_exit_u16_p_p_u8_u16() { \
	__asm \
		;; the only thing is to pop back the internal stack \
		MOV A, SP \
	__endasm; \
	__asm__("	ADD A, #-7\n"); \
	__asm \
		MOV SP, A \
	__endasm; \
}

///////////////////////////////////////////////////////////////////
// This section handles return values.

// return in R1 by IAR,
// we copy it to DPL for SDCC.
#define i2s_ret_u8() { \
	__asm \
		MOV DPL, R1 \
	__endasm; \
}

#define i2s_ret_u16() { \
	__asm \
		MOV DPL, R2 \
		MOV DPH, R3 \
	__endasm; \
}

#define i2s_ret_u24() { \
	__asm \
		MOV DPL, R1 \
		MOV DPH, R2 \
		MOV B, R3 \
	__endasm; \
}

#define i2s_ret_u32() { \
	__asm \
		MOV DPL, R2 \
		MOV DPH, R3 \
		MOV B, R4 \
		MOV A, R5 \
	__endasm; \
}

/**************************** jump table *****************************/
#define i2s_callback_save_reg() {\
	__asm \
		PUSH 6      \
		PUSH 7      \
		PUSH dpl    \
		PUSH dph    \
	__endasm;       \
}

#define i2s_callback_restore_reg() {\
	__asm \
		POP dph \
		POP dpl \
		POP 7   \
		POP 6   \
	__endasm;    \
}

#define i2s_jumptable_call_void(callee) { \
	i2s_callback_save_reg();\
	__asm \
		LCALL callee \
	__endasm; \
	i2s_callback_restore_reg();\
	__asm\
		LJMP  0x0122 ; ?BRET_FF\
	__endasm; \
}


#define i2s_jumptable_call_u8(callee) { \
	i2s_callback_save_reg();\
	__asm \
		MOV DPL, R1 \
		LCALL callee \
	__endasm; \
	i2s_callback_restore_reg();\
	__asm\
		LJMP  0x0122 ; ?BRET_FF\
	__endasm; \
}

#define i2s_enter_main() { \
	i2s_callback_save_reg();\
}

#define i2s_callback_ret() { \
	i2s_callback_restore_reg();\
}

#endif