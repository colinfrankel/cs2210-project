; Euclid's GCD algorithm (repeated subtraction, sign-bit version)
;
; Preconditions:
;   R5 contains initial value a (positive)
;   R6 contains initial value b (positive)
; Result:
;   GCD is written to memory at [R0 + #0]

START:
    LOADI R0, #0          ; base memory address
    LOADI R5, #0x2A       ; a = 42 (test case)
    LOADI R6, #0x5A       ; b = 90
    LOADI R3, #0          ; R3 = 0 initially
    LUI   R3, #0x80       ; R3 = 0x8000 mask for sign bit
    CALL  GCD
    HALT

GCD:
    SUB R7, R5, R6        ; R7 = a - b
    BEQ DONE              ; if a == b, exit
    AND R2, R7, R3        ; isolate sign bit of (a - b)
    BEQ A_GE_B            ; if sign bit == 0 then a >= b
    ; else: a < b, subtract a from b
B_GT_A:
    SUB R6, R6, R5        ; b = b - a
    B GCD
A_GE_B:
    SUB R5, R5, R6        ; a = a - b
    B GCD
DONE:
    STORE R5, [R0 + #0]   ; write GCD to memory at address 0
    RET
