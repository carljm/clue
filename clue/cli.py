from .cards import DECK
from .game import Game
from .player import Player, Me


class CliError(Exception):
    pass


class UnknownCardError(CliError):
    pass


class UnknownPlayerError(CliError):
    pass


def read_game():
    my_cards = read_cards("Your cards (separate with commas):")
    me = Me(my_cards)
    others = []
    cards_so_far = me.num_cards
    print("Tell me about the other players, starting from my left.")
    while cards_so_far < Game.player_num_cards:
        default_name = "Player %s" % (len(others) + 1)
        default_num_cards = min(3, Game.player_num_cards - cards_so_far)
        player = read_player(default_name, default_num_cards)
        others.append(player)
        cards_so_far += player.num_cards
    return Game(me, others)


def read_cards(prompt):
    cards = _read(prompt, required=True).split(',')
    while True:
        try:
            return [parse_card(c) for c in cards]
        except UnknownCardError as e:
            print(e)


def read_player(default_name, default_num_cards=3):
    name = _read("Name", default=default_name)
    num_cards = _read("# cards", default=default_num_cards, coerce_to=int)
    return Player(name, num_cards)


def parse_card(prefix):
    return _parse(prefix, DECK, UnknownCardError, 'card')


def parse_player(prefix, names):
    return _parse(prefix, names, UnknownPlayerError, 'player')


def _read(prompt, default=None, required=False, coerce_to=str):
    """Read a value from input with a default, and optional type coercion."""
    if default is not None:
        full_prompt = "%s [%s] " % (prompt, default)
    else:
        full_prompt = "%s " % prompt

    while True:
        raw = input(full_prompt)
        try:
            val = coerce_to(raw) if raw else default
        except (TypeError, ValueError):
            print("Sorry, I don't understand that.")
        else:
            if required and not val:
                print("Can't go on without an answer here!")
            return val


def _parse(prefix, options, exception_class, option_type):
    canonical = prefix.lower().strip()
    candidates = [o for o in options if o.lower().startswith(canonical)]
    if len(candidates) > 1:
        raise exception_class(
            "More than one %s matches %s." % (option_type, prefix))
    elif not candidates:
        raise exception_class("No %s matches %s." % (option_type, prefix))
    return candidates[0]
