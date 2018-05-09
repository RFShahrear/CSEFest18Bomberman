import Player


class MapData:
    def __init__(self, file_name, size, player_count=2):
        file = open(file_name, "r")
        self.over = False
        self.__player_count = player_count
        self.__size = size
        self.__game_over = False
        self.__current_round = 0
        self.__player_data = {}
        self.__event_queue = []
        self.__count = 0
        self.__coordinate_data = []
        self.__bomb_data = []
        self.__to_be_placed = []
        self.__power_placement_expand = []
        self.__power_placement_increase = []
        for i in range(0, size[0]):
            line = file.readline()
            line_data = []
            for j in range(0, size[1]):
                line_data.append(line[j])
            self.__coordinate_data.append(line_data)

        file.readline()

        for i in range(0, size[0]):
            line = file.readline()
            for j in range(0, size[1]):
                if self.__coordinate_data[i][j] == "W":
                    self.__coordinate_data[i][j] += " ," + line[j]

    def __add_player(self, player):
        if len(self.__player_data) == 0:
            self.__player_data[player] = {"coordinate": (1, 1), "bomb_size": 1, "turn": True, "bomb_count": 1, "index": 1, "name": player.name, "point": 0}
            self.__coordinate_data[1][1] = "P1"
        elif len(self.__player_data) == 1:
            self.__player_data[player] = {"coordinate": (self.__size[0] - 2, self.__size[1] - 2), "bomb_size": 1, "turn": True, "bomb_count": 1, "index": 2, "name": player.name, "point": 0}
            self.__coordinate_data[self.__size[0] - 2][self.__size[1] - 2] = "P2"
        elif len(self.__player_data) == 2:
            self.__player_data[player] = {"coordinate": (self.__size[0] - 2, 1), "bomb_size": 1, "turn": True, "bomb_count": 1, "index": 3, "name": player.name, "point": 0}
            self.__coordinate_data[self.__size[0] - 2][1] = "P3"
        elif len(self.__player_data) == 3:
            self.__player_data[player] = {"coordinate": (1, self.__size[1] - 2), "bomb_size": 1, "turn": True, "bomb_count": 1, "index": 4, "name": player.name, "point": 0}
            self.__coordinate_data[1][self.__size[1] - 2] = "P4"

    def skip_turn(self, player):
        self.__player_data[player]["turn"] = False
        self.__count += 1
        if self.__count == self.__player_count:
            self.__tick()

    def schedule_move(self, player, direction):
        self.__event_queue.append(["move", player, direction])
        self.__player_data[player]["turn"] = False
        self.__count += 1
        if self.__count == self.__player_count:
            self.__tick()

    def schedule_bomb(self, player):
        self.__player_data[player]["turn"] = False
        position = self.__player_data[player]["coordinate"]
        radius = self.__player_data[player]["bomb_size"]
        self.__event_queue.append(["bomb", position, radius, player])
        self.__count += 1
        if self.__count == self.__player_count:
            self.__tick()

    def get_full_map(self):
        return [list(value[0:2].rstrip() for value in data) for data in self.__coordinate_data]

    # def get_proximity_map(self, player, radius):
    #     position = self.player_data[player]["coordinate"]
    #     return [data[position[0] - radius: position[0] + radius + 1] for data in
    #             self.coordinate_data[position[1] - radius: position[1] + radius + 1]]

    def get_player_data(self, target_player_index):
        for player in self.__player_data:
            if self.__player_data[player]["index"] == target_player_index:
                return_dict = dict(self.__player_data[player])
                return_dict.pop("turn")
                return_dict.pop("name")
                return return_dict

    def get_self_data(self, player):
        return self.__player_data[player]

    def get_all_bombs(self):
        sending_data = []
        for bomb in self.__bomb_data:
            sending_data.append(dict())
            sending_data[-1]["coordinate"] = bomb[1]
            sending_data[-1]["radius"] = bomb[2]
            sending_data[-1]["player_index"] = bomb[3].index
            sending_data[-1]["time_till_detonation"] = bomb[0] - self.__current_round + 1
        return sending_data

    def __tick(self):
        for event in self.__event_queue:
            if event[0] == "move":
                event[1].success = self.__move(event[1], event[2])
            else:
                self.__place_bomb(event[1], event[2], event[3])
        self.__event_queue.clear()
        while len(self.__bomb_data) > 0 and self.__bomb_data[0][0] == self.__current_round:
            self.__explode(self.__bomb_data.pop(0))

        self.__current_round += 1
        print(self.__current_round)

    def __next_round(self):
        if self.__current_round == 301:
            self.over = True
            for player in self.__player_data:
                player.over = True
        else:
            self.__count = 0
            for player in self.__player_data:
                self.__player_data[player]["turn"] = True
                player.reset = True

    def __explode(self, bomb):
        try:
            self.__player_data[bomb[3]]["bomb_count"] += 1
        except KeyError:
            pass

        if self.__coordinate_data[bomb[1][0]][bomb[1][1]][0] == "P":
            self.__coordinate_data[bomb[1][0]][bomb[1][1]] = "."
            bomb[3].over = True
            self.__player_data.pop(bomb[3])
            self.__player_count -= 1
            if self.__player_count == 1:
                self.over = True
                for player in self.__player_data:
                    player.over = True
                return

        self.__coordinate_data[bomb[1][0]][bomb[1][1]] = "."
        left = True
        right = True
        top = True
        bottom = True
        for i in range(0, bomb[2]):
            if right:
                block = self.__coordinate_data[bomb[1][0] + i + 1][bomb[1][1]]
                if block[0] == "W":
                    try:
                        self.__player_data[bomb[3]]["point"] += 1
                    except KeyError:
                        pass
                    self.__coordinate_data[bomb[1][0] + i + 1][bomb[1][1]] = self.__coordinate_data[bomb[1][0] + i + 1][bomb[1][1]][-1]
                    right = False
                elif block == "B":
                    for j in range(0, len(self.__bomb_data)):
                        if self.__bomb_data[j][1][0] == bomb[1][0] + i + 1 and self.__bomb_data[j][1][1] == bomb[1][1]:
                            self.__explode(self.__bomb_data.pop(j))
                            break
                elif block == "I":
                    right = False
                elif block[0] == "P":
                    self.__coordinate_data[bomb[1][0] + i + 1][bomb[1][1]] = "."
                    for player in self.__player_data:
                        if self.__player_data[player]["coordinate"][0] == bomb[1][0] + i + 1 and \
                                        self.__player_data[player]["coordinate"][1] == bomb[1][1]:
                            player.over = True
                            self.__player_data.pop(player)
                            self.__player_count -= 1
                            break
                    if self.__player_count == 1:
                        self.over = True
                        for player in self.__player_data:
                            player.over = True

            if left:
                block = self.__coordinate_data[bomb[1][0] - i - 1][bomb[1][1]]
                if block[0] == "W":
                    try:
                        self.__player_data[bomb[3]]["point"] += 1
                    except KeyError:
                        pass
                    self.__coordinate_data[bomb[1][0] - i - 1][bomb[1][1]] = self.__coordinate_data[bomb[1][0] - i - 1][bomb[1][1]][-1]
                    left = False
                elif block == "B":
                    for j in range(0, len(self.__bomb_data)):
                        if self.__bomb_data[j][1][0] == bomb[1][0] - i - 1 and self.__bomb_data[j][1][1] == bomb[1][1]:
                            self.__explode(self.__bomb_data.pop(j))
                            break
                elif block == "I":
                    left = False
                elif block[0] == "P":
                    self.__coordinate_data[bomb[1][0] - i - 1][bomb[1][1]] = "."
                    for player in self.__player_data:
                        if self.__player_data[player]["coordinate"][0] == bomb[1][0] - i - 1 and \
                                        self.__player_data[player]["coordinate"][1] == bomb[1][1]:
                            player.over = True
                            self.__player_data.pop(player)
                            self.__player_count -= 1
                            break
                    if self.__player_count == 1:
                        self.over = True
                        for player in self.__player_data:
                            player.over = True

            if top:
                block = self.__coordinate_data[bomb[1][0]][bomb[1][1] + i + 1]
                if block[0] == "W":
                    try:
                        self.__player_data[bomb[3]]["point"] += 1
                    except KeyError:
                        pass
                    self.__coordinate_data[bomb[1][0]][bomb[1][1] + i + 1] = self.__coordinate_data[bomb[1][0]][bomb[1][1] + i + 1][-1]
                    top = False
                elif block == "B":
                    for j in range(0, len(self.__bomb_data)):
                        if self.__bomb_data[j][1][0] == bomb[1][0] and self.__bomb_data[j][1][1] == bomb[1][1] + i + 1:
                            self.__explode(self.__bomb_data.pop(j))
                            break
                elif block == "I":
                    top = False
                elif block[0] == "P":
                    self.__coordinate_data[bomb[1][0]][bomb[1][1] + i + 1] = "."
                    for player in self.__player_data:
                        if self.__player_data[player]["coordinate"][0] == bomb[1][0] and \
                                        self.__player_data[player]["coordinate"][1] == bomb[1][1] + i + 1:
                            player.over = True
                            self.__player_data.pop(player)
                            self.__player_count -= 1
                            break
                    if self.__player_count == 1:
                        self.over = True
                        for player in self.__player_data:
                            player.over = True

            if bottom:
                block = self.__coordinate_data[bomb[1][0]][bomb[1][1] - i - 1]
                if block[0] == "W":
                    try:
                        self.__player_data[bomb[3]]["point"] += 1
                    except KeyError:
                        pass
                    self.__coordinate_data[bomb[1][0]][bomb[1][1] - i - 1] = self.__coordinate_data[bomb[1][0]][bomb[1][1] - i - 1][-1]
                    bottom = False
                elif block == "B":
                    for j in range(0, len(self.__bomb_data)):
                        if self.__bomb_data[j][1][0] == bomb[1][0] and self.__bomb_data[j][1][1] == bomb[1][1] - i - 1:
                            self.__explode(self.__bomb_data.pop(j))
                            break
                elif block == "I":
                    bottom = False
                elif block[0] == "P":
                    self.__coordinate_data[bomb[1][0]][bomb[1][1] - i - 1] = "."
                    for player in self.__player_data:
                        if self.__player_data[player]["coordinate"][0] == bomb[1][0] and \
                                        self.__player_data[player]["coordinate"][1] == bomb[1][1] - i - 1:
                            player.over = True
                            self.__player_data.pop(player)
                            self.__player_count -= 1
                            break
                    if self.__player_count == 1:
                        self.over = True
                        for player in self.__player_data:
                            player.over = True

    def __move(self, player, direction):
        position = self.__player_data[player]["coordinate"]
        if direction == "W":
            if self.__coordinate_data[position[0]][position[1] - 1][0] not in ("I", "B", "W", "P"):
                if position in self.__to_be_placed:
                    self.__coordinate_data[position[0]][position[1]] = "B"
                    self.__to_be_placed.remove(position)
                else:
                    self.__coordinate_data[position[0]][position[1]] = "."

                if self.__coordinate_data[position[0]][position[1] - 1] == "+":
                    self.__player_data[player]["bomb_size"] += 1
                elif self.__coordinate_data[position[0]][position[1] - 1] == "O":
                    self.__player_data[player]["bomb_count"] += 1

                self.__player_data[player]["coordinate"] = (position[0], position[1] - 1)
                position = (position[0], position[1] - 1)
                self.__coordinate_data[position[0]][position[1]] = "P" + str(self.__player_data[player]["index"])
                return True
            else:
                return False

        if direction == "S":
            if self.__coordinate_data[position[0] + 1][position[1]][0] not in ("I", "B", "W", "P"):
                if position in self.__to_be_placed:
                    self.__coordinate_data[position[0]][position[1]] = "B"
                    self.__to_be_placed.remove(position)
                else:
                    self.__coordinate_data[position[0]][position[1]] = "."

                if self.__coordinate_data[position[0] + 1][position[1]] == "+":
                    self.__player_data[player]["bomb_size"] += 1
                elif self.__coordinate_data[position[0] + 1][position[1]] == "O":
                    self.__player_data[player]["bomb_count"] += 1

                self.__player_data[player]["coordinate"] = (position[0] + 1, position[1])
                position = (position[0] + 1, position[1])
                self.__coordinate_data[position[0]][position[1]] = "P" + str(self.__player_data[player]["index"])
                return True
            else:
                return False

        if direction == "N":
            if self.__coordinate_data[position[0] - 1][position[1]][0] not in ("I", "B", "W", "P"):
                if position in self.__to_be_placed:
                    self.__coordinate_data[position[0]][position[1]] = "B"
                    self.__to_be_placed.remove(position)
                else:
                    self.__coordinate_data[position[0]][position[1]] = "."

                if self.__coordinate_data[position[0] - 1][position[1]] == "+":
                    self.__player_data[player]["bomb_size"] += 1
                elif self.__coordinate_data[position[0] - 1][position[1]] == "O":
                    self.__player_data[player]["bomb_count"] += 1

                self.__player_data[player]["coordinate"] = (position[0] - 1, position[1])
                position = (position[0] - 1, position[1])
                self.__coordinate_data[position[0]][position[1]] = "P" + str(self.__player_data[player]["index"])
                return True
            else:
                return False

        if direction == "E":
            if self.__coordinate_data[position[0]][position[1] + 1][0] not in ("I", "B", "W", "P"):
                if position in self.__to_be_placed:
                    self.__coordinate_data[position[0]][position[1]] = "B"
                    self.__to_be_placed.remove(position)
                else:
                    self.__coordinate_data[position[0]][position[1]] = "."

                if self.__coordinate_data[position[0]][position[1] + 1] == "+":
                    self.__player_data[player]["bomb_size"] += 1
                elif self.__coordinate_data[position[0]][position[1] + 1] == "O":
                    self.__player_data[player]["bomb_count"] += 1

                self.__player_data[player]["coordinate"] = (position[0], position[1] + 1)
                position = (position[0], position[1] + 1)
                self.__coordinate_data[position[0]][position[1]] = "P" + str(self.__player_data[player]["index"])
                return True
            else:
                return False

    def __place_bomb(self, position, radius, player):
        if self.__player_data[player]["bomb_count"] > 0 and position not in self.__to_be_placed:
            self.__player_data[player]["bomb_count"] -= 1
            self.__bomb_data.append([self.__current_round + 7, position, radius, player])
            self.__bomb_data.sort(key=lambda data:data[0])
            self.__to_be_placed.append(position)
            return True
        return False

    def __deduce_winner(self):
        if self.__player_count == 1:
            for player in self.__player_data:
                position = self.__player_data[player]["coordinate"]
                if self.__coordinate_data[position[0]][position[1]][0] == "P":
                    return player
        else:
            max_point = -1
            winner = None
            for player in self.__player_data:
                if self.__player_data[player]["point"] > max_point:
                    max_point = self.__player_data[player]["point"]
                    winner = player

            return winner


def main():
    pass


if __name__ == '__main__':
    main()