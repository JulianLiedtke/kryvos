"""
This module contains the test cases for comparison operations on
wires.
"""
import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.listgates as listgates
from src.groups.wiregroup import Wire, WireGroup
import src.gates.voting.irv as irv

log = logging.getLogger(__name__)


class IRVTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        Wire.n_mul = 0
        self.group = WireGroup(11)
        self.bits = 2
        self.election = irv.IRV(3, irv.EliminateFirstPossibilityEliminator(self.group, self.bits), self.group)
        self.ballots = self.election.get_empty_ballots()
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_irv_eliminate_first(self):
        self.ballots.add_votes_for_ordering([0, 1, 2], self.group.gen(3))
        self.ballots.add_votes_for_ordering([1, 2, 0], self.group.gen(2))
        self.ballots.add_votes_for_ordering([2, 1, 0], self.group.gen(1))
        res = self.election.evaluate_election(self.ballots)
        self._test_lists_equal(res, [1, 0, 1])

    def test_irv_nsw(self):
        randomness = [[0, 1, 2], [0, 2, 1]]
        election = irv.IRV(3, irv.NSWEliminator(self.group, self.bits, randomness), self.group)
        ballots = election.get_empty_ballots()
        ballots.add_votes_for_ordering([0, 1, 2], self.group.gen(2))
        ballots.add_votes_for_ordering([1, 2, 0], self.group.gen(1))
        ballots.add_votes_for_ordering([2, 0, 1], self.group.gen(1))
        res = election.evaluate_election(ballots)
        self._test_lists_equal(res, [0, 1, 1])

    def _test_lists_equal(self, list_wires, list_exp):
        self.assertEqual(len(list_wires), len(list_exp))
        for wire, exp in zip(list_wires, list_exp):
            self.assertEqual(wire, exp)
            self.assertTrue(isinstance(wire, Wire))
