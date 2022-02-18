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

vert_shdr = '''
    uniform mat4 ModelViewProjectionMatrix;
    uniform mat4 ModelViewMatrix;
    #ifdef USE_WORLD_CLIP_PLANES
        uniform mat4 ModelMatrix;
    #endif
    in vec3 pos;
    void main()
    {
        gl_Position = ModelViewProjectionMatrix * ModelViewMatrix * vec4(pos, 1.0);
        #ifdef USE_WORLD_CLIP_PLANES
            world_clip_planes_calc_clip_distance((ModelMatrix * vec4(pos, 1.0)).xyz);
        #endif
    }
'''


custom_frag_shdr = '''
    #if defined(USE_COLOR_U32)
        uniform uint color;
        uniform uint resolution;
    #else
        uniform vec4 color;
        uniform vec4 resolution;
    #endif
    
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
        vec2 st = gl_FragCoord.xy  / resolution.xy;
        st.x *= resolution.x / resolution.y;
        st *= 10.0;
    
        float v = cellular(st);
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


def setup_draw(context):
    global shader_points, shader_edges, shader_faces, coords, batch_points, edges, batch_edges, faces, batch_faces
    vlander_obj = context.scene.world.vlander
    coords = square_grid_zigzag(vlander_obj.dimension + 1, vlander_obj.resolution, vlander_obj.space)
    edges = edges_grid_zigzag(vlander_obj.dimension + 1, vlander_obj.resolution)
    faces = faces_grid_zigzag(vlander_obj.dimension + 1, vlander_obj.resolution)
    shader_points = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch_points = batch_for_shader(
        shader_points,
        'POINTS',
        {"pos": coords}
    )
    # shader_faces = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    shader_faces = gpu.types.GPUShader(vert_shdr, custom_frag_shdr)
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


def draw_callback_px(self, context):
    if context.scene.world.vlander.created:
        global shader_points, shader_edges, shader_faces, coords, batch_points, edges, batch_edges, faces, batch_faces
        bgl.glEnable(bgl.GL_BLEND)
        shader_points.bind()
        shader_points.uniform_float("color", (0, 1, 0, 0.3))
        batch_points.draw(shader_points)
        shader_edges.bind()
        shader_edges.uniform_float("color", (1, 1, 1, .2))
        batch_edges.draw(shader_edges)
        shader_faces.bind()
        shader_faces.uniform_float("color", (0, 1, 0, .2))
        shader_faces.bind()
        shader_faces.uniform_float("resolution", (
            context.scene.world.vlander.resolution * context.scene.world.vlander.dimension,
            context.scene.world.vlander.resolution * context.scene.world.vlander.dimension, 0, 0))
        batch_faces.draw(shader_faces)


draw_handler = False


def update_vlander_activation(self, context):
    if self.is_active:
        setup_draw(context)
        add_handler(self, context)
    else:
        remove_handler(self, context)


def update_vlander_creation(self, context):
    setup_draw(context)
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

