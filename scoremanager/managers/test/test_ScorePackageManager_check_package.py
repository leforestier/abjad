# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_check_package_01():

    input_ = 'red~example~score ck q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '6 of 6 required directories found:',
        '2 of 2 required files found:',
        '1 optional directory found:',
        ]
    for line in lines:
        assert line in contents


def test_ScorePackageManager_check_package_02():

    input_ = 'blue~example~score ck q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '6 of 6 required directories found:',
        '2 of 2 required files found:',
        '1 optional directory found:',
        '1 unrecognized file found:',
        ]
    for line in lines:
        assert line in contents