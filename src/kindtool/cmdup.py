from typing import Any, Dict

from kindtool import __version__, runner, templates, kindfile

class CmdUp:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._kindfile = kindfile.Kindfile(tpl)
        self._runner = runner.Runner()

    def run(self) -> None:
        self._kindfile.throw_if_no_kindfile_found()

        cluster_name = self._kindfile.cluster_name()
        if self._runner.kind_is_running(cluster_name):
            print(f"cluster {cluster_name} is already running")
            return

        self._create_content()

        if self._kindfile.has_internal_registry():
            script = "internal-registry-create.sh"
            if not self._runner.run_script(self._kindfile.scripts_dir(), script):
                print(f"error running: {script}")
                return

        args = [
            "create",
            "cluster",
            "--config", self._kindfile.config_yaml(),
            "--name", self._kindfile.cluster_name()
        ]

        if self._kindfile.has_local_kubeconfig():
            args.append("--kubeconfig")
            args.append(self._kindfile.kubeconfig())

        if not self._runner.kind(args):
            return "can't start the cluster"

        if self._kindfile.has_internal_registry():
            script = "internal-registry-connect.sh"
            if not self._runner.run_script(self._kindfile.scripts_dir(), script):
                return f"error running: {script}"

        if self._kindfile.has_ingress():
            script = "ingress-install.sh"
            if not self._runner.run_script(self._kindfile.scripts_dir(), script):
                return f"error running: {script}"

        if self._kindfile.has_metallb():
            script = "metallb-install.sh"
            if not self._runner.run_script(self._kindfile.scripts_dir(), script):
                return f"error running: {script}"
            script = "update-metallb-ipaddresspool.sh"
            if not self._runner.run_script(self._kindfile.scripts_dir(), script):
                return f"error running: {script}"


    def _create_content(self) -> str:
        self._tpl.delete_scripts_dir()
        self._tpl.delete_config_dir()

        cfg_data = self._kindfile.data()

        self._render_tpl_configs(cfg_data)

    def _render_tpl_configs(self, cfg_data: dict[str, str]) -> None:
        self._tpl.render_template(cfg_data, "j2/config.j2.yaml", ".kind/config")
        self._tpl.render_template(cfg_data, "j2/dot_gitignore.j2", ".kind", ".gitignore")

        key = "internal_registry"
        if key in cfg_data and cfg_data[key]:
            self._tpl.render_template(cfg_data, "j2/internal-registry-connect.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "j2/internal-registry-create.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "j2/internal-registry-delete.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "j2/internal-registry.j2.yaml", ".kind/config")

        key = "ingress"
        if key in cfg_data and cfg_data[key]:
            self._tpl.render_template(cfg_data, "j2/ingress-install.j2.sh", ".kind/scripts", "", 0o0755)

        key = "metallb"
        if key in cfg_data and cfg_data[key]:
            self._tpl.render_template(cfg_data, "j2/metallb-install.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "j2/update-metallb-ipaddresspool.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "metallb-config.tpl.yaml", ".kind/config")

        return None