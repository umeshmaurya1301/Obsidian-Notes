---
cssclasses:
  - ufocus-dash
tags:
  - dashboard
---
# 💻 Tech Hub

> [!info] What's here
> The index for all technical study. **Active Areas** are the topics with notes today; the **Learning Roadmap** below is the full curriculum (everything still planned). The auto-list pulls every note in `Tech/` so nothing gets lost. ⟵ back to [[Home]].

---

## 📚 Active Areas

- **[[Tech/DSA/DSA_Dashboard|🧮 DSA]]** — solved problems, patterns & review queue
- **[[Tech/Java/1. Java Program Life Cycle|☕ Java]]** — language & JVM internals
- **[[Tech/Python/1. Python Program Life Cycle|🐍 Python]]** — internals & Python-vs-Java
- **[[Tech/Concurrency/1. Core Fundamentals|🧵 Concurrency]]** — threads, sync & the JMM
- **[[Tech/Kafka/1. Kafka Intro|🟧 Kafka]]** — producer, consumer & DLQ enhancements
- **[[Tech/JUNIT 5 and Mockito/1. Introduction|🧪 Testing]]** — JUnit 5 & Mockito
- **[[Tech/AWS/01. Intro to AWS & Cloud Computing|☁️ AWS]]** — cloud fundamentals
- **[[Tech/Events/Events_Dashboard|🎯 Events]]** — hackathons & challenges

---

## 🗂️ All Tech Notes

```dataview
LIST rows.file.link
FROM "Tech"
WHERE !contains(file.name, "Dashboard") AND !contains(file.name, "Roadmap")
GROUP BY file.folder AS "📁 Folder"
SORT file.folder ASC
```

---

## 🧭 Learning Roadmap

> [!example]- The full curriculum (tick as you build out each area)
> - [x] **1. Java** — [[Tech/Java/1. Java Program Life Cycle|notes started]] ✅
> - [ ] **2. Spring Boot**
> - [ ] **3. Microservices**
> - [ ] **4. Database Management System**
>     - [ ] Relational Database
>     - [ ] Non-Relational Database
> - [ ] **5. Low Level Design**
> - [ ] **6. High Level Design**
> - [ ] **7. Generative AI**
>     - [ ] Basics & Terminology
>     - [ ] Hugging Face
>     - [ ] LangChain
> - [ ] **8. LINUX**
> - [ ] **9. Git and GitHub**
> - [ ] **10. Docker**
> - [ ] **11. Kubernetes**
> - [x] **12. AWS** — [[Tech/AWS/01. Intro to AWS & Cloud Computing|notes started]] ✅

---

> [!tip] Add a new area
> Create the folder + first note under `Tech/`, then add a card to **Active Areas** above and tick it off in the roadmap. The **All Tech Notes** list picks it up automatically.
