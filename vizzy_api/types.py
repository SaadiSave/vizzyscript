from dataclasses import dataclass
from typing import NewType, Self

__all__ = ["Vec", "Expr", "PID", "Rad", "Deg", "Planet"]


@dataclass
class Vec:
    x: float
    y: float
    z: float

    def length(self) -> float: ...

    def norm(self) -> Self: ...

    def __add__(self, other: Self) -> Self: ...

    def __sub__(self, other: Self) -> Self: ...

    def __mul__(self, other: float) -> Self: ...

    def __truediv__(self, other: float) -> Self: ...

    def __floordiv__(self, other: int) -> Self: ...


Rad = NewType("Rad", float)

Deg = NewType("Deg", float)

type Expr = float | str | bool | Vec

type PID = int

type Planet = str
