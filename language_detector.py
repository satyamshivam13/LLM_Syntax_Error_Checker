import os

def detect_language(code: str, filename: str | None = None) -> str:
    code_lower = code.lower()

    # -------------------------
    # 1. Filename-based (CLI)
    # -------------------------
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".py":
            return "Python"
        if ext == ".java":
            return "Java"
        if ext == ".c":
            return "C"
        if ext == ".cpp":
            return "C++"

    # -------------------------
    # 2. Content-based fallback
    # -------------------------
    if "def " in code_lower or "print(" in code_lower:
        return "Python"

    if "system.out.println" in code_lower or "public class" in code_lower:
        return "Java"

    if "cout <<" in code_lower:
        return "C++"

    if "printf(" in code_lower or "int main" in code_lower:
        return "C"

    return "Unknown"
