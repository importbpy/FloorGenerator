# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Floor Generator",
    "author" : "Marek Moravec, based on the Floorboard Generator addon from Michael Anders (varkenvarken) with contributions from Alain, Floric ,Lell",
    "description" : "Generates floors",
    "version" : (0, 1),
    "blender" : (2, 80, 0),
    "location" : "3D View -> N Panel -> Floor Gen",
    "warning" : "This version is early alpha. Use it just for testing!",
    "category" : "Generic"
}

import bpy
from bpy.props import PointerProperty

from . import auto_load
from .operators import menu_func
from .properties import FloorGenSettings

auto_load.init()



def register():
    auto_load.register()
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Object.floorgen_settings = bpy.props.PointerProperty(
            type=FloorGenSettings
            )

def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    auto_load.unregister()
    del bpy.types.Object.floorgen_settings