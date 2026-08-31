#!/usr/bin/env bash
set -euo pipefail

INSTALLER_URL="https://raw.githubusercontent.com/Irbis3D/MedusaHC-Control/main/install-manager.sh"
temporary="$(mktemp)"
cleanup() { rm -f -- "${temporary}"; }
trap cleanup EXIT

curl -fsSL --connect-timeout 15 --max-time 120 --retry 3 "${INSTALLER_URL}" -o "${temporary}"
bash "${temporary}" "$@"
