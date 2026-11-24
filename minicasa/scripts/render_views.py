import bpy, sys, os, math
from mathutils import Vector
blend, outdir = sys.argv[sys.argv.index('--')+1:][:2] if '--' in sys.argv else (sys.argv[1], sys.argv[2])
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'TEXTURE'; sh.show_shadows = False; sh.show_cavity = True
sc.render.resolution_x, sc.render.resolution_y = 900, 600
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.lens = 16; cam.data.clip_start = 0.05
views = {
  'exterior': ((4.5, -6.5, 1.8), (0, 1.5, 1.2), 28),
  'entrada': ((0.55, 0.25, 1.6), (0.0, 5.0, 1.2), 14),
  'cocina': ((0.3, 3.9, 1.6), (-0.6, 0.0, 0.9), 14),
  'living': ((-0.4, 1.2, 1.6), (0.9, 4.0, 1.0), 14),
  'bano': ((0.1, 4.55, 1.6), (-0.2, 6.0, 0.8), 12),
  'altillo': ((0.0, 4.6, 2.9), (0.0, 6.0, 2.3), 12),
}
only = sys.argv[sys.argv.index('--')+3:] if '--' in sys.argv and len(sys.argv) > sys.argv.index('--')+3 else list(views)
for name in only:
    loc, tgt, lens = views[name]
    cam.location = loc; cam.data.lens = lens
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(outdir, f'v_{name}.png')
    bpy.ops.render.render(write_still=True)
