from .parser import Parser
from ..decorators import memoize
from .node import Node

class TemplateParser(Parser):

    def __init__(self, tokenizer, start_tag, end_tag):
        super().__init__(tokenizer)
        # TODO: validate tags, probably should not have whitespace
        # TODO: tags need to be list of tokens.
        self.start_tag = start_tag
        self.end_tag = end_tag

    def _skip_whitespace(self):
        """
        This method will check the next token and 
         - Return None if it is at the end of the code.
         - Return itself if it is a whitespace token and it will move the position ahead 1.
         - Return pos if it is any non whitespace token and it sets the position to current.
        """
        pos = self.mark()
        # end of code return none
        if self.at_end(pos):
            return None
        token = self.expect('WHTSPC')
        if token is None:
            self.reset(pos)
            return pos
        return self._skip_whitespace()

    def _next_token(self):
        """Returns the next token and if we reached the end throw an Error."""
        token = self.expect()
        if token is None:
            raise Exception("Ended")
        return token

    def run(self):
        """Should match and save code blocks and non-code blocks for processing."""
        # (non-code | code)+
        pos = self.mark()
        while True:
            if self._match_tag(self.start_tag):
                self._code()
            else:
                # Didn't match start so skip token
                token = self._next_token()
                # TODO: add token to non-code
                # Update end_pos
                end_pos = self.mark()
            if self.at_end():
                break

    def _match_tag(self, tag_tokens):
        """Returns True when the tag matches, otherwise returns False."""
        if len(tag_tokens) == 0:
            raise Exception("Tag is not defined!")
        pos = self.mark()
        for tag in tag_tokens:
            token = self.expect(typ=tag.typ, value=tag.value)
            if token is None:
                # the callee needs to decide what to do with the token
                # if it does not match, so the callee has to cycle the
                # next token forward.
                self.reset(pos)
                return False
        return True

    def _code(self):
        # code ::= start_tag block end_tag
        pos = self.mark()
        #
        if not self._match_tag(self.start_tag):
            return None
        #
        block = self._block()
        if self._match_tag(self._end_tag):
            return Node('code', block)
        # raise error?
        return None

    def _general_block(self):
        # block ::= (expression | statement)+
        pos = self.mark()
        results = []
        while True:
            element = self._block_element()
            if element:
                results.append(element)
            else:
                self.reset(pos)
                break
        return Node('block', results)

    def _block_element(self):
        # expression | statement
        pos = self.mark()
        stmt = self._statement()
        if stmt:
            return stmt
        expr = self._expression()
        if expr:
            return expr
        self.reset(pos)
        return None

    def _expression(self):
        # expression ::= (variable | ternary)";"
        pos = self.mark()
        expr = self._expression_element()
        if expr is None:
            # raise Error?
            self.reset(pos)
            return None
        #
        pos = self._skip_whitespace()
        semicolon = self.expect(typ="SEMICOLON")
        if semicolon is None:
            # raise Error?
            self.reset(pos)
            return None
        #
        return exrp

    def _expression_element(self):
        # variable | ternary
        pos = self.mark()
        variable = self._variable()
        pos = self._skip_whitespace()
        token = self.expect(typ="QMARK")
        if token:
            return self._ternary(variable)
        return variable

    def _variable(self):
        # variable ::= literal | identifier
        pos = self._skip_whitespace()
        identifier = self._identifier()
        if identifier:
            return identifier
        return self._literal()

    def _identifier(self):
        # identifier ::= id_char(id_char|integer)*
        first = self._identifier_char()
        if first is None:
            return None
        idents = [first]
        while True:
            token = self._identifier_char()
            if token:
                indents.append(token)
                continue
            token = self._integer()
            if token:
                indents.append(token)
            else:
                break
        return Node('identifier', idents)

    def _identifier_char(self):
        # id_char ::= name | "_"
        token = self.expect(typ="NAME")
        if token:
            return token
        token = self.expect(typ="UNDERSCORE")
        if token:
            return token
        return None

    def _integer(self):
        # integer ::= (digit)+
        # digit ::= <[0-9]>
        token = self.expect(typ="NUMBER")
        if token is None:
            return None
        if '.' in token.value:
            return None
        return token

    def _ternary(self, result):
        # ternary ::= variable "?" boolean_opr ":" variable
        # already matched to '?'
        condition = self._boolean_opr()
        pos = self._skip_whitespace()
        token = self.expect(typ="COLON")
        if token is None:
            raise Exception("Invalid ternary statement.")
        pos = self._skip_whitespace()
        other_result = self._variable()
        return Node('ternary', [result, condition, other_result])

    def _statement(self):
        # statement ::= assign | for_stmt | if_stmt
        pos = self.mark()
        end_stmt = False
        stmt = None
        tokens = []
        while not end_stmt:
            if self.at_end():
                break
            if self._match_tag(self.end_tag):
                break
            # Advance to next token
            pos = self._skip_whitespace()
            # Check if end of the line
            token = self.expect(typ="NEWLINE")
            if token:
                break
            # Just get next token
            token = self.expect()
            if token.typ == "NAME":
                pass
            elif token.typ == "for":
                self._for_loop_block()
            elif token.typ == "if":
                self._if_block()
            else:
                raise Exception("Invalid statement")
        return stmt

    def _assign_stmt(self):
        # assign ::= identifier "=" expression
        identifier = self._identifier()
        if identifier is None:
            return None
        pos = self._skip_whitespace()
        token = self.expect(typ="ASSIGN")
        if token is None:
            raise Exception("Invalid assignment Operation")
        expr = self._expression()
        if expr is None:
            raise Exception("Assignment is missing expression")
        return Node('assign', [identifier, expr])

    def _bracket_block(self):
        pos = self._skip_whitespace()
        token = self.expect(typ="CURLY", value="{")
        elements = []
        while True:
            
            # if self._at_end(pos):
            #     break
            # if self._match_tag(self.end_tag):
            #     break
            token = self.expect(typ="CURLY", value="}")
            if token:
                break
            element = self._block_element()
            if element:
                elements.append(element)
            else:
                # raise error?
                break
            pos = self._skip_whitespace()
        return Node('block', elements)

    def _conditional_stmt(self):
        cond_chain = [self._if_stmt()]
        while True:
            pos = self._skip_whitespace()
            if self.at_end(pos):
                break
            if self._match_tag(self.end_tag):
                break
            token = self.expect(typ="elif")
            if token:
                self.reset(pos)
                cond_chain.append(self._elif_stmt())
            pos = self._skip_whitespace()
            token = self.expect(typ="else")
            if token:
                self.reset(pos)
                cond_chain.append(self._else_stmt)
                break
        return Node("conditional", cond_chain)

    def _if_stmt(self):
        pos = self._skip_whitespace()
        token = self.expect(typ="if")
        if token is None:
            raise Exception("Invalid if statement")
        condition = self._boolean_opr()
        block = self._block()
        return Node("if", block)
    
    def _elif_stmt(self):
        pos = self._skip_whitespace()
        token = self.expect(typ="elif")
        if token is None:
            raise Exception("Invalid elif statement")
        condition = self._boolean_opr()
        block = self._block()
        return Node("if", block)
    
    def _else_stmt(self):
        pos = self._skip_whitespace()
        token = self.expect(typ="else")
        if token is None:
            raise Exception("Invalid else statement")
        block = self._block()
        return Node("else", block)

    def _for_stmt(self):
        # for_stmt ::= "for" identifier "in" array "{" block "}"
        pos = self._skip_whitespace()
        token = self.expect(typ="for")
        pos = self._skip_whitespace()
        #
        identifier = self._identifier()
        if identifier is None:
            raise Exception("Invalid for loop syntax")
        pos = self._skip_whitespace()
        #
        token = self.expect(typ="in")
        if token is None:
            raise Exception("Invalid for loop syntax")
        pos = self._skip_whitespace()
        #
        array = self._array()
        block = self._bracket_block()
        return Node("for", [identifier, array, block])

    def _boolean_opr(self):
        # boolean_opr ::= or_test
        pos = self._skip_whitespace()
        opr = self._or_test()
        return opr

    def _or_test(self):
        # or_test ::= and_test | or_test "||" and_test
        rhs = self._and_test()
        pos = self._skip_whitespace()
        token = self.expect(typ="OR")
        if token:
            lhs = self._boolean_opr()
            return Node("or", [lhs, rhs])
        return rhs

    def _and_test(self):
        # and_test ::= not_test | and_test "&&" not_test
        rhs = self._not_test()
        pos = self._skip_whitespace()
        token = self.expect(typ="AND")
        if token:
            lhs = self._boolean_opr()
            return Node("and", [lhs, rhs])
        return rhs

    def _not_test(self):
        # not_test ::= comparison | "!" not_test 
        pos = self._skip_whitespace()
        token = self.expect(typ="NOT")
        comp = self._comparison()
        if token:
            return Node("not", comp)
        return comp

    def _literal(self):
        # literal ::= array | basic_type
        pos = self._skip_whitespace()
        token = self.expect(typ="SQUARE")
        if token:
            return self._array(token)
        return self._basic_type()

    def _comparison(self):
        # comparison ::= variable (comp_opr variable)*
        # comp_opr ::= "<" | ">" | "==" | ">=" | "<=" | "!="
        lhs = self._variable()
        # <, >, <=, >=
        comp_opr = self._comparison_opr()
        if comp_opr is None:
            return lhs
        else:
            pos = self._skip_whitespace()
            rhs = self._variable()
            return Node(comp_opr, [lhs, rhs])

    def _comparison_opr(self):
        # comp_opr ::= "<" | ">" | "==" | ">=" | "<=" | "!="
        pos = self._skip_whitespace()
        # <, >, <=, >=
        token = self.expect(typ="ARROW")
        if token:
            val = "gt" if token.value == ">" else "lt"
            token = self.expect(typ="ASSIGN")
            if token:
                return f"{val}_equal"
            return val
        # !=
        token = self.expect(typ="NOT")
        if token:
            token = self.expect("ASSIGN")
            if token is None:
                self.reset(pos)
                raise Exception("Invalid != conditional statement")
            return 'not_equal'
        # ==
        token = self.expect(typ="ASSIGN")
        if token:
            token = self.expect("ASSIGN")
            if token is None:
                self.reset(pos)
                raise Exception("Invalid == comparison statement")
            return 'equal'
        return None

    def _assign(self, lhs):
        # Already matched the '='
        pos = self._skip_whitespace()
        token = self.expect(typ="NEWLINE")
        if token:
            raise Exception("Invalid assignment syntax")
        rhs = self._expression()
        return Node('assignment', [lhs, rhs])

    def _array(self, token):
        # array ::= "[" (array_item)+ "]" | "[]"
        # array_item ::= basic_type ("," basic_type)*
        # Already matched first SQUARE
        if token.value != '[':
            raise Exception("Array must start with '['.")
        values = []
        while True:
            pos = self._skip_whitespace()
            token = self.expect(typ="SQUARE", value="]")
            if token:
                # empty array
                break
            values.append(self._basic_type())
            pos = self._skip_whitespace()
            token = self.expect(typ="COMMA")
            if token is None:
                token = self.expect(typ="SQUARE", value="]")
                if token is None:
                    raise Exception('Invalid array format.')
                break
        return Node('array', values)

    def _basic_type(self):
        pos = self.mark()
        token = self.expect(typ="NUMBER")
        if token:
            return self._number(token)
        token = self.expect(typ="QUOTE")
        if token:
            return self._string(token.value)
        self.reset(pos)
        raise Exception("No Basic Type was found")

    def _number(self, token):
        if '.' in token.value:
            num = float(token.value)
        else:
            num = int(token.value)
        return Node("number", num)

    def _string(self, quote):
        # already matched first QUOTE
        chars = []
        while True:
            pos = self.mark()
            if self.at_end(pos):
                raise Exception(f"Error matching string type")
            token = self.expect(typ="QUOTE", value=quote)
            if token:
                break
            else:
                token = self._next_token()
                chars.append(token.value)
        return Node('string', ''.join(chars))
        