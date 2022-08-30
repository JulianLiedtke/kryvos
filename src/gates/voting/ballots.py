"""
Contains evaluation functions for ballot relations.
"""
import itertools
from typing import List

import src.gates.assertgates as assertgates
import src.gates.bits as bitgates
import src.gates.branching as branching
import src.gates.comparison as comparison
import src.gates.listgates as listgates
from src.groups.group import Group
from src.groups.wiregroup import Wire


def assert_single_choice(group: Group, ballot: List[Wire]) -> None:
    """
    Asserts that each entry is binary and that exactly one one occurs.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :raises ValueError: Raised if the ballot does not verify.
    """
    for wire in ballot:
        assertgates.assert_bit(wire)
    assertgates.assert_equal(group, ballot, [group.gen(1)])


def verify_single_choice(group: Group, ballot: List[Wire]) -> Wire:
    """
    Verifies that each entry is binary and that exactly one one
    occurs.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :return: A wire with value 1 if the ballot verifies. Otherwise,
        the wire will have value 0.
    :rtype: Wire
    """
    wires_valid = []
    for wire in ballot:
        ind_bit = bitgates.verify_bit(group, wire)
        wires_valid.append(ind_bit)
    ind_comp = comparison.eq(group, sum(ballot), group.gen(1))
    wires_valid.append(ind_comp)
    return bitgates.and_gate(group, wires_valid)


def assert_multiple_choice(group: Group, ballot: List[Wire], max_choices: Wire = None, bits: int = None) -> None:
    """
    Asserts that each entry is binary and that exactly one one occurs.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :param max_choices: maximum number of possibles ones, defaults to
        None (arbitrary number of ones allowed)
    :type max_choices: int, optional
    :param bits: Maximum bit size of the entries in the ballot,
        defaults to None (only needed to be set if max_choices is set)
    :type bits: int, optional
    :raises ValueError: Raised if the ballot does not verify.
    """
    for wire in ballot:
        assertgates.assert_bit(wire)
    if max_choices is not None:
        n_choices = sum(ballot)
        assertgates.assert_gt(group, max_choices, n_choices, bits)


def verify_multiple_choice(group: Group, ballot: List[Wire], max_choices: Wire = None, bits: int = None) -> Wire:
    """
    Verifies that each entry is binary and that exactly one one occurs.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :param max_choices: maximum number of possibles ones, defaults to
        None (arbitrary number of ones allowed)
    :type max_choices: int, optional
    :param bits: Maximum bit size of the entries in the ballot,
        defaults to None (only needed to be set if max_choices is set)
    :type bits: int, optional
    :return: A wire with value 1 if the ballot verifies. Otherwise,
        the wire will have value 0.
    :rtype: Wire
    """
    wires_valid = []
    for wire in ballot:
        ind_bit = bitgates.verify_bit(group, wire)
        wires_valid.append(ind_bit)
    if max_choices is not None:
        n_choices = sum(ballot)
        ind_gt = comparison.gt(group, max_choices, n_choices, bits)
        wires_valid.append(ind_gt)
    return bitgates.and_gate(group, wires_valid)


def assert_borda_ballot(group: Group, ballot: List[Wire], ordered_points: List[Wire]) -> None:
    """
    Asserts a Borda ballot. If the same number of points is assigned
    to more than one choice (say, n many), the next n points in the
    point list cannot be assigned.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :param ordered_points: Ordered list of Borda points
    :type ordered_points: List[Wire]
    :raises ValueError: Raised if the ballot does not verify.
    """
    fuel = group.gen(0)
    for point in ordered_points:
        n_occ = listgates.get_n_occurences(group, ballot, point)
        ind_fuel_zero = comparison.eq_zero(group, fuel)
        ind_n_occ_zero = comparison.eq_zero(group, n_occ)
        xor_val = bitgates.xor_gate_two_inputs(group, ind_fuel_zero, ind_n_occ_zero)
        assertgates.assert_equal(group, [xor_val], [group.gen(1)])
        fuel = branching.if_then_else(ind_fuel_zero, fuel, fuel - 1)
        fuel = branching.if_then_else(ind_n_occ_zero, fuel, fuel + n_occ - 1)


def verify_borda_ballot(group: Group, ballot: List[Wire], ordered_points: List[Wire]) -> Wire:
    """
    Verifies a Borda ballot. If the same number of points is assigned
    to more than one choice (say, n many), the next n points in the
    point list cannot be assigned.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :param ordered_points: Ordered list of Borda points
    :type ordered_points: List[Wire]
    :return: A wire with value 1 if the ballot verifies. Otherwise,
        the wire will have value 0.
    :rtype: Wire
    """
    wires_valid = []
    fuel = group.gen(0)
    for point in ordered_points:
        n_occ = listgates.get_n_occurences(group, ballot, point)
        ind_fuel_zero = comparison.eq_zero(group, fuel)
        ind_n_occ_zero = comparison.eq_zero(group, n_occ)
        xor_val = bitgates.xor_gate_two_inputs(group, ind_fuel_zero, ind_n_occ_zero)
        wires_valid.append(comparison.eq(group, xor_val, group.gen(1)))
        fuel = branching.if_then_else(ind_fuel_zero, fuel, fuel - 1)
        fuel = branching.if_then_else(ind_n_occ_zero, fuel, fuel + n_occ - 1)
    return bitgates.and_gate(group, wires_valid)


def assert_majorityjudgement_ballot(group: Group, ballot: List[Wire], grades: List[Wire]) -> None:
    """
    Asserts a Majority Judgement ballot.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :param grades: List of possible grades
    :type grades: List[Wire]
    :raises ValueError: Raised if the ballot does not verify.
    """
    for choice in ballot:
        ind_poss_grade = listgates.is_value_in_list(group, choice, grades)
        assertgates.assert_equal(group, [ind_poss_grade], [group.gen(1)])


def verify_majorityjudgement_ballot(group: Group, ballot: List[Wire], grades: List[Wire]) -> Wire:
    """
    Verifies a Majority Judgement ballot.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[Wire]
    :param grades: List of possible grades
    :type grades: List[Wire]
    :return: A wire with value 1 if the ballot verifies. Otherwise,
        the wire will have value 0.
    :rtype: Wire
    """
    wires_valid = []
    for choice in ballot:
        ind_poss_grade = listgates.is_value_in_list(group, choice, grades)
        wires_valid.append(ind_poss_grade)
    return bitgates.and_gate(group, wires_valid)


def assert_condorcet_ballot(group: Group, ballot: List[List[Wire]]) -> None:
    """
    Asserts a Condorcet Judgement ballot.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[List[Wire]]
    :raises ValueError: Raised if the ballot does not verify.
    """
    for i, row in enumerate(ballot):
        for j, entry in enumerate(row):
            if i == j:
                continue
            assertgates.assert_bit(entry)

    comb_i_j_done = set()
    for i, j, k in itertools.product(range(len(ballot)), range(len(ballot)), range(len(ballot))):
        if i == j or i == k or j == k:
            continue
        if (i, j) in comb_i_j_done:
            continue
        if (j, i) in comb_i_j_done:
            continue
        value_i_j = ballot[i][j]
        value_j_i = ballot[j][i]
        value_i_k = ballot[i][k]
        value_j_k = ballot[j][k]
        assertgates.assert_equal(group, [value_i_j, value_j_i], [group.gen(1)])
        ind_false = bitgates.and_gate(group, [value_i_j, value_j_k, 1-value_i_k])
        assertgates.assert_equal(group, [ind_false], [group.gen(0)])
        comb_i_j_done.add((i, j))
        comb_i_j_done.add((j, i))


def verify_condorcet_ballot(group: Group, ballot: List[List[Wire]]) -> None:
    """
    Verifies a Condorcet Judgement ballot.

    :param group: The underlying group
    :type group: Group
    :param ballot: The ballot
    :type ballot: List[List[Wire]]
    :return: A wire with value 1 if the ballot verifies. Otherwise,
        the wire will have value 0.
    :rtype: Wire
    """
    wires_valid = []

    for i, row in enumerate(ballot):
        for j, entry in enumerate(row):
            if i == j:
                continue
            ind_bit = bitgates.verify_bit(group, entry)
            wires_valid.append(ind_bit)

    comb_i_j_done = set()
    for i, j, k in itertools.product(range(len(ballot)), range(len(ballot)), range(len(ballot))):
        if i == j or i == k or j == k:
            continue
        if (i, j) in comb_i_j_done:
            continue
        if (j, i) in comb_i_j_done:
            continue
        value_i_j = ballot[i][j]
        value_j_i = ballot[j][i]
        value_i_k = ballot[i][k]
        value_j_k = ballot[j][k]
        ind_ij_ji_one = comparison.eq(group, value_i_j + value_j_i, group.gen(1))
        wires_valid.append(ind_ij_ji_one)
        ind_false = bitgates.and_gate(group, [value_i_j, value_j_k, 1-value_i_k])
        ind_transitivity = comparison.eq_zero(group, ind_false)
        wires_valid.append(ind_transitivity)
        comb_i_j_done.add((i, j))
        comb_i_j_done.add((j, i))
    return bitgates.and_gate(group, wires_valid)


def compute_borda_tournament_style_ballot(group: Group, ranking: List[Wire], bits: int) -> List[Wire]:
    """
    Computes the tournament style Borda points based on the ranking of
    the choices.

    Important: Zero is interpreted as the highest rank.

    :param group: The underlying group
    :type group: Group
    :param ranking: Ranking of the choice. Greater value means higher
        rank
    :type ranking: List[Wire]
    :param bits: Maximum bit size of the entries in the ballot
    :type bits: int
    :return: List of points per choice
    :rtype: List[Wire]
    """
    points = []
    for i, ranking_val in enumerate(ranking):
        n_truely_greater = sum([comparison.gt(group, ranking_val - 1, comp_val, bits) for j, comp_val in enumerate(ranking) if j != i])
        n_eq = sum([comparison.eq(group, ranking_val, comp_val) for j, comp_val in enumerate(ranking) if j != i])
        points.append(2 * n_truely_greater + comparison.gt(group, n_eq, group.gen(1), bits))
    return points
