/*
 * iar3sdcc.h
 *
 * This is the (older) macro definition for writing callbacks compiled
 * in SDCC to be called by IAR.  it is here mainly for the rare cases
 * where 3-byte pointers on SDCC side is assumed. it shares the same
 * definition as iar2sdcc.h for those case that don't involve pointers.
 */


#ifndef IAR3SDCC_H
#define IAR3SDCC_H




//////////////////////////////////////////////////////
// (uint8 a1, uint8* a2)
#define i3s_call_u8_p() {\
	__asm \
		MOV R1, DPL ;; first param in DPL \
		PUSH 2 \
		PUSH 3 \
		CLR A \
		PUSH ACC \
	__endasm; \
}
#define i3s_exit_u8_p() {\
	__asm \
		MOV A, SP \
  __endasm; \
	__asm__("ADD A, #-3\n"); \
	__asm \
		MOV SP, A \
	__endasm; \
}

/////////////////////////////////////////////////////
//	(uint8 a1, uint8* a2, uint8 a3)
#define i3s_call_u8_p_u8() {\
	__asm \
		MOV DPL, R1  ;; first param in DPL \
		PUSH 4       ;; push arg3 first \
		PUSH 2       ;; push arg2 low byte \
		PUSH 3 	     ;; push arg2 high byte \
		CLR A        ;; push 0 to make 3-byte pointer \
		PUSH ACC \
	__endasm; \
}
#define i3s_exit_u8_p_u8() {\
	__asm \
		MOV A, SP \
  __endasm; \
	__asm__("ADD A, #-4\n"); \
	__asm \
		MOV SP, A \
	__endasm \
}


///////////////////////////////////////////////////
// (uint8* a1)
#define i3s_call_p() {\
		__asm \
			;; this one is simple: stara1 gets passed in on DPH:DPL, \
			;; then we pass it over to R2:R1 \
			MOV DPH, R2 \
			MOV DPL, R1 \
			CLR A \
			MOV B, A \
		__endasm; \
}
#define i3s_exit_p() {\
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

#define i3s_call_u16_p_p_p_u16_u8() { \
	__asm \
		;; incoming: arg1 in R3:R2, arg2 in R5:R4, arg3-5 on stack.  \
		;; question is what about arg6? in R1 or on stack? => my guess is R1. \
		;; set DPTR to XSTACK, where \
		;; (current top=lower) [arg3 p][arg4 p][arg5 16] \
		;; increment dptr, load in, and write to stack indirectly using @R1. \
		;; pre-allocated SP for [3][3][3][2][1] = 12 bytes,  \
		;; initialize R1 = SP, \
		;; and then copy from XSTACK. \
		MOV  A, SP \
	__endasm; \
	__asm__("ADD  A, #12\n" \
					"MOV  DPL, " XSP_L "\n" \
					"MOV  DPH, " XSP_H "\n"); \
	__asm \
		MOV SP, A \
		MOV B, R1 ;; save arg6, assuming it is passed in as R1. \
		MOV R1, A ;; use R1 to traverse the stack downward \
		;; we handle moving to DPTR last because it is first needed for XSP \
		CLR A \
		MOV @R1, A   ;; arg2 top zero byte for pointer (new sp)\
		DEC R1 \
		MOV @R1, 5  ;; arg2 higher byte (new sp-1). 5 is R5 in this case.\
		DEC R1 \
		MOV @R1, 4  ;; arg2 lower byte (sp-2).  4 is R4 in this case.\
		;; use R4 as a loop counter \
	__endasm; \
	__asm__("MOV R4, #2\n"); \
	__asm \
		DEC R1 \
00001$: \
		CLR A \
		MOV @R1, A   ;; arg3/4 top zero byte for pointer (sp-3)/(sp-6) \
		DEC R1 \
		MOVX A, @DPTR ;; arg3/4 lower byte \
		MOV R2, A    ;; save arg3/4 lower byte  \
		INC DPTR \
		MOVX A, @DPTR  ;; arg3/4 upper byte \
		INC DPTR \
		MOV @R1, A    ;; copy arg3/4 upper byte (sp-4)/(sp-7)\
		DEC R1 \
		MOV @R1, 2   ;; copy arg3/4 lower byte (sp-5)/(sp-8); 2 is R2.\
		DJNZ R4, 00001$  ;; loop twice: pass arg3 and arg4. \
		DEC R1 \
		MOVX A, @DPTR   ;; arg5 high lower byte \
		MOV R2, A      ;; save arg5 lower byte \
		INC DPTR \
		MOVX A, @DPTR   ;; arg5 lower byte \
		MOV @R1, 2     ;; copy arg5 higher byte (sp-9); 2 is R2. \
		DEC R1 \
		MOV @R1, A       ;; copy arg5 higher byte (sp-10) \
		DEC R1 \
		MOV @R1, B       ;; copy arg6 from saved B (sp-11) \
		MOV DPL, R2      ;; now pass arg1 in DPH:DPL \
		MOV DPH, R3 \
	__endasm; \
}
#define i3s_exit_u16_p_p_p_u16_u8() { \
	__asm \
		MOV  A, SP \
	__endasm; \
	__asm__("ADD  A, #-12\n"); \
	__asm \
		MOV SP, A \
	__endasm; \
}


#define i3s_call_u16_p_p_u8_u16() { \
	__asm \
		;; parameter comes on as [arg1] = R3:R2, [arg2] = R5:R4,  \
		;; [arg4] => R1 \
		;; XSTACK [arg3 L:H][arg5 L:H] \
		;; arg1 => DPH:DPL \
		;; istack is [arg2 0:H:L][arg3 0:H:L][arg4][arg5 H:L] \
	__endasm; \
	__asm__("MOV DPL, " XSP_L "\n" \
					"MOV DPH, " XSP_H "\n" \
					"MOV A, SP \n" \
					"ADD A, #9\n" \
			); \
	__asm \
		MOV SP, A \
		MOV B, R1   ;; preserve R1 so we can use it as pointer \
		CLR A       ;; clear high 0 byte for pointer \
		MOV @R1, A  ;; arg2 high 0 byte (sp) \
		MOV @R1, 5 ;; arg2 high byte (sp-1); 5 is R5. \
		DEC R1 \
		MOV @R1, 4 ;; arg2 low byte (sp-2); 4 is R4. \
		DEC R1 \
		CLR A   \
		MOV @R1, A     ;; arg3 high 0 byte (sp-3) \
		DEC R1 \
		MOVX A, @DPTR  ;; arg3 low byte \
		MOV R5, A      ;; save arg3 low byte in R5 \
		INC DPTR \
		MOVX A, @DPTR  ;; arg3 high byte \
		MOV @R1, A     ;; write arg3 high byte (sp-4) \
		DEC R1 \
		MOV @R1, 5    ;; write arg3 low byte (sp-5); 5 is R5. \
		DEC R1 \
		MOV @R1, B     ;; write arg4 (saved in B) (sp-6) \
		DEC R1 \
		;; grab arg5 from xstack \
		INC DPTR \
		MOVX A, @DPTR  ;; arg5 low byte \
		MOV R5, A   ;; save arg5 low byte \
		INC DPTR \
		MOVX A, @DPTR  ;; arg5 high byte \
		MOV @R1, A     ;; write arg5 high byte (sp-7)\
		DEC R1 \
		MOV @R1, 5    ;; write arg5 low byte (sp-8); 5 is R5. \
		;; finally, pass arg1 from R3:R2 to DPH:DPL \
		MOV DPL, R2 \
		MOV DPH, R3 \
	__endasm; \
}
#define i3s_exit_u16_p_p_u8_u16() { \
	__asm \
		;; the only thing is to pop back the internal stack \
		MOV A, SP \
	__endasm; \
	__asm__("	ADD A, #-9\n"); \
	__asm \
		MOV SP, A \
	__endasm; \
}

#endif