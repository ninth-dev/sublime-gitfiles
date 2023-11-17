#!/bin/bash
set -euo pipefail

__source="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$__source/.." || exit

plugin_dir="$(pwd)"
plugin_name="$(basename "$plugin_dir")"
plugin_path="${HOME}/Library/Application Support/Sublime Text/Packages/${plugin_name}"

if [[ -L "$plugin_path" ]]; then
  unlink "$plugin_path"
  echo "Unlinked... $plugin_path"
else
  echo "Symlink not found... $plugin_path"
fi
