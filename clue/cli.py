from .cards import DECK


class UnknownCardError(Exception):
    pass


def parse_card(prefix):
    lowered = prefix.lower()
    candidates = [c for c in DECK if c.startswith(lowered)]
    if len(candidates) > 1:
        raise UnknownCardError("More than one card matches %s." % prefix)
    elif not candidates:
        raise UnknownCardError("No cards match %s." % prefix)
    return candidates[0]
