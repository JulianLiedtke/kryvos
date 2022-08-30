"""
This module provides access to operations over lists.
"""
from typing import List, Tuple

import src.gates.arithmetic as arithmetic
import src.gates.assertgates as assertgates
import src.gates.bits as bitgates
import src.gates.branching as branching
import src.gates.comparison as comparison
from src.groups.group import Group
from src.groups.wiregroup import Wire


def is_value_in_list(group: Group, value: Wire, value_list: List[Wire]) -> Wire:
    """
    Checks whether the value of the wire is the same as the value of
    at least one wire in the list of wires.

    Returns a wire with value 1 if there exists such a wire in the
    list, and otherwise a wire with value 0.

    :param group: The group used for the wires.
    :type group: Group
    :param value: The value to find in the list.
    :type value: Wire
    :param value_list: The list of wires.
    :type value_list: List[Wire]
    :return: Wire with value 1 if there exists a wire of the given
        value, and otherwise wire with value 0.
    :rtype: Wire
    """
    ind_eq = [comparison.eq(group, value, vi) for vi in value_list]
    return bitgates.or_gate(group, ind_eq)


def is_threshold_reached(group: Group, wires: List[Wire], threshold: Wire) -> List[Wire]:
    """
    Computes for each wire whether it has value of at least threshold.

    The output is a list of (indicator-)wires. The wire at position i
    has value 1 if and only if the input wire at position i has a
    value which is at least threshold, otherwise, the indicator is set
    to 0.

    :param group: The group used for the wires.
    :type group: Group
    :param wires: List of wires
    :type wires: List[Wire]
    :param threshold: Votes threshold
    :type threshold: Wire
    :return: One indicator per wire
    :rtype: List[Wire]
    """
    return [comparison.gt(group, wire, threshold) for wire in wires]


def maximum(group: Group, wires: List[Wire], bits: int) -> List[Wire]:
    """
    Computes an indicator for each wire that states whether the value
    on the wire is the maximum value of the wires in the list.

    :param group: The group used for the wires.
    :type group: Group
    :param wires: List of wires
    :type wires: List[Wire]
    :param bits: The maximum number of bits of the wires in the list.
        This number needs to be lower than halve of the maximum bit
        size of the group, otherwise the gate is insecure.
    :type bits: int
    :return: One indicator per wire
    :rtype: List[Wire]
    """
    max_val = max(int(w) for w in wires)
    max_val = group.gen(max_val)
    ind_wires = []
    for wire in wires:
        ind_wires.append(comparison.eq(group, wire, max_val))
        assertgates.assert_gt(group, max_val, wire, bits)
    return ind_wires


def get_maximum_value(group: Group, wires: List[Wire], bits: int) -> Wire:
    """
    Returns the maximum value in the list.

    :param group: The group used for the wires.
    :type group: Group
    :param wires: List of wires
    :type wires: List[Wire]
    :param bits: The maximum number of bits of the wires in the list.
        This number needs to be lower than halve of the maximum bit
        size of the group, otherwise the gate is insecure.
    :type bits: int
    :return: Maximum value in list
    :rtype: Wire
    """
    max_val = max(int(w) for w in wires)
    max_val_wire = group.gen(max_val)
    for wire in wires:
        assertgates.assert_gt(group, max_val_wire, wire, bits)
    return max_val_wire


def minimum(group: Group, wires: List[Wire], bits: int) -> List[Wire]:
    """
    Computes an indicator for each wire that states whether the value
    on the wire is the minimum value of the wires in the list.

    :param group: The group used for the wires.
    :type group: Group
    :param wires: List of wires
    :type wires: List[Wire]
    :param bits: The maximum number of bits of the wires in the list.
        This number needs to be lower than halve of the maximum bit
        size of the group, otherwise the gate is insecure.
    :type bits: int
    :return: One indicator per wire
    :rtype: List[Wire]
    """
    min_val = min(int(w) for w in wires)
    min_wire = group.gen(min_val)
    ind_wires = []
    for wire in wires:
        ind_wires.append(comparison.eq(group, wire, min_wire))
        assertgates.assert_gt(group, wire, min_wire, bits)
    return ind_wires


def get_minimum_value(group: Group, wires: List[Wire], bits: int) -> Wire:
    """
    Returns the minimum value in the list.

    :param group: The group used for the wires.
    :type group: Group
    :param wires: List of wires
    :type wires: List[Wire]
    :param bits: The maximum number of bits of the wires in the list.
        This number needs to be lower than halve of the maximum bit
        size of the group, otherwise the gate is insecure.
    :type bits: int
    :return: Minimum value in list
    :rtype: Wire
    """
    min_val = min(int(w) for w in wires)
    min_wire = group.gen(min_val)
    for wire in wires:
        assertgates.assert_gt(group, wire, min_wire, bits)
    return min_wire


def find_first_indicator(group: Group, wires: List[Wire]) -> List[Wire]:
    """
    Finds the first entry in the list that is set to 1.

    :param group: The group used for the wires.
    :type group: Group
    :param wires: List of wires which are assumed to be bits.
    :type wires: List[Wire]
    :return: List of wires where all values are 0 except the entry of the first
        occurence of a 1 in the input wire list is set to 1.
    :rtype: List[Wire]
    """
    done = group.gen(0)
    res = []
    for wire in wires:
        res.append(wire * (1 - done))
        done += res[-1]
    return res


def find_and_count_min_of_set_inds(group: Group, wires: List[Wire], inds: List[Wire], bits: int) -> Tuple[List[Wire], Wire]:
    """
    Computes for each entry with set indicator whether this entry is
    of minimum value, considering only values where the indicator is
    set.

    :param group: The underlying group
    :type group: Group
    :param wires: The list of wires
    :type wires: List[Wire]
    :param inds: The list of indicators
    :type inds: List[Wire]
    :param bits: The maximum number of bits of the two input wires.
    :type bits: int
    :return: A list of indicators where the indicator is set when the
        value is minimal and a wire containing the number of how many
        times the minimal value occurs (both only considering values
        where the indicator is set)
    :rtype: Tuple[List[Wire], Wire]
    """
    min_val = min(int(w) for w, i in zip(wires, inds) if int(i) == 1)
    min_wire = group.gen(min_val)
    ind_wires = []
    sum_eq = group.gen(0)
    for wire, ind in zip(wires, inds):
        comp_eq = comparison.eq(group, wire, min_wire)
        sum_eq += branching.if_then_set_zero(1 - ind, comp_eq)
        comp_gt = comparison.gt(group, min_wire, wire, bits)
        comp = bitgates.and_gate(group, [comp_eq, comp_gt])
        ind_val = branching.if_then_set_zero(1 - ind, comp)
        ind_wires.append(ind_val)
    return ind_wires, sum_eq


def get_n_occurences(group: Group, wires: List[Wire], wire: Wire) -> Wire:
    """
    Returns how often the value on the wire occurs in the list.

    :param group: The underlying group
    :type group: Group
    :param wires: List of wires
    :type wires: List[Wire]
    :param wire: The wire with the value to find in the list
    :type wire: Wire
    :return: Returns how many wires in the list have the same value as
        the given wire.
    :rtype: Wire
    """
    n_occurences = group.gen(0)
    for wire_in_list in wires:
        ind_eq = comparison.eq(group, wire_in_list, wire)
        n_occurences += ind_eq
    return n_occurences


def get_list_with_index_set(group: Group, index: Wire, length: int) -> List[Wire]:
    """
    Returns a list of length length where the position at index is set
    to one and every other position is set to zero.

    :param group: The underlying group
    :type group: Group
    :param index: The index of the position to set to one
    :type index: Wire
    :param length: The length of the list
    :type length: int
    :return: List of length length with index at position set to one
    :rtype: List[Wire]
    """
    list_wires = []
    for i in range(length):
        comp = 1 - comparison.eq(group, index, group.gen(i))
        val = branching.if_then_set_zero(comp, group.gen(1))
        list_wires.append(val)
    return list_wires


def get_list_with_up_to_index_set(group: Group, index: Wire, length: int, bits: Wire) -> List[Wire]:
    """
    Returns a list of length length where all positions up to index
    are set to one and the remaining positions are set to zero.

    :param group: The underlying group
    :type group: Group
    :param index: The index of the position to set to one
    :type index: Wire
    :param length: The length of the list
    :type length: int
    :param bits: The maximum number of bits of the index wire
    :type bits: int
    :return: List of length length with positions up toindex at
        position set to one
    :rtype: List[Wire]
    """
    list_wires = []
    for i in range(length):
        comp = comparison.gt(group, i, index+1, bits)
        val = branching.if_then_set_zero(comp, group.gen(1))
        list_wires.append(val)
    return list_wires


def get_index_at(group: Group, wire_list: List[Wire], index: Wire) -> Wire:
    """
    Returns the value at index of the list.

    :param group: The underlying group
    :type group: Group
    :param wire_list: List of wires
    :type wire_list: List[Wire]
    :param index: Index
    :type index: Wire
    :return: wire_list[index]
    :rtype: Wire
    """
    index_list = get_list_with_index_set(group, index, len(wire_list))
    return sum([i*v for i, v in zip(index_list, wire_list)])


def get_median(group: Group, agg_wires: List[Wire], bits: int) -> Wire:
    """
    Computes the index containing the median of the aggregated values.

    :param group: The underlying group
    :type group: Group
    :param agg_wires: List of number of grades
    :type agg_wires: List[Wire]
    :param bits: The maximum number of bits of the index wire
    :type bits: int
    :return: The index of the median grade
    :rtype: Wire
    """
    vals = [int(i) for i in agg_wires]
    sum_vals_halve = sum(vals) / 2
    idx_median = 0
    current_val_sum = 0
    for i, val in enumerate(vals):
        current_val_sum += val
        if current_val_sum >= sum_vals_halve:
            idx_median = i
            break

    idx_median_prev = idx_median - 1
    if idx_median_prev < 0:
        idx_median_prev = 0

    idx_median_wire = group.gen(idx_median)
    idx_median_prev_wire = group.gen(idx_median_prev)

    n_votes_halve = arithmetic.division(sum(agg_wires), group.gen(2))

    index_list_median = get_list_with_up_to_index_set(group, idx_median_wire, len(agg_wires), bits)
    n_votes_median = sum([i * v for i, v in zip(index_list_median, agg_wires)])

    index_list_median_prev = get_list_with_up_to_index_set(group, idx_median_prev_wire, len(agg_wires), bits)
    n_votes_median_prev = sum([i * v for i, v in zip(index_list_median_prev, agg_wires)])

    comp_median = comparison.gt(group, n_votes_median, n_votes_halve, bits)
    comp_median_prev = comparison.gt(group, n_votes_median_prev, n_votes_halve, bits)
    comp_median_zero = comparison.eq(group, comp_median, group.gen(0))

    comp_or = bitgates.or_gate(group, [comp_median_prev, comp_median_zero])
    statement = bitgates.and_gate(group, [comp_median, comp_or])
    comparison.eq_zero(group, statement - 1)

    return idx_median_wire
