#!/bin/sh
# Lancia jobspy_parser.py con il Python dell'ambiente virtuale .venv-jobspy.
# Serve perché career-ops ignora un "command" che punta direttamente al Python del venv
# (il file reale è fuori dalla cartella del progetto). Va in career-ops/local/.
DIR="$(cd "$(dirname "$0")/.." && pwd)"
exec "$DIR/.venv-jobspy/bin/python" "$DIR/local/jobspy_parser.py" "$@"
