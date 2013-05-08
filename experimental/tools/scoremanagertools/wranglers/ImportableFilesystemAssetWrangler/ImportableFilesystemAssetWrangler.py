import os
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler


class ImportableFilesystemAssetWrangler(FilesystemAssetWrangler):

    def __init__(self,
        system_asset_container_directory_paths=None,
        system_asset_container_package_paths=None,
        user_asset_container_directory_paths=None,
        user_asset_container_package_paths=None,
        score_internal_asset_container_package_path_infix=None,
        session=None,
        ):
        FilesystemAssetWrangler.__init__(self,
            system_asset_container_directory_paths=system_asset_container_directory_paths,
            system_asset_container_package_paths=system_asset_container_package_paths,
            user_asset_container_directory_paths=user_asset_container_directory_paths,
            user_asset_container_package_paths=user_asset_container_package_paths,
            score_internal_asset_container_package_path_infix=score_internal_asset_container_package_path_infix,
            session=session,
            )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def temporary_asset_package_path(self):
        if self.current_asset_container_package_path:
            return '.'.join([
                self.current_asset_container_package_path,
                self._temporary_asset_name])
        else:
            return self._temporary_asset_name

    ### PUBLIC METHODS ###

    def list_asset_package_paths(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_package_paths(head=head))
        result.extend(self.list_score_internal_asset_package_paths(head=head))
        result.extend(self.list_user_asset_package_paths(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for package_path in self.list_asset_package_paths(head=head):
            asset_proxy = self.get_asset_proxy(package_path)
            result.append(asset_proxy)
        return result

    def list_score_external_asset_package_paths(self, head=None):
        result = []
        for directory_path in self.list_score_external_asset_container_directory_paths(head=head):
            for directory_entry in os.listdir(directory_path):
                package_path = packagepathtools.filesystem_path_to_package_path(directory_path)
                if directory_entry[0].isalpha():
                    result.append('.'.join([package_path, directory_entry]))
        return result

    def list_score_internal_asset_package_paths(self, head=None):
        result = []
        for asset_container_package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            if self.score_internal_asset_container_package_path_infix:
                asset_filesystem_path = packagepathtools.package_path_to_directory_path(
                    asset_container_package_path)
                for name in os.listdir(asset_filesystem_path):
                    if name[0].isalpha():
                        package_name = self.strip_file_extension_from_file_name(name)
                        result.append('{}.{}'.format(
                            asset_container_package_path, package_name))
            else:
                result.append(asset_container_package_path)
        return result

    def list_user_asset_package_paths(self, head=None):
        result = []
        for asset_filesystem_path in self.list_user_asset_container_directory_paths(head=head):
            for name in os.listdir(asset_filesystem_path):
                if name[0].isalpha():
                    result.append('.'.join([self.configuration.user_material_package_makers_package_path, name]))
        return result

    # TODO: try to reimplement without proxy instantiation
    def list_visible_asset_package_paths(self, head=None):
        result = []
        for asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(asset_proxy.package_path)
        return result

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_package_paths(head=head)
        bodies = self.list_visible_asset_space_delimited_lowercase_names(head=head)
        return zip(keys, bodies)
