
class Parser:
    """The Parser class is a parent parser that contains the most basic parsing functions."""
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        # cache - should only be used by the memoize decorator 
        self.memos = {}
        # final position - end of tokens
        self.end_pos = None

    def mark(self):
        return self.tokenizer.mark()

    def reset(self, pos):
        self.tokenizer.reset(pos)

    def at_end(self, pos=None):
        # Check if end was ever reached
        if pos is None:
            return self.end_pos is not None
        # Check if given position is end position. 
        return self.end_pos == pos

    def expect(self, typ=None, value=None):
        try:
            token = self.tokenizer.peek_token()
            # just get next token
            if typ is None and value is None:
                return self.tokenizer.get_token()
            # match both typ and value
            if typ is not None and value is not None:
                if token.typ == typ and token.value == value:
                    return self.tokenizer.get_token()
                else:
                    return None
            # just match typ
            if typ is not None and token.typ == typ:
                return self.tokenizer.get_token()
            # just match value
            if value is not None and token.value == value:
                return self.tokenizer.get_token()
            # no match
            return None
        except StopIteration:
            self.end_pos = self.tokenizer.pos
            return None
        except Exception:
            raise Exception('parsing error')