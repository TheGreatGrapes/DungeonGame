from tiles import tiles
class Room:
    def __init__(self, width, height):
        self.size = {"x": width, "y":height}
        self.pos = {"x": 0, "y":0}
        self.tiles = []

        """surround the room with walls, and fill the rest with floor"""
        for y,_ in enumerate(range(self.size.get("y")):
            row = []
            for x,_ in enumerate(range(self.size.get("x"))):
                if (y == 0 or y == (self.size.get("y") - 1) or
                    x == 0 or x == (self.size.get("x") - 1)):
                    row.append (tiles.get("wall"))
                else:
                    row.append(tiles.get("floor"))
            self.tiles.append(row)

    def hasStairs(self):
        """ find out if we have any stair tiles in the room """
        for y,_ in enumerate(range(self.size.get("y"))):
            for x,_ in enumerate(range(self.size.get("x"))):
                if (self.tiles[y][x] == tiles.get("stairsDown") or 
                self.tiles[y][x] == tiles.get("stairsUp")):
                return True
        return False

    def getDoorLocations(self):
        doors = []

        """ find all the doors and add their positions to the list """
        for y,_ in enumerate(range(self.size.get("y"))):
            for x,_ in enumerate(range(self.size.get("x"))):
                if (self.tiles[y][x] == tiles.get("door")):
                    doors.append({"x":x, "y":y})
        

        return doors;
    
    @staticmethod
    def areConnected(room1, room2):
        """ iterate the doors in room1 and see if any are also a door in room2 """
        doors = room1.getDoorLocations()
        for door in doors:
            """ move the door into "world space" using room1's position """
            door['x'] += room1.pos['x']
            door['y'] += room1.pos['y']

            """ move the door into room2 space by subtracting room2's position """
            door['x'] += room2.pos['x']
            door['y'] += room2.pos['y']

            """" make sure the position is valid for room2's tiles array """
            if (door['x'] < 0 or door['x'] > (room2.size['x'] - 1) or door['y'] < 0 or door['y'] > (room2.size['y']-1)):
                continue

            """ see if the tile is a door; if so this is a door from room1 to room2 so the rooms are connected """
            if (room2.tiles[door['y']][door['x']] == tiles['door']:
                return True


        return False
















    