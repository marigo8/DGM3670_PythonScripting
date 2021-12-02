import maya.cmds as cmds

class ToolUI():

    def __init__(self):
        self.m_window = 'changeColorUIWin'

    def create(self):
        self.delete()

        self.m_window = cmds.window(self.m_window, title="My Window", width=500, height=500)
        column = cmds.columnLayout(parent=self.m_window)
        cmds.button(parent=column, label="Create Empty Window", command=lambda x: create_empty_window())
        cmds.floatSlider(parent=column)
        cmds.floatSliderGrp(parent=column, label='Group 1', field=True)
        cmds.floatSliderGrp(parent=column, label='Group 2', field=True, minValue=-10.0, maxValue=10.0,
                            fieldMinValue=-100.0,
                            fieldMaxValue=100.0, value=0)
        cmds.colorIndexSliderGrp(parent=column, label="Color", maxValue=32)

        self.show()

    def delete(self):
        if cmds.window(self.m_window, exists=True):
            cmds.deleteUI(self.m_window)

    def show(self):
        if cmds.window(self.m_window, exists=True):
            cmds.showWindow(self.m_window)

myWindow = ToolUI()
myWindow.create()
help(myWindow)

myWindow.show()



def create_empty_window():
    empty_window = cmds.window(title="Empty Window")
    cmds.showWindow(empty_window)
    return
