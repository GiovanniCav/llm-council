---
name: manifest-sync
description: Sync data with MANIFEST.jsonl. Use before any indexing, writing, or multi-system sync operations to ensure idempotency and data parity.
---

# Manifest Sync Skill

## When to Use
- Before indexing new content into a database
- Before writing files to a content store
- When syncing between local and cloud storage
- When auditing data parity across systems
- User mentions "sync", "manifest", or "data parity"

## The Protocol

> [!IMPORTANT]
> **Manifest-First Sync**: Always update `MANIFEST.jsonl` *before* writing to the target system. This prevents drift and enables recovery.

### Step 1: Read Existing Manifest
```python
import json
from pathlib import Path

manifest_path = Path("data/MANIFEST.jsonl")
existing = {}
if manifest_path.exists():
    for line in manifest_path.read_text().splitlines():
        record = json.loads(line)
        existing[record["id"]] = record
```

### Step 2: Generate SHA256 Hash
```python
import hashlib

def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()
```

### Step 3: Diff Against Existing
```python
new_items = []
changed_items = []
unchanged_items = []

for item in incoming_items:
    item_hash = compute_checksum(item["content"])
    if item["id"] not in existing:
        new_items.append(item)
    elif existing[item["id"]]["checksum"] != item_hash:
        changed_items.append(item)
    else:
        unchanged_items.append(item)
```

### Step 4: Update Manifest FIRST
```python
# Write to manifest before any other operation
for item in new_items + changed_items:
    manifest_record = {
        "id": item["id"],
        "source_uri": item["source_uri"],
        "title": item["title"],
        "checksum": compute_checksum(item["content"]),
        "status": "indexed",
        "metadata": item.get("metadata", {})
    }
    with open(manifest_path, "a") as f:
        f.write(json.dumps(manifest_record) + "\n")
```

### Step 5: Write to Target System
Only after manifest is updated:
```python
for item in new_items + changed_items:
    write_to_target(item)  # Database, Google Drive, etc.
```

### Step 6: Log Activity
```python
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "event_type": "DATA_SYNC",
    "severity": "INFO",
    "instance_id": os.environ.get("INSTANCE_ID", "UNKNOWN"),
    "context": {
        "message": f"Synced {len(new_items)} new, {len(changed_items)} changed, {len(unchanged_items)} skipped",
        "new_ids": [i["id"] for i in new_items],
        "changed_ids": [i["id"] for i in changed_items]
    }
}
with open("logs/activity.jsonl", "a") as f:
    f.write(json.dumps(log_entry) + "\n")
```

## MANIFEST.jsonl Schema

```json
{
  "id": "string (atomic, e.g. 95)",
  "source_uri": "string (url/path)",
  "title": "string (human name)",
  "checksum": "string (sha256)",
  "status": "extracted | indexed | verified | error",
  "metadata": {
    "project_specific_key": "any"
  }
}
```

## Invariants

| Rule | Description |
|------|-------------|
| **SHA256 Idempotency** | Only re-index if checksum changes |
| **Atomic IDs** | Use `id` field as primary key, never title |
| **Manifest-First** | Update manifest before writing to target |
| **Log Everything** | Append to `logs/activity.jsonl` after sync |

## Integration Points
- **Jack's Automations**: Vault database sync
- **Roadmap**: Sales script versioning
- **Project Factory**: Central manifest for all repos
