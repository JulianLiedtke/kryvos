"""
Contains evaluation functions for Instant-Runoff voting (IRV).
"""
import itertools
from typing import Dict, List

import src.gates.bits as bitgates
import src.gates.branching as branching
import src.gates.comparison as comparison
import src.gates.listgates as listgates
from src.groups.group import Group
from src.groups.wiregroup import Wire


class IRVBallotManager():

    CHOICE_SEPARATOR_STR = '-'

    @classmethod
    def create(cls, n_choices: int, group: Group) -> 'IRVBallotManager':
        mapping = IRVBallotManager(n_choices)
        mapping.init_mapping(group)
        return mapping

    def __init__(self, n_choices: int) -> 'IRVBallotManager':
        self.n_choices = n_choices
        self.mapping: Dict[List[int], Wire] = {}

    def init_mapping(self, group: Group):
        self.mapping = {}
        for i in range(self.n_choices+1, 0, -1):
            for perm in itertools.permutations(range(self.n_choices), i):
                self.mapping[self._map_ballot_to_str(perm)] = group.gen(0)
        self.mapping[self._map_ballot_to_str([])] = group.gen(0)

    def add_votes_for_ordering(self, ordering: List[int], n_votes: Wire) -> None:
        ordering_str = self._map_ballot_to_str(ordering)
        self.mapping[ordering_str] += n_votes

    def _map_ballot_to_str(self, ballot: List[int]) -> str:
        return IRVBallotManager.CHOICE_SEPARATOR_STR.join([str(v) for v in ballot])

    def _map_str_to_ballot(self, ballot_str: str) -> List[int]:
        if ballot_str == '':
            return []
        return [int(i) for i in ballot_str.split(IRVBallotManager.CHOICE_SEPARATOR_STR)]

    def get_votes_per_choice(self) -> List[Wire]:
        votes_per_choice = []
        for possible_choice in range(self.n_choices):
            votes_per_choice.append(self.get_n_ballots_with_first_choice(possible_choice))
        return votes_per_choice

    def get_n_ballots_with_first_choice(self, first_choice: int) -> List[str]:
        n_ballots = None
        for key in self.mapping.keys():
            ballot_list = self._map_str_to_ballot(key)
            if len(ballot_list) == 0:
                continue
            if ballot_list[0] == first_choice:
                if n_ballots is None:
                    n_ballots = self.mapping[key]
                else:
                    n_ballots += self.mapping[key]
        return n_ballots

    def update_votes_on_elimination(self, inds_elim: Dict[int, Wire]) -> None:
        for ballot_str in self.mapping.keys():
            ballot_list = self._map_str_to_ballot(ballot_str)
            for pos_choice in range(self.n_choices):
                if pos_choice in ballot_list:
                    continue
                previous_ballot = [pos_choice] + [i for i in ballot_list]
                previous_ballot_str = self._map_ballot_to_str(previous_ballot)
                if not previous_ballot_str in self.mapping.keys():
                    continue
                self.mapping[ballot_str] += inds_elim[pos_choice] * self.mapping[previous_ballot_str]


class ChoiceEliminator():
    """
    Abstract class for elimination of choices.

    :param group: The underlying group.
    :type group: Group
    :param bits: Maximum bit size of the number of ballots per choice.
    :type bits: int
    """

    def __init__(self, group: Group, bits: int):
        self.group = group
        self.bits = bits

    def eliminate_choice(self, round: int, ind_elim: List[Wire], votes_per_choice: List[Wire]) -> List[Wire]:
        """
        Compute the choice that is eliminated in the current round.

        :param round: Number of current round
        :type round: int
        :param ind_elim: Indicator for each choice whether it is
            already eliminated (1: eliminated, 0: not yet eliminated).
        :type ind_elim: List[Wire]
        :param votes_per_choice: Contains for each choice the number
            of votes this choice currently has.
        :type votes_per_choice: List[Wire]
        :return: Returns an indicator per choice whether this choice
            gets eliminated in the current round.
        :rtype: List[Wire]
        """
        ind_min = self.compute_min(ind_elim, votes_per_choice)
        ind = self.break_ties(ind_min, votes_per_choice)
        return ind

    def compute_min(self, ind_elim: List[Wire], votes_per_choice: List[Wire]) -> List[Wire]:
        """
        Computes for each entry an indicator that is set if the
        candidate is not already eliminated and received the minimum
        number of votes (compared to all choices which are not already
        eliminated).

        :param ind_elim: Indicator for each choice whether it is
            already eliminated (1: eliminated, 0: not yet eliminated).
        :type ind_elim: List[Wire]
        :param votes_per_choice: Contains for each choice the number
            of votes this choice currently has.
        :type votes_per_choice: List[Wire]
        :return: For each entry an indicator that is set if the
            candidate is not already eliminated and received the
            minimum number of votes (compared to all choices which are
            not already eliminated).
        :rtype: List[Wire]
        """
        votes = [n_votes * (1 - elim) - elim for n_votes, elim in zip(votes_per_choice, ind_elim)]
        return listgates.minimum(self.group, votes, self.bits)

    def break_ties(self, ind_min: List[Wire], votes_per_choice: List[Wire]) -> List[Wire]:
        """
        Breaks ties between choices. This function need to be
        overwritten by subclasses.

        :param ind_min: Indicator whether the choice is included in
            the tie (1: tie, 0: not included).
        :type ind_min: List[Wire]
        :param votes_per_choice: Contains for each choice the number
            of votes this choice currently has.
        :type votes_per_choice: List[Wire]
        :return: Indicator for each choice whether it is eliminated
            (1: eliminated, 0: not yet eliminated).
        :rtype: List[Wire]
        """
        pass


class EliminateFirstPossibilityEliminator(ChoiceEliminator):
    """
    Always elimates the first choice in the list that is not already
    eliminated.
    """

    def break_ties(self, ind_min: List[Wire], votes_per_choice: List[Wire]) -> List[Wire]:
        return listgates.find_first_indicator(self.group, ind_min)


class NSWEliminator(ChoiceEliminator):
    """
    Eliminator for New South Wales (NSW) IRV.

    :param group: The underlying group.
    :type group: Group
    :param bits: Maximum bit size of the number of ballots per choice.
    :type bits: int
    :param randomness_per_round: List of randomness. For each round,
        paarwise different random values for each choice
    :type randomness_per_round: List[List[int]]
    """

    def __init__(self, group: Group, bits: int, randomness_per_round: List[List[int]]):
        super().__init__(group, bits)
        self.randomness_per_round: List[List[int]] = randomness_per_round
        self.votes_per_round: List[List[Wire]] = []
        self.current_round: int = 0

    def break_ties(self, ind_min: List[Wire], votes_per_choice: List[Wire]) -> List[Wire]:
        done = self.group.gen(0)
        res = [self.group.gen(0) for _ in ind_min]

        for votes in itertools.chain(reversed(self.votes_per_round), [self.randomness_per_round[self.current_round]]):
            min_ind, n_mins = listgates.find_and_count_min_of_set_inds(self.group, votes, ind_min, self.bits)
            ind_one_min = comparison.eq_zero(self.group, n_mins - 1)
            ind_set_res = bitgates.and_gate(self.group, [ind_one_min, 1 - done])
            done = ind_set_res
            res = [branching.if_then_else(ind_set_res, min_ind_i, res_i) for min_ind_i, res_i in zip(min_ind, res)]

        self.votes_per_round.append(votes_per_choice)
        return res


class IRV():
    """
    Represents an IRV election.
    """

    def __init__(self, n_choices: int, choice_eliminator: ChoiceEliminator, group: Group) -> 'IRV':
        self.n_choices = n_choices
        self.group = group
        self.choice_eliminator = choice_eliminator
        self.ballotmanager: IRVBallotManager = None
        self.ind_eliminated: List[Wire] = None
        self.round: int = 0

    def get_empty_ballots(self) -> IRVBallotManager:
        """
        Returns an IRVBallotManager with all possible ballots.

        :return: IRVBallotManager containing all possible ballots.
        :rtype: IRVBallotManager
        """
        return IRVBallotManager.create(self.n_choices, self.group)

    def evaluate_election(self, ballotmanager: IRVBallotManager, n_rounds: int = None) -> List[Wire]:
        """
        Evaluates an Instant-Runoff voting (IRV).

        :param ballotmanager: A manager of the ballots of the
            election.
        :type ballotmanager: IRVBallotManager
        :param n_rounds: Specifies how many rounds are evaluated (and
            thus how many choices are eliminated), defaults to None,
            which means that all except for one choice will be
            eliminated.
        :type n_rounds: int, optional
        :return: A list where each choice has an indicator with value
            0 if the choice was not eliminated and 1 if the choice was
            eliminated.
        :rtype: List[Wire]
        """
        self.round = 0
        self.ind_eliminated = self.group.gen_list([0 for _ in range(self.n_choices)])
        self.ballotmanager = ballotmanager
        if n_rounds is None:
            n_rounds = self.n_choices - 1
        for _ in range(n_rounds):
            self.evaluate_round()
            self.round += 1
        return self.ind_eliminated

    def evaluate_round(self):
        votes_per_choice = self.ballotmanager.get_votes_per_choice()
        inds_elim = self.choice_eliminator.eliminate_choice(self.round, self.ind_eliminated, votes_per_choice)
        for i in range(self.n_choices):
            self.ind_eliminated[i] += inds_elim[i]
        self.ballotmanager.update_votes_on_elimination(inds_elim)
