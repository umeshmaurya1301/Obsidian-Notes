---
created: 2026-06-09
tags:
  - dashboard
  - events
---
# 🎯 Tech Events & Hackathons Dashboard

> [!info] How this works
> One note per event lives in this folder (`Tech/Events/`), each with a `status`, `rating` (fit out of 10), and `fit` rationale in its frontmatter. This dashboard reads them live.
> **Status flow:** `TO_DO` → `REGISTERED` → `SUBMITTED` → `WON` / `REJECTED` / `MISSED` / `EXPIRED`
> **Rating** = composite of profile fit + prize/value + feasibility (open? solo-friendly? eligible?).
> The **Focus** view shows your actionable events (`REGISTERED` + `TO_DO`); the **Ranked** view sorts everything by fit; **All by status** groups everything.

---

## 🏆 Ranked by Fit (should I do it?)

```dataviewjs
const icon = {TO_DO:"🔭",REGISTERED:"🟡",SUBMITTED:"✅",WON:"🏆",REJECTED:"❌",MISSED:"⌛",EXPIRED:"⏰"};
const star = r => (r >= 8 ? "🟢" : r >= 6 ? "🟠" : "🔴");

let pages = dv.pages('"Tech/Events"')
  .where(p => p.type == "event" && p.file.name != "_Event_Template")
  .array()
  .sort((a,b) => (b.rating || 0) - (a.rating || 0));

dv.table(
  ["Rating","Event","Status","Deadline","Prize 💰","Why (fit)"],
  pages.map(p => [
    `${star(p.rating || 0)} ${p.rating ?? "—"}/10`,
    p.file.link,
    `${icon[p.status] || ""} ${p.status}`,
    p.deadline ? p.deadline : "TBD",
    p.prize || "—",
    p.fit || ""
  ])
);
```

---

## ⭐ Focus — Active Events

```dataviewjs
// Statuses shown in this focus view (edit to taste):
const FOCUS = ["REGISTERED", "TO_DO"];

const icon = {TO_DO:"🔭",REGISTERED:"🟡",SUBMITTED:"✅",WON:"🏆",REJECTED:"❌",MISSED:"⌛",EXPIRED:"⏰"};
const today = dv.date("today");

let pages = dv.pages('"Tech/Events"')
  .where(p => p.type == "event" && p.file.name != "_Event_Template" && FOCUS.includes(p.status))
  .array()
  .sort((a,b) => {
    const da = a.deadline ? dv.date(a.deadline) : null;
    const db = b.deadline ? dv.date(b.deadline) : null;
    if (!da && !db) return 0;
    if (!da) return 1;
    if (!db) return -1;
    return da - db;
  });

const rows = pages.map((p, i) => {
  const dl = p.deadline ? dv.date(p.deadline) : null;
  let daysLeft = "—";
  if (dl) {
    const d = Math.ceil(dl.diff(today, "days").days);
    daysLeft = d < 0 ? "⛔ closed" : (d <= 5 ? `🔴 ${d}d` : (d <= 14 ? `🟠 ${d}d` : `🟢 ${d}d`));
  }
  return [
    `${p.rating ?? "—"}/10`,
    p.file.link,
    p.deadline ? p.deadline : "TBD",
    daysLeft,
    p.phase || "—",
    p.prize || "—",
    p.mode || "—",
    p.applied ? "✅" : "❌",
    `${icon[p.status] || ""} ${p.status}`
  ];
});

dv.header(3, `Showing ${FOCUS.join(" + ")} — ${rows.length} event(s)`);
dv.table(
  ["Rating","Event","Deadline","Days Left","Phase","Prize 💰","Mode","Applied","Status"],
  rows
);
```

---

## 📊 Status Overview

```dataviewjs
const order = ["TO_DO","REGISTERED","SUBMITTED","WON","REJECTED","MISSED","EXPIRED"];
const icon = {TO_DO:"🔭",REGISTERED:"🟡",SUBMITTED:"✅",WON:"🏆",REJECTED:"❌",MISSED:"⌛",EXPIRED:"⏰"};

const pages = dv.pages('"Tech/Events"').where(p => p.type == "event" && p.file.name != "_Event_Template");
const counts = {}; for (const s of order) counts[s] = 0;
for (const p of pages) counts[p.status] = (counts[p.status] || 0) + 1;

dv.table(["Status","Count"],
  order.filter(s => counts[s] > 0).map(s => [`${icon[s]} ${s}`, counts[s]]));
dv.paragraph(`**Total tracked:** ${pages.length}`);
```

---

## 📂 All Events — grouped by status

```dataviewjs
const order = ["REGISTERED","TO_DO","SUBMITTED","WON","REJECTED","MISSED","EXPIRED"];
const icon = {TO_DO:"🔭",REGISTERED:"🟡",SUBMITTED:"✅",WON:"🏆",REJECTED:"❌",MISSED:"⌛",EXPIRED:"⏰"};
const today = dv.date("today");

const all = dv.pages('"Tech/Events"').where(p => p.type == "event" && p.file.name != "_Event_Template");

for (const status of order) {
  let pages = all.where(p => p.status == status)
    .array()
    .sort((a,b) => {
      const da = a.deadline ? dv.date(a.deadline) : null;
      const db = b.deadline ? dv.date(b.deadline) : null;
      if (!da && !db) return 0;
      if (!da) return 1;
      if (!db) return -1;
      return da - db;
    });
  if (pages.length === 0) continue;

  dv.header(3, `${icon[status]} ${status} (${pages.length})`);
  dv.table(
    ["Event","Deadline","Phase","Prize 💰","Mode","Applied"],
    pages.map(p => {
      let dl = p.deadline ? `${p.deadline}` : "TBD";
      if (p.deadline) {
        const d = Math.ceil(dv.date(p.deadline).diff(today,"days").days);
        if (d >= 0 && d <= 14) dl = `🔴 ${p.deadline} (${d}d)`;
        else if (d < 0) dl = `${p.deadline} (closed)`;
      }
      return [p.file.link, dl, p.phase || "—", p.prize || "—", p.mode || "—", p.applied ? "✅" : "❌"];
    })
  );
}
```

---

> [!tip] Add a new event
> Copy `_Event_Template.md`, rename it, fill the frontmatter (set `status:` to one of `TO_DO / REGISTERED / SUBMITTED / WON / REJECTED / MISSED`). It appears here automatically.
