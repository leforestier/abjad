from abjad import *


def test_instrumenttools_BassVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.BassVoice()

    assert voice._tools_package_qualified_indented_repr == 'instrumenttools.BassVoice()'
