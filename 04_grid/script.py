import bmesh
import bpy
from math import sin, cos, tau, pi, pow, sqrt

# Delete existing objects
for obj in bpy.data.objects:
    if obj.type == "MESH":
        bpy.data.objects.remove(obj)

count = 9
count_sq = count * count
grid_range = range(0, count_sq)

# Size of on grid
# ■□
# □□
gridSize = 2.0

# Size of total grid
# ■■
# ■■
totalGridSize = gridSize + gridSize

invCount = 1.0 / (count - 1.0)
padding = 0.0
itemSize = (totalGridSize / count) - padding

xCenter = 0.0
yCenter = 0.0

totalFrame = 100
theta = 0.0

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = totalFrame


def lerp(a, b, t):
    return (1.0 - t) * a + b * t

def map(value, beforeMin, beforeMax, afterMin, afterMax):
    return afterMin + (afterMax - afterMin) * ((value - beforeMin) / (beforeMax - beforeMin))

def ease_out_expo(x):
    t = x
    b = 0.0
    c = 1.0
    d = 1.0
    if t == d:
        return b + c
    else:
        return c * (-pow(2.0, -10.0 * t / d) + 1.0) + b


# Create new objects
for n in grid_range:
    x = n % count
    y = n // count
    posX = -gridSize + totalGridSize * invCount * x + xCenter
    posY = -gridSize + totalGridSize * invCount * y + yCenter

    d = sqrt(pow(posX, 2) + pow(posY, 2))

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=itemSize)
    mesh_data = bpy.data.meshes.new(
        "Cube ({0}, {1}, {2})".format(x, y, 0)
    )
    bm.to_mesh(mesh_data)
    bm.free()

    # Material
    mat = bpy.data.materials.new(
        name="Material ({0}, {1}, {2})".format(x, y, 0)
    )
    mat.diffuse_color = (1.0, 1.0, 0.0, 1.0)
    mesh_data.materials.append(mat)

    mesh_obj = bpy.data.objects.new(mesh_data.name, mesh_data)
    # Location of each cube
    mesh_obj.location = (posX, posY, 0)

    # Animation
    for frame in range(0, totalFrame):
        bpy.context.scene.frame_set(frame)
        e = ease_out_expo(map(sin(theta + d), -1, 1, 0, 1))
        mesh_obj.location.z = e * 0.6
        mesh_obj.keyframe_insert(data_path="location")
        mesh_obj.scale = ((1 - e), (1 - e), e)
        mesh_obj.keyframe_insert(data_path="scale")
        theta += tau / totalFrame

    bpy.context.collection.objects.link(mesh_obj)
