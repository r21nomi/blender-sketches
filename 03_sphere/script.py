import bpy
from math import cos, sin, sqrt, pi, tau
import bmesh
import colorsys

x_center = 0.0
y_center = 0.0
z_center = 0.0
scale = 8.0

sz_max = sqrt(2.0) * 6.0 / scale
sz_min = sz_max / 16.0

latitude = 16
longitude = latitude * 2

inv_latitude = 1.0 / (latitude - 1)
inv_longitude = 1.0 / (longitude - 1)

gamma = 2.2

lat_lon = latitude * longitude
grid_range = range(0, lat_lon, 1)
for n in grid_range:
    i = n // longitude
    j = n % longitude

    i_prc = i * inv_latitude
    inclination = pi * (i + 1) * inv_latitude
    sin_incl = sin(inclination)
    cos_incl = cos(inclination)

    incl_fac = abs(sin_incl)
    sz_cube = (1.0 - incl_fac) * sz_min + incl_fac * sz_max

    j_prc = j * inv_longitude
    azimuth = tau * j / longitude
    sin_azim = sin(azimuth)
    cos_azim = cos(azimuth)

    x = sin_incl * cos_azim * scale
    y = sin_incl * sin_azim * scale
    z = cos_incl * scale

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=sz_cube)
    mesh_data = bpy.data.meshes.new(
        "Cube ({0:0>2d}, {1:0>2d})".format(i, j)
    )
    bm.to_mesh(mesh_data)
    bm.free()

    mat = bpy.data.materials.new(
        name="Material ({0:0>2d}, {1:0>2d})".format(i, j)
    )
    rgb = colorsys.hsv_to_rgb(j_prc, 1.0 - i_prc, 1.0)
    rgba = (rgb[0] ** gamma, rgb[1] ** gamma, rgb[2] ** gamma, 1.0)
    mat.diffuse_color = rgba
    mesh_data.materials.append(mat)

    mesh_obj = bpy.data.objects.new(mesh_data.name, mesh_data)
    mesh_obj.location = (x, y, z)
    mesh_obj.rotation_euler = (0.0, inclination, azimuth)

    bpy.context.collection.objects.link(mesh_obj)