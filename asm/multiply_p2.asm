LOADI R0, #0x03 ; the original constant operand, 3
LOADI R1, #0x06 ; the greatest power of two we multiply by

ADD   R1, R0, R7 ; R1 = 3
ADD   R2, R1, R1 ; R2 = 6
ADD   R3, R2, R2 ; R3 = 12
ADD   R4, R3, R3 ; R4 = 24
ADD   R5, R4, R4 ; R5 = 48
ADD   R6, R5, R5 ; R6 = 96

HALT