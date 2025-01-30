from typing import Any, Self
import xml.etree.ElementTree as ET

type Element = ET.Element


class Instructions(ET.Element):
    def __init__(self) -> None:
        super().__init__("Instructions")


class WithStyle(ET.Element):
    def __init__(
        self, tag: str, style: str, attrib: dict[str, str] | None = None, **extra: str
    ) -> None:
        base = {"style": style}
        if attrib is not None:
            base |= attrib
        super().__init__(tag, base, **extra)


class Constant(ET.Element):
    def __init__(self, x: Any, data_type: str, can_replace: bool | None = None) -> None:
        attrs = {data_type: str(x)}
        if can_replace is not None:
            attrs |= {"canReplace": str(can_replace).lower()}

        super().__init__(self.__class__.__name__, attrs)

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


def If(test: Element, body: list[Element]):
    el = WithStyle(If.__name__, "if")
    el.append(test)

    bd = Instructions()
    for stmt in body:
        bd.append(stmt)

    el.append(bd)

    return el


class BinaryOp(WithStyle):
    def __init__(self, style: str, op: str, left: Element, right: Element) -> None:
        super().__init__(self.__class__.__name__, style, {"op": op})
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
    def __init__(self, style: str, op: str, left: Element, right: Element) -> None:
        super().__init__(style, op, left, right)
        self.tag = self.__class__.__name__

    @classmethod
    def and_(cls, left: Element, right: Element) -> Self:
        return cls("op-and", "and", left, right)

    @classmethod
    def or_(cls, left: Element, right: Element) -> Self:
        return cls("op-or", "or", left, right)


class Comparison(BinaryOp):
    def __init__(self, style: str, op: str, left: Element, right: Element) -> None:
        super().__init__(style, op, left, right)
        self.tag = self.__class__.__name__

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


def Not(inner: Element):
    el = WithStyle(Not.__name__, "op-not")
    el.append(inner)
    return el


def Program(name: str):
    return ET.Element(Program.__name__, {"name": name})


def SetActivationGroup(number: int, value: Element):
    el = ET.Element(SetActivationGroup.__name__, {"style": "set-ag"})
    el.append(Constant.from_number(number))
    el.append(value)
    return el


def Variables(variables: list[str]):
    el = ET.Element(Variables.__name__)
    for var in variables:
        el.append(ET.Element("Variable", {"name": var, "number": "0"}))
    return el


def Expressions():
    return ET.Element("Expressions")


def Variable(name: str, *, is_list: bool = False, is_local: bool = False):
    return ET.Element(
        Variable.__name__,
        {
            "list": str(is_list).lower(),
            "local": str(is_local).lower(),
            "variableName": name,
        },
    )


def SetVariable(name: str, expr: Element, *, is_local: bool = False):
    el = WithStyle(SetVariable.__name__, "set-variable")
    el.append(Variable(name, is_local=is_local))
    el.append(expr)
    return el


def Vector(x: Element, y: Element, z: Element):
    el = WithStyle(Vector.__name__, "vec")
    el.append(x)
    el.append(y)
    el.append(z)
    return el
