---
name: mtg
description: Use this skill when the user invokes "/mtg" or shares meeting transcription (文字起こし) and/or an Outlook screenshot to generate a post-meeting summary. Trigger immediately — no pre-meeting prep, just extract and summarize.
---

# MTG Summary

Generate a post-meeting summary from transcription text and/or an Outlook screenshot.

## Input

Accept any of:
- Transcription text (文字起こし) — pasted inline or as a file; Japanese or English
- Outlook calendar screenshot — to extract date, time, and participants

No clarifying questions. Extract everything from what's provided. If something is missing, infer or omit.

## Output

Output immediately. No preamble. Output language matches the transcription language — Japanese if the meeting was in Japanese, English if in English.

Title format: `YYYYMMDD_TITLE` (date from meeting, title inferred from topic)

```
# YYYYMMDD_TITLE

- Date: ...
- Participants: ...

### Decisions
- ...

### Action Items
| Action | Owner | Due |
|--------|-------|-----|

### Key Points
- ...
```

Rules:
- From Outlook screenshot: extract date, time, participants
- Action item owners are required; write TBD if unknown
- Omit Due column if no deadlines mentioned
- Omit any section with no content
- No filler. No padding.
