import maya.cmds as cmds
import random


def random_scatter(count=1, min_x=-10, min_y=-10, min_z=-10, max_x=10, max_y=10, max_z=10):
    sels = cmds.ls(sl=True)
    return_sels = []

    for sel in sels:
        for i in range(count):
            dup = cmds.duplicate(sel, rr=True)[0]
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            z = random.uniform(min_z, max_z)
            cmds.move(x, y, z, dup, absolute=True)
            return_sels.append(dup)

    cmds.select(return_sels)
    return return_sels


print(random_scatter(count=5))
