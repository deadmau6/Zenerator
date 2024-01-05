import pytest

from zenerator.peg_parser import TokenGenerator, Tokenizer, Parser, TemplateParser

class TestTemplateParser:
    
    def test_match_tag(self):
        tag = "ATAG_BTAG"
        tag_tokens = [t for t in TokenGenerator().generate_tokens(tag)]
        #
        code = "TATAG_ATAG_TAG_ATAG_BTAG"
        scanner = Tokenizer(code)
        template_parser = TemplateParser(scanner, tag, tag)
        #
        unmatched_tokens = ['TATAG', '_', 'ATAG', '_', 'TAG', '_']
        for i in range(len(unmatched_tokens)):
            # This will pass through all of the unmatched_tokens
            res = template_parser._match_tag(tag_tokens)
            pos = template_parser.mark()
            assert res == False
            assert pos == i
            # Move the head to the next token
            token = template_parser._next_token()
        # Finally we should be set on the last 'ATAG' token.
        res = template_parser._match_tag(tag_tokens)
        assert res == True

    def test_string_single_quote(self):
        #
        code = ['should',' ','not',' ',"'", 'should',' ','pass',"'",' ',"'","definetly",' ','should',' ','not']
        scanner = Tokenizer("".join(code))
        template_parser = TemplateParser(scanner, "start", "end")
        #
        with pytest.raises(Exception) as error:
            template_parser._basic_type()
            print(error)
            assert error.message == "No Basic Type was found"
        # move to first quote
        for i in range(4):
            t = template_parser._next_token()
        #
        node = template_parser._basic_type()
        assert node.typ == "string"
        assert node.children == ''.join(code[5:8])
        #
        pos = template_parser._skip_whitespace()
        #
        with pytest.raises(Exception) as error:
            t = template_parser._basic_type()
            assert error.message == "Error matching string type"

