"""Bug Diary (csv + datetime)
A personal log of the errors you hit while learning Python:
what went wrong, why, and how you fixed it. Data is saved in bug_diary.csv.
"""
import csv
import os
from datetime import datetime
from pathlib import Path

# next to this script, so the same diary opens from any folder
FILE = Path(__file__).with_name("bug_diary.csv")
FIELDS = ["id", "date", "error_type", "topic", "what_happened", "fix"]
ERROR_TYPES = ["SyntaxError", "IndentationError", "NameError", "TypeError",
               "ValueError", "IndexError", "KeyError", "Logic mistake", "Other"]


# ---------- storage (csv) ----------
def load_rows():
    try:
        with open(FILE, newline="", encoding="utf-8-sig") as f:
            raw = list(csv.DictReader(f))
    except FileNotFoundError:
        return []
    rows = []
    for r in raw:
        try:
            if None in r or None in r.values():  # too many / too few columns
                raise ValueError("wrong number of columns")
            r["id"] = int(r["id"])  # csv gives text, so convert back
            rows.append(r)
        except (KeyError, ValueError):
            print(f"Skipping damaged row: {r}")
    return rows


def save_rows(rows):
    tmp = FILE.with_suffix(".tmp")
    with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, FILE)  # all-or-nothing: old file stays intact if writing failed


# ---------- input helpers ----------
def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This cannot be empty.")


def pick_error_type():
    for i, e in enumerate(ERROR_TYPES, 1):
        print(f"  {i}. {e}")
    while True:
        try:
            n = int(input("Choose error type: "))
            if 1 <= n <= len(ERROR_TYPES):
                return ERROR_TYPES[n - 1]
        except ValueError:
            pass
        print(f"  Enter a number from 1 to {len(ERROR_TYPES)}.")


# ---------- display ----------
def show(rows):
    if not rows:
        print("Nothing found.")
        return
    for r in rows:
        print(f"\n#{r['id']}  {r['date']}  [{r['error_type']}]  topic: {r['topic']}")
        print(f"  What happened: {r['what_happened']}")
        print(f"  Fix          : {r['fix']}")
    print(f"\n{len(rows)} bug(s) shown.")


# ---------- menu actions ----------
def add_bug(rows):
    error_type = pick_error_type()
    topic = ask_text("Topic (e.g. loops, lists, files): ").lower()
    what = ask_text("What happened? ")
    fix = ask_text("How did you fix it? ")
    new_id = max((r["id"] for r in rows), default=0) + 1
    row = {"id": new_id, "date": datetime.now().strftime("%Y-%m-%d"),
           "error_type": error_type, "topic": topic,
           "what_happened": what, "fix": fix}
    rows.append(row)
    while True:
        try:
            save_rows(rows)
            break
        except PermissionError:
            if input("Cannot save - close the CSV in Excel. Retry? (y/n): ").lower() != "y":
                rows.remove(row)  # keep memory in sync with disk
                print("Not saved.")
                return
    print(f"Bug #{new_id} saved. Every bug you log is one you won't repeat!")


def search(rows):
    word = ask_text("Search word: ").lower()
    show([r for r in rows if word in " ".join(
        [r["topic"], r["what_happened"], r["fix"], r["error_type"]]).lower()])


def stats(rows):
    if not rows:
        print("No bugs logged yet.")
        return
    print(f"\nTotal bugs logged: {len(rows)}")
    counts = {}
    for r in rows:
        counts[r["error_type"]] = counts.get(r["error_type"], 0) + 1
    print("\nMistakes by type:")
    for name, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {name:<18}{'#' * n} {n}")
    top = max(counts.values())
    worst = ", ".join(k for k, v in counts.items() if v == top)
    print(f"\nYour most repeated mistake: {worst}. Revise it first!")

    topics = {}
    for r in rows:
        topics[r["topic"]] = topics.get(r["topic"], 0) + 1
    top = max(topics.values())
    print("Trickiest topic: " + ", ".join(k for k, v in topics.items() if v == top))

    week = 0
    for r in rows:
        try:
            d = datetime.strptime(r["date"], "%Y-%m-%d")
        except ValueError:
            continue  # skip rows with a bad date
        if (datetime.now() - d).days < 7:
            week += 1
    print(f"Bugs in the last 7 days: {week}")


def delete_bug(rows):
    try:
        target = int(input("Bug ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    for r in rows:
        if r["id"] == target:
            if input(f"Delete bug #{target}? (y/n): ").lower() == "y":
                rows.remove(r)
                try:
                    save_rows(rows)
                except PermissionError:
                    rows.append(r)
                    rows.sort(key=lambda x: x["id"])
                    print("Cannot save - close the CSV in Excel and try again.")
                    return
                print("Deleted.")
            return
    print("No bug with that ID.")


# ---------- main ----------
MENU = """
===== Bug Diary =====
1. Log a new bug
2. View all bugs
3. Search bugs
4. My mistake statistics
5. Delete a bug
0. Exit"""


def main():
    rows = load_rows()
    actions = {"1": add_bug, "2": show, "3": search,
               "4": stats, "5": delete_bug}
    try:
        while True:
            print(MENU)
            choice = input("\nChoose (0-5): ").strip()
            if choice == "0":
                break
            action = actions.get(choice)
            if action:
                action(rows)
            else:
                print("Invalid choice.")
    except (KeyboardInterrupt, EOFError):
        print()  # every action already saved, so nothing is lost
    print("Keep debugging, keep growing!")


if __name__ == "__main__":
    main()