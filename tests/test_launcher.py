import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


class LauncherCacheTests(unittest.TestCase):
    def test_manager_imports_do_not_create_cache_in_downloaded_source(self):
        script = (Path(__file__).parents[1] / "install.sh").read_text()
        commands = [shlex.split(line.strip()) for line in script.splitlines()
                    if line.strip().startswith(("python3 ", "sudo python3 "))]
        self.assertEqual(len(commands), 3)
        for command in commands:
            for result_code in (0, 7):
                with self.subTest(command=command, result_code=result_code), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    source = root / "installer"
                    source.mkdir()
                    (source / "config_edit.py").write_text("value = 42\n")
                    (source / "manager.py").write_text(
                        "import config_edit\nimport sys\n"
                        "assert config_edit.value == 42\n"
                        "raise SystemExit(int(sys.argv[-1]))\n")
                    # Exercise each actual launch command with this interpreter
                    # and a harmless manager importing a neighboring module.
                    argv = command[1:] if command[0] == "sudo" else command[:]
                    argv = [sys.executable if arg == "python3" else
                            str(source / "manager.py") if arg.endswith("/manager.py") else
                            "update" if arg == "${action}" else
                            str(result_code) if arg == "$@" else arg for arg in argv]
                    env = {key: value for key, value in os.environ.items()
                           if key not in {"PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX"}}
                    result = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, result_code, result.stderr)
                    self.assertFalse(list(source.rglob("*.pyc")), "Privileged imports would leave root-owned cache files")
                    self.assertFalse((source / "__pycache__").exists())
