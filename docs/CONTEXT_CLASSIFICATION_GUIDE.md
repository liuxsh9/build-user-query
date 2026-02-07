# Context Tag Classification Guide

## Granularity Hierarchy

Context tags represent code organization structure from smallest to largest:

```
snippet < single-function < single-file < multi-file < module < repository
```

## Tag Definitions and Classification Criteria

### snippet
**Definition**: Code fragment or snippet, smaller than a complete function, may lack imports or full context.

**When to use**:
- Code missing imports or context (uses undefined variables/functions)
- Illustrative examples (marked with "Example:", "Usage:")
- Incomplete code blocks (partial implementation)
- Single expressions or statements without function wrapper
- Lambda expressions
- Tutorial code fragments
- Q&A site code answers (StackOverflow, etc.)
- Inline documentation examples

**Examples of snippets**:
```python
# Expression - missing context
result = api.get_user(id)  # 'api' not defined

# Partial code block
for item in items:
    print(item.name)

# Lambda expression
lambda x: x * 2

# Single expression
list(map(int, input().split()))
```

### single-function
**Definition**: Complete, runnable function with signature and implementation.

**When to use**:
- Has complete function signature (def/function keyword with name and parameters)
- Has full implementation body
- Can be executed or tested independently (given standard library)
- May use standard library imports implicitly

**Decision rule**:
- ✅ "Can it run independently?" → single-function
- ❌ "Needs context/missing imports?" → snippet

**Examples of single-function**:
```python
# Complete function - can run independently
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

# Simple but complete
def add(a, b):
    return a + b

# Complete with standard library
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

**Edge case - function with external imports**:
```python
# This is a SNIPPET (not single-function)
# because 'requests' is not standard library
def fetch_data(url):
    return requests.get(url).json()  # 'requests' not imported
```

### single-file
**Definition**: Complete file with imports, structure, and potentially multiple functions/classes.

**When to use**:
- Complete Python/JS/etc. file with imports
- May contain multiple functions, classes, or top-level code
- Has proper file structure (imports at top, main code below)

### multi-file
**Definition**: Changes spanning multiple files.

**When to use**:
- Cross-file refactoring
- Import reorganization
- Renaming that affects multiple files

### module
**Definition**: Module or package level code.

**When to use**:
- Implementing a complete module
- Package with __init__.py
- Library/SDK development

### repository
**Definition**: Repository-level operations.

**When to use**:
- Dependency upgrades affecting many files
- Large-scale refactoring
- Repository configuration (.gitignore, README, etc.)

## Edge Cases and Decision Guide

### One-liner functions
```python
# Simple one-liner WITH function signature → single-function
def square(x): return x * x

# One-liner WITHOUT function wrapper → snippet
x ** 2
```

### Borderline cases
**Decision rule**: "Has function signature AND can run independently?"
- ✅ YES → single-function
- ❌ NO → snippet

### Multiple functions in one snippet
If code contains multiple tiny functions but lacks complete file structure:
- Still a snippet if missing proper imports/structure
- Becomes single-file when properly structured with imports

## Common Patterns

**Documentation examples** → Usually `snippet`
**Tutorial code sections** → Usually `snippet` (unless complete files)
**Q&A answers** → Usually `snippet`
**Algorithm implementations** → `single-function` if complete, `snippet` if partial
**Utility functions** → `single-function` if self-contained
**Test cases** → Depends on structure (snippet/function/file)
