# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A personal **Obsidian vault** — Markdown study notes, not a software project. There is no build, no tests, no dependencies to install. "Code" in this vault is illustrative snippets inside notes, not a compiled program. See `README.md` for the folder map.

## Owner context

Umesh Maurya — backend engineer (~3.5 yrs, Java/Python), preparing for MAANG SDE-2 interviews. Notes are written for his own revision, so keep them concise, accurate, and interview-relevant.

## Working rules

- **Edit Markdown directly.** Preserve the existing voice, emoji-prefixed headings, and Obsidian callout style (`> [!info]`, `> [!example]`, `> [!warning]`).
- **Don't render or "fix" Dataview / dataviewjs / Templater blocks.** Files like `DSA_Dashboard.md` and the template contain code that only executes inside Obsidian. Leave the syntax intact.
- **Respect frontmatter.** Question notes carry YAML frontmatter (`created`, `tags`, `source`, `problem_id`, `difficulty`, `status`, `review_date`). Keep keys and formats consistent when editing or creating notes.
- **Numbered-note ordering.** When adding a sequential topic note, follow the `N. Title.md` convention and pick the next number.
- **Don't auto-commit.** The Obsidian Git plugin handles `vault backup` commits. Only commit when explicitly asked; branch off `main` if so.
- **`.obsidian/` is config/cache.** Don't modify plugin, theme, or workspace files unless asked.

## DSA conventions (the most active area)

When adding a solved-problem note under `Tech/DSA/Questions/`:

- **File name:** `LT_<id>_<Problem_Title>.md` (LeetCode). Mirror the existing naming.
- **Structure** (see `LT_2401_Longest_Nice_SubArray.md` as the reference): Link → Problem Description → Examples → Constraints → Intuition → Evolution of Solutions (code in fenced blocks, usually Java; Python practiced alongside).
- **Template:** new notes are normally generated from `Templates/DsaTemplates/DSA_Question_Template.md` via Templater.
- **Roadmap sync:** `Tech/DSA/Roadmap.md` tracks problems as checkboxes. When a problem is solved, mark `- [x]`, append `✅ <YYYY-MM-DD>`, and update the Progress Tracker table counts if asked.
- Difficulty/status vocabularies: difficulty = Easy/Medium/Hard; status = To Do / In Progress / Solved / Review Needed.

## Environment

- Windows 11, PowerShell. Use `$null`, `$env:VAR`, backtick line continuation in shell commands.
- Vault root: `C:\Users\Umesh Maurya\Notes\Obsidian-Notes`.
