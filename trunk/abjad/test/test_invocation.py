from abjad import *


### TEST INIT TYPICAL INVOCATION ###

def test_init_typical_invocation_01( ):
   t = Staff([ ])
   assert repr(t.invocation) == '_Invocation(Staff)'
   assert t.format == '\\new Staff {\n}'

def test_init_typical_invocation_02( ):
   t = Staff([ ])
   t.invocation = 'Breath'
   assert repr(t.invocation) == '_Invocation(Breath)'
   assert t.format == '\\new Breath {\n}'

def test_init_typical_invocation_03( ):
   t = Staff([ ])
   t.invocation = 'Breath', 'flute'
   assert repr(t.invocation) == '_Invocation(Breath, flute)'
   assert t.format == '\\new Breath = flute {\n}'

def test_init_typical_invocation_04( ):
   t = Staff([ ])
   t.invocation = 'Breath', 'flute'
   t.invocation.modifications = [r"\override NoteHead #'transparent = ##t"]
   assert repr(t.invocation) == '_Invocation(Breath, flute, ["\\\\override NoteHead #\'transparent = ##t"])'
   assert t.format == "\\new Breath = flute \\with {\n\t\\override NoteHead #'transparent = ##t\n} {\n}"
