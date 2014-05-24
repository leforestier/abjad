# -*- encoding: utf-8 -*-
import copy
import doctest
import os
import re
import shutil
import subprocess
from abjad.tools import datastructuretools
from abjad.tools import developerscripttools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.AssetController import AssetController


class Wrangler(AssetController):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abjad_storehouse_path',
        '_annotate_year',
        '_basic_breadcrumb',
        '_asset_identifier',
        '_human_readable',
        '_include_asset_name',
        '_include_extensions',
        '_main_menu',
        '_manager_class',
        '_score_storehouse_path_infix_parts',
        '_sort_by_annotation',
        '_user_storehouse_path',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        assert session is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._annotate_year = False
        self._asset_identifier = None
        self._basic_breadcrumb = None
        self._human_readable = True
        self._include_asset_name = True
        self._include_extensions = False
        self._manager_class = managers.PackageManager
        self._score_storehouse_path_infix_parts = ()
        self._sort_by_annotation = True
        self._user_storehouse_path = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        breadcrumb = self._basic_breadcrumb
        view_name = self._read_view_name()
        if not view_name:
            return breadcrumb
        view_inventory = self._read_view_inventory()
        if view_name in view_inventory:
            breadcrumb = '{} ({})'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _current_package_manager(self):
        path = self._get_current_directory()
        if path is None:
            return
        return self._io_manager._make_package_manager(path)

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory)
            parts.extend(self._score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self._abjad_storehouse_path

    @property
    def _init_py_file_path(self):
        path = self._get_current_directory()
        if path:
            return os.path.join(path, '__init__.py')

    @property
    def _input_to_method(self):
        superclass = super(Wrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'vap': self.apply_view,
            'vcl': self.clear_view,
            'vls': self.list_views,
            'vnew': self.make_view,
            'vren': self.rename_view,
            'vrm': self.remove_views,
            'vo': self.open_views_py,
            })
        return result

    @property
    def _views_package_manager(self):
        path = self._configuration.wrangler_views_directory
        return self._io_manager._make_package_manager(path)

    @property
    def _views_py_path(self):
        if self._session.is_in_score:
            directory = self._get_current_directory()
            return os.path.join(directory, '__views__.py')
        else:
            directory = self._configuration.wrangler_views_directory
            class_name = type(self).__name__
            file_name = '__{}_views__.py'.format(class_name)
            return os.path.join(directory, file_name)

    ### PRIVATE METHODS ###

    def _copy_asset(
        self, 
        extension=None,
        file_name_callback=None, 
        force_lowercase=True,
        new_storehouse=None
        ):
        old_path = self._select_visible_asset_path(infinitive_phrase='to copy')
        if not old_path:
            return
        old_name = os.path.basename(old_path)
        if new_storehouse:
            pass
        elif self._session.is_in_score:
            new_storehouse = self._get_current_directory()
        else:
            new_storehouse = self._select_storehouse_path()
            if self._session.is_backtracking:
                return
            if not new_storehouse:
                return
        prompt_string = 'new {} name'
        prompt_string = prompt_string.format(self._asset_identifier)
        # TODO: add additional help string: "leave blank to keep name"
        getter = self._io_manager._make_getter()
        getter.append_string(prompt_string)
        name = getter._run()
        if self._session.is_backtracking:
            return
        if not name:
            name = old_name
        name = stringtools.strip_diacritics(name)
        if file_name_callback:
            name = file_name_callback(name)
        name = name.replace(' ', '_')
        if force_lowercase:
            name = name.lower()
        if extension and not name.endswith(extension):
            name = name + extension
        new_path = os.path.join(new_storehouse, name)
        if os.path.exists(new_path):
            message = 'already exists: {}'.format(new_path)
            return
        messages = []
        messages.append('will copy ...')
        messages.append(' FROM: {}'.format(old_path))
        messages.append('   TO: {}'.format(new_path))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        if os.path.isfile(old_path):
            shutil.copyfile(old_path, new_path)
        elif os.path.isdir(old_path):
            shutil.copytree(old_path, new_path)
        else:
            raise TypeError(old_path)

    def _enter_run(self):
        pass

    def _extract_common_parent_directories(self, paths):
        parent_directories = []
        example_score_packages_directory = \
            self._configuration.example_score_packages_directory
        user_score_packages_directory = \
            self._configuration.user_score_packages_directory
        for path in paths:
            parent_directory = os.path.dirname(path)
            if parent_directory == user_score_packages_directory:
                parent_directories.append(path)
            elif parent_directory == example_score_packages_directory:
                parent_directories.append(path)
            elif parent_directory not in parent_directories:
                parent_directories.append(parent_directory)
        return parent_directories

    def _filter_asset_menu_entries_by_view(self, entries):
        view = self._read_view()
        if view is None:
            return entries
        entries = entries[:]
        filtered_entries = []
        for item in view:
            try:
                pattern = re.compile(item)
            except TypeError:
                pattern = None
                message = 'invalid regular expression: {!r}.'
                message  = message.format(item)
                self._io_manager._display(message)
            for entry in entries:
                display_string, _, _, path = entry
                if self._session.is_in_score:
                    string = self._get_without_annotation(display_string)
                else:
                    string = display_string
                if item == string:
                    filtered_entries.append(entry)
                elif pattern and pattern.match(string):
                    filtered_entries.append(entry)
        return filtered_entries

    def _find_git_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=True,
            repository='git',
            )
        return manager

    def _find_svn_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=False,
            repository='svn',
            )
        return manager

    def _find_up_to_date_manager(
        self,
        inside_score=True,
        must_have_file=False,
        system=True,
        repository='git',
        ):
        from scoremanager import core
        from scoremanager import wranglers
        abjad_library = False
        example_score_packages = False
        user_library = False
        user_score_packages = False
        if system and inside_score:
            example_score_packages = True
        elif system and not inside_score:
            abjad_library = True
        elif not system and inside_score:
            user_score_packages = True
        elif not system and not inside_score:
            user_library = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        if type(self) is wranglers.ScorePackageWrangler:
            if system:
                scores_directory = \
                    self._configuration.example_score_packages_directory
            else:
                scores_directory = \
                    self._configuration.user_score_packages_directory
            asset_paths = []
            for directory_entry in  os.listdir(scores_directory):
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(scores_directory, directory_entry)
                if os.path.isdir(path):
                    asset_paths.append(path)
        session = core.Session()
        for asset_path in asset_paths:
            manager = self._manager_class(
                path=asset_path,
                session=session,
                )
            if (repository == 'git' and
                manager._is_git_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager
            elif (repository == 'svn' and
                manager._is_svn_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager

    def _get_available_path(
        self,
        prompt_string=None,
        storehouse_path=None,
        ):
        storehouse_path = storehouse_path or self._current_storehouse_path
        while True:
            prompt_string = prompt_string or 'enter package name'
            getter = self._io_manager._make_getter()
            getter.append_space_delimited_lowercase_string(prompt_string)
            name = getter._run()
            if self._session.is_backtracking:
                return
            if not name:
                return
            name = stringtools.to_accent_free_snake_case(name)
            path = os.path.join(storehouse_path, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager._display(line)
            else:
                return path

    def _get_current_directory(self):
        score_directory = self._session.current_score_directory
        if score_directory is not None:
            parts = (score_directory,)
            parts += self._score_storehouse_path_infix_parts
            directory = os.path.join(*parts)
            assert '.' not in directory, repr(directory)
            return directory

    def _get_file_path_ending_with(self, string):
        path = self._get_current_directory()
        for file_name in self._list():
            if file_name.endswith(string):
                file_path = os.path.join(path, file_name)
                return file_path

    def _get_manager(self, path):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        return manager

    def _get_next_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[0]
        if last_path not in paths:
            return paths[0]
        index = paths.index(last_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path

    def _get_previous_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[-1]
        if last_path not in paths:
            return paths[-1]
        index = paths.index(last_path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _get_sibling_asset_path(self):
        if self._session.is_navigating_to_next_asset:
            return self._get_next_asset_path()
        if self._session.is_navigating_to_previous_asset:
            return self._get_previous_asset_path()

    def _get_visible_storehouses(self):
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        storehouses = set()
        for menu_entry in asset_section:
            path = menu_entry.return_value
            storehouse = self._configuration._path_to_storehouse(path)
            storehouses.add(storehouse)
        storehouses = list(sorted(storehouses))
        return storehouses

    @staticmethod
    def _get_without_annotation(display_string):
        if not display_string.endswith(')'):
            return display_string
        index = display_string.find('(')
        result = display_string[:index]
        result = result.strip()
        return result

    def _handle_numeric_user_input(self, result):
        self._io_manager.open_file(result)

    def _initialize_manager(self, path, asset_identifier=None):
        assert os.path.sep in path, repr(path)
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        if asset_identifier:
            manager._asset_identifier = asset_identifier
        return manager

    def _interpret_in_every_package(self, file_name):
        paths = []
        for segment_path in self._list_visible_asset_paths():
            path = os.path.join(segment_path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        _, extension = os.path.splitext(file_name)
        messages = []
        messages.append('will interpret ...')
        for path in paths:
            message = ' INPUT: {}'.format(path)
            messages.append(message)
            if extension == '.ly':
                output_path = path.replace('.ly', '.pdf')
                message = 'OUTPUT: {}'.format(output_path)
                messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        for path in paths:
            self._io_manager.interpret_file(path)

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry[0].isalpha():
            if not directory_entry.endswith('.pyc'):
                return True
        return False

    def _list(self, public_entries_only=False):
        result = []
        path = self._get_current_directory()
        if not path or not os.path.exists(path):
            return result
        if public_entries_only:
            for directory_entry in sorted(os.listdir(path)):
                if directory_entry[0].isalpha():
                    if not directory_entry.endswith('.pyc'):
                        if not directory_entry in ('test',):
                            result.append(directory_entry)
        else:
            for directory_entry in sorted(os.listdir(path)):
                if not directory_entry.startswith('.'):
                    if not directory_entry.endswith('.pyc'):
                        result.append(directory_entry)
        return result

    def _list_all_directories_with_metadata_pys(self):
        directories = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            result = self._list_directories_with_metadata_pys(path)
            directories.extend(result)
        return directories

    def _list_asset_paths(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        result = []
        directorys = self._list_storehouse_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        for directory in directorys:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            directory_entries =  sorted(os.listdir(directory))
            for directory_entry in directory_entries:
                if not self._is_valid_directory_entry(directory_entry):
                    continue
                path = os.path.join(directory, directory_entry)
                result.append(path)
        return result

    def _list_storehouse_paths(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        result = []
        if (abjad_library and
            self._abjad_storehouse_path is not None):
            result.append(self._abjad_storehouse_path)
        if user_library and self._user_storehouse_path is not None:
            result.append(self._user_storehouse_path)
        if (example_score_packages and
            self._score_storehouse_path_infix_parts):
            for score_directory in \
                self._configuration.list_score_directorys(abjad=True):
                parts = [score_directory]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                storehouse_path = os.path.join(*parts)
                result.append(storehouse_path)
        if user_score_packages and self._score_storehouse_path_infix_parts:
            for directory in \
                self._configuration.list_score_directorys(user=True):
                parts = [directory]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                path = os.path.join(*parts)
                result.append(path)
        return result

    def _list_visible_asset_managers(self):
        paths = self._list_visible_asset_paths()
        managers = []
        for path in paths:
            manager = self._initialize_manager(path=path)
            managers.append(manager)
        return managers

    def _list_visible_asset_paths(self):
        entries = self._make_asset_menu_entries()
        paths = [_[-1] for _ in entries]
        return paths

    def _make_asset(self, asset_name):
        if os.path.sep in asset_name:
            asset_name = os.path.basename(asset_name)
        assert stringtools.is_snake_case(asset_name)
        path = os.path.join(
            self._current_storehouse_path,
            asset_name,
            )
        manager = self._initialize_manager(path)
        if hasattr(manager, '_write_stub'):
            self._io_manager.write_stub(path)
        elif hasattr(manager, 'fix_package'):
            manager.fix_package(confirm=False, display=False)

    def _make_asset_menu_entries(
        self,
        apply_current_directory=True,
        apply_view=True,
        ):
        paths = self._list_asset_paths()
        current_directory = self._get_current_directory()
        if (apply_current_directory or apply_view) and current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        strings = [self._path_to_asset_menu_display_string(_) for _ in paths]
        pairs = list(zip(strings, paths))
        if not self._session.is_in_score and self._sort_by_annotation:
            def sort_function(pair):
                string = pair[0]
                if '(' not in string:
                    return string
                open_parenthesis_index = string.find('(')
                assert string.endswith(')')
                annotation = string[open_parenthesis_index:]
                annotation = annotation.replace("'", '')
                annotation = stringtools.strip_diacritics(annotation)
                return annotation
            pairs.sort(key=lambda _: sort_function(_))
        else:
            def sort_function(pair):
                string = pair[0]
                string = stringtools.strip_diacritics(string)
                string = string.replace("'", '')
                return string
            pairs.sort(key=lambda _: sort_function(_))
        entries = []
        for string, path in pairs:
            entry = (string, None, None, path)
            entries.append(entry)
        if apply_view and not self._session.is_test:
            entries = self._filter_asset_menu_entries_by_view(entries)
        if self._session.is_test:
            if getattr(self, '_only_example_scores_during_test', False):
                entries = [_ for _ in entries if 'Example Score' in _[0]]
        return entries

    def _make_asset_menu_section(self, menu):
        menu_entries = self._make_asset_menu_entries()
        if menu_entries:
            menu.make_asset_section(menu_entries=menu_entries)

    def _make_asset_selection_breadcrumb(
        self,
        human_readable_target_name=None,
        infinitival_phrase=None,
        is_storehouse=False,
        ):
        if human_readable_target_name is None:
            name = self._manager_class.__name__
            name = stringtools.upper_camel_case_to_space_delimited_lowercase(
                name)
            human_readable_target_name = name
        if infinitival_phrase:
            return 'select {} {}:'.format(
                human_readable_target_name,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select storehouse'
        else:
            return 'select {}:'.format(human_readable_target_name)

    def _make_asset_selection_menu(self):
        menu = self._io_manager._make_menu(name='asset selection')
        menu_entries = self._make_asset_menu_entries()
        menu.make_asset_section(menu_entries=menu_entries)
        return menu

    def _make_file(
        self, 
        extension='', 
        file_name_callback=None,
        force_lowercase=True,
        prompt_string='file name', 
        ):
        from scoremanager import managers
        if self._session.is_in_score:
            path = self._get_current_directory()
        else:
            path = self._select_storehouse_path()
            if self._session.is_backtracking:
                return
            if not path:
                return
        getter = self._io_manager._make_getter()
        getter.append_string(prompt_string)
        name = getter._run()
        if self._session.is_backtracking:
            return
        if not name:
            return
        name = stringtools.strip_diacritics(name)
        if file_name_callback:
            name = file_name_callback(name)
        name = name.replace(' ', '_')
        if force_lowercase:
            name = name.lower()
        if not name.endswith(extension):
            name = name + extension
        path = os.path.join(path, name)
        self._io_manager.write(path, '')
        self._io_manager.edit(path)

    def _make_main_menu(self):
        superclass = super(Wrangler, self)
        menu = superclass._make_main_menu()
        self._make_asset_menu_section(menu)
        self._make_views_menu_section(menu)
        self._make_views_py_menu_section(menu)
        return menu

    def _make_storehouse_menu_entries(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        from scoremanager import wranglers
        display_strings, keys = [], []
        keys.append(self._user_storehouse_path)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        paths = wrangler._list_asset_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = wrangler._initialize_manager(path)
            display_strings.append(manager._get_title())
            path_parts = (manager._path,)
            path_parts = path_parts + self._score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _make_views_menu_section(self, menu):
        commands = []
        commands.append(('views - apply', 'vap'))
        commands.append(('views - clear', 'vcl'))
        commands.append(('views - list', 'vls'))
        commands.append(('views - new', 'vnew'))
        commands.append(('views - remove', 'vrm'))
        commands.append(('views - rename', 'vren'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views',
            )

    def _make_views_py_menu_section(self, menu):
        commands = []
        commands.append(('__views.py__ - open', 'vo'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='__views__.py',
            )

    def _open_file_ending_with(self, string):
        path = self._get_file_path_ending_with(string)
        if path:
            self._io_manager.open_file(path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

    def _open_in_every_package(self, file_name, verb='open'):
        paths = []
        for segment_path in self._list_visible_asset_paths():
            path = os.path.join(segment_path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        if not paths:
            message = 'no {} files found.'
            message = message.format(file_name)
            self._io_manager._display(message)
            return
        messages = []
        message = 'will {} ...'.format(verb)
        messages.append(message)
        for path in paths:
            message = '   ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        self._io_manager.open_file(paths)

    def _path_to_annotation(self, path):
        score_storehouses = (
            self._configuration.example_score_packages_directory,
            self._configuration.user_score_packages_directory,
            )
        if path.startswith(score_storehouses):
            score_path = self._configuration._path_to_score_path(path)
            manager = self._io_manager._make_package_manager(path=score_path)
            metadata = manager._get_metadata()
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if self._annotate_year and year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = package_name
        elif path.startswith(self._user_storehouse_path):
            annotation = self._configuration.composer_last_name
        elif path.startswith(self._abjad_storehouse_path):
            annotation = 'Abjad'
        else:
            annotation = None
        return annotation

    def _path_to_asset_menu_display_string(self, path):
        if self._human_readable:
            asset_name = self._path_to_human_readable_name(path)
        else:
            asset_name = os.path.basename(path)
        if 'segments' in path:
            manager = self._io_manager._make_package_manager(path=path)
            name = manager._get_metadatum('name')
            asset_name = name or asset_name
        if self._session.is_in_score:
            string = asset_name
        else:
            annotation = self._path_to_annotation(path)
            if self._include_asset_name:
                string = '{} ({})'.format(asset_name, annotation)
            else:
                string = annotation
        if getattr(self, '_annotate_autoeditor', False):
            use_autoeditor = False
            manager = self._io_manager._make_package_manager(path=path)
            metadata = manager._get_metadata()
            if metadata:
                use_autoeditor = metadata.get('use_autoeditor')
            if use_autoeditor:
                string = string + ' (AE)'
        return string

    def _path_to_human_readable_name(self, path):
        path = os.path.normpath(path)
        name = os.path.basename(path)
        include_extensions = self._include_extensions
        if not include_extensions:
            name, extension = os.path.splitext(name)
        return stringtools.to_space_delimited_lowercase(name)

    def _read_view(self):
        view_name = self._read_view_name()
        if not view_name:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self):
        if self._views_py_path is None:
            return
        if not os.path.exists(self._views_py_path):
            return
        result = self._io_manager.execute_file(
            path=self._views_py_path,
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            messages = []
            message = '{} __views.py__ is corrupt:'
            message = message.format(type(self).__name__)
            messages.append(message)
            messages.append('')
            message = '    {}'.format(self._views_py_path)
            messages.append(message)
            self._io_manager._display(messages)
            return
        if not result:
            return
        assert len(result) == 1
        view_inventory = result[0]
        return view_inventory

    def _read_view_name(self):
        if self._session.is_test:
            return
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        if not manager:
            return
        return manager._get_metadatum(metadatum_name)

    def _remove_assets(self, confirm=True, display=True):
        from scoremanager import managers
        paths = self._select_visible_asset_paths()
        if not paths:
            return
        if confirm:
            count = len(paths)
            messages = []
            if count == 1:
                message = 'will remove {}'.format(paths[0])
                messages.append(message)
            else:
                messages.append('will remove ...')
                for path in paths:
                    message = '    {}'.format(path)
                    messages.append(message)
            if display:
                self._io_manager._display(messages)
            if count == 1:
                confirmation_string = 'remove'
            else:
                confirmation_string = 'remove {}'
                confirmation_string = confirmation_string.format(count)
            prompt_string = "type {!r} to proceed"
            prompt_string = prompt_string.format(confirmation_string)
            getter = self._io_manager._make_getter()
            getter.append_string(prompt_string)
            result = getter._run()
            if self._session.is_backtracking:
                return
            if not result == confirmation_string:
                return
        for path in paths:
            manager = managers.PackageManager(path=path, session=self._session)
            manager._remove(confirm=False, display=False)

    def _rename_asset(
        self,
        extension=None,
        file_name_callback=None, 
        force_lowercase=True,
        ):
        path = self._select_visible_asset_path(infinitive_phrase='to rename')
        if not path:
            return
        file_name = os.path.basename(path)
        message = 'existing file name> {}'
        message = message.format(file_name)
        self._io_manager._display(message)
        manager = self._initialize_manager(
            path,
            asset_identifier=self._asset_identifier,
            )
        manager._rename_interactively(
            extension=extension,
            file_name_callback=file_name_callback,
            force_lowercase=force_lowercase,
            )
        self._session._is_backtracking_locally = False

    def _run(self, input_=None):
        from scoremanager import iotools
        if input_:
            self._session._pending_input = input_
        controller = iotools.ControllerContext(
            consume_local_backtrack=True,
            controller=self,
            on_enter_callbacks=(self._enter_run,),
            )
        directory = systemtools.NullContextManager()
        if self._session.is_in_score:
            path = self._get_current_directory()
            directory = systemtools.TemporaryDirectoryChange(path)
        with controller, directory:
            result = None
            self._session._is_pending_output_removal = True
            while True:
                result = self._get_sibling_asset_path()
                if not result:
                    menu = self._make_main_menu()
                    result = menu._run()
                if self._session.is_backtracking:
                    return
                if result:
                    self._handle_main_menu_result(result)
                    if self._session.is_backtracking:
                        return

    def _select_asset_path(self):
        menu = self._make_asset_selection_menu()
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb()
            result = menu._run()
            if self._session.is_backtracking:
                return
            elif not result:
                continue
            elif result == '<return>':
                return
            else:
                break
        return result

    def _select_storehouse_path(self):
        from scoremanager import iotools
        menu_entries = self._make_storehouse_menu_entries(
            abjad_library=False,
            example_score_packages=False,
            user_library=True,
            user_score_packages=False,
            )
        selector = iotools.Selector(
            breadcrumb='storehouse',
            menu_entries=menu_entries,
            session=self._session,
            )
        result = selector._run()
        if self._session.is_backtracking:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from scoremanager import managers
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager._display(message)
            return
        view_names = list(view_inventory.keys())
        if is_ranged:
            breadcrumb = 'view(s)'
        else:
            breadcrumb = 'view'
        if infinitive_phrase:
            breadcrumb = '{} {}'.format(breadcrumb, infinitive_phrase)
        selector = self._io_manager._make_selector(
            breadcrumb=breadcrumb,
            is_ranged=is_ranged,
            items=view_names,
            )
        result = selector._run()
        if self._session.is_backtracking:
            return
        return result

    def _select_visible_asset_path(self, infinitive_phrase=None):
        getter = self._io_manager._make_getter()
        prompt_string = 'enter {}'.format(self._asset_identifier)
        if infinitive_phrase:
            prompt_string = prompt_string + ' ' + infinitive_phrase
        if hasattr(self, '_make_asset_menu_section'):
            dummy_menu = self._io_manager._make_menu()
            self._make_asset_menu_section(dummy_menu)
            asset_section = dummy_menu._asset_section
        else:
            menu = self._make_asset_selection_menu()
            asset_section = menu['assets']
        getter.append_menu_section_item(
            prompt_string, 
            asset_section,
            )
        numbers = getter._run()
        if self._session.is_backtracking:
            return
        if not len(numbers) == 1:
            return
        number = numbers[0]
        index = number - 1
        paths = [_.return_value for _ in asset_section.menu_entries]
        path = paths[index]
        return path

    def _select_visible_asset_paths(self):
        getter = self._io_manager._make_getter()
        plural_identifier = stringtools.pluralize(self._asset_identifier)
        prompt_string = 'enter {}(s) to remove'
        prompt_string = prompt_string.format(plural_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            prompt_string, 
            asset_section,
            )
        numbers = getter._run()
        if self._session.is_backtracking:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths

    def _set_is_navigating_to_sibling_asset(self):
        message = 'implement on concrete wrangler classes.'
        raise Exception(message)

    def _write_view_inventory(
        self, 
        view_inventory, 
        confirm=True,
        display=True,
        ):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('from scoremanager import iotools')
        lines.append('')
        lines.append('')
        view_inventory = self._sort_ordered_dictionary(view_inventory)
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        contents = '\n'.join(lines)
        self._io_manager.write(self._views_py_path, contents)
        if display:
            message = 'view inventory written to disk.'
            self._io_manager._display(message)

    ### PUBLIC METHODS ###

    def add_to_repository(self, confirm=True, display=True):
        r'''Adds files to repository.

        Returns none.
        '''
        self._session._attempted_to_add_to_repository = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            manager.add_to_repository(confirm=False, display=False)

    def apply_view(self):
        r'''Applies view.

        Writes view name to ``__metadata.py__``.

        Returns none.
        '''
        infinitive_phrase = 'to apply'
        view_name = self._select_view(infinitive_phrase=infinitive_phrase)
        if self._session.is_backtracking:
            return
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, view_name)

    def clear_view(self):
        r'''Clears view.

        Set 'view_name' to none in ``__metadata__.py``.

        Returns none.
        '''
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, None)

    def commit_to_repository(self, confirm=True, display=True):
        r'''Commits files to repository.

        Returns none.
        '''
        self._session._attempted_to_commit_to_repository = True
        if self._session.is_repository_test:
            return
        getter = self._io_manager._make_getter()
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._session.is_backtracking:
            return
        if confirm:
            line = 'commit message will be: "{}"'.format(commit_message)
            self._io_manager._display(line)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            if not result:
                return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            manager.commit_to_repository(
                commit_message=commit_message,
                confirm=False,
                display=False,
                )

    def list_views(self):
        r'''Lists views in ``__views__.py``.

        Returns none.
        '''
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            message = 'no views found.'
            self._io_manager._display(message)
            return
        messages = []
        names = list(view_inventory.keys())
        view_count = len(view_inventory)
        view_string = 'view'
        if view_count != 1:
            view_string = stringtools.pluralize(view_string)
        message = '{} {} found:'
        message = message.format(view_count, view_string)
        messages.append(message)
        messages.extend(names)
        self._io_manager._display(messages, capitalize=False)

    def make_view(self):
        r'''Makes view.

        Returns none.
        '''
        from scoremanager import iotools
        getter = self._io_manager._make_getter()
        getter.append_string('view name')
        view_name = getter._run()
        if self._session.is_backtracking:
            return
        menu_entries = self._make_asset_menu_entries(apply_view=False)
        display_strings = [_[0] for _ in menu_entries]
        view = iotools.View(
            items=display_strings,
            )
        breadcrumb = 'views - {} - edit:'
        breadcrumb = breadcrumb.format(view_name)
        autoeditor = self._io_manager._make_autoeditor(
            allow_item_edit=False,
            breadcrumb=breadcrumb,
            target=view,
            )
        autoeditor._run()
        if self._session.is_backtracking:
            return
        view = autoeditor.target
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            view_inventory = datastructuretools.TypedOrderedDict(
                item_class=iotools.View,
                )
        view_inventory[view_name] = view
        self._write_view_inventory(view_inventory)

    def open_views_py(self):
        r'''Opens ``__views__.py``.

        Returns none.
        '''
        if os.path.exists(self._views_py_path):
            self._io_manager.open_file(self._views_py_path)
        else:
            message = 'no __views.py__ found.'
            self._io_manager._display(message)

    def remove_views(self):
        r'''Removes view(s) from ``__views__.py``.

        Returns none.
        '''
        infinitive_phrase = 'to remove'
        view_names = self._select_view(
            infinitive_phrase=infinitive_phrase,
            is_ranged=True,
            )
        if self._session.is_backtracking:
            return
        if not view_names:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        for view_name in view_names:
            if view_name in view_inventory:
                del(view_inventory[view_name])
        self._write_view_inventory(view_inventory)

    def rename_view(self):
        r'''Renames view.

        Returns none.
        '''
        infinitive_phrase = 'to rename'
        old_view_name = self._select_view(infinitive_phrase=infinitive_phrase)
        if self._session.is_backtracking:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        view = view_inventory.get(old_view_name)
        if not view:
            return
        getter = self._io_manager._make_getter()
        getter.append_string('view name')
        new_view_name = getter._run()
        if self._session.is_backtracking:
            return
        del(view_inventory[old_view_name])
        view_inventory[new_view_name] = view
        self._write_view_inventory(view_inventory)

    def repository_clean(self, confirm=True, display=True):
        r'''Removes files not yet added to repository.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.repository_clean(display=display)

    def repository_status(self):
        r'''Displays repository status.

        Returns none.
        '''
        self._session._attempted_repository_status = True
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.repository_status()

    def revert_to_repository(self, confirm=True, display=True):
        r'''Reverts files to repository.

        Returns none.
        '''
        self._session._attempted_to_revert_to_repository = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.revert_to_repository(confirm=False, display=False)

    def update_from_repository(self, confirm=True, display=True):
        r'''Updates files from repository.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            manager.update_from_repository(confirm=False, display=False)