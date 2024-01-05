import pytest

from zenerator.peg_parser import Tokenizer, TokenGenerator

########################################################################
# Test TokenGenerator
########################################################################
class TestTokenGenerator:

    def test_token_generator(self):
        tg = TokenGenerator()
        code = "x = 41.0"
        # Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
        expected_tokens = [
            tg.Token('NAME', 'x', 1, 0),
            tg.Token('WHTSPC', ' ', 1, 1),
            tg.Token('ASSIGN', '=', 1, 2),
            tg.Token('WHTSPC', ' ', 1, 3),
            tg.Token('NUMBER','41.0', 1, 4)]
        i = 0
        for actual in tg.generate_tokens(code):
            expected = expected_tokens[i]
            # Check that tokens are equal
            assert actual.typ == expected.typ
            assert actual.value == expected.value
            assert actual.line == expected.line
            assert actual.column == expected.column
            i += 1

########################################################################
# Test Tokenizer
########################################################################
class TestTokenizer:

    def test_simple_get_token(self):
        # Arrange
        code = "x = 41.0"
        scanner = Tokenizer(code)
        # Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
        tg = TokenGenerator()
        expected_tokens = [
            tg.Token('NAME', 'x', 1, 0),
            tg.Token('WHTSPC', ' ', 1, 1),
            tg.Token('ASSIGN', '=', 1, 2),
            tg.Token('WHTSPC', ' ', 1, 3),
            tg.Token('NUMBER','41.0', 1, 4)]
        # Assert
        expected_pos = 0
        for expected in expected_tokens:
            actual = scanner.get_token()
            expected_pos += 1
            assert actual == expected
            assert scanner.pos == expected_pos
    
    def test_reset(self):
        # Arrange
        code = "x = 41.0"
        scanner = Tokenizer(code)
        scanner.reset(50)
        assert scanner.pos == 50
        scanner.reset(0)
        assert scanner.pos == 0
        scanner.reset(-1)
        assert scanner.pos == -1
        
