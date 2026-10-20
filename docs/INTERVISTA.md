# Intervista iniziale

Obiettivo: raccogliere **il 100% del contesto** necessario per configurare il sistema su misura per Enrico.

## Come condurla (istruzioni per Codex)
- Procedi **un blocco alla volta**, nell'ordine. Per ogni blocco fai le domande in modo colloquiale, non come un modulo.
- Se Enrico non sa rispondere, spiega a cosa serve la domanda e proponi un **default** (indicato sotto con *Default*). Segna le risposte di default con `(default)`.
- Se una risposta è vaga ("un lavoro nel marketing"), fai domande di approfondimento finché non hai elementi concreti (titoli di ruolo, esempi di annunci).
- Dopo ogni blocco salva le risposte in `profilo/RISPOSTE.md` (crea la cartella `profilo/` se non esiste), così nulla si perde se la sessione si interrompe. Se la sessione riparte e `RISPOSTE.md` esiste già, riprendi dal primo blocco mancante.
- Alla fine mostra un **riepilogo completo** e chiedi a Enrico di confermarlo o correggerlo. Solo dopo la conferma crea `profilo/STATO.md` con "Intervista completata" e passa a `docs/PIANO.md`.

---

## Blocco 1 — Il computer
1. Usi **Mac** o **Windows**? (Su Mac: chip Apple o Intel? Su Windows: versione 10 o 11?)
   - **Windows:** controlla subito se Codex sta girando dentro **Ubuntu (WSL2)** (ad esempio con `uname -a`). Se no, **interrompi l'intervista qui** e segui la Fase 0, passo 1 di `docs/PIANO.md` per passare a Ubuntu; poi riprendi l'intervista da lì, copiando la cartella `profilo/`.
2. Dove si trova questa cartella? Su Mac non deve stare in Scrivania, Documenti, Download o iCloud: macOS bloccherebbe l'automazione giornaliera. Se è lì, proponi di spostarla nella cartella utente (`~`) prima di continuare.
3. Il computer è **acceso la mattina**? A che ora di solito? (Serve per l'automazione giornaliera. Su Mac, se il computer è spento a quell'ora, la ricerca di quel giorno salta; su Windows parte appena il PC si riaccende.) *Default: 9:00.*
4. Fuso orario. *Default: Europe/Rome.*

## Blocco 2 — Codex
5. Che **piano** hai su ChatGPT / Codex (Plus, Pro, Business…)? Determina quante offerte al giorno possiamo far valutare. **Se Enrico non ha un piano che include Codex, fermati e spiegaglielo prima di continuare.**
6. Quanto vuoi "spendere" del piano per ogni valutazione?
   - **economy**: più veloce ed economico, adatto a tante offerte;
   - **standard**: equilibrato;
   - **premium**: il modello più capace, per le offerte che contano di più.
   *Default: standard.*

## Blocco 3 — Chi sei
7. Nome e cognome, città di residenza.
8. Email e telefono da mettere su CV e cover letter.
9. Link al profilo **LinkedIn** ed eventuali portfolio, GitHub, sito personale.
10. Hai la cittadinanza UE o un permesso di lavoro? Saresti disposto a trasferirti?

## Blocco 4 — Il tuo CV
11. Hai un CV attuale?
    - **(a) Sì:** chiedi di esportarlo in **PDF** (da Word: File → Salva come → PDF). Apri tu la cartella `profilo/` per lui (su Mac `open profilo`, su Ubuntu/WSL `explorer.exe profilo`) e chiedigli di trascinarci dentro il file. In alternativa può incollare il testo del CV in chat.
    - **(b) No:** lo costruirete insieme. Fai domande su esperienze lavorative (azienda, ruolo, periodo, cosa faceva, risultati), studi, competenze, lingue, certificazioni. Non inventare nulla.
12. Ci sono esperienze, progetti, certificazioni o risultati **non presenti nel CV** che vale la pena aggiungere? Cerca numeri concreti: fatturato, risparmi, clienti, team gestiti…
13. C'è qualcosa che **non vuoi** che compaia (es. un'esperienza vecchia, un'informazione personale)?

## Blocco 5 — Che lavoro cerchi
14. Quali **ruoli** cerchi? Chiedi 3–6 titoli concreti, **sia in italiano sia in inglese** (es. "analista dati" / "data analyst").
15. **Livello**: stage, junior, mid, senior, responsabile? (Importante: i filtri predefiniti di career-ops scartano "Junior" e "Intern/Internship"; se Enrico li cerca, vanno tolti. Se invece **non** cerca uno stage, aggiungi "Stage" e "Tirocinio" alle parole da scartare, D18.)
16. **Settori** preferiti e settori da evitare.
17. **Aziende** dei sogni (se ce ne sono) e aziende da escludere (es. ex datori di lavoro).
18. Parole che, se compaiono nel titolo, rendono l'offerta **da scartare** (es. "porta a porta", "senior" se sei junior). *Default: nessuna, la stabiliamo insieme.*
19. Tipo di contratto: indeterminato, determinato, partita IVA, freelance, stage?
20. **Stipendio**: RAL desiderata e RAL minima sotto la quale non ha senso candidarsi.
21. Quando potresti iniziare? Hai un preavviso da rispettare?
22. Cosa ti motiva in un lavoro e cosa invece ti pesa? Ci sono condizioni che escludono un'offerta a priori (es. niente startup sotto 20 persone, niente lavoro solo in presenza)?

## Blocco 6 — Dove
23. In quali **città** cerchi? (Il sistema cerca città per città.)
24. **Remoto / ibrido / in presenza**: cosa accetti? Se accetti il remoto, va bene **qualsiasi città italiana** purché da remoto?
25. Per ora il sistema cerca **solo in Italia**. Ti interessa anche l'estero? (Si annota e si può aggiungere dopo.)

## Blocco 7 — Lingue e stile
26. Che lingue parli e a che livello (madrelingua, C1, B2…)?
27. In che lingua vuoi report, CV e cover letter? career-ops usa una lingua principale per tutto; per un singolo annuncio in un'altra lingua potrai chiedere i documenti in quella lingua. *Default: italiano.*
28. Che **tono** preferisci per le cover letter: formale, diretto, caloroso? Hai una lettera o un testo scritto da te che ti piace, da usare come esempio di stile?

## Blocco 8 — Quanto automatizzare
29. Ogni mattina cosa deve fare il sistema da solo?
    - **(a) Solo valutazione:** trova le offerte e dà un voto. Tu scegli su quali preparare CV e lettera.
    - **(b) Valutazione + documenti:** per le offerte con voto alto prepara anche CV e cover letter.

    *Default: (a), pesa meno sul piano Codex. Si può cambiare in qualsiasi momento.*
30. Se hai scelto (b): da che **voto** in su preparare i documenti? *Default: 4.0/5.*
31. Quante **offerte al giorno** al massimo vuoi far valutare? *Default: 15.*
32. Quante **ricerche** diverse al giorno su LinkedIn e Indeed? Ognuna è un ruolo + una città. *Default: 4, per restare a basso volume.* Se le combinazioni ruolo + città sono di più, scegliete insieme le più importanti.

## Blocco 9 — LinkedIn, Indeed e regole
33. Spiega con chiarezza, poi chiedi una scelta esplicita:
    > LinkedIn e Indeed vietano nei loro termini d'uso la raccolta automatica degli annunci, anche senza login. Anche career-ops, nel suo `LEGAL_DISCLAIMER.md`, sconsiglia di usarlo per questo. Per un uso personale, a basso volume e senza login il rischio pratico è basso (al massimo un blocco temporaneo), ma esiste.

    - **(a) JobSpy:** raccolta automatica di LinkedIn e Indeed, senza login, a basso volume, dal computer di casa. È la scelta consigliata dal progetto.
    - **(b) Niente JobSpy:** solo siti carriere delle aziende, più i link di LinkedIn/Indeed che incolli tu a mano quando vedi un annuncio interessante.

    Registra in `profilo/RISPOSTE.md` la scelta **con le parole di Enrico** e la data.
34. Ti interessa anche **InfoJobs**? (Non è supportato da JobSpy: si annota e si valuta più avanti.)

## Blocco 10 — Dashboard
35. Cosa vuoi vedere a colpo d'occhio? Proponi: offerte nuove con voto, stato delle candidature (da valutare / documenti pronti / inviata / colloquio / rifiutata), link ai PDF, statistiche. Chiedi se manca qualcosa.

## Blocco 11 — Altro
36. C'è qualcosa che il sistema **non deve mai** fare, oltre alle regole già previste?
37. Domande o dubbi su come funziona?

---

## Dove finiscono le risposte (per Codex)

| Domande | Destinazione in `career-ops/` |
|---|---|
| 4, 6, 7, 8, 9, 10, 14, 20, 23, 24 | `node onboard-write.mjs` (profilo e portali, Fase 2) |
| 11, 12, 13 | `cv.md` e `article-digest.md` (Fase 2) |
| 15, 16, 17, 18, 22 | `modes/_profile.md`, `modes/_brief.md`, filtri titolo in `portals.yml`, `tracked_companies`, `data/blacklist.md` (Fase 2) |
| 19, 21, 26 | `config/profile.yml` / `modes/_profile.md` (Fase 2) |
| 27 | `language.output` in `config/profile.yml` (Fase 2) |
| 28 | `voice-dna.md` e, se c'è un testo d'esempio, `writing-samples/` (Fase 2) |
| 36 | `modes/_custom.md` (Fase 2) |
| 14, 23, 24, 32, 33 | `local/jobspy-searches.json` (Fase 3) |
| 29, 30, 31 | prompt giornaliero e `auto_pdf_score_threshold` (Fase 5) |
| 1, 2 | prerequisiti e posizione della cartella (Fase 0) |
| 3 | orario dell'automazione giornaliera (Fase 5) |
| 5 | calibrare D6 e D31 (quante offerte e con che modello) |
| 25, 34, 35 | note in `profilo/RISPOSTE.md` per sviluppi futuri / dashboard (Fase 6) |

## Formato di `profilo/RISPOSTE.md`

```markdown
# Risposte intervista — Enrico
Data: AAAA-MM-GG

## 1. Computer
- Sistema operativo: ...
...

## Riepilogo decisioni
- JobSpy (LinkedIn/Indeed): sì / no — consenso informato: "<parole di Enrico>" (data)
- Automazione: (a) solo valutazione | (b) valutazione + documenti, soglia X
- Ricerche JobSpy al giorno: N — Offerte valutate al giorno: N
- Orario automazione: HH:MM
- Lingua documenti: ...
```
