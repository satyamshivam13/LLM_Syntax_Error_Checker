EXPLANATIONS = {
    "MissingColon": {
        "why": "In many programming languages, certain statements must end with a delimiter such as ':' (Python) or ';' (C/Java/C++).",
        "fix": "Add the required delimiter at the end of the statement."
    },
    "MissingDelimiter": {
        "why": "Statements in C, C++, and Java must end with a semicolon.",
        "fix": "Add a semicolon ';' at the end of the statement."
    },
    "IndentationError": {
        "why": "Python uses indentation to define code blocks.",
        "fix": "Indent the statement correctly (usually 4 spaces inside blocks)."
    },
    "UnclosedString": {
        "why": "A string was started but not closed with a matching quote.",
        "fix": "Add the missing quote to close the string."
    },
    "UnmatchedBracket": {
        "why": "Every opening bracket '{', '(', '[' must have a matching closing bracket.",
        "fix": "Add or remove brackets so that all pairs match correctly."
    },
    "DivisionByZero": {
        "why": "Division by zero is undefined and will cause a runtime error.",
        "fix": "Ensure the denominator is not zero before performing division."
    },
    "UndeclaredIdentifier": {
        "why": "A variable or identifier is used without being declared.",
        "fix": "Declare the variable before using it."
    },
    "MissingInclude": {
        "why": "The function or object used requires a header file that has not been included.",
        "fix": "Add the required #include statement at the top of the file."
    },
    "TypeMismatch": {
        "why": "A value of one data type is being assigned to a variable of another type.",
        "fix": "Convert the value to the correct type or change the variable type."
    }
}

def explain_error(error_type: str):
    return EXPLANATIONS.get(
        error_type,
        {
            "why": "The code contains a structural or syntactic issue.",
            "fix": "Review the code structure and correct the error."
        }
    )
