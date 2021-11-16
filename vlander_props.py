# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, IntProperty
)
from . import draw
from bpy.types import World


class VlanderWorldProperties(PropertyGroup):
    is_active: BoolProperty(
        name='Vlander',
        description='Activate Vlander System',
        default=False,
        update=draw.update_vlander_activation
    )
    is_mode: BoolProperty(
        name='Is in active Mode',
        description='Vlander System Modal',
        default=False
    )
    dimension: IntProperty(
        name="dimension",
        description="Vlander Dimension",
        default=6,
        max=100,
        min=6
    )
    resolution: IntProperty(
        name="resolution",
        description="Vlander Resolution",
        default=4,
        max=32,
        min=4
    )
    created: BoolProperty(
        name="created",
        description="Vlander Created",
        default=False,
        update=draw.update_vlander_creation
    )


classes = [
    VlanderWorldProperties
]


def register_props():
    from bpy.utils import register_class
    from bpy.props import PointerProperty
    for c in classes:
        register_class(c)
    World.vlander = PointerProperty(type=VlanderWorldProperties)


def unregister_props():
    from bpy.utils import unregister_class
    from bpy.types import World
    for c in reversed(classes):
        unregister_class(c)
    del World.vlander
