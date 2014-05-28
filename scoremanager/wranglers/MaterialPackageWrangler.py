# -*- encoding: utf-8 -*-
import collections
import os
import traceback
from abjad.tools import systemtools
from scoremanager.wranglers.ScoreInternalPackageWrangler import \
    ScoreInternalPackageWrangler


class MaterialPackageWrangler(ScoreInternalPackageWrangler):
    r'''Material package wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MaterialPackageWrangler()

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = scoremanager.wranglers.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            MaterialPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotate_autoeditor',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        configuration = self._configuration
        path = configuration.abjad_material_packages_directory
        self._abjad_storehouse_path = path
        self._annotate_autoeditor = True
        self._asset_identifier = 'material package'
        self._basic_breadcrumb = 'materials'
        self._manager_class = managers.MaterialPackageManager
        self._score_storehouse_path_infix_parts = ('materials',)
        path = configuration.user_library_material_packages_directory
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(MaterialPackageWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'ili*': self.interpret_every_illustration_ly,
            #
            'ipo*': self.open_every_illustration_pdf,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_materials = False

    def _get_material_package_manager(self, class_name, path):
        import scoremanager
        from scoremanager import managers
        assert os.path.sep in path
        assert class_name is not None
        command = 'manager = scoremanager.managers.{}'
        command += '(path=path, session=self._session)'
        command = command.format(class_name)
        try:
            exec(command)
            return manager
        except AttributeError:
            pass
        command = 'from {0}.{1}.{1} import {1} as class_'
        configuration = self._configuration
        library_path = \
            configuration.user_library_material_packages_directory
        package_path = self._configuration.path_to_package_path(library_path)
        command = command.format(
            package_path,
            class_name,
            )
        try:
            exec(command)
        except ImportError:
            return
        package_path = self._configuration.path_to_package_path(path)
        manager = class_(package_path, session=self._session)
        return manager

    def _handle_numeric_user_input(self, result):
        manager = self._initialize_manager(result)
        if os.path.exists(manager._path):
            manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(MaterialPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_asset_paths(
        self,
        abjad_library=True,
        user_library=True,
        example_score_packages=True,
        user_score_packages=True,
        output_material_class_name='',
        ):
        from scoremanager import managers
        superclass = super(MaterialPackageWrangler, self)
        paths = superclass._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        if not output_material_class_name:
            return paths
        result = []
        for path in paths:
            manager = managers.PackageManager(
                path=path,
                session=self._session,
                )
            metadatum = manager._get_metadatum('output_material_class_name')
            if metadatum and metadatum == output_material_class_name:
                result.append(path)
        return result

    def _make_all_packages_menu_section(self, menu):
        commands = []
        commands.append(('all packages - __init__.py - list', 'nls*'))
        commands.append(('all packages - __init__.py - open', 'no*'))
        commands.append(('all packages - __init__.py - stub', 'ns*'))
        commands.append(('all packages - __metadata__.py - list', 'mdls*'))
        commands.append(('all packages - __metadata__.py - open', 'mdo*'))
        commands.append(('all packages - __metadata__.py - rewrite', 'mdw*'))
        commands.append(('all packages - illustration.ly - interpret', 'ili*'))
        commands.append(('all packages - illustration.pdf - open', 'ipo*'))
        commands.append(('all packages - version', 'vr*'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='zzz',
            )

    def _make_main_menu(self):
        superclass = super(MaterialPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_all_packages_menu_section(menu)
        self._make_material_command_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_material_command_menu_section(self, menu):
        commands = []
        commands.append(('materials - copy', 'cp'))
        commands.append(('materials - new', 'new'))
        commands.append(('materials - remove', 'rm'))
        commands.append(('materials - rename', 'ren'))
        menu.make_command_section(
            commands=commands,
            name='material',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_materials = True

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        self._copy_asset()

    def interpret_every_illustration_ly(self):
        r'''Interprets ``illustration.ly`` in every package.

        Returns none.
        '''
        self._interpret_in_every_package('illustration.ly')

    def make_package(self):
        r'''Makes package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._user_storehouse_path
        prompt_string = 'enter material package name'
        path = self._get_available_path(
            prompt_string=prompt_string,
            storehouse_path=storehouse_path,
            )
        if self._session.is_backtracking:
            return
        if not path:
            return
        manager = self._get_manager(path)
        manager._make_package()
        manager._run()

    def open_every_illustration_pdf(self):
        r'''Opens ``illustration.pdf`` in every package.

        Returns none.
        '''
        self._open_in_every_package('illustration.pdf')

    def remove_packages(self):
        r'''Removes one or more packages.

        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames package.

        Returns none.
        '''
        self._rename_asset()