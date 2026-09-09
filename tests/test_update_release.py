import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from installer import manager


class ReleaseDownloadTests(unittest.TestCase):
    def test_stable_and_explicit_tag_use_separate_endpoints(self):
        for tag in (None, "v2.19.0-medusahc.0.1.2-rc.1"):
            with self.subTest(tag=tag), tempfile.TemporaryDirectory() as temporary:
                payload = io.BytesIO()
                with zipfile.ZipFile(payload, "w") as archive:
                    archive.writestr("index.html", "candidate")
                release = {"tag_name": tag or "stable", "assets": [{
                    "name": manager.RELEASE_ASSET,
                    "browser_download_url": "https://example.invalid/candidate.zip"}]}
                with patch.object(manager.urllib.request, "urlopen", side_effect=[
                    io.BytesIO(json.dumps(release).encode()), io.BytesIO(payload.getvalue())
                ]) as request:
                    result = manager.download_mainsail_release(Path(temporary) / "release.zip", tag)
                endpoint = request.call_args_list[0].args[0].full_url
                self.assertTrue(endpoint.endswith("/latest" if tag is None else "/tags/" + tag))
                self.assertEqual(result, tag or "stable")


class UpdateTests(unittest.TestCase):
    def test_update_and_failure_preserve_original_backup(self):
        for mode in ("replace", "parallel"):
            for failure in (False, True):
                with self.subTest(mode=mode, failure=failure), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    standard, parallel = root / "mainsail", root / "mainsail-medusahc"
                    target = standard if mode == "replace" else parallel
                    target.mkdir()
                    (target / "index.html").write_text("old version")
                    original = root / "original-backup.tar.gz"
                    original.write_bytes(b"original pre-install backup")
                    manifest = {"mainsail": {"installed": True, "mode": mode,
                        "path": str(target), "backup": str(original)}}
                    def download(destination, release_tag):
                        self.assertEqual(release_tag, "candidate")
                        with zipfile.ZipFile(destination, "w") as archive:
                            archive.writestr("index.html", "new version")
                        return release_tag
                    def replace(archive, destination, uid, gid):
                        (destination / "index.html").write_text("new version")
                        if failure:
                            raise RuntimeError("simulated replacement failure")
                    with patch.object(manager, "require_root"), \
                         patch.object(manager, "load_manifest", return_value=manifest), \
                         patch.object(manager, "paths", return_value={"standard": standard, "parallel": parallel, "uid": 1, "gid": 1}), \
                         patch.object(manager, "panel_port", return_value=8090), \
                         patch.object(manager, "confirm", return_value=True), \
                         patch.object(manager, "download_mainsail_release", side_effect=download), \
                         patch.object(manager, "install_tree", side_effect=replace), \
                         patch.object(manager, "save_manifest") as save:
                        if failure:
                            with self.assertRaisesRegex(RuntimeError, "replacement failure"):
                                manager.update_mainsail("candidate")
                            save.assert_not_called()
                        else:
                            manager.update_mainsail("candidate")
                            self.assertEqual(save.call_args.args[0]["mainsail"]["archive"], "candidate")
                    self.assertEqual((target / "index.html").read_text(), "old version" if failure else "new version")
                    self.assertEqual(original.read_bytes(), b"original pre-install backup")
