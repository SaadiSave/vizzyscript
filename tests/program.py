from vizzy_api import *


class VAR:
    something: int
    vector: Vec


def process_vec(vec: Vec):
    global AG10  # need AG10 from global scope
    AG10 = not AG10
    VAR.vector += Vec(1, 2, 3)
    VAR.vector -= Vec(1, 2, 3)
    VAR.vector *= 2
    VAR.vector /= VAR.something
    if 1 <= VAR.something <= 200 or AG(VAR.something):
        AG.set(VAR.something, True)


point = Channel[types.Vec]("do")

point.receive(process_vec)
