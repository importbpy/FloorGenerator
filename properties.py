import bpy

class FloorGenSettings(bpy.types.PropertyGroup):
    width = bpy.props.FloatProperty(
        name="Floor Size X",
        description="Width (X) of the floor in Blender units",
        default="4.0"
    )
    length = bpy.props.FloatProperty(
        name="Floor Size Y",
        description="Length (Y) of the floor in Blender units",
        default="4.0"
    )

