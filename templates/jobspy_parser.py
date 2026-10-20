"""Parser locale per career-ops: porta offerte da LinkedIn e Indeed tramite JobSpy.

Va copiato in career-ops/local/ e lanciato da local/run-jobspy.sh (vedi docs/PIANO.md, fase 3).

Contratto con career-ops (providers/local-parser.mjs):
- stdout: SOLO un JSON {"jobs": [{title, company, location, date_posted, url}, ...]}
- log ed errori: solo su stderr
- il testo di ogni annuncio viene salvato in jds/jobspy/ e passato come url "local:jds/jobspy/..."

Configurazione: local/jobspy-searches.json (vedi templates/jobspy-searches.example.json).
Messaggi e blocchi (es. 429 di LinkedIn): data/jobspy.log.
Variabile d'ambiente JOBSPY_TEST=1: una sola ricerca, 5 risultati per sito (per i test).
"""

import hashlib
import json
import numbers
import os
import random
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # cartella career-ops/
CONFIG_PATH = ROOT / "local" / "jobspy-searches.json"
JD_DIR = ROOT / "jds" / "jobspy"
LOG_PATH = ROOT / "data" / "jobspy.log"  # career-ops non mostra lo stderr dei parser: i messaggi restano qui
MIN_DESCRIPTION_CHARS = 200


def log(msg):
    print(f"[jobspy] {msg}", file=sys.stderr, flush=True)
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}\n")
    except OSError:
        pass


def clean(value):
    """Converte NaN/None/date di pandas in valori JSON semplici."""
    if value is None:
        return None
    try:
        import pandas as pd

        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, (datetime, date)):
        return value.isoformat()[:10]
    if hasattr(value, "item"):  # scalari numpy -> tipi Python
        value = value.item()
    if isinstance(value, bool):
        return value
    if isinstance(value, numbers.Integral):
        return int(value)
    if isinstance(value, numbers.Real):
        return int(value) if float(value).is_integer() else float(value)
    text = str(value).strip()
    return text or None


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


# LinkedIn scrive le città in inglese, Indeed in italiano: servono per riconoscere i doppioni.
CITY_ALIASES = {"milan": "milano", "rome": "roma", "turin": "torino", "naples": "napoli",
                "florence": "firenze", "genoa": "genova", "venice": "venezia", "padua": "padova"}


def city_of(location):
    city = normalize((location or "").split(",")[0])
    return CITY_ALIASES.get(city, city)


def safe_id(raw, url):
    if raw:
        return re.sub(r"[^A-Za-z0-9_-]+", "-", raw)[:80]
    return hashlib.sha1((url or "").encode()).hexdigest()[:16]


def load_config():
    if not CONFIG_PATH.exists():
        log(f"configurazione mancante: {CONFIG_PATH}")
        sys.exit(1)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if os.environ.get("JOBSPY_TEST") == "1":
        config["searches"] = config.get("searches", [])[:1]
        config["results_per_search"] = 5
        log("modalità test: 1 ricerca, 5 risultati per sito")
    return config


def scrape(scrape_jobs, site, search, config):
    """Una ricerca su un solo sito. Ritorna (DataFrame o None, messaggio di errore o None)."""
    params = dict(
        site_name=[site],
        search_term=search["term"],
        results_wanted=int(config.get("results_per_search", 20)),
        hours_old=int(config.get("hours_old", 24)),
        description_format="markdown",
        verbose=0,
    )
    if site == "linkedin":
        # Sempre "Città, Italy": con il solo nome della città LinkedIn può restituire città omonime all'estero.
        params["location"] = search.get("location_linkedin") or config.get("location_linkedin")
    else:
        params["location"] = search.get("location_indeed") or config.get("location_indeed")
        params["country_indeed"] = config.get("country_indeed", "italy")

    try:
        try:
            df = scrape_jobs(fetch_description=True, **params)
        except TypeError:
            # Versioni di JobSpy precedenti alla 1.2.0 usano il vecchio nome del parametro.
            df = scrape_jobs(linkedin_fetch_description=True, **params)
    except Exception as exc:  # noqa: BLE001 - un errore di una fonte non deve bloccare le altre
        return None, str(exc)

    errors = (getattr(df, "attrs", {}) or {}).get("errors") or {}
    error = errors.get(site) if isinstance(errors, dict) else None
    return df, (str(error) if error else None)


def write_jd(row, site, title, company, location, posted, url):
    job_id = safe_id(clean(row.get("id")), url)
    filename = f"{site}-{job_id}.md"
    description = clean(row.get("description")) or ""
    frontmatter = {
        "source": site,
        "url": url,
        "apply_url": clean(row.get("job_url_direct")),
        "title": title,
        "company": company,
        "location": location,
        "posted": posted,
        "is_remote": clean(row.get("is_remote")),
        "job_type": clean(row.get("job_type")),
        "salary_min": clean(row.get("min_amount")),
        "salary_max": clean(row.get("max_amount")),
        "salary_currency": clean(row.get("currency")),
        "salary_interval": clean(row.get("interval")),
        "note": "Annuncio aggregatore (LinkedIn/Indeed): da confermare sul sito dell'azienda, vedi AGENTS.md di career-ops.",
    }
    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines += ["---", "", f"# {title} — {company}", "", description, ""]
    (JD_DIR / filename).write_text("\n".join(lines), encoding="utf-8")
    return f"local:jds/jobspy/{filename}"


def main():
    config = load_config()
    try:
        from jobspy import scrape_jobs
    except ImportError:
        log("JobSpy non installato: esegui .venv-jobspy/bin/pip install python-jobspy")
        sys.exit(1)

    JD_DIR.mkdir(parents=True, exist_ok=True)
    sites = [s for s in config.get("sites", ["linkedin", "indeed"]) if s in ("linkedin", "indeed")]
    searches = config.get("searches", [])[: int(config.get("max_searches_per_run", 4))]
    pause_min, pause_max = config.get("pause_between_searches_seconds", [20, 45])
    deadline = time.monotonic() + int(config.get("max_run_seconds", 600))

    jobs = {}  # chiave doppione -> offerta
    blocked = set()

    for index, search in enumerate(searches):
        for site in sites:
            if site in blocked:
                continue
            if time.monotonic() > deadline:
                log("tempo massimo raggiunto: mi fermo con le offerte trovate finora")
                break
            log(f"ricerca '{search['term']}' su {site}")
            df, error = scrape(scrape_jobs, site, search, config)
            if error:
                log(f"{site}: {error}")
                if "429" in error or "block" in error.lower():
                    log(f"{site} ha limitato le richieste: lo salto per il resto di questa esecuzione")
                    blocked.add(site)
            if df is None or df.empty:
                continue
            if site == "linkedin" and df["description"].isna().mean() > 0.5:
                # JobSpy non segnala come errore il blocco delle pagine di dettaglio: lo si vede dalle descrizioni mancanti.
                log("linkedin: descrizioni non scaricate (probabile limite 429), lo salto per il resto di questa esecuzione")
                blocked.add("linkedin")

            for _, row in df.iterrows():
                url = clean(row.get("job_url"))
                title = clean(row.get("title"))
                if not url or not title:
                    continue
                company = clean(row.get("company"))
                location = clean(row.get("location"))
                # Stessa azienda + titolo + città = stessa offerta pubblicata su più siti.
                # Senza azienda non si può riconoscere un doppione: si usa l'URL.
                key = (normalize(company), normalize(title), city_of(location)) if company else ("url", url)
                has_description = len(clean(row.get("description")) or "") >= MIN_DESCRIPTION_CHARS
                existing = jobs.get(key)
                # Un doppione sostituisce l'offerta già trovata solo se porta il testo dell'annuncio che mancava.
                if existing and (existing["url"].startswith("local:") or not has_description):
                    continue

                # Un segnaposto unico: career-ops riconosce i doppioni anche da azienda + titolo.
                company = company or f"Azienda non indicata ({site} {safe_id(clean(row.get('id')), url)})"
                posted = clean(row.get("date_posted"))
                job = {"title": title, "company": company, "location": location, "date_posted": posted, "url": url}
                if has_description:
                    job["url"] = write_jd(row, site, title, company, location, posted, url)
                jobs[key] = job

        if index < len(searches) - 1 and time.monotonic() < deadline:
            time.sleep(random.uniform(pause_min, pause_max))

    log(f"totale offerte: {len(jobs)}")
    print(json.dumps({"jobs": list(jobs.values())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
