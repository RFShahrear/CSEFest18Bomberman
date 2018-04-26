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
            (len(self.matrix[0]) * self.blockSize, len(self.matrix) * self.blockSize))
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
            image = pygame.image.load(canonized_path)
            _image_library[path] = image
        return image

    def start_visualization(self):
        self.game_loop()

    def update_map(self):
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
                elif self.matrix[i][j] == 'W':
                    image = 'breakwall.png'
                elif self.matrix[i][j] == '.':
                    image = 'path.png'
                elif self.matrix[i][j] == 'B':
                    image = 'bomb.png'
                elif self.matrix[i][j] == 'P1':
                    image = 'player1.PNG'
                elif self.matrix[i][j] == 'P2':
                    image = 'player2.PNG'
                elif self.matrix[i][j] == 'P3':
                    image = 'player3.PNG'
                elif self.matrix[i][j] == 'P4':
                    image = 'player4.PNG'

                self.gameDisplay.blit(self.get_image(image),
                                      (j * self.blockSize, i * self.blockSize, self.blockSize, self.blockSize))

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
            pygame.display.update()

        pygame.quit()
        quit()


def start(player):
    player.play()


def main():
    map_data = Processor.MapData("map.txt", (15, 17))
    game = Visualizer(map_data)
    p1 = Player.Player(map_data, "P1")
    p2 = Player.Player(map_data, "P2")
    map_data.add_player(p1)
    map_data.add_player(p2)
    t1 = Thread(target=start, args=(p1,))
    t2 = Thread(target=start, args=(p2,))
    t1.start()
    t2.start()
    while not p1.over:
        game.update_map()
        time.sleep(2)

        map_data._MapData__next_round()
    print(map_data._MapData__deduce_winner().name)


if __name__ == '__main__':
    main()
