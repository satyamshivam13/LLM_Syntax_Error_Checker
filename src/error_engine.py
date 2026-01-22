from .language_detector import detect_language
from .ml_engine import detect_error_ml
from .syntax_checker import detect_all
from .tutor_explainer import explain_error

CONFIDENCE_THRESHOLD = 0.65


def detect_errors(code: str, filename: str | None = None):
    # 🔑 language detection WITH filename
    language = detect_language(code, filename)

    # ------------------------------------------------
    # 1. Python: Rule-based detection is FINAL
    # ------------------------------------------------
    rule_based_issues = []

    if language == "Python":
        rule_based_issues = detect_all(code)

        if not rule_based_issues:
            return {
                "language": language,
                "predicted_error": "NoError",
                "confidence": 1.0,
                "tutor": {
                    "why": "The Python code follows correct syntax rules.",
                    "fix": "No changes are required."
                },
                "rule_based_issues": []
            }

    # ------------------------------------------------
    # 2. ML-based prediction
    # ------------------------------------------------
    ml_error, confidence = detect_error_ml(code)

    # ------------------------------------------------
    # 3. HARD RULES: Java / C / C++
    # ------------------------------------------------
    if language in ["Java", "C", "C++"]:
        lines = [l.strip() for l in code.splitlines() if l.strip()]

        semicolon_ok = all(
            l.endswith(";") or l.endswith("{") or l.endswith("}")
            for l in lines
        )

        # ❌ Missing semicolon is ALWAYS an error
        if not semicolon_ok:
            tutor_help = explain_error("MissingDelimiter")
            return {
                "language": language,
                "predicted_error": "MissingDelimiter",
                "confidence": confidence,
                "tutor": tutor_help,
                "rule_based_issues": []
            }

        # ✅ Semicolons OK → allow NoError
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "language": language,
                "predicted_error": "NoError",
                "confidence": confidence,
                "tutor": {
                    "why": "The code follows valid syntax rules for this language.",
                    "fix": "No changes are required."
                },
                "rule_based_issues": []
            }

    # ------------------------------------------------
    # 4. Fallback (non-Java languages only)
    # ------------------------------------------------
    if language not in ["Java", "C", "C++"] and confidence < CONFIDENCE_THRESHOLD:
        return {
            "language": language,
            "predicted_error": "NoError",
            "confidence": confidence,
            "tutor": {
                "why": "The code structure appears syntactically correct.",
                "fix": "No changes are required."
            },
            "rule_based_issues": []
        }

    # ------------------------------------------------
    # 5. ERROR CASE
    # ------------------------------------------------
    tutor_help = explain_error(ml_error)

    return {
        "language": language,
        "predicted_error": ml_error,
        "confidence": confidence,
        "tutor": tutor_help,
        "rule_based_issues": rule_based_issues
    }
