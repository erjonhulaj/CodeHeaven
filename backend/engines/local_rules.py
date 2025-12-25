import ast

MAX_FUNCTION_LENGTH = 25 # lines

def explain_local(code: str, language: str) -> str:

    # Local rule-based explanation with simple analysis
    if language.lower() == "python":
        issues = analyze_python_code(code)
    else:
        issues = ["(Only Python analysis supported for now)"]

    preview ="\n".join(code.strip().splitlines()[:3]) or "(empty)"

    result = (
        "[LOCAL MODE]\n"
        f"Language: {language}\n"
        "Detected Issues:\n"
        + ("\n".join(f"- {item}" for item in issues) or "None")
        + "\n\nPreview:\n"
        + preview
        )
    
    return result

def analyze_python_code(code: str) -> list[str]:
    # Analyze Python code and return a list of detected issues ("smells").
    smells: list[str] = []

    try:
        # turn the source code string into an AST tree
        tree = ast.parse(code)
    except SyntaxError as e:
        # if the code is invalid Python, report the syntax error
        return [f"Syntax Error in line: {e.lineno}: {e.msg}"]

    # TODO:
    #walk through all nodes in the AST tree
    for node in ast.walk(tree):
        # is this node an 'except' block without a specified exception type?
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            smells.append("Bare 'except:' without specifying an exception type.")
    #check for long functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            #starting line number of the function
            start = getattr(node, "lineno", None)
            #ending line number of the function
            end = start
            for inner in ast.walk(node):
                line = getattr(inner, "lineno", None)
                if line is not None and (end is None or line > end):
                    end = line

            if start is None or end is None:
                #if we cannot determine the length, skip this function
                continue

            length = end - start + 1

            if length > MAX_FUNCTION_LENGTH:
                smells.append(
                    f"Function '{node.name}' is long ({length} lines)."
                    f"Consider splitting it into smaller functions."
                )

    #check for missing docstring in functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            #a function had a docstring if the first statement is a string literal
            if (
                len(node.body) == 0
                or not isinstance(node.body[0], ast.Expr)
                or not isinstance(getattr(node.body[0], "value", None), ast.Constant)
                or not isinstance(getattr(node.body[0].value, "value", None), str)
            ):
                smells.append(f"Function '{node.name}' has no docstring."
                              "Consider adding a short description of its purpose."
                              )
                
    #check for unused variables
    assigned_vars = set()
    used_vars = set()

    for node in ast.walk(tree):
        #variable assignments: x ...
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                assigned_vars.add(node.id)
            elif isinstance(node.ctx, ast.Load): 
                used_vars.add(node.id)

    unused_vars = assigned_vars - used_vars
    for var in unused_vars:
        smells.append(f"Variable '{var}' is assigned but never used.")
    
    return smells