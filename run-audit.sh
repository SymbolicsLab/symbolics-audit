#!/bin/bash
# Convenience script to run the audit
# Usage: ./run-audit.sh

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python3 scripts/audit.py
