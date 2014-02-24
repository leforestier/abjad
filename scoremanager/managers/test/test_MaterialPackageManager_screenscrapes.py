# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageManager_screenscrapes_01():
    r'''Score material run from home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)

    assert score_manager._session.transcript.last_menu_lines == [
        'Red Example Score (2013) - materials - tempo inventory', 
        '', 
        '     output material - interact (omi)', 
        '     output material - view (omv)', 
        '', 
        '     Tempo(Duration(1, 8), 72)', 
        '     Tempo(Duration(1, 8), 108)', 
        '     Tempo(Duration(1, 8), 90)', 
        '     Tempo(Duration(1, 8), 135)', 
        '', 
        '     illustration builder - edit (ibe)', 
        '     illustration builder - execute (ibx)', 
        '     score stylesheet - select (sss)', 
        '', 
        '     output pdf - make (pdfm)', 
        '',
        ]
