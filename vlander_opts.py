# ----------------------------------------------------------
# Author: Daniele Giuliani (notwarp)
#
# ----------------------------------------------------------
from bpy.types import Operator
from bpy.props import (
    BoolProperty, IntProperty
)


class VLANDER_OT_create(Operator):
    bl_idname = "vlander.create"
    bl_label = "Create"
    bl_description = "Create"
    bl_options = {'REGISTER', 'UNDO'}

    is_active: BoolProperty(
        name="activate_vlander",
        description="Vlander Activation",
        default=False
    )

    @classmethod
    def poll(cls, context):
        print('poll operator create')
        return True

    def execute(self, context):
        print('execute operator create')
        self.is_active = True
        self.report({'INFO'}, 'B: %s' % self.is_active)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.report({'INFO'}, 'B: %s' % self.is_active)
        print('invoke operator create')
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
        print('poll operator clean')
        return True

    def invoke(self, context, event):
        print('invoke operator clean')
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
        print('poll operator type')
        return True

    def draw(self, context):
        print('draw operator type')
        layout = self.layout
        layout.template_icon_view(context.space_data.shading,
                                  "studio_light",
                                  show_labels=False,
                                  scale=6.0,
                                  scale_popup=5.0
                                  )

    def execute(self, context):
        print('execute operator type')
        print(context.object.location.x, self.bl_idname)
        return {'FINISHED'}

    def modal(self, context, event):
        print('modal operator type')
        if event.type == 'MOUSEMOVE':  # Apply
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('invoke operator type')
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


cls = [
    VLANDER_OT_create,
    VLANDER_OT_clean,
    VLANDER_OT_chosetypes,
]

import bpy


def register_opts():
    for c in cls:
        bpy.utils.register_class(c)


def unregister_opts():
    for c in reversed(cls):
        bpy.utils.unregister_class(c)
