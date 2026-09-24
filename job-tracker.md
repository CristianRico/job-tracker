# job-tracker: especificación v0.1 (Fase 2)

## Problema
Cuando llegues a la Fase 6 vas a mandar candidaturas cada semana y tienes que saber a qué empresa escribiste, cuándo lo hiciste y en qué punto está cada proceso. Esta herramienta es para ti y la vas a usar de verdad.

## Stack (cerrado; nada fuera de esta lista)
- Python 3 + librería estándar: `sqlite3`, `argparse`, `datetime`
- `pytest` como única dependencia externa (dev)
- Sin ORM, sin frameworks y sin web. Todo eso va a la lista de "más adelante".

## Qué guarda cada candidatura
Tú decides los tipos, las restricciones (`NOT NULL`, `DEFAULT`, `CHECK`...) y el nombre de la tabla, y lo escribes en `schema.sql`.
- identificador
- empresa (**obligatoria**)
- puesto (**obligatorio**)
- URL de la oferta (opcional)
- estado: uno de `wishlist`, `applied`, `interview`, `offer`, `rejected` (por defecto `wishlist`)
- fecha de candidatura (opcional; tiene sentido cuando pasa a `applied`)
- notas (opcional)
- fecha de creación del registro (automática)

## Comandos (CLI)
```
python -m job_tracker add --company "Acme" --position "Junior Python Dev" [--url ...] [--notes ...]
python -m job_tracker list [--status applied]
python -m job_tracker show ID
python -m job_tracker update ID --status interview
python -m job_tracker delete ID
python -m job_tracker stats          # nº de candidaturas por estado
```

## Reglas de negocio (cada una lleva su test)
1. Empresa o puesto vacíos (o solo espacios): error.
2. Estado fuera de la lista: error.
3. `show`/`update`/`delete` con un ID que no existe: error claro, nunca un traceback.
4. Si una candidatura pasa a `applied` y no tiene fecha, se guarda la de hoy.
5. En la CLI, cualquier error se muestra con un mensaje legible y el programa termina con un código distinto de 0.

## Arquitectura (obligatoria)
- La lógica y el SQL van en un módulo (p. ej. `db.py` o `repository.py`): funciones que reciben una conexión y devuelven datos. **No hacen `print`.**
- La CLI va en otro módulo (`cli.py` / `__main__.py`): solo parsea argumentos, llama a la lógica e imprime.
- Queries **siempre parametrizadas** con `?`. Nunca metas datos en el SQL con f-strings (aprende por qué: SQL injection).
- Los tests prueban la capa de lógica contra una base de datos temporal (`":memory:"` o la fixture `tmp_path` de pytest). **Nunca** contra tu base de datos real.

## Repo
- Repo público `job-tracker` en GitHub, **fuera** de `learn/` (p. ej. `~/dev/job-tracker`).
- `.gitignore`: venv, `__pycache__`, `*.db`
- `README.md`: qué es, instalación, uso con ejemplos y cómo ejecutar los tests.
- Commits pequeños con prefijo (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).

## Hitos (cada uno se cierra con pytest en verde **pegado** y un push)
1. **Esqueleto**: repo, venv, pytest, `schema.sql` y una función que añade una candidatura, con un test que la añade y la vuelve a leer.
2. **Lectura**: `list` (con filtro por estado) y `show`, más sus tests, incluido el del ID inexistente.
3. **Escritura**: `update` y `delete` con las reglas 1-4 y sus tests.
4. **CLI**: argparse conectado a la lógica, `stats` (GROUP BY) y la regla 5.
5. **Entrega**: README completo, repo limpio. Con esto cumples el criterio de salida de la Fase 2.

## Fuera de alcance (lista "más adelante")
API (Fase 3, FastAPI + PostgreSQL), frontend (React), usuarios y login, recordatorios, exportar a CSV.
