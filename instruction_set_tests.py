"""
Minimal human-eyeball tests for sanity of instruction set
helper function, opcode map, and Instruction class.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

"""

from instruction_set import OPCODE_MAP, get_instruction_spec, Instruction

if __name__ == '__main__':

    # Try a few instruction specs
    print("Test instruction spec helper function...")
    print(get_instruction_spec('ADD'))
    print(get_instruction_spec('LOADI'))
    print(get_instruction_spec('HALT'))
    print()

    # Print the opcode map
    print("Test opcode map...")
    print(OPCODE_MAP)
    print()

    # Test the instruction class
    print("Test instruction class...")
    i = Instruction(raw=0xD010)
    print(i)
    i = Instruction(opcode=0xD, rd=0, ra=0, rb=0, imm=16, addr=0)
    print(i)
    i = Instruction(raw=0x6250)
    print(i)
    i = Instruction(opcode=0x6, rd=1, ra=1, rb=2, imm=0, addr=0)
    print(i)
