from experimental.specificationtools.DivisionList import DivisionList


class SegmentDivisionList(DivisionList):
    '''Segment division list is a type of division list.

    Composers do not specify segment division lists; rather, 
    segment division lists arise during interpretation.

    Like other division lists, segment division lists are attributes of a voice.

    Segment division lists contrast with region division lists.
    The best way to show this is with an example::

        >>> from abjad.tools import *
        >>> from experimental.specificationtools import library
        >>> from experimental.specificationtools import ScoreSpecification

        >>> specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
        >>> segment = specification.append_segment()

        >>> segment.set_time_signatures(segment, [(4, 8), (3, 8)])
        Setting(Selection(contexts=['Grouped Rhythmic Staves Score'], timespan=Timespan(ScoreSliceIndicator(segment='1'))), 'time_signatures', [(4, 8), (3, 8)], persistent=True, truncate=False)

        >>> segment.set_divisions(segment.v1, [(3, 16)])
        Setting(Selection(contexts=['Voice 1'], timespan=Timespan(ScoreSliceIndicator(segment='1'))), 'divisions', [(3, 16)], persistent=True, truncate=False)

        >>> segment.set_rhythm(segment, library.thirty_seconds)
        Setting(Selection(contexts=['Grouped Rhythmic Staves Score'], timespan=Timespan(ScoreSliceIndicator(segment='1'))), 'rhythm', OutputBurnishedSignalFilledTimeTokenMaker('thirty_seconds'), persistent=True, truncate=False)

        >>> segment = specification.append_segment()
        >>> segment = specification.append_segment()

        >>> score = specification.interpret()

    After interpretation voice 1 has only one region division list::

        >>> for x in specification.payload_context_dictionary['Voice 1']['region_division_lists']: x
        ... 
        RegionDivisionList('[3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16]')

    But voice 1 has three segment division lists::

        >>> for x in specification.payload_context_dictionary['Voice 1']['segment_division_lists']: x
        ... 
        SegmentDivisionList('[3, 16], [3, 16], [3, 16], [3, 16], [2, 16)')
        SegmentDivisionList('(1, 16], [3, 16], [3, 16], [3, 16], [3, 16], [1, 16)')
        SegmentDivisionList('(2, 16], [3, 16], [3, 16], [3, 16], [3, 16]')

    After interpretation each voice carries exactly one segment division list per segment.
    
    (In this example voice 1 carries three segment division list because the score comprises three segments.)

    Segments division lists show the divisions belonging to a voice broken by score segment.

    The broken view that segment division lists provide will frequently be at odds with the
    unbroken divisions contained in the region division list belonging to a voice.
    '''

    pass
