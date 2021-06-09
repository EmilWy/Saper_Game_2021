from tkinter import *
from tkinter import messagebox as mbox
import json
from saper import Dict
import os.path


URL = {
    "Board": "/home/lucky/pipr/sem2/minesweeper/board.json",
    "saved": "/home/lucky/pipr/sem2/minesweeper/saved.json",
    "last_game": "/home/lucky/pipr/sem2/minesweeper/last_game.json"
    }


class Game:
    def __init__(self, root, wiersze, kolumny, bomby):
        self._wiersze = wiersze
        self._kolumny = kolumny
        self._bomby = bomby
        self._root = root
        self._flags = 0
        self._images = {
                "plain": PhotoImage(file="plain.png"),
                "blank": PhotoImage(file="blank.png"),
                "mine": PhotoImage(file="mine1.gif"),
                "flag": PhotoImage(file="flag.png"),
                "numbers": [PhotoImage(file=str(i)+".png") for i in range(1, 9)]
                }
        self._frame = Frame(self._root)
        self._frame.pack()

    def load_game(self):
        if os.path.isfile(URL["saved"]):
            self._tiles = {}
            with open(URL["saved"], "r") as file_with_board:
                tiles = json.load(file_with_board)
            for x in range(0, self._wiersze):
                for y in range(0, self._kolumny):
                    if y == 0:
                        self._tiles[x] = {}
                    tile = tiles[str(x)][str(y)]
                    tile["cover"] = Button(self._frame, image=self._images["plain"])
                    if tile["state"] == 1:
                        tile["cover"].config(image=self._images["numbers"][tile["value"]-1])
                    if tile["state"] == 2:
                        tile["cover"].config(image=self._images["flag"])
                    if tile["value"] == 0 and tile["state"] == 1:
                        tile["cover"].config(image=self._images["blank"])
                    tile["cover"].bind("<Button-1>", self.left_click(x, y))
                    tile["cover"].bind("<Button-3>", self.right_click(x, y))
                    tile["cover"].grid(row=x, column=y)
                    self._tiles[x][y] = tile
            with open(URL["last_game"], "r") as file_with_board:
                self._board = json.load(file_with_board)
        else:
            self.board()

    def board(self):
        self.new_board()
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
                tile["cover"].config(image=self._images["numbers"][tile["value"]-1])
                tile["state"] = 1
            else:
                tile["cover"].config(image=self._images["blank"])
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
                    self.uncover(x-1, y-1)
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
            if tile["value"] == 9:
                tile["cover"].config(image=self._images["mine"])
                for x in range(0, self._wiersze):
                    for y in range(0, self._kolumny):
                        tile = self._tiles[x][y]
                        if tile["value"] == 9:
                            tile["cover"].config(image=self._images["mine"])
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
                    if tile["state"] == 2 and tile["value"] != 9:
                        return
            self.game_over(True)

    def check_if_won_uncover(self):
        for x in range(0, self._wiersze):
            for y in range(0, self._kolumny):
                tile = self._tiles[x][y]
                if tile["state"] == 0 and tile["value"] != 9:
                    return
        self.game_over(True)

    def new_board(self):
        Dict(self._wiersze, self._kolumny, self._bomby)
        with open(URL["Board"], "r") as file_with_board:
            self._board = json.load(file_with_board)

    def game_over(self, result):
        if result is True:
            answer = mbox.askyesno("Game Over", "Congrats! You won\nDo you want to play again?")
        else:
            answer = mbox.askyesno("Game Over", "Sorry, maybe next time\nDo you want to play again?")
        if answer is False:
            quit()
        else:
            self.board()

    def file_save(self):
        board = self._tiles
        for x in range(0, self._wiersze):
            for y in range(0, self._kolumny):
                board[x][y].pop("cover")
        with open(URL["saved"], "w") as file_with_board:
            json.dump(board, file_with_board)
        with open(URL["last_game"], "w") as file_with_board:
            json.dump(self._board, file_with_board)

    def close(self):
        if mbox.askyesno('QUIT', "Are you sure you want to leave?\nIf so you can save your progress"):
            if mbox.askyesno('Save', "Do you want to save game?"):
                self.file_save()
            self._root.destroy()


def main():
    wiersze = 7
    kolumny = 7
    bomby = 7
    h = wiersze * 26
    w = kolumny * 26
    window = Tk()
    window.geometry(str(h)+'x'+str(w))
    game = Game(window, wiersze, kolumny, bomby)
    window.protocol('WM_DELETE_WINDOW', game.close)
    if mbox.askyesno('New Game', "Do you want to load last game?"):
        game.load_game()
    else:
        game.board()
    window.mainloop()


if __name__ == "__main__":
    main()
