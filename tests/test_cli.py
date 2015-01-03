import pytest

from clue import cli


class TestParseCard:
    def test_prefix(self):
        assert cli.parse_card('din') == 'dining room'

    def test_full(self):
        assert cli.parse_card('green') == 'green'

    def test_strip(self):
        assert cli.parse_card('  din ') == 'dining room'

    def test_case_insensitive(self):
        assert cli.parse_card('Revol') == 'revolver'

    def test_ambiguous(self):
        with pytest.raises(cli.UnknownCardError):
            cli.parse_card('b')

    def test_unknown(self):
        with pytest.raises(cli.UnknownCardError):
            cli.parse_card('foo')


class TestParsePlayer:
    def test_prefix(self):
        assert cli.parse_player('c', ['Carl', 'Kathy']) == 'Carl'

    def test_full(self):
        assert cli.parse_player('Kathy', ['Carl', 'Kathy']) == 'Kathy'

    def test_case_insensitive(self):
        assert cli.parse_player('kath', ['Carl', 'Kathy']) == 'Kathy'

    def test_ambiguous(self):
        with pytest.raises(cli.UnknownPlayerError):
            cli.parse_player('k', ['Kathy', 'Karissa'])

    def test_unknown(self):
        with pytest.raises(cli.UnknownPlayerError):
            cli.parse_player('foo', ['Carl', 'Kathy'])
