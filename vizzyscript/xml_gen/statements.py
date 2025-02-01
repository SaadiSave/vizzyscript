from .common import WithStyle, Element, Instructions
from .expr import Constant, Variable


class If(WithStyle):
    def __init__(self, test: Element, body: list[Element]):
        super().__init__("if")
        self.append(test)

        bd = Instructions()
        for stmt in body:
            bd.append(stmt)

        self.append(bd)


class SetActivationGroup(WithStyle):
    def __init__(self, ag: Element, value: Element) -> None:
        super().__init__("set-ag")
        self.append(ag)
        self.append(value)


class SetVariable(WithStyle):
    def __init__(self, name: str, expr: Element, *, is_local: bool = False) -> None:
        super().__init__("set-variable")
        self.append(Variable(name, is_local=is_local))
        self.append(expr)
