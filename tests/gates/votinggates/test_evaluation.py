"""
This module contains test cases for the voting evaluation functions
based on wires.
"""
import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.voting.ballots as ballots
import src.gates.voting.evaluation as votingeval
from src.groups.wiregroup import Wire, WireGroup

log = logging.getLogger(__name__)


class BallotGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        self.group = WireGroup(13)
        Wire.n_mul = 0
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_compute_most_votes(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        res = votingeval.compute_most_votes(self.group, tally, 2)
        self._test_lists_equal(res, [0, 0, 1, 0, 0, 1])

    def test_compute_threshold(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        threshold = self.group.gen(1)
        res = votingeval.compute_threshold(self.group, tally, threshold, 2)
        self._test_lists_equal(res, [0, 1, 1, 1, 0, 1])

    def test_compute_best_n_one(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        best_n = self.group.gen(1)
        res = votingeval.compute_best_n(self.group, tally, best_n, 2)
        self._test_lists_equal(res, [0, 0, 1, 0, 0, 1])

    def test_compute_best_n_two(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        best_n = self.group.gen(2)
        res = votingeval.compute_best_n(self.group, tally, best_n, 2)
        self._test_lists_equal(res, [0, 0, 1, 0, 0, 1])

    def test_compute_best_n_three(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        best_n = self.group.gen(3)
        res = votingeval.compute_best_n(self.group, tally, best_n, 2)
        self._test_lists_equal(res, [0, 1, 1, 1, 0, 1])

    def test_compute_best_n_four(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        best_n = self.group.gen(4)
        res = votingeval.compute_best_n(self.group, tally, best_n, 2)
        self._test_lists_equal(res, [0, 1, 1, 1, 0, 1])

    def test_compute_best_n_five(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        best_n = self.group.gen(5)
        res = votingeval.compute_best_n(self.group, tally, best_n, 2)
        self._test_lists_equal(res, [1, 1, 1, 1, 1, 1])

    def test_compute_best_n_six(self):
        tally = self.group.gen_list([0, 1, 2, 1, 0, 2])
        best_n = self.group.gen(6)
        res = votingeval.compute_best_n(self.group, tally, best_n, 2)
        self._test_lists_equal(res, [1, 1, 1, 1, 1, 1])

    def test_smith_set_single_winner(self):
        """
        Candidate three wins against all others.
        """
        group = WireGroup(251)
        tally = []
        tally.append(group.gen_list([5, 2, 0, 3]))
        tally.append(group.gen_list([1, 5, 1, 1]))
        tally.append(group.gen_list([3, 2, 5, 3]))
        tally.append(group.gen_list([0, 0, 0, 5]))
        res = votingeval.smith_set(group, tally, 3)
        self._test_lists_equal(res, [0, 0, 1, 0])

    def test_smith_set_single_winner(self):
        """
        1 wins against 2 and 4

        2 wins against 4

        3 wins against 1 and 4

        Tie between 2 and 3

        Smith Set 1, 2 and 3
        """
        group = WireGroup(251)
        tally = []
        tally.append(group.gen_list([5, 2, 0, 3]))
        tally.append(group.gen_list([1, 5, 2, 1]))
        tally.append(group.gen_list([3, 2, 5, 3]))
        tally.append(group.gen_list([0, 0, 0, 5]))
        res = votingeval.smith_set(group, tally, 3)
        self._test_lists_equal(res, [1, 1, 1, 0])

    def test_majority_judgement_one(self):
        group = WireGroup(251)
        n_votes = 6
        tally = []
        tally.append(group.gen_list([1, 2, 2, 1]))
        tally.append(group.gen_list([2, 1, 3, 0]))
        tally.append(group.gen_list([0, 6, 0, 0]))
        res = votingeval.compute_majority_judgement(group, tally, n_votes, 3)
        self._test_lists_equal(res, [0, 0, 1])

    def test_majority_judgement_two(self):
        group = WireGroup(251)
        n_votes = 6
        tally = []
        tally.append(group.gen_list([1, 2, 2, 1]))
        tally.append(group.gen_list([2, 1, 3, 0]))
        res = votingeval.compute_majority_judgement(group, tally, n_votes, 3)
        self._test_lists_equal(res, [0, 1])

    def _test_lists_equal(self, list_wires, list_exp):
        self.assertEqual(len(list_wires), len(list_exp))
        for wire, exp in zip(list_wires, list_exp):
            self.assertEqual(wire, exp)
            self.assertTrue(isinstance(wire, Wire))
