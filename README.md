For our final project we will build our own CPU simulator. Really.

We’ll call our CPU the Catamount Processing Unit.

We’re not going to try to simulate a real CPU with thousands of instructions in its instruction set, or any pipelining, or anything like that. We’re also not going to model down to the level of logic gates. But we will model a simplified CPU, at appropriate levels of abstraction.

This will be a guided project, with plenty of resources and scaffolding. We will spend time in labs to facilitate this. The remaining homeworks (2) will serve as checkpoints for the project.

We will implement our CPU in Python.

You should work in small teams of two or three people. I will not assign you to teams (unless you insist), but I will facilitate with introductions if you’re having trouble finding others to work with.

Everyone on a team must contribute to the project, and part of your project report will be an account of your individual contributions.

# Basic specifications

## Word size
Our CPU is a 16-bit RISC CPU. Words, instructions, and memory addresses are 16-bits—that’s two bytes.

## Memory architecture
Our CPU uses a Harvard architecture, meaning that there are separate memory stores for instructions and data. Accordingly, there are separate memory interfaces for instructions and data.


## Instruction set
We allow four bits for instruction opcodes. This means our architecture supports only 16 instructions.

Here is the instruction set.

### LOADI
- Opcode: 0
- Description: Load immediate 8-bit constant into Rd.
- Format: I
- Variant: imm-only
- Fields: opcode(4), rd(3), imm(8), zero(1)
- Semantics: Rd <– imm8 (zero-extended)
- Register write: True
- Memory write: False
- ALU: False
- Immediate: True
- Branch: False

### LUI
- Opcode: 1
- Description: Load immediate into upper byte of Rd.
- Format: I
- Variant: imm-only
- Fields: opcode(4), rd(3), imm(8), zero(1)
- Semantics: Rd[15:8] <– imm8
- Register write: True
- Memory write: False
- ALU: False
- Immediate: True
- Branch: False


### LOAD

- Opcode: 2
- Description: Load word from memory at Ra + offset into Rd.
- Format: M
- Fields: opcode(4), rd(3), ra(3), addr(6)
- Semantics: Rd <– MEM[Ra + signextend(addr6)]
- Register write: True
- Memory write: False
- ALU: True
- Immediate: False
- Branch: False


### STORE
- Opcode: 3
- Description: Store Ra to memory at Rb + offset.
- Format: M
- Fields: opcode(4), ra(3), rb(3), addr(6)
- Semantics: MEM[Rb + signextend(addr6)] <– Ra
- Register write: False
- Memory write: True
- ALU: True
- Immediate: False
- Branch: False

### ADDI
- Opcode: 4
- Description: Add signed 6-bit immediate value to Ra.
- Format: I
- Variant: reg+imm
- Fields: opcode(4), rd(3), ra(3), imm(6)
- Semantics: Rd <– Ra + signextend(imm6)
- Register write: True
- Memory write: False
- ALU: True
- Immediate: True
- Branch: False

### ADD
- Opcode: 5
- Description: Add values in two registers.
- Format: R
- Fields: opcode(4), rd(3), ra(3), rb(3), zero(3)
- Semantics: Rd <– Ra + Rb
- Register write: True
- Memory write: False
- ALU: True
- Immediate: False
- Branch: False

### SUB
- Opcode: 6
- Description: Subtract value in Rb from value in Ra.
- Format: R
- Fields: opcode(4), rd(3), ra(3), rb(3), zero(3)
- Semantics: Rd <– Ra − Rb
- Register write: True
- Memory write: False
- ALU: True
- Immediate: False
- Branch: False

### AND
- Opcode: 7
- Description: Bitwise AND of two registers.
- Format: R
- Fields: opcode(4), rd(3), ra(3), rb(3), zero(3)
- Semantics: Rd <– Ra & Rb
- Register write: True
- Memory write: False
- ALU: True
- Immediate: False
- Branch: False

### OR
- Opcode: 8
- Description: Bitwise OR of two registers.
- Format: R
- Fields: opcode(4), rd(3), ra(3), rb(3), zero(3)
- Semantics: Rd <– Ra | Rb
- Register write: True
- Memory write: False
- ALU: True
- Immediate: False
- Branch: False

### SHFT
- Opcode: 9
- Description: Logical shift left or right depending on MSB of Rb. Absolute value of shift amount is limited to 15. We use the MSB of Rb to indicate direction of the shift.If MSB is zero, then left shift; otherwise, right shift.We use the lowest four bits of Rb for shift amount.
- Format: R
- Fields: opcode(4), rd(3), ra(3), rb(3), zero(3)
- Semantics: if Rb & 0x8000: Rd <– Ra >> (Rb & 0xF) else Rd <– Ra << (Rb & 0xF)
- Register write: True
- Memory write: False
- ALU: True
- Immediate: False
- Branch: False

### BEQ
- Opcode: 10
- Description: Branch if zero flag is set.
- Format: B
- Variant: cond
- Fields: opcode(4), ra(3), offset(8), zero(1)
- Semantics: if Z == 1: PC <– Ra + signextend(offset8)
- Register write: False
- Memory write: False
- ALU: True
- Immediate: True
- Branch: True

### BNE
- Opcode: 11
- Description: Branch if zero flag is clear.
- Format: B
- Variant: cond
- Fields: opcode(4), ra(3), offset(8), zero(1)
- Semantics: if Z == 0: PC <– Ra + signextend(offset8)
- Register write: False
- Memory write: False
- ALU: True
- Immediate: True
- Branch: True

### B
- Opcode: 12
- Description: Unconditional branch by signed 8-bit PC-relative offset.
- Format: B
- Variant: uncond
- Fields: opcode(4), offset(8), zero(4)
- Semantics: PC <– PC + signextend(offset8)
- Register write: False
- Memory write: False
- ALU: False
- Immediate: True
- Branch: True

### CALL
- Opcode: 13
- Description: Call subroutine at address given by PC + signed 8-bit immediate. Return address (PC + 2) is pushed onto stack.
- Format: B
- Variant: link
- Fields: opcode(4), offset(8), zero(4)
- Semantics: Push (PC + 2); PC <– PC + signextend(offset8)
- Register write: False
- Memory write: False
- ALU: True
- Immediate: True
- Branch: True

### RET
- Opcode: 14
- Description: Return from subroutine.
- Format: B
- Variant: ret
- Fields: opcode(4), zero(12)
- Semantics: Pop PC
- Register write: False
- Memory write: False
- ALU: False
- Immediate: False
- Branch: True

### HALT
- Opcode: 15
- Description: Halt CPU.
- Format: O
- Variant: halt
- Fields: opcode(4), zero(12)
- Semantics: stop execution
- Register write: False
- Memory write: False
- ALU: False
- Immediate: False
- Branch: False

| **format** | **fields**                                                  | **instructions**        |
|------------|-------------------------------------------------------------|-------------------------|
| **R**      | opcode(4), rd(3), ra(3), rb(3), zero(3)                     | ADD, SUB, AND, OR, SHFT |
| **I**      | opcode(4), rd(3), imm(8), zero(1)   or rd(3), ra(3), imm(6) | LOADI, LUI, ADDI        |
| **M**      | opcode(4), rd(3), ra(3), addr(6)                            | LOAD, STORE             |
| **B**      | opcode(4), ra(3), offset(8), zero(1)                        | BEQ, BNE, B, CALL, RET  |
| **O**      | opcode(4), zero(12)                                         | HALT                    |

Custom assembler and disassembler will be provided at the appropriate time.

## ALU

There is one ALU, which supports ADD, ADDI, SUB, AND, OR, and SHFT. The ALU resets and then sets flags on all operations. Flags are Z (zero), N (negative), C (carry), and V (overflow).

## Register file

There is one register file, with eight general-purpose registers. Registers are 16-bits wide.



<br>
<br>

---

© 2025 Clayton Cafiero.