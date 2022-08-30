"""
Tests the xadd function used in the Montgomery ladder.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class XaddTest(unittest.TestCase):

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
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        d = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(9))

        a = ecgates.xadd(d, p, p)
        x_val = a.x / a.z
        self.assertEqual(1, a.x)
        self.assertEqual(4, a.z)
        self.assertEqual(10, x_val)

        self.assertTrue(isinstance(a.x, Wire))
        self.assertTrue(isinstance(a.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))

    def test_xadd_n_mults(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        d = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(9))

        _ = ecgates.xadd(d, p, p)
        self.assertEqual(6, Wire.n_mul)

    def test_xadd(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        d = ecgates.xdbl(p, self.A)
        a = ecgates.xadd(d, p, p)
        x_val = a.x / a.z
        self.assertEqual(1, a.x)
        self.assertEqual(4, a.z)
        self.assertEqual(10, x_val)

        self.assertTrue(isinstance(a.x, Wire))
        self.assertTrue(isinstance(a.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))
