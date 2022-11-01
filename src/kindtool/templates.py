from pathlib import Path
from typing import Dict
from jinja2 import Environment, FileSystemLoader
import os
import shutil

class Templates:
    def __init__(self, dest_dir: Path) -> None:
        self._tpl_path = self._detect_template_path()
        self._dest_dir = os.path.realpath(dest_dir)

    def _detect_template_path(self) -> str:
        # probably better ?
        # https://stackoverflow.com/questions/5897666/how-do-i-use-data-in-package-data-from-source-code
        tpl_dir_basename = "templates"
        file_path = os.path.realpath(__file__)
        file_dir = os.path.dirname(file_path)
        tpl_dir = os.path.join(file_dir, tpl_dir_basename)
        tpl_dir = os.path.abspath(tpl_dir)
        return tpl_dir

    def get_kindfile(self) -> str:
        kindfile = os.path.abspath(os.path.join(self._dest_dir, 'kindfile.yaml'))
        return kindfile

    def get_dest_dir(self) -> str:
        return self._dest_dir

    def copy_file(self, tpl_filename: str, dest_sub_dir: str="",
        mode: int=None) -> None:
        dest_file_path = self._dest_dir

        if dest_sub_dir:
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

    def render_template(self, data: Dict[str,str], tpl_filename: str,
            dest_sub_dir: str, dest_filename: str="", mode: int=None
        ) -> None:
        dest_file_path = os.path.join(self._dest_dir, dest_sub_dir)

        if not dest_filename:
            dest_filename = os.path.basename(tpl_filename)
            dest_filename = dest_filename.replace(".j2", "")

        if not os.path.exists(dest_file_path):
            os.makedirs(dest_file_path)

        dest_file = os.path.realpath(os.path.join(dest_file_path, dest_filename))

        self._render_template(data, tpl_filename, dest_file)

        if mode:
            try:
                Path(dest_file).chmod(mode)
            except Exception:
                # Windows friends
                pass

    def delete_dot_kind_dir(self) -> None:
        kind_dir = os.path.abspath(os.path.join(self.get_dest_dir(), '.kind'))
        shutil.rmtree(kind_dir, ignore_errors=False)
        return None

    def delete_scripts_dir(self) -> None:
        dir = os.path.abspath(os.path.join(self.get_dest_dir(), '.kind/scripts'))
        if os.path.exists(dir):
            shutil.rmtree(dir, ignore_errors=False)
        return None

    def delete_config_dir(self) -> None:
        dir = os.path.abspath(os.path.join(self.get_dest_dir(), '.kind/config'))
        if os.path.exists(dir):
            shutil.rmtree(dir, ignore_errors=False)
        return None

    def _render_template(self, cfg_data: dict[str, str], tpl_filename: str, dest_file: str) -> None:
        # https://ttl255.com/jinja2-tutorial-part-1-introduction-and-variable-substitution/
        # https://stackoverflow.com/questions/69056354/access-jinja2-templates-from-a-folder-outside-of-package

        env = Environment(loader=FileSystemLoader(self._tpl_path))
        tmpl = env.get_template(tpl_filename)
        data = tmpl.render(cfg_data)

        Path(dest_file).write_text(data)