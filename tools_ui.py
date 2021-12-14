import maya.cmds as cmds
import importlib


class tools_ui:
    def __init__(self):
        self.m_window = 'toolsUIWin'
        self.override_color = 0
        self.colorSlider = ''

    def create(self):
        self.delete()

        self.m_window = cmds.window(self.m_window, title="Tools")
        column = cmds.columnLayout(parent=self.m_window)

        # sequential renamer

        # change color
        self.colorSlider = cmds.colorIndexSliderGrp(parent=column,
                                                    label="OverrideColor",
                                                    minValue=1,
                                                    maxValue=32,
                                                    changeCommand=lambda *x: self.override_color_select_cmd())
        cmds.button(parent=column, label="Apply Color To Selection", command=lambda *x: self.override_color_apply_cmd())

        # controls
        cmds.button(parent=column, label="Create Controls", command=lambda *x: self.create_controls_cmd())

        self.show()

    def delete(self):
        if cmds.window(self.m_window, exists=True):
            cmds.deleteUI(self.m_window)

    def show(self):
        if cmds.window(self.m_window, exists=True):
            cmds.showWindow(self.m_window)

    def override_color_select_cmd(self):
        self.override_color = cmds.colorIndexSliderGrp(self.colorSlider, q=True, value=True) - 1

    def override_color_apply_cmd(self):
        import tools
        importlib.reload(tools)
        sels = cmds.ls(sl=True)
        for sel in sels:
            tools.change_color(sel, self.override_color)
        return

    def create_controls_cmd(self):
        import tools
        importlib.reload(tools)

        tools.create_controls_hierarchy(self.override_color)
