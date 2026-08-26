# MedusaHC Mainsail

Experimental Mainsail distribution with an embedded MedusaHC navigation tab.
The tab opens the independently installed MedusaHC Control service on port
8090, so the control panel remains usable directly when Mainsail is unavailable.

This repository is intentionally independent from `MedusaHC-Control`:

- this repository owns Mainsail integration and web release artifacts;
- `MedusaHC-Control` owns the panel service and the combined installer;
- Moonraker updates both components independently.

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

