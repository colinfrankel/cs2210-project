LOADI R0, #0xAA      ; operand A (patched in tests)
LOADI R1, #0x55      ; operand B (patched in tests)
LOADI R2, #0x0000    ; default result = 0

AND   R3, R0, R1     ; overlap between operands sets flags
BNE   DONE           ; if overlap != 0, keep R2 = 0

OR    R2, R0, R1     ; otherwise, no overlap: result is OR

DONE:
HALT
