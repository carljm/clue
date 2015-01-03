from . import cards
from . import player
from .exceptions import ImpossibleError


class Game:
    """Provide list of players in order from my left, and list of my cards.

    Each player should be a (name, num-cards) tuple.
    """
    def __init__(self, player_data, my_cards):
        self.other_names = [d[0] for d in player_data]
        self.others = [player.Player(*d) for d in player_data]
        self.me = player.Me(my_cards)
        total_cards = self.me.num_cards + sum(
            [p.num_cards for p in self.others])
        target = len(cards.DECK) - 3
        if total_cards != target:
            raise ImpossibleError(
                "%s cards held by players, should be %s."
                % (total_cards, target)
            )
