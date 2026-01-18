# ============================================================
# CLI Tool: Multi-Language Syntax Error Checker
# File: cli.py
# ============================================================

import sys
from error_engine import detect_errors


def print_usage():
    print("Usage:")
    print("  python cli.py <path_to_code_file>")
    print("Example:")
    print("  python cli.py test.java")


def main():
    # --------------------------------------------------------
    # 1. Argument Check
    # --------------------------------------------------------
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    file_path = sys.argv[1]

    # --------------------------------------------------------
    # 2. Read Code File
    # --------------------------------------------------------
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    # --------------------------------------------------------
    # 3. Detect Errors (PASS FILENAME 🔥)
    # --------------------------------------------------------
    result = detect_errors(code, filename=file_path)

    # --------------------------------------------------------
    # 4. Print Results
    # --------------------------------------------------------
    print("=" * 60)
    print("🧠 Multi-Language Syntax Error Checker (CLI)")
    print("=" * 60)

    print(f"📂 File        : {file_path}")
    print(f"🗂 Language    : {result['language']}")
    print(f"🤖 ML Error    : {result['predicted_error']}")
    print("-" * 60)

    # --------------------------------------------------------
    # 5. Rule-Based Issues (Python Only)
    # --------------------------------------------------------
    issues = result.get("rule_based_issues", [])

    if issues:
        print("⚠️ Rule-Based Syntax Issues (Python):")
        for i, issue in enumerate(issues, start=1):
            print(f"\n{i}. {issue.get('type')}")
            if issue.get("line"):
                print(f"   Line      : {issue.get('line')}")
            print(f"   Message   : {issue.get('message')}")
            if issue.get("suggestion"):
                print(f"   Suggestion: {issue.get('suggestion')}")
    else:
        print("✅ No rule-based syntax issues detected.")

    print("\n" + "=" * 60)
    print("Done.")
    print("=" * 60)


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
