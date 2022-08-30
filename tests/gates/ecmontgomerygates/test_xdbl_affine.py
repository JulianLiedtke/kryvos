"""
Tests the xdbl function for affine coordinates.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class XdblAffineTest(unittest.TestCase):

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

    def test_xdbl_gate(self):
        p = ecgates.AffinePoint(self.g.gen(4), None, 1)

        d = ecgates.xdbl_affine(p, self.A)
        self.assertEqual(12, d.x)
        self.assertEqual(1, d.z)

        self.assertTrue(isinstance(d.x, Wire))
        self.assertTrue(isinstance(d.z, int))

    def test_xdbl_n_mults(self):
        p = ecgates.AffinePoint(self.g.gen(4), None, 1)

        _ = ecgates.xdbl_affine(p, self.A)
        self.assertEqual(6, Wire.n_mul)

    def test_xdbl_simple(self):
        p = ecgates.AffinePoint(self.g.gen(1), None, 1)
        d = ecgates.xdbl_affine(p, self.A)
        self.assertEqual(0, d.x)
        self.assertEqual(1, d.z)

        self.assertTrue(isinstance(d.x, Wire))
        self.assertTrue(isinstance(d.z, int))

    def test_xdbl_advanced(self):
        p = ecgates.AffinePoint(self.g.gen(4), None, 1)
        d = ecgates.xdbl_affine(p, self.A)
        self.assertEqual(12, d.x)
        self.assertEqual(1, d.z)

        self.assertTrue(isinstance(d.x, Wire))
        self.assertTrue(isinstance(d.z, int))
