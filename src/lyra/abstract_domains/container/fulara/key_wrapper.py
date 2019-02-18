from abc import ABCMeta, abstractmethod

from typing import Set, Optional

# (Class) Adapter pattern
from lyra.abstract_domains.state import EnvironmentMixin
from lyra.core.expressions import VariableIdentifier


class KeyWrapper(EnvironmentMixin, metaclass=ABCMeta):
    """
    (Abstract) wrapper around a domain with some extra functions,
    that are needed for the key state of a FularaState.
    A concrete wrapper should inherit from this class and the state that should be 'wrapped'.
    """

    def __init__(self, k_var: VariableIdentifier):
        """
        :param k_var: special variable (with correct type)
                      representing the key values at a specific segment
        """
        EnvironmentMixin.__init__(self)
        self._k_var = k_var

    @property
    def k_var(self) -> VariableIdentifier:
        """The special key variable of this abstraction"""
        return self._k_var

    @abstractmethod
    def is_singleton(self) -> bool:
        """
        Returns true if in the current state k_var represents a single concrete value.
        (needed for strong updates)
        """

    @abstractmethod
    def decomp(self, exclude: 'KeyWrapper') -> Optional[Set['KeyWrapper']]:
        """
        Computes a decomposition/partition of self into a set of rest states,
        excluding all parts that overlap (meet not bottom) with the 'exclude' state.
        i.e.: 'subtracts the meet of self & exclude from state'
        Needs to fulfil these conditions:
        - the meet of any two KeyWrappers from the returned set
            and the meet of 'exclude' with any KeyWrapper from the returned set must be bottom
        - the union of all concretizations of 'exclude' and every element in the returned set
            must be the same as the concretization of self
        (- 'exclude' is not in the return set)

        If a decomposition is not possible, the function should return None,
        but then no strong updates with partitioning are possible.
        Remember to return the empty set if self == 'exclude', which should always be possible

        :param exclude: parts to be excluded
        :return: decomposition/partition of 'state' avoiding 'exclude'
        """

    @abstractmethod
    def __lt__(self, other):
        """Used to order disjoint segements for their unique representation.
        Does not (need to) conform with Lattice's less_equal"""

    @abstractmethod
    def is_bottom(self) -> bool:
        """Should be true if the special key variable is bottom
        (i.e. if it cannot have any concrete value)"""
