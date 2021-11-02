import maya.cmds as cmds


def sequential_rename_selection(name_pattern, start_num=1):

    # Get Selection #
    sels = cmds.ls(sl=True)

    # number of zeroes needed for zfill #
    z_count = name_pattern.count("#")

    # error out if no "#" symbols were found #
    if z_count == 0:
        print("name_pattern must include \"#\" symbols")
        return

    # generate "#" symbols for partition #
    z_place_holder = ""
    for z in range(z_count):
        z_place_holder += "#"

    # partition #
    par = name_pattern.partition(z_place_holder)

    # error out if "#" symbols are in multiple parts of the string
    if par[1] != z_place_holder:
        print("\"#\" symbols must be in the same part of the name_pattern")
        return

    # rename #
    for i in range(len(sels)):
        new_name = par[0]
        new_name += str(start_num + i).zfill(z_count)
        new_name += par[2]
        cmds.rename(sels[i], new_name)
        print(f"{sels[i]} renamed to {new_name}")


sequential_rename_selection("arm_##_Jnt", start_num=0)