import bpy
from bpy.props import PointerProperty

from .properties import FloorGenSettings

class FloorGenConvert(bpy.types.Operator):
    bl_idname = "mesh.floorgen_convert"
    bl_label = "Convert to Floorobject"

    def invoke(self, context, event):
        
        bpy.types.Object.floorgen_settings = bpy.props.PointerProperty(
            type=FloorGenSettings
            )
        active_obj = bpy.context.active_object
        settings = active_obj.floorgen_settings
        
        # remove all modifiers
        active_obj.modifiers.clear()

        # get the origin of the floor to front left corner of the 
        # bounding box
        origin_x = (active_obj.bound_box[0][0] 
            * active_obj.scale[0])
        origin_y = (active_obj.bound_box[0][1] 
            * active_obj.scale[1])

        # get the dimensions of the original object and change the 
        # scale to 1
        size_x = active_obj.dimensions[0]
        size_y = active_obj.dimensions[1]
        active_obj.scale = [1,1,1]

        # assign the values to the floorgen properties, it must be done
        # at the end, otherwise regen function is called
        settings.origin_x = origin_x
        settings.origin_y = origin_y
        settings.size_x = size_x
        settings.size_y = size_y
        

        # object is converted to floorobject
        settings.floorobject = True
        

        return {"FINISHED"}

