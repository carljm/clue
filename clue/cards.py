ROOMS = {
    'hall',
    'dining room',
    'billiard room',
    'ballroom',
    'kitchen',
    'study',
    'conservatory',
    'lounge',
    'library',
}

PEOPLE = {
    'green',
    'mustard',
    'scarlet',
    'plum',
    'white',
    'peacock',
}

WEAPONS = {
    'revolver',
    'rope',
    'lead pipe',
    'wrench',
    'candlestick',
    'knife',
}

DECK = ROOMS.union(PEOPLE.union(WEAPONS))


class InvalidTriple(ValueError):
    pass


class Triple:
    def __init__(self, person, weapon, room):
        if person not in PEOPLE:
            raise InvalidTriple("%s is not a person." % person)
        if weapon not in WEAPONS:
            raise InvalidTriple("%s is not a weapon." % weapon)
        if room not in ROOMS:
            raise InvalidTriple("%s is not a room." % room)
        self.person = person
        self.weapon = weapon
        self.room = room

    @property
    def all_cards(self):
        return [self.person, self.weapon, self.room]

    def __repr__(self):
        return "Triple(%r, %r, %r)" % (self.person, self.weapon, self.room)
