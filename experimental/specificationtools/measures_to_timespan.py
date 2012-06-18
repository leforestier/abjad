def measures_to_timespan(start_measure, stop_measure=None):
    r'''.. versionadded:: 1.0

    Change `start_measure` number to timespan::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.measures_to_timespan(1)
        Timespan(ScoreSliceIndicator(klass=measuretools.Measure, index=1))

    Change `start_measure` number to `stop_measure` number to timespan::

        >>> specificationtools.measures_to_timespan(20, stop_measure=23)
        Timespan(start=Timepoint(anchor=ScoreSliceIndicator(klass=measuretools.Measure, index=20), edge=Left), stop=Timepoint(anchor=ScoreSliceIndicator(klass=measuretools.Measure, index=23), edge=Right))

    Measures are ``1``-indexed by convention.

    Return timespan.
    '''
    from abjad.tools import measuretools
    from experimental import specificationtools

    assert isinstance(start_measure, int), repr(start_measure)
    assert isinstance(stop_measure, (int, type(None))), repr(stop_measure)

    start_anchor = specificationtools.ScoreSliceIndicator(klass=measuretools.Measure, index=start_measure)
    start_timepoint = specificationtools.Timepoint(anchor=start_anchor, edge=Left)

    if stop_measure is None:
        stop_timepoint = specificationtools.Timepoint(anchor=start_anchor, edge=Right)
    else:
        stop_anchor = specificationtools.ScoreSliceIndicator(klass=measuretools.Measure, index=stop_measure)
        stop_timepoint = specificationtools.Timepoint(anchor=stop_anchor, edge=Right)

    return specificationtools.Timespan(start=start_timepoint, stop=stop_timepoint)
