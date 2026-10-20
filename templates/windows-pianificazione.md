# Automazione giornaliera su Windows (WSL2)

Su Windows tutto il sistema vive dentro Ubuntu (WSL2). L'Utilità di pianificazione di Windows avvia ogni giorno lo script dentro Ubuntu.

## 1. Trova i dati necessari
In **PowerShell** (Windows), il nome della distribuzione, di solito "Ubuntu":
```powershell
wsl -l -v
```
In **Ubuntu**, il percorso completo di career-ops (es. `/home/enrico/job-scraper-per-enrico/career-ops`):
```bash
cd ~/job-scraper-per-enrico/career-ops && pwd
```

## 2. Crea l'attività (PowerShell di Windows, non serve amministratore)
Sostituisci `Ubuntu`, il percorso e l'orario:
```powershell
$azione  = New-ScheduledTaskAction -Execute "wsl.exe" -Argument '-d Ubuntu -- bash -lc "/home/enrico/job-scraper-per-enrico/career-ops/local/daily.sh"'
$orario  = New-ScheduledTaskTrigger -Daily -At 9am
$opzioni = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries
Register-ScheduledTask -TaskName "Job Scraper Enrico" -Action $azione -Trigger $orario -Settings $opzioni
```
`-StartWhenAvailable` fa partire l'attività appena possibile se il PC era spento all'orario previsto.

## 3. Prova e gestione
```powershell
Start-ScheduledTask -TaskName "Job Scraper Enrico"        # lancia subito (prova)
Disable-ScheduledTask -TaskName "Job Scraper Enrico"      # pausa
Enable-ScheduledTask -TaskName "Job Scraper Enrico"       # riattiva
Unregister-ScheduledTask -TaskName "Job Scraper Enrico"   # elimina
```
Il risultato si legge dentro Ubuntu in `career-ops/data/daily.log`.

## Note
- `codex` deve essere installato e autenticato **dentro Ubuntu**.
- Se Node è installato con nvm, `daily.sh` lo carica da solo.
