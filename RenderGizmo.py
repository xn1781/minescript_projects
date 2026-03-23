ARGB = JavaClass("net.minecraft.util.ARGB")

Vec3 = JavaClass("net.minecraft.world.phys.Vec3")
AABB = JavaClass("net.minecraft.world.phys.AABB")
BlockPos = JavaClass("net.minecraft.core.BlockPos")

Direction = JavaClass("net.minecraft.core.Direction")

Gizmos = JavaClass("net.minecraft.gizmos.Gizmos")
GizmoStyle = JavaClass("net.minecraft.gizmos.GizmoStyle")

# its annoying that i cant just do Gizmos[drawMethod] omfg
# gizmoDrawMethod = {
#     "blocks": "cuboid",
#     "circles": "circle",
#     "lines": "line",
#     "arrows": "arrow",
#     "plane": "rect",
#     "rect": "rect",
#     "point": "point"
# }

# THIS CODE IS BUNS
def drawGizmo(gizmoType, activeGizmo):
    if gizmoType == "blocks":
        return Gizmos.cuboid(*activeGizmo[:-3])
    elif gizmoType == "circles":
        return Gizmos.circle(*activeGizmo[:-3])
    elif gizmoType == "lines":
        return Gizmos.line(*activeGizmo[:-3])
    elif gizmoType == "arrows":
        return Gizmos.arrow(*activeGizmo[:-3])
    elif gizmoType == "plane":
        return Gizmos.rect(*activeGizmo[:-3])
    elif gizmoType == "rect":
        return Gizmos.rect(*activeGizmo[:-3])
    elif gizmoType == "point":
        return Gizmos.point(*activeGizmo[:-3])

class renderGizmo:
    def __init__(self):
        self.activeGizmos = {
            "blocks": {},
            "circles": {},
            "lines": {},
            "arrows": {},
            "plane": {},
            "rect": {},
            "point": {}
        }

        self.gizmoIds = {
            "blocks": 0,
            "circles": 0,
            "lines": 0,
            "arrows": 0,
            "plane": 0,
            "rect": 0,
            "point": 0
        }

    def _makeJavaAABB(self, data): 
        """INTERNAL"""
        dataLength = len(data)
        # wouldve used map() or 'int(pos) for pos in data' but it doesnt work in pyjinn scripts
        if dataLength == 3:
            return AABB(BlockPos(int(data[0]), int(data[1]), int(data[2])))
        if dataLength == 6:
            return AABB(float(data[0]), float(data[1]), float(data[2]),
                        float(data[3]), float(data[4]), float(data[5]))

    def _makeJavaStyle(self, s: list):
        """INTERNAL"""
        stype = str(s[0])
        color = int(s[1])
        width = float(s[2])
        
        if stype == "stroke":
            return GizmoStyle.stroke(color, width)
        elif stype == "fill":
            return GizmoStyle.fill(color)
        else:
            return GizmoStyle.strokeAndFill(color, width, int(s[3]))

    def _makeJavaPos(self, pos):
        """INTERNAL"""
        return Vec3(*pos)
    
    def _makeJavaFace(self, face):
        """INTERNAL"""
        # return Direction[face] whyyyy
        if face == "UP":
            return Direction.UP
        elif face == "DOWN":
            return Direction.DOWN
        elif face == "NORTH":
            return Direction.NORTH
        elif face == "SOUTH":
            return Direction.SOUTH
        elif face == "WEST":
            return Direction.WEST
        elif face == "EAST":
            return Direction.EAST

    def _addGizmo(self, gizmoType, data):
        """INTERNAL"""
        current_id = str(self.gizmoIds[gizmoType])
        self.activeGizmos[gizmoType][current_id] = data
        self.gizmoIds[gizmoType] += 1
        return current_id
    
    def deleteGizmo(self, gizmoType, gizmoId):
        """Deletes an active Gizmo object"""
        gizmoDict = self.activeGizmos.get(gizmoType)
        if gizmoDict != None and gizmoDict.get(gizmoId):
            del gizmoDict[gizmoId]

    def newBlock(self, aabb, style, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaAABB, javaStyle = self._makeJavaAABB(aabb), self._makeJavaStyle(style)
        return self._addGizmo("blocks", [javaAABB, javaStyle, alwaysOnTop, persistInMilliseconds, fadeOut])
    
    def newCircle(self, pos, radius, style, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaPos, javaStyle = self._makeJavaPos(pos), self._makeJavaStyle(style)
        return self._addGizmo("circles", [javaPos, radius, javaStyle, alwaysOnTop, persistInMilliseconds, fadeOut])
    
    def newLine(self, pos1, pos2, argb, width, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaPos1, javaPos2 = self._makeJavaPos(pos1), self._makeJavaPos(pos2)
        return self._addGizmo("lines", [javaPos1, javaPos2, argb, width, alwaysOnTop, persistInMilliseconds, fadeOut])
    
    def newArrow(self, pos1, pos2, argb, width, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaPos1, javaPos2 = self._makeJavaPos(pos1), self._makeJavaPos(pos2)
        return self._addGizmo("arrows", [javaPos1, javaPos2, argb, width, alwaysOnTop, persistInMilliseconds, fadeOut])

    def newPlane(self, pos1, pos2, face, style, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaPos1, javaPos2, javaFace, javaStyle = self._makeJavaPos(pos1), self._makeJavaPos(pos2), self._makeJavaFace(face), self._makeJavaStyle(style)
        return self._addGizmo("plane", [javaPos1, javaPos2, javaFace, javaStyle, alwaysOnTop, persistInMilliseconds, fadeOut])
    
    def newRect(self, pos1, pos2, pos3, pos4, style, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaPos1, javaPos2, javaPos3, javaPos4, javaStyle = self._makeJavaPos(pos1), self._makeJavaPos(pos2), self._makeJavaPos(pos3), self._makeJavaPos(pos4), self._makeJavaStyle(style)
        return self._addGizmo("rect", [javaPos1, javaPos2, javaPos3, javaPos4, javaStyle, alwaysOnTop, persistInMilliseconds, fadeOut])
    
    def newPoint(self, pos, argb, size, alwaysOnTop=True, persistInMilliseconds=None, fadeOut=False):
        javaPos = self._makeJavaPos(pos)
        return self._addGizmo("point", [javaPos, argb, size, alwaysOnTop, persistInMilliseconds, fadeOut])


RenderGizmo = renderGizmo()

def applyProperties(gizmo, activeGizmo, activeGizmos, gizmoId):
    if activeGizmo[-3]:
        gizmo.setAlwaysOnTop()
    if activeGizmo[-2]:
        gizmo.persistForMillis(activeGizmo[-2])
        
        if activeGizmo[-1]:
            gizmo.fadeOut()
            
        del activeGizmos[gizmoId]

def onRender(event):
    for gizmoType, activeGizmos in RenderGizmo.activeGizmos.items():
        for gizmoId, activeGizmo in activeGizmos.items():
            gizmo = drawGizmo(gizmoType, activeGizmo)
            applyProperties(gizmo, activeGizmo, activeGizmos, gizmoId)

add_event_listener("render", onRender)
