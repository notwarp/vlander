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
    from importlib import reload

    # alphabetically sorted all add-on modules since reload only happens from __init__.
    # modules with _bg are used for background computations in separate blender instance and that's why they don't need reload.

    icons = reload(icons)
    main_panel = reload(main_panel)

else:
    from vlander import icons
    from vlander import main_panel

from bpy.types import (
    Panel, WindowManager, PropertyGroup,
    AddonPreferences, Menu
)
from bpy.props import (
    BoolProperty, IntProperty
)


class VlanderPref(AddonPreferences):
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
                 icon_value=icons.icon_collections['main']['git-white'].icon_id
                 )
        col.prop(self, "get_beta",
                 icon_value=icons.icon_collections['main']['git'].icon_id
                 )

        col = split.column()
        box = col.box()
        row = box.row()
        col = row.column()
        col.label(text="Features:", icon='PROPERTIES')
        row = box.row()
        col = row.column()
        col.prop(self, "use_extra", icon='MOD_EXPLODE')
        col.prop(self, "use_experimental", icon='ERROR')


class VlanderRatingProps(PropertyGroup):
    rating_quality: IntProperty(name="Quality",
                                description="quality of the material",
                                default=0,
                                min=-1, max=10,
                                # update=ratings_utils.update_ratings_quality
                                )


classes = [
    VlanderPref,
    VlanderRatingProps
]

import bpy


def register():
    # settings.setup()
    for cls in classes:
        bpy.utils.register_class(cls)
    icons.register_icons()
    main_panel.register_main_panel()


def unregister():
    main_panel.unregister_main_panel()
    icons.unregister_icons()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # settings.destroy()


if __name__ == "__main__":
    register()
