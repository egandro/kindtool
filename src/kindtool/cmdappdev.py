from kindtool import logger, templates, kindfile
import os

log = logger.getLogger(__name__)

class CmdAppDefinition:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._kindfile = kindfile.Kindfile(tpl)

    def show_app_definition(self) -> None:
        self._kindfile.throw_if_no_kindfile_found()

        value=''

        raise NotImplementedError(f"not implemented")

        print(value)