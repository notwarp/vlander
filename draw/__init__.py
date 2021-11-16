import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader


def update_vlander_activation(self, context):
    if self.is_active:
        add_handler(self, context)
    else:
        remove_handler(self, context)


def update_vlander_creation(self, context):
    context.area.tag_redraw()


def draw_callback_px(self, context):
    def v_coords(dimension):
        coordinates = []
        for x in range(dimension):
            coordinates.append((x, x, 0))
            for y in range(x):
                coordinates.append((x, y, 0))
            for y in range(x):
                coordinates.append((x-y-1, x, 0))
        return coordinates

    if context.scene.world.vlander.created:
        dim = context.scene.world.vlander.dimension
        coords = v_coords(dim)

        edges = (
            (0, 1), (1, 2), (2, 3)
        )

        faces = [[(x*(y+1), x*(y+1)+1, x*(y+1)+dim+1), (x*(y+1)+dim+1, x*(y+1)+dim, x*(y+1))]
            for y in range(dim)
                for x in range(dim)
        ]
        # print(faces)
        faces = (
            (0, 1, 7), (7, 6, 0), (1, 2, 8), (8, 7, 1), (2, 3, 9), (9, 8, 2), (3, 4, 10), (10, 9, 3), (4, 5, 11), (11, 10, 4), (5, 6, 12), (12, 11, 5), (0, 1, 7), (7, 6, 0), (2, 3, 9), (9, 8, 2), (4, 5, 11), (11, 10, 4), (6, 7, 13), (13, 12, 6), (8, 9, 15), (15, 14, 8), (10, 11, 17), (17, 16, 10), (0, 1, 7), (7, 6, 0), (3, 4, 10), (10, 9, 3), (6, 7, 13), (13, 12, 6), (9, 10, 16), (16, 15, 9), (12, 13, 19), (19, 18, 12), (15, 16, 22), (22, 21, 15), (0, 1, 7), (7, 6, 0), (4, 5, 11), (11, 10, 4), (8, 9, 15), (15, 14, 8), (12, 13, 19), (19, 18, 12), (16, 17, 23), (23, 22, 16), (20, 21, 27), (27, 26, 20), (0, 1, 7), (7, 6, 0), (5, 6, 12), (12, 11, 5), (10, 11, 17), (17, 16, 10), (15, 16, 22), (22, 21, 15), (20, 21, 27), (27, 26, 20), (25, 26, 32), (32, 31, 25), (0, 1, 7), (7, 6, 0), (6, 7, 13), (13, 12, 6), (12, 13, 19), (19, 18, 12), (18, 19, 25), (25, 24, 18), (24, 25, 31), (31, 30, 24), (30, 31, 37), (37, 36, 30)
        )

        shader_faces = gpu.shader.from_builtin('3D_UNIFORM_COLOR')

        batch_points = batch_for_shader(shader_faces, 'POINTS', {"pos": coords})
        batch_faces = batch_for_shader(shader_faces, 'TRIS', {"pos": coords}, indices=faces)
        shader_edges = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch_edges = batch_for_shader(shader_edges, 'LINES', {"pos": coords}, indices=edges)

        bgl.glEnable(bgl.GL_BLEND)
        shader_faces.bind()
        shader_faces.uniform_float("color", (0, 0, 1, 0.2))
        batch_faces.draw(shader_faces)
        shader_edges.bind()
        shader_edges.uniform_float("color", (1, 1, 1, .2))
        batch_points.draw(shader_edges)
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
