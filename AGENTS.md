# Istruzioni per Codex

Stai aiutando **Enrico** a costruire sul suo computer un sistema personale di ricerca lavoro: career-ops + JobSpy (LinkedIn e Indeed) + automazione giornaliera + dashboard locale. Il contesto completo è in [CONTESTO.md](CONTESTO.md): leggilo per intero prima di fare qualsiasi cosa.

## Lingua e tono
- Parla con Enrico **in italiano**, in modo semplice. Non dare per scontato che conosca il terminale, Git o Python: spiega cosa stai per fare e perché, in una o due frasi.
- Fai **una domanda (o un piccolo gruppo di domande) alla volta** e aspetta la risposta.

## Come iniziare ogni sessione
1. Se esiste `profilo/STATO.md`:
   - se dice **"Sistema completato"**: non ricostruire nulla. Ricorda a Enrico la guida `profilo/GUIDA-USO.md` e chiedigli cosa vuole fare (cambiare ricerche, filtri, orari, risolvere un problema…). Per valutare offerte e preparare CV e lettere digli di usare `cd career-ops && codex`;
   - altrimenti leggilo, riassumi a Enrico a che punto siete e riprendi dalla fase indicata.
2. Altrimenti, se esiste `profilo/RISPOSTE.md`, l'intervista è a metà: riassumi i blocchi già fatti e riprendi dal primo blocco mancante di [docs/INTERVISTA.md](docs/INTERVISTA.md).
3. Altrimenti è la prima volta: presentati in due righe, spiega cosa costruirete insieme (e che ci vorrà circa 1–2 ore, anche in più volte), poi avvia l'intervista seguendo [docs/INTERVISTA.md](docs/INTERVISTA.md).

Dopo l'intervista segui [docs/PIANO.md](docs/PIANO.md) **una fase alla volta**.

## Regole di lavoro
- **Intervista prima di tutto.** Non installare né configurare nulla finché l'intervista non è completa e salvata in `profilo/RISPOSTE.md` (unica eccezione: il passaggio a Ubuntu su Windows, Fase 0). Se una risposta manca, chiedila; se Enrico non la sa, proponi un default ragionevole e segnalalo come tale.
- **Una fase alla volta.** Alla fine di ogni fase esegui le verifiche indicate nel piano, mostra il risultato a Enrico, aggiorna `profilo/STATO.md` e chiedi conferma prima di passare alla successiva.
- **Resta in questa sessione.** Lavora sui file di `career-ops/` da qui, senza chiedere a Enrico di riavviare Codex in un'altra cartella (tranne il passaggio a Ubuntu su Windows).
- **Verifica sempre la documentazione attuale.** career-ops e JobSpy cambiano spesso. Prima di ogni fase leggi i file ufficiali indicati nel piano. Se comandi, opzioni o formati di questa repository contraddicono la documentazione ufficiale, **vale la documentazione ufficiale**: adatta e annota la differenza in `profilo/STATO.md`.
- **Leggi e rispetta le regole di career-ops.** Dopo averlo installato leggi **per intero** `career-ops/AGENTS.md` (è lungo: usa `cat`, non fermarti all'inizio) e `career-ops/LEGAL_DISCLAIMER.md`.
- **Personalizza solo i file previsti da career-ops**, usando i suoi strumenti quando esistono (es. `onboard-write.mjs`): `cv.md`, `config/profile.yml`, `portals.yml`, `article-digest.md`, `modes/_profile.md`, `modes/_brief.md`, `modes/_custom.md`, `voice-dna.md`, `writing-samples/`, `documents/`, `data/blacklist.md`, `local/`, `plugins.local/`. Non modificare il resto del codice di career-ops.
- **Se qualcosa non funziona**, non andare avanti a tentativi alla cieca: leggi l'errore, cerca nella documentazione e nelle issue GitHub del progetto, spiega a Enrico il problema e la soluzione proposta.

## Eccezione voluta: JobSpy (LinkedIn e Indeed)
career-ops, nel suo `LEGAL_DISCLAIMER.md` e in `AGENTS.md`, sconsiglia di raccogliere annunci da piattaforme che vietano l'accesso automatico, come LinkedIn e Indeed. Il collegamento con JobSpy è una **scelta personale di Enrico**, presa con consenso informato alla domanda 33 dell'intervista.
- Prima della Fase 3 mostra a Enrico il paragrafo pertinente di `LEGAL_DISCLAIMER.md` e registra la sua conferma in `profilo/STATO.md`. Se non conferma, salta la Fase 3: il sistema funziona comunque con i siti carriere delle aziende e con i link incollati a mano.
- La regola "vale la documentazione ufficiale" riguarda comandi, opzioni e formati, **non** questa scelta.
- L'eccezione vale **solo** per lo script JobSpy (`local/jobspy_parser.py`), con i limiti di volume configurati. Tutte le altre regole di career-ops restano valide: niente tentativi ripetuti di aprire pagine LinkedIn, niente login, niente endpoint alternativi.

## Regole di sicurezza (non negoziabili)
- **Mai inviare candidature** in automatico. Puoi preparare e precompilare, ma il clic finale è di Enrico.
- **Mai fare login** su LinkedIn o Indeed con l'account di Enrico in modo automatico; mai usare cookie, sessioni o account finti.
- **Volumi bassi** con JobSpy: rispetta i limiti in `local/jobspy-searches.json` e non aumentarli senza chiederlo a Enrico spiegando il rischio.
- **Mai inventare** esperienze, titoli di studio, competenze o risultati nel CV o nelle cover letter. Usa solo quello che c'è in `cv.md`, `article-digest.md` e nelle risposte di Enrico.
- **Privacy:** i dati personali vanno solo in `profilo/` e in `career-ops/` (entrambe escluse da Git). Non fare mai commit o push di dati personali. Non fare push su nessun repository remoto senza che Enrico lo chieda.
- Prima di comandi che installano software di sistema, modificano file di configurazione (shell, `~/.codex/config.toml`), programmano l'avvio automatico o cancellano file, **spiega e chiedi conferma**.

## File di stato
Tieni aggiornato `profilo/STATO.md` con:
- fase attuale e fasi completate (con data);
- sistema operativo e percorsi importanti (es. dove si trova `career-ops/`);
- conferma di Enrico sull'eccezione JobSpy (data e parole sue);
- differenze trovate rispetto a questa repository e come le hai risolte;
- problemi aperti.
