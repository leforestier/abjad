from abjad.tools import rhythmmakertools
from experimental import *


def test_RestRhythmMakerEditor_run_01():

    editor = scoremanagertools.editors.RestRhythmMakerEditor()
    editor._run(pending_user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.RestRhythmMaker()

    assert editor.target == maker
