from abjad import *
from abjad.tools.parenttools.switch import _switch


def test__switch_01( ):

   t = Voice([ ])
   u = Voice(scale(4))

   components = u[:]
   _switch(components, t)

   assert check(u)
   assert len(u) == 0

   "Container t now assigned to components."
   "But components not in container t."
   
   assert components[0].parentage.parent is t
   assert components[0] not in t

   t._music.extend(components)

   "Components now in container t."

   assert check(t)
   assert components[0].parentage.parent is t
   assert components[0] in t
