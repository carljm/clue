import pytest

from clue.exceptions import ImpossibleError
from clue import game


class TestGame:
    def test_other_names(self):
        g = game.Game([("Foo", 3), ("Bar", 15)], {})

        assert g.other_names == ["Foo", "Bar"]

    def test_others(self):
        g = game.Game([("Foo", 4), ("Bar", 14)], {})

        assert len(g.others) == 2
        assert g.others[0].name == "Foo"
        assert g.others[0].num_cards == 4
        assert g.others[1].name == "Bar"
        assert g.others[1].num_cards == 14

    def test_me(self):
        g = game.Game([("Foo", 17)], {'white'})

        assert g.me.num_cards == 1
        assert g.me.has_cards == {'white'}

    def test_wrong_number_cards(self):
        with pytest.raises(ImpossibleError):
            game.Game([("Foo", 3)], {})
