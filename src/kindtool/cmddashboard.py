from kindtool import __version__, runner, templates, kindfile

import os

class CmdDashboard:
    def __init__(self, tpl: templates.Templates, version: str) -> None:
        self._tpl = tpl
        inject = {}
        inject["dashboard_version"] = version
        self._kindfile = kindfile.Kindfile(tpl, inject)
        self._runner = runner.Runner()

    def run(self) -> None:
        self._kindfile.throw_if_no_kindfile_found()

        cluster_name = self._kindfile.cluster_name()
        if not self._runner.kind_is_running(cluster_name):
            print(f"cluster {cluster_name} is no running")
            return

        self._create_content()

        script = "dashboard-install.sh"
        if not self._runner.run_script(self._kindfile.scripts_dir(), script):
            return f"error running: {script}"

    def _create_content(self) -> str:
        cfg_data = self._kindfile.data()
        self._tpl.render_template(cfg_data, "j2/dashboard-install.j2.sh", ".kind/scripts", "", 0o0755)
        self._tpl.render_template(cfg_data, "dashboard-admin-user.yaml", ".kind/config")
        self._tpl.render_template(cfg_data, "dashboard-cluster-admin.yaml", ".kind/config")