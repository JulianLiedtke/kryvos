"""
Tests the y-recovery.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class YRecoveryTest(unittest.TestCase):

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

    def test_y_recovery(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), self.g.gen(5), self.g.gen(1))
        p_ress = []
        p_ress.append((12, 12))
        p_ress.append((10, 6))
        p_ress.append((0, 0))
        p_ress.append((10, 7))
        p_ress.append((12, 1))
        p_ress.append((4, 8))
        p_ress.append("inf")
        p_ress.append((4, 5))
        p_ress.append((12, 12))
        p_ress.append((10, 6))

        for k, p_res in zip(range(2, 12), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, res2 = ecgates.ladder(k_bin, p, self.A)
            recovery_res = ecgates.y_recovery(self.g, self.A, self.B, p, res, res2)
            if res.z == 0:
                self.assertTrue(p_res == "inf")
            else:
                x_val = recovery_res.x / recovery_res.z
                self.assertEqual(x_val, p_res[0])
                self.assertTrue(isinstance(x_val, Wire))
                y_val = recovery_res.y / recovery_res.z
                self.assertEqual(y_val, p_res[1])
                self.assertTrue(isinstance(y_val, Wire))

    def test_y_recovery_p_minus_p(self):
        """
        Checks revovery in case Q = Minus P where the z-coordinates are
        different.
        """
        p = ecgates.HomogeneousPoint(self.g.gen(1), self.g.gen(0), self.g.gen(1))
        q = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(3))
        pq = ecgates.HomogeneousPoint(self.g.gen(9), None, self.g.gen(0))

        res = ecgates.y_recovery(self.g, self.A, self.B, p, q, pq)

        self.assertEqual(0, res.x)
        self.assertEqual(4, res.y)
        self.assertEqual(0, res.z)
