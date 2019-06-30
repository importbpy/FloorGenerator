import bpy
from mathutils import Vector
from random import uniform, seed

"""Creates a list of vertices and list of faces for a single tile"""
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
    def calc_tmp_offset(size, offset, tile, gap, center):
        if center:
            tiles_count = int((size - gap)//(gap + tile)) - 1
            offset_tmp = (size - gap 
                - tiles_count*(gap + tile))/2 + gap
            return offset_tmp
        offset_tmp = offset - ((offset)//(tile+gap))\
            *(tile+gap)
        return offset_tmp

    offset_x_tmp = calc_tmp_offset(size_x, offset_x, 
                                    tile_x, gap_x, settings.center_x)
    offset_y_tmp = calc_tmp_offset(size_y, offset_y, 
                                    tile_y, gap_y, settings.center_y)
    
    """Calculate the size and eventually the origin of the next tile"""
    def calc_tile_size_origin(id, size, origin, tile_origin,
                            offset_tmp, tile, gap):
        if id==0 and offset_tmp > gap: # first small tile
            tile_tmp = offset_tmp - gap
            if tile_tmp > size:
                tile_tmp = size
            return tile_tmp, tile_origin

        if id==0 and offset_tmp <= gap: # starting with gap
            tile_origin += offset_tmp
            tile_tmp = tile
            if tile_tmp > size:
                tile_tmp = size - offset_tmp
            return tile_tmp, tile_origin
        
        if tile_origin + tile > size + origin: # last tile
            tile_tmp = size + origin - tile_origin
            return tile_tmp, tile_origin
        
        tile_tmp = tile
        return tile_tmp, tile_origin


    """Generate rows"""
    tile_origin_y = origin_y # tile origin x
    index = 0 # face index
    row_id = 0 # row counter
    while True:
        tile_y_tmp, tile_origin_y = calc_tile_size_origin(row_id, size_y, 
                                origin_y, tile_origin_y,
                                offset_y_tmp, tile_y, gap_y)
        if settings.offset_x_random: # random offset of each row
            offset_x_tmp = uniform(0, tile_x + gap_x)
        
        if tile_origin_y >= size_y + origin_y:
            break

        """Generate tiles in the row"""
        tile_origin_x = origin_x # tile origin x
        tile_id = 0 # tile counter (per row)
        while True:
            tile_x_tmp, tile_origin_x = calc_tile_size_origin(
                                tile_id, size_x, 
                                origin_x, tile_origin_x,
                                offset_x_tmp, tile_x, gap_x)

            if tile_origin_x >= size_x + origin_x:
                break

            tile_verts, tile_faces = tile(tile_origin_x, tile_origin_y, 
                                            tile_x_tmp, tile_y_tmp, 
                                            index)
            verts.extend(tile_verts)
            faces.extend(tile_faces)
            tile_origin_x += tile_x_tmp + gap_x
            index += 4
            tile_id += 1
        
        tile_origin_y += tile_y_tmp +gap_y
        row_id += 1

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

    