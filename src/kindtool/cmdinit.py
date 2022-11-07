from kindtool import logger, templates
import os

log = logger.getLogger(__name__)

class CmdInit:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl

    def create_content(self) -> None:
        kind_filename = self._tpl.get_kindfile()
        log.debug(f"using kindfile: {kind_filename}")

        if os.path.exists(kind_filename):
            raise FileExistsError(f"kindfile.yaml exists {kind_filename}")

        self._tpl.copy_file(tpl_filename="kindfile.yaml")
