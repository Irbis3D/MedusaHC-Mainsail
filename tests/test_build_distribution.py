import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_distribution import build


class MainsailBuildTests(unittest.TestCase):
    def test_build_injects_integration_and_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "mainsail.zip"
            output = root / "medusahc-mainsail.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("index.html", "<html><body>ok</body></html>")
            result = build(source, output)
            with zipfile.ZipFile(output) as archive:
                self.assertIn("mainsail-medusahc.js", archive.namelist())
                self.assertIn("mainsail-medusahc.js", archive.read("index.html").decode())
                release = json.loads(archive.read("release_info.json"))
                self.assertEqual(release["project_name"], "medusahc-mainsail")
            self.assertEqual(result["output"], str(output))
            self.assertTrue(output.with_suffix(".zip.build.json").is_file())

    def test_unsafe_archive_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "unsafe.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("../outside", "bad")
            with self.assertRaises(SystemExit):
                build(source, root / "output.zip")


if __name__ == "__main__":
    unittest.main()

