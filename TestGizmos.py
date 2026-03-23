import system.lib.minescript as m
import system.lib.java as java

m.set_default_executor(m.script_loop)

ARGB = java.JavaClass("net.minecraft.util.ARGB")
Gizmo = java.import_pyjinn_script("Gizmo.pyj")

white = ARGB.color(255, 255, 255, 255)
red = ARGB.color(255, 255, 0, 0)
green = ARGB.color(255, 0, 255, 0)
blue = ARGB.color(255, 0, 0, 255)
yellow = ARGB.color(255, 255, 255, 0)
cyan = ARGB.color(255, 0, 255, 255)
magenta = ARGB.color(255, 255, 0, 255)

RenderGizmo = Gizmo.get("RenderGizmo")

RenderGizmo.newBlock([0, 0, 0], ["stroke", white, 1], True, None, True)
RenderGizmo.newBlock([5, 0, 0], ["fill", red, 1], True, None, True)
RenderGizmo.newBlock([10, 0, 0], ["strokeAndFill", green, 2, 128], True, None, True)

RenderGizmo.newCircle([0, 5, 0], 15, ["fill", blue, 1], True, None, True)
RenderGizmo.newCircle([0, 10, 0], 10, ["stroke", yellow, 1.5], True, None, True)
RenderGizmo.newCircle([0, 15, 0], 8, ["stroke", cyan, 2], True, None, True)

RenderGizmo.newLine([0, 0, 0], [10, 0, 0], red, 2, True, None, True)
RenderGizmo.newLine([0, 0, 0], [0, 10, 0], green, 2, True, None, True)
RenderGizmo.newLine([0, 0, 0], [0, 0, 10], blue, 2, True, None, True)

RenderGizmo.newArrow([5, 0, 0], [15, 0, 0], yellow, 2, True, None, True)
RenderGizmo.newArrow([0, 5, 0], [0, 15, 0], cyan, 2, True, None, True)
RenderGizmo.newArrow([0, 0, 5], [0, 0, 15], magenta, 2, True, None, True)

RenderGizmo.newPlane([0, 0, 0], [5, 5, 0], "UP", ["fill", white, 1], True, None, True)
RenderGizmo.newPlane([5, 0, 0], [10, 5, 0], "UP", ["stroke", red, 1], True, None, True)

RenderGizmo.newRect([0, 10, 0], [5, 10, 0], [5, 15, 0], [0, 15, 0], ["stroke", green, 1.5], True, None, True)
RenderGizmo.newRect([10, 10, 0], [15, 10, 0], [15, 15, 0], [10, 15, 0], ["fill", blue, 1], True, None, True)

RenderGizmo.newPoint([0, 0, 0], white, 0.5, True, None, True)
RenderGizmo.newPoint([5, 0, 0], red, 0.5, True, None, True)
RenderGizmo.newPoint([0, 5, 0], green, 0.5, True, None, True)
RenderGizmo.newPoint([0, 0, 5], blue, 0.5, True, None, True)

while True:
    pass

