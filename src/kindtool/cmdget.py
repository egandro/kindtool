from kindtool import templates, kindfile
import os

class CmdGet:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._kindfile = kindfile.Kindfile(tpl)

    def get(self, key: str) -> None:
        self._kindfile.throw_if_no_kindfile_found()

        value=''

        if key == 'name':
            value = self._kindfile.cluster_name()
        elif key == 'kubeconfig':
            if self._kindfile.has_local_kubeconfig():
                value = os.path.abspath(os.path.join(self._kindfile.config_dir(), 'config'))
        elif key == 'ingress':
            value = f"{self._kindfile.has_ingress()}"
        elif key == 'ingress_http_port':
            if self._kindfile.has_ingress():
                value = self._kindfile.get_raw('ingress_http_port')
        elif key == 'ingress_https_port':
            if self._kindfile.has_ingress():
                value = self._kindfile.get_raw('ingress_https_port')
        elif key == 'metallb':
            value = f"{self._kindfile.has_metallb()}"
        elif key == 'mountpoints':
            value = self._kindfile.get_raw('mountpoints')
        elif key == 'api_server_address':
            value = self._kindfile.get_raw('api_server_address')
        elif key == 'internal_registry_prefix':
            if self._kindfile.has_internal_registry():
                value = f"localhost:{self._kindfile.get_raw('internal_registry_docker_port')}"
        else:
            raise NotImplementedError(f"key '{key}' not implemented")

        print(value)