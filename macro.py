import maya.cmds as cmds


def mesh_combine(mesh0, mesh1, name):
    return cmds.polyUnite(mesh0, mesh1, constructionHistory=0, name=name)[0]


def create_limb(height=2, radius=.2, name="limb", parent_limb="", joint_height=.5, joint_radius=.25):
    # Create Limb
    limb = cmds.polyCylinder(axis=[0, 1, 0], height=height, radius=radius, ch=0, cuv=0)[0]
    cmds.move(0, -height / 2, 0, limb, absolute=1)
    cmds.move(0, 0, 0, limb + ".rotatePivot", absolute=1)
    cmds.makeIdentity(limb, apply=True, translate=1)

    joint = cmds.polyCylinder(axis=[1, 0, 0], height=joint_height, radius=joint_radius, ch=0, cuv=0)[0]

    limb = mesh_combine(limb, joint, name)

    if parent_limb != "":
        cmds.parent(limb, parent_limb)
        cmds.move(0, height, 0, parent_limb, relative=1)
    else:
        cmds.move(0, height, 0, limb, absolute=1)

    print(f"created limb: {limb}")
    return limb


# create_limb()
# create_limb(5)
# create_limb(height=3, radius=.4)

def create_robot_arm(prefix, shoulder_width=.6):
    arm_0 = create_limb(height=1.25, radius=.15, name=prefix + "_Arm_0", joint_height=shoulder_width, joint_radius=.4)

    arm_1 = create_limb(height=1, radius=.2, name=prefix + "_Arm_1", parent_limb=arm_0)
    hand = cmds.polySphere(radius=.35, name=prefix + "_Hand", ch=0, cuv=0)[0]
    cmds.parent(hand, f"{arm_0}|{arm_1}")
    return [arm_0, arm_1, hand]


def create_robot_leg(prefix, pelvis_width = .35):
    leg_0 = create_limb(height=1.5, radius=.15, name=prefix + "_Leg_0", joint_height=pelvis_width, joint_radius=.5)

    leg_1 = create_limb(height=1.5, radius=.25, name=prefix + "_Leg_1", parent_limb=leg_0, joint_height=.6, joint_radius=.3)
    foot = cmds.polyCube(width=.6, height=.5, depth=1.2, name=prefix + "_Foot", ch=0, cuv=0)[0]
    cmds.move(0, 0, .25, foot)
    cmds.move(0, 0, 0, foot + ".rotatePivot", absolute=1)
    cmds.makeIdentity(foot, apply=True, translate=1)

    cmds.parent(foot, f"{leg_0}|{leg_1}")
    return [leg_0, leg_1, foot]


def create_robot_torso(name="torso", torso_thickness=1, shoulder_width=2, pelvis_width=1.25, torso_offset=.2, head_radius=.75):
    torso0 = cmds.polySphere(name=name+"_0", radius=torso_thickness / 2, ch=0, cuv=0)[0]

    torso1 = cmds.polyCube(width=torso_thickness, height=torso_thickness, depth=torso_thickness, ch=0, cuv=0)[0]
    shoulders = cmds.polyCylinder(radius=torso_thickness / 2, height=shoulder_width, axis=[1, 0, 0], ch=0, cuv=0)[0]
    cmds.move(0, torso_thickness / 2, 0, shoulders)

    torso1 = mesh_combine(torso1, shoulders, name+"_1")

    head = cmds.polySphere(name="head", radius=head_radius, ch=0, cuv=0)[0]
    cmds.move(0, head_radius, 0, head)
    cmds.move(0, 0, 0, head + ".rotatePivot", absolute=1)
    cmds.makeIdentity(head, apply=True, translate=1)
    cmds.move(0, torso_thickness / 2, 0, head)
    cmds.parent(head, torso1);

    cmds.move(0, torso_thickness / 2 + torso_offset, 0, torso1)
    cmds.move(0, 0, 0, torso1 + ".rotatePivot", absolute=1)
    cmds.makeIdentity(torso1, apply=True, translate=1)

    pelvis = cmds.polyCylinder(name="pelvis", h=pelvis_width, r=torso_thickness/4, axis=[1, 0, 0], ch=0, cuv=0)[0]

    cmds.move(0, -torso_thickness / 4, 0, pelvis)
    cmds.move(0, 0, 0, pelvis + ".rotatePivot", absolute=1)
    cmds.makeIdentity(pelvis, apply=True, translate=1)

    cmds.parent(torso1, pelvis, torso0)
    shoulder_offset_x = shoulder_width/2
    shoulder_offset_y = torso_thickness+torso_offset
    pelvis_offset_x = pelvis_width/2
    pelvis_offset_y = -torso_thickness / 4
    return [torso0, torso1, head, pelvis, shoulder_offset_x, shoulder_offset_y, pelvis_offset_x, pelvis_offset_y]


def create_robot():
    torsoInfo = create_robot_torso()
    torso0 = torsoInfo[0]
    torso1 = torsoInfo[1]
    head = torsoInfo[2]
    pelvis = torsoInfo[3]

    shoulder_offset_x = torsoInfo[4]
    shoulder_offset_y = torsoInfo[5]
    shoulder_width = .6

    pelvis_offset_x = torsoInfo[6]
    pelvis_offset_y = torsoInfo[7]
    pelvis_width = .35

    l_armInfo = create_robot_arm("L", shoulder_width)
    cmds.move(shoulder_offset_x + shoulder_width / 2, shoulder_offset_y, 0, l_armInfo[0], absolute=1)
    r_armInfo = create_robot_arm("R", shoulder_width)
    cmds.move(-shoulder_offset_x - shoulder_width / 2, shoulder_offset_y, 0, r_armInfo[0], absolute=1)

    cmds.parent(l_armInfo[0], r_armInfo[0], f"{torso0}|{torso1}")

    l_legInfo = create_robot_leg("L", pelvis_width)
    cmds.move(pelvis_offset_x + pelvis_width / 2, pelvis_offset_y, 0, l_legInfo[0], absolute=1)
    r_legInfo = create_robot_leg("R", pelvis_width)
    cmds.move(-pelvis_offset_x - pelvis_width / 2, pelvis_offset_y, 0, r_legInfo[0], absolute=1)

    cmds.parent(l_legInfo[0], r_legInfo[0], f"{torso0}|{pelvis}")

    cmds.move(0, 3.5, 0, torso0)

    group = cmds.group(torso0, name="Robot")

    return [group,
                torso0,
                    torso1,
                        head,
                        l_armInfo[0],
                            l_armInfo[1],
                                l_armInfo[2],
                        r_armInfo[0],
                            r_armInfo[1],
                                r_armInfo[2],
                    pelvis,
                        l_legInfo[0],
                            l_legInfo[1],
                                l_legInfo[2],
                        r_legInfo[0],
                            r_legInfo[1],
                                r_legInfo[2]
            ]

robot = create_robot()
