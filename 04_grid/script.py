import bmesh
import bpy

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
padding = 0.025
itemSize = (totalGridSize / count) - padding

xCenter = 0.0
yCenter = 0.0

# Create new objects
for n in grid_range:
    x = n % count
    y = n // count
    posX = -gridSize + totalGridSize * invCount * x + xCenter
    posY = -gridSize + totalGridSize * invCount * y + yCenter

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=itemSize)
    mesh_data = bpy.data.meshes.new(
        "Cube ({0}, {1}, {2})".format(x, y, 0)
    )
    bm.to_mesh(mesh_data)
    bm.free()

    mesh_obj = bpy.data.objects.new(mesh_data.name, mesh_data)
    # Location of each cube
    mesh_obj.location = (posX, posY, 0)

    bpy.context.collection.objects.link(mesh_obj)