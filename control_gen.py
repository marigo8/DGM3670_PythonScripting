import maya.cmds as cmds


def changeColor(name, color_index):
    cmds.setAttr(f"{name}Shape.overrideEnabled", 1)
    cmds.setAttr(f"{name}Shape.overrideColor", color_index)


def create_controls(color_index=0):
    sels = cmds.ls(sl=True)
    if len(sels) > 0:
        for sel in sels:
            control = create_single_control(name=sel, color_index=color_index)
            cmds.matchTransform(control[0], sel)
    else:
        create_single_control(color_index=color_index)


def create_single_control(name="Control", color_index=0):
    control_name = ""
    if name.count("_") > 0:
        name_parts = name.rpartition("_")
        control_name = name_parts[0] + "_Ctrl"
    else:
        control_name = name + "_Ctrl"

    group_name = control_name + "_Grp"

    control = cmds.circle(name=control_name)[0]
    cmds.xform(control, rotation=(90, 0, 0))
    cmds.makeIdentity(control, apply=True)

    changeColor(control, color_index)

    group = cmds.group(control, name=group_name)
    return [group, control]

create_controls(13)