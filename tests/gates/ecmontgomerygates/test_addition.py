"""
Tests addition of points.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class AdditionTest(unittest.TestCase):

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

    def test_addition_affine_basic(self):
        """
        Checks the case :math:`P \\notin \{Q, \ominus Q\}`. 
        """
        exp = []
        exp.append([(4, 5), (12, 12), (10, 6, 1)])
        exp.append([(12, 12), (0, 0), (12, 1, 1)])
        exp.append([(12, 12), (10, 7), (4, 8, 1)])

        for (xp, yp), (xq, yq), (xpq, ypq, zpq) in exp:
            a_pq = ecgates.add_affine_points(self.g, self.A, self.B, ecgates.AffinePoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(1)), ecgates.AffinePoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(1)))
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_addition_affine_pp(self):
        """
        Checks the case of the :math:`P = Q`.
        """
        exp = []
        exp.append([(10, 6), (10, 6), (12, 1, 1)])
        exp.append([(12, 1), (12, 1), (0, 0, 1)])

        for (xp, yp), (xq, yq), (xpq, ypq, zpq) in exp:
            a_pq = ecgates.add_affine_points(self.g, self.A, self.B, ecgates.AffinePoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(1)), ecgates.AffinePoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(1)))
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_addition_affine_pminusq(self):
        """
        Checks the case of the :math:`P = \ominus Q`.
        """
        exp = []
        exp.append([(10, 6), (10, 7), (0, 1, 0)])
        exp.append([(4, 8), (4, 5), (0, 1, 0)])

        for (xp, yp), (xq, yq), (xpq, ypq, zpq) in exp:
            a_pq = ecgates.add_affine_points(self.g, self.A, self.B, ecgates.AffinePoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(1)), ecgates.AffinePoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(1)))
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_addition_affine_zero_plus_zero(self):
        """
        Tests the correctness of the addition based on the x-coordinates of two
        points.

        This test method checks the case of the :math:`P = \ominus Q`.
        """
        exp = []
        exp.append([(0, 0), (0, 0), (0, 1, 0)])

        for (xp, yp), (xq, yq), (xpq, ypq, zpq) in exp:
            a_pq = ecgates.add_affine_points(self.g, self.A, self.B, ecgates.AffinePoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(1)), ecgates.AffinePoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(1)))
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_add_homogeneous_points_standard(self):
        """
        Tests standard cases, no zero point and no point at infinity.
        """
        exp = []
        exp.append([(12, 12, 1), (10, 7, 1), (4, 8, 1)])
        for z in range(2, 13):
            exp.append([(z*12, z*12, z), (z*10, z*7, z), (4, 8, 1)])

        for (xp, yp, zp), (xq, yq, zq), (xpq, ypq, zpq) in exp:
            p = ecgates.HomogeneousPoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(zp))
            q = ecgates.HomogeneousPoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(zq))
            a_pq = ecgates.add_homogeneous_points(self.g, self.A, self.B, p, q)
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_add_homogeneous_points_pp(self):
        """
        Tests the addition of two identical points.
        """
        exp = []
        exp.append([(10, 6, 1), (10, 6, 1), (12, 1, 1)])
        for z in range(2, 13):
            exp.append([(z*12, z*12, z), (z*10, z*7, z), (4, 8, 1)])

        for (xp, yp, zp), (xq, yq, zq), (xpq, ypq, zpq) in exp:
            p = ecgates.HomogeneousPoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(zp))
            q = ecgates.HomogeneousPoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(zq))
            a_pq = ecgates.add_homogeneous_points(self.g, self.A, self.B, p, q)
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_add_homogeneous_points_zero(self):
        """
        Tests addition with the zero point.
        """
        exp = []
        exp.append([(4, 8, 1), (0, 0, 1), (10, 6, 1)])
        for z in range(2, 13):
            exp.append([(z*4, z*8, z), (z*0, z*0, z), (10, 6, 1)])
        exp.append([(0, 0, 1), (0, 0, 1), (0, 1, 0)])
        for z in range(2, 13):
            exp.append([(z*0, z*0, z), (z*0, z*0, z), (0, 1, 0)])

        for (xp, yp, zp), (xq, yq, zq), (xpq, ypq, zpq) in exp:
            a_pq = ecgates.add_homogeneous_points(self.g, self.A, self.B, ecgates.HomogeneousPoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(zp)), ecgates.HomogeneousPoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(zq)))
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_homogeneous_points_infty_first_param(self):
        """
        Tests infty + P.
        """
        exp = []
        exp.append([(0, 1, 0), (4, 8, 1), (4, 8, 1)])

        for (xp, yp, zp), (xq, yq, zq), (xpq, ypq, zpq) in exp:
            a_pq = ecgates.add_homogeneous_points(self.g, self.A, self.B, ecgates.HomogeneousPoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(zp)), ecgates.HomogeneousPoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(zq)))
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))

    def test_homogeneous_points_infty_second_param(self):
        """
        Tests P + infty.
        """
        exp = []
        exp.append([(4, 8, 1), (0, 1, 0), (4, 8, 1)])

        for (xp, yp, zp), (xq, yq, zq), (xpq, ypq, zpq) in exp:
            p1 = ecgates.HomogeneousPoint(self.g.gen(xp), self.g.gen(yp), self.g.gen(zp))
            p2 = ecgates.HomogeneousPoint(self.g.gen(xq), self.g.gen(yq), self.g.gen(zq))
            a_pq = ecgates.add_homogeneous_points(self.g, self.A, self.B, p1, p2)
            self.assertEqual(a_pq.x, xpq)
            self.assertEqual(a_pq.y, ypq)
            self.assertEqual(a_pq.z, zpq)

            self.assertTrue(isinstance(a_pq.x, Wire))
            self.assertTrue(isinstance(a_pq.y, Wire))
            self.assertTrue(isinstance(a_pq.z, Wire))
