def test_one():
    import inspect
    import vizzyscript as vz
    import xml.etree.ElementTree as ET
    import sys
    from . import program

    src = inspect.getsource(program)
    p = vz.Parser("Testing VizzyScript", src)
    p.generate()
    ET.indent(p.root)
    sys.stdout.buffer.write(ET.tostring(p.root, encoding="utf-8", xml_declaration=True))


if __name__ == "__main__":
    test_one()
