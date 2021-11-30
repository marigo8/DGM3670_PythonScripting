import maya.cmds as cmds

window = cmds.window(title="My Window", width=500, height=500)
column = cmds.columnLayout(parent=window)
cmds.button(parent=column, label="Create Empty Window", command="create_empty_window()")
cmds.floatSlider(parent=column)
cmds.floatSliderGrp(parent=column, label='Group 1', field=True)
cmds.floatSliderGrp(parent=column, label='Group 2', field=True, minValue=-10.0, maxValue=10.0, fieldMinValue=-100.0,
                    fieldMaxValue=100.0, value=0)
cmds.colorIndexSliderGrp(parent=column, label="Color")

cmds.showWindow(window)


def create_empty_window():
    empty_window = cmds.window(title="Empty Window")
    cmds.showWindow(empty_window)
    return
