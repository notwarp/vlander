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


def draw_vlander_settings(context, layout):
    if context.area.type == 'PROPERTIES':
        layout.prop(context.scene.world.vlander, 'dimension')
        layout.prop(context.scene.world.vlander, 'resolution')


def draw_vlander_actions(context, col):
    if not context.scene.world.vlander.created:
        draw_vlander_settings(context, col)
        col.operator(
            "vlander.create",
            text="Create",
            icon_value=icons.icon_collections['main']['vlander'].icon_id
        )
    else:
        col.operator(
            "vlander.clean",
            text="Clean",
            icon_value=icons.icon_collections['main']['vlander-white'].icon_id
        )


class PROPERTIES_PT_Vlander_panel(Panel):
    bl_label = f'Vlander'
    bl_idname = "PROPERTIES_PT_Vlander_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "world"

    def draw_header(self, context):
        if context.area.type == 'PROPERTIES':
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
        layout.label(text='Vlander Actions')
        col = layout.column()
        draw_vlander_actions(context, col)


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
    bl_keymap = None

    def draw_settings(context, layout, tool):
        layout.prop(
            context.scene.world.vlander,
            'is_active',
            icon_only=True,
            icon_value=icons.icon_collections['main']['vlander-white'].icon_id
        )
        draw_vlander_actions(context, layout)


classes = [
    PROPERTIES_PT_Vlander_panel
]


def register_panels():
    from bpy.utils import (
        register_class, register_tool
    )
    for c in classes:
        register_class(c)
    register_tool(Vlander)


def unregister_panels():
    from bpy.utils import (
        unregister_class, unregister_tool
    )
    for c in reversed(classes):
        unregister_class(c)
    unregister_tool(Vlander)
