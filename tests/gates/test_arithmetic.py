"""
This module contains test cases for the arithmetic operations based on wires.
"""
import logging
import time
import unittest
from time import time
from typing import List, Tuple

import src.gates.arithmetic as arithmetic
from src.groups.wiregroup import Wire, WireGroup
from src.utils.logging_utils import setup_logging

log = logging.getLogger(__name__)


class ArithmeticGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        Wire.n_mul = 0
        self.group = WireGroup(11)
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_division_unsafe_no_exception(self):
        a = self.group.gen(1)
        b = self.group.gen(2)
        res = arithmetic.division(a, b)
        self.assertEqual(6, res)
        self.assertTrue(isinstance(res, Wire))

    def test_division_unsafe_exception(self):
        a = self.group.gen(1)
        b = self.group.gen(0)
        self.assertRaises(ValueError, lambda: arithmetic.division(a, b))

    def test_division_safe_not_zero(self):
        a = self.group.gen(1)
        b = self.group.gen(2)
        res = arithmetic.division_safe(self.group, a, b)
        self.assertEqual(6, res)
        self.assertTrue(isinstance(res, Wire))

    def test_division_safe_zero(self):
        a = self.group.gen(1)
        b = self.group.gen(0)
        arithmetic.division_safe(self.group, a, b)

    def test_division_safe_multiple(self):
        wires = [self.group.gen(1), self.group.gen(2), self.group.gen(3)]
        b = self.group.gen(2)
        ress = arithmetic.division_safe_multiple(self.group, wires, b)
        self.assertEqual(len(ress), 3)
        self.assertEqual(6, ress[0])
        self.assertTrue(isinstance(ress[0], Wire))
        self.assertEqual(1, ress[1])
        self.assertTrue(isinstance(ress[1], Wire))
        self.assertEqual(7, ress[2])
        self.assertTrue(isinstance(ress[2], Wire))

    def test_r1cs_constraint_single_output_1_1(self) -> None:
        """
        Test whether 1*1=1.
        """
        values_a = []
        values_a.append((1, self.group.gen(1)))
        values_b = []
        values_b.append((1, self.group.gen(1)))
        exp_res = 1
        self._test_r1cs_constraint_single_output(values_a, values_b, exp_res)

    def test_r1cs_constraint_single_output_factors(self) -> None:
        """
        Test whether (2*3+3*4)*(3*1+2*6) = 6.
        """
        values_a = []
        values_a.append((2, self.group.gen(3)))
        values_a.append((3, self.group.gen(4)))
        values_b = []
        values_b.append((3, self.group.gen(1)))
        values_b.append((2, self.group.gen(6)))
        exp_res = 6
        self._test_r1cs_constraint_single_output(values_a, values_b, exp_res)

    def _test_r1cs_constraint_single_output(self, values_a: List[Tuple[int, Wire]], values_b: List[Tuple[int, Wire]], exp_res_val: int) -> None:
        """
        Tests the R1CS gate for given inputs.

        The function tests the output of the gate (value and type),
        and that the correct number of r1cs constraints was used to
        compute the result.

        :param values_a: Wire set a (with factors)
        :type values_a: List[Tuple[int, Wire]]
        :param values_b: Wire set b (with factors)
        :type values_b: List[Tuple[int, Wire]]
        :param exp_res_val: Expected output of the gate.
        :type exp_res_val: int
        """
        Wire.n_mul = 0
        act_res = arithmetic.r1cs_constraint_single_output(self.group, values_a, values_b)
        self.assertEqual(act_res.value, exp_res_val)
        self.assertTrue(isinstance(act_res, Wire))
        self.assertEqual(Wire.n_mul, 1)
