import bpy

class FloorGenConvert(bpy.types.Operator):
    bl_idname = "mesh.floorgen_convert"
    bl_label = "Convert to Floorobject"

    def invoke(self, context, event):
        object = bpy.context.active_object

        object.floorgen_settings.width = 5
        object.floorgen_settings.length = 3.0
        return {"FINISHED"}

