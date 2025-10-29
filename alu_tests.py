"""
Tests for Catamount Processor Unit ALU

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

"""

from alu import Alu

if __name__ == '__main__':

    tests = [{'opcode': 0b000, 'mnemonic': 'ADD',
             'a': 6, 'b': 3, 'expected': 9,
             'flags': {'zero': False, 'negative': False,
                       'carry': False, 'overflow': False}},
             {'opcode': 0b000, 'mnemonic': 'ADD',
              'a': 0, 'b': 0, 'expected': 0,
              'flags': {'zero': True, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b001, 'mnemonic': 'SUB',
              'a': 3, 'b': 3, 'expected': 0,
              'flags': {'zero': True, 'negative': False,
                        'carry': True, 'overflow': False}},  # because no borrow
             {'opcode': 0b001, 'mnemonic': 'SUB',
              'a': 3, 'b': 5, 'expected': -2,
              'flags': {'zero': False, 'negative': True,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b001, 'mnemonic': 'SUB',
              'a': 5, 'b': 3, 'expected': 2,
              'flags': {'zero': False, 'negative': False,
                        'carry': True, 'overflow': False}},  # because no borrow
             {'opcode': 0b010, 'mnemonic': 'AND',
              'a': 15, 'b': 240, 'expected': 0,
              'flags': {'zero': True, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b010, 'mnemonic': 'AND',
              'a': 15, 'b': 241, 'expected': 1,
              'flags': {'zero': False, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b011, 'mnemonic': 'OR',
              'a': 85, 'b': 42, 'expected': 127,
              'flags': {'zero': False, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b100, 'mnemonic': 'SHFT',
              'a': 1, 'b': -1, 'expected': 0,
              'flags': {'zero': True, 'negative': False,
                        'carry': True, 'overflow': False}},  # last bit shifted out
             {'opcode': 0b100, 'mnemonic': 'SHFT',
              'a': 1, 'b': 1, 'expected': 2,
              'flags': {'zero': False, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b100, 'mnemonic': 'SHFT',
              'a': 1, 'b': 15, 'expected': -32768,
              'flags': {'zero': False, 'negative': True,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b100, 'mnemonic': 'SHFT',
              'a': 1, 'b': 100, 'expected': 16,
              'flags': {'zero': False, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b000, 'mnemonic': 'ADD',
              'a': 32767, 'b': 1, 'expected': -32768,
              'flags': {'zero': False, 'negative': True,
                        'carry': False, 'overflow': True}},
             {'opcode': 0b100, 'mnemonic': 'SHFT',
              'a': 42, 'b': 0, 'expected': 42,
              'flags': {'zero': False, 'negative': False,
                        'carry': False, 'overflow': False}},
             {'opcode': 0b100, 'mnemonic': 'SHFT',
              'a': 42, 'b': 0, 'expected': 42,
              'flags': {'zero': False, 'negative': False,
                        'carry': False, 'overflow': False}}
             ]

    alu = Alu()  # instantiate ALU object

    failures = 0
    count = 0
    print("Running ALU self-test...")

    for count, t in enumerate(tests, 1):
        print(f"\n{t['mnemonic']}: {t['a']}, {t['b']}...")
        alu.decode(t['opcode'])
        if t['mnemonic'] == 'SHFT' and abs(t['b']) > 15:
            print("Shift amount is masked to 15 bits.")
            print("Shift amounts beyond word size wrap modulo 16.")
            if t['b'] < 0:
                print("Second operand is negative. Shift RIGHT.")
            elif t['b'] > 0:
                print("Second operand is positive. Shift LEFT.")
            else:
                print("Second operand is zero. No shift.")
            print(f"This will shift by {abs(t['b']) & 0xF}.")
        try:
            r = alu.execute(t['a'], t['b'])
            expected = t['expected']
            assert r == expected, f"Expected {expected}, got {r}"
            for k, v in t['flags'].items():
                assert getattr(alu, k) == v, f"Expected {v} for {k}, got {getattr(alu, k)}"
            print(f"Expected {expected}, got {r}, with flags {t['flags']}")
            print(f"Flags: {alu._flags:04b} (NZCV)")
            print("Passed!")
        except AssertionError as e:
            failures += 1
            print("Failed!")
            print(f"   {e}\n")

    if failures:
        print(f"\n{failures} of {count} tests failed.")
    else:
        print(f"\nAll {count} tests passed.")
