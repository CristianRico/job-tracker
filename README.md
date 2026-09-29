# job-tracker
CLI para llevar el seguimiento de candidaturas de empleo, con SQLite.

## Requisitos
Python 3.9+

## Instalación
```bash
git clone https://github.com/CristianRico/job-tracker.git
cd job-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso
Estados válidos: `wishlist`, `applied`, `interview`, `offer`, `rejected` (por defecto `wishlist`).
Al pasar una candidatura a `applied`, si no tiene fecha de candidatura se guarda la de hoy.

Los datos se guardan en `~/.job_tracker.db`.

### add
```
$ python -m job_tracker add --company "Wayne Enterprises" --position "Junior Software Engineer"
Candidatura en Wayne Enterprises como Junior Software Engineer añadida con id 6
```
Opcionales: `--url` y `--notes`.

### list
```
$ python -m job_tracker list
  id  company            position                  url                                         status     applied_at    notes                              created_at
----  -----------------  ------------------------  ------------------------------------------  ---------  ------------  ---------------------------------  ------------
   1  Acme               Junior Python Dev         https://acme.example.com/jobs/123           wishlist                 Referido por un antiguo compañero  2026-09-29
   2  Globex             Backend Developer         https://globex.example.com/careers/backend  applied    2026-09-29                                       2026-09-29
   3  Initech            Data Engineer                                                         interview  2026-09-29    Stack: Python + Airflow            2026-09-29
   4  Umbrella Labs      QA Automation Engineer                                                rejected   2026-09-29                                       2026-09-29
   5  Stark Industries   Python Developer                                                      offer      2026-09-29    Remoto, 3 entrevistas              2026-09-29
   6  Wayne Enterprises  Junior Software Engineer                                              wishlist                                                    2026-09-29
```

Filtrando por estado:
```
$ python -m job_tracker list --status wishlist
  id  company            position                  url                                status    applied_at    notes                              created_at
----  -----------------  ------------------------  ---------------------------------  --------  ------------  ---------------------------------  ------------
   1  Acme               Junior Python Dev         https://acme.example.com/jobs/123  wishlist                Referido por un antiguo compañero  2026-09-29
   6  Wayne Enterprises  Junior Software Engineer                                     wishlist                                                   2026-09-29
```

### show
```
$ python -m job_tracker show 3
Campo       Valor
----------  -----------------------
id          3
company     Initech
position    Data Engineer
url
status      interview
applied_at  2026-09-29
notes       Stack: Python + Airflow
created_at  2026-09-29
```

### update
```
$ python -m job_tracker update 1 --status applied
Campo       Valor
----------  ---------------------------------
id          1
company     Acme
position    Junior Python Dev
url         https://acme.example.com/jobs/123
status      applied
applied_at  2026-09-29
notes       Referido por un antiguo compañero
created_at  2026-09-29
```

### stats
```
$ python -m job_tracker stats
Estado       Total
---------  -------
wishlist         1
applied          2
interview        1
offer            1
rejected         1
```

### delete
```
$ python -m job_tracker delete 4
Se ha eliminado la candidatura 4
```

### Errores
Cualquier error se muestra con un mensaje legible y el programa termina con código 1:
```
$ python -m job_tracker show 999
Error: No se encontró candidatura con id 999
```

## Tests
```bash
python -m pytest
```
