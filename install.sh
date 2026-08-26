#!/usr/bin/env bash
set -euo pipefail

INSTALLER_URL="https://raw.githubusercontent.com/Irbis3D/MedusaHC-Control/python-controller/install-manager.sh"
temporary="$(mktemp)"
cleanup() { rm -f -- "${temporary}"; }
trap cleanup EXIT

curl -fsSL -H 'Cache-Control: no-cache' "${INSTALLER_URL}" -o "${temporary}"
bash "${temporary}" "$@"
