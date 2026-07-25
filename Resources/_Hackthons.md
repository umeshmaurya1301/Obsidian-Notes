# 🏆 Hackathon Tracker — 2026

> [!note] Migrated
> Live tracking is now per-event notes with a filterable dashboard at [[Events_Dashboard]] (`Tech/Events/`). **This file is the project-mapping reference** — how AEPO/AEGIS map onto tracks, the build roadmap, and the employer-IP ground rules. Refreshed **2026-07-25**.

> **Profile:** Backend Developer · 3.5 years experience · Bengaluru, India · Solo Participant
> **Projects:** AEPO (Autonomous Enterprise Payment Orchestrator) · AEGIS (Counterfactual Shadow Mode Policy Substrate)
> **Last Updated:** July 25, 2026

---

## 🎯 Open Targets — enterable now

> [!info] **Fit** = profile fit + value + feasibility, out of 10 — the same score [[Events_Dashboard]] ranks on (🟢 ≥8 · 🟠 6–7 · 🔴 <6). Table below is ordered by deadline; sort by Fit on the dashboard.

| # | Hackathon | Fit | Project | Prize 💰 | Deadline 📅 | Mode | Notes |
|---|---|---|---|---|---|---|---|
| 1 | [DataHub — The Agent Hackathon](https://datahub.devpost.com/) | 🟠 6 | AEPO | $20,500 | **Aug 10, 2026** | Online | AEPO as metadata-aware MCP data-agent |
| 2 | [Intain FinTech Challenge](https://www.hackerearth.com/challenges/competitive/intain-fintech-hackathon/) | 🟠 6 | — (hiring rep) | recognition/hiring | **Aug 14, 2026** | Online (India) | Timed proctored assessment · verify eligibility |
| 3 | [Build with Gemini XPRIZE](https://xprize.devpost.com/) | 🟠 6 | AEGIS / AEPO | $2,000,000 | **Aug 17, 2026** | Online | Startup-grade — only if genuinely launching |
| 4 | [CockroachDB × AWS — Agentic Memory](https://cockroachdb-ai.devpost.com/) | 🟠 7 ⭐ | AEPO | $8,750 | **Aug 18, 2026** | Online | **Best fit** — memory layer + your SQL depth |
| 5 | [API World — API+Cloud+AI](https://api-cloud-ai-hackathon-2026.devpost.com/) | 🟠 6 | AEGIS | non-cash | **Sep 3, 2026** | Hybrid | Reg opens Aug 17 · AEGIS finale showcase |
| 6 | [GFF Mumbai (PSB / SBI / iDEA)](https://www.globalfintechfest.com/gff-hackathons) | 🟠 6 | AEPO / AEGIS | ₹ pools | **Sep 8, 2026** | In-person | India fintech flagship · Mumbai |
| 7 | [ARC Prize — ARC-AGI-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3) | 🟠 7 | AEPO | $2M+ pool | **Sep 30 → Nov 2** | Online | Milestone #2 Sep 30 · OpenEnv-win domain |

## 🔭 Watch — no fixed window yet

| Hackathon                                                                                                  | Fit            | Project         | Prize              | When                | Notes                                                       |
| ---------------------------------------------------------------------------------------------------------- | -------------- | --------------- | ------------------ | ------------------- | ----------------------------------------------------------- |
| [IIT-Kanpur × Ericsson National Fintech Hackathon](https://www.iitk.ac.in/national-fintech-hackathon-2026) | 🟠 6           | AEPO (payments) | TBD                | 2026 (verify)       | **Payments = Card91/UPI bullseye**; confirm pro eligibility |
| [RBI HaRBInger](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=58059)                                                           | 🟠 7 (→9 live) | AEGIS           | ₹40L/statement     | ~Oct 2026           | Link = 2025 (4th-ed) release; watch rbi.org.in ~Oct for the 5th. See [[RBI_HaRBInger_2026_Watch]]                      |
| [Google Cloud Gen AI Academy — APAC](https://hack2skill.com/event/apac-genaiacademy)                       | 🟠 6           | AEPO            | up to $10K + Grand | Cohort 3 / year-end | Grand Hackathon open to non-cohort entrants                 |
| [IDFC FIRST CodeCraft](https://www.hackerrank.com/event/codecraft-backend-developer-hiring-hackathon-april-2026)                                                        | 🟠 7           | — (hiring)      | job offer          | next edition        | Link = Apr 2026 edition (closed); recurring pipeline. See [[IDFC_FIRST_CodeCraft_Backend]]                  |

---

## 🗓️ Deadline Timeline

```
Aug 10 ───── DataHub Agent Hackathon         🔭 AEPO
Aug 14 ───── Intain FinTech Challenge         🔭 India fintech (hiring rep)
Aug 17 ───── Build with Gemini XPRIZE         🔭 AEGIS/AEPO (launch-grade)
Aug 18 ───── CockroachDB × AWS Agentic Mem    ⭐ AEPO (best fit)
Sep 03 ───── API World (reg opens Aug 17)     🔭 AEGIS
Sep 08 ───── GFF Mumbai (in-person)           🔭 AEPO/AEGIS
Sep 30 ───── ARC Prize Milestone #2           🔭 AEPO
~Oct   ───── RBI HaRBInger 5th ed (watch)     🔭 AEGIS
Nov 02 ───── ARC Prize final                  🔭 AEPO
```

---

## 🚀 Project → Hackathon Mapping

### 🤖 AEPO (Autonomous Enterprise Payment Orchestrator)

> PyTorch RL · Gymnasium 0.29.1 · FastAPI · HuggingFace Spaces · Java Mirror · Meta PyTorch OpenEnv Round 1 Winner

| Hackathon | Track | Why it fits |
|---|---|---|
| CockroachDB × AWS | Agentic memory | Event-sourced memory → CockroachDB persistence + distributed vector indexing |
| DataHub Agent | Metadata-aware / production ML agent | Orchestration/decisioning loop reframed as an MCP data-agent |
| ARC Prize | ARC-AGI-3 interactive agents | Gymnasium/OpenEnv exploration muscle — the OpenEnv Round-1 win domain |
| IIT-K × Ericsson | Digital payments | Routing/decisioning on payment rails (Card91/UPI experience) |
| GFF / RBI | Fintech / fraud | Payment-ops flow + fraud framing |

### 🛡️ AEGIS (Counterfactual Shadow Mode Policy Substrate)

> DR Estimator · Z3 Verification · eBPF · K8s Operator · Sub-5ms decisions · Idea/Build Stage

| Hackathon | Track | Why it fits |
|---|---|---|
| Build with Gemini XPRIZE | Money & Financial Access | Productized AEGIS — policy shadow-testing for payment teams (needs real users/revenue) |
| API World | API + Cloud + AI | Full architecture: eBPF + K8s operator + plugin system (Slice C) |
| GFF PSB / RBI HaRBInger | Cybersecurity / fraud | Baseline security filter chain (velocity, replay, tenant violations) |

---

## 📦 Build Roadmap

| Slice | What to Build | Target Hackathon | Deadline |
|---|---|---|---|
| **Slice A** | AEPO as metadata-aware MCP data-agent | DataHub Agent | Aug 10 |
| **Slice B** ⭐ | AEPO memory/decision loop → CockroachDB + AWS | CockroachDB × AWS | Aug 18 |
| **Slice C** | AEGIS full architecture (eBPF + operator + plugin) | API World | Sep 3 |
| **Slice D** | AEPO exploration/reward scaffolding → ARC env API | ARC Prize (M2) | Sep 30 |

> [!tip] Don't split the fortnight
> Slices A and B are the same AEPO core in two wrappers. Pick **one primary** (Slice B / CockroachDB is the engineering-led, highest-fit play) rather than half-shipping both.

---

## 🏅 Submission History

> [!success] Formal submissions to date
> - **Meta PyTorch OpenEnv Round 1 — AEPO — 🏆 WON.** This is the **only** event AEPO has ever been formally submitted to.
> - **Participated (outcomes pending):** ET AI Hackathon 2.0, DevNetwork AI+ML 2026, MetLife APAC — see per-event notes in `Tech/Events/`.

> [!warning] Registered ≠ submitted
> Prior "registered" entries (Sui Overflow, DeveloperWeek NY, Google Cloud Rapid Agent, FIND EVIL!, API World, Qwen, etc.) were **registered/planned only, not submitted** — and those editions have now closed. When a new contest's rules say "significantly updated since submission-period start," the baseline is the **Meta PyTorch** submission, not any of these.

---

## ⚠️ Ground Rules

- [ ] 100% personal devices, personal time, personal internet
- [ ] No company name on submissions — registered as `Independent`
- [ ] All commits on personal GitHub with personal email
- [ ] No fintech-specific language on public submissions (AEPO/AEGIS framed as domain-agnostic)
- [ ] Read employment contract before each submission
- [ ] Document all work with timestamps showing after-hours activity

---

## 🔗 Quick Links

| Resource | Link |
|---|---|
| Devpost Profile | https://devpost.com |
| AEPO — HuggingFace | _(add your HF Spaces link)_ |
| AEPO — GitHub | _(add your personal GitHub repo)_ |
| AEGIS — GitHub | _(add your personal GitHub repo)_ |
| GFF Hackathons | https://www.globalfintechfest.com/gff-hackathons |
| RBI HaRBInger (2025 release) | https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=58059 |
| IIT-K × Ericsson Fintech | https://www.iitk.ac.in/national-fintech-hackathon-2026 |

---

_Refreshed: July 25, 2026 · Live status lives in [[Events_Dashboard]] — update this file only when project→track mapping changes._
