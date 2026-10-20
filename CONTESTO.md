# CONTESTO — Job Scraper per Enrico

Questo documento spiega **tutto il progetto**: cosa vogliamo ottenere, quali strumenti usiamo, perché li abbiamo scelti, come sono collegati e quali sono i rischi. È scritto sia per Enrico sia per Codex, che lo usa come riferimento durante la costruzione.

Ultimo aggiornamento della ricerca: **20 ottobre 2026**.

---

## 1. Obiettivo

Enrico sta cercando lavoro. Vogliamo un sistema che, sul suo computer:

1. **trovi** ogni giorno offerte nuove su **LinkedIn** e **Indeed** (più i siti carriere delle aziende);
2. le **valuti** rispetto al suo profilo (voto 1–5 con motivazione);
3. per quelle buone prepari un **CV su misura** e una **cover letter** personalizzata;
4. tenga traccia delle candidature;
5. mostri tutto in una **dashboard locale** nel browser.

**Regola fondamentale:** il sistema prepara, Enrico decide. Nessuna candidatura viene inviata in automatico.

---

## 2. Gli strumenti scelti

### career-ops — il "cervello"
- Repository: https://github.com/career-ops-hq/career-ops (prima era `santifer/career-ops`, il vecchio link reindirizza qui).
- Open source (licenza MIT), molto diffuso (~75.000 stelle), aggiornato di continuo.
- Funziona con **Codex** (ha un `AGENTS.md` e un `CODEX.md` dedicati).
- Cosa fa: valuta le offerte, genera CV in PDF ottimizzati per i filtri automatici delle aziende (ATS), scrive cover letter, tiene il tracker delle candidature, prepara ai colloqui.
- Ha già una **dashboard web locale** (in versione alpha) e una dashboard da terminale.
- Da solo cerca sui siti carriere delle aziende e sui loro sistemi di selezione (Greenhouse, Lever, Ashby, Workday…), **ma non su LinkedIn e Indeed**.

### JobSpy — gli "occhi" su LinkedIn e Indeed
- Repository: https://github.com/speedyapply/JobSpy · pacchetto Python `python-jobspy`.
- Open source (MIT), attivo (versione 1.4.0 del 19/10/2026).
- Legge gli annunci di **LinkedIn** e **Indeed** usando le pagine pubbliche, **senza login**.
- Provato il 20/10/2026 su Milano: ha restituito offerte reali da entrambi i siti senza errori.

### Come si collegano
career-ops permette di aggiungere "parser locali": piccoli script che portano offerte da fonti esterne. Noi aggiungiamo uno script che usa JobSpy. Le offerte trovate passano per gli stessi filtri di career-ops (titolo, città, età dell'annuncio, duplicati) e finiscono nella sua lista di offerte da valutare.

**Non modifichiamo il codice di career-ops**: aggiungiamo solo file nostri nelle cartelle previste per le personalizzazioni. Così career-ops si può aggiornare senza perdere nulla.

---

## 3. Alternative valutate e scartate

| Progetto | Perché no |
|---|---|
| [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) | Ottimo, ma pensato per **Claude Code** (su Codex funziona solo in parte), **non ha Indeed**, i portali inclusi sono danesi e richiede LaTeX. |
| [suxrobGM/jobpilot](https://github.com/suxrobGM/jobpilot) | Invia candidature in automatico con login su LinkedIn (rischio ban dell'account) e salva dati su un sito esterno. |
| [Pickle-Pixel/ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot) | Invio automatico, fermo da marzo 2026. |
| AIHawk, job-forge | Progetti non più disponibili. |

---

## 4. Come funziona, giorno per giorno

```
Ogni mattina (automatico, es. ore 9:00)
│
├─ 1. SCANSIONE  (nessun costo di AI)
│     career-ops scan.mjs
│       ├─ siti carriere delle aziende in portals.yml
│       └─ parser JobSpy → LinkedIn + Indeed
│              salva il testo di ogni annuncio in jds/jobspy/
│     → filtri (titolo, città, età, duplicati)
│     → nuove offerte in data/pipeline.md
│
├─ 2. VALUTAZIONE  (Codex, consuma il piano Codex)
│     codex exec → modalità "pipeline" di career-ops
│       → voto 1–5 + report in reports/
│       → (se scelto) CV + cover letter in output/ per le offerte con voto alto
│
└─ 3. ENRICO  (manuale)
      apre la dashboard → legge, sceglie, controlla i PDF → si candida lui
```

### Cartelle principali di career-ops

| Percorso | Contenuto |
|---|---|
| `cv.md` | Il CV di Enrico in formato testo (la base per tutti i CV su misura). |
| `config/profile.yml` | Profilo e preferenze. |
| `portals.yml` | Dove cercare: aziende, filtri su titolo e città, parser JobSpy. |
| `data/pipeline.md` | Offerte trovate, in attesa di valutazione. |
| `data/applications.md` | Tracker delle candidature. |
| `reports/` | Report di valutazione di ogni offerta. |
| `output/` | PDF di CV e cover letter generati. |
| `local/` | I nostri script personalizzati (JobSpy, automazione). |

---

## 5. Dettagli tecnici importanti (scoperti durante la ricerca)

1. **LinkedIn e le città.** Con JobSpy, se scrivi solo `"Milano"` LinkedIn restituisce offerte di **Milano, Texas**, senza nessun errore. Bisogna sempre scrivere `"Milano, Italy"` (o `"Milan, Lombardy, Italy"`). Per Indeed invece si usa `country_indeed="italy"` + `location="Milano"`.
2. **Limiti di LinkedIn.** Se si scaricano troppi annunci di fila LinkedIn blocca temporaneamente (errore 429, dura circa un minuto). Per questo: poche ricerche al giorno, pause tra una e l'altra, e lo script si ferma da solo se riceve un blocco.
3. **Il testo degli annunci va salvato subito.** career-ops ha una regola: per un link LinkedIn fa un solo tentativo di aprire la pagina, e Indeed spesso blocca l'apertura diretta. Quindi lo script JobSpy salva subito il testo di ogni annuncio in `jds/jobspy/` e passa a career-ops un riferimento `local:` a quel file.
4. **Annunci "da confermare".** career-ops considera le offerte di LinkedIn/Indeed come **non confermate** finché non trova la stessa posizione sul sito dell'azienda. Lo script salva anche il link diretto all'azienda (quando c'è) per facilitare il controllo.
5. **Timeout.** career-ops dà 20 secondi di default ai parser locali: troppo pochi per JobSpy. Va alzato (es. 20 minuti).
6. **Python dell'ambiente virtuale.** Se nel parser si indica direttamente il Python dell'ambiente virtuale, career-ops lo **ignora in silenzio** (perché il file reale è fuori dalla cartella). Si usa un piccolo script `sh` che lancia quel Python.
7. **Windows.** career-ops funzionerebbe anche su Windows nativo, ma i nostri script (`run-jobspy.sh`, `daily.sh`, il Python in `.venv-jobspy/bin/`) sono per Linux/Mac. Per questo su Windows **tutto** va dentro **WSL2 (Ubuntu)**, senza passare a Windows nativo a metà lavoro.
8. **Codex in automatico.** Il comando `codex exec` di default non può scrivere file né usare Internet: vanno abilitati esplicitamente. In modalità automatica non può chiedere approvazioni, quindi gli strumenti del browser (Playwright) vanno pre-approvati in `~/.codex/config.toml`, solo per la lettura delle pagine. Le opzioni cambiano tra le versioni di Codex: vanno sempre verificate con `codex exec --help`.
9. **Regole di career-ops troppo lunghe.** `career-ops/AGENTS.md` supera il limite che Codex legge di default (32 KB): senza alzare `project_doc_max_bytes`, Codex ignorerebbe proprio le regole più importanti (mai inviare candidature, annunci da confermare).
10. **Nomi delle città.** LinkedIn scrive le città in inglese ("Milan"), Indeed in italiano ("Milano"). Il filtro città di career-ops confronta parole intere, quindi ogni città va inserita in entrambe le lingue.
11. **Filtri predefiniti.** Il modello di configurazione di career-ops scarta già titoli con parole come "Junior", "Intern", "Java", "SAP". Vanno rivisti in base al profilo di Enrico.
12. **Mai `--verify`.** L'opzione `node scan.mjs --verify` considera "non validi" i riferimenti `local:` e scarterebbe per sempre tutte le offerte JobSpy.

---

## 6. Rischi e regole di sicurezza

### Termini d'uso
**LinkedIn e Indeed vietano nei loro termini d'uso la raccolta automatica degli annunci**, anche senza login (LinkedIn User Agreement §8.2; Indeed ToS §21). JobSpy quindi va contro queste regole, e anche career-ops lo sconsiglia nel suo `LEGAL_DISCLAIMER.md`. Per un uso **personale, a basso volume e senza login** il rischio pratico è basso (al massimo un blocco temporaneo), ma Enrico deve saperlo e accettarlo esplicitamente durante l'intervista. Se non lo accetta, il sistema funziona comunque con i siti carriere delle aziende e con i link incollati a mano. Questo non è un parere legale.

**Alternativa più "pulita"** (sviluppo futuro): attivare gli avvisi email di LinkedIn e Indeed e far leggere quelle email a career-ops (plugin Gmail). È più complicata da configurare (serve un progetto Google Cloud con OAuth) e porta meno offerte, quindi si valuta solo a sistema funzionante.

### Regole che il sistema rispetta sempre
- **Mai fare login** su LinkedIn o Indeed in modo automatico, mai usare cookie o account finti.
- **Mai inviare candidature** in automatico.
- **Volumi bassi**: una scansione al giorno, poche ricerche, pause, stop automatico se arriva un blocco.
- **Connessione di casa**, niente VPN o server esterni.
- **Mai pubblicare dati personali** su GitHub.
- CV e cover letter **non inventano nulla**: solo esperienze e competenze reali di Enrico.

---

## 7. Limiti noti

- **InfoJobs** non è supportato da JobSpy. Si può aggiungere solo con un parser dedicato (da valutare).
- La **dashboard web** di career-ops è in versione alpha: se non funziona bene, si usa la dashboard da terminale di career-ops (vedi `docs/PIANO.md`, Fase 6).
- Gli strumenti si aggiornano spesso: **se qualcosa in questo documento non corrisponde più alla documentazione ufficiale di career-ops o JobSpy, vale la documentazione ufficiale.**
- Ogni offerta valutata da Codex consuma il piano Codex di Enrico: il numero di offerte al giorno va calibrato.

---

## 8. Fonti

- career-ops: https://github.com/career-ops-hq/career-ops — in particolare `AGENTS.md`, `LEGAL_DISCLAIMER.md`, `docs/CODEX.md`, `docs/AUTOMATION.md`, `docs/local-parser-cookbook.md`, `modes/scan.md`, `modes/pipeline.md`, `web/README.md`
- JobSpy: https://github.com/speedyapply/JobSpy · https://pypi.org/project/python-jobspy/
- Codex non interattivo: https://developers.openai.com/codex/noninteractive
- LinkedIn User Agreement: https://www.linkedin.com/legal/user-agreement
- Indeed Terms of Service: https://www.indeed.com/legal
