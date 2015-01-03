from .cards import DECK, ROOMS, WEAPONS, PEOPLE, Triple
from .game import Game
from .player import Player, Me


class CliError(Exception):
    pass


class UnknownCardError(CliError):
    pass


class UnknownPlayerError(CliError):
    pass


def read_game():
    """Query the user about the initial game setup (players and cards)."""
    my_cards = read_cards("My cards (comma-separated):")
    print("My cards are %r" % my_cards)
    me = Me(my_cards)
    others = []
    cards_so_far = me.num_cards
    print("Tell me about the other players, starting from my left.")
    while cards_so_far < Game.num_player_cards:
        default_name = "Player %s" % (len(others) + 1)
        max_cards = Game.num_player_cards - cards_so_far
        default_num_cards = min(3, max_cards)
        player = read_player(
            default_name, default_num_cards, max_cards=max_cards)
        others.append(player)
        cards_so_far += player.num_cards
    return Game(me, others)


def read_triple(prompt):
    """Query user for a person/weapon/room triple."""
    while True:
        cards = read_cards(prompt)
        rooms = [c for c in cards if c in ROOMS]
        weapons = [c for c in cards if c in WEAPONS]
        people = [c for c in cards if c in PEOPLE]
        if any(len(l) != 1 for l in [rooms, weapons, people]):
            print("Need a person, a weapon, and a room.")
            continue
        return Triple(people[0], weapons[0], rooms[0])


def read_cards(prompt):
    """Query user for any non-empty list of valid cards."""
    while True:
        cards = _read(prompt, required=True).split(',')
        try:
            return [parse_card(c) for c in cards]
        except UnknownCardError as e:
            print(e)


def read_player(default_name, default_num_cards=3, max_cards=None):
    """Query user for name of a player."""
    name = _read("Name", default=default_name)
    while True:
        num_cards = _read(
            "How many cards does %s have?" % name,
            default=default_num_cards,
            coerce_to=int,
        )
        print("got %s" % num_cards)
        if max_cards and num_cards > max_cards:
            if max_cards == 1:
                msg = "There's only 1 card"
            else:
                msg = "There're only %s cards" % max_cards
            print("%s left for %s!" % (msg, name))
            continue
        return Player(name, num_cards)


def parse_card(prefix):
    """Parse a valid card from given unambiguous prefix."""
    return _parse(prefix, DECK, UnknownCardError, 'card')


def parse_player(prefix, names):
    """Parse a valid player name from given unambiguous prefix."""
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
                print("Can't go on without an answer!")
            else:
                return val


def _parse(prefix, options, exception_class, option_type):
    """Select one of ``options`` based on unambiguous ``prefix``."""
    canonical = prefix.lower().strip()
    candidates = [o for o in options if o.lower().startswith(canonical)]
    if len(candidates) > 1:
        raise exception_class(
            "More than one %s matches %s." % (option_type, prefix))
    elif not candidates:
        raise exception_class("No %s matches %s." % (option_type, prefix))
    return candidates[0]
