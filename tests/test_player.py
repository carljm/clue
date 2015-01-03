import pytest

from clue.cards import Triple, DECK
from clue.exceptions import ImpossibleError
from clue import player


class TestPlayer:
    def test_has_card(self):
        p = player.Player("Foo", 3)

        p.has_card('green')

        assert p.has_cards == {'green'}

    def test_has_too_many(self):
        p = player.Player("Foo", 3)

        p.has_card('green')
        p.has_card('hall')
        p.has_card('white')

        with pytest.raises(ImpossibleError):
            p.has_card('rope')

    def test_has_same(self):
        p = player.Player("Foo", 3)

        p.has_card('green')
        p.has_card('green')

        assert p.has_cards == {'green'}

    def test_ask(self):
        p = player.Player("Foo", 3)
        t = Triple('white', 'rope', 'hall')

        p.ask(t)

        assert p.asked == [t]

    def test_show(self):
        p = player.Player("Foo", 3)
        t = Triple('white', 'rope', 'hall')

        p.show(t)

        assert p.shown == [t]

    def test_show_impossible(self):
        p = player.Player("Foo", 3)
        t = Triple('white', 'rope', 'hall')

        p.not_has_cards = {'green', 'white', 'rope', 'hall'}

        with pytest.raises(ImpossibleError):
            p.show(t)

    def test_noshow(self):
        p = player.Player("Foo", 3)
        t = Triple('white', 'rope', 'hall')

        p.noshow(t)

        assert p.not_has_cards == {'white', 'rope', 'hall'}

    def test_noshow_impossible(self):
        p = player.Player("Foo", 3)
        t = Triple('white', 'rope', 'hall')

        p.has_cards = {'rope'}

        with pytest.raises(ImpossibleError):
            p.noshow(t)

    def test_check_good(self):
        p = player.Player("Foo", 3)

        p.has_cards = {'green', 'rope'}
        p.not_has_cards == {'white', 'revolver'}

        p.check()

    def test_check_bad(self):
        p = player.Player("Foo", 3)

        p.has_cards = {'white', 'rope'}
        p.not_has_cards = {'white', 'revolver'}

        with pytest.raises(ImpossibleError):
            p.check()

    def test_repr(self):
        p = player.Player("Foo", 3)

        assert repr(p) == "Player('Foo', 3)"


class TestMe:
    def test_init(self):
        m = player.Me({'white', 'green', 'hall'})

        assert m.has_cards == {'white', 'green', 'hall'}
        assert m.num_cards == 3
        assert m.not_has_cards == set(DECK).difference(m.has_cards)

    def test_dupes(self):
        m = player.Me(['white', 'green', 'hall', 'white'])

        assert m.has_cards == {'white', 'green', 'hall'}
        assert m.num_cards == 3
        assert m.not_has_cards == set(DECK).difference(m.has_cards)

    def test_repr(self):
        m = player.Me(['plum', 'wrench', 'hall'])

        assert repr(m) == "Me(['hall', 'plum', 'wrench'])"
