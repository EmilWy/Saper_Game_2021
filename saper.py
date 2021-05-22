import random
import json
URL = {"Board": "/home/emili/paragony/pipr-notes/PIPR/Saper/board.json", "Play_Board": "/home/emili/paragony/pipr-notes/PIPR/Saper/play_board.json"}

oznaczenie_bomb = 9
lista_obrazkow = ["[ ]", "1", "2", "3", "4", "5", "6", "7", "8", " B ", " F " , " X "]


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
        self.make_play_board()
        with open(URL["Play_Board"], "r") as file_with_play_board:
            self._new_board = json.load(file_with_play_board)

    def print_map_raw(self):
        for w in range(0, self._wiersz):
            print(str(self._new_board[str(w)]))

    def check_cell(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._board[str(w)][k]

    def check_cell_on_new(self, w, k):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            return self._new_board[str(w)][k]

    def make_play_board(self):
        new_board = {}
        for i in range(0, self._wiersz):
            wiersze = []
            for j in range(0, self._koluma):
                wiersze.append(lista_obrazkow[11])
            new_board[i] = wiersze
        with open(URL["Play_Board"], "w") as file_with_board:
            json.dump(new_board, file_with_board)
        return

    def click(self, mouse_button, wiersz, kolumna):
        wartosc_na_miejscu = self.check_cell(wiersz, kolumna)
        wartosc_na_miejscu_new = self.check_cell_on_new(wiersz, kolumna)
        if mouse_button == "l" and wartosc_na_miejscu_new != lista_obrazkow[10]:
            if wartosc_na_miejscu == oznaczenie_bomb:
                self._outcome = True
                self.show_bombs()
            if wartosc_na_miejscu in range(1, 9):
                self._new_board[str(wiersz)][kolumna] = f'[{lista_obrazkow[wartosc_na_miejscu]}]'
            if wartosc_na_miejscu == 0:
                self.odkryj_puste(wiersz, kolumna)
        if mouse_button == "p" and wartosc_na_miejscu_new == lista_obrazkow[11]:
            self.change_cell(wiersz, kolumna, lista_obrazkow[10])
            self._usedF += 1
        if mouse_button == "p" and wartosc_na_miejscu_new == lista_obrazkow[10]:
            self.change_cell(wiersz, kolumna, lista_obrazkow[11])
            self._usedF -= 1
        with open(URL["Play_Board"], "w") as file_with_board:
            json.dump(self._new_board, file_with_board)

    def show_bombs(self):
        for i in range(0, self._wiersz):
            for j in range(0, self._koluma):
                if self.check_cell(i, j) == oznaczenie_bomb:
                    self._new_board[str(i)][j] = lista_obrazkow[9]
        return

    def change_cell(self, w, k, val):
        if w >= 0 and w <= self._wiersz-1 and k >= 0 and k <= self._koluma-1:
            self._new_board[str(w)][k] = val
        return

    def odkryj_puste(self, wiersz, kolumna):
        self._new_board[str(wiersz)][kolumna] = lista_obrazkow[0]
        for i in range(self._koluma*self._wiersz):
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if self.check_cell_on_new(i+a, j+b) == lista_obrazkow[0]:
                                wartosc_na_miejscu = self.check_cell(i, j)
                                wartosc_na_miejscu_new = self.check_cell_on_new(i, j)
                                if wartosc_na_miejscu_new != lista_obrazkow[10]:
                                    if wartosc_na_miejscu == 0:
                                        self.change_cell(i, j, lista_obrazkow[0])
                                    else:
                                        self.change_cell(i, j, f'[{lista_obrazkow[wartosc_na_miejscu]}]')
        return

    def you_win(self):
        x = False
        if self._bomby == self._usedF:
            x = True
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    wartosc_na_miejscu = self.check_cell(i, j)
                    wartosc_na_miejscu_new = self.check_cell_on_new(i, j)
                    if wartosc_na_miejscu == oznaczenie_bomb and wartosc_na_miejscu_new != lista_obrazkow[10]:
                        x = False
        else:
            x = True
            for i in range(0, self._wiersz):
                for j in range(0, self._koluma):
                    wartosc_na_miejscu = self.check_cell(i, j)
                    wartosc_na_miejscu_new = self.check_cell_on_new(i, j)
                    if wartosc_na_miejscu < oznaczenie_bomb and wartosc_na_miejscu_new == lista_obrazkow[11]:
                        x = False
        return x


def main():
    wiersze = 5
    kolumny = 5
    bomny = 2
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
