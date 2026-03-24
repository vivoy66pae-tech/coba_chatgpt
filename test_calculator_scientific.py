import math
import unittest

from calculator_scientific import EvaluationError, evaluate_expression


class ScientificCalculatorTests(unittest.TestCase):
    def test_basic_math(self):
        self.assertEqual(evaluate_expression("2+3*4"), 14.0)

    def test_power_and_constants(self):
        self.assertAlmostEqual(evaluate_expression("sin(pi/2)"), 1.0)

    def test_log_with_base(self):
        self.assertEqual(evaluate_expression("log(100,10)"), 2.0)

    def test_reject_unsafe(self):
        with self.assertRaises(EvaluationError):
            evaluate_expression("__import__('os').system('ls')")

    def test_zero_division(self):
        with self.assertRaises(EvaluationError):
            evaluate_expression("1/0")


if __name__ == "__main__":
    unittest.main()
