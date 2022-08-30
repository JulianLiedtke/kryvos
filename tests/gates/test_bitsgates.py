import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.bits as bits
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class BitsGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        self.group = WireGroup(11)
        Wire.n_mul = 0
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_splitgate_split(self):
        expected = []
        expected.append((0, [0, 0, 0, 0]))
        expected.append((1, [0, 0, 0, 1]))
        expected.append((2, [0, 0, 1, 0]))
        expected.append((3, [0, 0, 1, 1]))
        expected.append((4, [0, 1, 0, 0]))
        expected.append((5, [0, 1, 0, 1]))
        expected.append((6, [0, 1, 1, 0]))
        expected.append((7, [0, 1, 1, 1]))
        expected.append((8, [1, 0, 0, 0]))
        expected.append((9, [1, 0, 0, 1]))
        expected.append((10, [1, 0, 1, 0]))
        for i, exp_res in expected:
            wire = self.group.gen(i)
            act_res = bits.split(self.group, wire)
            for exp_wire, act_wire in zip(exp_res, act_res):
                self.assertEqual(exp_wire, int(act_wire))
                self.assertTrue(isinstance(act_wire, Wire))

    def test_splitgate_w_bitlength(self):
        expected = []
        expected.append((0, [0, 0, 0]))
        expected.append((1, [0, 0, 1]))
        expected.append((2, [0, 1, 0]))
        expected.append((3, [0, 1, 1]))
        expected.append((4, [1, 0, 0]))
        expected.append((5, [1, 0, 1]))
        expected.append((6, [1, 1, 0]))
        expected.append((7, [1, 1, 1]))
        for i, exp_res in expected:
            wire = self.group.gen(i)
            act_res = bits.split(self.group, wire, bit_length=3)
            for exp_wire, act_wire in zip(exp_res, act_res):
                self.assertEqual(exp_wire, int(act_wire))
                self.assertTrue(isinstance(act_wire, Wire))

    def test_splitgate_n_mults(self):
        a = self.group.gen(7)
        bits.split(self.group, a, bit_length=5)
        self.assertEqual(5, Wire.n_mul)

    def test_verify_bit_gate_zero(self):
        a = self.group.gen(0)
        res = bits.verify_bit(self.group, a)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_bit_gate_one(self):
        a = self.group.gen(1)
        res = bits.verify_bit(self.group, a)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_bit_gate_non_bit(self):
        for a in range(2, len(self.group)):
            a = self.group.gen(a)
            res = bits.verify_bit(self.group, a)
            self.assertEqual(res, 0)
            self.assertTrue(isinstance(res, Wire))

    def test_and_gate_two_inputs_0_0(self):
        wire_one = self.group.gen(0)
        wire_two = self.group.gen(0)
        exp_res = 0
        exp_n_constraints = 1
        self._test_gate(bits.and_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_and_gate_two_inputs_0_1(self):
        wire_one = self.group.gen(0)
        wire_two = self.group.gen(1)
        exp_res = 0
        exp_n_constraints = 1
        self._test_gate(bits.and_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_and_gate_two_inputs_1_0(self):
        wire_one = self.group.gen(1)
        wire_two = self.group.gen(0)
        exp_res = 0
        exp_n_constraints = 1
        self._test_gate(bits.and_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_and_gate_two_inputs_1_1(self):
        wire_one = self.group.gen(1)
        wire_two = self.group.gen(1)
        exp_res = 1
        exp_n_constraints = 1
        self._test_gate(bits.and_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_and_gate_multiple_inputs_three_satisfied(self):
        wires = []
        for _ in range(3):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.and_gate_multiple_inputs, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_multiple_inputs_three_not_satisfied(self):
        wires = []
        for _ in range(2):
            wires.append(self.group.gen(1))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 2
        self._test_gate(bits.and_gate_multiple_inputs, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_two_inputs_satisfied(self):
        wires = []
        for _ in range(2):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 1
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_two_inputs_not_satisfied(self):
        wires = []
        for _ in range(1):
            wires.append(self.group.gen(1))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 1
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_three_inputs_satisfied(self):
        wires = []
        for _ in range(3):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_three_inputs_not_satisfied(self):
        wires = []
        for _ in range(2):
            wires.append(self.group.gen(1))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 2
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_five_inputs_satisfied(self):
        wires = []
        for _ in range(5):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_and_gate_five_inputs_not_satisfied(self):
        wires = []
        for _ in range(4):
            wires.append(self.group.gen(1))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 2
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_two_inputs_0_0(self):
        wire_one = self.group.gen(0)
        wire_two = self.group.gen(0)
        exp_res = 0
        exp_n_constraints = 1
        self._test_gate(bits.or_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_or_gate_two_inputs_0_1(self):
        wire_one = self.group.gen(0)
        wire_two = self.group.gen(1)
        exp_res = 1
        exp_n_constraints = 1
        self._test_gate(bits.or_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_or_gate_two_inputs_1_0(self):
        wire_one = self.group.gen(1)
        wire_two = self.group.gen(0)
        exp_res = 1
        exp_n_constraints = 1
        self._test_gate(bits.or_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_or_gate_two_inputs_1_1(self):
        wire_one = self.group.gen(1)
        wire_two = self.group.gen(1)
        exp_res = 1
        exp_n_constraints = 1
        self._test_gate(bits.or_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_or_gate_multiple_inputs_three_satisfied(self):
        wires = []
        for _ in range(3):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.or_gate_multiple_inputs, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_multiple_inputs_three_not_satisfied(self):
        wires = []
        for _ in range(2):
            wires.append(self.group.gen(0))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 2
        self._test_gate(bits.or_gate_multiple_inputs, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_two_inputs_satisfied(self):
        wires = []
        for _ in range(2):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 1
        self._test_gate(bits.or_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_two_inputs_not_satisfied(self):
        wires = []
        for _ in range(1):
            wires.append(self.group.gen(0))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 1
        self._test_gate(bits.or_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_three_inputs_satisfied(self):
        wires = []
        for _ in range(3):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.or_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_three_inputs_not_satisfied(self):
        wires = []
        for _ in range(2):
            wires.append(self.group.gen(0))
        wires.append(self.group.gen(0))
        exp_res = 0
        exp_n_constraints = 2
        self._test_gate(bits.and_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_five_inputs_satisfied(self):
        wires = []
        for _ in range(5):
            wires.append(self.group.gen(1))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.or_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_or_gate_five_inputs_satisfied_mix(self):
        wires = []
        for _ in range(4):
            wires.append(self.group.gen(1))
        wires.append(self.group.gen(0))
        exp_res = 1
        exp_n_constraints = 2
        self._test_gate(bits.or_gate, [self.group, wires], exp_res, exp_n_constraints)

    def test_xor_gate_two_inputs_0_0(self):
        wire_one = self.group.gen(0)
        wire_two = self.group.gen(0)
        exp_res = 0
        exp_n_constraints = 3
        self._test_gate(bits.xor_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_xor_gate_two_inputs_0_1(self):
        wire_one = self.group.gen(0)
        wire_two = self.group.gen(1)
        exp_res = 1
        exp_n_constraints = 3
        self._test_gate(bits.xor_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_xor_gate_two_inputs_1_0(self):
        wire_one = self.group.gen(1)
        wire_two = self.group.gen(0)
        exp_res = 1
        exp_n_constraints = 3
        self._test_gate(bits.xor_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def test_xor_gate_two_inputs_1_1(self):
        wire_one = self.group.gen(1)
        wire_two = self.group.gen(1)
        exp_res = 0
        exp_n_constraints = 3
        self._test_gate(bits.xor_gate_two_inputs, [self.group, wire_one, wire_two], exp_res, exp_n_constraints)

    def _test_gate(self, f_gate, inputs, exp_res, exp_n_constraints):
        Wire.n_mul = 0
        result = f_gate(*inputs)
        self.assertEqual(result, exp_res)
        self.assertTrue(isinstance(result, Wire))
        self.assertEqual(Wire.n_mul, exp_n_constraints)
