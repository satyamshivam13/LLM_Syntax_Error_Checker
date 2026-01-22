"""
Targeted augmentation for low-precision/recall error types.
Addresses: DivisionByZero, InvalidAssignment, MissingDelimiter, TypeMismatch
"""

import pandas as pd
import random

# Load existing dataset
df = pd.read_csv('dataset/merged/all_errors.csv')

print(f"Current dataset size: {len(df)}")
print("\nCurrent distribution of weak error types:")
weak_errors = ['DivisionByZero', 'InvalidAssignment', 'MissingDelimiter', 'TypeMismatch']
for error in weak_errors:
    count = len(df[df['error_type'] == error])
    print(f"  {error}: {count}")

# ============================================================
# DivisionByZero - Need more diverse patterns
# ============================================================
division_by_zero_samples = []

# Python patterns
for i in range(40):
    patterns = [
        f"result = {random.randint(1, 100)} / 0\nprint(result)",
        f"x = 0\ny = {random.randint(1, 100)} / x",
        f"def calculate():\n    denominator = 0\n    return {random.randint(1, 100)} / denominator",
        f"numbers = [{', '.join(str(random.randint(0, 10)) for _ in range(5))}]\nresult = {random.randint(1, 100)} / numbers[{random.randint(0, 4)}]",
        f"a = {random.randint(1, 100)}\nb = 0\nc = a / b",
        f"value = {random.randint(1, 100)} % 0",
        f"def divide(x, y=0):\n    return x / y\nresult = divide({random.randint(1, 100)})",
    ]
    division_by_zero_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'DivisionByZero',
        'language': 'Python'
    })

# Java patterns
for i in range(40):
    patterns = [
        f"int result = {random.randint(1, 100)} / 0;",
        f"int x = 0;\nint y = {random.randint(1, 100)} / x;",
        f"public int calculate() {{\n    int denominator = 0;\n    return {random.randint(1, 100)} / denominator;\n}}",
        f"int a = {random.randint(1, 100)};\nint b = 0;\nint c = a / b;",
        f"double result = {random.randint(1, 100)}.0 / 0.0;",
        f"int mod = {random.randint(1, 100)} % 0;",
    ]
    division_by_zero_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'DivisionByZero',
        'language': 'Java'
    })

# C patterns
for i in range(40):
    patterns = [
        f"int result = {random.randint(1, 100)} / 0;",
        f"int x = 0;\nint y = {random.randint(1, 100)} / x;",
        f"float calculate() {{\n    int denominator = 0;\n    return {random.randint(1, 100)} / denominator;\n}}",
        f"int a = {random.randint(1, 100)};\nint b = 0;\nint c = a / b;",
        f"double result = {random.randint(1, 100)}.0 / 0.0;",
    ]
    division_by_zero_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'DivisionByZero',
        'language': 'C'
    })

print(f"\nGenerated {len(division_by_zero_samples)} DivisionByZero samples")

# ============================================================
# InvalidAssignment - Need clearer invalid patterns
# ============================================================
invalid_assignment_samples = []

# Python patterns
for i in range(30):
    patterns = [
        f"{random.randint(1, 100)} = x",
        f"'string' = value",
        f"[1, 2, 3] = items",
        f"func() = result",
        f"x + y = z",
        f"True = false",
        f"None = value",
        f"5 + 3 = result",
        f"len(array) = size",
        f"max(a, b) = maximum",
    ]
    invalid_assignment_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'InvalidAssignment',
        'language': 'Python'
    })

# Java patterns
for i in range(30):
    patterns = [
        f"{random.randint(1, 100)} = x;",
        f'"string" = value;',
        f"new int[5] = array;",
        f"getValue() = result;",
        f"x + y = z;",
        f"true = false;",
        f"null = value;",
        f"5 + 3 = result;",
    ]
    invalid_assignment_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'InvalidAssignment',
        'language': 'Java'
    })

# C patterns
for i in range(20):
    patterns = [
        f"{random.randint(1, 100)} = x;",
        f'"string" = value;',
        f"getValue() = result;",
        f"x + y = z;",
        f"NULL = value;",
    ]
    invalid_assignment_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'InvalidAssignment',
        'language': 'C'
    })

print(f"Generated {len(invalid_assignment_samples)} InvalidAssignment samples")

# ============================================================
# MissingDelimiter - More varied patterns
# ============================================================
missing_delimiter_samples = []

# Python (colons)
for i in range(30):
    patterns = [
        f"def function_{i}()\n    return {random.randint(1, 100)}",
        f"class MyClass\n    pass",
        f"if x > {random.randint(1, 10)}\n    print('hello')",
        f"for i in range({random.randint(5, 20)})\n    print(i)",
        f"while True\n    break",
        f"try\n    pass\nexcept Exception\n    pass",
        f"with open('file.txt') as f\n    data = f.read()",
        f"elif condition\n    pass",
    ]
    missing_delimiter_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'MissingDelimiter',
        'language': 'Python'
    })

# Java (semicolons)
for i in range(40):
    patterns = [
        f"int x = {random.randint(1, 100)}",
        f"String name = \"value\"",
        f"return {random.randint(1, 100)}",
        f"System.out.println(\"Hello\")",
        f"i++",
        f"break",
        f"continue",
        f"double price = {random.uniform(1, 100):.2f}",
        f"boolean flag = true",
        f"char c = 'A'",
        f"list.add(item)",
        f"obj.method()",
    ]
    missing_delimiter_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'MissingDelimiter',
        'language': 'Java'
    })

# C (semicolons)
for i in range(40):
    patterns = [
        f"int x = {random.randint(1, 100)}",
        f"char* name = \"value\"",
        f"return {random.randint(1, 100)}",
        f"printf(\"Hello\")",
        f"i++",
        f"break",
        f"continue",
        f"float price = {random.uniform(1, 100):.2f}",
        f"int flag = 1",
    ]
    missing_delimiter_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'MissingDelimiter',
        'language': 'C'
    })

print(f"Generated {len(missing_delimiter_samples)} MissingDelimiter samples")

# ============================================================
# TypeMismatch - More explicit type conflicts
# ============================================================
type_mismatch_samples = []

# Python patterns
for i in range(40):
    patterns = [
        f"result = 'string' + {random.randint(1, 100)}",
        f"value = {random.randint(1, 100)} + 'text'",
        f"x = [1, 2, 3] + {random.randint(1, 100)}",
        f"y = {random.randint(1, 100)} + [1, 2, 3]",
        f"z = 'hello' * 'world'",
        f"a = {random.randint(1, 100)} / 'string'",
        f"b = True + 'false'",
        f"c = None + {random.randint(1, 100)}",
        f"d = {{1: 2}} + {random.randint(1, 100)}",
        f"def func(x: int):\n    return x\nfunc('string')",
    ]
    type_mismatch_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'TypeMismatch',
        'language': 'Python'
    })

# Java patterns
for i in range(40):
    patterns = [
        f"String result = {random.randint(1, 100)};",
        f"int value = \"string\";",
        f"boolean flag = {random.randint(1, 100)};",
        f"double x = \"text\";",
        f"char c = {random.randint(1, 100)};",
        f"int[] arr = {random.randint(1, 100)};",
        f"String name = true;",
        f"float price = new int[5];",
        f"Object obj = {random.randint(1, 100)} + \"string\";",
    ]
    type_mismatch_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'TypeMismatch',
        'language': 'Java'
    })

# C patterns
for i in range(40):
    patterns = [
        f"char* result = {random.randint(1, 100)};",
        f"int value = \"string\";",
        f"float x = \"text\";",
        f"char c = {random.randint(1, 100)}.5;",
        f"int* ptr = {random.randint(1, 100)};",
        f"double d = \"hello\";",
    ]
    type_mismatch_samples.append({
        'buggy_code': random.choice(patterns),
        'error_type': 'TypeMismatch',
        'language': 'C'
    })

print(f"Generated {len(type_mismatch_samples)} TypeMismatch samples")

# ============================================================
# Combine all new samples
# ============================================================
new_samples = (
    division_by_zero_samples +
    invalid_assignment_samples +
    missing_delimiter_samples +
    type_mismatch_samples
)

print(f"\n{'='*60}")
print(f"Total new samples generated: {len(new_samples)}")
print(f"{'='*60}")

# Create DataFrame and append to existing dataset
new_df = pd.DataFrame(new_samples)
augmented_df = pd.concat([df, new_df], ignore_index=True)

# Save augmented dataset
augmented_df.to_csv('dataset/merged/all_errors.csv', index=False)

print(f"\n✅ Augmented dataset saved!")
print(f"Previous size: {len(df)}")
print(f"New size: {len(augmented_df)}")
print(f"Samples added: {len(new_samples)}")

print("\n📊 Updated distribution:")
for error in weak_errors:
    count = len(augmented_df[augmented_df['error_type'] == error])
    print(f"  {error}: {count}")

print("\n✅ Ready to retrain model with: python scripts/optimize_model.py")
