---
cssclasses:
  - ufocus-dash
created: 2026-06-13
tags:
  - dashboard
---
# 🏠 Home

> [!info] Command center
> Your jumping-off point for the whole vault. The stats and lists below update themselves — solve a problem, edit a note, or add an event and it shows up here. Set this note as your startup page with the **Homepage** plugin (see [[Vault Setup Guide]]).

---

## 🚀 Quick Launch

- **[[Tech/DSA/DSA_Dashboard|🧮 DSA Lab]]** — solved problems, patterns & the review queue
- **[[Tech/Dashboard|💻 Tech Hub]]** — Java, Python, Kafka, Concurrency, Testing, AWS…
- **[[Tech/Events/Events_Dashboard|🎯 Events & Hackathons]]** — ranked by fit & deadline
- **[[Finance/Crypto & Web3/_Dashboard|🪙 Crypto & Web3]]** — learning the space from scratch
- **[[Finance/Investing Basics/_Dashboard|📈 Investing Basics]]** — investing fundamentals
- **[[Productivity/To Learn|🧠 To Learn]]** — the learning backlog
- **[[Resources/Tech Resources|🔗 Resources]]** — curated external links
- **[[Vault Map.canvas|🗺️ Vault Map]]** — a visual map of the whole vault

---

## 📈 DSA at a Glance

```dataviewjs
const qs = dv.pages('"Tech/DSA/Questions"').where(p => p.file.name != "DSA_Dashboard");
const norm = s => (s ?? "").toString().toLowerCase();
const total  = qs.length;
const solved = qs.where(p => norm(p.status).includes("solved")).length;
const diff   = d => qs.where(p => norm(p.difficulty) === d).length;
const easy = diff("easy"), med = diff("medium"), hard = diff("hard");

const today    = dv.date("today");
const weekAgo  = today.minus(dv.duration("7 days"));
const thisWeek = qs.where(p => p.file.ctime && p.file.ctime >= weekAgo).length;
const reviewDue = qs.where(p => p.review_date && dv.date(p.review_date) <= today).length;

const pct = total ? Math.round((solved / total) * 100) : 0;

const el = dv.el("div", "");
el.innerHTML = `
  <span class="ufocus-stat"><b>${total}</b><small>Tracked</small></span>
  <span class="ufocus-stat"><b>${solved}</b><small>Solved</small></span>
  <span class="ufocus-stat"><b>${easy}</b><small>Easy</small></span>
  <span class="ufocus-stat"><b>${med}</b><small>Medium</small></span>
  <span class="ufocus-stat"><b>${hard}</b><small>Hard</small></span>
  <span class="ufocus-stat"><b>${thisWeek}</b><small>New · 7d</small></span>
  <span class="ufocus-stat"><b>${reviewDue}</b><small>Review due</small></span>
  <div class="ufocus-bar" title="${solved} of ${total} solved"><span style="width:${pct}%"></span></div>
  <small style="color:var(--text-muted)">${pct}% of tracked problems solved</small>`;
```

---

## 🕓 Continue Where You Left Off

```dataview
TABLE WITHOUT ID file.link AS "📄 Note", dateformat(file.mtime, "MMM dd · HH:mm") AS "Last edited"
WHERE !contains(file.folder, "Templates")
  AND !contains(file.name, "Dashboard")
  AND !contains(list("Home", "CLAUDE", "README", "DSS"), file.name)
SORT file.mtime DESC
LIMIT 8
```

---

## 🎯 Active Events

```dataviewjs
const FOCUS = ["REGISTERED", "TO_DO"];
const icon = {TO_DO:"🔭",REGISTERED:"🟡",SUBMITTED:"✅",WON:"🏆",REJECTED:"❌",MISSED:"⌛"};
const today = dv.date("today");

let ev = dv.pages('"Tech/Events"')
  .where(p => p.type === "event" && p.file.name !== "_Event_Template" && FOCUS.includes(p.status))
  .array()
  .sort((a, b) => {
    const da = a.deadline ? dv.date(a.deadline) : null;
    const db = b.deadline ? dv.date(b.deadline) : null;
    if (!da && !db) return 0;
    if (!da) return 1;
    if (!db) return -1;
    return da - db;
  })
  .slice(0, 6);

if (ev.length === 0) {
  dv.paragraph("_Nothing active right now — open the [[Tech/Events/Events_Dashboard|Events dashboard]] to scout more._");
} else {
  dv.table(["Event", "Deadline", "Days left", "Status"], ev.map(p => {
    const dl = p.deadline ? dv.date(p.deadline) : null;
    let days = "—";
    if (dl) {
      const d = Math.ceil(dl.diff(today, "days").days);
      days = d < 0 ? "⛔ closed" : (d <= 5 ? `🔴 ${d}d` : (d <= 14 ? `🟠 ${d}d` : `🟢 ${d}d`));
    }
    return [p.file.link, p.deadline || "TBD", days, `${icon[p.status] || ""} ${p.status}`];
  }));
}
```

---

## 🗺️ Roadmaps

- 🧮 [[Tech/DSA/Roadmap|DSA Roadmap]] · [[Tech/DSA/Revision|Revision Queue]]
- 🐍 [[Tech/Python/Roadmap|Python Roadmap]]
- 🧵 [[Tech/Concurrency/Roadmap|Concurrency Roadmap]]
- 🤖 [[Quick/Gen AI Roadmap|Gen AI Roadmap]]

---

> [!tip] Make this your front door
> Install the **Homepage** plugin and point it at `Home` so this opens every time you launch Obsidian. Full instructions in [[Vault Setup Guide]].
