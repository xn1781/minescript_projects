# very unoptimized!

import system.lib.minescript as m
import system.lib.java as java
import time

m.set_default_executor(m.script_loop)

script = java.eval_pyjinn_script(r"""
Minecraft = JavaClass("net.minecraft.client.Minecraft")
ShapeRenderer = JavaClass("net.minecraft.client.renderer.ShapeRenderer")
PoseStack = JavaClass("com.mojang.blaze3d.vertex.PoseStack")
Shapes = JavaClass("net.minecraft.world.phys.shapes.Shapes")

RenderPipelines = JavaClass("net.minecraft.client.renderer.RenderPipelines")
RenderPipeline = JavaClass("com.mojang.blaze3d.pipeline.RenderPipeline")
Builder = JavaClass("com.mojang.blaze3d.pipeline.RenderPipeline$Builder")
Snippet = JavaClass("com.mojang.blaze3d.pipeline.RenderPipeline$Snippet")
RenderType = JavaClass("net.minecraft.client.renderer.rendertype.RenderType")
RenderSetup = JavaClass("net.minecraft.client.renderer.rendertype.RenderSetup")
RenderSetupBuilder = JavaClass("net.minecraft.client.renderer.rendertype.RenderSetup$RenderSetupBuilder")
LayeringTransform = JavaClass("net.minecraft.client.renderer.rendertype.LayeringTransform")

DepthTestFunction = JavaClass("com.mojang.blaze3d.platform.DepthTestFunction")
DefaultVertexFormat = JavaClass("com.mojang.blaze3d.vertex.DefaultVertexFormat")
VertexFormatMode = JavaClass("com.mojang.blaze3d.vertex.VertexFormat$Mode")
BlendFunction = JavaClass("com.mojang.blaze3d.pipeline.BlendFunction")
UniformType = JavaClass("com.mojang.blaze3d.shaders.UniformType")

# make lines with no depth (basically renders through walls)
# we cannot call builders directly otherwise it will error
def builder(*snippets):
    builder_instance = Builder()

    for snippet in snippets:
        builder_instance.withSnippet(snippet)

    return builder_instance

def renderSetupBuilder(pipeline):
    return RenderSetupBuilder(pipeline)

MATRICES_PROJECTION_SNIPPET = builder() \
    .withUniform("DynamicTransforms", UniformType.UNIFORM_BUFFER) \
    .withUniform("Projection", UniformType.UNIFORM_BUFFER) \
    .buildSnippet(); \
FOG_SNIPPET = builder().withUniform("Fog", UniformType.UNIFORM_BUFFER).buildSnippet()
GLOBALS_SNIPPET = builder().withUniform("Globals", UniformType.UNIFORM_BUFFER).buildSnippet()
MATRICES_FOG_SNIPPET = builder(MATRICES_PROJECTION_SNIPPET, FOG_SNIPPET).buildSnippet()
LineSnippet = builder(MATRICES_FOG_SNIPPET, GLOBALS_SNIPPET) \
    .withVertexShader("core/rendertype_lines") \
    .withFragmentShader("core/rendertype_lines") \
    .withBlend(BlendFunction.TRANSLUCENT) \
    .withCull(False) \
    .withVertexFormat(DefaultVertexFormat.POSITION_COLOR_NORMAL_LINE_WIDTH, VertexFormatMode.LINES) \
    .buildSnippet();
LINES_NO_DEPTH = builder(LineSnippet) \
    .withDepthTestFunction(DepthTestFunction.NO_DEPTH_TEST) \
    .withDepthWrite(False) \
    .withLocation("pipeline/lines_no_depth_custom") \
    .build()

LINES_NO_DEPTH_RT = RenderType.create(
    "lines_no_depth_custom",
    renderSetupBuilder(LINES_NO_DEPTH) \
    .setLayeringTransform(LayeringTransform.VIEW_OFFSET_Z_LAYERING) \
    .createRenderSetup()
)

def getRenderDistance() -> int:
    return Minecraft.getInstance().options.method_42503().method_41753()

shared_ores = []

def on_render(event):
    if not shared_ores: return
    mc = Minecraft.getInstance()
    source = mc.field_1769.field_20951.method_23000()
    builder = source.getBuffer(LINES_NO_DEPTH_RT)
    poseStack = PoseStack()
    shape = Shapes.method_1077()
    pos = mc.field_1773.mainCamera.position()
    cx, cy, cz = float(pos.x), float(pos.y), float(pos.z)
    for data in shared_ores:
        rx = float(data[0]) - cx
        ry = float(data[1]) - cy
        rz = float(data[2]) - cz
        ShapeRenderer.method_62296(poseStack, builder, shape, rx, ry, rz, int(data[3]), 2.0)
    source.method_37104()

# bind this to minescript's render event
add_event_listener("render", on_render)
""")


def toARGB(r, g, b, a=1):
    alpha = max(0, min(int(a * 255 + 0.5), 255))
    red   = max(0, min(int(r * 255 + 0.5), 255))
    green = max(0, min(int(g * 255 + 0.5), 255))
    blue  = max(0, min(int(b * 255 + 0.5), 255))
    value = (alpha << 24) | (red << 16) | (green << 8) | blue
    if value > 0x7FFFFFFF: value -= 0x100000000
    return value

ores = {
    "minecraft:diamond_ore": toARGB(0, 255, 255, 1),
    "minecraft:emerald_ore": toARGB(0, 255, 0, 1),
    "minecraft:lapis_ore": toARGB(0, 0, 255, 1),
    "minecraft:redstone_ore": toARGB(255, 25, 0, 1),
    "minecraft:gold_ore": toARGB(255, 213, 0, 1),
    "minecraft:copper_ore": toARGB(255, 121, 43, 1),
    "minecraft:iron_ore": toARGB(50, 50, 50, 1),
    "minecraft:coal_ore": toARGB(0, 0, 0, 1),
    "minecraft:deepslate_diamond_ore": toARGB(0, 255, 255, 1),
    "minecraft:deepslate_emerald_ore": toARGB(0, 255, 0, 1),
    "minecraft:deepslate_lapis_ore": toARGB(0, 0, 255, 1),
    "minecraft:deepslate_redstone_ore": toARGB(255, 25, 0, 1),
    "minecraft:deepslate_gold_ore": toARGB(255, 213, 0, 1),
    "minecraft:deepslate_copper_ore": toARGB(255, 121, 43, 1),
    "minecraft:deepslate_iron_ore": toARGB(50, 50, 50, 1),
    "minecraft:deepslate_coal_ore": toARGB(0, 0, 0, 1),
    "minecraft:ancient_debris": toARGB(102, 59, 55, 1),
}

getRenderDistance = script.get("getRenderDistance")

while True:
    px, py, pz = [round(axis) for axis in m.player_position()]
    renderDistance = getRenderDistance() # will fix this later

    firstCorner = (px + renderDistance, py + renderDistance, pz + renderDistance)
    secondCorner = (px - renderDistance, py - renderDistance, pz - renderDistance)
    blockRegion = m.get_block_region(firstCorner, secondCorner, safety_limit=True)

    to_draw = []

    for x in range(blockRegion.min_pos[0], blockRegion.max_pos[0] + 1):
        for y in range(blockRegion.min_pos[1], blockRegion.max_pos[1] + 1):
            for z in range(blockRegion.min_pos[2], blockRegion.max_pos[2] + 1):
                block = blockRegion.get_block(x, y, z)
                if block in ores:
                    to_draw.append((float(x), float(y), float(z), ores[block]))

    script.set("shared_ores", to_draw)
    time.sleep(0.1)
