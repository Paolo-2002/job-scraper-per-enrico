# Piano di costruzione

Istruzioni per Codex. Esegui le fasi **in ordine**, una alla volta. Ogni fase ha:
- **Leggi prima**: documentazione ufficiale da consultare (la versione attuale vale più di questo file, salvo l'eccezione JobSpy descritta in `AGENTS.md`);
- **Passi**: cosa fare;
- **Verifica**: come controllare che funzioni. Mostra il risultato a Enrico;
- **Fine fase**: aggiorna `profilo/STATO.md` e chiedi conferma prima di proseguire.

**Dove si lavora.** Resta sempre in **questa sessione**, aperta nella cartella progetto: non chiedere a Enrico di riavviare Codex in un'altra cartella. career-ops viene installato in `./career-ops/` (esclusa da Git); dalla Fase 1 in poi esegui i comandi con cartella di lavoro `career-ops/`, salvo dove indicato. Quando lavori su career-ops segui le regole di `career-ops/AGENTS.md`: è lungo, leggilo **per intero** (`cat`), non solo l'inizio.

I numeri delle domande (D1, D2…) si riferiscono a [INTERVISTA.md](INTERVISTA.md).

---

## Fase 0 — Prerequisiti

**Leggi prima:** README di https://github.com/career-ops-hq/career-ops (requisiti) e [CONTESTO.md](../CONTESTO.md) §5.

**Passi**
1. **Solo Windows — passaggio a Ubuntu (WSL2).** Tutto il sistema deve stare dentro Ubuntu, perché i nostri script sono per Linux/Mac. Se Codex non sta già girando dentro Ubuntu:
   1. fai aprire a Enrico **PowerShell come amministratore** e scrivere `wsl --install`, poi riavviare il PC e creare utente e password di Ubuntu;
   2. dal menu Start apri **Ubuntu**: da qui in poi tutti i comandi si scrivono lì;
   3. in Ubuntu installa Node.js e Codex CLI (vedi passo 3), poi esegui `codex` e accedi;
   4. clona di nuovo la repository: `cd ~ && git clone https://github.com/Paolo-2002/job-scraper-per-enrico.git`;
   5. **copia le risposte già date**, se esistono: `cp -r /mnt/c/Users/<utente>/<percorso>/job-scraper-per-enrico/profilo ~/job-scraper-per-enrico/`;
   6. chiedi a Enrico di chiudere Codex su Windows e riaprirlo in Ubuntu: `cd ~/job-scraper-per-enrico && codex`. La nuova sessione riprenderà da `profilo/`.
2. **Solo Mac:** verifica che la cartella progetto non sia in Scrivania, Documenti, Download o iCloud (D2). Se lo è, proponi di spostarla in `~` prima di andare avanti.
3. Controlla le versioni installate e installa ciò che manca (spiega e chiedi conferma prima):
   - **Git**.
   - **Node.js ≥ 22.13** (controlla `engines` in `career-ops/package.json` dopo la Fase 1). Su Mac Homebrew o nvm; su Ubuntu nvm.
   - **Python ≥ 3.10**. Su Ubuntu installa anche `sudo apt install -y python3-venv python3-pip`. Su Mac, se `python3 --version` è 3.9 o meno, installa Python con Homebrew (`brew install python`).
   - **pdftotext** (serve per leggere il CV in PDF): `brew install poppler` su Mac, `sudo apt install -y poppler-utils` su Ubuntu.
   - **Codex CLI** disponibile come comando `codex` e autenticato.
4. Opzionale: **Go**, nella versione indicata in `career-ops/dashboard/go.mod` (al momento 1.26), solo se servirà la dashboard da terminale (Fase 6).

**Verifica:** `git --version`, `node --version`, `python3 --version`, `pdftotext -v`, `codex --version` mostrano versioni adeguate.

---

## Fase 1 — Installare career-ops

**Leggi prima:** README e `docs/CODEX.md` di career-ops.

**Passi**
1. Dalla cartella progetto: `git clone https://github.com/career-ops-hq/career-ops.git career-ops`, poi `cd career-ops && npm install` (installa anche Chromium per i PDF). Su Ubuntu, se Chromium non parte, `npx playwright install-deps chromium`.
2. Leggi **per intero** `career-ops/AGENTS.md` e `career-ops/LEGAL_DISCLAIMER.md`.
3. **Configura Codex** in `~/.codex/config.toml`. Mostra a Enrico le modifiche e chiedi conferma prima di salvarle; conserva il resto del file.
   ```toml
   # career-ops/AGENTS.md è più lungo del limite predefinito di Codex (32 KB): senza questa riga Codex ne leggerebbe solo l'inizio.
   project_doc_max_bytes = 131072

   [mcp_servers.playwright]
   command = "npx"
   args = ["-y", "@playwright/mcp@latest"]

   # Approvazione automatica solo per leggere pagine (servono alle esecuzioni automatiche).
   # Clic e digitazione restano soggetti ad approvazione: così nessun modulo viene inviato da solo.
   [mcp_servers.playwright.tools.browser_navigate]
   approval_mode = "approve"
   [mcp_servers.playwright.tools.browser_snapshot]
   approval_mode = "approve"
   [mcp_servers.playwright.tools.browser_wait_for]
   approval_mode = "approve"
   [mcp_servers.playwright.tools.browser_close]
   approval_mode = "approve"
   ```
   `project_doc_max_bytes` va **in cima al file**, prima di qualsiasi sezione `[...]`. Se la sintassi è cambiata, verifica con la documentazione di Codex (https://developers.openai.com/codex/config-reference). Le modifiche valgono dalla prossima sessione Codex.
4. Registra che usi Codex: `node remember-cli.mjs codex`.

**Verifica:** `npm run doctor` senza errori bloccanti (il controllo MCP per Codex viene saltato da doctor: è normale). `codex mcp list` mostra `playwright`.

---

## Fase 2 — Profilo di Enrico

**Leggi prima:** in `career-ops/AGENTS.md` la sezione **"First Run — Onboarding"** (Step 0–6) e `node onboard-write.mjs --help`. Questa fase segue quella procedura usando le risposte già raccolte: **non rifare a Enrico domande a cui ha già risposto.**

**Passi** (dentro `career-ops/`)
1. `node doctor.mjs --json --init-templates`: crea i file di personalizzazione mancanti (`modes/_profile.md`, `modes/_brief.md`, `modes/_custom.md`, `voice-dna.md`).
2. **Profilo e portali** in un solo comando, **prima** del CV (onboard-write non sovrascrive un `config/profile.yml` già esistente): `node onboard-write.mjs --answers -` con le risposte (D4, D6, D7, D8, D9, D10, D14, D20, D23, D24), valuta EUR, paese Italy; D10 va nei campi di permesso di lavoro indicati da `node onboard-write.mjs --help`. **Non copiare né modificare a mano i template.** Per `portals`:
   - `positive`: i titoli di ruolo di D14 in italiano e inglese, con le varianti comuni;
   - `negative`: le parole di D18;
   - `cities`: ogni città di D23 **sia in italiano sia in inglese** (Milano + Milan, Roma + Rome, Torino + Turin, Napoli + Naples, Firenze + Florence, Genova + Genoa, Venezia + Venice, Padova + Padua…), perché LinkedIn scrive le città in inglese;
   - `countries`: vuoto, **a meno che** Enrico accetti qualsiasi città italiana da remoto (D24): in quel caso `["Italy", "Italia"]`;
   - non mettere mai "Remote", "Remoto", "Ibrido" o "Da remoto" come località: il writer rifiuta solo le parole inglesi, ma anche quelle italiane farebbero passare offerte da qualsiasi paese;
   - `max_posting_age_days`: 14.

   Se l'output elenca `config/profile.yml` sotto `kept`, il file esisteva già: rilancia con `--force --only profile`.
3. **CV → `cv.md`.** Se c'è un PDF in `profilo/`, copialo in `documents/cv/` e usa la modalità `intake` di career-ops (`modes/intake.md`) per creare `cv.md`; altrimenti parti dal testo incollato o dalle risposte (D11b). Rispetta la struttura richiesta da AGENTS.md (Step 1). Togli ciò che Enrico non vuole (D13). Non inventare nulla. Fai rileggere il risultato a Enrico.
4. **Rivedi i filtri predefiniti.** Il template di career-ops scarta già alcune parole nel titolo (es. "Junior", "Intern", "Java", "SAP", "PHP"…). Mostra a Enrico l'elenco completo `title_filter.negative` in `portals.yml` e togli ogni voce in conflitto con il suo livello (D15) o i suoi ruoli. Questa è l'unica modifica a mano consentita su quei campi, insieme a quelle del passo 5 e della Fase 3.
5. **Aziende:** in `portals.yml` → `tracked_companies` disattiva (`enabled: false`) le aziende di esempio non pertinenti per Enrico e aggiungi le aziende dei sogni (D17) con il loro `careers_url`. Le aziende da escludere (D17) vanno nella blacklist di career-ops: `cp templates/blacklist.example.md data/blacklist.md`, poi una riga per azienda (`| Azienda | AAAA-MM-GG | company | motivo |`).
6. **Personalizzazione** (AGENTS.md Step 5):
   - `modes/_profile.md`: archetipi, obiettivo, livello, settori, motivazioni ed esclusioni (D15, D16, D19, D21, D22, D26);
   - `modes/_brief.md`: breve sintesi per lo smistamento rapido (livello, ruoli, RAL minima D20, città e remoto D23/D24, esclusioni D16/D22), senza segnaposto `{...}` rimasti;
   - `article-digest.md`: risultati e progetti extra (D12);
   - `voice-dna.md` e `writing-samples/`: tono e testi d'esempio (D27, D28);
   - `modes/_custom.md`: cose che il sistema non deve mai fare (D36).
7. **Lingua:** in `config/profile.yml` imposta `language.output` secondo D27 (`it` o `en`): career-ops scrive report, CV e lettere in quella lingua, qualunque sia la lingua dell'annuncio. Per un singolo annuncio in un'altra lingua, Enrico può chiedere a Codex i documenti in quella lingua. **Non** impostare `language.modes_dir: modes/it`: la pipeline in italiano ignora `auto_pdf_score_threshold` (Fase 5).

**Verifica:** `node doctor.mjs --json` mostra `onboardingNeeded: false`, `missing: []` e `unpersonalized: []`. Mostra a Enrico, in parole semplici, cosa cercherà il sistema (ruoli, città, filtri, aziende).

---

## Fase 3 — Collegare LinkedIn e Indeed (JobSpy)

**Salta questa fase** se a D33 Enrico ha scelto **(b) niente JobSpy**: annotalo in `STATO.md` e vai alla Fase 4. Prima di iniziare, ricorda a Enrico in due righe cosa ha accettato a D33.

**Leggi prima:** `career-ops/docs/local-parser-cookbook.md`, `career-ops/providers/local-parser.mjs`, `modes/scan.md` (livello 0), README di https://github.com/speedyapply/JobSpy.

**Passi** (dentro `career-ops/`)
1. Ambiente Python dedicato:
   ```bash
   python3 -m venv .venv-jobspy
   .venv-jobspy/bin/pip install "python-jobspy==1.4.0"
   ```
   Non aggiornare JobSpy senza aver letto il changelog: i parametri usati in `jobspy_parser.py` devono restare validi.
2. Copia i template:
   ```bash
   mkdir -p local
   cp ../templates/jobspy_parser.py local/
   cp ../templates/run-jobspy.sh local/ && chmod +x local/run-jobspy.sh
   cp ../templates/jobspy-searches.example.json local/jobspy-searches.json
   ```
3. Compila `local/jobspy-searches.json`:
   - in `searches` una voce per ogni combinazione ruolo + città (D14, D23), **al massimo il numero di D32**, e imposta `max_searches_per_run` uguale a D32: le voci oltre il limite verrebbero ignorate senza avviso;
   - `location_linkedin` sempre nel formato **"Città, Italy"** (es. `"Milano, Italy"`): con il solo nome LinkedIn può restituire città omonime all'estero (es. Milano, Texas);
   - `location_indeed` solo il nome della città (es. `"Milano"`), con `country_indeed: "italy"`;
   - se Enrico accetta il remoto da tutta Italia (D24): una ricerca con `location_linkedin: "Italy"` e `location_indeed: "Italia"`;
   - lascia `max_run_seconds` (600) ben sotto il `timeout_ms` di `portals.yml` (1.200.000 ms = 20 minuti).
4. `.venv-jobspy/` non è escluso dal `.gitignore` di career-ops: aggiungilo a `.git/info/exclude` (non modificare il `.gitignore` di career-ops). `local/` e `jds/` sono già esclusi.
5. **Test isolato** dello script, con una sola ricerca e 5 risultati per sito:
   ```bash
   JOBSPY_TEST=1 sh local/run-jobspy.sh > /tmp/jobspy-test.json
   ```
   Lo script fa richieste a Internet: se la sandbox di Codex blocca la rete, chiedi a Enrico l'approvazione per eseguirlo con accesso alla rete.
6. Aggiungi a `portals.yml`, dentro `tracked_companies`, il blocco di [templates/portals-jobspy.yml](../templates/portals-jobspy.yml). Controlla con `node validate-portals.mjs`.
7. Esegui la scansione **una volta**: `node scan.mjs`.
   - **Non** usare `--dry-run`: rifarebbe comunque tutte le ricerche, raddoppiando il volume su LinkedIn/Indeed.
   - **Non** usare mai `--verify`: scarterebbe per sempre tutte le offerte JobSpy (i riferimenti `local:` risultano "non validi").

**Verifica**
- Il test isolato produce un JSON valido con `jobs` non vuoto e i file in `jds/jobspy/` contengono il testo degli annunci.
- Le località sono davvero in Italia (nessuna "Milano, TX").
- L'output di `node scan.mjs` mostra **"1 local parser"** (se mostra 0, il percorso dello script o l'interprete sono sbagliati).
- `data/pipeline.md` contiene righe `local:jds/jobspy/...` e `data/scan-history.tsv` le registra. Se molte offerte LinkedIn risultano `skipped_location` o `skipped_title`, rivedi città e filtri della Fase 2.
- `data/jobspy.log` non contiene blocchi. Se compare un **429** o un blocco di LinkedIn: aspetta, riduci `results_per_search`, non insistere.

---

## Fase 4 — Primo giro manuale

**Leggi prima:** `modes/pipeline.md` e le modalità di valutazione e generazione PDF descritte in `career-ops/AGENTS.md`.

**Passi** (in questa stessa sessione, lavorando su `career-ops/`)
1. Valuta 2–3 offerte da `data/pipeline.md` con la modalità pipeline di career-ops.
2. Per l'offerta con il voto più alto genera **CV su misura** e **cover letter**.
3. Apri con Enrico il report (`reports/`) e i PDF (`output/`). Chiedi cosa cambierebbe: tono, lunghezza, cosa evidenziare, errori.
4. Applica le correzioni ai file di base (`cv.md`, `modes/_profile.md`, `voice-dna.md`, `article-digest.md`), non solo al singolo PDF, così valgono per tutte le offerte future. Per le correzioni di stile usa la modalità `retro` di career-ops.

**Verifica:** Enrico è soddisfatto della qualità di almeno un CV e una cover letter. Non andare avanti finché non lo è.

---

## Fase 5 — Automazione giornaliera

**Leggi prima:** `career-ops/docs/AUTOMATION.md`, `codex exec --help` (le opzioni cambiano tra versioni), https://developers.openai.com/codex/noninteractive.

**Passi** (dentro `career-ops/`)
1. Prompt giornaliero, in base a D29:
   - **(a) solo valutazione:** `cp ../templates/prompt-giornaliero-valutazione.md local/prompt-giornaliero.md` e in `config/profile.yml` imposta `auto_pdf_score_threshold: 6` (il voto massimo è 5, quindi nessun PDF automatico);
   - **(b) valutazione + documenti:** `cp ../templates/prompt-giornaliero-documenti.md local/prompt-giornaliero.md` e imposta `auto_pdf_score_threshold` uguale alla soglia di D30.

   Sostituisci i segnaposto `{{MAX_OFFERTE}}` (D31) e `{{SOGLIA}}` (D30).
2. `cp ../templates/daily.sh local/ && chmod +x local/daily.sh`. Controlla con `codex exec --help` che le opzioni usate nello script esistano ancora e correggile se necessario.
3. **Prova manuale:** va eseguita **fuori dalla sandbox di Codex** (serve la rete e l'accesso a `~/.codex`). Chiedi a Enrico di aprire una seconda finestra del terminale e lanciare `cd <percorso>/career-ops && bash local/daily.sh` (sempre `bash`, non `sh`). Poi leggi insieme a lui `data/daily.log` e `data/jobspy.log`.
4. Programma l'esecuzione all'orario di D3:
   - **Mac:** usa [templates/io.career-ops.daily.plist](../templates/io.career-ops.daily.plist): sostituisci `PERCORSO_CAREER_OPS` e l'orario, copialo in `~/Library/LaunchAgents/`, caricalo con `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/io.career-ops.daily.plist`. Se il Mac è in stop all'orario previsto, launchd esegue il job al risveglio; se è **spento**, quel giorno il job salta.
   - **Windows:** segui [templates/windows-pianificazione.md](../templates/windows-pianificazione.md) (Utilità di pianificazione che avvia lo script dentro Ubuntu).
5. Spiega a Enrico come **mettere in pausa** e **disattivare** l'automazione (i comandi sono nei template; vanno anche nella guida finale).

**Verifica:** dopo la prova manuale `data/daily.log` mostra scansione + valutazione senza errori; il job risulta registrato (`launchctl list | grep career-ops` su Mac, Utilità di pianificazione su Windows).

---

## Fase 6 — Dashboard

**Leggi prima:** `career-ops/web/README.md`.

**Passi**
1. Prepara la web UI una volta: `cd career-ops/web && npm ci && npm run build`.
2. Avviala con `npm start` (dentro `career-ops/web`) e apri http://127.0.0.1:3000. Usa `npm start`, non `npm run ui`: quest'ultimo avvia la versione di sviluppo, più lenta.
3. Controlla con Enrico che mostri ciò che ha chiesto a D35: offerte nuove, candidature e stato, report, statistiche.
4. Crea un comando rapido `dashboard-lavoro` nel file della shell (`~/.zshrc` su Mac, `~/.bashrc` su Ubuntu), chiedendo conferma prima di modificarlo:
   ```bash
   alias dashboard-lavoro='cd <percorso>/career-ops/web && npm start'
   ```
   (Su Mac può anche aprire il browser: `(sleep 3 && open http://127.0.0.1:3000) & npm start`.)
5. **Se la web UI non funziona** dopo un tentativo ragionevole di correzione (è in versione alpha): usa la dashboard da terminale, `npm run serve:dashboard` dentro `career-ops/` (richiede Go), e annota il problema in `STATO.md`. Non scrivere una dashboard nuova.

**Verifica:** Enrico apre la dashboard da solo con il comando rapido e ritrova le offerte del primo giro.

---

## Fase 7 — Consegna

**Passi**
1. Scrivi `profilo/GUIDA-USO.md`, breve e in italiano semplice:
   - **routine quotidiana:** `dashboard-lavoro`, leggere le offerte e i voti, controllare i PDF, candidarsi a mano, aggiornare lo stato;
   - **CV e lettera per un'offerta specifica:** `cd <percorso>/career-ops && codex`, poi incollare il link o il testo dell'annuncio e chiedere CV e cover letter;
   - come cambiare ricerche, città, filtri e numero di offerte (chiedendolo a Codex nella cartella progetto);
   - come mettere in pausa e disattivare l'automazione;
   - **aggiornare:** `cd career-ops && npm run update:check && npm run update && (cd web && npm run build)`; JobSpy solo dopo aver letto il changelog;
   - cosa fare se `data/jobspy.log` mostra un 429 o se una fonte smette di funzionare.
2. Aggiorna `profilo/STATO.md`: "Sistema completato" con la data.
3. Fai un riepilogo finale a Enrico di cosa è stato costruito e ricordagli dove trova la guida.

## Sviluppi futuri (solo se Enrico li chiede, a sistema funzionante)
- **Avvisi email** di LinkedIn/Indeed letti dal plugin Gmail di career-ops (`plugins/gmail/`): richiede un progetto Google Cloud con OAuth. Se attivato, aggiungi `node plugins.mjs run gmail` in `local/daily.sh` (riga già presente, commentata).
- **InfoJobs** o ricerche all'estero (D25, D34).
