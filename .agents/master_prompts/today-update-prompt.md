# Today's Update Generator

Paste this file into your AI chat to automatically generate a "Today's Update" post.

---

## Instructions for AI

Generate a **brief, plain-English "Today's Update"** post based on the git changes made today across the two repositories below.

### Tone & Style
- Short bullet points — no jargon unless necessary
- Top-level bullets = broad area of work
- Sub-bullets only if a point genuinely needs a short clarification (max 1 level deep)
- No code formatting (no backticks, no function names) unless it's a proper noun
- Max ~6 top-level bullets total
- Write as if the developer is giving a quick team standup update

### Example Output Format

**Today's update:**

- Fixed a double-tap race condition in the battle game — rapid taps could both pass the answer lock before React state updated, solved with a synchronous ref
- Fixed winner detection — was checking if winner was truthy instead of comparing the winner ID against the current user's ID
- Backend: replaced per-battle N+1 question queries with a single batched query per test type, chunked at 500 IDs

---

## Step 1 — Run these commands and paste the output below

### Main app repo (`brain-battle`)
```bash
cd /home/keni/Documents/CODING_PROJECTS/WORK/brain-battle/brain-battle

# Commits made today
git --no-pager log --since="midnight" --format="%s%n%b" --all

# Files changed today (unstaged + staged)
git --no-pager diff HEAD --stat
git --no-pager diff --cached --stat
```

### Backend repo (`battle-backend`)
```bash
cd /home/keni/Documents/CODING_PROJECTS/WORK/brain-battle/brain-battle/battle-backend

# Commits made today
git --no-pager log --since="midnight" --format="%s%n%b" --all

# Files changed today (unstaged + staged)
git --no-pager diff HEAD --stat
git --no-pager diff --cached --stat
```

---

## Step 2 — Paste command output here

> Replace this block with the output from the commands above, then send to AI.

```
[PASTE OUTPUT HERE]
```

---

## Step 3 — AI generates the update

Once output is pasted, the AI will produce the "Today's Update" post ready to copy into Slack/Discord.
