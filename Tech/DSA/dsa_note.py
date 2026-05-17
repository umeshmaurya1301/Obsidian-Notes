import ollama
import re
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

INPUT_DIR     = Path(r"C:\Users\Umesh Maurya\Notes\Obsidian-Notes\Tech\DSA")
RAW_TEXT_FILE = INPUT_DIR / "raw_text.txt"
OUTPUT_DIR    = Path(r"C:\Users\Umesh Maurya\Notes\Obsidian-Notes\Tech\DSA\Questions")
MODEL_NAME    = "qwen2.5-coder:32b"


# ─────────────────────────────────────────────
# PARSE FIRST LINE → filename parts
# ─────────────────────────────────────────────

def parse_first_line(first_line):
    stem = first_line.strip()
    match = re.match(r"^(LT_\d+)_(.+)$", stem)
    if not match:
        raise ValueError(
            f"First line does not match pattern 'LT_XXXX_TITLE'.\n"
            f"Got: '{stem}'\n"
            f"Example: LT_0043_MULTIPLY_STRINGS"
        )
    code_prefix = match.group(1)                        # LT_0043
    raw_title   = match.group(2)                        # MULTIPLY_STRINGS
    title       = raw_title.replace("_", " ").title()   # Multiply Strings
    title_slug  = raw_title.title()                     # Multiply_Strings
    output_name = f"{code_prefix}_{title_slug}.md"      # LT_0043_Multiply_Strings.md
    return code_prefix, title, output_name


# ─────────────────────────────────────────────
# PARSE METADATA FOR LOGGING
# ─────────────────────────────────────────────

def parse_metadata(content):
    meta = {}
    for key, pattern in {
        "id":         r"^ID:\s*(.+)$",
        "difficulty": r"^Difficulty:\s*(.+)$",
        "tags":       r"^Tags:\s*(.+)$",
        "source":     r"^Source:\s*(.+)$",
    }.items():
        m = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        meta[key] = m.group(1).strip() if m else "Not found"
    return meta


# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are a precise Obsidian note formatter for DSA problems.

Convert plain-text DSA notes into Obsidian Markdown. Output ONLY raw markdown — no preamble, no wrapping code fence.

INPUT has metadata fields (FILE, ID, Difficulty, Tags, Source) followed by sections:
Problem Description, Examples, Constraints, Intuition, Approach, Dry Run, Edge Cases, Complexity, Java Code, Key Insights, Patterns, Pitfalls

RULES:
1. Never add or remove information.
2. Tags → YAML list. Split commas.
3. problem_id → no leading zeros, quoted string like "43".
4. status → always "Completed". review_date → always blank.
5. Script prepends "created" and opening "---". Do NOT output those. Start from "tags:" field.
6. CRITICAL: You MUST output a closing "---" after the review_date line to close the frontmatter block.
7. Java code → wrap in ```java fences. Copy indentation EXACTLY.
8. Use Obsidian callouts: > [!info], > [!example], > [!warning].
9. Wrap ALL inline code in backticks: variable names, array accesses, complexity expressions, string values.
10. Each section separated by --- horizontal rule.
11. Missing sections → write: _Not provided._

OUTPUT FORMAT:

tags:
  - Tag1
  - Tag2
source: {URL}
problem_id: "{id}"
difficulty: {Easy|Medium|Hard}
status: Completed
review_date:
---
# {CODE_PREFIX} – {Title}

**Link:** [Open Problem]({URL})

---

## 📝 Problem Description
> [!info]
> {text}

---

## 🧪 Examples
> [!example]
> **Input:** {input}
> **Output:** {output}
> **Explanation:** {explanation}

---

## ⚠️ Constraints
> [!warning]
> - {constraint}

---

## 🔍 Intuition
{text}

---

## 🧠 Approach
{text}

---

## 🧪 Dry Run
> [!example]
> {all steps preserved exactly}

---

## 🔑 Key Insights
- {insight}

---

## 🔮 Patterns
- {pattern}

---

## 🧩 Edge Cases
- {edge case}

---

## ⚠️ Pitfalls
> [!warning]
> - {pitfall}

---

## ⏱️ Complexity
- **Time:** `{time}`
- **Space:** `{space}`

---

## ✅ Java Implementation
```java
{code}
```
"""


# ─────────────────────────────────────────────
# USER PROMPT
# ─────────────────────────────────────────────

def build_user_prompt(code_prefix, title, raw_content):
    return f"""Convert this plain-text DSA note into Obsidian markdown format.

CODE_PREFIX: {code_prefix}
TITLE: {title}

RAW CONTENT:
{raw_content}

CRITICAL REMINDERS:
- Start output from "tags:" field. Script prepends "---" and "created:".
- You MUST output "---" after "review_date:" to close frontmatter.
- End output after closing ``` of Java Implementation.
- Do NOT wrap entire output in a code fence.
- Preserve all Dry Run details exactly.
- Copy Java code exactly — every space, every newline.
- Add backticks around all inline code references.
- problem_id must be a quoted string with no leading zeros.
"""


# ─────────────────────────────────────────────
# CALL QWEN VIA OLLAMA
# ─────────────────────────────────────────────

def call_qwen(system_prompt, user_prompt):
    print(f"  ⏳ Sending to {MODEL_NAME} via Ollama ...")
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        options={
            "temperature": 0.1,
            "num_predict": 6000,
        }
    )
    return response["message"]["content"]


# ─────────────────────────────────────────────
# POST-PROCESSING FIXES
# These run on Qwen's output to guarantee
# correctness regardless of what Qwen produces
# ─────────────────────────────────────────────

def fix_frontmatter(markdown):
    """
    Ensure frontmatter has proper closing ---.
    Scans line by line. Once we're past the opening ---,
    if we hit a # heading or a blank line followed by # heading
    without seeing a closing ---, we insert one.
    """
    lines = markdown.split("\n")
    result = []
    found_opening = False
    found_closing = False

    for i, line in enumerate(lines):
        # Detect opening ---
        if not found_opening and line.strip() == "---":
            found_opening = True
            result.append(line)
            continue

        # Inside frontmatter, look for closing ---
        if found_opening and not found_closing:
            if line.strip() == "---":
                found_closing = True
                result.append(line)
                continue

            # If we hit a markdown heading, frontmatter wasn't closed
            if line.startswith("#"):
                result.append("---")
                found_closing = True
                result.append(line)
                continue

            # If we hit a blank line, peek ahead for a heading
            if line.strip() == "":
                # Look ahead to see if next non-blank line is a heading
                next_content = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        next_content = lines[j]
                        break
                if next_content.startswith("#"):
                    # Blank line before heading = end of frontmatter
                    result.append("---")
                    found_closing = True
                    result.append(line)
                    continue

            result.append(line)
        else:
            result.append(line)

    return "\n".join(result)


def fix_problem_id(markdown):
    """Ensure problem_id is always a quoted string."""
    return re.sub(
        r'problem_id:\s*"?(\d+)"?',
        lambda m: f'problem_id: "{m.group(1)}"',
        markdown
    )


def fix_java_indentation(markdown):
    """
    Re-indent Java code block using brace counting.
    Guarantees proper 4-space indentation regardless of Qwen output.
    """
    java_match = re.search(r"```java\n(.*?)\n```", markdown, re.DOTALL)
    if not java_match:
        return markdown

    code = java_match.group(1)
    lines = code.split("\n")
    fixed = []
    indent = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            fixed.append("")
            continue

        # Decrease indent for closing braces
        if stripped.startswith("}"):
            indent = max(0, indent - 1)

        fixed.append("    " * indent + stripped)

        # Increase indent for opening braces
        if stripped.endswith("{"):
            indent += 1

    fixed_code = "\n".join(fixed)
    return markdown.replace(java_match.group(0), f"```java\n{fixed_code}\n```")


# ─────────────────────────────────────────────
# ASSEMBLE FINAL MARKDOWN
# ─────────────────────────────────────────────

def assemble_markdown(llm_output):
    created = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build the full markdown
    markdown = f"---\ncreated: {created}\n{llm_output.strip()}"

    # Apply all fixes
    markdown = fix_frontmatter(markdown)
    markdown = fix_problem_id(markdown)
    markdown = fix_java_indentation(markdown)

    return markdown


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("\n🚀 DSA Note Generator\n" + "─" * 40)

    # 1. Check file exists
    if not RAW_TEXT_FILE.exists():
        print(f"❌ raw_text.txt not found at:\n   {RAW_TEXT_FILE}")
        return

    # 2. Read file
    full_text = RAW_TEXT_FILE.read_text(encoding="utf-8")
    lines = full_text.splitlines()

    if not lines or not lines[0].strip():
        print("❌ raw_text.txt is empty or first line is blank.")
        print("   First line must be: LT_0043_MULTIPLY_STRINGS")
        return

    # 3. Parse first line → filename
    try:
        code_prefix, title, output_name = parse_first_line(lines[0])
    except ValueError as e:
        print(f"❌ {e}")
        return

    # 4. Raw content = everything after line 1
    raw_content = "\n".join(lines[1:]).strip()
    if not raw_content:
        print("❌ No content found after the first line.")
        return

    # 5. Display metadata
    meta = parse_metadata(raw_content)
    print(f"📄 File     : {RAW_TEXT_FILE.name}")
    print(f"   Prefix  : {code_prefix}")
    print(f"   Title   : {title}")
    print(f"   ID      : {meta['id']}")
    print(f"   Diff    : {meta['difficulty']}")
    print(f"   Tags    : {meta['tags']}")
    print(f"   Source  : {meta['source']}")
    print(f"   Output  : {output_name}")
    print()

    # 6. Call Qwen
    llm_output = call_qwen(SYSTEM_PROMPT, build_user_prompt(code_prefix, title, raw_content))

    # 7. Assemble + fix + write
    final_markdown = assemble_markdown(llm_output)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / output_name
    output_path.write_text(final_markdown, encoding="utf-8")

    print(f"\n  ✅ Note saved → {output_path}")
    print("\n🎉 Done!")


if __name__ == "__main__":
    main()