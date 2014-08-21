# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class BurnishSpecifier(AbjadValueObject):
    r'''Burnish specifier.

    ..  container:: example

        Forces first leaf of each division to be a rest:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=[-1],
            ...     left_lengths=[1],
            ...     )

    ..  container:: example

        Forces the first three leaves of each division to be rests:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=[-1],
            ...     left_lengths=[3],
            ...     )

    ..  container:: example

        Forces last leaf of each division to be a rest:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=[-1],
            ...     right_lengths=[1],
            ...     )

    ..  container:: example

        Forces the last three leaves of each division to be rests:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=[-1],
            ...     right_lengths=[3],
            ...     )

    ..  container:: example

        Forces the first leaf of every even-numbered division to be a rest;
        forces the first leaf of every odd-numbered division to be a note.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=[-1, 1],
            ...     left_lengths=[1],
            ...     )

    ..  container:: example

        Forces the last leaf of every even-numbered division to be a rest;
        forces the last leaf of every odd-numbered division to be a note.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=[-1, 1],
            ...     right_lengths=[1],
            ...     )

    ..  container:: example

        Forces the first leaf of every even-numbered division to be a rest;
        leave the first leaf of every odd-numbered division unchanged.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=[-1, 0],
            ...     left_lengths=[1],
            ...     )

    ..  container:: example

        Forces the last leaf of every even-numbered division to be a rest;
        leave the last leaf of every odd-numbered division unchanged.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=[-1, 0],
            ...     right_lengths=[1],
            ...     )

    Burnish specifiers are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_burnish_each_division',
        '_burnish_output',
        '_left_lengths',
        '_lefts',
        '_middles',
        '_right_lengths',
        '_rights',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        burnish_each_division=False,
        burnish_output=False,
        lefts=None,
        middles=None,
        rights=None,
        left_lengths=None,
        right_lengths=None,
        ):
        assert isinstance(burnish_each_division, bool)
        assert isinstance(burnish_output, bool)
        assert not (burnish_each_division and burnish_output)
        self._burnish_each_division = burnish_each_division
        self._burnish_output = burnish_output
        lefts = self._to_tuple(lefts)
        middles = self._to_tuple(middles)
        rights = self._to_tuple(rights)
        left_lengths = self._to_tuple(left_lengths)
        right_lengths = self._to_tuple(right_lengths)
        assert self._is_sign_tuple(lefts)
        assert self._is_sign_tuple(middles)
        assert self._is_sign_tuple(rights)
        assert self._is_length_tuple(left_lengths)
        assert self._is_length_tuple(right_lengths)
        self._lefts = lefts
        self._middles = middles
        self._rights = rights
        self._left_lengths = left_lengths
        self._right_lengths = right_lengths

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a burnish specifier with input parameters
        equal to those of this burnish specifier. Otherwise false.

        ..  container:: example

            ::

                >>> burnish_specifier_1 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     left_lengths=[1],
                ... )
                >>> burnish_specifier_2 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     left_lengths=[1],
                ... )
                >>> burnish_specifier_3 = rhythmmakertools.BurnishSpecifier()

            ::

                >>> burnish_specifier_1 == burnish_specifier_1
                True
                >>> burnish_specifier_1 == burnish_specifier_2
                True
                >>> burnish_specifier_1 == burnish_specifier_3
                False
                >>> burnish_specifier_2 == burnish_specifier_1
                True
                >>> burnish_specifier_2 == burnish_specifier_2
                True
                >>> burnish_specifier_2 == burnish_specifier_3
                False
                >>> burnish_specifier_3 == burnish_specifier_1
                False
                >>> burnish_specifier_3 == burnish_specifier_2
                False
                >>> burnish_specifier_3 == burnish_specifier_3
                True

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     burnish_output=True,
                ...     lefts=[-1, 0],
                ...     left_lengths=[1],
                ...     )

            ::

                >>> print(format(burnish_specifier))
                rhythmmakertools.BurnishSpecifier(
                    burnish_output=True,
                    lefts=(-1, 0),
                    left_lengths=(1,),
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __hash__(self):
        r'''Hashes burnish specifier.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(BurnishSpecifier, self).__hash__()

    def __ne__(self, expr):
        r'''Is true when `expr` does not equal burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier_1 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     left_lengths=[1],
                ... )
                >>> burnish_specifier_2 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     left_lengths=[1],
                ... )
                >>> burnish_specifier_3 = rhythmmakertools.BurnishSpecifier()

            ::

                >>> burnish_specifier_1 != burnish_specifier_1
                False
                >>> burnish_specifier_1 != burnish_specifier_2
                False
                >>> burnish_specifier_1 != burnish_specifier_3
                True
                >>> burnish_specifier_2 != burnish_specifier_1
                False
                >>> burnish_specifier_2 != burnish_specifier_2
                False
                >>> burnish_specifier_2 != burnish_specifier_3
                True
                >>> burnish_specifier_3 != burnish_specifier_1
                True
                >>> burnish_specifier_3 != burnish_specifier_2
                True
                >>> burnish_specifier_3 != burnish_specifier_3
                False

        Returns boolean.
        '''
        return AbjadValueObject.__ne__(self, expr)

    def __repr__(self):
        r'''Gets interpreter representation of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     left_lengths=[1],
                ...     )

            ::

                >>> burnish_specifier
                BurnishSpecifier(lefts=(-1, 0), left_lengths=(1,))

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='burnish_each_division',
                command='bd',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='burnish_output',
                command='bo',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='lefts',
                command='l',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='middles',
                command='m',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='rights',
                command='r',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='left_lengths',
                command='ll',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='right_lengths',
                command='rl',
                editor=idetools.getters.get_integers,
                ),
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        if self.burnish_each_division == False:
            keyword_argument_names.remove('burnish_each_division')
        if self.burnish_output == False:
            keyword_argument_names.remove('burnish_output')
        if not self.lefts:
            keyword_argument_names.remove('lefts')
        if not self.middles:
            keyword_argument_names.remove('middles')
        if not self.rights:
            keyword_argument_names.remove('rights')
        if not self.left_lengths:
            keyword_argument_names.remove('left_lengths')
        if not self.right_lengths:
            keyword_argument_names.remove('right_lengths')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_length_tuple(expr):
        if expr is None:
            return True
        if mathtools.all_are_nonnegative_integer_equivalent_numbers(expr):
            if isinstance(expr, tuple):
                return True
        return False

    @staticmethod
    def _is_sign_tuple(expr):
        if expr is None:
            return True
        if isinstance(expr, tuple):
            return all(x in (-1, 0, 1) for x in expr)
        return False

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def burnish_each_division(self):
        r'''Is true when rhythm-maker should burnish each division in output.
        Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._burnish_each_division

    @property
    def burnish_output(self):
        r'''Is true when rhythm-maker should burnish first and last division
        in output. Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._burnish_output

    @property
    def left_lengths(self):
        r'''Gets left lengths of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1],
                ...     )

            ::

                >>> burnish_specifier.left_lengths
                (2,)

        Returns tuple or none.
        '''
        return self._left_lengths

    @property
    def lefts(self):
        r'''Gets lefts of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1],
                ...     )

            ::

                >>> burnish_specifier.lefts
                (-1, 0)

        Returns tuple or none.
        '''
        return self._lefts

    @property
    def middles(self):
        r'''Gets middles of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1],
                ...     )

            ::

                >>> burnish_specifier.middles
                (0,)

        Returns tuple or none.
        '''
        return self._middles

    @property
    def right_lengths(self):
        r'''Gets right lengths of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1],
                ...     )

            ::

                >>> burnish_specifier.right_lengths
                (1,)

        Returns tuple or none.
        '''
        return self._right_lengths

    @property
    def rights(self):
        r'''Gets rights of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1],
                ...     )

            ::

                >>> burnish_specifier.rights
                (-1, -1, 0)

        Returns tuple or none.
        '''
        return self._rights

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses burnish specification.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     burnish_each_division=True,
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1],
                ...     )

            ::

                >>> print(format(burnish_specifier.reverse()))
                rhythmmakertools.BurnishSpecifier(
                    burnish_each_division=True,
                    lefts=(0, -1),
                    middles=(0,),
                    rights=(0, -1, -1),
                    left_lengths=(2,),
                    right_lengths=(1,),
                    )

        Returns new burnish specification.
        '''
        from abjad.tools import rhythmmakertools
        lefts = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.lefts)
        middles = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.middles)
        rights = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.rights)
        left_lengths = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.left_lengths)
        right_lengths = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.right_lengths)
        result = new(
            self,
            lefts=lefts,
            middles=middles,
            rights=rights,
            left_lengths=left_lengths,
            right_lengths=right_lengths,
            )
        return result

    def rotate(self, n=0):
        r'''Rotates burnish specification.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     burnish_each_division=True,
                ...     lefts=[-1, 0],
                ...     middles=[0],
                ...     rights=[-1, -1, 0],
                ...     left_lengths=[2],
                ...     right_lengths=[1, 2, 3],
                ...     )

            ::

                >>> print(format(burnish_specifier.rotate(1)))
                rhythmmakertools.BurnishSpecifier(
                    burnish_each_division=True,
                    lefts=(0, -1),
                    middles=(0,),
                    rights=(0, -1, -1),
                    left_lengths=(2,),
                    right_lengths=(3, 1, 2),
                    )

        Returns new burnish specification.
        '''
        from abjad.tools import rhythmmakertools
        lefts = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.lefts, n)
        middles = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.middles, n)
        rights = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.rights, n)
        left_lengths = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.left_lengths, n)
        right_lengths = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.right_lengths, n)
        return new(
            self,
            lefts=lefts,
            middles=middles,
            rights=rights,
            left_lengths=left_lengths,
            right_lengths=right_lengths,
            )