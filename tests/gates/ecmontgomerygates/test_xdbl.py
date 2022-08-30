"""
Tests the xdbl function used in the Montgomery ladder.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class XdblTest(unittest.TestCase):

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
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))

        d = ecgates.xdbl(p, self.A)
        x_val = d.x / d.z
        self.assertEqual(4, d.x)
        self.assertEqual(9, d.z)
        self.assertEqual(12, x_val)

        self.assertTrue(isinstance(d.x, Wire))
        self.assertTrue(isinstance(d.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))

    def test_xdbl_n_mults(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))

        _ = ecgates.xdbl(p, self.A)
        self.assertEqual(5, Wire.n_mul)

    def test_xdbl_simple(self):
        p = ecgates.HomogeneousPoint(self.g.gen(1), None, self.g.gen(1))
        d = ecgates.xdbl(p, self.A)
        self.assertEqual(0, d.x)
        self.assertEqual(7, d.z)

        self.assertTrue(isinstance(d.x, Wire))
        self.assertTrue(isinstance(d.z, Wire))

    def test_xdbl_advanced(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        d = ecgates.xdbl(p, self.A)
        x_val = d.x / d.z
        self.assertEqual(4, d.x)
        self.assertEqual(9, d.z)
        self.assertEqual(12, x_val)

        self.assertTrue(isinstance(d.x, Wire))
        self.assertTrue(isinstance(d.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))
