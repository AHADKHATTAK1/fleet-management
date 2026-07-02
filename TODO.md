# TODO - scan all code finalize it

## Step 1 — Decide final product

- Choose Streamlit (`waybill_app.py`) as final UI.
- Keep React (`App.jsx`, `App.css`) and `index.html` as non-final prototypes (fix only glaring runtime bugs if needed).

## Step 2 — Professionalize Streamlit app

- Ensure receiving approvals update receiving status consistently.
- Ensure inventory updates are consistent when approvals happen.
- Clean up obvious inconsistencies and UI copy.
- Improve structure (small refactors only; keep behavior).

## Step 3 — Professionalize React (non-final)

- Fix toast timer initialization guard.
- Improve shipments search wiring (non-final / best-effort; React may not be runnable in this repo as-is).

## Step 4 — Professionalize Vanilla HTML (non-final)

- Ensure modal open/close handlers are robust.
- Fix any glaring JS errors / missing DOM hooks.

## Step 5 — Docs

- Update `README.md` with how to run the final app (Streamlit), plus notes about prototypes.

## Step 6 — Verify

- Run `python -m streamlit run waybill_app.py`.
- (Optional) run React build if a scaffold exists (likely not present).
