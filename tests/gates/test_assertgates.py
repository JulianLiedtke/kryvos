import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.assertgates as assertgates
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class AssertGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        self.group = WireGroup(11)
        Wire.n_mul = 0
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_assert_bit_gate_zero(self):
        a = self.group.gen(0)
        assertgates.assert_bit(a)
        self.assertTrue(isinstance(a, Wire))

    def test_assert_bit_gate_one(self):
        a = self.group.gen(1)
        assertgates.assert_bit(a)
        self.assertTrue(isinstance(a, Wire))

    def test_assert_bit_gate_non_bit(self):
        for a in range(2, len(self.group)):
            a_wire = self.group.gen(a)
            self.assertRaises(ValueError, lambda: assertgates.assert_bit(a_wire))

    def test_assert_bit_gate_n_mults(self):
        a = self.group.gen(1)
        assertgates.assert_bit(a)
        self.assertTrue(isinstance(a, Wire))
        self.assertEqual(1, Wire.n_mul)

    def test_assert_gt_strict_gt(self):
        one = self.group.gen(1)
        two = self.group.gen(0)
        assertgates.assert_gt(self.group, one, two, 2)
        assertgates.assert_gt(self.group, one, two, 1)

    def test_assert_gt_eq(self):
        one = self.group.gen(1)
        two = self.group.gen(1)
        assertgates.assert_gt(self.group, one, two, 2)
        assertgates.assert_gt(self.group, one, two, 1)

    def test_assert_gt_raises_assert(self):
        one = self.group.gen(0)
        two = self.group.gen(1)
        self.assertRaises(ValueError, lambda: assertgates.assert_gt(self.group, one, two, 2))

