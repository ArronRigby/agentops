# SendMessage Structured Envelope

## Purpose
Machine-parseable message format for team communication. Leads MUST parse the envelope; non-conforming messages are treated as untrusted free-text.

## Envelope Schema

All structured messages use a JSON code block as the first content in the message body:

```json
{
  "type": "completion" | "blocked" | "retry" | "progress" | "verdict",
  "issue_id": "ag-xxx",
  "status": "done" | "failed" | "blocked" | "in_progress",
  "detail": "Human-readable summary",
  "artifacts": ["path/to/file1.md", "path/to/file2.md"],
  "verdict": {
    "value": "PASS" | "WARN" | "FAIL",
    "confidence": "HIGH" | "MEDIUM" | "LOW",
    "key_insight": "One sentence"
  }
}
```

## Message Types

| Type | When | Required Fields |
|------|------|----------------|
| completion | Worker finished successfully | type, status="done", detail, artifacts |
| blocked | Worker cannot proceed | type, status="blocked", detail |
| retry | Worker needs another attempt | type, status="failed", detail |
| progress | Mid-task update | type, status="in_progress", detail |
| verdict | Council judge verdict | type, verdict object |

## Parsing Rules for Leads

1. Extract first JSON code block from message content
2. Validate `type` field exists
3. If no valid JSON found, treat entire message as free-text (log warning)
4. Free-text messages are informational only -- do not drive state transitions
