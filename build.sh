#!/usr/bin/env bash
# Build script for the Dyslexic Firefox extension.
# Packages the extension/ directory into a .zip that can be loaded in Firefox.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXT_DIR="$SCRIPT_DIR/extension"
OUTPUT="$SCRIPT_DIR/dyslexic-firefox.zip"

if [ ! -f "$EXT_DIR/manifest.json" ]; then
  echo "Error: manifest.json not found in $EXT_DIR"
  exit 1
fi

# Remove old build
rm -f "$OUTPUT"

# Package the extension
cd "$EXT_DIR"
zip -r "$OUTPUT" . -x '.*'

echo ""
echo "✅ Extension built: $OUTPUT"
echo ""
echo "To install in Firefox:"
echo "  1. Open Firefox and go to about:debugging"
echo "  2. Click 'This Firefox' > 'Load Temporary Add-on'"
echo "  3. Select the file: $OUTPUT"
