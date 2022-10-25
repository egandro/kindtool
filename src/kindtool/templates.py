from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import os
import shutil

class Templates:
    def __init__(self) -> None:
        self._tpl_path = self._detect_template_path()
        self._dest_dir = None

    def _detect_template_path(self) -> str:
        file_path = os.path.realpath(__file__)
        file_dir = os.path.dirname(file_path)
        upper = os.path.dirname(os.path.dirname(file_dir)) # 2 level up
        tpl_dir = os.path.join(upper, "kindtool_templates")
        return tpl_dir

    def get_cluster_config_file(self) -> str:
        cfg = os.path.join(self._dest_dir, 'config')
        cfg = os.path.join(cfg, 'cluster-configuration')
        return cfg

    def has_valid_dest_dir(self, dest_dir: Path) -> str:
        self._dest_dir = dest_dir
        file_path = os.path.realpath(self._dest_dir)

        if not os.path.exists(file_path):
            return f"error: directory '{file_path}' does not exists."

        if not os.path.exists(self.get_cluster_config_file()):
            return f"error: directory '{file_path}' has no file 'config/cluster-configuration'."

        return ""

    def prepare_dest_dir(self, dest_dir: Path) -> str:
        self._dest_dir = dest_dir
        file_path = os.path.realpath(self._dest_dir)

        if os.path.exists(file_path):
            return f"error: directory '{file_path}' already exists."

        result=""
        try:
            os.makedirs(file_path)
            # this is now the main path
            self._dest_dir = file_path
        except Exception as err:
            result = str(err)
        return result

    def get_dest_dir(self) -> str:
        return self._dest_dir

    def copy_file(self, tpl_filename: str, dest_sub_dir: str, mode: any=None) -> None:
        dest_file_path = os.path.join(self._dest_dir, dest_sub_dir)

        if not os.path.exists(dest_file_path):
            os.makedirs(dest_file_path)

        src_file = os.path.join(self._tpl_path, tpl_filename)

        dest_file = os.path.join(dest_file_path, os.path.basename(tpl_filename))
        dest_file = os.path.realpath(dest_file)

        shutil.copyfile(src_file, dest_file)

        if mode:
            try:
                Path(dest_file).chmod(mode)
            except Exception:
                # Windows friends
                pass

    def render_template(self, yaml_var_file: str, tpl_filename: str, dest_sub_dir: str, dest_filename: str) -> None:
        dest_file_path = os.path.join(self._dest_dir, dest_sub_dir)

        if not os.path.exists(dest_file_path):
            os.makedirs(dest_file_path)

        dest_file = os.path.join(dest_file_path, dest_filename)
        dest_file = os.path.realpath(dest_file)

        self._render_template(yaml_var_file, tpl_filename, dest_file)

    def _render_template(self, cfg_data: dict[str, str], tpl_filename: str, dest_file: str) -> None:
        # https://ttl255.com/jinja2-tutorial-part-1-introduction-and-variable-substitution/
        # https://stackoverflow.com/questions/69056354/access-jinja2-templates-from-a-folder-outside-of-package

        env = Environment(loader=FileSystemLoader(self._tpl_path))
        tmpl = env.get_template(tpl_filename)
        dest = tmpl.render(cfg_data)

        Path(dest_file).write_text(dest)