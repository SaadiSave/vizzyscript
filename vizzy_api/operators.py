from typing import Any
from .types import Vec, Rad, Deg, Expr


# single argument functions
class Math:
    @staticmethod
    def abs(x: float) -> float: ...

    @staticmethod
    def floor(x: float) -> float: ...

    @staticmethod
    def ceiling(x: float) -> float: ...

    @staticmethod
    def round(x: float) -> float: ...

    @staticmethod
    def sqrt(x: float) -> float: ...

    @staticmethod
    def sin(r: Rad) -> float: ...

    @staticmethod
    def cos(r: Rad) -> float: ...

    @staticmethod
    def tan(r: Rad) -> float: ...

    @staticmethod
    def asin(x: float) -> Rad: ...

    @staticmethod
    def acos(x: float) -> Rad: ...

    @staticmethod
    def atan(x: float) -> Rad: ...

    @staticmethod
    def ln(x: float) -> float: ...

    @staticmethod
    def log(x: float) -> float: ...

    @staticmethod
    def rad2deg(r: Rad) -> Deg: ...

    @staticmethod
    def deg2rad(d: Deg) -> Rad: ...


# standalone


def random(lower: float, upper: float) -> float: ...


def min_of(lower: float, upper: float) -> float: ...


def max_of(lower: float, upper: float) -> float: ...


def atan2(y: float, x: float) -> Rad: ...


def join(*args: Expr) -> str: ...


def length_of(s: str) -> int: ...


def letter(idx: int, s: str) -> str: ...


def letters(i_from: int, i_to: int, s: str) -> str: ...


def contains(char: str, s: str) -> bool: ...


class Friendly:
    @staticmethod
    def acceleration(x: float) -> str: ...

    @staticmethod
    def angular_velocity(x: float) -> str: ...

    @staticmethod
    def coordinate(x: float) -> str: ...

    @staticmethod
    def density(x: float) -> str: ...

    @staticmethod
    def distance(x: float) -> str: ...

    @staticmethod
    def energy(x: float) -> str: ...

    @staticmethod
    def force(x: float) -> str: ...

    @staticmethod
    def specific_impulse(x: float) -> str: ...

    @staticmethod
    def mass(x: float) -> str: ...

    @staticmethod
    def power(x: float) -> str: ...

    @staticmethod
    def pressure(x: float) -> str: ...

    @staticmethod
    def temperature(x: float) -> str: ...

    @staticmethod
    def time(x: float) -> str: ...

    @staticmethod
    def datetime(x: float) -> str: ...

    @staticmethod
    def velocity(x: float) -> str: ...


class VectorMath:
    @staticmethod
    def angle(v1: Vec, v2: Vec) -> Deg: ...

    @staticmethod
    def clamp(v1: Vec, v2: Vec) -> float: ...

    @staticmethod
    def cross(v1: Vec, v2: Vec) -> Vec: ...

    @staticmethod
    def dot(v1: Vec, v2: Vec) -> float: ...

    @staticmethod
    def dist(v1: Vec, v2: Vec) -> float: ...

    @staticmethod
    def min(v1: Vec, v2: Vec) -> Vec: ...

    @staticmethod
    def max(v1: Vec, v2: Vec) -> Vec: ...

    @staticmethod
    def project(v1: Vec, v2: Vec) -> Vec: ...

    @staticmethod
    def scale(v1: Vec, v2: Vec) -> Vec: ...


def fUNk(funk: str) -> Any: ...
