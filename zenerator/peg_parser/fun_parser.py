from .parser import Parser
from .node import Node
from ..decorators import memoize, memoize_left_recur
class FunParser(Parser):
    @memoize
    def statement(self):
        a = self.assignment()
        if a:
            return a
        e = self.expr()
        if e:
            return e
        i = self.conditional()
        if i:
            return i
        return None

    def assignment(self):
        pos = self.mark()
        target = self.expect("NAME")
        if target:
            if self.expect('='):
                e = self.expr()
                if e:
                    return Node('assign', [target, e])
        self.reset(pos)
        return None

    # def expr(self):
    #     t = self.term()
    #     if t:
    #         pos = self.mark()
    #         op = self.expect("+")
    #         if op:
    #             e = self.expr()
    #             if e:
    #                 return Node('add', [t, e])
    #         self.reset(pos)
    #         op = self.expect("-")
    #         if op:
    #             e = self.expr()
    #             if e:
    #                 return Node('subtract', [t, e])
    #         self.reset(pos)
    #         return t
    #     return None

    @memoize_left_recur
    def expr(self):
        pos = self.mark()
        e = self.expr()
        opr = self.expect("OPR")
        t = self.term()
        if e and opr and t:
            if opr.value == '+':
                return Node('add', [e, t])
            elif opr.value == '-':
                return Node('subtract', [e, t])
        self.reset(pos)
        t = self.term()
        if t:
            return Node('term', [t])
        self.reset(pos)
        return None

    @memoize_left_recur
    def term(self):
        pos = self.mark()
        t = self.term()
        opr = self.expect("OPR")
        a = self.atom()
        if t and opr and a:
            if opr.value == '*':
                return Node('multiply', [t, a])
            elif opr.value == '/':
                return Node('divide', [t, a])
        self.reset(pos)
        a = self.atom()
        if a:
            return a
        self.reset(pos)
        return None

    # def term(self):
    #     a = self.atom()
    #     if a:
    #         pos = self.mark()
    #         op = self.expect("*")
    #         if op:
    #             t = self.term()
    #             if t:
    #                 return Node('multiply', [a, t])
    #         self.reset(pos)
    #         op = self.expect("/")
    #         if op:
    #             t = self.term()
    #             if t:
    #                 return Node('divide', [a, t])
    #         self.reset(pos)
    #         return a
    #     return None

    def atom(self):
        token = self.expect("NAME")
        if token:
            return token
        token = self.expect("NUMBER")
        if token:
            return token
        pos = self.mark()
        if self.expect("("):
            e = self.expr()
            if e:
                if self.expect(")"):
                    return e
        self.reset(pos)
        return None

    def conditional(self):
        pos = self.mark()
        if self.expect('if'):
            e = self.expr()
            if e and self.expect(':'):
                stmt = self.statement()
                if stmt:
                    return Node('if', [e, stmt])
        self.reset(pos)
        return None
