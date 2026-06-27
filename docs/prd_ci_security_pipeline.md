# Product Requirements Document: CI Security & Quality Layers

## 1. Goal
Enhance the Continuous Integration (CI) pipeline for the Chinese Chess project by introducing automated static security scanning and code linting. This ensures high code quality, enforces style consistency, and prevents security vulnerabilities or leaked secrets from being merged into production branches.

## 2. Scope
* **Static Application Security Testing (SAST):** Integrate [Bandit](https://bandit.readthedocs.io/) to scan Python source code for common security issues (e.g., hardcoded passwords, dangerous `eval()` usage).
* **Code Linting & Formatting:** Integrate [Ruff](https://docs.astral.sh/ruff/) to rapidly check for syntax errors, undefined variables, unused imports, and style violations.
* **Supply Chain Security:** Implement Action Pinning (using commit SHAs) for GitHub Actions to prevent hijacking via modified action tags (e.g., `v4`).

## 3. Out of Scope
* Deep dependency locking (e.g., converting `requirements.txt` to `Pipfile.lock` or `poetry.lock`) is deferred to a future phase to avoid disrupting the current development workflow.
* Dynamic Application Security Testing (DAST) or complex tools like CodeQL which require longer setup and execution times.

## 4. Implementation Details
* A new workflow file `.github/workflows/quality-and-security.yml` will be created.
* This workflow will run concurrently with the existing `project-correctness.yml` to minimize overall CI runtime.
* It will trigger on `push` and `pull_request` events.
* Steps:
  1. Secure Checkout (`actions/checkout` pinned to SHA).
  2. Setup Python environment with caching.
  3. Install `ruff` and `bandit`.
  4. Execute `ruff check .`.
  5. Execute `bandit -r .`.

## 5. Success Criteria
* The new GitHub Actions workflow successfully triggers on PRs and pushes.
* Any syntax errors, unused imports, or critical security flaws correctly fail the CI build, preventing merges of bad code.
* The workflow runs quickly (under 30 seconds) without impacting the broader evaluation suite.
