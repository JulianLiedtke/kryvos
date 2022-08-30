"""
Contains evaluation functions for voting methods.
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


def compute_most_votes(group: Group, tally: List[Wire], bits: int) -> List[Wire]:
    """
    Computes the choices which received the most votes.

    :param group: The underlying group
    :type group: Group
    :param tally: The aggregated tally
    :type tally: List[Wire]
    :param bits: The maximal number of bits of the values in the tally
    :type bits: int
    :return: Indicator for each choice indicating whether it received
        the most votes.
    :rtype: List[Wire]
    """
    return listgates.maximum(group, tally, bits)


def compute_threshold(group: Group, tally: List[Wire], threshold: Wire, bits: int) -> List[Wire]:
    """
    Computes for each choice whether is received at least threshold
    many votes.

    :param group: The underlying group
    :type group: Group
    :param tally: The aggregated tally
    :type tally: List[Wire]
    :param threshold: The treshold
    :type threshold: Wire
    :param bits: The maximal number of bits of the values in the tally
    :type bits: int
    :return: Indicator for each choice indicating whether it received
        the most votes.
    :rtype: List[Wire]
    """
    return [comparison.gt(group, votes, threshold, bits) for votes in tally]


def compute_best_n(group: Group, tally: List[Wire], n_best: Wire, bits: int) -> List[Wire]:
    """
    Computes the n choices which received the most votes.

    :param group: The underlying group
    :type group: Group
    :param tally: The aggregated tally
    :type tally: List[Wire]
    :param n_best: The number of best choices
    :type n_best: Wire
    :param bits: The maximal number of bits of the values in the tally
    :type bits: int
    :return: Indicator for each choice indicating whether it received
        the most votes.
    :rtype: List[Wire]
    """
    max_threshold = 0
    for votes in tally:
        votes_int = int(votes)
        n_choices = sum([1 for i in tally if int(i) >= votes_int])
        if n_choices >= int(n_best):
            if votes_int > max_threshold:
                max_threshold = votes_int
    threshold = group.gen(max_threshold)
    threshold_plus_one = group.gen(max_threshold + 1)
    ind_best_n_choices = compute_threshold(group, tally, threshold, bits)
    ind_best_n_choices_plus_one = compute_threshold(group, tally, threshold_plus_one, bits)
    assertgates.assert_gt(group, sum(ind_best_n_choices), n_best, bits)
    assertgates.assert_gt(group, n_best, sum(ind_best_n_choices_plus_one) + 1, bits)
    return ind_best_n_choices


def smith_set(group: Group, tally: List[List[Wire]], bits: int) -> List[Wire]:
    """
    Computes the Smith set.

    :param group: The underlying group
    :type group: Group
    :param tally: The aggregated tally
    :type tally: List[List[Wire]]
    :param bits: The maximal number of bits of the values in the tally
    :type bits: int
    :return: Indicator for each choice indicating whether it is in the
        Smith set.
    :rtype: List[Wire]
    """
    cache_comparisons = {}

    ind_smith_set = group.gen_list([0 for _ in tally])
    won_duels = []
    for choice in range(len(tally)):
        n_won_duels = group.gen(0)
        for other_choice in range(len(tally)):
            if other_choice == choice:
                continue
            ind_won = comparison.gt(group, tally[choice][other_choice], tally[other_choice][choice], bits)
            if choice not in cache_comparisons:
                cache_comparisons[choice] = {}
            cache_comparisons[choice][other_choice] = ind_won
            n_won_duels = branching.if_then_else(ind_won, n_won_duels + 1, n_won_duels)
        won_duels.append(n_won_duels)

    ind_smith_set = compute_most_votes(group, won_duels, len(tally))

    for _ in range(len(tally) - 1):
        for choice in range(len(tally)):
            for other_choice in range(len(tally)):
                if other_choice == choice:
                    continue
                ind_won = cache_comparisons[choice][other_choice]
                new_ind_smith_choice = bitgates.and_gate(group, [ind_smith_set[other_choice], ind_won])
                ind_smith_set[choice] = branching.if_then_else(new_ind_smith_choice, group.gen(1), ind_smith_set[choice])

    return ind_smith_set


def compute_majority_judgement(group: Group, tally: List[List[Wire]], n_votes: int, bits: int) -> Wire:
    """
    Computes the winner of a majority judgement election.

    :param group: The underlying group
    :type group: Group
    :param tally: The (aggregated) tally
    :type tally: List[List[Wire]]
    :param n_votes: The number of votes
    :type n_votes: int
    :type tally: List[List[Wire]]
    :param bits: The maximal number of bits of the values in the tally
    :type bits: int
    :return: Indicator for each choice whether it won
    :rtype: Wire
    """
    n_choices = len(tally)
    n_votes_halved = group.gen(n_votes // 2)
    median_grades = [listgates.get_median(group, agg_grades, bits) for agg_grades in tally]
    best_median = listgates.get_minimum_value(group, median_grades, bits)
    ind_winner = [comparison.eq(group, med_grade, best_median) for med_grade in median_grades]
    i_plus = group.gen(1)
    i_minus = group.gen(1)
    s = group.gen(1)
    ps = []
    qs = []
    ms_minus = []
    ms_plus = []
    ind_better_than_median_grade = listgates.get_list_with_up_to_index_set(group, best_median - 1, n_choices, bits)
    ind_worst_than_median_grade = [1-i for i in listgates.get_list_with_up_to_index_set(group, best_median, n_choices, bits)]
    for agg_grades in tally:
        ps.append(sum([i * v for i, v in zip(ind_better_than_median_grade, agg_grades)]))
        qs.append(sum([i * v for i, v in zip(ind_worst_than_median_grade, agg_grades)]))
        ms_minus.append(n_votes_halved - ps[-1])
        ms_plus.append(n_votes_halved - qs[-1])
    for _ in range(n_choices):
        # Assuming at least one choice is eliminated per round
        sis = []
        for i in range(n_choices):
            comp = comparison.lt(group, ms_minus[i], ms_plus[i], bits)
            si = ind_winner[i] * (branching.if_then_else(comp, ps[i], -qs[i]) + n_votes_halved)
            sis.append(si)
        s_max = listgates.get_maximum_value(group, sis, bits)
        ind_s_max_zero = comparison.eq_zero(group, s_max - n_votes_halved)
        ind_winner = [branching.if_then_else(ind, comparison.eq(group, sis[i], s_max), ind) for i, ind in enumerate(ind_winner)]
        ind_s_max_gt_zero = comparison.gt(group, s_max, n_votes_halved, bits)

        ms_plus_sgtzero = [mi_plus - mi_minus for mi_plus, mi_minus in zip(ms_plus, ms_minus)]
        ms_minus_sgtzero = [listgates.get_index_at(group, tally[i], best_median - i_minus) for i in range(n_choices)]
        ps_sgtzero = [ps[i] - ms_minus_sgtzero[i] for i in range(n_choices)]
        i_minus_sgtzero = i_minus + 1

        ms_minus_slzero = [mi_minus - mi_plus for mi_plus, mi_minus in zip(ms_plus, ms_minus)]
        ms_plus_slzero = [listgates.get_index_at(group, tally[i], best_median + i_plus) for i in range(n_choices)]
        qs_slzero = [qs[i] - ms_plus_slzero[i] for i in range(n_choices)]
        i_plus_sgtzero = i_plus + 1

        ms_plus = [branching.if_then_else(ind_s_max_gt_zero, ms_plus_sgtzero[i], ms_plus_slzero[i]) for i in range(n_choices)]
        ms_minus = [branching.if_then_else(ind_s_max_gt_zero, ms_minus_sgtzero[i], ms_minus_slzero[i]) for i in range(n_choices)]
        ps = [branching.if_then_else(ind_s_max_gt_zero, ps_sgtzero[i], ps[i]) for i in range(n_choices)]
        qs = [branching.if_then_else(ind_s_max_gt_zero, qs[i], qs_slzero[i]) for i in range(n_choices)]
        i_minus = branching.if_then_else(ind_s_max_gt_zero, i_minus_sgtzero, i_minus)
        i_plus = branching.if_then_else(ind_s_max_gt_zero, i_plus, i_plus_sgtzero)

    return ind_winner
