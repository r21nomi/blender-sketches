import bpy, bmesh
import noise
import sys
from math import tau, sin

print(sys.path)

totalFrame = 100
theta = 0.0

# Delete existing objects
for obj in bpy.data.objects:
    if obj.type == "MESH":
        bpy.data.objects.remove(obj)

for i in range(0, 1):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, size=1, x_segments=10, y_segments=10)
    mesh_data = bpy.data.meshes.new(
        "Cube ({0}, {1}, {2})".format(0, 0, 0)
    )

    # for index, v in enumerate(bm.verts):
    #     n = noise.snoise2(index, index)
    #     if index % 2 == 0:
    #         v.co += (n * 0.5 * v.normal)

    bm.to_mesh(mesh_data)
    bm.free()

    # Material
    mat = bpy.data.materials.new(
        name="Material"
    )
    rgba = (0.1, 0.1, 0.8, 1.0)
    mat.diffuse_color = rgba
    mesh_data.materials.append(mat)

    mesh_obj = bpy.data.objects.new(mesh_data.name, mesh_data)
    mesh_obj.location = (0, 0, 0.5)

    # Animation
    for frame in range(0, totalFrame):
        bpy.context.scene.frame_set(frame)

        for index, v in enumerate(mesh_data.vertices):
            n = noise.snoise2(index, index)
            if index % 2 == 0:
                # animate only z-axis
                v.co[2] = (sin(theta + n * 10) * 0.3 * v.normal[2])
                v.keyframe_insert(data_path="co")
        theta += tau / totalFrame
        print(theta)

    bpy.context.collection.objects.link(mesh_obj)