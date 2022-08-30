import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class WireGroupTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_bitlength(self):
        group = WireGroup(11)
        self.assertTrue(4, group.bit_length)

    def test_convert_int(self):
        group = WireGroup(11)
        a = group.gen(3)
        a_int = int(a)
        self.assertTrue(isinstance(a_int, int))
        self.assertEqual(3, a_int)

    def test_neg(self):
        group = WireGroup(11)
        a = group.gen(3)
        b = -a
        self.assertTrue(isinstance(b, Wire))
        self.assertEqual(8, b)

    def test_add_no_overflow(self):
        group = WireGroup(11)
        a = group.gen(3)
        b = group.gen(4)
        s = a + b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(7, s)

    def test_add_overflow(self):
        group = WireGroup(11)
        a = group.gen(7)
        b = group.gen(8)
        s = a + b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(4, s)

    def test_radd_with_int(self):
        group = WireGroup(11)
        a = group.gen(3)
        s = 1 + a
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(4, s)

    def test_sub_no_underflow(self):
        group = WireGroup(11)
        a = group.gen(9)
        b = group.gen(4)
        s = a - b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(5, s)

    def test_sub_underflow(self):
        group = WireGroup(11)
        a = group.gen(4)
        b = group.gen(7)
        s = a - b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(8, s)

    def test_sub_with_int(self):
        group = WireGroup(11)
        a = group.gen(4)
        b = group.gen(7)
        s = 4 - b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(8, s)
        s = a - 7
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(8, s)

    def test_mul_no_overflow(self):
        group = WireGroup(11)
        a = group.gen(2)
        b = group.gen(3)
        s = a * b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(6, s)

    def test_mul_overflow(self):
        group = WireGroup(11)
        a = group.gen(3)
        b = group.gen(4)
        s = a * b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(1, s)

    def test_rmul_with_int(self):
        group = WireGroup(11)
        a = group.gen(3)
        s = 2 * a
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(6, s)

    def test_pow_no_overflow(self):
        group = WireGroup(11)
        a = group.gen(2)
        s = a ** 2
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(4, s)

    def test_pow_overflow(self):
        group = WireGroup(11)
        a = group.gen(3)
        s = a ** 3
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(5, s)

    def test_div(self):
        group = WireGroup(11)
        a = group.gen(2)
        b = group.gen(3)
        s = a / b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(8, s)

    def test_div_with_int(self):
        group = WireGroup(11)
        a = group.gen(2)
        b = group.gen(3)
        s = a / 3
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(8, s)
        s = 2 / b
        self.assertTrue(isinstance(s, Wire))
        self.assertEqual(8, s)

    def test_invert(self):
        modulus = 11
        group = WireGroup(modulus)
        for x in range(1, modulus):
            a = group.gen(x)
            a_inv = a.invert()
            self.assertTrue(isinstance(a_inv, Wire))
            res_mul = a * a_inv
            self.assertEqual(1, res_mul)

    def test_isconst_neg_no_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = -a
        self.assertFalse(b.is_const)

    def test_isconst_neg_is_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = -a
        self.assertTrue(b.is_const)

    def test_isconst_add_no_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=False)
        c = a + b
        self.assertFalse(c.is_const)

    def test_isconst_add_first_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=True)
        c = a + b
        self.assertFalse(c.is_const)

    def test_isconst_add_second_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=False)
        c = a + b
        self.assertFalse(c.is_const)

    def test_isconst_add_all_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=True)
        c = a + b
        self.assertTrue(c.is_const)

    def test_isconst_add_no_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = 3
        c = a + b
        self.assertFalse(c.is_const)

    def test_isconst_add_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = 3
        c = a + b
        self.assertTrue(c.is_const)

    def test_isconst_sub_no_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=False)
        c = a - b
        self.assertFalse(c.is_const)

    def test_isconst_sub_first_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=True)
        c = a - b
        self.assertFalse(c.is_const)

    def test_isconst_sub_second_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=False)
        c = a - b
        self.assertFalse(c.is_const)

    def test_isconst_sub_all_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=True)
        c = a - b
        self.assertTrue(c.is_const)

    def test_isconst_sub_no_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = 3
        c = a - b
        self.assertFalse(c.is_const)

    def test_isconst_rsub_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = 3
        c = b - a
        self.assertTrue(c.is_const)

    def test_isconst_sub_no_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = 3
        c = a - b
        self.assertFalse(c.is_const)

    def test_isconst_rsub_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = 3
        c = b - a
        self.assertTrue(c.is_const)

    def test_isconst_mul_no_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=False)
        c = a * b
        self.assertFalse(c.is_const)

    def test_isconst_mul_first_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=True)
        c = a * b
        self.assertFalse(c.is_const)

    def test_isconst_mul_second_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=False)
        c = a * b
        self.assertFalse(c.is_const)

    def test_isconst_mul_all_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=True)
        c = a * b
        self.assertTrue(c.is_const)

    def test_isconst_mul_no_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = 3
        c = a * b
        self.assertFalse(c.is_const)

    def test_isconst_mul_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = 3
        c = a * b
        self.assertTrue(c.is_const)

    def test_isconst_div_no_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=False)
        c = a / b
        self.assertFalse(c.is_const)

    def test_isconst_div_first_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = g.gen(3, is_const=True)
        c = a / b
        self.assertFalse(c.is_const)

    def test_isconst_div_second_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=False)
        c = a / b
        self.assertFalse(c.is_const)

    def test_isconst_div_all_const(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = g.gen(3, is_const=True)
        c = a / b
        self.assertTrue(c.is_const)

    def test_isconst_div_no_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = 3
        c = a / b
        self.assertFalse(c.is_const)

    def test_isconst_rdiv_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = 3
        c = b / a
        self.assertTrue(c.is_const)

    def test_isconst_div_no_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=False)
        b = 3
        c = a / b
        self.assertFalse(c.is_const)

    def test_isconst_rdiv_const_w_int(self):
        g = WireGroup(11)
        a = g.gen(4, is_const=True)
        b = 3
        c = b / a
        self.assertTrue(c.is_const)
