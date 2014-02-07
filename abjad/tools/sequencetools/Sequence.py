# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject


class Sequence(AbjadObject):
    r'''A sequence.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_elements',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        args = args or ()
        elements = tuple(args)
        self._elements = elements

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds `expr` to sequence.

        ..  container:: example

            ::

                >>> Sequence(1, 2, 3) + Sequence(4, 5, 6)
                Sequence(1, 2, 3, 4, 5, 6)

            ::

                >>> Sequence(1, 2, 3) + (4, 5, 6)
                Sequence(1, 2, 3, 4, 5, 6)

            ::

                >>> Sequence(1, 2, 3) + [4, 5, 6]
                Sequence(1, 2, 3, 4, 5, 6)

        Returns new sequence.
        '''
        expr = type(self)(*expr)
        elements = self._elements + expr._elements
        return type(self)(*elements)

    def __eq__(self, expr):
        r'''Is true when `expr` is a sequence with elements equal to those of
        this sequence.

        ..  container:: example

            ::

                >>> Sequence(1, 2, 3, 4, 5, 6) == Sequence(1, 2, 3, 4, 5, 6)
                True

        ..  container:: example

            Otherwise false:

            ::

                >>> Sequence(1, 2, 3, 4, 5, 6) == (1, 2, 3, 4, 5, 6)
                False

        '''
        if isinstance(expr, type(self)):
            return self._elements == expr._elements
        return False

    def __len__(self):
        r'''Gets length of sequence.

        Returns nonnegative integer.
        '''
        return len(self._elements)

    def __getitem__(self, i):
        r'''Gets item `i` from sequence.

        Returns item.
        '''
        return self._elements.__getitem__(i)

    def __getslice__(self, start, stop):
        r'''Gets slice from `start` to `stop`.

        Returns new sequence.
        '''
        result = self._elements.__getslice__(start, stop)
        result = type(self)(*result)
        return result

    def __radd__(self, expr):
        r'''Adds sequence to `expr`.

        ..  container:: example

            ::

                >>> Sequence(1, 2, 3) + Sequence(4, 5, 6)
                Sequence(1, 2, 3, 4, 5, 6)

            ::

                >>> (1, 2, 3) + Sequence(4, 5, 6)
                Sequence(1, 2, 3, 4, 5, 6)

            ::

                >>> [1, 2, 3] + Sequence(4, 5, 6)
                Sequence(1, 2, 3, 4, 5, 6)

        Returns new sequence.
        '''
        expr = type(self)(*expr)
        elements = expr._elements + self._elements
        return type(self)(*elements)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = tuple(self._elements)
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def degree_of_rotational_symmetry(self):
        '''Gets degree of rotational symmetry.

        ..  container:: example

            ::

                >>> Sequence(1, 2, 3, 4, 5, 6).degree_of_rotational_symmetry
                1

            ::

                >>> Sequence(1, 2, 3, 1, 2, 3).degree_of_rotational_symmetry
                2

            ::

                >>> Sequence(1, 2, 1, 2, 1, 2).degree_of_rotational_symmetry
                3

            ::

                >>> Sequence(1, 1, 1, 1, 1, 1).degree_of_rotational_symmetry
                6

        Returns positive integer.
        '''
        degree_of_rotational_symmetry = 0
        for index in range(len(self)):
            rotation = self[index:] + self[:index]
            if rotation == self:
                degree_of_rotational_symmetry += 1
        return degree_of_rotational_symmetry

    ### PUBLIC METHODS ###

    def get_period_of_rotation(self, n):
        '''Gets period of rotation.

        ..  container:: example

            ::

                >>> Sequence(1, 2, 3, 1, 2, 3).get_period_of_rotation(1)
                3

            ::

                >>> Sequence(1, 2, 3, 1, 2, 3).get_period_of_rotation(2)
                3

            ::

                >>> Sequence(1, 2, 3, 1, 2, 3).get_period_of_rotation(3)
                1

        Returns positive integer.
        '''
        degree = self.degree_of_rotational_symmetry
        period = len(self) / degree
        divisors_of_n = set(mathtools.divisors(n))
        divisors_of_period = set(mathtools.divisors(period))
        max_shared_divisor = max(divisors_of_n & divisors_of_period)
        return period / max_shared_divisor

    def is_decreasing(self, strict=True):
        r'''Is true when sequence decreases.

        ..  container:: example

            With ``strict=True``:

            ::

                >>> Sequence(5, 4, 3, 2, 1, 0).is_decreasing(strict=True)
                True

            ::

                >>> Sequence(3, 3, 3, 2, 1, 0).is_decreasing(strict=True)
                False

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_decreasing(strict=True)
                False

            ::

                >>> Sequence().is_decreasing(strict=True)
                True

        ..  container:: example

            With ``strict=False``:

            ::

                >>> Sequence(5, 4, 3, 2, 1, 0).is_decreasing(strict=False)
                True

            ::

                >>> Sequence(3, 3, 3, 2, 1, 0).is_decreasing(strict=False)
                True

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_decreasing(strict=False)
                True

            ::

                >>> Sequence().is_decreasing(strict=False)
                True

        Returns boolean.
        '''
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current < previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current <= previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_increasing(self, strict=True):
        r'''Is true when sequence increases.

        ..  container:: example

            With ``strict=True``:

            ::

                >>> Sequence(0, 1, 2, 3, 4, 5).is_increasing(strict=True)
                True

            ::

                >>> Sequence(0, 1, 2, 3, 3, 3).is_increasing(strict=True)
                False

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_increasing(strict=True)
                False

            ::

                >>> Sequence().is_increasing(strict=True)
                True

        ..  container:: example

            With ``strict=False``:

            ::

                >>> Sequence(0, 1, 2, 3, 4, 5).is_increasing(strict=False)
                True

            ::

                >>> Sequence(0, 1, 2, 3, 3, 3).is_increasing(strict=False)
                True

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_increasing(strict=False)
                True

            ::

                >>> Sequence().is_increasing(strict=False)
                True

        Returns boolean.
        '''
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous < current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous <= current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_permutation(self, length=None):
        '''Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            ::

                >>> Sequence(4, 5, 0, 3, 2, 1).is_permutation()
                True

        ..  container:: example

            Is false when sequence is not a permutation:

            ::

                >>> Sequence(1, 1, 5, 3, 2, 1).is_permutation()
                False

        Returns boolean.
        '''
        return sorted(self) == range(len(self))

    def is_repetition_free(self):
        '''Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence contains no repetitions:

            ::

                >>> Sequence(0, 1, 2, 6, 7, 8).is_repetition_free()
                True

            Is true when sequence is empty: 

            ::

                >>> Sequence().is_repetition_free()
                True

        ..  container:: example

            Is false when sequence contains repetitions:

            ::

                >>> Sequence(0, 1, 2, 2, 7, 8).is_repetition_free()
                False

        Returns boolean.
        '''
        from abjad.tools import sequencetools
        try:
            pairs = sequencetools.iterate_sequence_nwise(self)
            for left, right in pairs:
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    def is_restricted_growth_function(self):
        '''Is true when sequence is a restricted growth function.

        ..  container:: example

            Is true when sequence is a restricted growth function:

            ::

                >>> Sequence(1, 1, 1, 1).is_restricted_growth_function()
                True

            ::


                >>> Sequence(1, 1, 1, 2).is_restricted_growth_function()
                True

            ::

                >>> Sequence(1, 1, 2, 1).is_restricted_growth_function()
                True

            ::

                >>> Sequence(1, 1, 2, 2).is_restricted_growth_function()
                True

        ..  container:: example

            Is false when sequence is not a restricted growth function:
            
            ::

                >>> Sequence(1, 1, 1, 3).is_restricted_growth_function()
                False

            ::

                >>> Sequence(17).is_restricted_growth_function()
                False

        A restricted growth function is a sequence ``l`` such that 
        ``l[0] == 1`` and such that ``l[i] <= max(l[:i]) + 1`` for 
        ``1 <= i <= len(l)``.

        Returns boolean.
        '''
        try:
            for i, n in enumerate(self):
                if i == 0:
                    if not n == 1:
                        return False
                else:
                    if not n <= max(self[:i]) + 1:
                        return False
            return True
        except TypeError:
            return False
