LOADI R0, #0x0003    ; base value 3
LOADI R2, #0x0001    ; shift amount starts at 1 (will end at 6)

SHFT  R1, R0, R2     ; R1 = 3 << 1 = 6

ADDI  R2, R2, #1     ; shift = 2
SHFT  R3, R0, R2     ; R3 = 3 << 2 = 12

ADDI  R2, R2, #1     ; shift = 3
SHFT  R4, R0, R2     ; R4 = 3 << 3 = 24

ADDI  R2, R2, #1     ; shift = 4
SHFT  R5, R0, R2     ; R5 = 3 << 4 = 48

ADDI  R2, R2, #1     ; shift = 5
SHFT  R6, R0, R2     ; R6 = 3 << 5 = 96

ADDI  R2, R2, #1     ; shift = 6 (R2 now 6 as expected)
SHFT  R7, R0, R2     ; R7 = 3 << 6 = 192

HALT
