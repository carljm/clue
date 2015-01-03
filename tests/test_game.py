import pytest

from clue.exceptions import ImpossibleError
from clue.player import Player, Me
from clue import game


class TestGame:
    def test_others(self):
        g = game.Game(Me({}), [Player("Foo", 4), Player("Bar", 14)])

        assert len(g.others) == 2
        assert g.others[0].name == "Foo"
        assert g.others[0].num_cards == 4
        assert g.others[1].name == "Bar"
        assert g.others[1].num_cards == 14

    def test_me(self):
        g = game.Game(Me({'white'}), [Player("Foo", 17)])

        assert g.me.num_cards == 1
        assert g.me.has_cards == {'white'}

    def test_wrong_number_cards(self):
        with pytest.raises(ImpossibleError):
            game.Game(Me({}), [Player("Foo", 3)])

    def test_repr(self):
        g = game.Game(Me({'white'}), [Player("Foo", 17)])

        assert repr(g) == "Game(Me(['white']), [Player('Foo', 17)])"
