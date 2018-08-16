/*
 * sdcc2iar.h
 * This is the translator from SDCC caller to IAR.
 * To use this file, you need to modify the source code so that all
 * pointers need to be qualified with either __xdata or __code, or else
 * SDCC will treat it as a generic pointer and use 3-byte pointer
 * instead.  If you want 3-byte pointer you can use sdcc3iar.h instead.
 * It can be helpful if you just want to quickly compile your code with
 * minimal modification.
 * This file is supposed to be generated from python after parsing the
 * code signature, and written either automatically or manually in
 * assembly.  There is probably no need for sdcc2iar.c.
 */

#ifndef SDCC2IAR_H
#define SDCC2IAR_H

/* code pointer type -- assuming --small-model,
 * so code pointer is 16 bits,
 * and this pointer resides in xdata. hope it compiles.
 */
#define XSP_L  "0x18"
#define XSP_H  "(0x18+1)"

#define sdcc_main_return {\
	__asm \
	LJMP 0x0122 ; ?BRET_FF \
	__endasm; \
}

extern __xdata unsigned char * __data __at (XSP_L) XSP;

// identical because no pointer is used.
#define s2i_call_void(callee) {\
	__asm \
		LCALL callee \
	__endasm; \
}

/*********************************************************
 * utility macros to factor out definition so they are less likely to
 * make mistakes!  Not meant for users.
 *********************************************************/
#define s2i_call(callee) { \
	__asm \
		LCALL callee \
	__endasm; \
}
#define s2i_pass_arg1_u8() { \
	__asm__("MOV R1, DPL\n"); \
}
#define s2i_pass_arg1_u16() { \
	__asm \
		MOV R2, DPL \
		MOV R3, DPH \
	__endasm; \
}
#define s2i_pass_arg1_u32() { \
	s2i_pass_arg1_u16(); \
	__asm \
		MOV R4, B \
		MOV R5, A \
	__endasm; \
}
/* this is the part where after passing arg1, we want to fetch more
 * parameters from (SDCC's) istack, but we need to point the stack at
 * 3 bytes below, beause they are taken by the 2-byte return address
 * of the caller and the frame pointer bp.
 * So, by default, you should call with s2i_skipRetBp(-3).
 * But in other cases, if you want to skip more, e.g.,
 * s2i_call_p_p_p.. then you could skip -5 so you get to arg3 first to
 * copy all other args before going back to the -3 position (so you an
 * pass arg in R5:R4).  But it is not clear whether that is a real
 * win.
 *
 * As a side effect, we save
 * the old stack pointer in B register so we can restore it easily
 * later.
 */
#define s2i_skipRetBp() { \
	__asm \
		MOV A, SP  \
		MOV B, A   ;; save a copy \
	__endasm; \
	__asm__("ADD A, #-3 ;; skip return address and frame pointer \n" \
				  "MOV SP, A\n"); \
}
/* restore the istack poitner SP saved in B by s2i_skipRetBp(). */
#define s2i_restoreSPfromB() { \
	__asm__("MOV SP, B\n"); \
}
/*
 * External stack: allocate space. to allocate 2 bytes, call with
 * s2i_allocXstack(2), which will SUBTRACT 2 from XSP.
 * It will not work if you give a negative number!
 * also, need to pass the nBytes as a string!!!!
 */
#define s2i_allocXstack(nBytes) { \
	__asm__("MOV A, " XSP_L "\n" \
			"ADD A, #-" nBytes "\n" \
			"MOV DPL, A\n" \
			"MOV " XSP_L ", A\n" \
			"JC 00001$\n" \
			"DEC " XSP_H "\n" \
	"00001$:" \
			"MOV DPH, " XSP_H "\n");  \
}

#define s2i_deallocXstack(nBytes) { \
	__asm__("MOV A, " XSP_L "\n" \
			"ADD A, #" nBytes "\n" \
			"MOV " XSP_L ", A\n" \
		  "JNC 00004$ ;; if no carry, skip updating upper byte \n" \
			"INC " XSP_H "\n" \
		"00004$: "); \
}

/*********************************************************
 * macros for users
 *********************************************************/

#define s2i_call_u8(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_call(callee); \
}

#define s2i_call_u16(callee) {\
	s2i_pass_arg1_u16(); \
	s2i_call(callee); \
}
// (uint8* a1)
#define s2i_call_p(callee) \
	s2i_call_u16(callee)


#define s2i_call_u32(callee) { \
	s2i_pass_arg1_u32(); \
	s2i_call(callee); \
}

#define s2i_call_u32_u16(callee) {\
	/* pass arg1 in R5:R2, u16 on xstack */ \
	s2i_pass_arg1_u32(); \
	s2i_skipRetBp(); \
	s2i_allocXstack("2"); \
		__asm \
			POP 1         ;; put higher byte of arg2 in R1 \
			POP ACC       ;; put lower byte of arg2 in A \
			MOVX @DPTR, A ;; write lower byte of arg2 \
			INC DPTR      ;; point xstack one byte higher \
			MOV A, R1     ;; \
			MOVX @DPTR, A ;; write upper byte of arg2 \
		__endasm; \
		s2i_restoreSPfromB(); \
		s2i_call(callee); \
	s2i_deallocXstack("2"); \
}

// (uint8 a1, uint8 a2)
// neo: sdcc-> arg1 DPL, arg2 iStack
#define s2i_call_u8_u8(callee) {\
	s2i_pass_arg1_u8(); \
	/* instead of s2i_skipRetBp(), we optimize by not writing back to SP */\
	/* but just load indirectly thru @R0 so we don't need to restore SP. */\
	__asm \
		MOV A, SP  \
	__endasm; \
	__asm__("ADD A, #-3\n"); /* 3 byte return addres */\
	__asm \
		MOV R0, A   ;; now R0 points at the argument \
		MOV 2, @R0  ;; move stack content to register R2 \
	__endasm;\
	s2i_call(callee); \
}

// (uinit8, uint8, uint8)
// stack looks like [ret H:L][bp][u8 arg2][u8 arg3]
#define s2i_call_u8_u8_u8(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 2 \
			POP 3 \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}

// (uinit8, uint8, void*)
// stack looks like [ret H:L][bp][arg2 u8][arg3 H:L] 
// pass as  [R1], [R2], [R5:R4] 
#define s2i_call_u8_u8_p(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 2      ;; arg2 \
			POP 5      ;; arg3 high byte \
			POP 4      ;; arg3 low byte \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}
#define s2i_call_u8_u8_u16(callee) \
	s2i_call_u8_u8_p(callee)

// (uint8, uint8, uint8, uint8, uint8)
#define s2i_call_u8_u8_u8_u8_u8(callee) {\
	/* stack is [ret H:L][bp][a2][a3][a4][a5]; a1 is in DPL */ \
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 2 \
			POP 3 \
			POP 4 \
			POP 5 \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}

/* stack is [ret H:L][bp][a2][a3][p]; a1 is in DPL */
#define s2i_call_u8_u8_u8_p(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 2       ;; arg2 \
			POP 3       ;; arg3 \
			POP 5       ;; arg4 high byte \
			POP 4       ;; arg4 low byte \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}

/* stack is [ret H:L][bp][a2][a3][p][p][p]; a1 is in DPL */
#define s2i_call_u8_u8_u8_p_p_p(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
	__asm \
		POP 2       ;; arg2 \
		POP 3       ;; arg3 \
		POP 5       ;; arg4 H \
		POP 4       ;; arg4 L \
	__endasm; \
	s2i_allocXstack("4"); \
	__asm__("MOV R7, #2  ;; use R7 as loop counter\n"); \
	__asm \
	00002$: \
		POP 6         ;; save arg 5/6 high byte in R6 \
		POP ACC       ;; arg 5/6 low byte \
		MOVX A, @DPTR ;; write arg5 low byte \
		INC DPTR      ;; \
		MOV A, R6     ;; set up arg 5/6 high byte \
		MOVX A, @DPTR ;; write arg 5/6 low byte \
		INC DPTR      ;; \
		DJNZ R7, 00002$  ;; loop twice \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("4"); \
}


// (uint8 a1, uint8* a2)
#define s2i_call_u8_p(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 3       ;; high byte goes ito R3 \
			POP 2       ;; low byte goes into R2 \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}
#define s2i_call_u8_u16(callee)\
	s2i_call_u8_p(callee) 

#define s2i_call_u8_p_p(callee) { \
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 3 \
			POP 2 \
			POP 5 \
			POP 4 \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}

#define s2i_call_u8_p_p_u8(callee) { \
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
	__asm \
		POP 3 \
		POP 2 \
		POP 5 \
		POP 4 \
	__endasm; \
	s2i_allocXstack("1"); \
	__asm \
		POP ACC \
		MOVX A, @DPTR \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("1"); \
}
#define s2i_call_u8_p_u16_u8(callee) \
	s2i_call_u8_p_p_u8(callee)
#define s2i_call_u8_u16_p_u8(callee) \
	s2i_call_u8_p_p_u8(callee)


#define s2i_call_u8_p_p_p(callee) { \
	s2i_pass_arg1_u8();  /* uses R1 */\
	s2i_skipRetBp(); \
	__asm \
		POP 3   ;; pass arg2 high byte in R3\
		POP 2   ;; pass arg2 low byte in R2 \
		POP 5   ;; pass arg3 high byte in R5 \
		POP 4   ;; pass arg3 low byte in R4 \
		s2i_allocXstack("2"); \
		POP 6   \
		POP ACC \
		MOV @DPTR, A \
		INC DPTR \
		MOV A, R6 \
		MOV @DPTR, A \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("2"); \
}


#define s2i_call_p_p(callee) {\
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
    POP 5       ;; high byte goes ito R3 \
    POP 4       ;; low byte goes into R2 \
  __endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}
#define s2i_call_u16_u16(callee) \
	s2i_call_u16_p(callee)
#define s2i_call_u16_p(callee) \
	s2i_call_p_p(callee)
#define s2i_call_p_u16(callee) \
	s2i_call_p_p(callee)

//	(uint8 a1, uint8* a2, uint8 a3)
// stack is [returnAddr H:L][bp][arg2 H:L][arg3]
// param uint8a1 is in DPL => R1
// stack has uint8a3 (1 byte) => R4, uint8stara2 (2 bytes) => R3:R2
#define s2i_call_u8_p_u8(callee) {\
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
		__asm \
			POP 3        ;; uint8stara2 => R3:R2 \
			POP 2 	     ;; \
			POP 4        ;; uint8a3 => R4 \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}
#define s2i_call_u8_u16_u8(callee) \
	s2i_call_u8_p_u8(callee)


// passs arg1 DPL => R1, arg2 stack => R3:R2, arg3 stack => xstack
#define s2i_call_u8_u16_u32(callee) { \
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
	__asm \
		POP 3   ;; arg2 high byte \
		POP 2   ;; arg2 low byte \
	__endasm; \
	s2i_allocXstack("4"); \
	__asm__( \
				"MOV R4, #4   ;; use R4 as a loop counter \n" \
				"MOV A, SP	\n" \
				"ADD A, #-3\n	;; Neo: now sp at arg2(low byte)-1, should move #3. " );  \
	__asm \
		;; move four bytes -- in a loop \
		MOV R0, A \
		SJMP 00003$ \
00002$: \
		INC R0        ;; increment internal pointer \
		INC DPTR      ;; increment external pointer \
00003$: \
		MOV A, @R0    ;; load indirect \
		MOVX @DPTR, A  ;; write to external memory \
		DJNZ R4, 00002$   ;; test loop count \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("4"); \
}


// stack looks like [ret H:L][bp][arg2]
#define s2i_call_p_u8(callee) {\
	s2i_pass_arg1_u16(); \
	__asm \
		;; we optimize here by not calling "s2i_skipRetBp()" because \
		;; we are just reading one byte from (SP) so no need to pop/restore. \
		MOV A, SP   \
	__endasm; \
	__asm__("ADD A, #-3    ;; skip over ret addr and bp \n"); \
	__asm \
		MOV R0, A \
		MOV 1, @R0   ;; first available is R1, so we try it even though it comes after \
		LCALL callee \
	__endasm; \
}
#define s2i_call_u16_u8(callee) \
	s2i_call_p_u8(callee)

// arg1 in DPH:DPL => R3:R2
// arg2 on stack => R1
// arg3 on stack => R5:R4
#define s2i_call_u16_u8_p(callee) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		POP 1      ;; put arg2 in R1 \
		POP 5      ;; put arg3 high byte in R5 \
		POP 4      ;; put arg3 low byte in R4 \
		;; no xstack to restore \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}
#define s2i_call_p_u8_p(callee)  \
	s2i_call_u16_u8_p(callee)
#define s2i_call_p_u8_u16(callee) \
	s2i_call_u16_u8_p(callee)


// arg1 in DPH:DPL => R3:R2
// arg2 on stack => R1
// arg3 on stack => R5:R4
// arg4 on stack => XSTACK
#define s2i_call_u16_u8_p_u8(callee) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		POP 1      ;; put arg2 in R1 \
		POP 5      ;; put arg3 high byte in R5 \
		POP 4      ;; put arg3 low byte in R4 \
	__endasm; \
	s2i_allocXstack("1"); \
	__asm \
		POP ACC       ;; get arg4 \
		MOVX @DPTR, A ;; write it to newly allocated space on xstack \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("1"); \
}



#define s2i_call_p_u8_u8(callee) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
		__asm \
			POP 1 \
			POP 4 \
		__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
}


// (int16* a1, int16* a2, int16* a3)
// stack is (top) [retAddr H:L][bp][arg2 H:L][arg3 H:L]
// params are
// arg1 in DPH:DPL => R3:R2
// arg2 in (internal) stack => R5:R4,
// arg3 in (internal) stack => XSTACK
// strategy: decrement SP by 3 (not 4) first to skip H:L ,
// pop twice to get arg2, (do not pop an extra time),
// pop twice to get arg3, and then restore SP.

#define s2i_call_p_p_p(callee) {\
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		POP 5 ;; pass arg2 into R5:R4 pair, upper byte. istack -3. \
		POP 4 ;; lower byte of arg2 passed in R4; istack -4. \
	__endasm; \
	s2i_allocXstack("2"); \
	__asm \
		POP 1   ;; grab arg3 upper byte from internal stack. istack-5. \
		POP ACC ;; grab arg3 lower byte from internal stack, istack-6. \
		MOVX @DPTR, A ;; XMEM[oldXSP-2] = arg3 lower byte \
		INC DPTR \
		MOV A, R1 \
		MOVX @DPTR, A ;; XMEM[oldXSP-1] = arg3 upper byte \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("2"); \
}
// GATTServApp_RegisterService() -- same type signature as p_p_p(), so
// we reuse it.
#define s2i_call_p_u16_p(callee) \
	s2i_call_p_p_p(callee) 
#define s2i_call_u16_u16_u16(callee) \
	s2i_call_p_p_p(callee)
#define s2i_call_u16_p_u16(callee) \
	s2i_call_p_p_p(callee)
#define s2i_call_p_p_u16(callee) \
	s2i_call_p_p_p(callee)
	

// (uint8* day, uint8* date, uint8* month, uint8* year, uint8* century )
// stack is [ret H:L][bp][arg2][arg3][arg4][arg5]
// pop stack into XStack. set XSP = XSP - 6, load DPTR, then copy.
// arg3 to arg5 -- from istack-5 for 2-byte ptr (was 7 for 3-byte ptr)
#define s2i_call_p_p_p_p_p(callee) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		POP 5 ;; pass arg2 high byte \
		POP 4 ;; pass parg2 low byte \
	__endasm; \
	s2i_allocXstack("6"); \
	__asm__("MOV R1, #3 ;; use R1 as loop count. \n"); \
	__asm \
		;; now copy arg3..5 by popping H and L \
00002$: \
		POP 6 ;; high byte (istack-5,-7,-9 ) \
		POP ACC ;; low byte (istack-6,-8,-10)\
		MOVX @DPTR, A  ;; arg[i] low byte \
		INC DPTR \
		MOV A, R6 ;; get high byte \
		MOVX @DPTR, A  ;; arg[i] high byte \
		INC DPTR \
		;; no need for 2-byte ptr: POP 5 ;; top 0 of arg[i-1], discard \
		DJNZ R1, 00002$ \
		;; finished copying stack parameter. now need to copy arg2! \
		;; stack is now at oldSP - 11; want to point at arg2 high byte \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	/* restore the external stack by adding 6 back */ \
	s2i_deallocXstack("6"); \
}
#define s2i_call_u16_u16_p_u16_u16(callee) \
	s2i_call_p_p_p_p_p(callee)

// this macro is for 3 pointers or more. if 3 then Nptrs = 1;
// stack is [ret H:L][bp][arg2][arg3]...
#define s2i_call_p_p_pn(callee, Nptrs) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		;; pop stack into XStack. set XSP = XSP - (2*Nptrs), load DPTR, then copy. \
		;; arg3 to n -- from istack-5 down (was -7 for 3-byte ptr)\
		POP 5 ;; pass arg2 high byte in R5 \
		POP 4 ;; pass arg2 low byte in R4 \
	__endasm;\
	s2i_allocXstack("(" #Nptrs "*2)"); \
	__asm__("MOV R1, #" #Nptrs " ;; use R1 as loop count. \n"); \
	__asm \
		;; now copy arg3..(Nptrs+2) by popping H and L \
00002$: \
		POP 6 ;; high byte \
		POP ACC ;; low byte \
		MOVX @DPTR, A  ;; arg[i] low byte \
		INC DPTR \
		MOV A, R6 ;; get high byte \
		MOVX @DPTR, A  ;; arg[i] high byte \
		INC DPTR \
		;; no need for 2-byte ptr: POP 5 ;; top 0 of arg[i-1], discard \
		DJNZ R1, 00002$ \
		;; finished copying stack parameter. \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	/* restore the external stack by adding 2*Nptrs back */ \
	s2i_deallocXstack("(" #Nptrs "* 2)"); \
}


// Nptr is number of pointers beyond 2.  so if there are 6 p's followed
// by a u8, then pass Nptr=4.
// stack is [ret H:L][bp][arg2H:L][arg3H:L]..[arg(N+2)H:L]    [argLast]
// positions are[0:1][ 2][    3:4][    5:6]..[(3+2*N):(3+2*N)+1][5+2*N]
// pass [arg3..arg(N+2)] on xstack, argLast in R1.
#define s2i_call_p_p_pn_u8(callee, Nptrs) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		POP 5   ;; pass arg2 high byte in R5 \
		POP 4   ;; pass arg2 low byte in R4 \
	__endasm; \
	s2i_allocXstack("(" #Nptrs "*2)"); \
	__asm__("MOV R1, #" #Nptrs " ;; use R1 as loop count. \n"); \
	__asm \
		;; now copy arg3..arg(N+2) by popping H and L \
00002$: \
		POP 6 ;; high byte \
		POP ACC ;; low byte \
		MOVX @DPTR, A  ;; arg[i] low byte \
		INC DPTR \
		MOV A, R6 ;; get high byte \
		MOVX @DPTR, A  ;; arg[i] high byte \
		INC DPTR \
		DJNZ R1, 00002$ \
		;; finished copying stack parameter.   \
		;; pop one more to pass in R1 \
		POP 1 \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	/* restore the external stack by adding 2*Nptrs back */ \
	s2i_deallocXstack("(" #Nptrs "*2)"); \
}
#define s2i_call_p_p_p_p_p_p_u8(callee) \
	s2i_call_p_p_pn_u8(callee, 4)
#define s2i_call_u16_p_u16_p_p_u16_u8(callee) \
	s2i_call_p_p_p_p_p_p_u8(callee)

#define s2i_call_p_p_p_p_u8(callee) \
	s2i_call_p_p_pn_u8(callee, 2)
#define s2i_call_u16_u16_u16_u16_u8(callee) \
	s2i_call_p_p_p_p_u8(callee)



#define s2i_call_u8_u8_u8_u8_u8_u8_u8(callee) { \
	s2i_pass_arg1_u8(); \
	s2i_skipRetBp(); \
	/* pass param R1-R5 and stack */ \
	__asm \
		POP 2 ;; arg2, stack-4\
		POP 3 ;; arg3, stack-5\
		POP 4 ;; arg4, stack-6\
		POP 5 ;; arg5, stack-7\
	__endasm; \
	s2i_allocXstack("2"); \
	__asm \
			POP A ;; arg6, stack-8\
			MOVX @DPTR, A \
			INC DPTR \
			POP A ;; arg7, stack-9 \
			MOVX @DPTR, A \
			;; restore internal stack \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	s2i_deallocXstack("2"); \
}

// (uint8* day, uint8* date, uint8* month, uint8* year, uint8* century )
// stack is [ret H:L][bp][arg2 H:L][arg3 H:L][arg4][arg5 H:L][arg6 H:L]
// arg1=>R3:R2, arg2=>R5:R4, arg4=>R1
// xstack=> [arg3 H:L][arg5 H:L][arg6 H:L]
#define s2i_call_u16_p_p_u8_u16_u16(callee) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		;; pop stack into XStack. set XSP = XSP - 6, load DPTR, then copy. \
		;; arg3,5,6 -- from istack-5:-6, istack-8:-9, -10:-11) \
		POP 5 ;; pass arg2 high byte in R5 \
		POP 4 ;; pass arg2 low byte in R4 \
	__endasm;\
	s2i_allocXstack("6"); \
	__asm__("MOV R7, #3 ;; use R7 as loop count. \n" ); \
	__asm \
		;; now copy arg3,5,6 by popping H and L \
00002$: \
		POP 6 ;; high byte (istack-5,-8,-10 ) \
		POP ACC ;; low byte (istack-6,-9,-11)\
		MOVX @DPTR, A  ;; arg[i] low byte \
		INC DPTR \
		MOV A, R6 ;; get high byte \
		MOVX @DPTR, A  ;; arg[i] high byte \
		INC DPTR \
		;; no need for 2-byte ptr: POP 5 ;; top 0 of arg[i-1], discard \
	__endasm;\
	__asm__("CJNE R7, #3, 00003$\n");\
	__asm \
		;; in case of arg3, need to skip arg4 and put it in R1 \
		POP 1 ;; stack-8 \
	00003$:\
		DJNZ R7, 00002$ \
	__endasm; \
	s2i_restoreSPfromB(); \
	s2i_call(callee); \
	/* restore the external stack by adding 6 back */ \
	s2i_deallocXstack("6"); \
}

//
// stack is [ret H:L][bp][arg2 H:L][arg3][arg4 H:L][arg5 H:L][arg6]
// arg1=>R3:R2, arg2=>R5:R4, arg3=>R1,
// xstack=> [arg4 H:L][arg5 H:L][arg6]
// 
#define s2i_call_p_p_u8_p_u16_u8(callee) { \
	s2i_pass_arg1_u16(); \
	s2i_skipRetBp(); \
	__asm \
		;; pop stack into XStack. set XSP = XSP - 5, load DPTR, then copy. \
		;; arg 4,5,6 -- from istack-6:-7, istack-8:-9, -10 \
		POP 5   ;; pass arg2 high byte in R5 \
		POP 4   ;; pass arg2 low byte in R4 \
		POP 1   ;; pass arg3 in R1 \
	__endasm;\
	s2i_allocXstack("5"); \
		__asm__("MOV R6, #2 ;; use R6 as loop count. \n"); \
		__asm \
			;; now copy arg4,5 by popping H and L \
	00002$: \
			POP 5 ;; high byte (istack-6,-8) \
			POP ACC ;; low byte (istack-7,-9)\
			MOVX @DPTR, A  ;; arg[i] low byte \
			INC DPTR \
			MOV A, R5 ;; get high byte \
			MOVX @DPTR, A  ;; arg[i] high byte \
			INC DPTR \
			DJNZ R6, 00002$ \
			;; now pop one more time to copy arg6 to xstack \
			POP ACC ;; istack-10\
			MOVX @DPTR, A ;; \
		__endasm; \
		s2i_restoreSPfromB();\
		s2i_call(callee); \
		/* restore the external stack by adding 5 back */ \
	s2i_deallocXstack("5"); \
}

///////////////////////////////////////////////////////////////////
// This section handles return values.

// return in R1 by IAR,
// we copy it to DPL for SDCC.
#define s2i_ret_u8() { \
	__asm \
		MOV DPL, R1 \
	__endasm; \
}

#define s2i_ret_u16() { \
	__asm \
		MOV DPL, R2 \
		MOV DPH, R3 \
	__endasm; \
}
#define s2i_ret_p()  \
	s2i_ret_u16()

#define s2i_ret_u24() { \
	__asm \
		MOV DPL, R1 \
		MOV DPH, R2 \
		MOV B, R3 \
	__endasm; \
}

#define s2i_ret_u32() { \
	__asm \
		MOV DPL, R2 \
		MOV DPH, R3 \
		MOV B, R4 \
		MOV A, R5 \
	__endasm; \
}



#endif
