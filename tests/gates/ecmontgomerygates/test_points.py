"""
Tests points and simple operations on points.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class PointsTest(unittest.TestCase):

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

    def test_homogeneous_point_coordinates(self):
        p = ecgates.HomogeneousPoint(1, 2, 3)
        self.assertEqual(1, p.x)
        self.assertEqual(2, p.y)
        self.assertEqual(3, p.z)
        p.x = 4
        p.y = 5
        p.z = 6
        self.assertEqual(4, p.x)
        self.assertEqual(5, p.y)
        self.assertEqual(6, p.z)

    def test_affine_point_coordinates(self):
        p = ecgates.AffinePoint(1, 2, 0)
        self.assertEqual(1, p.x)
        self.assertEqual(2, p.y)
        self.assertEqual(0, p.z)
        p.x = 4
        p.y = 5
        p.z = 1
        self.assertEqual(4, p.x)
        self.assertEqual(5, p.y)
        self.assertEqual(1, p.z)

    def test_convert_homogeneous_to_affine(self):
        """
        Tests the conversion from homogeneous to affine coordinates.
        """
        x = self.g.gen(5)
        y = self.g.gen(8)
        z = self.g.gen(7)
        p = ecgates.HomogeneousPoint(x, y, z)

        x_homogeneous = x * z
        y_homogeneous = y * z

        affine_p = ecgates.convert_homogeneous_to_affine_coordinates(self.g, ecgates.HomogeneousPoint(x_homogeneous, y_homogeneous, z))

        self.assertEqual(x, affine_p.x)
        self.assertEqual(y, affine_p.y)
        self.assertEqual(1, affine_p.z)

        self.assertTrue(isinstance(affine_p.x, Wire))
        self.assertTrue(isinstance(affine_p.y, Wire))
        self.assertTrue(isinstance(affine_p.z, Wire))

    def test_convert_homogeneous_to_affine_infty(self):
        """
        Converts the point at infinity to affine coordinates.
        """
        p = ecgates.HomogeneousPoint(self.g.gen(0), self.g.gen(1), self.g.gen(0))

        affine_p = ecgates.convert_homogeneous_to_affine_coordinates(self.g, p)

        self.assertEqual(0, affine_p.x)
        self.assertEqual(1, affine_p.y)
        self.assertEqual(0, affine_p.z)

        self.assertTrue(isinstance(affine_p.x, Wire))
        self.assertTrue(isinstance(affine_p.y, Wire))
        self.assertTrue(isinstance(affine_p.z, Wire))
