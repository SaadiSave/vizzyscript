from typing import Any, Self
from .common import WithStyle, Element


class Constant(Element):
    def __init__(self, x: Any, data_type: str, can_replace: bool | None = None) -> None:
        attrs = {data_type: str(x)}
        if can_replace is not None:
            attrs |= {"canReplace": str(can_replace).lower()}

        super().__init__(attrs)

    @classmethod
    def from_number(cls, x: int | float) -> Self:
        return cls(x, "number")

    @classmethod
    def from_text(cls, s: str) -> Self:
        return cls(s, "text")

    @classmethod
    def from_bool(cls, b: bool) -> Self:
        bool_const = cls(str(b).lower(), "bool")
        bool_const.set("style", "true" if b else "false")
        return bool_const


class ActivationGroup(WithStyle):
    def __init__(self, n: Element) -> None:
        super().__init__("activation-group")
        self.append(n)

    @classmethod
    def fixed(cls, n: int) -> Self:
        return cls(Constant.from_number(n))


class BinaryOp(WithStyle):
    def __init__(self, style: str, op: str, left: Element, right: Element) -> None:
        super().__init__(style, {"op": op})
        self.append(left)
        self.append(right)

    @classmethod
    def add(cls, left: Element, right: Element) -> Self:
        return cls("op-add", "+", left, right)

    @classmethod
    def sub(cls, left: Element, right: Element) -> Self:
        return cls("op-sub", "-", left, right)

    @classmethod
    def mul(cls, left: Element, right: Element) -> Self:
        return cls("op-mul", "*", left, right)

    @classmethod
    def div(cls, left: Element, right: Element) -> Self:
        return cls("op-div", "/", left, right)

    @classmethod
    def mod(cls, left: Element, right: Element) -> Self:
        return cls("op-mod", "%", left, right)


class BoolOp(BinaryOp):
    # inheritance automatically sets self.__class__.__name__ to BoolOp
    # in BinaryOp's constructor

    @classmethod
    def and_(cls, left: Element, right: Element) -> Self:
        return cls("op-and", "and", left, right)

    @classmethod
    def or_(cls, left: Element, right: Element) -> Self:
        return cls("op-or", "or", left, right)


class Comparison(BinaryOp):
    @classmethod
    def eq(cls, left: Element, right: Element) -> Self:
        return cls("op-eq", "=", left, right)

    @classmethod
    def lt(cls, left: Element, right: Element) -> Self:
        return cls("op-lt", "l", left, right)

    @classmethod
    def gt(cls, left: Element, right: Element) -> Self:
        return cls("op-gt", "g", left, right)

    @classmethod
    def lte(cls, left: Element, right: Element) -> Self:
        return cls("op-lte", "le", left, right)

    @classmethod
    def gte(cls, left: Element, right: Element) -> Self:
        return cls("op-gte", "ge", left, right)


class Not(WithStyle):
    def __init__(self, inner: Element) -> None:
        super().__init__("op-not")
        self.append(inner)


class Vector(WithStyle):
    def __init__(self, x: Element, y: Element, z: Element) -> None:
        super().__init__("vec")
        self.append(x)
        self.append(y)
        self.append(z)


class Variable(Element):
    def __init__(self, name: str, *, is_list: bool = False, is_local: bool = False):
        super().__init__(
            {
                "list": str(is_list).lower(),
                "local": str(is_local).lower(),
                "variableName": name,
            }
        )
