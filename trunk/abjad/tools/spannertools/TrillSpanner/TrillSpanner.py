from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.TrillSpanner._TrillSpannerFormatInterface import _TrillSpannerFormatInterface


class TrillSpanner(Spanner):
   r'''Abjad trill spanner::

      abjad> t = Staff(macros.scale(4))
      abjad> spannertools.TrillSpanner(t[:])
      spannertools.TrillSpanner(c'8, d'8, e'8, f'8)
      abjad> print t.format
      \new Staff {
         c'8 \startTrillSpan
         d'8
         e'8
         f'8 \stopTrillSpan
      }

   Interface to LilyPond ``startTrillSpan``, ``stopTrillSpan`` commands.

   Handles LilyPond TrillSpanner grob.

   Return trill spanner.
   '''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _TrillSpannerFormatInterface(self)
      self._pitch = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def pitch( ):
      def fget(self):
         r'''Optional read / write pitch for pitched trills.
   
            ::

               abjad> t = Staff(macros.scale(4))
               abjad> trill = spannertools.TrillSpanner(t[:2])
               abjad> trill.pitch = pitchtools.NamedChromaticPitch('cs', 4)

            ::

               abjad> f(t)
               \new Staff {
                  \pitchedTrill c'8 \startTrillSpan cs'
                  d'8 \stopTrillSpan
                  e'8
                  f'8
               }
         '''
         return self._pitch
      def fset(self, expr):
         from abjad.tools import pitchtools
         if expr is None:
            self._pitch = expr
         else:
            pitch = pitchtools.NamedChromaticPitch(expr)
            self._pitch = pitch
      return property(**locals( ))
