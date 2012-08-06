from abjad.tools import *
from experimental import *
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting
from experimental.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


def test_MultipleContextSettingInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    multiple_context_setting_inventory_1 = segment.multiple_context_settings

    storage_format = multiple_context_setting_inventory_1.storage_format

    r'''
    settingtools.MultipleContextSettingInventory([
        settingtools.MultipleContextSetting(
            'time_signatures',
            [(4, 8), (3, 8)],
            selectortools.TimespanSelector(
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                ),
            context_names=['Grouped Rhythmic Staves Score'],
            persist=True,
            truncate=False
            )
        ])
    '''

    multiple_context_setting_inventory_2 = eval(storage_format)

    assert isinstance(multiple_context_setting_inventory_1, MultipleContextSettingInventory)
    assert isinstance(multiple_context_setting_inventory_2, MultipleContextSettingInventory)
    assert not multiple_context_setting_inventory_1 is multiple_context_setting_inventory_2
    assert multiple_context_setting_inventory_1 == multiple_context_setting_inventory_2
