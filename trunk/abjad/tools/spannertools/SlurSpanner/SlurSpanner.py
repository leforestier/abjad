from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.SlurSpanner._SlurSpannerFormatInterface import \
   _SlurSpannerFormatInterface


class SlurSpanner(Spanner):
   '''Abjad slur spanner.

   Return slur spanner.
   '''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _SlurSpannerFormatInterface(self)
