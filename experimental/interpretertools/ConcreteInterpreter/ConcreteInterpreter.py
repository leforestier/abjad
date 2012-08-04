from abjad.tools import *
from experimental import divisiontools
from experimental import helpertools
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import timespantools
from experimental.interpretertools.Interpreter import Interpreter
import copy


class ConcreteInterpreter(Interpreter):
    r'''.. versionadded:: 1.0

    Concrete interpreter.

    Currently the only interpreter implemented.

    The ``'concrete'`` designation is provisional.
    '''

    ### INITIALIZER ###

    def __call__(self, score_specification):
        '''Top-level interpretation entry point::

            * interpret time signatures
            * interpret divisions
            * interpret rhythms
            * interpret pitch-classes
            * interpret registration
            * interpret additional parameters

        Return Abjad score object.
        '''
        self.score_specification = score_specification
        self.score = self.instantiate_score()
        self.unpack_multiple_context_settings_for_score()
        self.store_single_context_time_signature_settings()
        self.add_time_signatures_to_score()
        self.calculate_segment_offset_pairs()
        self.store_single_context_division_settings()
        self.add_division_lists_to_score()
        self.store_single_context_rhythm_settings()
        self.add_rhythms_to_score()
        self.store_single_context_pitch_class_settings()
        self.apply_pitch_classes()
        self.store_single_context_registration_settings()
        self.apply_registration()
        self.store_additional_single_context_settings()
        self.apply_additional_parameters()
        return self.score

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def add_division_lists_to_score(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_division_lists_to_voice(voice)

    def add_division_lists_to_voice(self, voice):
        #self._debug(voice)
        division_region_division_lists = self.make_division_region_division_lists_for_voice(voice)
        #self._debug(division_region_division_lists, 'drdl')
        if division_region_division_lists:
            self.score_specification.contexts[voice.name]['division_region_division_lists'] = \
                division_region_division_lists
            voice_division_list = self.make_voice_division_list_for_voice(voice)
            self.score_specification.contexts[voice.name]['voice_division_list'] = voice_division_list
            segment_division_lists = self.make_segment_division_lists_for_voice(voice)
            self.score_specification.contexts[voice.name]['segment_division_lists'] = segment_division_lists
            self.add_segment_division_lists_to_voice(
                voice, segment_division_lists)
            #self._debug(voice_division_list, 'vdl')
            #self._debug(segment_division_lists, 'sdl')

    def add_rhythm_to_voice(self, voice, rhythm_maker, rhythm_region_division_list):
#        self._debug(rhythm_maker)
#        self._debug(rhythm_region_division_list)
        assert isinstance(rhythm_maker, timetokentools.TimeTokenMaker), repr(rhythm_maker)
        assert isinstance(rhythm_region_division_list, divisiontools.RhythmRegionDivisionList)
        leaf_lists = rhythm_maker(rhythm_region_division_list.pairs)
        rhythm_containers = [containertools.Container(x) for x in leaf_lists]
        voice.extend(rhythm_containers)
        self.conditionally_beam_rhythm_containers(rhythm_maker, rhythm_containers)

    def add_rhythms_to_score(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_rhythms_to_voice(voice)

    def add_rhythms_to_voice(self, voice):
        from experimental import specificationtools
        voice_division_list = self.get_voice_division_list(voice)
        if len(voice_division_list) == 0:
            return
        voice_divisions = voice_division_list.divisions
        voice_division_durations = [durationtools.Duration(x) for x in voice_divisions]
        rhythm_commands = self.get_rhythm_commands_for_voice(voice)
        rhythm_commands = self.fuse_like_rhythm_commands(rhythm_commands)
        rhythm_command_durations = [x.duration for x in rhythm_commands]
        division_region_division_lists = self.score_specification.contexts[voice.name][
            'division_region_division_lists']
        #self._debug(division_region_division_lists)
        division_region_durations = [x.duration for x in division_region_division_lists]
        #self._debug(division_region_durations)
        #self._debug(rhythm_command_durations)
        rhythm_region_durations = sequencetools.merge_duration_sequences(
            division_region_durations, rhythm_command_durations)
        args = (voice_division_durations, rhythm_region_durations)
        rhythm_region_division_duration_lists = sequencetools.partition_sequence_by_backgrounded_weights(*args)
        assert len(rhythm_region_division_duration_lists) == len(rhythm_region_durations)
        rhythm_region_lengths = [len(l) for l in rhythm_region_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_once_by_counts_without_overhang(
            voice_divisions, rhythm_region_lengths)
        assert len(rhythm_region_division_lists) == len(rhythm_region_durations)
        input_pairs = [(command.resolved_value, command.duration) for command in rhythm_commands]
        output_pairs = sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            rhythm_region_durations, input_pairs)
        rhythm_makers = [output_pair[-1] for output_pair in output_pairs]
        assert len(rhythm_makers) == len(rhythm_region_division_lists)
        self.make_rhythms_and_add_to_voice(voice, rhythm_makers, rhythm_region_division_lists)

    def add_segment_division_lists_to_voice(
        self, voice, segment_division_lists):
        assert len(self.score_specification.segment_specifications) == len(segment_division_lists)
        for segment_specification, segment_division_list in zip(
            self.score_specification.segment_specifications, segment_division_lists):
            segment_specification.contexts[voice.name]['segment_division_list'] = segment_division_list
            segment_specification.contexts[voice.name]['segment_pairs'] = [
                x.pair for x in segment_division_list]

    def add_time_signatures_for_segment(self, segment_specification):
        time_signatures = segment_specification.time_signatures
        if time_signatures is not None:
            measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
            context = componenttools.get_first_component_in_expr_with_name(self.score, 'TimeSignatureContext')
            context.extend(measures)

    def add_time_signatures_to_score(self):
        for segment_specification in self.score_specification.segment_specifications:
            self.add_time_signatures_for_segment(segment_specification)

    def apply_additional_parameters(self):
        pass

    def apply_pitch_classes(self):
        pass

    def apply_registration(self):
        pass

    def attribute_request_to_resolved_single_context_setting(self, attribute_request):
        segment_specification = self.get_segment_specification(attribute_request.segment_name)
        context_proxy = segment_specification.resolved_single_context_settings[attribute_request.context_name]
        resolved_single_context_setting = context_proxy.get_setting(attribute=attribute_request.attribute)
        return resolved_single_context_setting

    def calculate_segment_offset_pairs(self):
        '''Set ``'segment_durations'`` property on score specification.

        Set ``'score_duration'`` property on score specification.

        Set ``'segment_offset_pairs'`` property on score specification.
        '''
        segment_durations = [x.duration for x in self.score_specification.segment_specifications]
        if sequencetools.all_are_numbers(segment_durations):
            self.score_specification.segment_durations = segment_durations
            self.score_specification.score_duration = sum(self.score_specification.segment_durations)
            segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(
                self.score_specification.segment_durations)
            segment_offset_pairs = [
                (durationtools.Offset(x[0]), durationtools.Offset(x[1])) for x in segment_offset_pairs]
            self.score_specification.segment_offset_pairs = segment_offset_pairs

    def clear_persistent_resolved_single_context_settings(self, context_name, attribute):
        r'''Clear persistent resolved single-context settings.
        '''
        if attribute in self.score_specification.resolved_single_context_settings[context_name]:
            del(self.score_specification.resolved_single_context_settings[context_name][attribute])

    def conditionally_beam_rhythm_containers(self, rhythm_maker, rhythm_containers):
        if getattr(rhythm_maker, 'beam', False):
            durations = [x.preprolated_duration for x in rhythm_containers]
            beamtools.DuratedComplexBeamSpanner(rhythm_containers, durations=durations, span=1)

    def division_request_to_divisions(self, division_request):
        voice = componenttools.get_first_component_in_expr_with_name(self.score, division_request.voice)
        assert isinstance(voice, voicetools.Voice), voice
        division_region_division_lists = self.score_specification.contexts[voice.name][
            'division_region_division_lists']
        divisions = []
        for division_region_division_list in division_region_division_lists:
            divisions.extend(division_region_division_list)
        assert isinstance(divisions, list), divisions
        start_segment_expr = division_request.inequality.timespan.selector.start_identifier
        stop_segment_expr = division_request.inequality.timespan.selector.stop_identifier
        start_segment_index = self.score_specification.segment_identifier_expression_to_segment_index(
            start_segment_expr)
        stop_segment_index = self.score_specification.segment_identifier_expression_to_segment_index(
            stop_segment_expr)
        segment_count =  stop_segment_index - start_segment_index
        start_offset, stop_offset = self.score_specification.segment_name_to_segment_offsets(
            start_segment_index, segment_count)
        total_amount = stop_offset - start_offset
        divisions = [mathtools.NonreducedFraction(x) for x in divisions]
        divisions = sequencetools.split_sequence_once_by_weights_with_overhang(divisions, [0, total_amount])
        divisions = divisions[1]
        if division_request.callback is not None:
            divisions = division_request.callback(divisions)
        return divisions

    def fix_boundary_indicators_to_raw_segment_division_lists(self,
        voice_division_list, raw_segment_division_lists):
        #self._debug(voice_division_list, 'vdl')
        #self._debug(raw_segment_division_lists, 'rsdl')
        voice_divisions = voice_division_list.divisions
        voice_divisions = [mathtools.NonreducedFraction(x) for x in voice_divisions]
        parts = sequencetools.partition_sequence_by_backgrounded_weights(
            voice_divisions, self.score_specification.segment_durations)
        overage_from_previous_segment = 0
        segment_division_lists = []
        for part, raw_segment_division_list in zip(parts, raw_segment_division_lists):
            segment_division_list = copy.copy(raw_segment_division_list)
            segment_division_list[0].is_left_open = bool(overage_from_previous_segment)
            segment_duration_plus_fringe = overage_from_previous_segment + sum(part)
            overage_from_current_segment = segment_duration_plus_fringe - raw_segment_division_list.duration
            segment_division_list[-1].is_right_open = bool(overage_from_current_segment)
            overage_from_previous_segment = overage_from_current_segment
            segment_division_lists.append(segment_division_list)
        return segment_division_lists

    def fuse_like_rhythm_commands(self, rhythm_commands):
        if not rhythm_commands:
            return []
        result = [copy.deepcopy(rhythm_commands[0])]
        for rhythm_command in rhythm_commands[1:]:
            if rhythm_command.resolved_value == result[-1].resolved_value and not rhythm_command.fresh:
                result[-1]._duration += rhythm_command.duration
            else:
                result.append(copy.deepcopy(rhythm_command))
        return result

    def get_resolved_single_context_settings(self, segment_specification, attribute, context_name,
        include_improper_parentage=False):
        context = componenttools.get_first_component_in_expr_with_name(
            segment_specification.score_model, context_name)
        result = []
        for component in componenttools.get_improper_parentage_of_component(context):
            context_proxy = segment_specification.resolved_single_context_settings[component.name]
            resolved_single_context_settings = context_proxy.get_settings(attribute=attribute)
            if resolved_single_context_settings:
                result.extend(resolved_single_context_settings)
                if not include_improper_parentage:
                    break
        return result

    def get_rhythm_commands_for_voice(self, voice):
        from experimental import interpretertools
        from experimental import library
        rhythm_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            commands = self.get_rhythm_commands_that_start_during_segment(segment_specification, voice.name)
            rhythm_commands.extend(commands)
        if not rhythm_commands:
            rhythm_command = interpretertools.RhythmCommand(
                library.rest_filled_tokens, 
                segment_specification.segment_name,
                'FOO CONTEXT NAME',
                self.score_specification.duration, 
                0,
                segment_specification.duration,
                True
                )
            rhythm_commands.append(rhythm_command)
        return rhythm_commands

    def get_rhythm_commands_that_start_during_segment(self, segment_specification, voice_name):
        from experimental import interpretertools
        from experimental import library
        resolved_single_context_settings = self.get_resolved_single_context_settings(
            segment_specification, 'rhythm', voice_name)
        if resolved_single_context_settings is None:
            return []
        rhythm_commands = []
        for resolved_single_context_setting in resolved_single_context_settings:
            if isinstance(resolved_single_context_setting.target, selectortools.CountRatioPartSelector):
                raise Exception('implement me when it comes time.')
            else:
                rhythm_command = interpretertools.RhythmCommand(
                    resolved_single_context_setting.resolved_value, 
                    segment_specification.segment_name,
                    'FOO CONTEXT NAME',
                    segment_specification.duration, 
                    0,
                    segment_specification.duration,
                    resolved_single_context_setting.fresh
                    )
            rhythm_commands.append(rhythm_command)
        return rhythm_commands

    def get_segment_specification(self, expr):
        return self.score_specification.get_segment_specification(expr)

    def get_uninterpreted_division_commands_for_voice(self, voice):
        from experimental import interpretertools
        #self._debug(voice)
        uninterpreted_division_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            #self._debug('segment')
            commands = self.get_uninterpreted_division_commands_that_start_during_segment(
                segment_specification, voice.name)
            #self._debug(commands, 'commands')
            commands = self.sort_and_split_uninterpreted_division_commands(commands)
            #self._debug(commands, 'sorted')
            if commands:
                uninterpreted_division_commands.extend(commands)
            elif segment_specification.time_signatures:
                command = interpretertools.UninterpretedDivisionCommand(
                    segment_specification.time_signatures,
                    segment_specification.segment_name,
                    self.score_specification.score_name,
                    segment_specification.duration,
                    0,
                    segment_specification.duration,
                    True, 
                    False
                    )
                uninterpreted_division_commands.append(command)
        #print ''
        return uninterpreted_division_commands

    def get_uninterpreted_division_commands_that_start_during_segment(self, 
        segment_specification, context_name):
        resolved_single_context_settings = self.get_resolved_single_context_settings(
            segment_specification, 'divisions', context_name, include_improper_parentage=True)
        uninterpreted_division_commands = []
        for resolved_single_context_setting in resolved_single_context_settings:
            uninterpreted_division_command = \
                self.resolved_single_context_setting_to_uninterpreted_division_command(
                resolved_single_context_setting, segment_specification)
            uninterpreted_division_commands.append(uninterpreted_division_command)
        return uninterpreted_division_commands

    def get_voice_division_list(self, voice):
        from experimental import specificationtools
        voice_division_list = self.score_specification.contexts[voice.name].get('voice_division_list')
        if voice_division_list is None:
            time_signatures = self.score_specification.time_signatures
            voice_division_list = divisiontools.VoiceDivisionList(time_signatures)
        return voice_division_list

    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    def make_division_region_division_lists_for_voice(self, voice):
        uninterpreted_division_commands = self.get_uninterpreted_division_commands_for_voice(voice)
        #for x in uninterpreted_division_commands:
        #    self._debug(x, 'udc')
        region_division_commands = self.uninterpreted_division_commands_to_region_division_commands(
            uninterpreted_division_commands)
        #self._debug(uninterpreted_division_commands, 'rdc')
        division_region_division_lists = self.region_division_commands_to_division_region_division_lists(
            region_division_commands)
        self.score_specification.contexts[voice.name]['division_region_division_lists'] = \
            division_region_division_lists[:]
        self.score_specification.contexts[voice.name]['division_region_division_lists'] = \
            division_region_division_lists[:]
        return division_region_division_lists

    def make_rhythms_and_add_to_voice(self, voice, rhythm_makers, rhythm_region_division_lists):
        for rhythm_maker, rhythm_region_division_list in zip(rhythm_makers, rhythm_region_division_lists):
            if rhythm_region_division_list:
                rhythm_region_division_list = divisiontools.RhythmRegionDivisionList(
                    rhythm_region_division_list)
                self.add_rhythm_to_voice(voice, rhythm_maker, rhythm_region_division_list)

    def make_segment_division_lists_for_voice(self, voice):
        #self._debug(voice, 'voice')
        voice_division_list = self.score_specification.contexts[voice.name]['voice_division_list']
        voice_divisions = [mathtools.NonreducedFraction(x) for x in voice_division_list.divisions]
        segment_durations = self.score_specification.segment_durations
        #self._debug(voice_divisions, 'vd')
        #self._debug(segment_durations, 'sd')
        shards = sequencetools.split_sequence_once_by_weights_with_overhang(voice_divisions, segment_durations)
        raw_segment_division_lists = []
        for i, shard in enumerate(shards[:]):
            raw_segment_division_list = divisiontools.SegmentDivisionList(shard)
            raw_segment_division_lists.append(raw_segment_division_list)
        #self._debug(voice_division_list, 'vdl')
        #self._debug(raw_segment_division_lists, 'rsdl')
        segment_division_lists = self.fix_boundary_indicators_to_raw_segment_division_lists(
            voice_division_list, raw_segment_division_lists)
        return segment_division_lists

    def make_uninterpreted_division_command(
        self, resolved_single_context_setting, segment_name, duration, start_offset, stop_offset):
        from experimental import interpretertools
        uninterpreted_division_command = interpretertools.UninterpretedDivisionCommand(
            resolved_single_context_setting.resolved_value,
            segment_name,
            resolved_single_context_setting.target.context_name,
            duration,
            start_offset,
            stop_offset,
            resolved_single_context_setting.fresh,
            resolved_single_context_setting.truncate
            )
        return uninterpreted_division_command

    def make_voice_division_list_for_voice(self, voice):
        division_region_division_lists = self.score_specification.contexts[voice.name][
            'division_region_division_lists']
        voice_divisions = []
        for division_region_division_list in division_region_division_lists:
            voice_divisions.extend(division_region_division_list.divisions)
        voice_division_list = divisiontools.VoiceDivisionList(voice_divisions)
        return voice_division_list

    def region_division_command_to_division_region_division_list(self, region_division_command):
        if isinstance(region_division_command.resolved_value, list):
            divisions = [mathtools.NonreducedFraction(x) for x in region_division_command.resolved_value]
            region_duration = region_division_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            divisions = [x.pair for x in divisions]
            divisions = [divisiontools.Division(x) for x in divisions]
        elif isinstance(region_division_command.resolved_value, selectortools.SingleContextDivisionSliceSelector):
            division_request = region_division_command.resolved_value
            divisions = self.division_request_to_divisions(division_request)
        else:
            raise NotImplementedError('implement for {!r}.'.format(revision_division_command.resolved_value))
        division_region_division_list = divisiontools.DivisionRegionDivisionList(divisions)
        division_region_division_list.fresh = region_division_command.fresh
        division_region_division_list.truncate = region_division_command.truncate
        return division_region_division_list

    def region_division_commands_to_division_region_division_lists(self, region_division_commands):
        division_region_division_lists = []
        for region_division_command in region_division_commands:
            division_region_division_list = self.region_division_command_to_division_region_division_list(
                region_division_command)
            division_region_division_lists.append(division_region_division_list)
        return division_region_division_lists

    def resolve_attribute_request(self, attribute_request):
        from experimental import requesttools
        assert isinstance(attribute_request, requesttools.AttributeRequest), repr(attribute_request)
        resolved_single_context_setting = self.attribute_request_to_resolved_single_context_setting(
            attribute_request)
        resolved_value = resolved_single_context_setting.resolved_value
        assert resolved_value is not None, repr(resolved_value)
        if attribute_request.callback is not None:
            resolved_value = attribute_request.callback(resolved_value)
        result = requesttools.resolve_request_offset_and_count(attribute_request, resolved_value)
        return result

    def resolve_single_context_setting(self, single_context_setting):
        if isinstance(single_context_setting, settingtools.ResolvedSingleContextSetting):
            return single_context_setting
        value = self.resolve_single_context_setting_source(single_context_setting)
        args = (
            single_context_setting.attribute,
            single_context_setting.source,
            value,
            single_context_setting.target,
            )
        resolved_single_context_setting = settingtools.ResolvedSingleContextSetting(
            *args,
            persist=single_context_setting.persist,
            truncate=single_context_setting.truncate,
            fresh=single_context_setting.fresh
            )
        return resolved_single_context_setting

    def resolve_single_context_setting_source(self, single_context_setting):
        if isinstance(single_context_setting.source, requesttools.AttributeRequest):
            return self.resolve_attribute_request(single_context_setting.source)
        elif isinstance(single_context_setting.source, requesttools.StatalServerRequest):
            return single_context_setting.source()
        else:
            return single_context_setting.source

    def resolved_single_context_setting_to_uninterpreted_division_command(
        self, resolved_single_context_setting, segment_specification):
        selector = resolved_single_context_setting.target
        assert selector.segment_identifier == segment_specification.segment_name
        duration = selector.get_duration(self.score_specification)
        start_offset, stop_offset = selector.get_segment_offsets(self.score_specification)
        segment_name = segment_specification.segment_name
        uninterpreted_division_command = self.make_uninterpreted_division_command(
            resolved_single_context_setting, segment_name, duration, start_offset, stop_offset)
        #self._debug(uninterpreted_division_command, 'udc')
        return uninterpreted_division_command

    def sort_and_split_uninterpreted_division_commands(self, uninterpreted_division_commands):
        result = []
        start_segment_names = [x.start_segment_name for x in uninterpreted_division_commands]
        assert sequencetools.all_are_equal(start_segment_names)
        #self._debug(uninterpreted_division_commands)
        for uninterpreted_division_command in uninterpreted_division_commands:
            command_was_delayed, command_was_split = False, False
            commands_to_remove, commands_to_shorten, commands_to_delay, commands_to_split = [], [], [], []
            for command in result:
                if uninterpreted_division_command.start_offset <= command.start_offset:
                    if command.stop_offset <= uninterpreted_division_command.stop_offset:
                        commands_to_remove.append(command)
                    else:
                        commands_to_delay.append(command)
                if command.start_offset < uninterpreted_division_command.start_offset < command.stop_offset:
                    if uninterpreted_division_command.stop_offset < command.stop_offset:
                        commands_to_split.append(command)
                    else:
                        commands_to_shorten.append(command)
            #print commands_to_remove, commands_to_shorten, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                result.remove(command_to_remove)
            for command_to_shorten in commands_to_shorten:
                command_to_shorten._stop_offset = uninterpreted_division_command.start_offset
                duration = command_to_shorten.stop_offset - command_to_shorten.start_offset
                command_to_shorten._duration = duration
            for command_to_delay in commands_to_delay:
                command_to_delay._start_offset = uninterpreted_division_command.stop_offset
                duration = command_to_delay.stop_offset - command_to_delay.start_offset
                command_to_delay._duration = duration
                command_was_delayed = True
            for command_to_split in commands_to_split:
                left_command = command_to_split
                middle_command = uninterpreted_division_command
                right_command = copy.deepcopy(left_command)
                left_command._stop_offset = middle_command.start_offset
                left_duration = left_command.stop_offset - left_command.start_offset
                left_command._duration = left_duration
                right_command._start_offset = middle_command.stop_offset
                right_duration = right_command.stop_offset - right_command.start_offset
                right_command._duration = right_duration
                command_was_split = True
            if command_was_delayed:
                index = result.index(command)
                result.insert(index, uninterpreted_division_command)
            elif command_was_split:
                result.append(middle_command)
                result.append(right_command)
            else:
                result.append(uninterpreted_division_command)
        #self._debug(result)
        return result

    def store_additional_single_context_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_resolved_single_context_setting(self,
        segment_specification, resolved_single_context_setting, clear_persistent_first=False):
        context_name = resolved_single_context_setting.target.context_name
        if context_name is None:
            context_name = segment_specification.resolved_single_context_settings.score_name
        attribute = resolved_single_context_setting.attribute
        if clear_persistent_first:
            self.clear_persistent_resolved_single_context_settings(context_name, attribute)
        if attribute in segment_specification.resolved_single_context_settings[context_name]:
            segment_specification.resolved_single_context_settings[context_name][attribute].append(
                resolved_single_context_setting)
        else:
            segment_specification.resolved_single_context_settings[context_name][attribute] = [
                resolved_single_context_setting]
        if resolved_single_context_setting.persist:
            if attribute in self.score_specification.resolved_single_context_settings[context_name]:
                self.score_specification.resolved_single_context_settings[context_name][attribute].append(
                    resolved_single_context_setting)
            else:
                self.score_specification.resolved_single_context_settings[context_name][attribute] = [
                    resolved_single_context_setting]

    def store_single_context_division_settings(self):
        '''For every segment specification:

        Get every single-context division setting defined for segment.

        Then store every single-context division setting in context proxy dictionaries.
        '''
        for segment_specification in self.score_specification.segment_specifications:
            single_context_settings = segment_specification.single_context_settings.get_settings(
                attribute='divisions')
            if not single_context_settings:
                single_context_settings = []
                resolved_single_context_settings = \
                    self.score_specification.resolved_single_context_settings.get_settings(
                    attribute='divisions')
                for resolved_single_context_setting in resolved_single_context_settings:
                    single_context_setting = resolved_single_context_setting.copy_setting_to_segment(segment_specification)
                    single_context_settings.append(single_context_setting)
            self.store_single_context_settings(single_context_settings, clear_persistent_first=True)

    def store_single_context_pitch_class_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_single_context_registration_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_single_context_rhythm_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            settings = segment_specification.single_context_settings.get_settings(attribute='rhythm')
            if not settings:
                settings = []
                existing_settings = self.score_specification.resolved_single_context_settings.get_settings(
                    attribute='rhythm')
                for existing_setting in existing_settings:
                    setting = existing_setting.copy_setting_to_segment(segment_specification)
                    settings.append(setting)
            self.store_single_context_settings(settings, clear_persistent_first=True)

    def store_single_context_setting(self, single_context_setting, clear_persistent_first=False):
        '''Resolve single-context setting and find segment in which single-context setting starts.

        Store resolved single-context setting in segment resolved single-context settings.

        If setting persists then store setting in score resolved single-context settings, too.
        '''
        resolved_single_context_setting = self.resolve_single_context_setting(single_context_setting)
        selector = resolved_single_context_setting.target
        segment_specification = self.get_segment_specification(selector)
        self.store_resolved_single_context_setting(
            segment_specification, resolved_single_context_setting,
            clear_persistent_first=clear_persistent_first)

    def store_single_context_settings(self, single_context_settings, clear_persistent_first=False):
        for single_context_setting in single_context_settings:
            self.store_single_context_setting(
                single_context_setting, clear_persistent_first=clear_persistent_first)

    def store_single_context_time_signature_settings(self):
        '''For each segment:

        Check segment for an explicit time signature setting.

        If none, check score resolved settings context dictionary for current time signature setting.

        Halt interpretation if no time signature setting is found.

        Otherwise store time signature setting.
        '''
        for segment_specification in self.score_specification.segment_specifications:
            settings = segment_specification.single_context_settings.get_settings(attribute='time_signatures')
            if settings:
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
            else:
                settings = self.score_specification.resolved_single_context_settings.get_settings(
                    attribute='time_signatures')
                if not settings:
                    return
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
                setting = setting.copy_setting_to_segment(segment_specification.segment_name)
            #assert setting.target.context == segment_specification.score_name, repr(setting)
            assert setting.target.context_name == segment_specification.score_name, repr(setting)
            assert setting.target.timespan == segment_specification.timespan, [
                repr(setting), '\n', repr(segment_specification.timespan)]
            self.store_single_context_setting(setting, clear_persistent_first=True)

    # CURRENT WORK: extend this method to handle overlapping uninterpreted division commands
    def uninterpreted_division_commands_to_region_division_commands(self, uninterpreted_division_commands):
        from experimental import interpretertools
        region_division_commands = []
        if not uninterpreted_division_commands:
            return []
        if any([x.resolved_value is None for x in uninterpreted_division_commands]):
            return []
        assert uninterpreted_division_commands[0].fresh, repr(uninterpreted_division_commands[0])
        for uninterpreted_division_command in uninterpreted_division_commands:
            if uninterpreted_division_command.fresh or uninterpreted_division_command.truncate:
                region_division_command = interpretertools.RegionDivisionCommand(
                    *uninterpreted_division_command.vector)
                region_division_commands.append(region_division_command)
            else:
                last_region_division_command = region_division_commands[-1]
                assert last_region_division_command.resolved_value == uninterpreted_division_command.resolved_value
                if last_region_division_command.truncate:
                    region_division_command = interpretertools.RegionDivisionCommand(
                        *uninterpreted_division_command.vector)
                    region_division_commands.append(region_division_command)
                else:
                    duration = last_region_division_command.duration + uninterpreted_division_command.duration
                    start_offset = last_region_division_command.start_offset
                    stop_offset = last_region_division_command.stop_offset + \
                        uninterpreted_division_command.duration
                    region_division_command = interpretertools.RegionDivisionCommand(
                        last_region_division_command.resolved_value,
                        last_region_division_command.start_segment_name,
                        uninterpreted_division_command.context_name,
                        duration,
                        start_offset,
                        stop_offset,
                        last_region_division_command.fresh,
                        uninterpreted_division_command.truncate
                        )
                    region_division_commands[-1] = region_division_command
        #self._debug(region_division_commands)
        return region_division_commands

    def unpack_multiple_context_settings_for_score(self):
        for segment_specification in self.score_specification.segment_specifications:
            settings = self.unpack_multiple_context_settings_for_segment(segment_specification)
            self.score_specification.single_context_settings.extend(settings)

    def unpack_multiple_context_settings_for_segment(self, segment_specification):
        for multiple_context_setting in segment_specification.multiple_context_settings:
            segment_specification.single_context_settings.extend(multiple_context_setting.unpack())
        return segment_specification.single_context_settings
