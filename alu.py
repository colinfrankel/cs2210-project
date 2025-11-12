"""
Starter code for Catamount Processor Unit ALU

We are limited to 16 bits, and five operations: ADD, SUB, AND, OR, and SHFT.

ALU maintains status flags:

    - N: negative, 1000   (8)
    - Z: zero, 0100       (4)
    - C: carry out, 0010  (2)
    - V: overflow, 0001   (1)

Our ALU will set flags as appropriate on each operation (no special
instructions are needed for setting flags).

- Negative flag is set if the MSB = 1, regardless of operation.

- Zero flag is set if result is zero, regardless of operation.

- Carry flag under the following conditions:
    - If an arithmetic operation is used and a bit is carried out.
    - For similarity with ARM architecture carry is set on a SUB
      if the minuend is larger than the subtrahend, e.g., with
      5 - 2 = 3, 5 is the minuend, and 2 is the subtrahend.
    - On a left shift, the carry flag is set to the value of the last
      bit shifted out. So, for example, in four bits, `0b1001 << 1`
      would set the carry flag to 1. However, `0b1001 << 2` would set
      the carry flag to 0, because the last bit shifted out was 0.
      On a right shift, the carry flag is set to the value of the last
      bit shifted out on the right. For example, `0b1001 >> 1` would
      set carry flag to 1, and `0b1001 >> 2` would set carry flag to 0.
    - In the odd but permitted case of shift by zero, the carry flag
      is left unchanged.
    - Carry flag is never changed on a bitwise operation.

- Overflow only applies to arithmetic operations.
"""

from constants import WORD_SIZE, WORD_MASK

N_FLAG = 0b1000
Z_FLAG = 0b0100
C_FLAG = 0b0010
V_FLAG = 0b0001


class Alu:

    def __init__(self):
        """
        Here we initialize the ALU when instantiated.
        """
        self._op = None
        self._flags = 0b0000
        # Dictionary to look up methods by operation name.
        self._ops = {
            "ADD"  : self._add,
            "SUB"  : self._sub,
            "AND"  : self._and,
            "OR"   : self._or,
            "SHFT" : self._shft
        }

    def set_op(self, op):
        """
        Public-facing setter. Added 2025-11-09. Students will need to add this
        to their ALU implementation.
        """
        if op in self._ops.keys():
            self._op = op
        else:
            raise ValueError(f"Bad op: {op}")
        
        
    def decode(self, c):
        """
        Decode control signal to determine operation.
        """
        c = c & 0b111 # ensure only three bits are used
        match c:
            case 0b000:
                self._op = "ADD"
            case 0b001:
                self._op = "SUB"
            case 0b010:
                self._op = "AND"
            case 0b011:
                self._op = "OR"
            case 0b100:
                self._op = "SHFT"
            case _:
                raise ValueError("Invalid control signal")
        # Return value is for testing.
        # We don't really need return value for normal use.
        return self._op

    # The @property decorator makes a getter method accessible
    # as if it were a property or attribute. For example, we can
    # access the zero flag with `alu.zero`.

    @property
    def zero(self):
        # Return zero flag; do not modify this method!
        return bool(self._flags & Z_FLAG)

    @property
    def negative(self):
        # Return negative flag
        return bool(self._flags & N_FLAG)

    @property
    def carry(self):
        # Return carry flag
        return bool(self._flags & C_FLAG)

    @property
    def overflow(self):
        # Return overflow flag
        return bool(self._flags & V_FLAG)

    def execute(self, a, b):
        """
        Execute operation with operands a and b. This will
        clear flags before operation, then call the function
        that we looked up in self._ops. It returns the result
        as signed to handle two's complement correctly.

        Do not change this method!
        """
        self._flags = 0   # clear flags before operation
        result = self._ops[self._op](a, b)
        return self._to_signed(result)

    def _add(self, a, b):
        """
        ADD
        """
        a = a & WORD_MASK
        b = b & WORD_MASK
        result = (a + b) & WORD_MASK
        self._update_arith_flags_add(a, b, result)
        return result

    def _sub(self, a, b):
        """
        SUB
        """
        a = a & WORD_MASK
        b = b & WORD_MASK
        result = (a - b) & WORD_MASK
        self._update_arith_flags_sub(a, b, result)
        return result

    def _and(self, a, b):
        """
        Bitwise AND
        """
        a = a & WORD_MASK
        b = b & WORD_MASK
        result = (a & b) & WORD_MASK
        self._update_logic_flags(result)
        return result

    def _or(self, a, b):
        """
        Bitwise OR
        """
        a = a & WORD_MASK
        b = b & WORD_MASK
        result = (a | b) & WORD_MASK
        self._update_logic_flags(result)
        return result

    def _shft(self, a, b):
        """
        SHFT

        shift left if b > 0, right if b < 0, no shift if b = 0

        Keep in mind when we shift we need to keep track of the
        last bit shifted out. This is used to set the carry flag.
        """
        a &= WORD_MASK  # Keep this line as is

    # We must interpret the shift amount `b` as a signed WORD_SIZE-bit
    # value (two's complement) so direction (left/right) is determined
    # correctly when b has the MSB set. Also, if the masked shift amount
    # equals zero (e.g. shifting by a multiple of WORD_SIZE), the carry
    # flag must be left unchanged.
        # Determine direction from signed value, but determine magnitude
        # from the low bits of the unsigned representation. This makes
        # e.g. 0x8001 (32769) be a RIGHT shift by 1 (low 4 bits = 1).
        b_u = b & WORD_MASK
        b_signed = self._to_signed(b_u)
        shift = b_u & (WORD_SIZE - 1)

        if b_signed > 0:
            # Left shift
            if shift == 0:
                result = a
                bit_out = None  # None means "leave carry unchanged"
            else:
                result = (a << shift) & WORD_MASK
                bit_out = (a >> (WORD_SIZE - shift)) & 1
        elif b_signed < 0:
            # Right shift
            if shift == 0:
                result = a
                bit_out = None  # leave carry unchanged
            else:
                result = (a >> shift) & WORD_MASK
                bit_out = (a >> (shift - 1)) & 1
        else:
            # No shift
            result = a
            bit_out = None  # leave carry unchanged

        # Update flags; if bit_out is None, _update_shift_flags will
        # preserve the previous carry flag instead of clearing it.
        self._update_shift_flags(result, bit_out)
        return result

    def _to_signed(self, x):
        """
        Helper to convert unsigned to signed

        Do not modify this method!
        """
        if x & (1 << (WORD_SIZE - 1)):
            return x - (1 << WORD_SIZE)
        return x

    def _update_logic_flags(self, result):
        self._flags = 0
        if result & (1 << (WORD_SIZE - 1)):
            self._flags |= N_FLAG
        if result == 0:
            self._flags |= Z_FLAG

    def _update_arith_flags_add(self, a, b, result):
        """
        This is given to you as an example which will help you write
        the other methods to update flags.
        """
        if result & (1 << (WORD_SIZE - 1)):
            self._flags |= N_FLAG
        if result == 0:
            self._flags |= Z_FLAG
        if a + b > WORD_MASK:
            self._flags |= C_FLAG
        sa, sb, sr = ((a >> (WORD_SIZE - 1)) & 1,
                      (b >> (WORD_SIZE - 1)) & 1,
                      (result >> (WORD_SIZE - 1)) & 1)
        if sa == sb and sr != sa:
            self._flags |= V_FLAG

    def _update_arith_flags_sub(self, a, b, result):
        if result & (1 << (WORD_SIZE - 1)):
            self._flags |= N_FLAG
        if result == 0:
            self._flags |= Z_FLAG
        if a >= b:
            self._flags |= C_FLAG
        sa, sb, sr = ((a >> (WORD_SIZE - 1)) & 1,
                      (b >> (WORD_SIZE - 1)) & 1,
                      (result >> (WORD_SIZE - 1)) & 1)
        if sa != sb and sr != sa:
            self._flags |= V_FLAG

    def _update_shift_flags(self, result, bit_out):
        # Preserve existing carry flag unless bit_out explicitly
        # indicates the last bit shifted out (True/False). If
        # bit_out is None, leave carry unchanged (per spec for
        # shift-by-zero).
        existing_carry = self._flags & C_FLAG

        # Reset flags except carry (we'll reapply carry below)
        self._flags = 0
        if result & (1 << (WORD_SIZE - 1)):
            self._flags |= N_FLAG
        if result == 0:
            self._flags |= Z_FLAG

        if bit_out is None:
            # Leave carry unchanged
            self._flags |= existing_carry
        elif bit_out:
            self._flags |= C_FLAG
