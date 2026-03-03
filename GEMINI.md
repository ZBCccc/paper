# GEMINI.md - PhD Thesis Research Context (VSSE)

This workspace is dedicated to the research and writing of a PhD thesis titled (tentatively) "Verifiable Searchable Symmetric Encryption (VSSE) with Forward and Backward Privacy". The research focus is on enhancing the **Nomos** protocol with verifiable mechanisms using Merkle Hash Trees (MHT) and Embedded Commitments.

## 1. Project Overview

- **Core Goal**: Implement and document a lightweight verifiable mechanism for multi-user, multi-keyword searchable encryption in the limited-leakage privacy model.
- **Main Innovations**:
    1. **Verifiable Status Check (VQ)**: Using a Merkle-ized XSet (QTree) to ensure bit-value authenticity (Server cannot forge bit values in Bloom Filter-like structures).
    2. **Embedded Commitment (AB)**: Using embedded commitments in TSet records to bind XSet physical addresses, preventing "Address Substitution Attacks" where the server proves bit values for the wrong addresses.
- **Combined Result**: Complete verifiable eligibility testing (Correct Address + Authentic Bit Value).

## 2. Directory Structure & Strategy

The project follows a three-layer document structure as defined in `CLAUDE.md`:

| Level | Path | Loading Strategy |
| :--- | :--- | :--- |
| **Global** | `CLAUDE.md`, `GEMINI.md` | Auto-loaded every session. |
| **Rules** | `rules/` | Auto-loaded at session start. Contains `控制面板.md` (Status), `角色与硬约束.md` (Style), `工作流程.md` (Workflow). |
| **Docs** | `docs/` | On-demand. Contains `memory/` (Research logs), `论文Markdown库/` (Xray literature), and methodology. |
| **Latex** | `HUST-PhD-Thesis-Latex/` | The primary LaTeX engineering project. |
| **Refs** | `ref-thesis/` | Original PDF literature. |

## 3. Building and Running

### LaTeX Project (`HUST-PhD-Thesis-Latex/`)
- **Main File**: `main.tex`
- **Compiler**: `xelatex` + `bibtex`.
- **Standard Compilation Cycle**: `xelatex -> bibtex -> xelatex -> xelatex`.
- **Editor Recommendation**: VSCode with `LaTeX Workshop` (settings provided in `.vscode/settings.json`).
- **Cleaning**: Clean `.aux` and temporary files before full validation of cross-references (`\label`/`\ref`).
- **Note**: `pgfplots` is used for 8 experimental figures in `experiments.tex`; initial compilation may be slow.

### Scripts
- **Plotting**: `HUST-PhD-Thesis-Latex/scripts/plot_experiments.py` for generating figures from data.

## 4. Development & Writing Conventions

### Academic Writing Role
You are a **Top-tier Cryptography Researcher and Writing Coach**.
- **Style**: Direct, technical, objective, and restrained. Use "PPT adversary", "leakage function", "negl(λ)".
- **Meta-narrative Prohibited**: Avoid phrases like "For ease of description," "We will now introduce," or "It is worth noting." Stick to direct technical statements about models, definitions, and proofs.
- **Consistency**: Rigorously maintain symbol consistency across all chapters (Definitions, Algorithms, and Proofs).

### Verification Workflow
- **Bug Fixes**: Reproduce any LaTeX/BibTeX errors before fixing.
- **Security Proofs**: Use the **Game-Hopping** technique for all formal proofs.
- **New Literature**: Before citing new PDFs, extract them into `docs/论文Markdown库/` using the `ljg-xray-paper` skill.

## 5. Current Thesis Status (as of 2026-02-27)

- **Chapter 1 (Intro)**: Core tables refined; citation cleanup needed.
- **Chapter 2 (MHT/VQ)**: Formal definitions (Propositions 1-4) and `booktabs` tables complete.
- **Chapter 3 (Embedded/AB)**: Formal proofs (Propositions 5-6) and algorithm blocks (5-7) complete.
- **Chapter 4 (Experiments)**: Framework and `pgfplots` templates ready. **Experimental data is pending (marked as 【待补充】).**
- **Chapter 5 (Conclusion)**: Framework only.

## 6. Maintenance
Update `rules/控制面板.md` after completing any sub-task. Every week, ensure the project is in a "Compilable State."
