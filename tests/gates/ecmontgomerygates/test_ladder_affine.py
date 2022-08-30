"""
Tests the Montgomery ladder for affine coordinates..
"""

import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.ecsmontgomery as ecgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class LadderAffineTest(unittest.TestCase):

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
        p = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))
        res, _ = ecgates.ladder_affine([1], p, self.A)
        self.assertEqual(4, res.x)
        self.assertEqual(1, res.z)

        self.assertTrue(isinstance(res.x, Wire))
        self.assertTrue(isinstance(res.z, int))

    def test_ladder_k_2(self):
        p = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))
        res, _ = ecgates.ladder_affine([1, 0], p, self.A)
        self.assertEqual(12, res.x)
        self.assertEqual(1, res.z)

        self.assertTrue(isinstance(res.x, Wire))
        self.assertTrue(isinstance(res.z, int))

    def test_ladder_k_3(self):
        p = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))
        res, _ = ecgates.ladder_affine([1, 1], p, self.A)
        self.assertEqual(10, res.x)
        self.assertEqual(1, res.z)

        self.assertTrue(isinstance(res.x, Wire))
        self.assertTrue(isinstance(res.z, int))

    def test_ladder_comparison_addition_4_5(self):
        """
        Start with point (4, 5).
        """
        p = ecgates.AffinePoint(self.g.gen(4), None, self.g.gen(1))

        p_ress = []
        p_ress.append((12, 12))
        p_ress.append((10, 6))
        p_ress.append((0, 0))

        for k, p_res in zip(range(2, len(p_ress) + 2), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, _ = ecgates.ladder_affine(k_bin, p, self.A)
            self.assertEqual(res.x, p_res[0])
            self.assertTrue(isinstance(res.x, Wire))

    def test_ladder_comparison_addition_10_6(self):
        """
        Start with point (10, 6).
        """
        p = ecgates.AffinePoint(self.g.gen(10), None, self.g.gen(1))

        p_ress = []
        p_ress.append((12, 1))
        p_ress.append((4, 5))
        p_ress.append((0, 0))
        p_ress.append((4, 8))

        for k, p_res in zip(range(2, len(p_ress) + 2), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, _ = ecgates.ladder_affine(k_bin, p, self.A)
            self.assertEqual(res.x, p_res[0])
            self.assertTrue(isinstance(res.x, Wire))

    def test_ladder_comparison_addition_10_7(self):
        """
        Start with point (10, 7).
        """
        p = ecgates.AffinePoint(self.g.gen(10), None, self.g.gen(1))

        p_ress = []
        p_ress.append((12, 12))
        p_ress.append((4, 8))
        p_ress.append((0, 0))
        p_ress.append((4, 5))

        for k, p_res in zip(range(2, len(p_ress) + 2), p_ress):
            k_bin = [int(i) for i in "{0:b}".format(k)]
            res, _ = ecgates.ladder_affine(k_bin, p, self.A)
            self.assertEqual(res.x, p_res[0])
            self.assertTrue(isinstance(res.x, Wire))
