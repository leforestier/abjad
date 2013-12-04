# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BaritoneSaxophone(Instrument):
    r'''A baritone saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP
        >>> baritone_sax = instrumenttools.BaritoneSaxophone()
        >>> attach(baritone_sax, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Baritone saxophone }
            \set Staff.shortInstrumentName = \markup { Bar. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The baritone saxophone targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='baritone saxophone',
        short_instrument_name='bar. sax.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='ef,',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-24, 8)
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])
        self._copy_default_starting_clefs_to_default_allowable_clefs()

#    ### PUBLIC PROPERTIES ###
#
#    @property
#    def sounding_pitch_of_written_middle_c(self):
#        r'''Gets and sets sounding pitch of written middle C.
#
#        ::
#
#            >>> baritone_sax.sounding_pitch_of_written_middle_c
#            NamedPitch('ef,')
#
#        ::
#
#            >>> baritone_sax.sounding_pitch_of_written_middle_c = 'e' 
#            >>> baritone_sax.sounding_pitch_of_written_middle_c
#            NamedPitch('e')
#
#        ::
#
#            >>> baritone_sax.sounding_pitch_of_written_middle_c = None
#            >>> baritone_sax.sounding_pitch_of_written_middle_c
#            NamedPitch('ef,')
#
#        Returns named pitch.
#        '''
#        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
#
#    @sounding_pitch_of_written_middle_c.setter
#    def sounding_pitch_of_written_middle_c(self, pitch):
#        Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
