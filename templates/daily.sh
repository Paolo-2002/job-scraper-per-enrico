#!/bin/bash
# Routine giornaliera: scansione (senza costi AI) + valutazione con Codex.
# Va in career-ops/local/. Lanciato da launchd (Mac) o dall'Utilità di pianificazione via WSL (Windows).
# Per provarlo a mano: bash local/daily.sh (sempre bash, non sh), fuori dalla sandbox di Codex.
# Prima di usarlo verifica con `codex exec --help` che le opzioni qui sotto esistano nella tua versione di Codex.
# Non aggiungere mai --verify a scan.mjs: scarterebbe per sempre le offerte JobSpy (local:jds/...).

set -u
cd "$(dirname "$0")/.." || exit 1
LOG="data/daily.log"
mkdir -p data

# Gli avvii automatici non caricano sempre il PATH della shell: aggiungiamo i percorsi più comuni.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
[ -s "$HOME/.nvm/nvm.sh" ] && . "$HOME/.nvm/nvm.sh"

# Evita due esecuzioni in contemporanea. Un blocco più vecchio di 6 ore è rimasto da un'esecuzione interrotta.
LOCK="data/.daily.lock"
find data -maxdepth 1 -name .daily.lock -type d -mmin +360 -exec rmdir {} \; 2>/dev/null
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "$(date '+%F %T') esecuzione già in corso, esco" >> "$LOG"
  exit 0
fi
trap 'rmdir "$LOCK"' EXIT

echo "=== $(date '+%F %T') inizio ===" >> "$LOG"

# 1. Scansione: siti aziende + JobSpy (LinkedIn/Indeed). Non consuma il piano Codex.
#    I messaggi di JobSpy (es. blocchi 429) sono in data/jobspy.log.
if ! node scan.mjs >> "$LOG" 2>&1; then
  echo "$(date '+%F %T') ATTENZIONE: scansione terminata con errori (vedi sopra)" >> "$LOG"
fi

# 1b. (Solo se attivati gli avvisi email, vedi docs/PIANO.md "Sviluppi futuri")
# node plugins.mjs run gmail >> "$LOG" 2>&1 || echo "$(date '+%F %T') ATTENZIONE: plugin gmail con errori" >> "$LOG"

# 2. Valutazione con Codex, solo se ci sono offerte in attesa.
#    Le righe "unreadable" restano in attesa per sempre: non le contiamo, altrimenti Codex partirebbe ogni giorno a vuoto.
PENDING=$(grep '^- \[ \] ' data/pipeline.md 2>/dev/null | grep -vc 'unreadable' || true)
PENDING=${PENDING:-0}
echo "$(date '+%F %T') offerte in attesa: $PENDING" >> "$LOG"

if [ "$PENDING" -gt 0 ]; then
  # Limite di 3 ore, se il comando timeout è disponibile (Ubuntu: timeout, Mac con coreutils: gtimeout).
  TIMEOUT=""
  if command -v timeout >/dev/null; then TIMEOUT="timeout 3h"
  elif command -v gtimeout >/dev/null; then TIMEOUT="gtimeout 3h"
  fi

  # project_doc_max_bytes: career-ops/AGENTS.md è più lungo del limite predefinito (32 KB).
  # < /dev/null: senza, codex exec può restare in attesa di input.
  $TIMEOUT codex exec \
    --sandbox workspace-write \
    -c sandbox_workspace_write.network_access=true \
    -c project_doc_max_bytes=131072 \
    "$(cat local/prompt-giornaliero.md)" < /dev/null >> "$LOG" 2>&1 \
    || echo "$(date '+%F %T') ATTENZIONE: codex exec terminato con errori" >> "$LOG"
fi

echo "=== $(date '+%F %T') fine ===" >> "$LOG"
