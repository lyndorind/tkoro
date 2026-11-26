# Lab 7 — unfinished requirements: ready-to-apply repository files

This overlay is for `github.com/lyndorind/tkoro`. It **does not replace** your working `compose.yaml`, `db_api.py`, `Dockerfile`, `main.py`, or Lab 5 / Lab 6 workflows.

## What is included

| File | Purpose |
| --- | --- |
| `.github/workflows/lab7-pr-ci.yml` | PR CI: parallel unit tests, temporary Docker image tag, Postman integration tests with PostgreSQL `services`, JMeter load test with resource monitoring |
| `tests/test_lab7_model.py` | Four fast Pydantic validation tests |
| `postman/lab7.postman_collection.json` | Five API requests: health, create, read, 404, invalid note |
| `jmeter/lab7.jmx` | 20 threads × 10 repetitions × two GET requests = ~400 samples |
| `scripts/lab7_load_ci.sh` | JMeter CLI + repeated CPU/memory measurements using `docker stats` |
| `VM_DEPLOYMENT.md` | Separate virtual-machine deployment and screenshot evidence |
| `CONTROL_QUESTIONS.md` | Answers to all 10 control questions from the lab assignment (Ukrainian) |

## Before using

1. The original Lab 7 PR was already merged into `main`. Create a **new branch and a new PR** for these missing requirements.
2. Copy the **contents** of this overlay into the **root of your existing `tkoro` repository**. Preserve nested paths such as `.github/workflows/`.
3. Don't commit or upload `secrets/`, a database password, `.env` containing secrets, or PostgreSQL volume data. This overlay contains no production credentials. All CI DB passwords are deliberately dummy test values.
4. Your existing `db_api.py` must have `NoteIn(text: str = Field(min_length=1, max_length=500))`, the POST and GET note endpoints, and the `DB_PASSWORD` environment-variable fallback. These were present in the earlier PR screenshots.
5. Your existing `main.py` must expose `app` and `/health`, importing `db_api` and creating the notes table at startup.

## Windows PowerShell: create the next PR

From the repository folder:

```powershell
cd C:\Users\ADMIN\Desktop\git-lab2\tkoro
git switch main
git pull origin main
git switch -c feature/lab7-pr-ci-tests
```

Extract `lab7_completion_bundle.zip` somewhere (for example `Downloads`) and copy its **inside folders and files** into this `tkoro` directory. Windows File Explorer can merge the `.github` directory. Then:

```powershell
git add .github/workflows/lab7-pr-ci.yml tests/test_lab7_model.py postman/lab7.postman_collection.json jmeter/lab7.jmx scripts/lab7_load_ci.sh README_LAB7.md VM_DEPLOYMENT.md CONTROL_QUESTIONS.md
git diff --cached --stat
git commit -m "feat: add Lab 7 PR integration and load test pipeline"
git push -u origin feature/lab7-pr-ci-tests
Start-Process "https://github.com/lyndorind/tkoro/compare/main...feature/lab7-pr-ci-tests"
```

Click **Create pull request**, choose one of the repository organization members as reviewer, and let the four **Lab 7** jobs run. The old **Lab 5 – Lint and Tests** check does not need to be fixed for this lab, as discussed.

## What successful CI looks like

The workflow has four independent (parallel) jobs:

1. **Lab 7 unit tests**: four Pydantic validation tests succeed.
2. **Build Docker image with temporary PR tag**: Docker image builds locally with a tag `quay.io/lyndorind/tkoro:pr-N-COMMITSHA`. It is intentionally **not pushed** to Quay.
3. **Postman integration tests and HTML report**: PostgreSQL runs as GitHub Actions `services.postgres`; FastAPI starts on the runner; Newman verifies real database operations. Artifact `lab7-postman-report-*` includes `index.html` and `results.json`.
4. **JMeter load and Docker resource monitoring**: PostgreSQL again runs as a `services` container; API runs as a Docker container. JMeter issues ~400 HTTP requests while `docker stats` records API and PostgreSQL CPU and memory. Artifact `lab7-jmeter-report-*` includes `html/index.html`, `results.jtl`, `docker-stats.csv`, and `jmeter.log`.

Go to **PR → Checks**, select the job and scroll to **Artifacts** in the workflow run to download the reports. These files are only generated **after GitHub Actions actually runs**; they are not pre-existing evidence.

## Verification from your Windows machine

For the already-working local Docker Compose stack, run:

```powershell
docker compose ps
docker inspect tkoro-api-1 --format '{{.Name}} {{.State.Status}} {{.Config.Image}}'
docker inspect tkoro-db-1 --format '{{.Name}} {{.State.Health.Status}} {{.Config.Image}}'
docker compose logs --tail=30 api
docker compose logs --tail=30 db
docker stats --no-stream tkoro-api-1 tkoro-db-1
Invoke-RestMethod "http://localhost:8000/notes/1"
```

Take screenshots of these **successful** outputs. Avoid `docker compose down -v`: it removes the database volume and loses notes.

## Suggested evidence screenshots (Ukrainian labels)

1. **Скрін №1 — Створення PR із завданнями лабораторної роботи №7.**
2. **Скрін №2 — Паралельне виконання unit-тестів, Docker build, Postman і JMeter у GitHub Actions.**
3. **Скрін №3 — Тимчасовий PR-тег Docker-образу в успішному job.**
4. **Скрін №4 — HTML-звіт Newman/Postman та artifact у GitHub Actions.**
5. **Скрін №5 — HTML Dashboard Apache JMeter і файл статистики docker-stats.csv.**
6. **Скрін №6 — Налаштування окремої віртуальної машини Ubuntu.**
7. **Скрін №7 — Запущені контейнери API та PostgreSQL у ВМ.**
8. **Скрін №8 — docker inspect, docker logs та docker stats у ВМ.**
9. **Скрін №9 — Успішний GET /notes/1 через переадресацію порту ВМ.**

Do not present screenshots or CI reports as actual evidence until the corresponding test or VM run has been completed.
