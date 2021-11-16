# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, IntProperty
)
import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from bpy.types import World


def update_vlander_activation(self, context):
    if self.is_active:
        add_handler(self, context)
    else:
        remove_handler(self, context)


def update_vlander_creation(self, context):
    context.area.tag_redraw()


def draw_callback_px(self, context):

    if context.scene.world.vlander.created:
        coords = (
            (-1, -1, -1), (+1, -1, -1),
            (-1, +1, -1), (+1, +1, -1),
            (-1, -1, +1), (+1, -1, +1),
            (-1, +1, +1), (+1, +1, +1))

        edges = (
            (0, 1), (0, 2), (1, 3), (2, 3),
            (4, 5), (4, 6), (5, 7), (6, 7),
            (0, 4), (1, 5), (2, 6), (3, 7)
        )

        faces = (
            (0, 1, 2), (2, 3, 0),
            (4, 5, 6), (4, 6, 3),
            (5, 7, 8), (6, 7, 0),
            (0, 4, 3), (1, 5, 2),
            (2, 6, 4), (3, 7, 6)
        )

        shader_faces = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch_faces = batch_for_shader(shader_faces, 'TRIS', {"pos": coords}, indices=faces)
        shader_edges = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch_edges = batch_for_shader(shader_edges, 'LINES', {"pos": coords}, indices=edges)

        bgl.glEnable(bgl.GL_BLEND)
        shader_faces.bind()
        shader_faces.uniform_float("color", (0, 0, 1, 0.2))
        batch_faces.draw(shader_faces)
        shader_edges.bind()
        shader_edges.uniform_float("color", (0, 1, 0, 1))
        batch_edges.draw(shader_edges)


draw_handler = False


def add_handler(self, context):
    args = (self, context)
    global draw_handler
    draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')


def remove_handler(self, context):
    global draw_handler
    if draw_handler:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
        draw_handler = False


class VlanderWorldProperties(PropertyGroup):
    is_active: BoolProperty(
        name='Vlander',
        description='Activate Vlander System',
        default=False,
        update=update_vlander_activation
    )
    is_mode: BoolProperty(
        name='Is in active Mode',
        description='Vlander System Modal',
        default=False
    )
    dim: IntProperty(
        name="dimension",
        description="Vlander Dimension",
        default=6,
        max=100,
        min=6
    )
    created: BoolProperty(
        name="created",
        description="Vlander Created",
        default=False,
        update=update_vlander_creation
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
