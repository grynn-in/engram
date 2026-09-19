# shellcheck shell=bash
#
# Bash view of the Engram layer registry. Sourced, never executed.
#
# The registry itself lives in layers.py — this file only forwards to it, so
# bash and Python commands can never disagree about which layers exist.
#
# Usage:
#   source "$SCRIPT_DIR/../lib/layers.sh"
#   for layer in $(engram_layers all); do ...; done
#   engram_layers transferable
#   engram_protocol_block > /tmp/block.md
#
# Sets: all, curated, searchable, transferable, shared, session, append_only

ENGRAM_LIB_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

# engram_layers [set] — print the layer names in a set, one per line.
# Exits non-zero (and explains) on an unknown set, so a typo fails loudly
# rather than silently iterating over nothing.
engram_layers() {
  python3 "$ENGRAM_LIB_DIR/layers.py" "${1:-all}"
}

# engram_layers_csv [set] — the same names as "a, b, c" for messages.
engram_layers_csv() {
  # paste cycles through a multi-char delimiter list, so join on ',' alone
  # and widen afterwards.
  engram_layers "${1:-all}" | paste -sd',' - | sed 's/,/, /g'
}

# engram_layers_brace [set] — the same names as "{a,b,c}" for mkdir -p.
engram_layers_brace() {
  printf '{%s}' "$(engram_layers "${1:-all}" | paste -sd',' -)"
}

# engram_protocol_block — the "## Engram" section for a project's CLAUDE.md.
engram_protocol_block() {
  python3 "$ENGRAM_LIB_DIR/layers.py" --protocol
}

# engram_layer_count — number of layers including CLAUDE.md (core identity).
engram_layer_count() {
  python3 "$ENGRAM_LIB_DIR/layers.py" --count
}
