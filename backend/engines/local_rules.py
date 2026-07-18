# local_rules.py

import ast
from backend.models import Finding

MAX_FUNCTION_LENGTH = 25  # lines


def explain_local(code: str, language: str) -> dict:
    if language.lower() == "python":
        issues = analyze_python_code(code)
    else:
        issues = [Finding(
            rule="unsupported",
            message=f"Language '{language}' is not yet supported in local mode. Only Python is supported.",
            severity="info"
        )]

    return {"issues": [issue.model_dump() for issue in issues]}


def analyze_python_code(code: str) -> list[Finding]:
    findings: list[Finding] = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [Finding(
            rule="syntax_error",
            message=f"Syntax error on line {e.lineno}: {e.msg}",
            severity="high",
            line=e.lineno
        )]

    # Bare except
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(Finding(
                rule="bare_except",
                message="Bare 'except:' catches all exceptions including KeyboardInterrupt. Specify the exception type (e.g. 'except ValueError:').",
                severity="high",
                line=getattr(node, "lineno", None)
            ))

    # Long functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = getattr(node, "lineno", None)
            end = start
            for inner in ast.walk(node):
                line = getattr(inner, "lineno", None)
                if line is not None and (end is None or line > end):
                    end = line

            if start is not None and end is not None:
                length = end - start + 1
                if length > MAX_FUNCTION_LENGTH:
                    findings.append(Finding(
                        rule="long_function",
                        message=f"Function '{node.name}' is {length} lines long (limit: {MAX_FUNCTION_LENGTH}). Consider splitting it into smaller functions.",
                        severity="medium",
                        line=start
                    ))

    # Missing docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            has_docstring = (
                len(node.body) > 0
                and isinstance(node.body[0], ast.Expr)
                and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                and isinstance(node.body[0].value.value, str)
            )
            if not has_docstring:
                findings.append(Finding(
                    rule="missing_docstring",
                    message=f"Function '{node.name}' has no docstring. Add a short description of what it does.",
                    severity="low",
                    line=getattr(node, "lineno", None)
                ))

    # Unused variables (track line numbers)
    assigned: dict[str, int | None] = {}
    used: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                if node.id not in assigned:
                    assigned[node.id] = getattr(node, "lineno", None)
            elif isinstance(node.ctx, ast.Load):
                used.add(node.id)

    for var, line in assigned.items():
        if var not in used and not var.startswith("_"):
            findings.append(Finding(
                rule="unused_variable",
                message=f"Variable '{var}' is assigned but never used.",
                severity="medium",
                line=line
            ))

    return findings
