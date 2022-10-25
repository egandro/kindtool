from typing import Any, Dict

from kindtool import __version__, runner, templates, kindfile

class CmdDestroy:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._kindfile = kindfile.Kindfile(tpl)
        self._runner = runner.Runner()

    def run(self) -> str:
        result = ""
        try:
            if not self._kindfile.has_config():
                result = "cluster is not configured"
            if result:
                return

            args = [
                "delete",
                "cluster",
                "--name", self._kindfile.cluster_name()
            ]

            if not self._runner.kind(args):
                return "can't delete the cluster"

            if self._kindfile.has_internal_registry():
                script = "internal-registry-delete.sh"
                if not self._runner.run_script(self._kindfile.scripts_dir(), script):
                    return f"error running: {script}"

        except Exception as err:
            result = repr(err)
        return result
