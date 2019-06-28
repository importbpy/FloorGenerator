import bpy
from mathutils import Vector
from random import uniform, seed

def tile(origin_x, origin_y, tile_x, tile_y, index):
    verts = [
        (origin_x, origin_y, 0),
        (origin_x+tile_x, origin_y, 0),
        (origin_x+tile_x, origin_y+tile_y, 0),
        (origin_x, origin_y+tile_y, 0),
        ]
    faces = [[0+index, 1+index, 2+index, 3+index]]
    return verts, faces



def tiles(
    size_x, size_y, 
    origin_x, origin_y, 
    offset_x, offset_y,
    tile_x, tile_y, 
    gap_x, gap_y):
    verts = []
    faces = []
    settings = bpy.context.active_object.floorgen_settings

    seed(settings.random_seed) # set the random seed

    """Calculate the real (normalized) value of the offset"""
    if settings.center_x:
        tiles_count_x = int((size_x - gap_x)//(gap_x + tile_x)) - 1
        offset_x_tmp = (size_x - gap_x 
            - tiles_count_x*(gap_x + tile_x))/2 + gap_x
    else:
        offset_x_tmp = offset_x - ((offset_x)//(tile_x+gap_x))\
            *(tile_x+gap_x)
    
    if settings.center_y:
        tiles_count_y = int((size_y - gap_y)//(gap_y + tile_y)) - 1
        offset_y_tmp = (size_y - gap_y - tiles_count_y
            *(gap_y + tile_y))/2 + gap_y
    else:
        offset_y_tmp = offset_y - ((offset_y)//(tile_y+gap_y))\
            *(tile_y+gap_y)

    """Generate rows"""
    to_y = origin_y # tile origin x
    index = 0 # face index
    c = 0 # counter
    while True:
        """Define the Y dimension of a tile"""
        if c==0 and offset_y_tmp > gap_y: # first small tile
            tile_y_tmp = offset_y_tmp - gap_y
            if tile_y_tmp > size_y:
                tile_y_tmp = size_y

        elif c==0 and offset_y_tmp <= gap_y: # starting with gap
            to_y += offset_y_tmp
            tile_y_tmp = tile_y
            if tile_y_tmp > size_y:
                tile_y_tmp = size_y - offset_y_tmp
        elif to_y + tile_y > size_y + origin_y: # last tile
            tile_y_tmp = size_y + origin_y - to_y
        else: # full size tile
            tile_y_tmp = tile_y
        
        

        if to_y >= size_y + origin_y:
            break

        """Generate single row"""
        if settings.offset_x_random: # random offset of each row
            offset_x_tmp = uniform(0, tile_x + gap_x)
        to_x = origin_x # tile origin x
        i = 0 # counter
        while True:
            """Define the X dimension of a tile"""
            if i==0 and offset_x_tmp > gap_x: # first small tile
                tile_x_tmp = offset_x_tmp - gap_x
                if tile_x_tmp > size_x:
                    tile_x_tmp = size_x
            elif i==0 and offset_x_tmp <= gap_x: # starting with gap
                to_x += offset_x_tmp
                tile_x_tmp = tile_x
                if tile_x_tmp > size_x:
                    tile_x_tmp = size_x - offset_x_tmp
            elif to_x + tile_x > size_x + origin_x: # last tile
                tile_x_tmp = size_x + origin_x - to_x
            else: # full size tile
                tile_x_tmp = tile_x

            if to_x >= size_x + origin_x:
                break

            tile_verts, tile_faces = tile(to_x, to_y, tile_x_tmp, 
                                            tile_y_tmp, index)
            verts.extend(tile_verts)
            faces.extend(tile_faces)
            to_x += tile_x_tmp + gap_x
            index += 4
            i += 1
        to_y += tile_y_tmp +gap_y
        c += 1

    return verts, faces

def regen_modifiers(self, context):
    active_obj = bpy.context.active_object
    settings = active_obj.floorgen_settings
        
    active_obj.modifiers["Solidify"].thickness = settings.thickness
    active_obj.modifiers["Bevel"].width = settings.bevel_width
    active_obj.modifiers["Bevel"].segments = 2
    active_obj.modifiers["Bevel"].limit_method = 'ANGLE'
    active_obj.modifiers["Bevel"].harden_normals = True
    active_obj.modifiers["Bevel"].use_clamp_overlap = False

def regen(self, context):
    active_obj = bpy.context.active_object
    settings = active_obj.floorgen_settings
    
    verts, faces = tiles(settings.size_x, settings.size_y,
                             settings.origin_x, settings.origin_y,
                             settings.offset_x, settings.offset_y,
                             settings.tile_x, settings.tile_y,
                             settings.gap_x, settings.gap_y)
    mesh = bpy.data.meshes.new(name='Floor')
    mesh.from_pydata(verts, [], faces)

    mesh.update(calc_edges=True)
    
    active_obj.data = mesh
    active_obj.data.use_auto_smooth = True
    # add a solidify modifier if there is not one
    

    if settings.proxy:
        active_obj.modifiers.clear()    
    else:
        if not active_obj.modifiers:
            solidify = active_obj.modifiers.new(name="Solidify", type="SOLIDIFY")
            bevel = active_obj.modifiers.new(name="Bevel", type="BEVEL")
        regen_modifiers(None, None)

    