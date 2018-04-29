import os
import pygame
import Player
from threading import Thread
import Processor
import time

_image_library = {}


class Visualizer:
    def __init__(self, map_data):
        pygame.init()
        self.map_data = map_data
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.breakBox = (174, 117, 48)
        self.unbreakBox = (166, 51, 13)
        self.path = (238, 138, 0)
        self.bluePlayer = (1, 138, 204)
        self.greenPlayer = (164, 215, 22)
        self.violetPlayer = (175, 7, 21)
        self.orangePlayer = (202, 94, 6)
        self.blackBomb = (71, 95, 102)
        self.redBomb = (207, 33, 50)

        self.simplePlayer = (164, 215, 22)

        self.blockSize = 37

        self.matrix = map_data.get_full_map()

        self.gameDisplay = pygame.display.set_mode(
            (len(self.matrix[0]) * self.blockSize + 300, len(self.matrix) * self.blockSize))
        pygame.display.set_caption('Bomberman')

    def checkExit(self):
        game_exit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                break
            pygame.event.clear()

        return game_exit

    def get_image(self, path):
        global _image_library
        image = _image_library.get(path)
        if image is None:
            canonized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(os.path.join("Images", canonized_path))
            _image_library[path] = image
        return image

    def start_visualization(self):
        self.game_loop()

    def message_to_screen(self, msg, color, x, y, angle=0):
        font = pygame.font.SysFont("times new roman", 25)
        screen_text = font.render(msg, True, color)
        screen_text = pygame.transform.rotate(screen_text, angle)
        self.gameDisplay.blit(screen_text, [x, y])

    def update_map(self, players):
        if self.checkExit():
            pygame.quit()
            quit()
        self.matrix = self.map_data.get_full_map()
        pygame.event.clear()
        pygame.display.update()
        self.gameDisplay.fill(self.white)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                image = None
                if self.matrix[i][j] == 'I':
                    image = 'unbreakwall.png'
                elif self.matrix[i][j][0] == 'W':
                    image = 'breakwall.png'
                elif self.matrix[i][j] == '.':
                    image = 'path.png'
                elif self.matrix[i][j] == 'B':
                    image = 'bomb.png'
                elif self.matrix[i][j] == "+":
                    image = 'explosionUp.png'
                elif self.matrix[i][j] == "O":
                    image = 'bombUp.png'
                elif self.matrix[i][j] == "P1,B" or self.matrix[i][j] == 'P1':
                    image = 'player1.PNG'
                elif self.matrix[i][j] == "P2,B" or self.matrix[i][j] == 'P2':
                    image = 'player2.PNG'
                elif self.matrix[i][j] == "P3,B" or self.matrix[i][j] == 'P3':
                    image = 'player3.PNG'
                elif self.matrix[i][j] == "P4,B" or self.matrix[i][j] == 'P4':
                    image = 'player4.PNG'

                self.gameDisplay.blit(self.get_image(image),
                                      (j * self.blockSize, i * self.blockSize, self.blockSize, self.blockSize))
        pygame.draw.rect(self.gameDisplay, self.black,
                         (len(self.matrix[0]) * self.blockSize, 0, 300, len(self.matrix) * self.blockSize))

        for player in players:
            i = players[player]["index"] - 1
            imagename = 'player' + str(i + 1) + 'Large.png'
            self.gameDisplay.blit(self.get_image(imagename), (len(self.matrix[0]) * self.blockSize, i*112))
            name = players[player]["name"]
            bomb_size = "Bomb Size " + str(players[player]["bomb_size"])
            bomb_count = "Bomb Count" + str(players[player]["bomb_count"])
            self.message_to_screen(name, self.white, len(self.matrix[0]) * self.blockSize + 114, i*112 + 5)
            self.message_to_screen(bomb_size, self.white, len(self.matrix[0]) * self.blockSize + 114, i * 112 + 30)
            self.message_to_screen(bomb_count, self.white, len(self.matrix[0]) * self.blockSize + 114, i * 112 + 55)

        pygame.display.update()

    def get_position(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 'P':
                    return i, j

    def move_left(self):
        x_pos, y_pos = self.get_position()
        if y_pos > 0 and len(self.matrix[0]) - 1 and self.matrix[x_pos][y_pos - 1] == '.':
            self.matrix[x_pos][y_pos] = '.'
            self.matrix[x_pos][y_pos - 1] = 'P'

    def move_right(self):
        x_pos, y_pos = self.get_position()
        if y_pos < len(self.matrix[0]) - 1 and self.matrix[x_pos][y_pos + 1] == '.':
            self.matrix[x_pos][y_pos] = '.'
            self.matrix[x_pos][y_pos + 1] = 'P'

    def move_up(self):
        x_pos, y_pos = self.get_position()
        if x_pos > 0 and self.matrix[x_pos - 1][y_pos] == '.':
            self.matrix[x_pos][y_pos] = '.'
            self.matrix[x_pos - 1][y_pos] = 'P'

    def move_down(self):
        x_pos, y_pos = self.get_position()
        if x_pos < len(self.matrix[0]) - 1 and self.matrix[x_pos + 1][y_pos] == '.':
            self.matrix[x_pos][y_pos] = '.'
            self.matrix[x_pos + 1][y_pos] = 'P'

    def game_loop(self):
        game_exit = False

        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
            pygame.event.clear()

            pygame.display.update()
            self.gameDisplay.fill(self.white)
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    image = None
                    if self.matrix[i][j] == 'I':
                        image = 'unbreakwall.png'
                    elif self.matrix[i][j] == 'W':
                        image = 'breakwall.png'
                    elif self.matrix[i][j] == '.':
                        image = 'path.png'
                    elif self.matrix[i][j] == 'B':
                        image = 'bomb.png'
                    elif self.matrix[i][j] == 'P':
                        image = 'player1.PNG'

                    self.gameDisplay.blit(self.get_image(image), (j * self.blockSize, i * self.blockSize, self.blockSize, self.blockSize))
            pygame.draw.rect(self.gameDisplay, self.black, (len(self.matrix[0]) * self.blockSize, 0, 300, len(self.matrix) * self.blockSize))
            pygame.display.update()

        pygame.quit()
        quit()


def start(player):
    player.play()


def main():
    map_data = Processor.MapData("map.txt", (15, 17), 4)
    game = Visualizer(map_data)
    p1 = Player.Player(map_data, "P1")
    p2 = Player.Player(map_data, "P2")
    p3 = Player.Player(map_data, "P3")
    p4 = Player.Player(map_data, "P4")

    map_data.add_player(p1)
    map_data.add_player(p2)
    map_data.add_player(p3)
    map_data.add_player(p4)

    p1.index = 1
    p2.index = 2
    p3.index = 3
    p4.index = 4

    t1 = Thread(target=start, args=(p1,))
    t2 = Thread(target=start, args=(p2,))
    t3 = Thread(target=start, args=(p3,))
    t4 = Thread(target=start, args=(p4,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    while not p1.over:
        game.update_map(map_data._MapData__player_data)
        time.sleep(0.5)

        map_data._MapData__next_round()
    print(map_data._MapData__deduce_winner().name)


if __name__ == '__main__':
    main()
