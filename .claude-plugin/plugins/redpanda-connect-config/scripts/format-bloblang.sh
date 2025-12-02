#!/bin/bash
# Format bloblang functions or methods metadata from jsonschema output
# Usage: ./format-bloblang.sh <category>
# Examples:
#   ./format-bloblang.sh bloblang-functions
#   ./format-bloblang.sh bloblang-methods

set -euo pipefail

CATEGORY="$1"  # "bloblang-functions" or "bloblang-methods"

# Validate category
if [[ "$CATEGORY" != "bloblang-functions" && "$CATEGORY" != "bloblang-methods" ]]; then
    echo "Error: CATEGORY must be 'bloblang-functions' or 'bloblang-methods'" >&2
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Fetch jsonschema for ALL items and pipe to Python formatter
rpk connect list --format jsonschema "$CATEGORY" | python3 "$SCRIPT_DIR/format-bloblang.py"
