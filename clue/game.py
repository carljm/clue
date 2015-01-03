from . import cards
from .exceptions import ImpossibleError


class Game:
    """Provide list of players in order from my left, and list of my cards.

    Each player should be a (name, num-cards) tuple.
    """
    player_num_cards = len(cards.DECK) - 3

    def __init__(self, me, others):
        self.others = others
        self.me = me
        total_cards = self.me.num_cards + sum(
            [p.num_cards for p in self.others])
        if total_cards != self.player_num_cards:
            raise ImpossibleError(
                "%s cards held by players, should be %s."
                % (total_cards, self.player_num_cards)
            )
