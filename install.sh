#!/usr/bin/env bash
set -euo pipefail

REPOSITORY="${MEDUSAHC_MAINSAIL_REPOSITORY:-Irbis3D/MedusaHC-Mainsail}"
REPOSITORY_REF="${MEDUSAHC_MAINSAIL_REF:-main}"
PACKAGE_URL="${MEDUSAHC_MAINSAIL_PACKAGE_URL:-https://api.github.com/repos/${REPOSITORY}/tarball/${REPOSITORY_REF}}"
temporary="$(mktemp -d /tmp/medusahc-mainsail-install.XXXXXX)"
cleanup() { rm -rf -- "${temporary}"; }
trap cleanup EXIT

command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
command -v tar >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 1; }

package="${temporary}/source.tar.gz"
source_directory="${temporary}/source"
mkdir -p "${source_directory}"
curl -fL --retry 3 --connect-timeout 15 "${PACKAGE_URL}" -o "${package}"
tar -xzf "${package}" -C "${source_directory}" --strip-components=1

action="${1:-install}"
if [[ "$#" -gt 0 ]]; then shift; fi
case "${action}" in
  install|update|uninstall|status) ;;
  *) echo "Usage: $0 [install|update|uninstall|status]" >&2; exit 2 ;;
esac

if [[ "${action}" == "status" ]]; then
  exec python3 "${source_directory}/installer/manager.py" status "$@"
fi
if [[ "${EUID}" -eq 0 ]]; then
  exec python3 "${source_directory}/installer/manager.py" "${action}" "$@"
else
  exec sudo python3 "${source_directory}/installer/manager.py" "${action}" "$@"
fi
