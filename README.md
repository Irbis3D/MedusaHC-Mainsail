# MedusaHC Mainsail

Experimental Mainsail distribution with an embedded MedusaHC navigation tab.
The tab opens the independently installed MedusaHC Control service on port
8090, so the control panel remains usable directly when Mainsail is unavailable.

This repository is intentionally independent from `MedusaHC-Control`:

- this repository owns Mainsail integration and web release artifacts;
- `MedusaHC-Control` owns the panel service and the combined installer;
- Moonraker updates both components independently.

## Install

Open an SSH terminal on the printer and run:

```bash
curl -fsSL -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh | bash
```

This opens the common MedusaHC installation menu. The same menu is available
from the MedusaHC Control repository; this small entry point delegates to that
canonical installer so the two copies cannot diverge.

The menu can install the standalone panel, replace the primary Mainsail, or
install MedusaHC Mainsail in parallel. Before modifying `moonraker.conf`, it
prints the exact diff and requests separate approval.

## Pinned upstream build

`upstream.json` records the tested Mainsail version. Build from an already
downloaded official Mainsail release archive:

```bash
python3 build_distribution.py mainsail.zip dist/medusahc-mainsail.zip
```

The builder does not download or publish anything. It writes the release ZIP
and a `.build.json` provenance file containing the source and output SHA-256
hashes. New upstream releases remain candidates until they are tested and a
MedusaHC Mainsail release is explicitly published.
