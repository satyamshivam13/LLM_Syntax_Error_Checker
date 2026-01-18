# ============================================================
# Streamlit App: Live AI Tutor – Multi-Language Syntax Checker
# File: app.py
# ============================================================

import streamlit as st
from error_engine import detect_errors

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Live Multi-Language Syntax Error Checker",
    layout="centered"
)

st.title("🧠 Live Multi-Language Syntax Error Checker")

st.write(
    """
This tool acts as an **AI tutor** and detects issues **automatically as you paste or type code**.

✔ Python / Java / C / C++  
✔ ML-based multi-error classification  
✔ Rule-based Python syntax validation  
✔ Clear explanations (why + how to fix)  
✔ Positive feedback for correct code  
"""
)

# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------

if "code" not in st.session_state:
    st.session_state.code = ""

# ------------------------------------------------------------
# Code Input
# ------------------------------------------------------------

code_input = st.text_area(
    "Paste your code here",
    height=300,
    key="code",
    placeholder="Paste Python / Java / C / C++ code here..."
)

uploaded = st.file_uploader(
    "Or upload a code file",
    type=["py", "java", "c", "cpp"]
)

if uploaded:
    try:
        st.session_state.code = uploaded.read().decode("utf-8")
        code_input = st.session_state.code
    except Exception:
        st.error("❌ Unable to read uploaded file.")

# ------------------------------------------------------------
# LIVE DETECTION (NO BUTTON)
# ------------------------------------------------------------

if code_input.strip():
    # Pass filename if file is uploaded (important for Java/C/C++)
    filename = uploaded.name if uploaded else None
    result = detect_errors(code_input, filename=filename)


    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    st.success(f"🗂 Detected Language: **{result['language']}**")

    # --------------------------------------------------------
    # NO ERROR CASE (AUTHORITATIVE)
    # --------------------------------------------------------

    if result["predicted_error"] == "NoError":
        st.success("✅ No syntax errors detected")

        st.subheader("🧠 AI Tutor Feedback")
        st.write("✔ Your code is syntactically correct.")
        st.write("✔ No corrections are required.")

        error_lines = set()

    # --------------------------------------------------------
    # ERROR CASE
    # --------------------------------------------------------

    else:
        st.error(f"❌ Detected Error Type: **{result['predicted_error']}**")

        st.subheader("🧠 AI Tutor Explanation")
        st.write(f"**Why this happened:** {result['tutor']['why']}")
        st.write(f"**How to fix it:** {result['tutor']['fix']}")

        # ----------------------------------------------------
        # Rule-Based Issues (Python)
        # ----------------------------------------------------

        issues = result.get("rule_based_issues", [])
        error_lines = set()

        if issues:
            st.subheader("⚠️ Detailed Syntax Issues (Python)")
            for i, iss in enumerate(issues, start=1):
                st.error(f"{i}. {iss.get('type')} (Line {iss.get('line')})")
                st.write(iss.get("message"))
                if iss.get("suggestion"):
                    st.info(iss.get("suggestion"))
                if iss.get("line"):
                    error_lines.add(iss["line"])
        else:
            # Non-Python / ML-only case → highlight entire snippet
            error_lines = set(range(1, len(code_input.splitlines()) + 1))

    # --------------------------------------------------------
    # Code Display with Highlighting
    # --------------------------------------------------------

    st.markdown("---")
    st.subheader("📄 Code with Highlighted Errors")

    lines = code_input.splitlines()
    highlighted_code = []

    for i, line in enumerate(lines, start=1):
        if i in error_lines:
            highlighted_code.append(
                f"<span style='color:red; font-weight:bold;'>❌ {i:03d}: {line}</span>"
            )
        else:
            highlighted_code.append(f"{i:03d}: {line}")

    st.markdown(
        "<pre style='background-color:#f6f8fa; padding:12px; border-radius:6px;'>"
        + "\n".join(highlighted_code)
        + "</pre>",
        unsafe_allow_html=True
    )

else:
    st.info("👆 Paste or upload code to start live analysis.")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.markdown("---")
st.caption(
    "🔴 Live detection | Hybrid Rule-Based + ML | AI Tutor–Style Feedback | Academic Project"
)
