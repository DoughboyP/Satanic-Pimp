#!/usr/bin/env python3
"""
doughboyP - Python Programmer
General purpose Python code by doughboyP
"""

__author__ = "doughboyP"
__version__ = "1.0.0"


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to doughboyP's code."


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


def factorial(n: int) -> int:
    """Return the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> list:
    """Return the first n numbers of the Fibonacci sequence."""
    if n <= 0:
        return []
    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]


def reverse_string(s: str) -> str:
    """Return the reverse of a string."""
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Return True if the string is a palindrome, ignoring case and spaces."""
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    print(greet("World"))
    print(f"5 + 3 = {add(5, 3)}")
    print(f"Fibonacci(10) = {fibonacci(10)}")
    print(f"Factorial(7) = {factorial(7)}")
    print(f"Is 'racecar' a palindrome? {is_palindrome('racecar')}")
