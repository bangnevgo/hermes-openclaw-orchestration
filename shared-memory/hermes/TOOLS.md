# TOOLS.md - Hermes OpenClaw Orchestration Tools

## Hermes Bridge — Shared Folder Communication

### Sending Commands to OpenClaw Agents
- **Path:** `/home/bangnevgo/AI-Team/shared-memory/hermes/out/`
- **Format:** `command_YYYYMMDD_HHMMSS.md`
- **Example:**
```markdown
FROM:hermes
TO:{agent-id}
TYPE:command
PRIORITY:high/medium/low
---
{task description}
```

### Receiving Reports from OpenClaw Agents
- **Path:** `/home/bangnevgo/AI-Team/shared-memory/hermes/in/`
- **Format:** `laporan_YYYYMMDD_dari_{agent-id}.md`
- **Example:**
```markdown
FROM:{agent-id}
TO:hermes
TYPE:laporan
STATUS:done/failed/in_progress
---
{report content}
```

## OpenClaw Agent Workspaces

| Agent | Workspace Path |
|-------|---------------|
| Stephani | `.openclaw/workspace-stephani-the-social-media-manager` |
| Nancy | `.openclaw/workspace-nancy-lead-manager` |
| Siska | `.openclaw/workspace-siska-finance-advertising-manager` |
| Lena | `.openclaw/workspace-lena-website-manager` |
| SiSuz | `.openclaw/workspace` |

## Agent Communication IDs

| Agent | Communication ID |
|-------|-----------------|
| Stephani | `stephani-the-social-media-manager` |
| Nancy | `nancy-lead-manager` |
| Siska | `siska---finance-advertising-manager` |
| Lena | `lena-website-manager` |
| SiSuz | `main` |

## Shared Memory Structure

```
/home/bangnevgo/AI-Team/shared-memory/
├── hermes/
│   ├── out/              # Hermes → Agent commands
│   ├── in/               # Agent → Hermes reports
│   └── memory/          # Hermes long-term memory
└── openclaw/
    └── {agent-id}/in/   # Per-agent inboxes
```
