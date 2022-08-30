"""
Tests exponentations.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class ExponentationTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        Wire.n_mul = 0
        self.modulus = 13
        self.g = WireGroup(self.modulus)
        self.A = self.g.gen(3, is_const=True)
        self.B = self.g.gen(1, is_const=True)
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_exponent_affine_point_4_8(self):
        """
        Start with point (4, 8).
        """
        p = ecgates.AffinePoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))

        exp = []
        exp.append((self.g.gen(2), (12, 1)))
        exp.append((self.g.gen(3), (10, 7)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_affine_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))

    def test_exponent_affine_point_10_6(self):
        """
        Start with point (10, 6).
        """
        p = ecgates.AffinePoint(self.g.gen(10), self.g.gen(6), self.g.gen(1))

        exp = []
        exp.append((self.g.gen(2), (12, 1)))
        exp.append((self.g.gen(3), (4, 5)))
        exp.append((self.g.gen(4), (0, 0)))
        exp.append((self.g.gen(5), (4, 8)))
        exp.append((self.g.gen(6), (12, 12)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_affine_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))

    def test_exponent_homogeneous_point_bits_4_8(self):
        """
        Start with point (4, 8, 1).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))

        exp = []
        exp.append(([self.g.gen(1), self.g.gen(0)], (3, 10, 10)))
        exp.append(([self.g.gen(1), self.g.gen(1)], (3, 6, 12)))

        for (exponent_bits, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point_bit_exponent(self.g, self.A, self.B, p, exponent_bits)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_point_bits_10_6(self):
        """
        Start with point (10, 6, 1).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(6), self.g.gen(1))

        exp = []
        exp.append(([self.g.gen(1), self.g.gen(0)], (4, 9, 9)))
        exp.append(([self.g.gen(1), self.g.gen(1)], (4, 5, 1)))

        for (exponent_bits, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point_bit_exponent(self.g, self.A, self.B, p, exponent_bits)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_bits_infty(self):
        """
        Checks exponentation of infty in homogeneous coordinates.
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))

        exp = []
        exp.append(([self.g.gen(1), self.g.gen(0)], (0, 1, 0)))
        exp.append(([self.g.gen(1), self.g.gen(1)], (0, 1, 0)))
        exp.append(([self.g.gen(1), self.g.gen(0), self.g.gen(0)], (0, 1, 0)))
        exp.append(([self.g.gen(1), self.g.gen(0), self.g.gen(1)], (0, 1, 0)))

        for (exponent_bits, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point_bit_exponent(self.g, self.A, self.B, p, exponent_bits)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_bits_zero_even(self):
        """
        Checks exponentation of the zero point with even exponent
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(0), self.g.gen(1))

        exp = []
        exp.append(([self.g.gen(1), self.g.gen(0)], (0, 1, 0)))
        exp.append(([self.g.gen(1), self.g.gen(0), self.g.gen(0)], (0, 1, 0)))
        exp.append(([self.g.gen(1), self.g.gen(0), self.g.gen(0), self.g.gen(0)], (0, 1, 0)))

        for (exponent_bits, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point_bit_exponent(self.g, self.A, self.B, p, exponent_bits)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_bits_zero_odd(self):
        """
        Checks exponentation of the zero point with odd exponent
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(0), self.g.gen(1))

        exp = []
        exp.append(([self.g.gen(1), self.g.gen(1)], (0, 0, 1)))
        exp.append(([self.g.gen(1), self.g.gen(0), self.g.gen(1)], (0, 0, 1)))
        exp.append(([self.g.gen(1), self.g.gen(1), self.g.gen(1)], (0, 0, 1)))

        for (exponent_bits, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point_bit_exponent(self.g, self.A, self.B, p, exponent_bits)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_point_4_8(self):
        """
        Start with point (4, 8, 1).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))

        exp = []
        exp.append((self.g.gen(2), (3, 10, 10)))
        exp.append((self.g.gen(3), (3, 6, 12)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_point_10_6(self):
        """
        Start with point (10, 6, 1).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(6), self.g.gen(1))

        exp = []
        exp.append((self.g.gen(2), (10, 3, 3)))
        exp.append((self.g.gen(3), (10, 6, 9)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_infty(self):
        """
        Checks exponentation of infty in homogeneous coordinates.
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))

        exp = []
        exp.append((self.g.gen(2), (0, 1, 0)))
        exp.append((self.g.gen(3), (0, 1, 0)))
        exp.append((self.g.gen(4), (0, 1, 0)))
        exp.append((self.g.gen(5), (0, 1, 0)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_zero_even(self):
        """
        Checks exponentation of the zero point with even exponent
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(0), self.g.gen(1))

        exp = []
        exp.append((self.g.gen(2), (0, 1, 0)))
        exp.append((self.g.gen(4), (0, 1, 0)))
        exp.append((self.g.gen(6), (0, 1, 0)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))

    def test_exponent_homogeneous_zero_odd(self):
        """
        Checks exponentation of the zero point with odd exponent
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(0), self.g.gen(1))

        exp = []
        exp.append((self.g.gen(3), (0, 0, 1)))
        exp.append((self.g.gen(5), (0, 0, 1)))
        exp.append((self.g.gen(7), (0, 0, 1)))

        for (exponent, exp_res) in exp:
            exp = ecgates.exponent_homogeneous_point(self.g, self.A, self.B, p, exponent)
            self.assertEqual(exp_res[0], exp.x)
            self.assertEqual(exp_res[1], exp.y)
            self.assertEqual(exp_res[2], exp.z)

            self.assertTrue(isinstance(exp.x, Wire))
            self.assertTrue(isinstance(exp.y, Wire))
            self.assertTrue(isinstance(exp.z, Wire))
