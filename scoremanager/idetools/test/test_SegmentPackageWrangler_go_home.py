# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_home_01():
    r'''From score segments to library.
    '''

    input_ = 'red~example~score g H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_home_02():
    r'''From all segments to library.
    '''

    input_ = 'G H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles