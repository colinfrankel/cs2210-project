LOADI R1, #0x000A     ; current value = 10 (5 * 2^1)
LOADI R2, #0x0000     ; pointer to data memory address (starts at 0)
LOADI R3, #0x0009     ; loop counter: 9 values to store
LOADI R4, #0x0001     ; constant 1 for shift amount and decrement

LOOP:
    STORE R1, [R2]     ; mem[R2] = R1
    ADDI  R2, R2, #1   ; advance pointer to next address
    SHFT  R1, R1, R4   ; double value for next entry (shift left by 1)

    SUB   R3, R3, R4   ; decrement counter
    BNE   LOOP         ; continue until counter reaches zero

HALT
