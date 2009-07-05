from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.log_render_lilypond_input import _log_render_lilypond_input
from abjad.cfg.open_file import _open_file
from abjad.cfg.read_config_value import _read_config_value
import os


def show(expr, template = None, title = None, footer = None, lilytime = 10):
   '''Format `expr` as a valid string of LilyPond input.

   Call LilyPond on the formatted version of `expr`.

   Open the PDF that LilyPond creates.

   Render `t` and open the resulting PDF::

      abjad> t = Note(0, (1, 4))
      abjad> show(t)

   Render `t` with the ``tangiers.ly`` template and then 
   open the resulting PDF::

      abjad> show(t, template = 'tangiers')

   Render `t` with a score title and open the resulting PDF::

      abjad> show(t, title = 'Score Title')

   Render `t` with a multiline score title and open the resulting PDF::

      abjad> show(t, title = ['Score Title', 'score subtitle', 'more subtitle'])

   .. versionadded:: 1.1.1
      Render `t` with a footer and open the resulting PDF:

   ::

      abjad> show(t, footer = '"This is footer text."')

   Render `t` and open the resulting PDF. Alert the composer
   if LilyPond takes greater than 60 seconds to render::

      abjad> show(t, lilytime = 60)

   .. note:: Abjad writes to the ``~/.abjad/output`` directory by default. \
      If the directory does not exist, Abjad writes to ``$ABJADOUTPUT``.
   '''

   name = _log_render_lilypond_input(expr, template = template, 
      title = title, footer = footer, lilytime = lilytime)
   pdfviewer = _read_config_value('pdfviewer')
   name = os.path.join(ABJADOUTPUT, name)
   _open_file('%s.pdf' % name[:-3], pdfviewer)
