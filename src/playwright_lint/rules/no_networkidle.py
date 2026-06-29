import ast
from pathlib import Path

from playwright_lint.finding import Finding

CODE = "PWS003"
MESSAGE = (
    'Avoid wait_for_load_state("networkidle"); prefer a locator assertion or a '
    "specific application condition."
)


def check(tree: ast.AST, path: Path) -> list[Finding]:
    findings: list[Finding] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if _is_networkidle_wait(node):
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


def _is_networkidle_wait(node: ast.Call) -> bool:
    func = node.func

    if not isinstance(func, ast.Attribute):
        return False

    if func.attr != "wait_for_load_state":
        return False

    return _has_networkidle_positional_arg(node) or _has_networkidle_state_keyword(node)


def _has_networkidle_positional_arg(node: ast.Call) -> bool:
    if not node.args:
        return False

    return _is_networkidle_literal(node.args[0])


def _has_networkidle_state_keyword(node: ast.Call) -> bool:
    for keyword in node.keywords:
        if keyword.arg == "state" and _is_networkidle_literal(keyword.value):
            return True

    return False


def _is_networkidle_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value == "networkidle"
