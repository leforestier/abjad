from abc import ABCMeta
from abjad.tools.pitchtools._Counterpoint import _Counterpoint
from abjad.tools.pitchtools.IntervalObject import IntervalObject


class _CounterpointInterval(IntervalObject, _Counterpoint):
    '''..versionadded:: 2.0

    Counterpoint interval base class.
    '''
    __metaclass__ = ABCMeta

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        raise NotImplementedError
