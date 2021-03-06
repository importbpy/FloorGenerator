import bpy
from bl_operators.presets import AddPresetBase
from bpy.types import Operator, Menu, Panel
from bl_ui.utils import PresetPanel

from .properties import FloorGenSettings

class FLOOR_PT_presets(PresetPanel, Panel):
    bl_label = "Floor Presets"
    preset_subdir = "floorgen"
    preset_operator = "script.execute_preset"
    preset_add_operator = "floor.add_preset"


class FBGPanelMain(bpy.types.Panel):
    """Main panel"""
    bl_idname = "FLOOR_BOARD_GEN_PT_main"
    bl_label = "Main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Floor Gen"
    bl_order = 0
    
    

    @classmethod
    def poll(cls, context):
        return ((context.active_object != None)
            and (context.mode == 'OBJECT'))
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(
            row_major=True, 
            columns=0,
            even_columns=True, 
            even_rows=False, 
            align=False
            )
        
        active_obj = bpy.context.active_object

        if 'floorgen_settings' not in active_obj:
            layout.operator('mesh.floorgen_convert')
           
        else:
            col = flow.column(align=True)
            col.prop(active_obj.floorgen_settings, 'size_x')
            col.prop(active_obj.floorgen_settings, 'size_y')
          
            col = flow.column(align=True)
            col.prop(active_obj.floorgen_settings, 'proxy')

    

            


class FBGPanelMainOffset(bpy.types.Panel):
    bl_idname = "FLOOR_BOARD_GEN_PT_main_offset"
    # bl_parent_id = "FLOOR_BOARD_GEN_PT_main"
    bl_label = "Origin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Floor Gen"
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return (
            (context.active_object != None)
            and (context.mode == 'OBJECT') 
            and 'floorgen_settings' in bpy.context.active_object
            ) 
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(
            row_major=True, 
            columns=0,
            even_columns=True, 
            even_rows=False, 
            align=False
            )
        
        active_obj = bpy.context.active_object

        col = flow.column(align=True)
        col.prop(active_obj.floorgen_settings, 'origin_x')
        col.prop(active_obj.floorgen_settings, 'origin_y')

class FBGPanelTileSettings(bpy.types.Panel):
    bl_idname = "FLOOR_BOARD_GEN_PT_tile_settings"
    bl_label = "Tile"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Floor Gen"
    bl_order = 3

    def draw_header_preset(self, context):
        FLOOR_PT_presets.draw_panel_header(self.layout)
        
    @classmethod
    def poll(cls, context):
        return (
            (context.active_object != None)
            and (context.mode == 'OBJECT') 
            and 'floorgen_settings' in bpy.context.active_object
            ) 
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(
            row_major=True, 
            columns=0,
            even_columns=True, 
            even_rows=False, 
            align=False
            )
        
        active_obj = bpy.context.active_object
        settings = active_obj.floorgen_settings
    
        col = flow.column(align=True)
        col.prop(active_obj.floorgen_settings, 'tile_x')
        col.prop(active_obj.floorgen_settings, 'tile_y')
        
        col = flow.column(align=True)
        col.prop(active_obj.floorgen_settings, 'gap_x')
        col.prop(active_obj.floorgen_settings, 'gap_y')

        col = flow.column(align=True)
        if settings.proxy:   
            col.enabled = False
        col.prop(active_obj.floorgen_settings, 'thickness')

        col = flow.column(align=True)
        if settings.proxy:   
            col.enabled = False
        col.prop(active_obj.floorgen_settings, 'bevel_width')

class FBGPanelGridSettings(bpy.types.Panel):
    bl_idname = "FLOOR_BOARD_GEN_PT_grid_settings"
    bl_label = "Grid"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Floor Gen"
    bl_order = 4

    @classmethod
    def poll(cls, context):
        return (
            (context.active_object != None)
            and (context.mode == 'OBJECT') 
            and 'floorgen_settings' in bpy.context.active_object
            ) 
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(
            row_major=True, 
            columns=0,
            even_columns=True, 
            even_rows=False, 
            align=False
            )
        
        active_obj = bpy.context.active_object
        settings = active_obj.floorgen_settings

        col = flow.column(align=True)
        col.prop(active_obj.floorgen_settings, 'offset_x_random')
        col = flow.column(align=True)
        if not settings.offset_x_random:   
            col.enabled = False
        col.prop(active_obj.floorgen_settings, 'random_seed')

        col = flow.column(align=True)
        col.prop(active_obj.floorgen_settings, 'center_x')
        if settings.offset_x_random:   
            col.enabled = False
        col = flow.column(align=True)
        if settings.center_x or settings.offset_x_random:   
            col.enabled = False
        col.prop(active_obj.floorgen_settings, 'offset_x')

        col = flow.column(align=True)
        col.prop(active_obj.floorgen_settings, 'center_y')
        col = flow.column(align=True)
        if settings.center_y:   
            col.enabled = False
        col.prop(active_obj.floorgen_settings, 'offset_y')

class OT_FloorGenPreset(AddPresetBase, Operator):
    bl_idname = 'floor.add_preset'
    bl_label = 'Add Floor Preset'
    preset_menu = 'OBJECT_MT_floor_presets'  

    preset_defines = [
        'settings = bpy.context.active_object.floorgen_settings'
    ]  

    preset_values = [
        'settings.tile_x',
        'settings.tile_y',
        'settings.gap_x',
        'settings.gap_y',
        'settings.thickness',
        'settings.bevel_width'
    ]

    preset_subdir = 'floorgen'

class MT_FloorPresets(Menu): 
    bl_idname = "OBJECT_MT_floor_presets"
    bl_label = 'Floor Presets' 
    preset_subdir = 'floorgen' 
    preset_operator = 'script.execute_preset' 
    draw = Menu.draw_preset