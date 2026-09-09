# Mainsail 2.19.0 stable update

Release: `v2.19.0-medusahc.0.1.2`.
Stable fallback: `v2.18.2-medusahc.0.1.1`.

This builds the MedusaHC navigation integration on the official Mainsail
2.19.0 archive. The independent Control service and printer configuration
are not replaced. The installer accepts `update --release TAG` for explicit
candidate testing or returning to an older release. Normal updates still
use the latest stable GitHub release.

Upstream changes include macro sorting/search fixes, preset editing fixes,
console and heightmap performance improvements, editor grammar changes,
G-code viewer updates, translations and dependency updates.
See https://github.com/mainsail-crew/mainsail/releases/tag/v2.19.0.

## Install the update

While the printer is idle, run in an SSH terminal:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- update
```

Reload the browser with Ctrl+F5. This updates an existing MedusaHC Mainsail
installation in its current replace/parallel mode. It preserves the original
pre-install backup. The ordinary installer Update action now selects this
stable release. Existing RC1 installations can use the same update command.

## Printer validation

- Confirm Mainsail loads and connects to Moonraker without new errors.
- Open MedusaHC, confirm tool states and running/saved settings load.
- Navigate back to Dashboard, Console and Machine; check the panel hides.
- Open a configuration file and inspect the editor without saving changes.
- Check the macro list, G-code viewer and navigation on the screen sizes used.
- Verify the independent Control URL still works.

The owner tested RC1 on the printer and reported that it works, approving
promotion to stable. This release uses the same application and integration
files as RC1; only the release version metadata changes. The checks above
remain a useful checklist after installation.

Local validation: 13 tests passed, including explicit/stable release selection,
failed-update rollback in both installation modes, configuration editing and
installer cleanup. Shell and integration JavaScript syntax checks passed.
The source archive SHA-256 matches the official GitHub release digest:
`c4d9d96f89851c6ae0709c2f20725447f3fe8c57cf193869b0083441bd93378a`.
198 upstream files are byte-identical. Only `index.html` and `release_info.json`
are modified, and `mainsail-medusahc.js` is added.

## Return to the previous stable build

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- update --release v2.18.2-medusahc.0.1.1
```

Reload with Ctrl+F5. Uninstall is not needed for this rollback.
