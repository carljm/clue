from . import cards
from .exceptions import ImpossibleError


class Game:
    """Provide list of players in order from my left, and list of my cards.

    Each player should be a (name, num-cards) tuple.
    """
    num_player_cards = len(cards.DECK) - 3

    def __init__(self, me, others):
        self.others = others
        self.others_by_name = {p.name: p for p in others}
        if len(self.others_by_name) != len(self.others):
            raise ImpossibleError("Player names must be unique.")
        self.me = me
        total_cards = self.me.num_cards + sum(
            [p.num_cards for p in self.others])
        if total_cards != self.num_player_cards:
            raise ImpossibleError(
                "%s cards held by players, should be %s."
                % (total_cards, self.num_player_cards)
            )

    def snapshot(self):
        return self.__class__(
            self.me.snapshot(),
            [p.snapshot() for p in self.others]
        )

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.me, self.others)
