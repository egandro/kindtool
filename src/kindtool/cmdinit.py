from kindtool import templates
import os

class CmdInit:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl

    def create_content(self) -> None:
        kind_filename = self._tpl.get_kindfile()
        if os.path.exists(kind_filename):
            raise FileExistsError(f"Kindfile exists {kind_filename}")

        self._tpl.copy_file(tpl_filename="Kindfile", fail_if_exists=True)
