# Obsidian Notes Vault

A personal knowledge base maintained in [Obsidian](https://obsidian.md/) by Umesh Maurya — primarily backend-engineering study notes and a structured DSA / MAANG interview-prep system.

## What's inside

| Folder | Purpose |
|---|---|
| `Tech/` | Core technical notes — the bulk of the vault |
| `Finance/` | Finance topics (currently Blockchain & Crypto) |
| `Productivity/` | Learning backlog and productivity notes |
| `Quick/` | Scratch / quick-reference notes and roadmaps |
| `Resources/` | Curated external resources (tech links, hackathons) |
| `Templates/` | Obsidian note templates (Templater) |

### `Tech/` breakdown

| Sub-folder | Topic |
|---|---|
| `DSA/` | Data Structures & Algorithms — interview prep (see below) |
| `Java/` | Java internals |
| `Python/` | Python internals + Python-vs-Java comparison |
| `Concurrency/` | Java concurrency and threading |
| `Kafka/` | Apache Kafka — intro, producer, consumer, enhancements |
| `JUNIT 5 and Mockito/` | Unit testing with JUnit 5 & Mockito |
| `Dev Ops/` | Kubernetes and related topics |
| `AEPO/` | Learning docs for the Autonomous Enterprise Payment Orchestrator hackathon project — RL fundamentals, architecture, source walkthrough, training/inference pipelines, deployment, interview prep |
| `Dashboard.md` | Top-level index of tech learning areas |

## The DSA system

`Tech/DSA/` is the most actively maintained area. It is built around three moving parts:

- **`Roadmap.md`** — a 16-week / 4-month MAANG prep plan (~400 problems). Problems are checkbox tasks (`- [ ]` / `- [x]`) grouped by week and pattern, each linking to LeetCode/GFG. Solved items are tagged with a completion date.
- **`Questions/`** — one note per solved problem, named `LT_<id>_<Title>.md`. Each captures the problem, intuition, and the evolution of solutions with code.
- **`DSA_Dashboard.md`** — a `dataviewjs` dashboard that auto-tables every note in `Questions/` by difficulty, status, tags, and review date.

New question notes are created from `Templates/DsaTemplates/DSA_Question_Template.md`, which uses Templater to prompt for difficulty, status, and URL, then writes YAML frontmatter (`created`, `tags`, `source`, `problem_id`, `difficulty`, `status`, `review_date`).

## Conventions

- **Numbered notes** — sequential topics use a `N. Title.md` prefix (e.g. `1. Kafka Intro.md`) to enforce reading order.
- **Roadmap files** — most learning areas have a `Roadmap.md` listing what to study.
- **Dashboards** — index notes (`*Dashboard.md`) use the Dataview plugin and must be viewed inside Obsidian to render.
- **Callouts** — notes use Obsidian callouts (`> [!info]`, `> [!example]`, `> [!warning]`) heavily.
- **Wiki-links & emoji headings** — internal links and emoji-prefixed headings are used throughout.

## Plugins in use

Calendar, Dataview, Excalidraw, Obsidian Git, Tasks, Sortable Tables, Table Editor, Templater.

## Notes

- The vault is git-backed; the Obsidian Git plugin makes periodic `vault backup` commits.
- `.obsidian/` (workspace/cache) is git-ignored, though some plugin/theme files were committed before the ignore rule.
- For full functionality (dashboards, task tracking, templates) open the folder as a vault in Obsidian rather than reading the Markdown raw.
