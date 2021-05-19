import random
import json
URL = {"Board": "/home/emili/paragony/pipr-notes/PIPR/Saper/board.json"}

oznaczenie_bomb = 11


class Dict:
    def __init__(self, wiersz, koluma, bomby):
        self._wiersz = wiersz
        self._koluma = koluma
        self._bomby = bomby
        self._map = self.make_d()
        self._map_neigh = self.neighbours()
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
    def __init__(self, wiersz, kolumna, bomby):
        self._outcome = False
        self._wiersz = wiersz
        self._koluma = kolumna
        self._bomby = bomby
        self._usedF = 0
        with open(URL["Board"], "r") as file_with_board:
            self._board = json.load(file_with_board)
        self._new_board = self.make_play_board()

    def print_map_raw(self):
        for w in range(0, self._wiersz):
            print(str(self._new_board[w]))

    def check_cell(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._board[str(w)][k]

    def check_cell_on_new(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._new_board[w][k]

    def make_play_board(self):
        new_board = {}
        for i in range(0, self._wiersz):
            wiersze = []
            for j in range(0, self._koluma):
                wiersze.append(" X ")
            new_board[i] = wiersze
        return new_board

    def click(self, mouse_button, wiersz, kolumna):
        wartosc_na_miejscu = self.check_cell(wiersz, kolumna)
        wartosc_na_miejscu_new = self.check_cell_on_new(wiersz, kolumna)
        if mouse_button == "l" and wartosc_na_miejscu_new != " F ":
            if wartosc_na_miejscu == 11:
                self._outcome = True
                self.show_bombs()
            if wartosc_na_miejscu in range(1, 10):
                self._new_board[wiersz][kolumna] = f'[{wartosc_na_miejscu}]'
            if wartosc_na_miejscu == 0:
                self.odkryj_puste(wiersz, kolumna)
        if mouse_button == "p" and wartosc_na_miejscu_new == ' X ':
            self.change_cell(wiersz, kolumna, " F ")
            self._usedF += 1
        if mouse_button == "p" and wartosc_na_miejscu_new == ' F ':
            self.change_cell(wiersz, kolumna, " X ")
            self._usedF -= 1

    def show_bombs(self):
        for i in range(0, self._wiersz):
            for j in range(0, self._koluma):
                if self.check_cell(i, j) == oznaczenie_bomb:
                    self._new_board[i][j] = " B "
        return

    def change_cell(self, w, k, val):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            self._new_board[w][k] = val
        return

    def odkryj_puste(self, wiersz, kolumna):
        self._new_board[wiersz][kolumna] = '[ ]'
        for i in range(self._koluma*self._wiersz):
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if self.check_cell_on_new(i+a, j+b) == '[ ]':
                                wartosc_na_miejscu = self.check_cell(i, j)
                                wartosc_na_miejscu_new = self.check_cell_on_new(i, j)
                                if wartosc_na_miejscu_new != " F ":
                                    if wartosc_na_miejscu == 0:
                                        self.change_cell(i, j, '[ ]')
                                    else:
                                        self.change_cell(i, j, f'[{wartosc_na_miejscu}]')
        return

    def you_win(self):
        x = False
        if self._bomby == self._usedF:
            x = True
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    wartosc_na_miejscu = self.check_cell(i, j)
                    wartosc_na_miejscu_new = self.check_cell_on_new(i, j)
                    if wartosc_na_miejscu == 11 and wartosc_na_miejscu_new != " F ":
                        x = False
        else:
            x = True
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    wartosc_na_miejscu = self.check_cell(i, j)
                    wartosc_na_miejscu_new = self.check_cell_on_new(i, j)
                    if wartosc_na_miejscu < 11 and wartosc_na_miejscu_new == " X ":
                        x = False
        return x


def main():
    wiersze = 10
    kolumny = 10
    bomny = 7
    mapa = Dict(wiersze, kolumny, bomny)
    mapa.print_map_raw()
    a = Play_board(wiersze, kolumny, bomny)
    a.print_map_raw()
    while a._outcome is False:
        myszka = input("myszka: ")
        wiersz = int(input("wiersz: "))-1
        kolumna = int(input("kolumna: "))-1
        if wiersz >= 0 and wiersz <= wiersze and kolumna >= 0 and kolumna <= kolumny:
            a.click(myszka, wiersz, kolumna)
            a.print_map_raw()
            if a._outcome is True:
                print("You loose")
            if a.you_win() is True:
                print("You win")
                a._outcome = True
        else:
            print("Wrong input try again")


if __name__ == "__main__":
    main()
