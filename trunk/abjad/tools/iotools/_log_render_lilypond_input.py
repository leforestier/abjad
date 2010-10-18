from abjad.cfg._read_config_file import _read_config_file
from abjad.components._Context import _Context
from abjad.tools import lilyfiletools
from abjad.tools.iotools._insert_expr_into_lily_file import _insert_expr_into_lily_file
from abjad.tools.iotools._run_lilypond import _run_lilypond
from abjad.tools.iotools._verify_output_directory import _verify_output_directory
from abjad.tools.iotools.get_next_output_file_name import get_next_output_file_name
import os
import time


def _log_render_lilypond_input(expr, template = None):
   '''Private function that stores both .ly and .pdf files in the
   ``abjad_output`` directory. 

   .. versionadded:: 1.1.2
      New format_time keyword to message conditionally output
      Abjad format time of `expr`.

   .. versionchanged:: 1.1.2
      Returns triple of name of file created, Abjad format time,
      LilyPond render time.
   '''

   lily_time = 10
   format_time = 10

   ## log score
   current_directory = os.path.abspath('.')
   ABJADOUTPUT = _read_config_file( )['abjad_output']
   _verify_output_directory(ABJADOUTPUT)
   os.chdir(ABJADOUTPUT)
   name = get_next_output_file_name( )
   outfile = open(name, 'w')

   ## catch Abjad tight loops that result in excessive format time
   start_format_time = time.time( )
   lily_file = _insert_expr_into_lily_file(expr, template = template)
   formatted_lily_file = lily_file.format
   stop_format_time = time.time( )
   actual_format_time = int(stop_format_time - start_format_time)
   if format_time <= actual_format_time:
      print 'Abjad format time equal to %s sec.' % actual_format_time
   outfile.write(formatted_lily_file)
   outfile.close( )

   if getattr(lily_file, '_is_temporary', False):
      ## TODO: eliminate this exception handler? ##
      try:
         music = lily_file.score_block.pop( )
         delattr(music, '_lily_file')
      except (IndexError, AttributeError):
         pass
      del(lily_file)

   ## render
   start_time = time.time( )
   _run_lilypond(name, _read_config_file( )['lilypond_path'])
   stop_time = time.time( )
   actual_lily_time = int(stop_time - start_time)

   os.chdir(current_directory)

   ## catch LilyPond taking a long time to render
   if lily_time <= actual_lily_time:
      print 'LilyPond processing time equal to %s sec.' % actual_lily_time

   return name, actual_format_time, actual_lily_time
