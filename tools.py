import maya.cmds as cmds


def change_color(name, color_index):
    shapes = cmds.listRelatives(name, shapes=True)
    cmds.setAttr(f"{shapes[0]}.overrideEnabled", 1)
    cmds.setAttr(f"{shapes[0]}.overrideColor", color_index)
