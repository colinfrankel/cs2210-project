LOADI R0, #0x00C0    ; base value = 448 (0x01C0)
LUI   R0, #0x01

LOADI R1, #0x0001    ; shift amount starts at 1 (MSB=1 means right shift)
LUI   R1, #0x80

SHFT  R2, R0, R1     ; R2 = R0 >> 1 = 224
ADDI  R1, R1, #1     ; next shift amount = 2
SHFT  R3, R0, R1     ; R3 = R0 >> 2 = 112
ADDI  R1, R1, #1     ; next shift amount = 3
SHFT  R4, R0, R1     ; R4 = R0 >> 3 = 56
ADDI  R1, R1, #1     ; next shift amount = 4
SHFT  R5, R0, R1     ; R5 = R0 >> 4 = 28
ADDI  R1, R1, #1     ; next shift amount = 5
SHFT  R6, R0, R1     ; R6 = R0 >> 5 = 14
ADDI  R1, R1, #1     ; next shift amount = 6 (final value of R1)
SHFT  R7, R0, R1     ; R7 = R0 >> 6 = 7

HALT
