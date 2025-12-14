# Repository Guidelines

## Project Structure & Module Organization
- Keep all implementation code under `src/` with clear subfolders per feature (e.g., `src/pipelines/`, `src/ui/`, `src/utils/`).
- Store reusable assets (sample images, fixtures) in `assets/` and keep large files out of the repo when possible; prefer download scripts.
- Place automated tests in `tests/`, mirroring the `src/` layout for easy discovery (`tests/ui/test_viewer.py` → `src/ui/viewer.py`).
- Reserve `scripts/` for one-off maintenance or data-prep tools; document usage in script headers.

## Build, Test, and Development Commands
- Create and activate a virtual environment before working: `python -m venv .venv && source .venv/bin/activate`.
- Install dependencies from `requirements.txt` (or `pyproject.toml` when added): `pip install -r requirements.txt`.
- Run the full test suite with `pytest` from the repo root once tests are present.
- Format and lint before pushing: `ruff check .` (lint) and `ruff format .` (format) if ruff is configured; otherwise run the equivalent tools you add.
- For local smoke checks of scripts, prefer `python -m src.<module>` so imports resolve consistently.

## Coding Style & Naming Conventions
- Follow PEP 8 for Python: 4-space indentation, lowercase_with_underscores for functions and variables, CapWords for classes.
- Keep modules focused; avoid files that do “too much.” Extract shared helpers into `src/utils/`.
- Use explicit type hints on public functions and dataclasses for structured data passed between stages.
- Name image-processing stages descriptively (`load_image`, `detect_edges`, `aggregate_stats`), and keep side effects (I/O) at the boundaries.

## Testing Guidelines
- Co-locate tests that mirror the code under test; name files `test_<module>.py` and functions `test_<behavior>`.
- Prefer deterministic fixtures; store small image fixtures in `tests/fixtures/` and generate larger ones at test time to keep the repo light.
- Aim for meaningful coverage on core pipelines (parsers, detectors, analyzers); add regression tests for any bug fix.
- When adding CLI or script behavior, include an integration-style test that exercises argument parsing and a happy-path run.

## Commit & Pull Request Guidelines
- Use concise commit subjects in imperative mood (e.g., `Add histogram analyzer`, `Refine edge detection thresholds`); add a short body if behavior changes.
- Reference issues in commit bodies or PR descriptions when applicable.
- PRs should summarize the change, list test commands run, and include screenshots or sample outputs when UI or image results change.
- Keep PRs small and focused; split refactors from feature work to ease review.

## Security & Configuration Tips
- Avoid committing secrets or API keys; use environment variables and a `.env.example` stub if configuration is needed.
- Check large binary assets into LFS or provide a download script instead of storing them directly in the repo.
- Pin dependencies when possible to keep image-processing outputs reproducible across machines.
