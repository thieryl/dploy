"""
The logic and workings behind the link sub-commands
"""

import dploy.actions as actions
import dploy.utils as utils
import dploy.errors as errors
import dploy.main as main

# pylint: disable=too-few-public-methods
class Link(main.AbstractBaseSubCommand):
    """
    Concrete class implementation of the link sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("link", [source], dest, is_silent, is_dry_run, ignore_patterns)

    def _is_valid_input(self, sources, dest):
        """
        Check to see if the input is valid
        """
        return LinkInput(self.errors, self.subcmd).is_valid(sources, dest)


    def _collect_actions(self, source, dest):
        """
        Concrete method to collect required actions to perform a link
        sub-command
        """

        if dest.exists():
            if utils.is_same_file(dest, source):
                self.actions.add(actions.AlreadyLinked(self.subcmd, source, dest))
            else:
                self.errors.add(errors.ConflictsWithExistingFile(self.subcmd, source, dest))
        elif dest.is_symlink():
            self.errors.add(errors.ConflictsWithExistingLink(self.subcmd, source, dest))

        elif not dest.parent.exists():
            self.errors.add(errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest.parent))

        else:
            self.actions.add(actions.SymbolicLink(self.subcmd, source, dest))


class LinkInput(main.Input):
    """
    Input validator for the link command
    """

    def __init__(self, errors, subcmd):
        """
        """
        super().__init__(errors, subcmd)

    def _is_valid_dest(self, dest):
        if not dest.parent.exists():
            self.errors.add(errors.NoSuchFileOrDirectory(self.subcmd, dest.parent))
            return False

        elif (not utils.is_file_writable(dest.parent)
              or not utils.is_directory_writable(dest.parent)):
            self.errors.add(errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
            return False

        else:
            return True

    def _is_valid_source(self, source):
        if not source.exists():
            self.errors.add(errors.NoSuchFileOrDirectory(self.subcmd, source))
            return False

        elif (not utils.is_file_readable(source)
              or not utils.is_directory_readable(source)):
            self.errors.add(errors.InsufficientPermissions(self.subcmd, source))
            return False

        else:
            return True