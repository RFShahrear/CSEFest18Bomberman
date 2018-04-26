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
        while not self.over:
            print(self.map_data.get_player_data(1))
            if count == 2:
                self.map_data.schedule_bomb(self)
            else:
                self.map_data.schedule_move(self, "E")
            count += 1
            while not self.reset:
                pass

            self.reset = False



