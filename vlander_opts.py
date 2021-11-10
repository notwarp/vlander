from bpy.types import Operator


class VLANDER_OT_create(Operator):
    bl_idname = "vlander.create"
    bl_label = "Create"
    bl_description = "Create"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        print('poll operator create')
        return True

    def invoke(self, context, event):
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


cls = [
    VLANDER_OT_create,
    VLANDER_OT_clean
]

import bpy


def register_opts():
    for c in cls:
        bpy.utils.register_class(c)


def unregister_opts():
    for c in reversed(cls):
        bpy.utils.unregister_class(c)
