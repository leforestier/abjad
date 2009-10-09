from abjad import *


def test_pitchtools_ChromaticInterval___init___01( ):
   '''Init from positive number.'''

   i = pitchtools.ChromaticInterval(3)
   assert i._number == 3

def test_pitchtools_ChromaticInterval___init___02( ):
   '''Init from negative number.'''

   i = pitchtools.ChromaticInterval(-3)
   assert i._number == -3


def test_pitchtools_ChromaticInterval___init___03( ):
   '''Init from diatonic interval.'''

   diatonic_interval = pitchtools.DiatonicInterval('perfect', 4)
   i = pitchtools.ChromaticInterval(diatonic_interval)
   assert i._number == 5
