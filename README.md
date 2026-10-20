# Job Scraper per Enrico

Sistema personale di ricerca lavoro che gira **sul tuo computer**:

- cerca ogni giorno nuove offerte su **LinkedIn** e **Indeed** (e sui siti carriere delle aziende);
- le valuta rispetto al tuo profilo con un voto da 1 a 5;
- per le offerte migliori prepara **CV su misura** e **cover letter** in PDF;
- ti mostra tutto in una **dashboard locale** nel browser.

Non invia mai candidature da solo: l'ultimo clic su "Invia" è sempre tuo.

## Come si parte (circa 1–2 ore, anche in più volte)

### Solo se usi Windows: prima prepara Ubuntu
1. Apri **PowerShell come amministratore** e scrivi `wsl --install`. Riavvia il PC e crea utente e password di Ubuntu quando te lo chiede.
2. Dal menu Start apri **Ubuntu**: da qui in poi **tutti** i comandi vanno scritti lì, compresa l'installazione di Codex.
3. In Ubuntu installa Node.js (serve per installare Codex): `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash`, chiudi e riapri Ubuntu, poi `nvm install --lts`.

### Per tutti
1. **Installa Codex** (se non ce l'hai): su Mac `brew install --cask codex` oppure, ovunque, `npm install -g @openai/codex`. Poi scrivi `codex`, scegli **Sign in with ChatGPT** e accedi (serve un piano ChatGPT che includa Codex, es. Plus). Chiudi Codex con `/quit`.
2. **Scarica questa repository** nella tua cartella utente (su Mac **non** in Scrivania, Documenti o Download):
   ```bash
   cd ~
   git clone https://github.com/Paolo-2002/job-scraper-per-enrico.git
   cd job-scraper-per-enrico
   ```
3. **Avvia Codex** dentro la cartella:
   ```bash
   codex
   ```
   Al primo avvio Codex chiede se ti fidi della cartella (*"Trust this folder?"*): scegli **Trust and continue**. Se scegli altro, Codex non legge le istruzioni.
4. Scrivi:
   > **Ciao, iniziamo.**

Codex leggerà le istruzioni in [AGENTS.md](AGENTS.md), ti farà un'intervista per conoscerti (lavoro cercato, città, CV, preferenze…) e poi costruirà tutto passo passo, chiedendoti conferma alla fine di ogni fase. Durante il lavoro ti chiederà spesso il permesso di eseguire comandi: leggi la spiegazione e approva.

Se Codex risponde senza proporti l'intervista, chiudilo (`/quit`), rilancia `codex` nella cartella e scegli **Trust and continue**.

Puoi interrompere quando vuoi: alla prossima apertura (`cd ~/job-scraper-per-enrico && codex`) Codex riprende da dove eravate rimasti.

## Dopo la configurazione
- **Ogni giorno:** scrivi `dashboard-lavoro` nel terminale e apri il browser su http://127.0.0.1:3000.
- **CV e lettera per un'offerta:** `cd ~/job-scraper-per-enrico/career-ops && codex`, poi incolla il link o il testo dell'annuncio.
- **Cambiare qualcosa** (ricerche, città, orari): `cd ~/job-scraper-per-enrico && codex` e chiedilo.
- Istruzioni complete: `profilo/GUIDA-USO.md` (la crea Codex alla fine).

## Cosa c'è qui dentro

| File | A cosa serve |
|---|---|
| [CONTESTO.md](CONTESTO.md) | Spiegazione completa del progetto: cosa fa, scelte fatte, rischi e limiti. Leggilo se vuoi capire come funziona. |
| [AGENTS.md](AGENTS.md) | Le regole che Codex segue in questa cartella. |
| [docs/INTERVISTA.md](docs/INTERVISTA.md) | Le domande che Codex ti farà all'inizio. |
| [docs/PIANO.md](docs/PIANO.md) | Il piano di costruzione, fase per fase. |
| [templates/](templates/) | File pronti che Codex copia e adatta (collegamento a LinkedIn/Indeed, automazione giornaliera…). |

## Privacy

I tuoi dati (CV, risposte, offerte, documenti generati) restano **solo sul tuo computer**: le cartelle `profilo/` e `career-ops/` sono escluse da Git e non finiscono mai su GitHub.
