from vizzy_api import *


class VAR:
    something: int
    vector: Vec


def process_vec(vec: Vec):
    AG10 = False
    VAR.vector += Vec(1, 2, 3)
    VAR.vector -= Vec(1, 2, 3)
    VAR.vector *= 2
    VAR.vector /= VAR.something
    if 1 >= VAR.something or VAR.something >= 200:
        VAR.vector *= 2


point = Channel[types.Vec]("do")

point.receive(process_vec)
