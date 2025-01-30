from dataclasses import dataclass
from typing import Callable
from .types import Expr, PID, Planet

__all__ = [
    "on_start",
    "on_exploded",
    "on_docked",
    "on_enter_soi",
    "on_collide",
    "Channel",
    "DatalessChannel",
]


def on_start(_: Callable[[], None]) -> None: ...


def on_exploded(_: Callable[[PID], None]) -> None: ...


def on_docked(_: Callable[[PID, PID], None]) -> None: ...


def on_enter_soi(_: Callable[[Planet], None]) -> None: ...


def on_collide(_: Callable[[PID, PID, float, float], None]) -> None:
    """
    Example:

    ```
    def collision_handler(part: PID, other: PID, velocity: float, impulse: float):
        pass

    on_collide(collision_handler)
    ```
    """


@dataclass
class Channel[T: Expr]:
    msg: str

    def receive(self, _: Callable[[T], None]) -> None: ...

    def broadcast(self, data: T): ...

    def broadcast_to_craft(self, data: T): ...

    def broadcast_to_nearby_craft(self, data: T): ...


@dataclass
class DatalessChannel:
    msg: str

    def receive(self, _: Callable[[], None]) -> None: ...

    def broadcast(self) -> None: ...

    def broadcast_to_craft(self) -> None: ...

    def broadcast_to_nearby_craft(self) -> None: ...
