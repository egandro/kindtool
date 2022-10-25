import subprocess
import os

from typing import List


class Runner:
    def __init__(self) -> None:
        self._kind_cmd = "kind"
        return None

    def kind_is_running(self, cluster_name: str) -> bool:
        # kind get cluster 2>/dev/null | grep ${cluster_name}

        cmd = [self._kind_cmd, "get", "clusters"]
        p = subprocess.Popen(cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL)
        out, _ = p.communicate()

        if p.returncode:
            return False

        if not out:
            return False

        out_str = out.decode('utf-8')
        res = cluster_name in out_str
        return res

    def kind(self, args: List[str]) -> bool:

        cmd = [self._kind_cmd]
        for arg in args:
            cmd.append(arg)

        p = subprocess.Popen(cmd)
        p.communicate()

        if p.returncode:
            return False

        return True

    def run_script(self, scripts_dir: str, script: str) -> bool:
        cmd = []
        cmd.append(os.path.abspath(os.path.join(scripts_dir, script)))

        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

        if p.returncode:
            return False

        return True