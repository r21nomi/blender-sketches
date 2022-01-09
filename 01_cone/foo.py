import bpy, os, sys, importlib
from math import sin, tau

dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)

import bar
importlib.reload(bar)
print(bar.greeting)

# clear meshs in the scene
for obj in bpy.data.objects:
    if obj.type == "MESH":
        bpy.data.objects.remove(obj)

# animation variables
total_frames = 150
theta = 0.0

# define a one hundle frame timeline
bpy.context.scene.frame_end = total_frames
bpy.context.scene.frame_start = 0

for x in range(30):
    for y in range(30):
        cone = bpy.ops.mesh.primitive_cone_add()
        cone = bpy.context.object
        cone.name = "Cone-{}-{}".format(x, y)
        cone.location[0] = x * 2
        cone.location[1] = y * 2
        # add keyframes to each cone
        for frame in range(0, total_frames):
            bpy.context.scene.frame_set(frame)
            cone.location.z = sin(theta + x) * 2 - 1
            cone.keyframe_insert(data_path="location")
            scale = sin(theta + y)
            cone.scale = (scale, scale, scale)
            cone.keyframe_insert(data_path="scale")
            theta += tau / total_frames