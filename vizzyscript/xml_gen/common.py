from .expr import Constant, Variable
import xml.etree.ElementTree as ET


class Element(ET.Element):
    def __init__(self, attrib: dict[str, str] | None = None) -> None:
        super().__init__(self.__class__.__name__, attrib if attrib is not None else {})


class Instructions(Element):
    def __init__(self) -> None:
        super().__init__()


class WithStyle(Element):
    def __init__(self, style: str, attrib: dict[str, str] | None = None) -> None:
        base = {"style": style}
        if attrib is not None:
            base |= attrib
        super().__init__(base)
