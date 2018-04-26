import Processor


class Player:
    def __init__(self, map_data : "Processor.MapData", name=None):
        if name is None:
            self.name = "Unnamed"
        else:
            self.name = name
        self.map_data = map_data
        self.over = False
        self.success = True
        self.reset = False

    def play(self):
        count = 0
        direction = "E"
        while not self.over:
            if not self.success:
                direction = "S"
                count = 0
                self.success = True
            if direction == "S" and count == 1:
                direction = "W"
                count += 0
            if count == 4:
                self.map_data.schedule_bomb(self)
            else:
                self.map_data.schedule_move(self, direction)
            count += 1
            while not self.reset:
                pass

            self.reset = False




