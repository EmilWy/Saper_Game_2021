import random
import json
URL = {
    "Board": "/home/emili/paragony/pipr-notes/PIPR/Saper/board.json",
    "Play_Board": "/home/emili/paragony/pipr-notes/PIPR/Saper/play_board.json"
    }

oznaczenie_bomb = 11


class Dict:
    def __init__(self, wiersz, kolumna, bomby, mapa=None):
        self._wiersz = wiersz
        self._koluma = kolumna
        if (wiersz or kolumna) <= 0:
            raise KeyError
        if bomby <= wiersz*kolumna:
            self._bomby = bomby
        else:
            self._bomby = random.randint(0, kolumna*wiersz)
        if not mapa:
            self._map = self.make_d()
        else:
            self._map = mapa
        self.neighbours()
        with open(URL["Board"], "w") as file_with_board:
            json.dump(self._map, file_with_board)
        file_with_board.close()

    def print_map_raw(self):
        for w in range(0, self._wiersz):
            print(str(self._map[w]))

    def make_d(self):
        N = self._bomby
        dictionary = {}
        array = []
        for i in range(0, self._wiersz*self._koluma):
            if N > 0:
                array.append(oznaczenie_bomb)
                N = N-1
            else:
                array.append(0)
        random.shuffle(array)
        n = 0
        k = self._koluma
        for i in range(0, self._wiersz):
            dictionary[i] = array[n:k]
            n += self._koluma
            k = k + self._koluma
        return dictionary

    def find_cell(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._map[w][k]
        else:
            pass

    def change_cell(self, w, k, val):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            self._map[w][k] = val
            return

    def neighbours(self):
        for i in range(0, self._wiersz):
            for j in range(0, self._koluma):
                a = 1
                if self.find_cell(i, j) == 0:
                    for n in range(-1, 2):
                        for m in range(-1, 2):
                            if self.find_cell(i+n, j+m) == oznaczenie_bomb:
                                self.change_cell(i, j, a)
                                a += 1
        return


class Play_board:
    def __init__(self, wiersz, kolumna, bomby, lista_o=None, New_game=True):
        if (wiersz or kolumna) <= 0:
            raise KeyError
        if bomby <= wiersz*kolumna:
            self._bomby = bomby
        self.lista_ob = lista_o
        self._outcome = False
        self._wiersz = wiersz
        self._koluma = kolumna
        self._bomby = bomby
        self._usedF = 0
        self._win = None
        with open(URL["Board"], "r") as file_with_board:
            self._board = json.load(file_with_board)
        if New_game:
            self.make_play_board()
        with open(URL["Play_Board"], "r") as file_with_play_board:
            self._new_board = json.load(file_with_play_board)

    def print_raw_map_raw(self):
        for w in range(0, self._wiersz):
            print(str(self._board[str(w)]))

    def print_map_raw(self):
        for w in range(0, self._wiersz):
            print(str(self._new_board[str(w)]))

    def check_cell(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._board[str(w)][k]

    def check_cell_on_new(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._new_board[str(w)][k]

    def change_cell(self, w, k, val):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            self._new_board[str(w)][k] = val
        return

    def make_play_board(self):
        new_board = {}
        for i in range(0, self._wiersz):
            wiersze = []
            for j in range(0, self._koluma):
                wiersze.append(self.lista_ob[11])
            new_board[i] = wiersze
        with open(URL["Play_Board"], "w") as file_with_board:
            json.dump(new_board, file_with_board)
        return

    def click(self, mouse_button, wiersz, kolumna):
        if mouse_button == "l":
            self.left_click(wiersz, kolumna)
        if mouse_button == "p":
            self.right_click(wiersz, kolumna)
        with open(URL["Play_Board"], "w") as file_with_board:
            json.dump(self._new_board, file_with_board)
        if self._outcome is False:
            self.you_win()

    def left_click(self, wiersz, kolumna):
        wartosc = self.check_cell(wiersz, kolumna)
        wart_na_new = self.check_cell_on_new(wiersz, kolumna)
        if wart_na_new != self.lista_ob[10]:
            if wartosc == oznaczenie_bomb:
                self._outcome = True
                self.show_bombs()
            if wartosc in range(1, 9):
                self.change_cell(wiersz, kolumna, self.lista_ob[wartosc])
            if wartosc == 0:
                self.odkryj_puste(wiersz, kolumna)

    def right_click(self, wiersz, kolumna):
        wartosc_na_miejscu_new = self.check_cell_on_new(wiersz, kolumna)
        if wartosc_na_miejscu_new == self.lista_ob[11]:
            self.change_cell(wiersz, kolumna, self.lista_ob[10])
            self._usedF += 1
        if wartosc_na_miejscu_new == self.lista_ob[10]:
            self.change_cell(wiersz, kolumna, self.lista_ob[11])
            self._usedF -= 1

    def show_bombs(self):
        for i in range(0, self._wiersz):
            for j in range(0, self._koluma):
                if self.check_cell(i, j) == oznaczenie_bomb:
                    self.change_cell(i, j, self.lista_ob[9])
        self._win = False
        return

    def odkryj_puste(self, wiersz, kolumna):
        self.change_cell(wiersz, kolumna, self.lista_ob[0])
        for i in range(self._koluma*self._wiersz):
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if self.check_cell_on_new(i+a, j+b) == self.lista_ob[0]:
                                wartosc = self.check_cell(i, j)
                                wartosc_na_new = self.check_cell_on_new(i, j)
                                if wartosc_na_new != self.lista_ob[10]:
                                    if wartosc == 0:
                                        self.change_cell(i, j, self.lista_ob[0])
                                    else:
                                        self.change_cell(i, j, self.lista_ob[wartosc])
        return

    def you_win(self):
        self._outcome = True
        for i in range(0, self._wiersz):
            for j in range(0, self._koluma):
                wartosc_na_miejscu = self.check_cell(i, j)
                wartosc_new = self.check_cell_on_new(i, j)
                if wartosc_na_miejscu != oznaczenie_bomb and wartosc_new == self.lista_ob[10]:
                    self._outcome = False
                elif wartosc_na_miejscu != oznaczenie_bomb and wartosc_new == self.lista_ob[11]:
                    self._outcome = False
        if self._outcome is True:
            self._win = True
        return


def main():
    lista_obrazkow = [" ", "1", "2", "3", "4", "5", "6", "7", "8", "B", "F", "X"]
    wiersze = 3
    kolumny = 3
    bomny = 1
    new_game = input("New_game?")
    if new_game == '1':
        mapa = Dict(wiersze, kolumny, bomny)
        a = Play_board(wiersze, kolumny, bomny, lista_obrazkow)
    else:
        a = Play_board(wiersze, kolumny, bomny, lista_obrazkow, False)
    a.print_raw_map_raw()
    a.print_map_raw()
    while a._outcome is False:
        myszka = input("myszka: ")
        wiersz = int(input("wiersz: "))
        kolumna = int(input("kolumna: "))
        if wiersz >= 0 and wiersz <= wiersze and kolumna >= 0 and kolumna <= kolumny:
            a.click(myszka, wiersz, kolumna)
            a.print_map_raw()
            if a._win is False:
                print("You loose")
            if a._win is True:
                print("You win")
        else:
            print("Wrong input try again")


if __name__ == "__main__":
    main()
