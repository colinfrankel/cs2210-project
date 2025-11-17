"""
In our Catamount Processing Unit we have eight general purpose registers.
These do not include special-purpose registers elsewhere in the CPU:
  - instruction register,
  - program counter,
  - etc.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

"""

from constants import WORD_SIZE


class Register:
    """
    Class representing a single register.

    Registers understand their name, e.g., R0, R1, ..., etc. and the range
    of values they can store (and not much else).
    """

    MAX_VALUE = 2**WORD_SIZE - 1
    MIN_VALUE = -(2**WORD_SIZE - 1)  # or 0 - 2 ** WORD_SIZE - 1 ?

    def __init__(self, name):
        self.name = name
        self.value = 0

    def read(self):
        return self.value

    def write(self, value):
        if value < self.MIN_VALUE or value > self.MAX_VALUE:
            raise ValueError("Value out of bounds!")
        else:
            self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value:04X}"


class RegisterFile:
    """
    Two read port, one write port register file, with the specified number
    of registers.
    """

    NUM_REGISTERS = 8

    def __init__(self):
        self.registers = []
        for i in range(self.NUM_REGISTERS):
            reg_name = f"R{i}"
            self.registers.append(Register(reg_name))

    def _check_index(self, idx):
        """
        We cannot rely on Python's index out-of-bounds, because we don't want
        to permit negative indices (permitted by Python).
        """
        if not 0 <= idx < self.NUM_REGISTERS:
            raise IndexError("Register index out of bounds!")

    def _read(self, ra, rb):
        """
        Read has been requested.

        Check bounds on `ra`, and check bounds on `rb` (if not None).

        Ensure source register(s) correctly specified. If `ra` and `rb` are
        both `None` raise `TypeError` with message: "Cannot read; no source
        register(s) specified!". If `rb` specified and not `ra`, raise
        `TypeError` with message: "Cannot read; single register read should
        specify `ra`!"

        If only `ra` is specified, return tuple: (value of `ra`, `None`).
        If both `ra` and `rb` are specified, return tuple: (value of `ra`,
        value of `rb`).

        """
        self._check_index(ra)
        if rb is not None:
            self._check_index(rb)
        return (self.registers[ra].read(), self.registers[rb].read() if rb is not None else None)

    def _write(self, rd, data):
        """This is called if `write_enable` is `True`. This is how we detect
        that a write is intended. However, we need a destination and data for a
        successful write, so we have two failure modes (at this level):

            - `rd` is None
            - `data` is None

        Each of these should raise a `TypeError`. To simplify raising of
        exceptions, handle these in the order: bad `rd`, bad `data`.
        Messages should be:

            - "Cannot write; no destination specified!"
            - "Cannot write: no data!"

        respectively.

        Check bounds on `rd`.
        """
        if rd is None:
            raise TypeError
        if data is None:
            raise TypeError
        self._check_index(rd)
        self.registers[rd].write(data)

    def execute(self, rd=None, ra=None, rb=None, data=None, write_enable=False):
        """
        `rd`: destination register (an `int`)
        `ra`: source register 1 (an `int`)
        `rb`: source register 2 (an `int`)
        `data`: data to write (an `int`)
        `write_enable`: `True` to enable write or `False`
        """
        if write_enable:
            self._write(rd, data)  # looks like a write
            return

        return self._read(ra, rb)  # looks like a read

    def __repr__(self):
        # Notice that this expects a member field `registers`, a list.
        vals = [str(r) for r in self.registers]
        return "\n".join(vals)


if __name__ == "__main__":

    # Quick smoke test...
    rf = RegisterFile()
    rf.execute(ra=0)
    rf.execute(rd=4, data=0xABCD, write_enable=True)

    print(rf)
