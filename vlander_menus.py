# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
import bpy
from bpy.types import Menu
from . import icons


class VIEW3D_MT_Vlander_menu(Menu):
    """Vlander Blender Menu"""
    bl_idname = "VIEW3D_MT_Vlander_menu"
    bl_label = "Vlander"

    @classmethod
    def poll(cls, context):
        return context.scene.world.vlander.is_active

    def draw(self, context):
        print('draw menu')
        layout = self.layout
        layout.operator("vlander.clean", text="Clean", icon='REMOVE')
        layout.operator("vlander.create", text="Create", icon='ADD')


classes = [
    VIEW3D_MT_Vlander_menu
]


def register_menus():
    from bpy.utils import register_class
    for c in classes:
        register_class(c)


def unregister_menus():
    from bpy.utils import unregister_class
    for c in reversed(classes):
        unregister_class(c)
