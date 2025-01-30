from .types import Expr


def wait(seconds: float) -> None: ...


def wait_until(expr: bool) -> None: ...


def display(expr: Expr) -> None: ...


def local_log(expr: Expr) -> None: ...


def flight_log(expr: Expr, overwrite: bool) -> None: ...


def comment(s: str) -> None:
    """
    Only use if comments must be retained in the generated Vizzy program.
    Use normal python comments otherwise.
    """
