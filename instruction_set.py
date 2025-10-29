"""
This is the instruction set for our CPU---Catamount processing unit.
It supports only a small set of instructions.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

"""
from dataclasses import dataclass  # For Instruction class, below.


# Instruction set specification
ISA = {
    'LOADI': {
        'opcode': 0x0,
        'format': 'I',
        'variant': 'imm-only',
        'fields': ['opcode(4)', 'rd(3)', 'imm(8)', 'zero(1)'],
        'semantics': 'Rd <-- imm8 (zero-extended)',
        'description': 'Load immediate 8-bit constant into Rd.',
        'register_write': True,
        'memory_write': False,
        'alu': False,
        'immediate': True,
        'branch': False
    },
    'LUI': {
        'opcode': 0x1,
        'format': 'I',
        'variant': 'imm-only',
        'fields': ['opcode(4)', 'rd(3)', 'imm(8)', 'zero(1)'],
        'semantics': 'Rd[15:8] <-- imm8, Rd[7:0] <-- 0',
        'description': 'Load immediate into upper byte of Rd.',
        'register_write': True,
        'memory_write': False,
        'alu': False,
        'immediate': True,
        'branch': False
    },
    'LOAD': {
        'opcode': 0x2,
        'format': 'M',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'addr(6)'],
        'semantics': 'Rd <-- MEM[Ra + signextend(addr6)]',
        'description': 'Load word from memory at Ra + offset into Rd.',
        'register_write': True,
        'memory_write': False,
        'alu': False,
        'immediate': False,
        'branch': False
    },
    'STORE': {
        'opcode': 0x3,
        'format': 'M',
        'fields': ['opcode(4)', 'ra(3)', 'rb(3)', 'addr(6)'],
        'semantics': 'MEM[Rb + signextend(addr6)] <-- Ra',
        'description': 'Store Ra to memory at Rb + offset.',
        'register_write': False,
        'memory_write': True,
        'alu': False,
        'immediate': False,
        'branch': False
    },
    'ADDI': {
        'opcode': 0x4,
        'format': 'I',
        'variant': 'reg+imm',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'imm(6)'],
        'semantics': 'Rd <-- Ra + signextend(imm6)',
        'description': 'Add signed 6-bit immediate value to Ra.',
        'register_write': True,
        'memory_write': False,
        'alu': True,
        'immediate': True,
        'branch': False
    },
    'ADD': {
        'opcode': 0x5,
        'format': 'R',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'rb(3)', 'zero(3)'],
        'semantics': 'Rd <-- Ra + Rb',
        'description': 'Add values in two registers.',
        'register_write': True,
        'memory_write': False,
        'alu': True,
        'immediate': False,
        'branch': False
    },
    'SUB': {
        'opcode': 0x6,
        'format': 'R',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'rb(3)', 'zero(3)'],
        'semantics': 'Rd <-- Ra − Rb',
        'description': 'Subtract value in Rb from value in Ra.',
        'register_write': True,
        'memory_write': False,
        'alu': True,
        'immediate': False,
        'branch': False
    },
    'AND': {
        'opcode': 0x7,
        'format': 'R',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'rb(3)', 'zero(3)'],
        'semantics': 'Rd <-- Ra & Rb',
        'description': 'Bitwise AND of two registers.',
        'register_write': True,
        'memory_write': False,
        'alu': True,
        'immediate': False,
        'branch': False
    },
    'OR': {
        'opcode': 0x8,
        'format': 'R',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'rb(3)', 'zero(3)'],
        'semantics': 'Rd <-- Ra | Rb',
        'description': 'Bitwise OR of two registers.',
        'register_write': True,
        'memory_write': False,
        'alu': True,
        'immediate': False,
        'branch': False
    },
    'SHFT': {
        'opcode': 0x9,
        'format': 'R',
        'fields': ['opcode(4)', 'rd(3)', 'ra(3)', 'rb(3)', 'zero(3)'],
        'semantics': 'if Rb >= 0: Rd <-- Ra << Rb else Rd <-- Ra >> |Rb|',
        'description': 'Logical shift left or right depending on sign of Rb.',
        'register_write': True,
        'memory_write': False,
        'alu': True,
        'immediate': False,
        'branch': False
    },
    'BEQ': {
        'opcode': 0xA,
        'format': 'B',
        'variant': 'cond',
        'fields': ['opcode(4)', 'ra(3)', 'offset(8)', 'zero(1)'],
        'semantics': 'if Z == 1: PC <-- Ra + signextend(offset8)',
        'description': 'Branch if zero flag is set.',
        'register_write': False,  # writes directly to PC, not general-purpose register
        'memory_write': False,
        'alu': False,
        'immediate': False,
        'branch': True
    },
    'BNE': {
        'opcode': 0xB,
        'format': 'B',
        'variant': 'cond',
        'fields': ['opcode(4)', 'ra(3)', 'offset(8)', 'zero(1)'],
        'semantics': 'if Z == 0: PC <-- Ra + signextend(offset8)',
        'description': 'Branch if zero flag is clear.',
        'register_write': False,  # writes directly to PC, not general-purpose register
        'memory_write': False,
        'alu': False,
        'immediate': False,
        'branch': True
    },
    'B': {
        'opcode': 0xC,
        'format': 'B',
        'variant': 'uncond',
        'fields': ['opcode(4)', 'ra(3)', 'offset(8)', 'zero(1)'],
        'semantics': 'PC <-- Ra + signextend(offset8)',
        'description': 'Unconditional branch using register base plus signed 8-bit offset.',
        'register_write': False,
        'memory_write': False,
        'alu': False,
        'immediate': False,
        'branch': True
    },
    'CALL': {
        'opcode': 0xD,
        'format': 'B',
        'variant': 'link',
        'fields': ['opcode(4)', 'offset(8)', 'zero(4)'],
        'semantics': 'Push (PC + 2); PC <-- PC + signextend(offset8)',
        'description': 'Call subroutine at address given by signed 8-bit immediate. '
                       'Return address (PC + 2) is pushed onto stack.',
        'register_write': False,
        'memory_write': False,
        'alu': False,
        'immediate': True,  # offset
        'branch': True
    },
    'RET': {
        'opcode': 0xE,
        'format': 'B',
        'variant': 'ret',
        'fields': ['opcode(4)', 'zero(12)'],
        'semantics': 'Pop PC',
        'description': 'Return from subroutine.',
        'register_write': False,
        'memory_write': False,
        'alu': False,
        'immediate': False,
        'branch': True
    },
    'HALT': {
        'opcode': 0xF,
        'format': 'O',
        'variant': 'halt',
        'fields': ['opcode(4)', 'zero(12)'],
        'semantics': 'stop execution',
        'description': 'Halt CPU.',
        'register_write': False,
        'memory_write': False,
        'alu': False,
        'immediate': False,
        'branch': False
    }
}


# Reverse map for opcode lookup
OPCODE_MAP = {v['opcode']: k for k, v in ISA.items()}

def get_instruction_spec(key):
    """
    Helper function. Returns the ISA specification for a
    given mnemonic (str) or opcode (int).
    """
    if isinstance(key, str):
        return ISA[key.upper()]
    return ISA[OPCODE_MAP[key]]


@dataclass
class Instruction:
    """
    Represents a single decoded instruction for the Catamount
    Processing Unit (CPU).

    Fields correspond to the 16-bit ISA specification.

    We use Python dataclass for minimal, lightweight classes,
    almost like structs in C. When we instantiate an instruction,
    `i`, we can access its fields using dot notation, like this:

    i.opcode       # gets us the opcode of instruction i
    i.rd           # gets us the destination register of instruction i
    etc.
    """

    # Defaults (constructor is implicit)
    opcode: int = 0
    mnem: str = ""
    rd: int = 0
    ra: int = 0
    rb: int = 0
    imm: int = 0
    addr: int = 0
    raw: int = 0

    def __post_init__(self):
        """
        This is called immediately after the object is instantiated.
        If raw bytes have been provided, the instruction is auto-
        decoded. If not, then we assume all necessary fields have
        been supplied to the constructor.
        """
        if self.raw:
            self._decode_from_word(self.raw)
        if not self.mnem and self.opcode:
            self.mnem = OPCODE_MAP.get(self.opcode, "???")
        if not self.opcode and self.mnem:
            self.opcode = ISA[self.mnem]['opcode']

    def _decode_from_word(self, word):
        self.opcode = (word >> 12) & 0xF
        self.mnem = OPCODE_MAP.get(self.opcode, "???")
        spec = ISA.get(self.mnem)
        if not spec:
            return
        fmt = spec['format']
        if fmt == 'R':
            self.rd = (word >> 9) & 0x7
            self.ra = (word >> 6) & 0x7
            self.rb = (word >> 3) & 0x7
        elif self.mnem in ('LOADI', 'LUI'):
            self.rd = (word >> 9) & 0x7
            self.imm = word & 0xFF
        elif self.mnem == 'ADDI':
            self.rd = (word >> 9) & 0x7
            self.ra = (word >> 6) & 0x7
            self.imm = word & 0x3F
        elif fmt == 'M':
            self.rd = (word >> 9) & 0x7
            self.ra = (word >> 6) & 0x7
            self.addr = word & 0x3F
        elif fmt == 'B':
            self.ra = (word >> 9) & 0x7
            self.imm = word & 0xFF

    def __repr__(self):
        return (
            f"Instruction({self.mnem} (opcode={self.opcode}): "
            f"rd={self.rd}, ra={self.ra}, rb={self.rb}, "
            f"imm={self.imm}, addr={self.addr}, raw=0x{self.raw:04X})"
        )
