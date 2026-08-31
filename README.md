# MedusaHC Mainsail

> [!IMPORTANT]
> **[Installation, updates, removal, and manual setup](INSTALLATION.md)**

Experimental Mainsail distribution with an embedded MedusaHC navigation tab.
The tab opens the independently installed MedusaHC Control service through the
same-origin `/medusahc/` route. The installer proxies only that isolated path
to the panel's configured local port, while direct access to the panel port
remains available when Mainsail is unavailable.

This repository is intentionally independent from `MedusaHC-Control`:

- this repository owns Mainsail integration and web release artifacts;
- `MedusaHC-Control` owns only the independently installed panel service;
- Moonraker updates both components independently.

## Install

Open an SSH terminal on the printer and run:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)"
```

This starts the standalone MedusaHC Mainsail installer. It first verifies that
MedusaHC Control is installed, then asks whether to replace the primary
Mainsail or install the modified interface in parallel.

Update, status and removal use the same entry point:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- update
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- status
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- uninstall
```

The installer manages only this Mainsail integration. It can replace the primary
Mainsail, install MedusaHC Mainsail in parallel, show status, or remove the mod
and restore the previous Mainsail. It never installs, updates, or removes the
standalone MedusaHC Control panel. Before modifying `moonraker.conf`, it prints
the exact diff and requests separate approval.

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
