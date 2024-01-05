import pytest

from zenerator.peg_parser import Tokenizer, Parser

########################################################################
# Test TokenGenerator
########################################################################
class TestParser:

    def test_simple_expect(self):
        # Arrange
        code = "x = 41.0"
        scanner = Tokenizer(code)
        parser = Parser(scanner)
        # expected_tokens:
        #   Token('NAME', 'x', 1, 0)
        #   Token('WHTSPC', ' ', 1, 1)
        #   Token('ASSIGN', '=', 1, 2)
        #   Token('WHTSPC', ' ', 1, 3)
        #   Token('NUMBER','41.0', 1, 4)
        # Assert
        assert parser.mark() == 0
        # Should match by typ
        token = parser.expect(typ="NAME")
        assert token.typ == "NAME"
        assert token.value == "x"
        assert parser.mark() == 1
        # Should skip and return token.
        token = parser.expect()
        assert token.typ == "WHTSPC"
        assert parser.mark() == 2
        # Should match by value
        token = parser.expect(value="=")
        assert token.typ == "ASSIGN"
        assert token.value == "="
        assert parser.mark() == 3
        # Should not match and not move forward
        token = parser.expect(typ="no_match")
        assert token == None
        assert parser.mark() == 3
        # Should skip
        token = parser.expect()
        assert token.typ == "WHTSPC"
        assert parser.mark() == 4
        # Should match
        token = parser.expect(typ="NUMBER")
        assert token.typ == "NUMBER"
        assert token.value == "41.0"
        assert parser.mark() == 5
        # Should return None because it is at the end.
        token = parser.expect(None)
        assert token == None
        assert parser.mark() == 5

    def test_parser_expect_error(self):
        # Arrange
        code = "x = 41.0"
        scanner = Tokenizer(code)
        parser = Parser(scanner)
        # Act
        parser.reset(50)
        with pytest.raises(Exception) as exc:
            parser.expect(typ="NAME")
        assert str(exc.value) == "parsing error"

