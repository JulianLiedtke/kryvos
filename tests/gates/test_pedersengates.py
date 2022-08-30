"""
This module contains test cases for the Pedersen operations based on wires.
"""

import logging
import time
import unittest
from time import time

import src.gates.ecsmontgomery as ecgates
import src.gates.pedersengates as pedersen
from src.groups.wiregroup import Wire, WireGroup
from src.utils.logging_utils import setup_logging

log = logging.getLogger(__name__)


class PedersenGatesTest(unittest.TestCase):

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

    def test_pedersen_commitment_over_montgomery_curve_bits(self):
        """
        Tests Pedersen commitments of Montgomery curves.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(6), self.g.gen(1))
        m = self.g.gen(3)
        r = self.g.gen(6)
        r = [self.g.gen(1), self.g.gen(1), self.g.gen(0)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(4, com.x)
        self.assertEqual(8, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_bits_m_max_bits(self):
        """
        Tests Pedersen commitments of Montgomery curves with max bits of m.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(6), self.g.gen(1))
        m = self.g.gen(3)
        r = [self.g.gen(1), self.g.gen(1), self.g.gen(0)]

        for i in range(4, 6):
            com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r, n_max_bits_m=i)

            self.assertEqual(4, com.x)
            self.assertEqual(8, com.y)
            self.assertEqual(1, com.z)

            self.assertTrue(isinstance(com.x, Wire))
            self.assertTrue(isinstance(com.y, Wire))
            self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_h_infty_bits(self):
        """
        h is infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        m = self.g.gen(7)
        r = [self.g.gen(1), self.g.gen(0), self.g.gen(1)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(10, com.x)
        self.assertEqual(6, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_h_infty_2_bits(self):
        """
        Another test case where h is infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        m = self.g.gen(9)
        r = [self.g.gen(1), self.g.gen(0), self.g.gen(0), self.g.gen(0)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(12, com.x)
        self.assertEqual(11, com.y)
        self.assertEqual(9, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_g_infty_bits(self):
        """
        g is infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        h = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        m = self.g.gen(5)
        r = [self.g.gen(1), self.g.gen(1), self.g.gen(1)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(10, com.x)
        self.assertEqual(6,com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_both_infty_bits(self):
        """
        g and h are infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        m = self.g.gen(5)
        r = self.g.gen(7)
        r = [self.g.gen(1), self.g.gen(1), self.g.gen(1)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(0, com.x)
        self.assertEqual(1, com.y)
        self.assertEqual(0, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_h_zero_bits(self):
        """
        h is the zero point.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(12), self.g.gen(1), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(0), self.g.gen(1))
        m = self.g.gen(5)
        r = [self.g.gen(1), self.g.gen(1)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(12, com.x)
        self.assertEqual(12, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_example_1_bits(self):
        """
        Example values.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        m = self.g.gen(9)
        r = [self.g.gen(1), self.g.gen(0), self.g.gen(0), self.g.gen(0)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(12, com.x)
        self.assertEqual(11, com.y)
        self.assertEqual(9, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_example_2_bits(self):
        """
        Example values.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        m = self.g.gen(9)
        r = [self.g.gen(1), self.g.gen(1), self.g.gen(0)]

        com = pedersen.pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(4, com.x)
        self.assertEqual(8, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve(self):
        """
        Tests Pedersen commitments of Montgomery curves.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(6), self.g.gen(1))
        m = self.g.gen(3)
        r = self.g.gen(6)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(4, com.x)
        self.assertEqual(8, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_h_infty(self):
        """
        h is infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        m = self.g.gen(7)
        r = self.g.gen(5)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(10, com.x)
        self.assertEqual(6, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_h_infty_2(self):
        """
        Another test case where h is infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        m = self.g.gen(9)
        r = self.g.gen(8)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(12, com.x)
        self.assertEqual(11, com.y)
        self.assertEqual(9, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_g_infty(self):
        """
        g is infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        h = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        m = self.g.gen(5)
        r = self.g.gen(7)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(10, com.x)
        self.assertEqual(6,com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_both_infty(self):
        """
        g and h are infty.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))
        m = self.g.gen(5)
        r = self.g.gen(7)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(0, com.x)
        self.assertEqual(1, com.y)
        self.assertEqual(0, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_h_zero(self):
        """
        h is the zero point.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(12), self.g.gen(1), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(0), self.g.gen(1))
        m = self.g.gen(5)
        r = self.g.gen(3)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(12, com.x)
        self.assertEqual(12, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_example_1(self):
        """
        Example values.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        m = self.g.gen(9)
        r = self.g.gen(8)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(12, com.x)
        self.assertEqual(11, com.y)
        self.assertEqual(9, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_pedersen_commitment_over_montgomery_curve_example_2(self):
        """
        Example values.
        """
        g = ecgates.HomogeneousPoint(self.g.gen(10), self.g.gen(7), self.g.gen(1))
        h = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(8), self.g.gen(1))
        m = self.g.gen(9)
        r = self.g.gen(6)

        com = pedersen.pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, g, h, m, r)

        self.assertEqual(4, com.x)
        self.assertEqual(8, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_vector_pedersen_commitment_over_montgomery_curve_bits(self):
        """
        Tests vector Pedersen commitments of Montgomery curves.
        """
        g_one = ecgates.HomogeneousPoint(*self.g.gen_list([4, 5, 1]))
        g_two = ecgates.HomogeneousPoint(*self.g.gen_list([10, 7, 1]))
        g_three = ecgates.HomogeneousPoint(*self.g.gen_list([12, 12, 1]))
        gs = [g_one, g_two, g_three]
        h = ecgates.HomogeneousPoint(*self.g.gen_list([10, 6, 1]))
        m_one = self.g.gen(3)
        m_two = self.g.gen(2)
        m_three = self.g.gen(4)
        ms = [m_one, m_two, m_three]
        r_bits = self.g.gen_list([1, 0])

        com = pedersen.vector_pedersen_commitment_over_montgomery_curve_bit_randomness(self.g, self.A, self.B, gs, h, ms, r_bits)

        self.assertEqual(10, com.x)
        self.assertEqual(6, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))

    def test_vectorpedersen_commitment_over_montgomery_curve(self):
        """
        Tests vector Pedersen commitments of Montgomery curves.
        """
        g_one = ecgates.HomogeneousPoint(*self.g.gen_list([4, 5, 1]))
        g_two = ecgates.HomogeneousPoint(*self.g.gen_list([10, 7, 1]))
        g_three = ecgates.HomogeneousPoint(*self.g.gen_list([12, 12, 1]))
        gs = [g_one, g_two, g_three]
        h = ecgates.HomogeneousPoint(*self.g.gen_list([10, 6, 1]))
        m_one = self.g.gen(3)
        m_two = self.g.gen(2)
        m_three = self.g.gen(4)
        ms = [m_one, m_two, m_three]
        r = self.g.gen(2)

        com = pedersen.vector_pedersen_commitment_over_montgomery_curve(self.g, self.A, self.B, gs, h, ms, r)

        self.assertEqual(10, com.x)
        self.assertEqual(6, com.y)
        self.assertEqual(1, com.z)

        self.assertTrue(isinstance(com.x, Wire))
        self.assertTrue(isinstance(com.y, Wire))
        self.assertTrue(isinstance(com.z, Wire))
