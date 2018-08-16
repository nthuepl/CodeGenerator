/*
 * sdcc3iar.h
 * This is the translator from SDCC caller to IAR,
 * where the "3" indicates 3-byte pointers. This is the default if you
 * don't want to convert source code.  However, it will cause problems
 * when you manipulate pointer data structures.  The proper thing to do
 * is to use sdcc2iar.h after you annotate all pointers with __xdata in
 * front.. e.g., __xdata uint8 *p; for function pointers, use __code.
 *
 * if you want an array of pointers, then you need to probably typedef
 * it?
 *
 * __xdata uint8* __xdata A[100]; does this mean an array in __xdata of
 * pointers to __xdata?
 *
 * This file is supposed to be generated from python after parsing the
 * code signature, and written either automatically or manually in
 * assembly.  There is probably no need for sdcc2iar.c.
 */

#ifndef SDCC3IAR_H
#define SDCC3IAR_H
#include "sdcc2iar.h"  /* reuse all definitions from sdcc2iar.h,
													so we only do the 3-byte pointer ones here */





// (uinit8, uint8, void*)
#define s3i_call_u8_u8_p(callee) {\
	__asm \
		;; stack looks like [ret H:L][bp][arg2 u8][arg3 0:H:L] \
		;; pass as  [R1], [R2], [R5:R4] \
		MOV R1, DPL ;; arg1 \
		MOV A, SP \
	__endasm; \
	__asm__("ADD A, #-3\n"); /* skip over pad and return address */ \
	__asm \
		MOV SP, A \
		POP 2      ;; arg2 \
		POP 5      ;; filling 0 of arg3, discard \
		POP 5      ;; arg3 high byte \
		POP 4      ;; arg3 low byte \
	__endasm; \
	__asm__("ADD A, #3\n"); /* restore stack */ \
	__asm \
		MOV SP, A \
		LCALL callee \
	__endasm; \
}


// (uint8 a1, uint8* a2)
#define s3i_call_u8_p(callee) {\
	__asm \
		MOV R1, DPL ;; first param in DPL \
	  ;; need to skip over the return address, plus an extra byte for pointer\
	  ;; plus one extra byte as a result of the call! So, add -4 to SP \
    MOV A, SP  \
  __endasm; \
	__asm__("ADD A, #-4\n"); \
	__asm \
	  MOV SP, A   ;; now SP points at the argument \
    POP 3       ;; high byte goes ito R3 \
    POP 2       ;; low byte goes into R2 \
	__endasm; \
	__asm__("ADD A, #4\n"); /* restore old stack value */\
	__asm \
    MOV SP, A \
		LCALL callee \
  __endasm; \
}

//	(uint8 a1, uint8* a2, uint8 a3)
#define s3i_call_u8_p_u8(callee) {\
	__asm \
	  ;; stack is [returnAddr H:L][bp][arg2 0:H:L][arg3] \
		;; param uint8a1 is in DPL => R1 \
		;; stack has uint8a3 (1 byte) => R4, uint8stara2 (2 bytes) => R3:R2, \
		MOV R1, DPL  ;; first param in DPL \
	  MOV A, SP    \
	__endasm; \
	__asm__("ADD A, #-4\n"); \
	__asm \
		POP 3        ;; uint8stara2 => R3:R2 \
		POP 2 	     ;; \
		POP 4        ;; uint8a3 => R4 \
	__endasm; \
	__asm__("ADD A, #4\n"); /* A still has old val before pop, add 4 back */\
	  MOV SP, A    ;; restore stack state  \
		LCALL  callee \
  __endasm; \
}



// (uint8* a1)
#define s3i_call_p(callee) {\
		__asm \
			;; this one is simple: stara1 gets passed in on DPH:DPL, \
			;; then we pass it over to R2:R1 \
			MOV R2, DPH \
			MOV R1, DPL \
			LCALL callee \
		__endasm; \
}


#define s3i_call_p_u8(callee) {\
	__asm \
		;; stack looks like [ret H:L][bp][arg2] \
		MOV R2, DPL ;; arg1 is in DPH:DPL \
		MOV R3, DPH ;; \
		MOV A, SP   \
	__endasm; \
	__asm__("ADD A, #-3    ;; skip over ret addr and bp \n"); \
	__asm \
		MOV SP, A \
		POP 1   ;; first available is R1, so we try it even though it comes after \
	__endasm; \
	__asm__("ADD A, #3     ;; restore old stack value \n"); \
	__asm \
		MOV SP, A \
		LCALL callee \
	__endasm; \
}


// (int16* a1, int16* a2, int16* a3)
#define s3i_call_p_p_p(callee) {\
	__asm \
		;; stack is (top) [retAddr H:L][bp][arg2 0:H:L][arg3 0:H:L] \
		;; params are  \
		;; arg1 in B:DPH:DPL => :R3:R2 \
		;; arg2 in (internal) stack => :R5:R4, \
		;; arg3 in (internal) stack => :XSTACK \
	  ;; strategy: decrement SP by 4 first to skip 0:H:L 0, \
		;; pop twice to get arg2, pop an extra time,  \
		;; pop twice to get arg3, and then restore SP. \
		MOV R3, DPH \
		MOV R2, DPL \
		MOV A, SP \
	__endasm;\
	__asm__("ADD A, #-4\n"); \
	__asm \
		MOV SP, A ;; istack offset: -4 \
		POP 5 ;; pass arg2 into R5:R4 pair, upper byte. istack -5. \
		POP 4 ;; lower byte of arg2 passed in R4; istack -6. \
		POP 1  ;; use R1 as temp. this one is the top 0 byte of arg2, discard. istack-7. \
	__endasm; \
	__asm__("MOV A, " XSP_L " \n"); \
	__asm \
		;; strategy here: XSP = DPTR = (XSP - 2), then we do \
		;; mem[DPTR++] = lower, mem[DPTR++] = upper. \
	__endasm; \
	__asm__("ADD A, #-2\n" \
					"MOV DPL, A\n" \
					"MOV " XSP_L ", A\n" \
					"MOV DPH, " XSP_H "\n" );  \
	__asm \
		JC 00001$  ;; anything not 0 or 1 need not decrement higher byte, skip.\
	  DEC DPH      ;; decrement upper byte \
	__endasm; \
	__asm__("MOV " XSP_H ", DPH\n" );  \
	__asm \
00001$:  ;; now processing lower byte \
		POP 1   ;; grab arg3 upper byte from internal stack. istack-8. \
		POP ACC ;; grab arg3 lower byte from internal stack, istack-9. \
		MOVX @DPTR, A ;; XMEM[oldXSP-2] = arg3 lower byte \
		INC DPTR \
		MOV A, R1 \
		MOVX @DPTR, A ;; XMEM[oldXSP-1] = arg3 upper byte \
		;; now restore SP \
		MOV A, SP \
	__endasm; \
	__asm__("ADD A, #9\n"); \
	__asm \
	  MOV SP, A \
		LCALL callee   ;; making actual call \
		;; we may have to tear down the XSP, right? perhaps do this after \
		;; fetching the return value, as a separate macro? \
		;; tear down stack by popping two from XSTACK \
	__endasm; \
	__asm__("MOV A, " XSP_L "\n" \
			"ADD A, #2\n" \
			"MOV " XSP_L ", A\n"); \
	__asm \
		JNC 00002$ ;; if no carry, skip updating upper byte and just update lower \
	__endasm; \
	__asm__("INC " XSP_H "\n"); \
	__asm__("00002$: "); \
}

// (uint8* day, uint8* date, uint8* month, uint8* year, uint8* century )
#define s3i_call_p_p_p_p_p(callee) { \
	__asm \
	  ;; stack is [ret H:L][bp][arg2][arg3][arg4][arg5] \
		MOV R2, DPL  ;; pass arg1 \
		MOV R3, DPH  ;; pass arg1 \
		;; pop stack into XStack. set XSP = XSP - 6, load DPTR, then copy. \
		;; arg3 to arg5 -- from istack-7 \
		MOV A, SP \
	__endasm;\
	__asm__("ADD A, #-7 \n" \
		"MOV SP, A ;; internal stack now points at arg3 high byte \n" \
		"MOV A, " XSP_L "\n" \
		"ADD A, #-6  ;; make room for arg3-arg5\n" \
		"MOV DPL, A\n" \
		"MOV " XSP_L ", A\n" \
		"JC 00001$\n" \
		"DEC " XSP_H "\n" \
"00001$: " \
		"MOV DPH, " XSP_H "\n" \
		"MOV R1, #3 ;; use R1 as loop count. \n"  \
		); \
	__asm \
		;; now copy arg3..5 by popping H and L \
00002$: \
		POP 5 ;; high byte \
		POP ACC ;; low byte \
		MOVX @DPTR, A  ;; arg[i] low byte \
		INC DPTR \
		MOV A, R5 ;; get high byte \
		MOVX @DPTR, A  ;; arg[i] high byte \
		INC DPTR \
		POP 5 ;; top 0 of arg[i-1], discard \
		DJNZ R1, 00002$ \
		;; finished copying stack parameter. now need to copy arg2! \
		;; stack is now at oldSP - 16; want to point at arg2 high byte \
		MOV A, SP \
	__endasm; \
	__asm__("ADD A, #12 ;; makes offset oldSP-4\n"); \
	__asm \
		MOV SP, A \
		POP 5 \
		POP 4 \
		;; now restore stack. add 6 back to SP (or add 4 back to A). \
	__endasm; \
	__asm__("ADD A, #4\n"); \
	__asm \
		MOV SP, A \
		LCALL callee \
	__endasm; \
	/* restore the external stack by adding 6 back */ \
	__asm__("MOV A, " XSP_L "\n" \
		"ADD A, #6  ;; pop room for arg3-arg5\n" \
		"MOV " XSP_L ", A\n" \
		"JNC 00003$\n" \
		"INC " XSP_H "\n" \
"00003$: \n"); \
}

// this macro is for 3 pointers or more. if 3 then Nptrs = 1;
#define s3i_call_p_p_pn(callee, Nptrs) { \
	__asm \
	  ;; stack is [ret H:L][bp][arg2][arg3]...  \
		MOV R2, DPL  ;; pass arg1 \
		MOV R3, DPH  ;; pass arg1 \
		;; pop stack into XStack. set XSP = XSP - (2*Nptrs), load DPTR, then copy. \
		;; arg3 to n -- from istack-7 down \
		MOV A, SP \
	__endasm;\
	__asm__("ADD A, #-7 \n" \
		"MOV SP, A ;; internal stack now points at arg3 high byte \n" \
		"MOV A, " XSP_L "\n" \
		"ADD A, #-(" #Nptrs "*2)  ;; make room for arg3-arg(Ndptrs+2)\n" \
		"MOV DPL, A\n" \
		"MOV " XSP_L ", A\n" \
		"JC 00001$\n" \
		"DEC " XSP_H "\n" \
"00001$: " \
		"MOV DPH, " XSP_H "\n" \
		"MOV R1, #" #Nptrs " ;; use R1 as loop count. \n"  \
		); \
	__asm \
		;; now copy arg3..(Nptrs+2) by popping H and L \
00002$: \
		POP 5 ;; high byte \
		POP ACC ;; low byte \
		MOVX @DPTR, A  ;; arg[i] low byte \
		INC DPTR \
		MOV A, R5 ;; get high byte \
		MOVX @DPTR, A  ;; arg[i] high byte \
		INC DPTR \
		POP 5 ;; top 0 of arg[i-1], discard \
		DJNZ R1, 00002$ \
		;; finished copying stack parameter. now need to copy arg2! \
		;; stack is now at oldSP - 6 - (Nptrs*3); want to point at arg2 high byte \
		MOV A, SP \
	__endasm; \
	__asm__("ADD A, #(" #Nptrs "*3 + 3);; makes offset oldSP-4\n"); \
	__asm \
		MOV SP, A \
		POP 5 \
		POP 4 \
		;; now restore stack. add 4 back to a. \
	__endasm; \
	__asm__("ADD A, #4\n"); \
	__asm \
		MOV SP, A \
		LCALL callee \
	__endasm; \
	/* restore the external stack by adding 2*Nptrs back */ \
	__asm__("MOV A, " XSP_L "\n" \
		"ADD A, #(" #Nptrs "*2)  ;; pop room for arg3-Nptrs\n" \
		"MOV " XSP_L ", A\n" \
		"JNC 00003$\n" \
		"INC " XSP_H "\n" \
"00003$: \n"); \
}


#endif
