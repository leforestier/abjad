def score_to_timespan(score=None):
    r'''.. versionadded:: 1.0

    Change optional `score` to timespan::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.score_to_timespan()
        Timespan(ScoreSliceIndicator())

    Return timespan.
    '''
    from experimental import specificationtools
    
    # check input
    if score is None:
        score_name = None
    else:
        score_name = specificationtools.expr_to_score_name(score)

    # make score indicator
    score_indicator = specificationtools.ScoreSliceIndicator()

    # return timespan
    return score_indicator.timespan
