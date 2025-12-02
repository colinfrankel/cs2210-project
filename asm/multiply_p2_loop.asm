LOADI R1, #0x000A     ; current value = 10 (5 * 2^1)
LOADI R2, #0x0000     ; pointer to data memory address (starts at 0)
LOADI R3, #0x0009     ; loop counter: 9 values to store

LOOP:
    STORE R1, [R2, #0] ; mem[R2 + 0] = R1
    ADDI  R2, R2, #1   ; advance pointer to next address
    ADD   R1, R1, R1   ; double value for next entry

    ADDI  R3, R3, #-1  ; decrement counter
    BNE   LOOP         ; continue until counter reaches zero

HALT