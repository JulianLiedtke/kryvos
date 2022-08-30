"""
This module contains test cases for the ballot verification operations
based on wires.
"""
import logging
import time
import unittest
from time import time

from src.utils.logging_utils import setup_logging
import src.gates.voting.ballots as ballots
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

    def test_assert_single_choice_ok(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 0])
        ballots.assert_single_choice(self.group, ballot)

    def test_assert_single_choice_no_1(self):
        ballot = self.group.gen_list([0, 0, 0, 0, 0])
        self.assertRaises(ValueError, lambda: ballots.assert_single_choice(self.group, ballot))

    def test_assert_single_choice_multiple_1(self):
        ballot = self.group.gen_list([0, 1, 0, 1, 0])
        self.assertRaises(ValueError, lambda: ballots.assert_single_choice(self.group, ballot))

    def test_assert_single_choice_non_binary(self):
        ballot = self.group.gen_list([0, 2, 0, 1, 0])
        self.assertRaises(ValueError, lambda: ballots.assert_single_choice(self.group, ballot))

    def test_verify_single_choice_ok(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 0])
        res = ballots.verify_single_choice(self.group, ballot)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_single_choice_no_1(self):
        ballot = self.group.gen_list([0, 0, 0, 0, 0])
        res = ballots.verify_single_choice(self.group, ballot)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_single_choice_multiple_1(self):
        ballot = self.group.gen_list([0, 1, 0, 1, 0])
        res = ballots.verify_single_choice(self.group, ballot)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_single_choice_non_binary(self):
        ballot = self.group.gen_list([0, 2, 0, 1, 0])
        res = ballots.verify_single_choice(self.group, ballot)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_assert_multiple_choice_ok(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 0])
        ballots.assert_multiple_choice(self.group, ballot)

    def test_assert_multiple_choice_multiple_ok(self):
        ballot = self.group.gen_list([0, 1, 1, 0, 1])
        ballots.assert_multiple_choice(self.group, ballot)

    def test_assert_multiple_choice_all_ok(self):
        ballot = self.group.gen_list([1, 1, 1, 1, 1])
        ballots.assert_multiple_choice(self.group, ballot)

    def test_assert_multiple_choice_no_1(self):
        ballot = self.group.gen_list([0, 0, 0, 0, 0])
        ballots.assert_multiple_choice(self.group, ballot)

    def test_assert_multiple_choice_non_binary(self):
        ballot = self.group.gen_list([0, 2, 0, 1, 0])
        self.assertRaises(ValueError, lambda: ballots.assert_multiple_choice(self.group, ballot))

    def test_assert_multiple_choice_max_chocies_ok(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 0])
        ballots.assert_multiple_choice(self.group, ballot, max_choices=1, bits=2)

    def test_assert_multiple_choice_max_chocies_too_many(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 1])
        self.assertRaises(ValueError, lambda: ballots.assert_multiple_choice(self.group, ballot, max_choices=1, bits=2))

    def test_verify_multiple_choice_ok(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 0])
        res = ballots.verify_multiple_choice(self.group, ballot)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_multiple_choice_multiple_ok(self):
        ballot = self.group.gen_list([0, 1, 1, 0, 1])
        res = ballots.verify_multiple_choice(self.group, ballot)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_multiple_choice_all_ok(self):
        ballot = self.group.gen_list([1, 1, 1, 1, 1])
        res = ballots.verify_multiple_choice(self.group, ballot)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_multiple_choice_no_1(self):
        ballot = self.group.gen_list([0, 0, 0, 0, 0])
        res = ballots.verify_multiple_choice(self.group, ballot)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_multiple_choice_non_binary(self):
        ballot = self.group.gen_list([0, 2, 0, 1, 0])
        res = ballots.verify_multiple_choice(self.group, ballot)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_multiple_choice_max_chocies_ok(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 0])
        res = ballots.verify_multiple_choice(self.group, ballot, max_choices=1, bits=2)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_multiple_choice_max_chocies_too_many(self):
        ballot = self.group.gen_list([0, 0, 1, 0, 1])
        res = ballots.verify_multiple_choice(self.group, ballot, max_choices=1, bits=2)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_assert_borda_ok(self):
        ballot = self.group.gen_list([5, 1, 3, 2, 4])
        points = self.group.gen_list([5, 4, 3, 2, 1])
        ballots.assert_borda_ballot(self.group, ballot, points)

    def test_assert_borda_ok_with_skip(self):
        ballot = self.group.gen_list([5, 1, 3, 2, 4])
        points = self.group.gen_list([5, 5, 3, 2, 1])
        ballots.assert_borda_ballot(self.group, ballot, points)

    def test_assert_borda_ok_with_large_skip(self):
        ballot = self.group.gen_list([5, 1, 3, 2, 4])
        points = self.group.gen_list([5, 5, 1, 2, 5])
        ballots.assert_borda_ballot(self.group, ballot, points)

    def test_assert_borda_skipped_too_many(self):
        ballot = self.group.gen_list([5, 5, 1, 1, 0])
        points = self.group.gen_list([5, 4, 3, 2, 1])
        self.assertRaises(ValueError, lambda: ballots.assert_borda_ballot(self.group, ballot, points))

    def test_assert_borda_skipped_not_enough(self):
        ballot = self.group.gen_list([5, 5, 4, 1, 0])
        points = self.group.gen_list([5, 4, 3, 2, 1])
        self.assertRaises(ValueError, lambda: ballots.assert_borda_ballot(self.group, ballot, points))

    def test_verify_borda_ok(self):
        ballot = self.group.gen_list([5, 1, 3, 2, 4])
        points = self.group.gen_list([5, 4, 3, 2, 1])
        res = ballots.verify_borda_ballot(self.group, ballot, points)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_borda_ok_with_skip(self):
        ballot = self.group.gen_list([5, 1, 3, 2, 4])
        points = self.group.gen_list([5, 5, 3, 2, 1])
        res = ballots.verify_borda_ballot(self.group, ballot, points)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_borda_ok_with_large_skip(self):
        ballot = self.group.gen_list([5, 1, 3, 2, 4])
        points = self.group.gen_list([5, 5, 1, 2, 5])
        res = ballots.verify_borda_ballot(self.group, ballot, points)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_borda_skipped_too_many(self):
        ballot = self.group.gen_list([5, 5, 1, 1, 0])
        points = self.group.gen_list([5, 4, 3, 2, 1])
        res = ballots.verify_borda_ballot(self.group, ballot, points)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_borda_skipped_not_enough(self):
        ballot = self.group.gen_list([5, 5, 4, 1, 0])
        points = self.group.gen_list([5, 4, 3, 2, 1])
        res = ballots.verify_borda_ballot(self.group, ballot, points)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_assert_mj_ballot_ok(self):
        ballot = self.group.gen_list([0, 0, 3, 3, 0])
        grades = self.group.gen_list([0, 3])
        ballots.assert_majorityjudgement_ballot(self.group, ballot, grades)

    def test_assert_mj_grade_not_in_list(self):
        ballot = self.group.gen_list([0, 1, 3, 3, 0])
        grades = self.group.gen_list([0, 3])
        self.assertRaises(ValueError, lambda: ballots.assert_majorityjudgement_ballot(self.group, ballot, grades))

    def test_verify_mj_ballot_ok(self):
        ballot = self.group.gen_list([0, 0, 3, 3, 0])
        grades = self.group.gen_list([0, 3])
        res = ballots.verify_majorityjudgement_ballot(self.group, ballot, grades)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_mj_grade_not_in_list(self):
        ballot = self.group.gen_list([0, 1, 3, 3, 0])
        grades = self.group.gen_list([0, 3])
        res = ballots.verify_majorityjudgement_ballot(self.group, ballot, grades)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_assert_condorcet_ok(self):
        ballot_plain = [[2, 1, 1, 1], [0, 3, 1, 1], [0, 0, 5, 0], [0, 0, 1, 7]]
        ballot = [self.group.gen_list(l) for l in ballot_plain]
        ballots.assert_condorcet_ballot(self.group, ballot)

    def test_assert_condorcet_tie(self):
        ballot_plain = [[2, 1, 1, 1], [1, 3, 1, 1], [0, 0, 5, 0], [0, 0, 1, 7]]
        ballot = [self.group.gen_list(l) for l in ballot_plain]
        self.assertRaises(ValueError, lambda: ballots.assert_condorcet_ballot(self.group, ballot))

    def test_assert_condorcet_not_transitive(self):
        ballot_plain = [[2, 1, 1, 1], [0, 3, 1, 1], [0, 0, 5, 0], [0, 1, 1, 7]]
        ballot = [self.group.gen_list(l) for l in ballot_plain]
        self.assertRaises(ValueError, lambda: ballots.assert_condorcet_ballot(self.group, ballot))

    def test_verify_condorcet_ok(self):
        ballot_plain = [[2, 1, 1, 1], [0, 3, 1, 1], [0, 0, 5, 0], [0, 0, 1, 7]]
        ballot = [self.group.gen_list(l) for l in ballot_plain]
        res = ballots.verify_condorcet_ballot(self.group, ballot)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_condorcet_tie(self):
        ballot_plain = [[2, 1, 1, 1], [1, 3, 1, 1], [0, 0, 5, 0], [0, 0, 1, 7]]
        ballot = [self.group.gen_list(l) for l in ballot_plain]
        res = ballots.verify_condorcet_ballot(self.group, ballot)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_verify_condorcet_not_transitive(self):
        ballot_plain = [[2, 1, 1, 1], [0, 3, 1, 1], [0, 0, 5, 0], [0, 1, 1, 7]]
        ballot = [self.group.gen_list(l) for l in ballot_plain]
        res = ballots.verify_condorcet_ballot(self.group, ballot)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_borda_tournament_style_ballot_no_ties(self):
        group = WireGroup(251)
        ranking = group.gen_list([10, 8, 9, 3, 1, 12])
        ballot = ballots.compute_borda_tournament_style_ballot(group, ranking, bits=4)
        self._test_lists_equal(ballot, [8, 4, 6, 2, 0, 10])

    def test_borda_tournament_style_ballot_ties_last_place(self):
        group = WireGroup(251)
        ranking = group.gen_list([10, 8, 1, 9, 3, 1, 12])
        ballot = ballots.compute_borda_tournament_style_ballot(group, ranking, bits=4)
        self._test_lists_equal(ballot, [10, 6, 1, 8, 4, 1, 12])

    def test_borda_tournament_style_ballot_ties_first_place(self):
        group = WireGroup(251)
        ranking = group.gen_list([10, 8, 12, 9, 3, 1, 12])
        ballot = ballots.compute_borda_tournament_style_ballot(group, ranking, bits=4)
        self._test_lists_equal(ballot, [8, 4, 11, 6, 2, 0, 11])

    def test_borda_tournament_style_ballot_multiple_ties(self):
        group = WireGroup(251)
        ranking = group.gen_list([11, 1, 7, 3, 7, 3])
        ballot = ballots.compute_borda_tournament_style_ballot(group, ranking, bits=4)
        self._test_lists_equal(ballot, [10, 0, 7, 3, 7, 3])

    def test_borda_tournament_style_ballot_tie_multiple_choices(self):
        group = WireGroup(251)
        ranking = group.gen_list([11, 1, 4, 4, 4, 4])
        ballot = ballots.compute_borda_tournament_style_ballot(group, ranking, bits=4)
        self._test_lists_equal(ballot, [10, 0, 3, 3, 3, 3])

    def _test_lists_equal(self, list_wires, list_exp):
        self.assertEqual(len(list_wires), len(list_exp))
        for wire, exp in zip(list_wires, list_exp):
            self.assertEqual(wire, exp)
            self.assertTrue(isinstance(wire, Wire))
