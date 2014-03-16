# -*- encoding: utf-8 -*-
import os


def show(expr, return_timing=False, **kwargs):
    r'''Shows `expr`.

    ..  container:: example

        **Example 1.** Shows a note:

        ::

            >>> note = Note("c'4")
            >>> show(note) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Shows a note and returns Abjad and LilyPond processing
        times in seconds.

        ::

            >>> note = Note("c'4")
            >>> show(note, return_timing=True) # doctest: +SKIP
            (0.0017380714416503906, 0.6541821956634521)

    Abjad writes LilyPond input files to the ``~/.abjad/output/``
    directory by default.

    You may change this by setting the ``abjad_output`` variable in
    the Abjad ``config.py`` file.

    Returns none when `return_timing` is false.
    
    Returns pair of `abjad_formatting_time` and `lilypond_rendering_time`
    when `return_timing` is true.
    '''
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    assert '__illustrate__' in dir(expr)
    result = topleveltools.persist(expr).as_pdf(**kwargs)
    pdf_file_path = result[0]
    abjad_formatting_time = result[1]
    lilypond_rendering_time = result[2]
    success = result[3]
    if success:
        systemtools.IOManager.open_file(pdf_file_path)
    if return_timing:
        return abjad_formatting_time, lilypond_rendering_time
