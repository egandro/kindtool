from kindtool import templates

class ConfigInit:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl

    def create_content(self) -> str:
        result = ""
        try:
            self._tpl.copy_file("cluster-configuration", "config")
        except Exception as err:
            result = str(err)
        return result
