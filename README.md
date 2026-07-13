# Contract Intelligence — Client Demo Package

Static UI bundle that talks directly to the Cloud Run backend. No GCP
account, no `gcloud` CLI, no proxy — just a local static HTTP server.

## Contents

- `dist/` — pre-built React frontend (Vite). Configured to hit the public
  Cloud Run URL below.
- `start.sh` — convenience launcher (`python3 -m http.server`).

Backend URL baked into the bundle:

```
https://contract-intelligence-997090888022.us-central1.run.app
```

## Requirements

- Python 3 (macOS/Linux ship with it) **or** any static HTTP server of your
  choice (`npx serve dist`, nginx, IIS, etc.).
- A modern browser (Chrome / Edge / Safari / Firefox).

## Run

```bash
./start.sh          # serves on http://localhost:8080
PORT=3000 ./start.sh   # override port
```

Or, if you prefer not to use the script:

```bash
python3 -m http.server 8080 --directory dist
# then open http://localhost:8080
```

## Using the UI

- The **tenant** pill in the top-right of the header switches which tenant's
  data is queried. Default is `000001` (the seeded demo tenant).
- The tenant id is stored per-browser in `localStorage`. Clear site data to
  reset.
- All API calls carry the `X-Tenant-Id` header automatically; tenant
  isolation is enforced server-side.

## What you can demo

- **Query** — natural-language questions over the contract portfolio
  (SQL / RAG / hybrid routing happens server-side).
- **Contract list / detail** — browse the ingested corpus with clause-level
  drill-downs.
- **Upload & ingest** — drag-drop PDFs; the pipeline extracts clauses,
  embeds them into Pinecone, and stores structured facts in Cloud SQL.
- **Policies** — CRUD compliance policies and evaluate them across the
  portfolio.
- **Graph views** — portfolio and per-contract entity graphs.

## Troubleshooting

- **Blank page / CORS errors in the console** — Make sure you opened
  `http://localhost:8080`, not `file:///…/index.html`. Some browsers block
  `fetch()` on `file://` origins.
- **API calls fail with 403** — The Cloud Run service was locked back
  down. Ask the owning team to re-open `allUsers` invoker on the
  `contract-intelligence` service in `gcp-jai-platform-dev`.
- **Empty lists** — Wrong tenant. Click the tenant pill and set it to
  `000001`.

## Security note

The backend is publicly invokable **for the duration of the client demo
window** to support laptops without GCP credentials. Tenant isolation is
still enforced inside the app via the `X-Tenant-Id` header, but there is
no network-level auth. Lock the service back down (`gcloud run services
remove-iam-policy-binding contract-intelligence --member=allUsers
--role=roles/run.invoker --region=us-central1`) after the demo.
