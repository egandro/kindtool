from kindtool import templates

class CmdInit:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl

    def create_content(self) -> str:
        result = ""
        try:
            self._tpl.copy_file("Kindfile")
        except Exception as err:
            result = repr(err)
        return result