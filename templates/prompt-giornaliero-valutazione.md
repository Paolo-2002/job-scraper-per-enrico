Prima leggi per intero `AGENTS.md` (con `cat AGENTS.md`), poi esegui la modalità **pipeline** di career-ops sulle offerte in attesa in `data/pipeline.md`, rispettando quelle regole.

Regole per questa esecuzione automatica:
- Valuta al massimo **{{MAX_OFFERTE}}** offerte, partendo dalle più recenti.
- Per le righe `local:jds/jobspy/...` usa il testo dell'annuncio già salvato nel file: **non** aprire le pagine di LinkedIn o Indeed. Sono annunci aggregatori: trattali come indicato in `AGENTS.md` (da confermare sul sito dell'azienda; il link diretto, se c'è, è nel campo `apply_url`).
- Scrivi report e voto come previsto dalla modalità pipeline.
- **Non** generare CV né cover letter in questa esecuzione: lo decide Enrico (`auto_pdf_score_threshold` è impostato a 6 apposta).
- **Non** inviare candidature e **non** compilare moduli.
- Alla fine scrivi un riepilogo breve in italiano: quante offerte valutate e le 3 migliori con voto e motivo.
