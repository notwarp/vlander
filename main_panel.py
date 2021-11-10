# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
import bpy
from vlander import icons
from vlander import vlander_opts

from bpy.types import (
    Panel, Menu
)


class OBJECT_MT_Vlander_menu(Menu):
    """Vlander Blender Menu"""
    bl_idname = "OBJECT_MT_Vlander_menu"
    bl_label = "create"

    def draw(self, context):
        print('draw menu')
        layout = self.layout
        layout.operator("vlander.clean", text="Clean", icon='REMOVE')
        layout.operator("vlander.create", text="Create", icon='ADD')


class VIEW3D_PT_Vlander_menu_pop(Panel):
    """Vlander Blender Menu"""
    bl_idname = "VIEW3D_PT_Vlander_menu_pop"
    bl_label = "types"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_HEADER'

    def draw(self, context):
        print('draw menu pop')
        layout = self.layout
        layout.label(text="test:")
        # print(settings, '\n\n', settings.enum_icons)
        # print(settings.icons_collection["main"], '\n\n', settings.icons_collection["main"]['git'])
        # print(context.space_data.shading, '\n\n', context.space_data.shading.studio_light)

        # layout.template_icon_view(settings,
        #                           "enum_icons",
        #                           show_labels=False,
        #                           scale=6.0,
        #                           scale_popup=5.0
        #                           )
        # layout.template_icon_view(context.space_data.shading,
        #                           "studio_light",
        #                           show_labels=False,
        #                           scale=6.0,
        #                           scale_popup=5.0
        #                           )


class VIEW3D_MT_Vlander_panel(Menu):
    """Vlander Blender Panel"""
    bl_label = f' Vlander '
    bl_idname = "VIEW3D_MT_Vlander_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_HEADER'

    def draw(self, context):
        print('draw menu')
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Generate:", icon='DOT')
        col.separator()
        col.menu("OBJECT_MT_Vlander_menu",
                 text=OBJECT_MT_Vlander_menu.bl_label,
                 icon_value=icons.icon_collections['main']['git'].icon_id
                 )
        col.popover("VIEW3D_PT_Vlander_menu_pop",
                    text=VIEW3D_PT_Vlander_menu_pop.bl_label,
                    icon_value=icons.icon_collections['main']['git'].icon_id
                    )


def header_panel_draw(self, context):
    layout = self.layout
    layout.separator_spacer()
    if context.mode in {'EDIT_MESH', 'OBJECT'}:
        row = layout.row(align=True)
        row.menu("VIEW3D_MT_Vlander_panel",
                 text=VIEW3D_MT_Vlander_panel.bl_label,
                 icon_value=icons.icon_collections['main']['git'].icon_id
                 )


cls = [
    OBJECT_MT_Vlander_menu,
    VIEW3D_PT_Vlander_menu_pop,
    VIEW3D_MT_Vlander_panel
]


def register_main_panel():
    vlander_opts.register_opts()
    for c in cls:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_editor_menus.append(header_panel_draw)


def unregister_main_panel():
    bpy.types.VIEW3D_MT_editor_menus.remove(header_panel_draw)
    for c in reversed(cls):
        bpy.utils.unregister_class(c)
    vlander_opts.unregister_opts()
