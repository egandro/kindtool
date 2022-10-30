from kindtool import __version__, runner, templates, kindfile

import os

class CmdShell:
    def __init__(self, tpl: templates.Templates, pod: str, namespace: str, image: str, command: str) -> None:
        self._tpl = tpl
        inject = {}
        inject["shell_podname"] = pod
        inject["shell_namespace"] = namespace
        inject["shell_image"] = image
        inject["shell_command"] = command
        self._kindfile = kindfile.Kindfile(tpl, inject)
        self._runner = runner.Runner()

    def create_or_attach(self) -> None:
        self._kindfile.throw_if_no_kindfile_found()

        cluster_name = self._kindfile.cluster_name()
        if not self._runner.kind_is_running(cluster_name):
            print(f"cluster {cluster_name} is no running")
            return

        self._create_content()

        script = "shell-install.sh"
        if not self._runner.run_script(self._kindfile.scripts_dir(), script):
            return f"error running: {script}"

    def kill(self) -> None:
        self._kindfile.throw_if_no_kindfile_found()

        cluster_name = self._kindfile.cluster_name()
        if not self._runner.kind_is_running(cluster_name):
            print(f"cluster {cluster_name} is no running")
            return

        self._create_content()

        script = "shell-delete.sh"
        if not self._runner.run_script(self._kindfile.scripts_dir(), script):
            return f"error running: {script}"

    def _create_content(self) -> str:
        cfg_data = self._kindfile.data()
        self._tpl.render_template(cfg_data, "j2/shell-install.j2.sh", ".kind/scripts", "", 0o0755)
        self._tpl.render_template(cfg_data, "j2/shell-delete.j2.sh", ".kind/scripts", "", 0o0755)