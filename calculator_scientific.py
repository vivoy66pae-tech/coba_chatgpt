#!/usr/bin/env python3
"""Safe scientific expression evaluator used by the GUI app."""

from __future__ import annotations

import ast
import math
from typing import Any

ALLOWED_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "log": math.log,
    "log10": math.log10,
    "sqrt": math.sqrt,
    "exp": math.exp,
    "factorial": math.factorial,
    "abs": abs,
    "round": round,
}

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}

ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a**b,
    ast.Mod: lambda a, b: a % b,
    ast.FloorDiv: lambda a, b: a // b,
}

ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


class EvaluationError(ValueError):
    """Raised when expression cannot be evaluated safely."""


def evaluate_expression(expression: str) -> float:
    """Safely evaluate an arithmetic/scientific expression and return float."""
    expression = expression.strip()
    if not expression:
        raise EvaluationError("Ekspresi tidak boleh kosong.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise EvaluationError("Sintaks ekspresi tidak valid.") from exc

    result = _eval_node(tree.body)
    if not isinstance(result, (int, float)):
        raise EvaluationError("Hasil bukan angka.")
    return float(result)


def _eval_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise EvaluationError("Hanya konstanta numerik yang didukung.")

    if isinstance(node, ast.Name):
        if node.id in ALLOWED_CONSTANTS:
            return ALLOWED_CONSTANTS[node.id]
        raise EvaluationError(f"Nama tidak dikenal: {node.id}")

    if isinstance(node, ast.BinOp):
        operator = type(node.op)
        if operator not in ALLOWED_BINOPS:
            raise EvaluationError("Operator biner tidak didukung.")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        try:
            return ALLOWED_BINOPS[operator](left, right)
        except ZeroDivisionError as exc:
            raise EvaluationError("Tidak boleh membagi dengan nol.") from exc

    if isinstance(node, ast.UnaryOp):
        operator = type(node.op)
        if operator not in ALLOWED_UNARYOPS:
            raise EvaluationError("Operator unary tidak didukung.")
        operand = _eval_node(node.operand)
        return ALLOWED_UNARYOPS[operator](operand)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise EvaluationError("Pemanggilan fungsi tidak valid.")
        func_name = node.func.id
        if func_name not in ALLOWED_FUNCTIONS:
            raise EvaluationError(f"Fungsi tidak didukung: {func_name}")
        args = [_eval_node(arg) for arg in node.args]
        if node.keywords:
            raise EvaluationError("Argumen keyword tidak didukung.")
        try:
            return ALLOWED_FUNCTIONS[func_name](*args)
        except (TypeError, ValueError) as exc:
            raise EvaluationError(f"Error pada fungsi {func_name}: {exc}") from exc

    raise EvaluationError(f"Ekspresi tidak didukung: {type(node).__name__}")


__all__ = [
    "EvaluationError",
    "evaluate_expression",
    "ALLOWED_FUNCTIONS",
    "ALLOWED_CONSTANTS",
]
