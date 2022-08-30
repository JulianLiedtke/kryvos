"""
This module contains the test cases for comparison operations on
wires.
"""
import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.comparison as comparison
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class ComparisonGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        Wire.n_mul = 0
        self.group = WireGroup(11)
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_eq_zero_false(self):
        """
        Tests a wire that is not zero to be zero.
        """
        input_wire = self.group.gen(2)
        res_wire = comparison.eq_zero(self.group, input_wire)
        self.assertEqual(0, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_eq_zero_true(self):
        """
        Tests a wire that is zero to be zero.
        """
        input_wire = self.group.gen(0)
        res_wire = comparison.eq_zero(self.group, input_wire)
        self.assertEqual(1, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_eq_true(self):
        """
        Test eq of two wires of equal value.
        """
        wire_a = self.group.gen(3)
        wire_b = self.group.gen(3)
        res_wire = comparison.eq(self.group, wire_a, wire_b)
        self.assertEqual(1, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_eq_false(self):
        """
        Test eq of two wires of different value.
        """
        wire_a = self.group.gen(3)
        wire_b = self.group.gen(2)
        res_wire = comparison.eq(self.group, wire_a, wire_b)
        self.assertEqual(0, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_eq_zero_multiple_single_true(self):
        wires = []
        wires.append(self.group.gen(0))
        res_wire = comparison.eq_zero_multiple(self.group, wires)
        self.assertEqual(1, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))
        self.assertEqual(2, Wire.n_mul)

    def test_eq_zero_multiple_single_false(self):
        wires = []
        wires.append(self.group.gen(2))
        res_wire = comparison.eq_zero_multiple(self.group, wires)
        self.assertEqual(0, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))
        self.assertEqual(2, Wire.n_mul)

    def test_eq_zero_multiple_three_true(self):
        wires = []
        wires.append(self.group.gen(3))
        wires.append(self.group.gen(6))
        wires.append(self.group.gen(2))
        res_wire = comparison.eq_zero_multiple(self.group, wires)
        self.assertEqual(1, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))
        self.assertEqual(2, Wire.n_mul)

    def test_eq_zero_multiple_three_false(self):
        wires = []
        wires.append(self.group.gen(3))
        wires.append(self.group.gen(6))
        wires.append(self.group.gen(1))
        res_wire = comparison.eq_zero_multiple(self.group, wires)
        self.assertEqual(0, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))
        self.assertEqual(2, Wire.n_mul)

    def test_eq_multiple_true(self):
        wires_a = []
        wires_a.append(self.group.gen(2))
        wires_a.append(self.group.gen(3))
        wires_a.append(self.group.gen(1))
        wires_b = []
        wires_b.append(self.group.gen(1))
        wires_b.append(self.group.gen(4))
        wires_b.append(self.group.gen(1))
        res_wire = comparison.eq_multiple(self.group, wires_a, wires_b)
        self.assertEqual(1, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))
        self.assertEqual(2, Wire.n_mul)

    def test_eq_multiple_false(self):
        wires_a = []
        wires_a.append(self.group.gen(2))
        wires_a.append(self.group.gen(3))
        wires_a.append(self.group.gen(1))
        wires_b = []
        wires_b.append(self.group.gen(1))
        wires_b.append(self.group.gen(4))
        wires_b.append(self.group.gen(0))
        res_wire = comparison.eq_multiple(self.group, wires_a, wires_b)
        self.assertEqual(0, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))
        self.assertEqual(2, Wire.n_mul)

    def test_gt_exception_even(self):
        """
        Group length with even bit size (11 has 4 bits).
        """
        a = self.group.gen(1)
        b = self.group.gen(0)
        self.assertRaises(ValueError, lambda: comparison.gt(self.group, a, b, 5))
        self.assertRaises(ValueError, lambda: comparison.gt(self.group, a, b, 4))
        self.assertRaises(ValueError, lambda: comparison.gt(self.group, a, b, 3))

    def test_gt_no_exception_even(self):
        """
        Group length with even bit size (11 has 4 bits).
        """
        a = self.group.gen(1)
        b = self.group.gen(0)
        _ = comparison.gt(self.group, a, b, 2)
        _ = comparison.gt(self.group, a, b, 1)

    def test_gt_exception_odd(self):
        """
        Group length with odd bit size (17 has 5 bits).
        """
        group_uneven = WireGroup(17)
        a = group_uneven.gen(1)
        b = group_uneven.gen(0)
        self.assertRaises(ValueError, lambda: comparison.gt(group_uneven, a, b, 6))
        self.assertRaises(ValueError, lambda: comparison.gt(group_uneven, a, b, 5))
        self.assertRaises(ValueError, lambda: comparison.gt(group_uneven, a, b, 4))
        self.assertRaises(ValueError, lambda: comparison.gt(group_uneven, a, b, 3))

    def test_gt_no_exception_odd(self):
        """
        Group length with odd bit size (17 has 5 bits).
        """
        group_uneven = WireGroup(17)
        a = group_uneven.gen(1)
        b = group_uneven.gen(0)
        _ = comparison.gt(group_uneven, a, b, 2)
        _ = comparison.gt(group_uneven, a, b, 1)

    def test_gt_truely_greater(self):
        """
        Test a >= b with a > b
        """
        for a in range(4):
            wire_a = self.group.gen(a)
            for b in range(0, a):
                wire_b = self.group.gen(b)
                res = comparison.gt(self.group, wire_a, wire_b, 2)
                self.assertEqual(1, int(res))
                self.assertTrue(isinstance(res, Wire))

    def test_gt_eq(self):
        """
        Test a >= b with a == b
        """
        for a in range(4):
            wire_a = self.group.gen(a)
            wire_b = self.group.gen(a)
            res = comparison.gt(self.group, wire_a, wire_b, 2)
            self.assertEqual(1, int(res))
            self.assertTrue(isinstance(res, Wire))

    def test_gt_less(self):
        """
        Test a >= b with a < b
        """
        for a in range(4):
            wire_a = self.group.gen(a)
            for b in range(a+1, 4):
                wire_b = self.group.gen(b)
                res = comparison.gt(self.group, wire_a, wire_b, 2)
                self.assertEqual(0, int(res))
                self.assertTrue(isinstance(res, Wire))

    def test_lt_truely_greater(self):
        """
        Test a <= b with a > b
        """
        for a in range(4):
            wire_a = self.group.gen(a)
            for b in range(0, a):
                wire_b = self.group.gen(b)
                res = comparison.lt(self.group, wire_a, wire_b, 2)
                self.assertEqual(0, int(res))
                self.assertTrue(isinstance(res, Wire))

    def test_lt_eq(self):
        """
        Test a <= b with a == b
        """
        for a in range(4):
            wire_a = self.group.gen(a)
            wire_b = self.group.gen(a)
            res = comparison.lt(self.group, wire_a, wire_b, 2)
            self.assertEqual(1, int(res))
            self.assertTrue(isinstance(res, Wire))

    def test_lt_less(self):
        """
        Test a <= b with a < b
        """
        for a in range(4):
            wire_a = self.group.gen(a)
            for b in range(a+1, 4):
                wire_b = self.group.gen(b)
                res = comparison.lt(self.group, wire_a, wire_b, 2)
                self.assertEqual(1, int(res))
                self.assertTrue(isinstance(res, Wire))
