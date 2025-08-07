# Formula Engine – Business‑Level Logic & Functionality

## 1 | Purpose
A universal back‑tracing service that turns any complex Excel workbook into a **transparent, scenario‑ready digital model**.  It reveals how the headline KPI (profit, NPV, margin, loan‑covenant) is computed, isolates the exact input levers, and lets a user tweak those levers without ever touching raw Excel.

## 2 | Core Business Capabilities
| Capability | Why it matters to the business |
|---|---|
| **One‑click lineage** | Decision‑makers see *only* the formulas that actually drive the headline number; legacy tabs & “black” sheets are silently ignored. |
| **Dynamic‑link resolver** | Even models with `INDIRECT`, `OFFSET`, `XLOOKUP`, table refs, etc. are traced with 100 % fidelity via a headless Excel session. |
| **Plan / Fact split** | The engine tags every path as **FACT** (actuals to date) vs **PLAN** (forecast remainder) → supports rolling re‑forecasts & scenario deltas. |
| **Input panel auto‑generation** | For every leaf cell that is manually typed (or external), the UI surface shows a friendly control (slider, date‑picker, % field). |
| **Scenario sandbox** | Users drag sliders on mobile and instantly see recalculated KPIs; Monte‑Carlo & sensitivity can be launched from the same screen. |
| **Audit trail** | One‑click PDF/HTML dossier: tree diagram, list of manual inputs, cycles, Excel≠Engine mismatches, and key unit conversions. |

## 3 | End‑to‑End Flow (business language)
1. **Upload Workbook** → the engine fingerprints the file; no data leaves the secure perimeter.
2. **Choose Seed KPI** → usually a cell on the summary sheet (Profit, NPV, LLCR, DSCR).
3. **Engine Trace** (5‑10 s typical)
   * Reads workbook structure (no calc).
   * Parses static references in the seed formula.
   * If formula contains dynamic functions, fires a sandboxed Excel `Evaluate()` and logs every cell Excel reads.
   * Repeats recursively until reaching pure values / external links.
4. **Clean DAG** returned – only 1–3 % of the workbook, zero noise.
5. **Semantic pass**
   * Labels nodes (price / cost / volume / tax…) by NLP on nearby headers.
   * Tags FACT vs PLAN by sheet‑names & date‑cut.
6. **UI build**
   * For each PLAN leaf → suitable input control.
   * For each FACT leaf → greyed, read‑only.
7. **User Scenarios**
   * Mobile slider “Key Rate –1 pp” → engine recomputes only impacted sub‑DAG, returns new KPI in <300 ms.
   * Monte‑Carlo: engine applies stoch. distributions on selected levers, streams summary stats.
8. **Audit Report** → PDF/HTML for board or lender, timestamped & tamper‑proof.

## 4 | Module Responsibilities (non‑technical wording)
* **xls‑extractor** – turns Excel into a neutral JSON snapshot, but does *not* calculate.
* **static‑refs** – finds obvious links in any formula.
* **dynamic‑trace** – uses *real* Excel to catch hidden links; guarantees 100 % coverage.
* **dag‑builder** – assembles the minimal dependency tree and removes dead sheets.
* **excel‑verify** – double‑checks every computed value against Excel to prove fidelity.
* **unit‑normalizer** – aligns units (₽, тыс ₽, м², шт, кВт⋅ч) and stitches timeseries.
* **semantic‑tagger** – attaches business meaning so the UI can speak finance, not “Sheet3!C42”.
* **scenario‑runner** – fast deterministic calc + Monte‑Carlo + optimisation hooks.
* **audit‑reporter** – renders a Gantt‑style tree & KPI deltas for compliance packs.
* **api‑gateway** – single entry, auth, rate‑limit, cache.

## 5 | Key Business Rules
1. **No orphan data** – if a sheet/column is not referenced, it is excluded automatically.
2. **Excel is the truth** – the engine must reproduce the exact numeric result of the original workbook; mismatch >1e‑6 —— flags error.
3. **Read‑only default** – unless user explicitly overrides, FACT cells remain locked.
4. **Unit integrity** – currency mismatches (₽ vs $) raise a blocking error before calc.
5. **Cycle intolerance** – cycles are detected; either resolved by user or simulated iteratively (if flagged as intentional cash‑flow spiral).

## 6 | User Benefits (non‑dev speak)
* **Executives** – “I see what drives my bottom line and can run ‘what‑if’ in the lift.”
* **Analysts** – spend time on thinking, not tracing 30 000 formulas.
* **Risk & Audit** – instant provenance map; known manual overrides highlighted.
* **IT / Security** – sensitive numbers stay on‑prem; output is a thin JSON graph.

## 7 | Roadmap (business milestones)
| Q | Deliverable | Business outcome |
|---|--------------|------------------|
| Q1 | MVP (trace, DAG, input panel) | Pilot with 2 developers, 1 bank |
| Q2 | Monte‑Carlo + audit pdf | Lender due‑diligence ready |
| Q3 | On‑prem bundle + RBAC | Large enterprise roll‑outs |
| Q4 | Cross‑model scenario hub | Portfolio “what‑if” across 50 projects |

---
*Document version 0.1 · prepared by Leonardo‑GPT for FORMULA‑ENGINE kick‑off.*

