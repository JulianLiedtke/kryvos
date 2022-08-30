import logging
import time
import unittest
from time import time

import src.gates.branching as branching
import src.gates.comparison as comparison
from src.groups.wiregroup import Wire, WireGroup
from src.utils.logging_utils import setup_logging

log = logging.getLogger(__name__)


class BranchingGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        Wire.n_mul = 0
        self.group = WireGroup(11)
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_if_then_else_gate_true(self):
        condition_wire = comparison.eq_zero(self.group, self.group.gen(0))
        if_wire = self.group.gen(2)
        else_wire = self.group.gen(3)
        res = branching.if_then_else(condition_wire, if_wire, else_wire)
        self.assertEqual(res, 2)
        self.assertTrue(isinstance(res, Wire))

    def test_if_then_else_gate_false(self):
        condition_wire = comparison.eq(self.group, self.group.gen(0), self.group.gen(1))
        if_wire = self.group.gen(2)
        else_wire = self.group.gen(3)
        res = branching.if_then_else(condition_wire, if_wire, else_wire)
        self.assertEqual(res, 3)
        self.assertTrue(isinstance(res, Wire))

    def test_if_then_set_zero_gate_true(self):
        condition_wire = comparison.eq_zero(self.group, self.group.gen(0))
        if_wire = self.group.gen(2)
        res = branching.if_then_set_zero(condition_wire, if_wire)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_if_then_set_zero_gate_false(self):
        condition_wire = comparison.eq(self.group, self.group.gen(0), self.group.gen(1))
        if_wire = self.group.gen(2)
        res = branching.if_then_set_zero(condition_wire, if_wire)
        self.assertEqual(res, 2)
        self.assertTrue(isinstance(res, Wire))
