# noinspection PyUnresolvedReferences
import bpy
# noinspection PyUnresolvedReferences
from bpy.types import (
    Panel, WindowManager, PropertyGroup,
    AddonPreferences, Menu
)

settings = {}


# ----------------------------------------------------
# Vlander Menu on 3d viewport
# ----------------------------------------------------

class VIEW3D_PT_Vlander_menu(Panel):
    """Vlander Blender Menu"""
    bl_label = f'Vlander'
    bl_idname = "VIEW3D_PT_Vlander_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text=f'No sources detected', icon='DOT')

    #############################################################################
    # the following two methods add/remove Vlander to/from the main 3D View menu
    # NOTE: this is a total hack: hijacked the draw function!
    # Copied from RetopoFlow
    # https://github.com/CGCookie/retopoflow/blob/bcab937bd03f15a8e7ea188bc9809e955020ea80/__init__.py#L556
    #############################################################################
    @staticmethod
    def menu_add():
        VIEW3D_PT_Vlander_menu.menu_remove()
        VIEW3D_PT_Vlander_menu._menu_original = bpy.types.VIEW3D_MT_editor_menus.draw_collapsible

        def hijacked(context, layout):
            VIEW3D_PT_Vlander_menu._menu_original(context, layout)
            if context.mode in {'EDIT_MESH', 'OBJECT'}:
                row = layout.row(align=True)
                row.popover(panel="VIEW3D_PT_Vlander_menu",
                            text=VIEW3D_PT_Vlander_menu.bl_label,
                            icon_value=settings.icons_collection['main']['git'].icon_id
                            )

        bpy.types.VIEW3D_MT_editor_menus.draw_collapsible = hijacked

    @staticmethod
    def menu_remove():
        if not hasattr(VIEW3D_PT_Vlander_menu, '_menu_original'): return
        bpy.types.VIEW3D_MT_editor_menus.draw_collapsible = VIEW3D_PT_Vlander_menu._menu_original
        del VIEW3D_PT_Vlander_menu._menu_original

    @staticmethod
    def register():
        VIEW3D_PT_Vlander_menu.menu_add()

    @staticmethod
    def unregister():
        VIEW3D_PT_Vlander_menu.menu_remove()
