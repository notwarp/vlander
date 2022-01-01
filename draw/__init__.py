import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from ..geometry import (
    square_grid_diagonal,
    edges_grid_diagonal,
    square_grid_zigzag,
    edges_grid_zigzag,
    faces_grid_zigzag
)

shader_points = None
batch_points = None
shader_edges = None
batch_edges = None
shader_faces = None
batch_faces = None
coords = None
faces = None
edges = None


def setup_draw(context):
    global shader_points, shader_edges, shader_faces, coords, batch_points, edges, batch_edges, faces, batch_faces
    coords = square_grid_zigzag(context.scene.world.vlander.dimension, context.scene.world.vlander.distance)
    edges = edges_grid_zigzag(context.scene.world.vlander.dimension)
    faces = faces_grid_zigzag(context.scene.world.vlander.dimension)
    shader_points = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch_points = batch_for_shader(
        shader_points,
        'POINTS',
        {"pos": coords}
    )
    shader_faces = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch_faces = batch_for_shader(
        shader_faces,
        'TRIS',
        {"pos": coords},
        indices=faces
    )
    shader_edges = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch_edges = batch_for_shader(
        shader_edges,
        'LINES',
        {"pos": coords},
        indices=edges
    )


def update_vlander_activation(self, context):
    if self.is_active:
        setup_draw(context)
        add_handler(self, context)
    else:
        remove_handler(self, context)


def update_vlander_creation(self, context):
    setup_draw(context)
    context.area.tag_redraw()


def draw_callback_px(self, context):
    if context.scene.world.vlander.created:
        global shader_points, shader_edges, shader_faces, coords, batch_points, edges, batch_edges, faces, batch_faces
        bgl.glEnable(bgl.GL_BLEND)
        shader_points.bind()
        shader_points.uniform_float("color", (0, 0, 1, 0.2))
        batch_faces.draw(shader_points)
        shader_edges.bind()
        shader_edges.uniform_float("color", (1, 1, 1, .2))
        batch_points.draw(shader_edges)
        shader_faces.bind()
        shader_faces.uniform_float("color", (0, 1, 0, 1))
        batch_edges.draw(shader_faces)


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
