from .common import Instructions, WithStyle, Element
from .expr import Constant


class Event(WithStyle):
    def __init__(self, event: str, style: str) -> None:
        super().__init__(style, {"event": event})


def ReceiveMessage(msg: str, body: list[Element]):
    root = Instructions()
    trigger = Event(ReceiveMessage.__name__, "receive-msg")
    trigger.append(Constant(msg, "text", False))
    root.append(trigger)

    for stmt in body:
        root.append(stmt)

    return root
