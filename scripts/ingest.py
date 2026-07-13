#!/usr/bin/env python3
import sys, json, subprocess, os

BASE = "https://contract-intelligence-997090888022.us-central1.run.app/api/v1"
TENANT = "000001"

def extract(path):
    # multipart upload, SSE response; capture full body
    out = subprocess.run(
        ["curl", "-sS", "-N", "-X", "POST",
         "-H", f"X-Tenant-Id: {TENANT}",
         "-F", f"file=@{path}",
         f"{BASE}/ingest/extract"],
        capture_output=True, text=True, timeout=1200)
    if out.returncode != 0:
        raise RuntimeError(f"extract curl failed: {out.stderr}")
    result = None
    last_progress = None
    for line in out.stdout.splitlines():
        if not line.startswith("data: "):
            continue
        try:
            m = json.loads(line[6:])
        except json.JSONDecodeError:
            continue
        t = m.get("type")
        if t == "progress":
            last_progress = m.get("stage") + ":" + str(m.get("status"))
        elif t == "result":
            result = m.get("data")
        elif t == "error":
            raise RuntimeError("extraction error: " + str(m.get("detail")))
    if result is None:
        raise RuntimeError(f"no result. last progress={last_progress}. raw tail:\n{out.stdout[-500:]}")
    return result

def store(data):
    payload = {
        "file_path": data.get("file_path"),
        "content_hash": data.get("content_hash"),
        "metadata": data.get("metadata"),
        "clauses": data.get("clauses"),
        "obligations": data.get("obligations") or [],
        "contract_summary": data.get("contract_summary"),
    }
    out = subprocess.run(
        ["curl", "-sS", "-X", "POST",
         "-H", f"X-Tenant-Id: {TENANT}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload),
         f"{BASE}/ingest/store"],
        capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        raise RuntimeError(f"store curl failed: {out.stderr}")
    return out.stdout

def main():
    path = sys.argv[1]
    name = os.path.basename(path)
    print(f">>> extracting {name} ...", flush=True)
    data = extract(path)
    if data.get("status") == "duplicate":
        print(f"    SKIP (already ingested): {data.get('contract_name')!r}", flush=True)
        print("DONE(dup)", name, flush=True)
        return
    md = data.get("metadata") or {}
    print(f"    extracted: title={md.get('title')!r} type={md.get('contract_type')!r} "
          f"clauses={len(data.get('clauses') or [])} obligations={len(data.get('obligations') or [])}", flush=True)
    print(f">>> storing {name} ...", flush=True)
    res = store(data)
    print(f"    store response: {res[:400]}", flush=True)
    print("DONE", name, flush=True)

if __name__ == "__main__":
    main()
