"""
Tests the xadd function for affine coordinates.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class XaddAffineTest(unittest.TestCase):

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

    def test_xadd_gate(self):
        p = ecgates.AffinePoint(self.g.gen(12), None, self.g.gen(1))
        q = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))
        pqm = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))

        a = ecgates.xadd_affine(p, q, pqm)
        self.assertEqual(10, a.x)
        self.assertEqual(1, a.z)

        self.assertTrue(isinstance(a.x, Wire))
        self.assertTrue(isinstance(a.z, int))

    def test_xadd_n_mults(self):
        p = ecgates.AffinePoint(self.g.gen(12), None, self.g.gen(1))
        q = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))
        pqm = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))

        _ = ecgates.xadd_affine(p, q, pqm)
        self.assertEqual(6, Wire.n_mul)
