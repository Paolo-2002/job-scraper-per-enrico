Prima leggi per intero `AGENTS.md` (con `cat AGENTS.md`), poi esegui la modalità **pipeline** di career-ops sulle offerte in attesa in `data/pipeline.md`, rispettando quelle regole.

Regole per questa esecuzione automatica:
- Valuta al massimo **{{MAX_OFFERTE}}** offerte, partendo dalle più recenti.
- Per le righe `local:jds/jobspy/...` usa il testo dell'annuncio già salvato nel file: **non** aprire le pagine di LinkedIn o Indeed. Sono annunci aggregatori: trattali come indicato in `AGENTS.md` (da confermare sul sito dell'azienda; il link diretto, se c'è, è nel campo `apply_url`).
- Scrivi report e voto come previsto dalla modalità pipeline.
- Solo per le offerte con voto **≥ {{SOGLIA}}/5** (lo stesso valore di `auto_pdf_score_threshold`): genera il **CV su misura** in PDF e una **cover letter** personalizzata, nella lingua configurata in `language.output`, usando solo informazioni vere presenti in `cv.md` e `article-digest.md`.
- **Non** inviare candidature e **non** compilare moduli.
- Alla fine scrivi un riepilogo breve in italiano: quante offerte valutate, per quali sono pronti i documenti e dove si trovano i file.
