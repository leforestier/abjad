from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.settingtools.CallbackMixin import CallbackMixin


class NonstartPositionedPayloadCallbackMixin(CallbackMixin):
    '''Nonstart-positioned payload callback mixin.
    '''
    
    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        callback = 'result = self.___and__(expr, {!r})'.format(timespan)
        return self._copy_and_append_callback(callback)

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    def __getitem__(self, expr):
        '''Return copy of expression with appended callback.
        '''
        callback = 'result = self.___getitem__(expr, {!r})'
        callback = callback.format(expr)
        return self._copy_and_append_callback(callback)

    ### PRIVATE METHODS ###

    def ___and__(self, expr, timespan):
        from experimental.tools import settingtools
        if hasattr(expr, '__and__'):
            result = expr & timespan
            assert isinstance(result, timespantools.TimespanInventory), repr(result)
            assert len(result) == 1, repr(result)
            result = result[0]
            return result
        else:
            if not sequencetools.all_are_numbers(expr):
                expr = [mathtools.NonreducedFraction(x) for x in expr]
            division_region_product = settingtools.DivisionRegionProduct(
                payload=expr, voice_name='dummy voice name', start_offset=durationtools.Offset(0))
            result = division_region_product & timespan
            result = result[0]
            divisions = result.payload.divisions
            return divisions

    def ___getitem__(self, expr, s):
        assert isinstance(s, slice)
        if hasattr(expr, '_getitem'):
            result = expr._getitem(s) 
            return result
        else:
            start_index, stop_index, stride = s.indices(len(expr))
            selected_expr = expr[s]
            return selected_expr

    def _apply_callbacks(self, expr):
        from experimental.tools import settingtools
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': settingtools.RotationIndicator,
            'Timespan': timespantools.Timespan,
            'expr': expr,
            'self': self,
            'result': None,
            'sequencetools': sequencetools,
            }
        for callback in self.callbacks:
            print callback
            assert 'expr' in callback
            evaluation_context['expr'] = expr
            exec(callback, evaluation_context)
            expr = evaluation_context['result']
        return expr

    def _duration_helper(self, expr):
        if hasattr(expr, 'duration'):
            return expr.duration
        elif hasattr(expr, 'prolated_duration'):
            return expr.prolated_duration
        else:
            duration = durationtools.Duration(expr)
            return duration

    def _partition_by_ratio(self, expr, ratio, part):
        if hasattr(expr, 'partition_by_ratio'):
            parts = expr.partition_by_ratio(ratio)
            selected_part = parts[part]
            return selected_part
        else:
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(expr, ratio)
            selected_part = parts[part]
            return selected_part

    def _partition_by_ratio_of_durations(self, expr, ratio, part):
        if hasattr(expr, 'partition_by_ratio_of_durations'):
            parts = expr.partition_by_ratio_of_durations(ratio)
            selected_part = parts[part]
            return selected_part
        else:
            element_durations = [self._duration_helper(x) for x in expr]
            element_tokens = durationtools.durations_to_integers(element_durations)
            token_parts = sequencetools.partition_sequence_by_ratio_of_weights(element_tokens, ratio)
            part_lengths = [len(x) for x in token_parts]
            duration_parts = sequencetools.partition_sequence_by_counts(element_durations, part_lengths)
            element_parts = sequencetools.partition_sequence_by_counts(expr, part_lengths)
            selected_part = element_parts[part]
            return selected_part

    def _reflect(self, expr):
        if hasattr(expr, 'reflect'):
            expr = expr.reflect() or expr
        elif expr.__class__.__name__ in ('tuple', 'list'):
            expr = type(expr)(reversed(expr))
        else:
            expr = expr.reverse() or expr
        return expr

    def _repeat_to_duration(self, expr, duration):
        if hasattr(expr, 'repeat_to_duration'):
            result = expr.repeat_to_duration(duration)
            return result
        else:
            if not sequencetools.all_are_numbers(expr):
                expr = [mathtools.NonreducedFraction(x) for x in expr]
            expr = sequencetools.repeat_sequence_to_weight_exactly(expr, duration)
            return expr

    def _repeat_to_length(self, expr, length):
        if hasattr(expr, 'repeat_to_length'):
            result = expr.repeat_to_length(length)
            return result
        else:
            expr = sequencetools.repeat_sequence_to_length(expr, length)
            return expr

    def _rotate(self, expr, n):
        if hasattr(expr, 'rotate'):
            expr.rotate(n)
        else:
            expr = sequencetools.rotate_sequence(expr, n)
        return expr

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Return tuple of newly constructed expressions with callbacks appended.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio(expr, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio_of_durations(expr, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def reflect(self):
        '''Return copy of expression with appended callback.
        '''
        callback = 'result = self._reflect(expr)'
        return self._copy_and_append_callback(callback)

    def repeat_to_duration(self, duration):
        '''Return copy of expression with appended callback.
        '''
        duration = durationtools.Duration(duration)
        callback = 'result = self._repeat_to_duration(expr, {!r})'.format(duration)
        return self._copy_and_append_callback(callback)

    def repeat_to_length(self, length):
        '''Return copy of expression with appended callback.
        '''
        assert mathtools.is_nonnegative_integer(length)
        callback = 'result = self._repeat_to_length(expr, {!r})'.format(length)
        return self._copy_and_append_callback(callback)

    def rotate(self, index):
        '''Return copy of expression with appended callback.
        '''
        from experimental.tools import settingtools
        assert isinstance(index, (int, durationtools.Duration, settingtools.RotationIndicator))
        callback = 'result = self._rotate(expr, {!r})'.format(index)    
        return self._copy_and_append_callback(callback)
