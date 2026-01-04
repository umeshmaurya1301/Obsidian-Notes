<%*
// Prompt for Difficulty with a dropdown
const difficulty = await tp.system.suggester(
    ["Easy", "Medium", "Hard"],
    ["Easy", "Medium", "Hard"]
);

// Prompt for the Status
const status = await tp.system.suggester(
    ["To Do", "In Progress", "Solved", "Review Needed"],
    ["To Do", "In Progress", "Solved", "Review Needed"]
);

// Prompt for the URL (optional, can press Esc to skip)
const url = await tp.system.prompt("Problem URL");
_%>
---
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
tags: [dsa]
source: 
problem_id: 
difficulty: <% difficulty %>
status: <% status %>
review_date: 
---

# <% tp.file.title %>

**Link:** [Open Problem](<% url %>)

## 📝 Problem Description
> [!info] Description
> Paste the problem description here.

> [!example] Test Cases
> **Input:** > **Output:** > [!warning] Constraints
> - Constraint 1
> - Constraint 2

---

## 💡 Solutions

### Approach 1: (Name, e.g., Brute Force)
*Intuition:* ```java
// Code here