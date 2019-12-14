from dungeon import *
from keys import *
from tiles import *
from level import Level
import math

tileSize = 16

class Level():
    def __init__(self):
        """Creates a dungeon"""
        self.dungeon = Dungeon(100, 100)
        self.dungeon.generate()

        """the current collision map for the dungeon"""
        self.collisionMap = self.dungeon.getCollisionMap()

        """The tiles in the map"""
        self.tiles = self.dungeon.getFlattenedTiles()

        """Basic player object"""
        self.player = {
            pos : {"x" : 0, "y" : 0},
            size : {"x" : 12, "y" : 12},
            speed : 175,
            color : "#0CED13",
            onStairs : True
        }

        """Place the player at the up stair case"""
        stairs = self.dungeon.getStairs()
        self.player.pos.x = stairs.up.x * tileSize / 2 - self.player.size.x / 2
        self.player.pos.y = stairs.up.y * tileSize / 2 - self.player.size.y / 2


    def width():
        return self.dungeon.size.x*tilesize


    def height():
        return self.dungeon.size.y*tileSize
        

    def update(elapsed, keysDown):
        """"handle input to move the player"""
        move = {"x" : 0, "y" : 0}
        if keys.left == keysDown:
            move.x -= self.player.speed * elapsed

        if keys.right == keysDown:
            move.x -= self.player.speed * elapsed

        if keys.up == keysDown:
            move.y -= self.player.speed * elapsed

        if keys.down == keysDown:
            move.y -= self.player.speed * elapsed

        """collide the player against the dungeon"""
        self.player.pos = self.moveEntity(self.player.pos, self.player.size, move)

        """compute the players center"""
        cx = math.floor((self.player.pos.x + self.player.size.x / 2) / tileSize)
        cy = math.floor((self.player.pos.y + self.player.size.y / 2) / tileSize)

        """the return value for the destination. -1 means go up a floor, 1 means go down a floor"""
        dest = 0

        """tracks if the player is on stairs this frame"""
        onStairs = false

        """grab the new current list of rooms"""
        rooms = self.dungeon.roomGrid[cy][cx]
        for i in range(0, rooms.length, 1):
            r = rooms[i]
            
            """"get the player's center in room coordinates"""
            lx = cx - r.pos.x
            ly = cy - r.pos.y

            """if we're on the up stairs, return -1 to indicate we want to move up"""
            if r.tiles[ly][lx] == tiles.stairsUp:
                onStairs = true

                if not self.player.onStairs:
                    dest = -1
                    break
        
            """if we're on the down stairs, return 1 to indicate we want to move down"""
            if r.tiles[ly][lx] == tiles.stairsDown:
                onStairs = true
                
                if not self.player.onStairs:
                    dest = 1
                    break

        """update the player's "onStairs" property"""
        self.player.onStairs = onStairs

        """return our destination"""
        return des

    
    def isTileVisible(visibility, x0, y0, x1, y1):
        """all tiles are visible if we're not doing visibility checks"""
        if visibility == "none":
            return True
        
        """for room mode, just check that we're in the same room as the tile"""
        if visibility == "room":
            rooms = self.dungeon.roomGrid[y0][x0]
            if room != None:
                for i in range(0, rooms.length, 1): 
                    r = rooms[i]
                    if x1 >= r.pos.x & x1 < r.pos.x + r.size.x & y1 >= r.pos.y & y1 < r.pos.y + r.size.y:
                        return True
        
        """if we're using los visibility, we want to do a basic line of sight algorithm"""
        if visibility == "los":
            if x0 < 0 | x0 >= self.dungeon.size.x | x1 < 0 | x1 >= self.dungeon.size.x | y0 < 0 | y0 >= self.dungeon.size.y | y1 < 0 | y1 >= self.dungeon.size.y:
                return True
        
        """get the deltas and steps for both axis"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        """stores an error factor we use to change the axis coordinates"""
        err = dx - dy

        while x0 != x1 | y0 != y1:
            """check our collision map to see if this tile blocks visibility"""
            if self.collisionMap[y0][x0] == 1:
                return false

            """check our error value against our deltas to see if
            we need to move to a new point on either axis"""
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += dy

        """if we're here we hit no occluders and therefore can see this tile"""
        return True


    
    def draw(canvas, context, camera, visibility):
        """compute the player's center in tile space for the tile visibility checks"""
        cx = floor((self.player.pos.x + self.player.size.x / 2) / tileSize)
        cy = floor((self.player.pos.y + self.player.size.y / 2) / tileSize)

        """calculate the base tile coordinates using the camera"""
        baseTileX = floor(camera.x / tileSize) - 1
        baseTileY = floor(camera.y / tileSize) - 1

        """calculating the pixel offset based on the camera"""
        pixelOffsetX = ((camera.x % tileSize) + tileSize) % tileSize
        pixelOffsetY = ((camera.y % tileSize) + tileSize) % tileSize

        """calculate the min and max X/Y values"""
        pixelMinX = -pixelOffsetX - tileSize
        pixelMinY = -pixelOffsetY - tileSize
        pixelMaxX = canvas.width + tileSize - pixelOffsetX
        pixelMaxY = canvas.height + tileSize - pixelOffsetY

        """loop over each row, using both tile coordinates and pixel coordinates"""
        tileY = baseTileY
        for y in range(pixelMinY, pixelMaxY, tileSize):
            tileY += 1
            """verify this row is actually inside the dungeon"""
            if tileY < 0 | tileY >= self.dungeon.size.y:
                continue

            """loop over each column, using both tile coordinates and pixel coordinates"""
            tileX = baseTileX
            for x in range(pixelMinX, pixelMaxX, tileSize):
                tileX += 1
                """verify this column is actually inside the dungeon"""
                if tileX < 0 | tileX >= self.dungeon.size.x:
                    continue

                """get the current tile and make sure it's valid"""
                tile = self.tiles[tileY][tileX]
                if tile != None:
                    """test if the tile is visible"""
                    canBeSeen = self.isTileVisible(visibility, cx, cy, tileX, tileY)

                    """make sure the tile stores a record if it's ever been seen"""
                    if canBeSeen:
                        tile.HasBeenSeen = True

                    """if we have ever seen this tile, we need to draw it"""
                    if tile.HasBeenSeen:
                        """choose the color by the type and whether the tile is currently visible"""
                        if tile.type == tiles.floor:
                            break
                        if tile.type == tiles.door:
                            #context.fillStyle = canBeSeen ? "#B8860B" : "#705104"
                            break
                        if tile.type == tiles.wall:
                            #context.fillStyle = canBeSeen ? "#8B4513" : "#61300D"
                            break
                        if tile.type == tiles.stairsDown:
                            context.fillStyle = "#7A5A0D"
                            break
                        if tile.type == tiles.stairsUp:
                            context.fillStyle = "#F2CD27"
                            break

                    """draw the tile"""
                    context.fillRect(x, y, tileSize, tileSize)

        """draw the player"""
        context.fillStyle = self.player.color
        context.fillRect(floor(self.player.pos.x - camera.x), floor(self.player.pos.y - camera.y), 
        floor(self.player.size.x), floor(self.player.size.y))

    
    def moveEntity(size, move):
        """start with the end goal position"""
        endPos = {
            "x" : pos.x + move.x, 
            "y" : pos.y + move.y
            }

        """check X axis motion for collisions"""
        if move.x:
            """calculate the X tile coordinate where we'd like to be"""
            if move.x > 0:
                offset = size.x
            else:
                offset = 0

            #offset = move.x > 0 ? size.x : 0
            x = floor((pos.x + move.x + offset) / tileSize)
            
            """figure out the range of Y tile coordinates that we can collide with"""
            start = floor(pos.y / tileSize)
            end = math.ceil((pos.y + size.y) / tileSize)
            
            
            """determine whether these tiles are all inside the map"""
            if end >= 0 & start < self.dungeon.size.y & x >= 0 & x < self.dungeon.size.x:
                """go down each of the tiles along the Y axis"""
                for y in range(start, end, 1):
                    """if there is a wall in the tile"""
                    if self.collisionMap[y][x] == tiles.wall:
                        """we adjust our end position accordingly"""
                        if move.x < 0:
                            endPos.x = x * tileSize - offset + tileSize
                        else:
                            endPos.x = x * tileSize - offset + 0
                        break
          
        """then check Y axis motion for collisions"""
        if move.y:
            """calculate the X tile coordinate where we'd like to be"""
            if move.y > 0:
                offset = size.y
            else:
                offset = 0
            #offset = move.y > 0 ? size.y : 0
            y = floor((pos.y + move.y + offset) / tileSize)

            """figure out the range of X tile coordinates that we can collide with"""
            start = floor(endPos.x / tileSize)
            end = Math.ceil((endPos.x + size.x) / tileSize)
            
            """determine whether these tiles are all inside the map"""
            if end >= 0 & start < self.dungeon.size.x & y >= 0 & y < self.dungeon.size.y:
                """go across each of the tiles along the X axis"""
                for x in range(start, end, 1):
                    """if there is a wall in the tile"""
                    if self.collisionMap[y][x] == tiles.wall:
                        """we adjust our end position accordingly"""
                        if move.y < 0:
                            endPos.y = y * tileSize - offset + tileSize
                        else:
                            endPos.y = y * tileSize - offset + 0
                        break

        """give back the new position for the object"""
        return endPos


    
