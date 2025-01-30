from .expr import Element
import xml.etree.ElementTree as ET


class Variables(Element):
    def __init__(self, variables: list[str]) -> None:
        super().__init__()
        for var in variables:
            self.append(ET.Element("Variable", {"name": var, "number": "0"}))


class Expressions(Element):
    pass


class Program(Element):
    def __init__(self, name: str) -> None:
        super().__init__({"name": name})
