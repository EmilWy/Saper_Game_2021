from saper import Dict, Play_board

mapa_raw3x3 = {
            0: [0, 0, 0],
            1: [11, 0, 0],
            2: [0, 0, 0]
            }
wiersze3x3 = 3
kolumny3x3 = 3
bomny3x3 = 1
mapa_raw2x2 = {
            0: [0, 11],
            1: [11, 0]
            }
wiersze2x2 = 2
kolumny2x2 = 2
bomny2x2 = 2
lista_obrazkow = [" ", "1", "2", "3", "4", "5", "6", "7", "8", "B", "F", "X"]


class TestDict():
    def test_check_cell(self):
        mapa = Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        value_in_0x0 = mapa.find_cell(0, 0)
        assert value_in_0x0 == 1

    def test_change_cell(self):
        mapa = Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        mapa.change_cell(0, 0, 3)
        mapa.change_cell(2, 2, 6)
        mapa_sasiedzi = {
            0: [3, 1, 0],
            1: [11, 1, 0],
            2: [1, 1, 6]
            }
        assert mapa._map == mapa_sasiedzi

    def test_sasiedzi(self):
        mapa = Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        mapa_sasiedzi = {
            0: [1, 1, 0],
            1: [11, 1, 0],
            2: [1, 1, 0]
            }
        assert mapa._map == mapa_sasiedzi


class TestPlayBoard():
    def test_check_cell(self):
        Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        mapa_new = Play_board(wiersze3x3, kolumny3x3, bomny3x3, lista_obrazkow)
        value_in_0x0 = mapa_new.check_cell(0, 0)
        assert value_in_0x0 == 1
        value_in_1x0 = mapa_new.check_cell(1, 0)
        assert value_in_1x0 == 11
        value_in_22x0 = mapa_new.check_cell(22, 0)
        assert value_in_22x0 is None
        value_in_new_0x0 = mapa_new.check_cell_on_new(1, 0)
        assert value_in_new_0x0 == 'X'
        mapa_newA = {
            "0": ["X", "X", "X"],
            "1": ["X", "X", "X"],
            "2": ["X", "X", "X"]
            }
        assert mapa_new._new_board == mapa_newA

    def test_change_cell(self):
        Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        mapa_new = Play_board(wiersze3x3, kolumny3x3, bomny3x3, lista_obrazkow)
        mapa_new.change_cell(1, 0, 'A')
        mapa_newA = {
            "0": ["X", "X", "X"],
            "1": ["A", "X", "X"],
            "2": ["X", "X", "X"]
            }
        assert mapa_new._new_board == mapa_newA

    def test_left_click(self):
        Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        mapa_new = Play_board(wiersze3x3, kolumny3x3, bomny3x3, lista_obrazkow)
        mapa_new.click("l", 0, 0)
        mapa_newA = {
            "0": ["1", "X", "X"],
            "1": ["X", "X", "X"],
            "2": ["X", "X", "X"]
            }
        assert mapa_newA == mapa_new._new_board
        mapa_new.click("l", 0, 2)
        mapa_newB = {
            "0": ["1", "1", " "],
            "1": ["X", "1", " "],
            "2": ["X", "1", " "]
            }
        assert mapa_newB == mapa_new._new_board
        assert mapa_new._outcome is False
        mapa_new.click("l", 0, 1)
        assert mapa_newB == mapa_new._new_board
        assert mapa_new._outcome is False
        mapa_new.click("l", 2, 0)
        mapa_newC = {
            "0": ["1", "1", " "],
            "1": ["X", "1", " "],
            "2": ["1", "1", " "]
            }
        assert mapa_newC == mapa_new._new_board
        assert mapa_new._outcome is True

    def test_right_click(self):
        Dict(wiersze3x3, kolumny3x3, bomny3x3, mapa_raw3x3)
        mapa_new = Play_board(wiersze3x3, kolumny3x3, bomny3x3, lista_obrazkow)
        mapa_new.click("l", 0, 0)
        mapa_newA = {
            "0": ["1", "X", "X"],
            "1": ["X", "X", "X"],
            "2": ["X", "X", "X"]
            }
        assert mapa_newA == mapa_new._new_board
        # oflagowanie punktu 0, 2
        mapa_new.click("p", 0, 2)
        mapa_newAA = {
            "0": ["1", "X", "F"],
            "1": ["X", "X", "X"],
            "2": ["X", "X", "X"]
            }
        assert mapa_new._outcome is False
        assert mapa_newAA == mapa_new._new_board
        # próba wciśnięcia punktu 0, 2 lewym przyciskiem - nieudana
        # mapa_newAA pozostaje bez zmian
        mapa_new.click("l", 0, 2)
        assert mapa_newAA == mapa_new._new_board
        # wciśniecie pola pod flagą - odkrycie sąsiednich pól pustych
        # bez oflagowanego miejsca
        mapa_new.click("l", 1, 2)
        mapa_newB = {
            "0": ["1", "1", "F"],
            "1": ["X", "1", " "],
            "2": ["X", "1", " "]
            }
        assert mapa_newB == mapa_new._new_board
        assert mapa_new._outcome is False
        # ponowna próba wciśnięcia oflagowanego miejsca - bez zmian
        mapa_new.click("l", 2, 0)
        mapa_newC = {
            "0": ["1", "1", "F"],
            "1": ["X", "1", " "],
            "2": ["1", "1", " "]
            }
        assert mapa_newC == mapa_new._new_board
        # odciśnięcie flagi "F" -> "X"
        # nadal nie skończyliśmy outcome = false
        mapa_new.click("p", 0, 2)
        mapa_newC = {
            "0": ["1", "1", "X"],
            "1": ["X", "1", " "],
            "2": ["1", "1", " "]
            }
        assert mapa_new._outcome is False
        # klikamy pozostały punkt 0, 2 i wygrywamy
        mapa_new.click("l", 0, 2)
        assert mapa_new._outcome is True
        assert mapa_new._win is True

    def test_wygrana(self):
        Dict(wiersze2x2, kolumny2x2, bomny2x2, mapa_raw2x2)
        mapa_new = Play_board(wiersze2x2, kolumny2x2, bomny2x2, lista_obrazkow)
        mapa_new.click("l", 0, 0)
        mapa_new_A = {
            "0": ["2", "X"],
            "1": ["X", "X"],
        }
        assert mapa_new_A == mapa_new._new_board
        mapa_new.click("p", 0, 0)
        assert mapa_new_A == mapa_new._new_board
        mapa_new.click("p", 0, 1)
        mapa_new_B = {
            "0": ["2", "F"],
            "1": ["X", "X"],
        }
        assert mapa_new_B == mapa_new._new_board
        assert mapa_new._outcome is False
        assert mapa_new._win is None
        mapa_new.click("l", 1, 1)
        mapa_new_C = {
            "0": ["2", "F"],
            "1": ["X", "2"],
        }
        assert mapa_new_C == mapa_new._new_board
        assert mapa_new._outcome is True
        assert mapa_new._win is True

    def test_klikniecie_na_bombe(self):
        Dict(wiersze2x2, kolumny2x2, bomny2x2, mapa_raw2x2)
        mapa_new = Play_board(wiersze2x2, kolumny2x2, bomny2x2, lista_obrazkow)
        mapa_new.click("p", 0, 1)
        mapa_new_B = {
            "0": ["X", "F"],
            "1": ["X", "X"],
        }
        assert mapa_new_B == mapa_new._new_board
        assert mapa_new._outcome is False
        assert mapa_new._win is None
        mapa_new.click("l", 1, 0)
        mapa_new_C = {
            "0": ["X", "B"],
            "1": ["B", "X"],
        }
        assert mapa_new_C == mapa_new._new_board
        assert mapa_new._outcome is True
        assert mapa_new._win is False

    def test_win_only_flagi(self):
        Dict(wiersze2x2, kolumny2x2, bomny2x2, mapa_raw2x2)
        mapa_new = Play_board(wiersze2x2, kolumny2x2, bomny2x2, lista_obrazkow)
        mapa_new.click("p", 0, 1)
        mapa_new.click("p", 1, 0)
        mapa_new_B = {
            "0": ["X", "F"],
            "1": ["F", "X"],
        }
        assert mapa_new_B == mapa_new._new_board
        assert mapa_new._outcome is False
        assert mapa_new._win is None
        mapa_new.click("l", 0, 0)
        assert mapa_new._outcome is False
        assert mapa_new._win is None
        mapa_new.click("l", 1, 1)
        mapa_new_C = {
            "0": ["2", "F"],
            "1": ["F", "2"],
        }
        assert mapa_new_C == mapa_new._new_board
        assert mapa_new._outcome is True
        assert mapa_new._win is True

    def test_win_only_miny(self):
        Dict(wiersze2x2, kolumny2x2, bomny2x2, mapa_raw2x2)
        mapa_new = Play_board(wiersze2x2, kolumny2x2, bomny2x2, lista_obrazkow)
        mapa_new.click("l", 1, 1)
        mapa_new.click("l", 0, 0)
        mapa_new_C = {
            "0": ["2", "X"],
            "1": ["X", "2"],
        }
        assert mapa_new_C == mapa_new._new_board
        assert mapa_new._outcome is True
        assert mapa_new._win is True
