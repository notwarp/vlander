# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------

import bpy
from bpy.types import Operator
from bpy.props import (
    BoolProperty, IntProperty
)


class VLANDER_OT_create(Operator):
    bl_idname = "vlander.create"
    bl_label = "Create"
    bl_description = "Create"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = {'INVOKE_DEFAULT'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        context.scene.world.vlander.created = True
        if context.mode == "OBJECT":
            # TODO create all
            pass
        return {'FINISHED'}


class VLANDER_OT_clean(Operator):
    bl_idname = "vlander.clean"
    bl_label = "Clean"
    bl_description = "Clean"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        context.scene.world.vlander.created = False
        if context.mode == "OBJECT":
            # TODO create all
            pass
        return {'FINISHED'}


class VLANDER_OT_chosetypes(Operator):
    """Chose Type model assets"""
    bl_idname = "vlander.chosetypes"
    bl_label = "Type"
    bl_description = "Type"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        print("Start VLANDER_OT_chosetypes")

    def __del__(self):
        print("End VLANDER_OT_chosetypes")

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.template_icon_view(context.space_data.shading,
                                  "studio_light",
                                  show_labels=False,
                                  scale=6.0,
                                  scale_popup=5.0
                                  )

    def execute(self, context):
        print(context.object.location.x, self.bl_idname)
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


cls = [
    VLANDER_OT_create,
    VLANDER_OT_clean,
    VLANDER_OT_chosetypes,
]


def register_opts():
    for c in cls:
        bpy.utils.register_class(c)


def unregister_opts():
    for c in reversed(cls):
        bpy.utils.unregister_class(c)
