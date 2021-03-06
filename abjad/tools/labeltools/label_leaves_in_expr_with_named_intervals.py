# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools import pitchtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_named_intervals(expr, markup_direction=Up):
    r"""Label leaves in `expr` with named intervals:

    ::

        >>> notes = scoretools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)])
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_named_intervals(staff)

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            c'8 ^ \markup { +aug15 }
            cs'''8 ^ \markup { -M9 }
            b'8 ^ \markup { -aug9 }
            af8 ^ \markup { -m7 }
            bf,8 ^ \markup { +aug1 }
            b,8 ^ \markup { +m14 }
            a'8 ^ \markup { +m2 }
            bf'8 ^ \markup { -dim4 }
            fs'8 ^ \markup { -aug1 }
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    """

    for note in iterate(expr).by_class(scoretools.Note):
        logical_voice_iterator = iterate(note).by_logical_voice_from_component(
            scoretools.Leaf,
            )
        try:
            next(logical_voice_iterator)
            next_leaf = next(logical_voice_iterator)
            if isinstance(next_leaf, scoretools.Note):
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    note, next_leaf)
                markup = markuptools.Markup(mdi, markup_direction)
                attach(markup, note)
        except StopIteration:
            pass
