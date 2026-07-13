#!/usr/bin/env bash
# One-shot launcher for the Contract Intelligence client demo.
#
# The UI is a fully static Vite bundle that talks directly to the public
# Cloud Run backend. All we need is a local HTTP server to serve the files
# (opening index.html via file:// works too, but some browsers restrict
# fetch() from file:// origins — a real HTTP server avoids that).

set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-8080}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.9+ from https://www.python.org/downloads/"
  exit 1
fi

echo "Contract Intelligence — Client Demo"
echo "-----------------------------------"
echo "Serving ./dist/ at http://localhost:${PORT}"
echo "Backend: https://contract-intelligence-997090888022.us-central1.run.app"
echo "(Ctrl-C to stop)"
echo

exec python3 -m http.server "$PORT" --directory dist --bind 127.0.0.1
