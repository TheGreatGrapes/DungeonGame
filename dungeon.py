from room import Room
from tiles import tiles

class Dungeon:
    def addStairs(self, type):
        room = None

        # keep picking random rooms until we find one that has only one door and doesn't already have stairs in it
        while True:
            room = self.randomElement(self.rooms)
            if (len(room.getDoorLocations) > 1 or
                room.hasStairs()):
                break
        
        # build a list of all locations in the room that qualify for stairs
        candidates = []
        for y, _ in enumerate(room.size['y'] -2):
            for x in enumerate(room.size['x'] -2):
                # only put stairs on the floor
                if (room.tiles[y][x] != tiles.floor):
                    continue
                
                if (
                    room.tiles[y - 1][x] == tiles.door or
                    room.tiles[y + 1][x] == tiles.door or
                    room.tiles[y][x - 1] == tiles.door or 
                    room.tiles[y][x + 1] == tiles.door):
                    continue
                # add it to the candidate list
                candidates.append({ 'x': x, 'y': y })            

        
        loc = randomElement(candidates)
        room.tiles[loc['y']][loc['x']] = type