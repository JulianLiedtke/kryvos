"""
Tests the Montgomery ladder.
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class LadderTest(unittest.TestCase):

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

    def test_ladder_k_1(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        res, _ = ecgates.ladder([1], p, self.A)
        x_val = res.x / res.z
        self.assertEqual(4, res.x)
        self.assertEqual(1, res.z)
        self.assertEqual(4, x_val)

        self.assertTrue(isinstance(res.x, Wire))
        self.assertTrue(isinstance(res.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))

    def test_ladder_k_2(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        res, _ = ecgates.ladder([1, 0], p, self.A)
        x_val = res.x / res.z
        self.assertEqual(4, res.x)
        self.assertEqual(9, res.z)
        self.assertEqual(12, x_val)

        self.assertTrue(isinstance(res.x, Wire))
        self.assertTrue(isinstance(res.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))

    def test_ladder_k_3(self):
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        res, _ = ecgates.ladder([1, 1], p, self.A)
        x_val = res.x / res.z
        self.assertEqual(1, res.x)
        self.assertEqual(4, res.z)
        self.assertEqual(10, x_val)

        self.assertTrue(isinstance(res.x, Wire))
        self.assertTrue(isinstance(res.z, Wire))
        self.assertTrue(isinstance(x_val, Wire))

    def test_ladder_comparison_addition_4_5(self):
        """
        Start with point (4, 5).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(4), None, self.g.gen(1))
        x = p.x / p.z
        y = 5

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

        for k, p_res in zip(range(2, len(p_ress) + 2), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, _ = ecgates.ladder(k_bin, p, self.A)
            if res.z == 0:
                self.assertTrue(p_res == "inf")
            else:
                x_val = res.x / res.z
                self.assertEqual(x_val, p_res[0])
                self.assertTrue(isinstance(res.x, Wire))

    def test_ladder_comparison_addition_10_6(self):
        """
        Start with point (10, 6).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(10), None, self.g.gen(1))
        x = p.x / p.z
        y = 6

        p_ress = []
        p_ress.append((12, 1))
        p_ress.append((4, 5))
        p_ress.append((0, 0))
        p_ress.append((4, 8))
        p_ress.append((12, 12))
        p_ress.append((10, 7))
        p_ress.append("inf")

        for k, p_res in zip(range(2, len(p_ress) + 2), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, _ = ecgates.ladder(k_bin, p, self.A)
            if res.z == 0:
                self.assertTrue(p_res == "inf")
            else:
                x_val = res.x / res.z
                self.assertEqual(x_val, p_res[0])
                self.assertTrue(isinstance(x_val, Wire))

    def test_ladder_comparison_addition_10_7(self):
        """
        Start with point (10, 7).
        """
        p = ecgates.HomogeneousPoint(self.g.gen(10), None, self.g.gen(1))
        x = p.x / p.z
        y = 7

        p_ress = []
        p_ress.append((12, 12))
        p_ress.append((4, 8))
        p_ress.append((0, 0))
        p_ress.append((4, 5))
        p_ress.append((12, 1))
        p_ress.append((10, 6))
        p_ress.append("inf")

        for k, p_res in zip(range(2, len(p_ress) + 2), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, _ = ecgates.ladder(k_bin, p, self.A)
            if res.z == 0:
                self.assertTrue(p_res == "inf")
            else:
                x_val = res.x / res.z
                self.assertEqual(x_val, p_res[0])
                self.assertTrue(isinstance(x_val, Wire))
