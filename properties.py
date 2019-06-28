import bpy
from bpy.types import PropertyGroup
from bpy.props import FloatProperty, BoolProperty, IntProperty

from .functions import regen, regen_modifiers

class FloorGenSettings(bpy.types.PropertyGroup):
    floorobject: bpy.props.BoolProperty(
        name="Is floor object", 
        description="Determines whether the object is an floor object", 
        default=False,
        update=regen
        )
    size_x: bpy.props.FloatProperty(
        name="Floor Size X",
        description="Width (X) of the floor in Blender units", 
        default=1.0,
        min = 0.0,
        soft_min = 0.1,
        update=regen
        )
    size_y: bpy.props.FloatProperty(
        name="Y", 
        description="Length (Y) of the floor in Blender units", 
        default=1.0,
        min = 0.0,
        soft_min = 0.1,
        update=regen
        )
    origin_x: bpy.props.FloatProperty(
        name="Origin X",
        default=0.0,
        update=regen
        )
    origin_y: bpy.props.FloatProperty(
        name="Y",
        default=0.0,
        update=regen
        )
    offset_x: bpy.props.FloatProperty(
        name="Grid Offset X",
        default=0.0,
        min = 0.0,
        update=regen
        )
    offset_y: bpy.props.FloatProperty(
        name="Grid Offset Y",
        default=0.0,
        min = 0.0,
        update=regen
        ) 
    center_x: bpy.props.BoolProperty(
        name="Center X", 
        description="Make the tiles centered in X direction", 
        default=False,
        update=regen
        )
    center_y: bpy.props.BoolProperty(
        name="Center Y", 
        description="Make the tiles centered in Y direction", 
        default=False,
        update=regen
        )
    tile_x: bpy.props.FloatProperty(
        name="Size X",
        default=0.6,
        min = 0.01,
        soft_min = 0.1,
        update=regen
        )
    tile_y: bpy.props.FloatProperty(
        name="Y",
        default=0.3,
        min = 0.01,
        soft_min = 0.1,
        update=regen
        )
    gap_x: bpy.props.FloatProperty(
        name="Gap X",
        default=0.005,
        min = 0.0,
        step=0.1,
        precision=3,
        update=regen
        )
    gap_y: bpy.props.FloatProperty(
        name="Y",
        default=0.005,
        min = 0.0,
        step=0.1,
        precision=3,
        update=regen
        )
    thickness: bpy.props.FloatProperty(
        name="Thickness",
        default=0.01,
        step=0.1,
        precision=3,
        update=regen_modifiers
        )  
    bevel_width: bpy.props.FloatProperty(
        name="Bevel amount",
        default=0.002,
        step=0.01,
        precision=4,
        update=regen_modifiers
        )      
    proxy: bpy.props.BoolProperty(
        name="Proxy", 
        description="Shows siplified version of the floor make it faster", 
        default=False,
        update=regen
        )
    offset_x_random: bpy.props.BoolProperty(
        name="Random offset", 
        description="Random offset in X direction", 
        default=False,
        update=regen
        )
    random_seed: bpy.props.IntProperty(
        name="Random Seed",
        default=0,
        update=regen
        )      

