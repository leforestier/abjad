# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_NaturalHarmonic___init___01():
    r'''Init natural harmonic from note.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    natural_harmonic = scoretools.NaturalHarmonic(staff[1])
    staff[1:2] = [natural_harmonic]

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8
            \once \override NoteHead #'style = #'harmonic
            d'8
            e'8
            f'8
        }
        '''
        )
