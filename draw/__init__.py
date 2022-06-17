import bpy
import bgl
import gpu
from mathutils import Matrix
from gpu_extras.batch import batch_for_shader
from ..geometry import *

shader_points = None
batch_points = None
shader_edges = None
batch_edges = None
shader_faces = None
batch_faces = None
shader_poi = None
batch_poi = None
points = None
faces = None
edges = None
poi = None

vert_shdr = '''
    uniform mat4 viewProjectionMatrix;
    
    in vec3 pos;
    in vec2 uv;
    
    out vec2 uvInterp;
    void main()
    {
        uvInterp = uv;
        gl_Position = viewProjectionMatrix * vec4(pos, 1.0);
    }
'''


custom_frag_shdr = '''
    #if defined(USE_COLOR_U32)
        uniform uint color;
        uniform uint resolution;
    #else
        uniform vec4 color;
        // uniform vec4 resolution;
        uniform vec2 u_resolution;
    #endif
    in vec2 uvInterp;
    out vec4 fragColor;
    
    vec2 random2(vec2 p) {
        return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
    }
    
    float cellular(vec2 p) {
        vec2 i_st = floor(p);
        vec2 f_st = fract(p);
        float m_dist = 10.;
        for (int j=-1; j<=1; j++ ) {
            for (int i=-1; i<=1; i++ ) {
                vec2 neighbor = vec2(float(i),float(j));
                vec2 point = random2(i_st + neighbor);
                point = 0.5 + 0.5*sin(6.2831*point);
                vec2 diff = neighbor + point - f_st;
                float dist = length(diff);
                if( dist < m_dist ) {
                    m_dist = dist;
                }
            }
        }
        return m_dist;
    }
    
    void main() {
        float v = cellular(uvInterp.xy);
        fragColor = vec4(vec3(v),color.a);
        fragColor = blender_srgb_to_framebuffer_space(fragColor);
    }
'''


frag_shdr = '''
    #if defined(USE_COLOR_U32)
        uniform uint color;
    #else
        uniform vec4 color;
    #endif
    out vec4 fragColor;
    void main()
    {
        #if defined(USE_COLOR_U32)
            fragColor = vec4(((color)&uint(0xFF)) * (1.0f / 255.0f),
                       ((color >> 8) & uint(0xFF)) * (1.0f / 255.0f),
                       ((color >> 16) & uint(0xFF)) * (1.0f / 255.0f),
                       ((color >> 24)) * (1.0f / 255.0f));
        #else
            fragColor = color;
        #endif
        fragColor = blender_srgb_to_framebuffer_space(fragColor);
    }
'''


def generate_points(obj, vlander_type):
    if vlander_type == 'HEX':
        _points = hex_grid_zigzag(obj.dimension + 1, obj.resolution, obj.space)
    else:
        _points = square_grid_zigzag(obj.dimension + 1, obj.resolution, obj.space)
    return _points


def generate_uv_from_points(coords, obj, vlander_type):
    _uvs = calculate_uv_from_coords(coords)
    # if vlander_type == 'HEX':
    #     _uvs = hex_uv_zigzag(obj.dimension + 1, obj.resolution, obj.space)
    # else:
    #     _uvs = square_grid_zigzag(obj.dimension + 1, obj.resolution, obj.space)
    return _uvs


def setup_draw(context, vlander_type):
    global shader_points, points, batch_points, \
        shader_edges, edges, batch_edges, \
        shader_faces, faces, batch_faces, \
        shader_poi, poi, batch_poi

    vlander_obj = context.scene.world.vlander

    points = generate_points(vlander_obj, vlander_type)
    uvs = generate_uv_from_points(points, vlander_obj, vlander_type)
    poi = poi_from_coords_zigzag(points, vlander_obj.dimension, vlander_obj.resolution)
    if vlander_obj.is_hidden:
        shader_points = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch_points = batch_for_shader(
            shader_points,
            'POINTS',
            {"pos": points}
        )
        faces = faces_grid_zigzag(vlander_obj.dimension + 1, vlander_obj.resolution)
        # shader_faces = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        shader_faces = gpu.types.GPUShader(vert_shdr, custom_frag_shdr)
        batch_faces = batch_for_shader(
            shader_faces,
            'TRIS',
            {
                "pos": points,
                "uv": uvs
            },
            indices=faces
        )
        edges = edges_grid_zigzag(vlander_obj.dimension + 1, vlander_obj.resolution)
        shader_edges = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch_edges = batch_for_shader(
            shader_edges,
            'LINES',
            {"pos": points},
            indices=edges
        )
    if vlander_obj.only_poi:
        shader_poi = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch_poi = batch_for_shader(
            shader_poi,
            'POINTS',
            {"pos": poi}
        )


def draw_callback_px(self, context):
    if context.scene.world.vlander.created:
        global shader_points, points, batch_points, \
            shader_edges, edges, batch_edges, \
            shader_faces, faces, batch_faces, \
            shader_poi, poi, batch_poi
        vlander_obj = context.scene.world.vlander
        if vlander_obj.is_hidden:
            bgl.glEnable(bgl.GL_BLEND)
            # POINTS
            shader_points.bind()
            shader_points.uniform_float("color", (.5, 1, 0, 1))
            batch_points.draw(shader_points)
            # EDGES
            shader_edges.bind()
            shader_edges.uniform_float("color", (1, 1, 1, .2))
            batch_edges.draw(shader_edges)
            # FACES
            # shader_faces.bind()
            shader_faces.bind()
            shader_faces.uniform_float("color", (0, 1, 0, .3))
            # shader_faces.uniform_float("u_resolution", (
            #         context.scene.world.vlander.dimension,
            #         context.scene.world.vlander.dimension
            #     )
            # )
            # shader_faces.uniform_float("modelMatrix", Matrix.Translation((1, 2, 3)) @ Matrix.Scale(3, 4))
            shader_faces.uniform_float("viewProjectionMatrix", context.region_data.perspective_matrix)
            batch_faces.draw(shader_faces)
        if vlander_obj.only_poi:
            # MIDDLE POINTS
            bgl.glEnable(bgl.GL_BLEND)
            shader_poi.bind()
            shader_poi.uniform_float("color", (1, 0, .5, 1))
            batch_poi.draw(shader_poi)


draw_handler = False


def update_vlander_activation(self, context):
    if self.is_active:
        setup_draw(context, self.types)
        add_handler(self, context)
    else:
        remove_handler(self, context)


def update_vlander_creation(self, context):
    setup_draw(context, self.types)
    context.area.tag_redraw()


def add_handler(self, context):
    args = (self, context)
    global draw_handler
    draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')


def remove_handler(self, context):
    global draw_handler
    if draw_handler:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
        draw_handler = False

