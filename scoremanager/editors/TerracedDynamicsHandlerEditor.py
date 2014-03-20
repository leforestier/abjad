# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class TerracedDynamicsHandlerEditor(Editor):
    r'''TerracedDynamicsHandler editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            handlertools.TerracedDynamicsHandler,
            ('dynamics', None, 'dy', getters.get_dynamics, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )
