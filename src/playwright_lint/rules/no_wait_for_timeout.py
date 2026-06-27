import ast
from pathlib import Path

from playwright_lint.finding import Finding

CODE = "PWS002"
MESSAGE = (
    "Avoid page.wait_for_timeout(); prefer a locator assertion or a specific wait "
    "condition."
)


def check(tree: ast.AST, path: Path) -> list[Finding]:
    findings: list[Finding] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func = node.func

        if isinstance(func, ast.Attribute) and func.attr == "wait_for_timeout":
            findings.append(
                Finding(
                    path=path,
                    line=node.lineno,
                    col=node.col_offset + 1,
                    code=CODE,
                    message=MESSAGE,
                    url="",
                )
            )

    return findings
