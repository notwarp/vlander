# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, IntProperty, EnumProperty
)

from . import draw
from bpy.types import World


def get_types_of_vlander(self, context):
    preferences = context.preferences
    vlander_experimental = preferences.addons['vlander'].preferences.use_experimental
    vlander_extra = preferences.addons['vlander'].preferences.use_extra
    enums = [
        ('QUAD', 'Quad', "Simple square Vlander type"),
        ('HEX', 'Hexagonal', "Simple hexagonal Vlander type")
    ]
    if vlander_extra:
        enums.append(('CIRCLE', 'Circle', "Simple circle Vlander type"))
    if vlander_experimental:
        enums.append(('CUSTOM', 'Custom', "Custom shape of Vlander type"))

    return enums


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
        min=6,
        update=draw.update_vlander_creation
    )
    space: IntProperty(
        name="space",
        description="Vlander Space",
        default=1,
        max=100,
        min=1,
        update=draw.update_vlander_creation
    )
    resolution: IntProperty(
        name="resolution",
        description="Vlander Resolution",
        default=1,
        max=5,
        min=1,
        update=draw.update_vlander_creation
    )
    created: BoolProperty(
        name="created",
        description="Vlander Created",
        default=False,
        update=draw.update_vlander_creation
    )
    is_hidden: BoolProperty(
        name="debug visualizer",
        description="Vlander debug visualization",
        default=False,
        update=draw.update_vlander_creation
    )
    only_poi: BoolProperty(
        name="show only POI",
        description="Vlander show only POI",
        default=False,
        update=draw.update_vlander_creation
    )
    types: EnumProperty(
        name="type of vlander",
        description="Select Vlander type",
        items=get_types_of_vlander,
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
