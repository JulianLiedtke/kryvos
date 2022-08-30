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

log = logging.getLogger(__name__)


class ListGatesTest(unittest.TestCase):

    def setUp(self):
        setup_logging()
        Wire.n_mul = 0
        self.group = WireGroup(11)
        self.startTime = time()

    def tearDown(self):
        t = time() - self.startTime
        log.info(f"{self.__class__.__name__}.{self._testMethodName}: {t:.3f}s")

    def test_is_value_in_list_true(self):
        """
        Test that the value in the list is found.
        """
        value = self.group.gen(3)
        values_list = self.group.gen_list([1, 2, 3, 4, 5, 6])
        res_wire = listgates.is_value_in_list(self.group, value, values_list)
        self.assertEqual(1, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_is_value_in_list_false(self):
        """
        Test missing value in list.
        """
        value = self.group.gen(3)
        values_list = self.group.gen_list([1, 2, 4, 5, 6])
        res_wire = listgates.is_value_in_list(self.group, value, values_list)
        self.assertEqual(0, res_wire)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_maximum_single_maximum(self):
        wires = self.group.gen_list([0, 1, 2])
        res_ind = listgates.maximum(self.group, wires, 2)
        self._test_lists_equal(res_ind, [0, 0, 1])

    def test_maximum_all_maximum(self):
        wires = self.group.gen_list([1, 1, 1, 1])
        res_ind = listgates.maximum(self.group, wires, 2)
        self._test_lists_equal(res_ind, [1, 1, 1, 1])

    def test_maximum_multiple_maximum(self):
        wires = self.group.gen_list([1, 0, 1, 0, 1])
        res_ind = listgates.maximum(self.group, wires, 2)
        self._test_lists_equal(res_ind, [1, 0, 1, 0, 1])

    def test_get_maximum_value_single_maximum(self):
        wires = self.group.gen_list([0, 1, 2])
        res = listgates.get_maximum_value(self.group, wires, 2)
        self.assertEqual(2, res)
        self.assertTrue(isinstance(res, Wire))

    def test_get_maximum_value_all_maximum(self):
        wires = self.group.gen_list([1, 1, 1, 1])
        res = listgates.get_maximum_value(self.group, wires, 2)
        self.assertEqual(1, res)
        self.assertTrue(isinstance(res, Wire))

    def test_get_maximum_value_multiple_maximum(self):
        wires = self.group.gen_list([1, 0, 1, 0, 1])
        res = listgates.get_maximum_value(self.group, wires, 2)
        self.assertEqual(1, res)
        self.assertTrue(isinstance(res, Wire))

    def test_minimum_single_minimum(self):
        wires = self.group.gen_list([0, 1, 2])
        res_ind = listgates.minimum(self.group, wires, 2)
        self._test_lists_equal(res_ind, [1, 0, 0])

    def test_minimum_all_minimum(self):
        wires = self.group.gen_list([1, 1, 1, 1])
        res_ind = listgates.minimum(self.group, wires, 2)
        self._test_lists_equal(res_ind, [1, 1, 1, 1])

    def test_minimum_multiple_minimum(self):
        wires = self.group.gen_list([1, 0, 1, 0, 1])
        res_ind = listgates.minimum(self.group, wires, 2)
        self._test_lists_equal(res_ind, [0, 1, 0, 1, 0])

    def test_get_minimum_value_single_minimum(self):
        wires = self.group.gen_list([0, 1, 2])
        res = listgates.get_minimum_value(self.group, wires, 2)
        self.assertEqual(0, res)
        self.assertTrue(isinstance(res, Wire))

    def test_get_minimum_value_all_minimum(self):
        wires = self.group.gen_list([1, 1, 1, 1])
        res = listgates.get_minimum_value(self.group, wires, 2)
        self.assertEqual(1, res)
        self.assertTrue(isinstance(res, Wire))

    def test_get_minimum_value_multiple_minimum(self):
        wires = self.group.gen_list([1, 0, 1, 0, 1])
        res = listgates.get_minimum_value(self.group, wires, 2)
        self.assertEqual(0, res)
        self.assertTrue(isinstance(res, Wire))

    def test_find_indicator_in_list_mid(self):
        wires = self.group.gen_list([0, 1, 0])
        res = listgates.find_first_indicator(self.group, wires)
        self._test_lists_equal(res, [0, 1, 0])

    def test_find_indicator_in_list_start(self):
        wires = self.group.gen_list([1, 0, 0])
        res = listgates.find_first_indicator(self.group, wires)
        self._test_lists_equal(res, [1, 0, 0])

    def test_find_indicator_in_list_end(self):
        wires = self.group.gen_list([0, 0, 1])
        res = listgates.find_first_indicator(self.group, wires)
        self._test_lists_equal(res, [0, 0, 1])

    def test_find_indicator_in_list_multiple(self):
        wires = self.group.gen_list([0, 0, 1, 0, 1, 0, 1])
        res = listgates.find_first_indicator(self.group, wires)
        self._test_lists_equal(res, [0, 0, 1, 0, 0, 0, 0])

    def test_find_and_count_min_of_set_inds_1(self):
        """
        One occurence of the minimum
        """
        wires = self.group.gen_list([0, 0, 3, 0, 2, 0, 1])
        wires_ind = self.group.gen_list([0, 0, 1, 0, 1, 0, 1])
        res_list, res_wire = listgates.find_and_count_min_of_set_inds(self.group, wires, wires_ind, 2)
        self._test_lists_equal(res_list, [0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(res_wire, 1)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_find_and_count_min_of_set_inds_2(self):
        """
        Two occurences of the minimum
        """
        wires = self.group.gen_list([0, 0, 1, 0, 2, 0, 1])
        wires_ind = self.group.gen_list([0, 0, 1, 0, 1, 0, 1])
        res_list, res_wire = listgates.find_and_count_min_of_set_inds(self.group, wires, wires_ind, 2)
        self._test_lists_equal(res_list, [0, 0, 1, 0, 0, 0, 1])
        self.assertEqual(res_wire, 2)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_find_and_count_min_of_set_ind_all_equal(self):
        """
        Three occurences of the minimum and all values are equal
        """
        wires = self.group.gen_list([0, 0, 0, 0, 0, 0, 0])
        wires_ind = self.group.gen_list([0, 0, 1, 0, 1, 0, 1])
        res_list, res_wire = listgates.find_and_count_min_of_set_inds(self.group, wires, wires_ind, 2)
        self._test_lists_equal(res_list, [0, 0, 1, 0, 1, 0, 1])
        self.assertEqual(res_wire, 3)
        self.assertTrue(isinstance(res_wire, Wire))

    def test_get_n_occurences_1(self):
        wires = self.group.gen_list([0, 1, 2, 3, 4, 5, 6])
        wire = self.group.gen(1)
        res = listgates.get_n_occurences(self.group, wires, wire)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_get_n_occurences_find_all(self):
        wires = self.group.gen_list([5, 4, 3, 2, 1])
        for i in range(1, 6):
            wire = self.group.gen(i)
            res = listgates.get_n_occurences(self.group, wires, wire)
            self.assertEqual(res, 1)
            self.assertTrue(isinstance(res, Wire))

    def test_get_n_occurences_2(self):
        wires = self.group.gen_list([0, 1, 2, 3, 4, 3, 6])
        wire = self.group.gen(3)
        res = listgates.get_n_occurences(self.group, wires, wire)
        self.assertEqual(res, 2)
        self.assertTrue(isinstance(res, Wire))

    def test_get_n_occurences_no_matches(self):
        wires = self.group.gen_list([0, 1, 2, 0, 4, 5, 6])
        wire = self.group.gen(3)
        res = listgates.get_n_occurences(self.group, wires, wire)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def test_list_with_index_set(self):
        res = listgates.get_list_with_index_set(self.group, 3, 5)
        self._test_lists_equal(res, [0, 0, 0, 1, 0])

    def test_list_with_index_set_zero(self):
        res = listgates.get_list_with_index_set(self.group, 0, 5)
        self._test_lists_equal(res, [1, 0, 0, 0, 0])

    def test_list_with_up_to_index_set(self):
        res = listgates.get_list_with_up_to_index_set(self.group, 3, 5, 2)
        self._test_lists_equal(res, [1, 1, 1, 1, 0])

    def test_list_with_up_to_index_set_zero(self):
        res = listgates.get_list_with_up_to_index_set(self.group, 0, 5, 2)
        self._test_lists_equal(res, [1, 0, 0, 0, 0])

    def test_list_with_up_to_index_set_negative(self):
        res = listgates.get_list_with_up_to_index_set(self.group, -1, 5, 2)
        self._test_lists_equal(res, [0, 0, 0, 0, 0])

    def test_get_index(self):
        wire_list = self.group.gen_list([1,2,3,4])
        index = self.group.gen(2)
        res = listgates.get_index_at(self.group, wire_list, index)
        self.assertEqual(res, 3)
        self.assertTrue(isinstance(res, Wire))

    def test_median_one(self):
        agg_grades = [1, 2, 0, 2, 1]
        res = listgates.get_median(self.group, agg_grades, 2)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_median_two(self):
        agg_grades = [2, 1, 3, 0, 0]
        res = listgates.get_median(self.group, agg_grades, 2)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_median_three(self):
        agg_grades = [0, 6, 0, 0, 0, 0]
        res = listgates.get_median(self.group, agg_grades, 2)
        self.assertEqual(res, 1)
        self.assertTrue(isinstance(res, Wire))

    def test_median_first_entry(self):
        agg_grades = [6, 0, 0, 0, 0, 0]
        res = listgates.get_median(self.group, agg_grades, 2)
        self.assertEqual(res, 0)
        self.assertTrue(isinstance(res, Wire))

    def _test_lists_equal(self, list_wires, list_exp):
        self.assertEqual(len(list_wires), len(list_exp))
        for wire, exp in zip(list_wires, list_exp):
            self.assertEqual(wire, exp)
            self.assertTrue(isinstance(wire, Wire))
