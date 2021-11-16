# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
import bpy
import os
from bpy.types import (
    Panel, WorkSpaceTool
)
from . import icons


class PROPERTIES_PT_Vlander_panel(Panel):
    bl_label = f'Vlander'
    bl_idname = "PROPERTIES_PT_Vlander_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "world"

    def draw_header(self, context):
        if context.area.type == 'PROPERTIES':
            # Example property to display a checkbox, can be anything
            self.layout.prop(
                context.scene.world.vlander,
                'is_active',
                text=''
            )
        else:
            self.layout.prop(
                context.scene.world.vlander,
                'is_active',
                icon_only=True,
                icon_value=icons.icon_collections['main']['vlander-white'].icon_id
            )

    def draw(self, context):
        layout = self.layout
        layout.enabled = context.scene.world.vlander.is_active
        layout.label(text='Vlander Properties')
        row = layout.row()
        row.operator("vlander.create", text="Create", icon_value=icons.icon_collections['main']['vlander'].icon_id)
        row = layout.row()
        row.operator("vlander.clean", text="Clean", icon_value=icons.icon_collections['main']['vlander-white'].icon_id)


class Vlander(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'
    bl_idname = "vlander"
    bl_label = "Vlander"
    bl_icon = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vlander', 'icons', 'vlander')
    bl_widget = None
    # bl_keymap = '3D View Tool: Hops'

    bl_description = (
        "This is a tooltip\n"
        "with multiple lines"
    )
    bl_keymap = (
        ("vlander.mode", {"type": "MOUSEMOVE", "value": "ANY"}, None),
    )

    # def draw_settings(context, layout, tool):
    #     layout.prop(
    #         context.scene.world.vlander,
    #         'is_active',
    #         icon_only=True,
    #         icon_value=icons.icon_collections['main']['vlander-white'].icon_id
    #     )


classes = [
    PROPERTIES_PT_Vlander_panel
]


def header_panel_draw(self, context):
    layout = self.layout
    if context.mode in {'EDIT_MESH', 'OBJECT'}:
        row = layout.row()
        if bpy.app.version[0] == 2:
            row.separator_spacer()
        row.popover(
            "PROPERTIES_PT_Vlander_panel",
            text=''
        )


def register_panels():
    from bpy.utils import (
        register_class, register_tool
    )
    for c in classes:
        register_class(c)
    if bpy.app.version[0] == 2:
        bpy.types.VIEW3D_MT_editor_menus.append(header_panel_draw)
    else:
        bpy.types.VIEW3D_HT_tool_header.prepend(header_panel_draw)
    register_tool(Vlander)

def unregister_panels():
    from bpy.utils import (
        unregister_class, unregister_tool
    )
    if bpy.app.version[0] == 2:
        bpy.types.VIEW3D_MT_editor_menus.remove(header_panel_draw)
    else:
        bpy.types.VIEW3D_HT_tool_header.remove(header_panel_draw)
    for c in reversed(classes):
        unregister_class(c)
    unregister_tool(Vlander)
