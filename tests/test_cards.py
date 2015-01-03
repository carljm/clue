import pytest

from clue import cards


class TestTriple:
    def test_invalid_person(self):
        with pytest.raises(cards.InvalidTriple):
            cards.Triple('foo', 'rope', 'hall')

    def test_invalid_weapon(self):
        with pytest.raises(cards.InvalidTriple):
            cards.Triple('green', 'foo', 'hall')

    def test_invalid_room(self):
        with pytest.raises(cards.InvalidTriple):
            cards.Triple('green', 'rope', 'foo')

    def test_person(self):
        t = cards.Triple('green', 'rope', 'hall')

        assert t.person == 'green'

    def test_weapon(self):
        t = cards.Triple('green', 'rope', 'hall')

        assert t.weapon == 'rope'

    def test_room(self):
        t = cards.Triple('green', 'rope', 'hall')

        assert t.room == 'hall'

    def test_all_cards(self):
        t = cards.Triple('green', 'rope', 'hall')

        assert t.all_cards == ['green', 'rope', 'hall']

    def test_repr(self):
        t = cards.Triple('green', 'rope', 'hall')

        assert repr(t) == "Triple('green', 'rope', 'hall')"
