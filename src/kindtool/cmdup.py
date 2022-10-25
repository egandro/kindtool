from typing import Any, Dict

from kindtool import __version__, templates, kindfile

class CmdUp:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._kindfile = kindfile.Kindfile(tpl)

    def run(self) -> str:
        result = ""
        try:
            if not self._kindfile.has_config():
                result = self._create_content()
            if result:
                return
        except Exception as err:
            result = repr(err)
        return result

    def _create_content(self) -> str:
        result = ""
        try:
            cfg_data = self._kindfile.data()
            self._render_tpl_configs(cfg_data)
        except Exception as err:
            result = repr(err)
        return result

    def _render_tpl_configs(self, cfg_data: dict[str, str]) -> None:
        self._tpl.render_template(cfg_data, "j2/config.j2.yaml", ".kind/config")

        key = "internal_registry"
        if key in cfg_data and cfg_data[key]:
            self._tpl.render_template(cfg_data, "j2/internal-registry-connect.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "j2/internal-registry-create.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "j2/internal-registry.j2.yaml", ".kind/config")

        key = "loadbalancer"
        if key in cfg_data and cfg_data[key]:
            self._tpl.render_template(cfg_data, "j2/update-metallb-ipaddresspool.j2.sh", ".kind/scripts", "", 0o0755)
            self._tpl.render_template(cfg_data, "metallb-config.tpl.yaml", ".kind/config")

        return None