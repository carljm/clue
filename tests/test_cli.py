from unittest import mock

import pytest

from clue import cli


@pytest.fixture
def mock_input(request, monkeypatch):
    m = mock.Mock()
    monkeypatch.setattr('builtins.input', m)
    if 'inputs' in request.keywords:
        inputs = list(reversed(request.keywords['inputs'].args))
        m.side_effect = lambda x: inputs.pop()
    return m


class TestReadGame:
    @pytest.mark.inputs(
        'din,ha,wh',
        'Barb', '4',
        'Elaine', '',
        'Kathy', '',
        'Mark', '',
        'Bobby', '',
    )
    def test_read_game(self, mock_input):
        g = cli.read_game()

        assert g.me.num_cards == 3
        assert g.me.has_cards == {'dining room', 'hall', 'white'}
        assert [(p.name, p.num_cards) for p in g.others] == [
            ("Barb", 4), ("Elaine", 3), ("Kathy", 3), ("Mark", 3), ("Bobby", 2)
        ]


class TestReadTriple:
    def test_triple(self, mock_input):
        mock_input.return_value = 'ro,plum,ha'

        t = cli.read_triple("Hey")

        assert t.room == 'hall'
        assert t.weapon == 'rope'
        assert t.person == 'plum'

    @pytest.mark.inputs('ro,rev,ha', 'din,wh,le')
    def test_bad_triple(self, mock_input, capsys):
        t = cli.read_triple("Hey")

        assert t.room == 'dining room'
        assert t.weapon == 'lead pipe'
        assert t.person == 'white'
        assert mock_input.call_count == 2
        out, err = capsys.readouterr()
        assert out == "Need a person, a weapon, and a room.\n"


class TestReadCards:
    def test_read_cards(self, mock_input):
        mock_input.return_value = 'din,wh'
        ret = cli.read_cards("Yo")

        assert ret == ['dining room', 'white']

    @pytest.mark.inputs('foo, wh', 'ha, wh')
    def test_bad_card(self, mock_input, capsys):
        ret = cli.read_cards("Yo")

        assert ret == ['hall', 'white']
        assert mock_input.call_count == 2
        out, err = capsys.readouterr()
        assert out == "No card matches foo.\n"


class TestReadPlayer:
    @pytest.mark.inputs('Kathy', '3')
    def test_read_player(self, mock_input):
        p = cli.read_player("P1", 4)

        assert p.name == "Kathy"
        assert p.num_cards == 3
        mock_input.assert_any_call("Name [P1] ")
        mock_input.assert_any_call("How many cards does Kathy have? [4] ")

    @pytest.mark.inputs('', '')
    def test_use_defaults(self, mock_input):
        p = cli.read_player("P1", 4)

        assert p.name == "P1"
        assert p.num_cards == 4


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


class TestRead:
    def test_simple(self, mock_input):
        mock_input.return_value = "yo"
        ret = cli._read("Foo")

        assert ret == "yo"
        mock_input.assert_called_with("Foo ")

    def test_default_used(self, mock_input):
        mock_input.return_value = ''
        ret = cli._read("Hey", default="def")

        assert ret == "def"
        mock_input.assert_called_with("Hey [def] ")

    def test_default_not_used(self, mock_input):
        mock_input.return_value = 'not'
        ret = cli._read("Hey", default="def")

        assert ret == "not"
        mock_input.assert_called_once_with("Hey [def] ")

    def test_coerce_to(self, mock_input):
        mock_input.return_value = '3'
        ret = cli._read("Hey", coerce_to=int)

        assert ret == 3

    @pytest.mark.inputs('foo', '5')
    def test_coerce_fail(self, mock_input, capsys):
        ret = cli._read("Hey", coerce_to=int)

        assert ret == 5
        assert mock_input.call_count == 2
        out, err = capsys.readouterr()
        assert out == "Sorry, I don't understand that.\n"

    @pytest.mark.inputs('', 'foo')
    def test_required_fail(self, mock_input, capsys):
        ret = cli._read("Hey", required=True)

        assert ret == 'foo'
        assert mock_input.call_count == 2
        out, err = capsys.readouterr()
        assert out == "Can't go on without an answer!\n"
