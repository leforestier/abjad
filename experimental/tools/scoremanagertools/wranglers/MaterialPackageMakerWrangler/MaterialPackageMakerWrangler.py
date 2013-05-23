import os
from abjad.tools import stringtools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageMakerWrangler(PackageWrangler):
    '''Material package maker wrangler.

    ::
    
        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.material_package_maker_wrangler
        >>> wrangler
        MaterialPackageMakerWrangler()

    Return material package maker wrangler.
    '''

    ### CLASS VARIABLES ###

    built_in_external_storehouse_packagesystem_path = \
        PackageWrangler.configuration.built_in_material_package_makers_package_path

    forbidden_directory_entries = (
        'FunctionInputMaterialPackageMaker',
        'InventoryMaterialPackageMaker',
        'MaterialPackageMaker',
        )

    storehouse_path_infix_parts = None

    user_external_storehouse_packagesystem_path = \
        PackageWrangler.configuration.user_material_package_makers_package_path
    
    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'material package makers'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        else:
            raise ValueError

    def _initialize_asset_proxy(self, package_path):
        from experimental.tools.scoremanagertools.proxies.MaterialPackageProxy import MaterialPackageProxy
        if os.path.sep in package_path:
            package_path = self.configuration.filesystem_path_to_packagesystem_path(package_path)
        material_package_proxy = MaterialPackageProxy(package_path, session=self._session)
        material_package_maker_class_name = material_package_proxy.material_package_maker_class_name
        if material_package_maker_class_name is not None:
            material_package_maker_class = None
            command = 'from experimental.tools.scoremanagertools.materialpackagemakers '
            command += 'import {} as material_package_maker_class'
            command = command.format(material_package_maker_class_name)
            try:
                exec(command)
            except ImportError:
                command = 'from {} import {} as material_package_maker_class'
                command = command.format(
                    self.configuration.user_material_package_makers_package_path, 
                    material_package_maker_class_name)
                exec(command)
            material_package_proxy = material_package_maker_class(
                package_path, session=self._session)
        return material_package_proxy

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(where=self._where, is_numbered=True)
        section.tokens = self.list_asset_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new material package maker'))
        return menu

    def _make_menu_tokens(self, head=None):
        keys = self.list_asset_packagesystem_paths(head=head)
        bodies = self.list_asset_names(head=head)
        return zip(keys, bodies)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        '''Asset proxy class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'PackageProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    @property
    def storage_format(self):
        '''Material package maker wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.MaterialPackageMakerWrangler()'

        Return string.
        '''
        return super(type(self), self).storage_format

    ### PUBLIC METHODS ###

    def list_asset_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset filesystem paths.

        Example. List built-in material package maker filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/materialpackagemakers/ArticulationHandlerMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/DynamicHandlerMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/ListMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/MarkupInventoryMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/OctaveTranspositionMappingInventoryMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/PitchRangeInventoryMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/RhythmMakerMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/SargassoMeasureMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/TempoMarkInventoryMaterialPackageMaker'

        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_names(self, built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset names.

        Example. List built-in asset names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     user_external=False, user_score=False):
            ...     x
            'articulation handler material package maker'
            'dynamic handler material package maker'
            'list material package maker'
            'markup inventory material package maker'
            'octave transposition mapping inventory material package maker'
            'pitch range inventory material package maker'
            'rhythm maker material package maker'
            'sargasso measure material package maker'
            'tempo mark inventory material package maker'

        Return list.
        '''
        return super(type(self), self).list_asset_names(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_packagesystem_paths(self, built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset packagesystem_paths.

        Example. List built-in asset packagesystem_paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            'experimental.tools.scoremanagertools.materialpackagemakers.ArticulationHandlerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.DynamicHandlerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.ListMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.MarkupInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.OctaveTranspositionMappingInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.RhythmMakerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.TempoMarkInventoryMaterialPackageMaker'
            'materialpackagemakers.ConstellationCircuitSelectionMaterialPackageMaker'
            'materialpackagemakers.ZaggedPitchClassMaterialPackageMaker'

        .. note:: FIXME: user collateral shows up even when not requested.

        Return list.
        '''
#        return super(type(self), self).list_asset_packagesystem_paths(
#            built_in_external=built_in_external,
#            user_external=user_external,
#            built_in_score=built_in_score,
#            user_score=user_score,
#            head=head)
        return super(type(self), self).list_asset_packagesystem_paths()

    # TODO: make this work
#    def list_asset_proxies(self, built_in_external=True, user_external=True,
#        built_in_score=True, user_score=True, head=None):
#        '''List asset proxies.
#
#        Example. List built-in material package maker proxies:
#            
#        ::
#
#            >>> for x in wrangler.list_asset_proxies(
#            ...     user_external=False, user_score=False):
#            ...     x
#
#        Return list.
#        '''
#        return super(type(self), self).list_asset_proxies(
#            built_in_external=built_in_external,
#            user_external=user_external,
#            built_in_score=built_in_score,
#            user_score=user_score,
#            head=head)

    def list_external_asset_packagesystem_paths(self, head=None):
        '''List external asset packagesystem paths:

        ::

            >>> for x in wrangler.list_external_asset_packagesystem_paths():
            ...     x
            'experimental.tools.scoremanagertools.materialpackagemakers.ArticulationHandlerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.DynamicHandlerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.ListMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.MarkupInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.OctaveTranspositionMappingInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.RhythmMakerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.TempoMarkInventoryMaterialPackageMaker'
            'materialpackagemakers.ConstellationCircuitSelectionMaterialPackageMaker'
            'materialpackagemakers.ZaggedPitchClassMaterialPackageMaker'

        .. note:: FIXME: user collateral should be fully qualified.

        Return list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_score=False, user_score=False, head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_score_asset_packagesystem_paths(self, head=None):
        '''List score asset package paths:

        ::

            >>> wrangler.list_score_asset_packagesystem_paths()
            []

        Return list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_external=False, user_external=False, head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_storehouse_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List storehouse filesystem paths.

        Example. List built-in material package maker storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/materialpackagemakers'

        Return list.
        '''
        return super(type(self), self).list_storehouse_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    # TODO: change to boilerplate
    def make_asset_class_file(self, package_name, generic_output_name):
        class_file_name = os.path.join(
            self._list_built_in_external_storehouse_packagesystem_path()[0],
            package_name, package_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from music.foo import foo')
        lines.append('from music.foo import make_illustration_from_output_material')
        lines.append('from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker import MaterialPackageMaker')
        lines.append('from experimental.tools.scoremanagertools.editors.UserInputWrapper import UserInputWrapper')
        lines.append('from experimental.tools import scoremanagertools')
        lines.append('')
        lines.append('')
        lines.append('class {}(MaterialPackageMaker):'.format(package_name))
        lines.append('')
        lines.append('    def __init__(self, package_path=None, session=None):')
        lines.append('        MaterialPackageMaker.__init__(')
        lines.append('            self, package_path=package_path, session=seession')
        lines.append('')
        lines.append('    ### READ-ONLY PUBLIC PROPERTIES ###')
        lines.append('')
        lines.append('    generic_output_name = {!r}'.format(generic_output_name))
        lines.append('')
        lines.append('    illustration_maker = staticmethod(make_illustration_from_output_material)')
        lines.append('')
        lines.append('    output_material_checker = staticmethod(componenttools.all_are_components)')
        lines.append('')
        lines.append('    output_material_maker = staticmethod(music.foo)')
        lines.append('')
        lines.append('    output_material_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_demo_values = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_tests = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    ### PUBLIC METHODS ###')
        lines.append('')
        lines.append('    @property')
        lines.append('    def output_material_module_body_lines(self):')
        lines.append('        lines = []')
        lines.append('        output_material = self.output_material')
        lines.append("        lines.append('{} = {!r}'.format(self.material_package_name, output_material)")
        class_file.write('\n'.join(lines))
        class_file.close()

    # TODO: change to boilerplate
    def make_asset_initializer(self, package_name):
        initializer_file_name = os.path.join(
            self._list_built_in_external_storehouse_packagesystem_path()[0],
            package_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools import importtools\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("importtools.import_structured_package(__path__[0], globals())\n")
        initializer.close()

    def make_asset_interactively(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_material_package_maker_class_name('material proxy name')
        getter.append_space_delimited_lowercase_string('generic output product')
        result = getter._run()
        if self._session.backtrack():
            return
        material_package_maker_class_name, generic_output_product_name = result
        material_package_maker_directory = os.path.join(
            self._list_built_in_external_storehouse_packagesystem_path[0],
            material_package_maker_class_name)
        os.mkdir(material_package_maker_directory)
        self.make_asset_initializer(material_package_maker_class_name)
        self.make_asset_class_file(
            material_package_maker_class_name, generic_output_product_name)
        self.make_asset_stylesheet(material_package_maker_class_name)

    # TODO: change to boilerplate
    def make_asset_stylesheet(self, package_name):
        stylesheet = lilypondfiletools.make_basic_lilypond_file()
        stylesheet.pop()
        stylesheet.file_initial_system_comments = []
        stylesheet.default_paper_size = 'letter', 'portrait'
        stylesheet.global_staff_size = 14
        stylesheet.layout_block.indent = 0
        stylesheet.layout_block.ragged_right = True
        stylesheet.paper_block.markup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)
        stylesheet.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 10, 0)
        stylesheet_file_name = os.path.join(
            self._list_built_in_external_storehouse_packagesystem_path()[0],
            package_name, 'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()
