# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, IntProperty
)


class VlanderWorldProperties(PropertyGroup):
    is_active: BoolProperty(
        name='Vlander',
        description='Activate Vlander System',
        default=False
    )


classes = [
    VlanderWorldProperties
]


def register_props():
    from bpy.utils import register_class
    from bpy.props import PointerProperty
    from bpy.types import World
    for c in classes:
        register_class(c)
    World.vlander = PointerProperty(type=VlanderWorldProperties)


def unregister_props():
    from bpy.utils import unregister_class
    from bpy.types import World
    for c in reversed(classes):
        unregister_class(c)
    del World.vlander
