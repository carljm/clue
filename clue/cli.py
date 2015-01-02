from .cards import DECK


class CliError(Exception):
    pass


class UnknownCardError(CliError):
    pass


class UnknownPlayerError(CliError):
    pass


def parse_card(prefix):
    return _parse(prefix, DECK, UnknownCardError, 'card')


def parse_player(prefix, names):
    return _parse(prefix, names, UnknownPlayerError, 'player')


def _parse(prefix, options, exception_class, option_type):
    lowered = prefix.lower()
    candidates = [o for o in options if o.lower().startswith(lowered)]
    if len(candidates) > 1:
        raise exception_class(
            "More than one %s matches %s." % (option_type, prefix))
    elif not candidates:
        raise exception_class("No %s matches %s." % (option_type, prefix))
    return candidates[0]
