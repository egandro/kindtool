import yaml
import os
from subprocess import check_output
from typing import Any, Dict

from kindtool import __version__, templates

class Kindfile:
    def __init__(self, tpl: templates.Templates, inject: Dict[str, str] = {}) -> None:
        self._tpl = tpl
        self._cfg = ClusterConfig(tpl)
        self._data = None
        self._inject = inject

    def throw_if_no_kindfile_found(self) -> None:
        kind_filename = self._tpl.get_kindfile()
        if not os.path.exists(kind_filename):
            raise FileNotFoundError(f"kindfile.yaml not found {kind_filename}")

    def data(self) -> Dict[str, str]:
        if not self._data:
            self._cfg.parse(self._inject)
            self._data = self._cfg.data()
        return self._data

    def has_config(self) -> bool:
        config_yml = self.config_yaml()
        res = os.path.exists(config_yml)
        return res

    def kubeconfig(self) -> str:
        config_dir = self.config_dir()

        if not config_dir:
            return ""

        res = os.path.abspath(os.path.join(config_dir, 'config'))
        return res

    def config_yaml(self) -> str:
        config_dir = self.config_dir()

        if not config_dir:
            return ""

        res = os.path.abspath(os.path.join(config_dir, 'config.yaml'))
        return res

    def scripts_dir(self) -> str:
        res = os.path.abspath(os.path.join(self._tpl.get_dest_dir(), '.kind/scripts'))
        return res

    def config_dir(self) -> str:
        key = 'config_dir'
        config_dir = self.get_raw(key)
        res = os.path.abspath(config_dir)
        return res

    def cluster_name(self) -> str:
        key = 'cluster_name'
        return self.get_raw(key)

    def has_local_kubeconfig(self) -> bool:
        key = 'local_kubeconfig'
        return self.get_raw(key)

    def has_internal_registry(self) -> bool:
        key = 'internal_registry'
        return self.get_raw(key)

    def has_ingress(self) -> bool:
        key = 'ingress'
        return self.get_raw(key)

    def has_metallb(self) -> bool:
        key = 'metallb'
        return self.get_raw(key)

    def get_raw(self, key: str) -> str:
        data = self.data()

        if key not in data:
            return ""

        res = data[key]
        return res

class ClusterConfig:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._data = {}

    def parse(self, inject: Dict[str, Any] = {}) -> None:

        with open(self._tpl.get_kindfile(), "r") as stream:
            self._data = yaml.safe_load(stream)

        # inject data not in kindfile.yaml
        for key in inject:
            value = inject[key]
            self._data[key] = value

        # patch a few things
        self._update_api_server_address()
        self._update_config_dir()

        key = "mountpoints"
        if self.getboolean(key):
            self._update_mount_dir()

        key = "cluster_name"
        self._data[key] = self.get(key, "kind")

        key = "internal_registry"
        if self.getboolean(key):
            key = "internal_registry_docker_name"
            self._data[key] = self._data["cluster_name"]  + "-registry"
            key = "internal_registry_docker_port"
            self._data[key] = self.getint(key, 5001)

        key = "ingress"
        if self.getboolean(key):
            key = "ingress_http_port"
            self._data[key] = self.getint(key, 8000)
            key = "ingress_https_port"
            self._data[key] = self.getint(key, 8443)

        key = "worker_nodes"
        self._data[key] = self.getint(key, 0)

        # inject our version
        key = "kindtool_version"
        self._data[key] = __version__


    def data(self) -> dict[str, Any]:
        return self._data

    def get(self, key: str, default: str = "") -> str:
        if key in self._data:
            if self._data[key] != None and str(self._data[key]).lower() != "none":
                return self._data[key]
        self._data[key] = default
        return self._data[key]

    def getboolean(self, key: str, default: bool = False) -> bool:
        if key in self._data:
            if self._data[key] != None and str(self._data[key]).lower() != "none":
                return self._data[key]
        self._data[key] = default
        return self._data[key]

    def getint(self, key: str, default: int = 0) -> int:
        if key in self._data:
            if self._data[key] != None and str(self._data[key]).lower() != "none":
                return self._data[key]
        self._data[key] = default
        return self._data[key]

    def getfloat(self, key: str, default: float = 0) -> float:
        if key in self._data:
            if self._data[key] != None and str(self._data[key]).lower() != "none":
                return self._data[key]
        self._data[key] = default
        return self._data[key]

    def _update_config_dir(self) -> str:
        key = "config_dir"
        value = self.get(key, "")
        if not value:
            value = os.path.realpath(os.path.join(self._tpl.get_dest_dir(), ".kind/config"))
        #value = os.path.abspath(value)
        self._data[key] = value

    def _update_mount_dir(self) -> str:
        key = "mount_dir"
        value = self.get(key, "")
        if not value:
            value = os.path.realpath(os.path.join(self._tpl.get_dest_dir(), ".kind/data"))
            self._data[key] = value
            # this enforces our automatic generated dir to be 755 and our user
            os.makedirs(value, exist_ok=True)

    def _update_api_server_address(self) -> None:
        key = "api_server_address"
        value = self.get(key, "")
        if not value:
            value = self._get_ip()
            self._data[key] = value

    def _get_ip(self):
        ip = "127.0.0.1"
        try:
            # bash style of getting a "cool" ip address
            # will fail on macOS / Windows / and a lot of Linux versions - help is welcome!
            ips = check_output(['hostname', '--all-ip-addresses'])
            ips = ips.decode('ascii')
            ip_arr = ips.split()
            ip = ip_arr[0]
        except Exception:
            # bad luck...
            pass
        return ip
