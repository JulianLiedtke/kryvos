import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
from src.groups.residuegroup import ResidueGroup, Residue

log = logging.getLogger(__name__)


class ResidueGroupTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_convert_int(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        a_int = int(a)
        self.assertTrue(isinstance(a_int, int))
        self.assertEqual(3, a_int)

    def test_neg(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        b = -a
        self.assertTrue(isinstance(b, Residue))
        self.assertEqual(8, b)

    def test_equality_negative_ints(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        a_int = 3 - 11
        self.assertEqual(a, a_int)

    def test_add_no_overflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        b = group.gen(4)
        s = a + b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(7, s)

    def test_add_overflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(7)
        b = group.gen(8)
        s = a + b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(4, s)

    def test_radd_with_int(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        s = 1 + a
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(4, s)

    def test_sub_no_underflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(9)
        b = group.gen(4)
        s = a - b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(5, s)

    def test_sub_underflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(4)
        b = group.gen(7)
        s = a - b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(8, s)

    def test_sub_with_int(self):
        group = ResidueGroup.create(11)
        a = group.gen(4)
        b = group.gen(7)
        s = 4 - b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(8, s)
        s = a - 7
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(8, s)

    def test_negation(self):
        group = ResidueGroup.create(11)
        a = group.gen(7)
        s = -a
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(4, s)

    def test_mul_no_overflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(2)
        b = group.gen(3)
        s = a * b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(6, s)

    def test_mul_overflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        b = group.gen(4)
        s = a * b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(1, s)

    def test_rmul_with_int(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        s = 2 * a
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(6, s)

    def test_pow_no_overflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(2)
        s = a ** 2
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(4, s)

    def test_pow_overflow(self):
        group = ResidueGroup.create(11)
        a = group.gen(3)
        s = a ** 3
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(5, s)

    def test_div(self):
        group = ResidueGroup.create(11)
        a = group.gen(2)
        b = group.gen(3)
        s = a / b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(8, s)

    def test_div_with_int(self):
        group = ResidueGroup.create(11)
        a = group.gen(2)
        b = group.gen(3)
        s = a / 3
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(8, s)
        s = 2 / b
        self.assertTrue(isinstance(s, Residue))
        self.assertEqual(8, s)

    def test_invert(self):
        modulus = 11
        group = ResidueGroup.create(modulus)
        for x in range(1, modulus):
            a = group.gen(x)
            a_inv = a.invert()
            self.assertTrue(isinstance(a_inv, Residue))
            res_mul = a * a_inv
            self.assertEqual(1, res_mul)
