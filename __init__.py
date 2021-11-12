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

    # alphabetically sorted all add-on modules since reload only happens from __init__. modules with _bg are used for
    # background computations in separate blender instance and that's why they don't need reload.

    icons = reload(icons)
    main_panel = reload(main_panel)
    vlander_menus = reload(vlander_menus)
    vlander_opts = reload(vlander_opts)
    vlander_panels = reload(vlander_panels)
    vlander_props = reload(vlander_props)

else:
    from . import vlander_props
    from . import vlander_opts
    from . import vlander_panels
    from . import vlander_menus
    from . import icons

from bpy.types import (
    AddonPreferences
)
from bpy.props import (
    BoolProperty
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


classes = [
    VlanderPref
]


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    vlander_opts.register_opts()
    vlander_props.register_props()
    vlander_panels.register_panels()
    vlander_menus.register_menus()
    icons.register_icons()


def unregister():
    from bpy.utils import unregister_class
    icons.unregister_icons()
    vlander_menus.unregister_menus()
    vlander_panels.unregister_panels()
    vlander_props.unregister_props()
    vlander_opts.unregister_opts()
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

