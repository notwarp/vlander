# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
import bpy
from bpy.types import Panel
from . import icons


class PROPERTIES_PT_Vlander_panel(Panel):
    bl_label = f'Vlander'
    bl_idname = "PROPERTIES_PT_Vlander_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "world"

    # @classmethod
    # def poll(cls, context):
    #     return context.scene.world.vlander.is_active

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


classes = [
    PROPERTIES_PT_Vlander_panel
]


def header_panel_draw(self, context):
    layout = self.layout
    if context.mode in {'EDIT_MESH', 'OBJECT'}:
        row = layout.row()
        if bpy.app.version[0] == 2:
            row.separator_spacer()
        # row.prop(
        #     context.scene.world.vlander,
        #     'is_active',
        #     icon_only=True,
        #     icon_value=icons.icon_collections['main']['git-white'].icon_id
        # )
        row.popover(
            "PROPERTIES_PT_Vlander_panel",
            text=''
        )


def register_panels():
    from bpy.utils import register_class
    for c in classes:
        register_class(c)
    if bpy.app.version[0] == 2:
        bpy.types.VIEW3D_MT_editor_menus.append(header_panel_draw)
    else:
        bpy.types.VIEW3D_HT_tool_header.prepend(header_panel_draw)


def unregister_panels():
    from bpy.utils import unregister_class
    if bpy.app.version[0] == 2:
        bpy.types.VIEW3D_MT_editor_menus.remove(header_panel_draw)
    else:
        bpy.types.VIEW3D_HT_tool_header.remove(header_panel_draw)
    for c in reversed(classes):
        unregister_class(c)
