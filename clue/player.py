from . import cards
from .exceptions import ImpossibleError


class Player:
    def __init__(self, name, num_cards):
        self.name = name
        # number of cards this player holds
        self.num_cards = num_cards
        # set of cards this player is known to have
        self.has_cards = set()
        # set of cards this player is known NOT to have
        self.not_has_cards = set()
        # list of triples asked about
        self.asked = []
        # list of triples of which one has been shown to someone
        self.shown = []

    def has_card(self, card):
        self.has_cards.add(card)
        if len(self.has_cards) > self.num_cards:
            raise ImpossibleError(
                "%s has only %s cards but has shown %r" % (
                    self.name, self.num_cards, self.has_cards)
            )

    def ask(self, triple):
        self.asked.append(triple)

    def show(self, triple):
        if set(triple.all_cards).issubset(self.not_has_cards):
            raise ImpossibleError(
                "%s showed one of %s, but earlier declined to show all those."
                % (self.name, triple)
            )
        self.shown.append(triple)

    def noshow(self, triple):
        has = self.has_cards.intersection(triple.all_cards)
        if has:
            raise ImpossibleError(
                "%s declined for %s, but we know they have %s" %
                (self.name, triple.all_cards, has)
            )
        self.not_has_cards.update(triple.all_cards)

    def check(self):
        impossible = self.has_cards.intersection(self.not_has_cards)
        if impossible:
            raise ImpossibleError(
                "%s is known to have and known to not have %r"
                % (self.name, impossible)
            )

    def snapshot(self):
        s = self.__class__(self.name, self.num_cards)
        s.has_cards = self.has_cards.copy()
        s.not_has_cards = self.not_has_cards.copy()
        s.asked = self.asked.copy()
        s.shown = self.shown.copy()
        return s

    def __repr__(self):
        return "%s(%r, %r)" % (
            self.__class__.__name__, self.name, self.num_cards)


class Me(Player):
    def __init__(self, my_cards):
        my_cards = set(my_cards)
        super().__init__("Me", len(my_cards))
        self.has_cards.update(my_cards)
        self.not_has_cards = set(cards.DECK).difference(self.has_cards)

    def snapshot(self):
        s = self.__class__(self.has_cards)
        s.asked = self.asked.copy()
        s.shown = self.shown.copy()
        return s

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, sorted(self.has_cards))
