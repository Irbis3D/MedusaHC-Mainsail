# MedusaHC Mainsail installation

MedusaHC Mainsail is an optional modified Mainsail interface containing an
embedded MedusaHC Control tab. Install MedusaHC Control first. The panel remains
an independent service and stays directly accessible on its own port.

> [!WARNING]
> Do not install, update, remove, or restart printer services during a print.

## Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)"
```

The installer verifies MedusaHC Control and then offers two modes:

1. Replace the primary Mainsail with MedusaHC Mainsail.
2. Install MedusaHC Mainsail in parallel on port `81`.

Before changing `moonraker.conf`, the installer shows the planned change and
asks for separate approval. It creates a backup of the existing Mainsail and
records the installation mode. The panel service, Core, and Calibrate are not
modified.

## Status

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- status
```

## Update

Use the normal Mainsail/Fluidd Update Manager or run:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- update
```

The updater preserves the original pre-installation Mainsail backup. It does
not replace that backup with a copy of the already modified interface.

## Uninstall

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Irbis3D/MedusaHC-Mainsail/main/install.sh)" -- uninstall
```

The uninstaller:

- removes the MedusaHC Mainsail files;
- removes only its managed nginx and Moonraker changes;
- restores the original primary Mainsail in replacement mode, or restores the
  previous parallel-path state in parallel mode;
- keeps MedusaHC Control, Core, Calibrate, and all panel data.

Removal requires confirmation and refuses to delete unrelated nginx
configuration.

## Local installation

From a clone, run the Python manager directly:

```bash
sudo python3 installer/manager.py install
```

Use `--mode replace` or `--mode parallel` to select a mode without the mode
prompt. The same manager accepts `status`, `update`, and `uninstall`.
