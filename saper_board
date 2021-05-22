from tkinter import *
from tkinter import messagebox as mbox
import json
from saper import Dict
URL = {"Board": "/home/emili/paragony/pipr-notes/PIPR/Saper/board.json"}


class Game(Dict):
    def __init__(self, root, wiersze, kolumny, bomby):
        self._wiersze = wiersze
        self._kolumny = kolumny
        self._bomby = bomby
        self._root = root
        self._flags = 0
        with open(URL["Board"], "r") as file_with_board:
            self._board = json.load(file_with_board)
        self._images = {
                "plain": PhotoImage(file="/home/emili/paragony/pipr-notes/PIPR/Saper/plain.png"),
                "blank": PhotoImage(file="/home/emili/paragony/pipr-notes/PIPR/Saper/blank.png"),
                "mine": PhotoImage(file="/home/emili/paragony/pipr-notes/PIPR/Saper/mine1.gif"),
                "flag": PhotoImage(file="/home/emili/paragony/pipr-notes/PIPR/Saper/flag.png"),
                "numbers": [PhotoImage(file="/home/emili/paragony/pipr-notes/PIPR/Saper/"+str(i)+".png") for i in range(1, 9)]
                }
        self._frame = Frame(self._root)
        self._frame.pack()

    def board(self):
        self._tiles = {}
        for x in range(0, self._wiersze):
            for y in range(0, self._kolumny):
                if y == 0:
                    self._tiles[x] = {}
                tile = {
                    "x": x,
                    "y": y,
                    "cover": Button(self._frame, image=self._images["plain"]),
                    "value": self._board[str(x)][y],
                    "state": 0,
                    "flag": 0
                }
                tile["cover"].bind("<Button-1>", self.left_click(x, y))
                tile["cover"].bind("<Button-3>", self.right_click(x, y))
                tile["cover"].grid(row=x, column=y)
                self._tiles[x][y] = tile

    def uncover(self, x, y):
        tile = self._tiles[x][y]
        if tile["state"] == 0:
            if 0 < tile["value"] <= 8:
                tile["cover"].config(image = self._images["numbers"][tile["value"]-1])
                tile["state"] = 1
            else:
                tile["cover"].config(image = self._images["blank"])
                tile["state"] = 1
                if x > 0:
                    self.uncover(x-1, y)
                if x < self._wiersze - 1:
                    self.uncover(x+1, y)
                if y > 0:
                    self.uncover(x, y-1)
                if y < self._kolumny - 1:
                    self.uncover(x, y+1)
                if x > 0 and y > 0:
                    self.uncover(x-1,y-1)
                if x > 0 and y < self._kolumny - 1:
                    self.uncover(x-1, y+1)
                if x < self._wiersze - 1 and y > 0:
                    self.uncover(x+1, y-1)
                if x < self._wiersze - 1 and y < self._kolumny - 1:
                    self.uncover(x+1, y+1)

    def right_click(self, x, y):
        return lambda Button: self.right_click_action(self._tiles[x][y])

    def right_click_action(self, tile):
        if tile["state"] == 0:
            tile["cover"].config(image=self._images["flag"])
            tile["flag"] = 1
            tile["state"] = 2
            self._flags += 1
        elif tile["state"] == 2:
            tile["cover"].config(image=self._images["plain"])
            tile["flag"] = 0
            tile["state"] = 0
            self._flags -= 1
        self.check_if_won_flags()

    def left_click(self, x, y):
        return lambda Button: self.left_click_action(self._tiles[x][y])

    def left_click_action(self, tile):
        if tile["state"] == 0:
            if tile["value"] == 11:
                tile["cover"].config(image = self._images["mine"])
                self.game_over(False)
                return
            else:
                x = tile["x"]
                y = tile["y"]
                self.uncover(x, y)
                self.check_if_won_uncover()

    def check_if_won_flags(self):
        if self._flags == self._bomby:
            for x in range(0, self._wiersze):
                for y in range(0, self._kolumny):
                    tile = self._tiles[x][y]
                    if tile["state"] == 2 and tile["value"] != 11:
                        return
            self.game_over(True)

    def check_if_won_uncover(self):
        for x in range(0, self._wiersze):
            for y in range(0, self._kolumny):
                tile = self._tiles[x][y]
                if tile["state"] == 0 and tile["value"] != 11:
                    return
        self.game_over(True)

    def game_over(self, result):
        if result is True:
            answer = mbox.askyesno("Game Over", "Congrats! You won")
        else:
            answer = mbox.askyesno("Game Over", "Sorry, maybe next time")
        if answer is False:
            quit()
        else:
            self.board()


def main():
    wiersze = 10
    kolumny = 10
    bomby = 7
    Dict(wiersze, kolumny, bomby)
    window = Tk()
    game = Game(window, wiersze, kolumny, bomby)
    game.board()
    window.mainloop()


if __name__ == "__main__":
    main()
