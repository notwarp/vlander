# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------

bl_info = {
    'name': 'Vlander',
    'description': 'Land Generator for Blender 3D',
    'author': 'notwarp',
    'license': 'GPL',
    'deps': '',
    'version': (0, 0, 1),
    'blender': (2, 90, 0),
    'location': 'View3D > Header',
    'warning': '',
    'doc_url': 'https://github.com/notwarp/vlander/wiki',
    'tracker_url': 'https://github.com/notwarp/vlander/issues',
    'link': 'https://github.com/notwarp/vlander',
    'support': 'COMMUNITY',
    'category': 'View 3D'
}

if "bpy" in locals():
    import importlib as imp

    imp.reload(vlander_settings)
    settings = vlander_settings.VlanderSettings()
    imp.reload(vlander_menu)
    vlander_menu.settings = settings

else:
    from . import vlander_settings
    settings = vlander_settings.VlanderSettings()
    from . import vlander_menu
    vlander_menu.settings = settings

# noinspection PyUnresolvedReferences
import bpy
# noinspection PyUnresolvedReferences
from bpy.types import (
    Panel, WindowManager, PropertyGroup,
    AddonPreferences, Menu
)
from bpy.props import (
    EnumProperty, PointerProperty,
    StringProperty, BoolProperty,
    IntProperty, FloatProperty, FloatVectorProperty
)

# ----------------------------------------------------
# Addon preferences
# ----------------------------------------------------


class Vlander_Pref(AddonPreferences):
    bl_idname = __name__
    settings = {}
    auto_fetch: BoolProperty(
        name="Auto Update",
        description="Vlander Auto Update",
        default=False
    )
    get_beta: BoolProperty(
        name="Get Beta Update",
        description="Vlander Beta",
        default=False
    )
    use_extra: BoolProperty(
        name="Use Extra Features",
        description="Vlander Extra Features",
        default=False
    )
    use_experimental: BoolProperty(
        name="Use Experimental Features",
        description="Vlander Experimental Features",
        default=False
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        split = row.split(factor=0.5)
        col = split.column()
        box = col.box()

        row = box.row()
        col = row.column()
        col.label(text="Update:", icon='TEMP')

        row = box.row()
        col = row.column()
        col.prop(self, "auto_fetch",
                 icon_value=settings.icons_collection['main']['git-white'].icon_id)
        col.prop(self, "get_beta", icon_value=settings.icons_collection['main']['git'].icon_id)

        col = split.column()
        box = col.box()
        row = box.row()
        col = row.column()
        col.label(text="Features:", icon='PROPERTIES')
        row = box.row()
        col = row.column()
        col.prop(self, "use_extra", icon='MOD_EXPLODE')
        col.prop(self, "use_experimental", icon='ERROR')


settings.VLANDER_classes += [Vlander_Pref]

# ----------------------------------------------------
# Add imported classes in VLANDER_classes array
# ----------------------------------------------------

settings.VLANDER_classes += [vlander_menu.VIEW3D_PT_Vlander_menu]


def register():
    settings.setup()
    for cls in settings.VLANDER_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(settings.VLANDER_classes):
        bpy.utils.unregister_class(cls)
    settings.destroy()


if __name__ == "__main__":
    register()
