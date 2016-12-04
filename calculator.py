# -*- coding: utf-8 -*-


def debug_type(_var, _type):
    return "%s should be %s type." % (_var, _type)


class Node:
    left_paren = "[{("
    right_paren = ")}]"
    paren = left_paren + right_paren
    digit = '1234567890'
    dot = '.'
    numeric = dot + digit
    binary_op = '+-*/%'
    unary_op = 'EL'
    op = binary_op + unary_op

    def __init__(self, _expr):
        assert isinstance(_expr, str), debug_type("_expr", "str")
        self.value = 0.0
        self.archive(_expr)
        pass

    def __str__(self):
        return "%s" % self.value

    def archive(self, _expr):
        _expr = _expr.strip()
        if _expr[0] == Node.dot:
            _expr = '0' + _expr
        elif _expr[-1] == Node.dot:
            _expr += '0'

        if _expr.isnumeric():
            # number
            self.value = float(_expr)
        elif _expr in self.paren:
            # parenthesis
            self.value = _expr
        else:
            # otherwise
            self.value = _expr

    pass


class Parser:
    def __init__(self, _expr):
        assert isinstance(_expr, str), debug_type("_expr", "str")
        assert self.is_valid(_expr), "Invalid syntax: %s" % _expr
        self.expr = _expr
        pass

    def parse(self):
        result = []

        val = ''
        for s in self.expr:
            if s in Node.op + Node.paren:
                if val:
                    result.append(str(Node(val)))
                result.append(str(Node(s)))
                val = ''
            elif s in Node.numeric:
                val += s
            elif s == ' ':
                pass
            else:
                raise AssertionError("Invalid expr")
        if val:
            result.append(str(Node(val)))

        return result

    def is_valid(self, _expr):
        _val = 0
        _flag = True
        for s in _expr:
            if s in Node.left_paren:
                _val += 1
                _flag = True
            elif s in Node.right_paren:
                _val -= 1
                _flag = True
            elif s == Node.dot:
                if _flag:
                    _flag = False
                else:
                    return False
            elif s in " " + Node.numeric + Node.op:
                _flag = True

        return _val == 0
    pass


if __name__ == "__main__":
    expr1 = '1+2'
    expr2 = '2*3'
    expr3 = '4%.2'
    expr4 = '1.0/2. 3'
    expr5 = '(E2) + {L.3}'
    p1 = Parser(expr1)
    p2 = Parser(expr2)
    p3 = Parser(expr3)
    p4 = Parser(expr4)
    p5 = Parser(expr5)
    print(list(map(str, p1.parse())))
    print(list(map(str, p2.parse())))
    print(list(map(str, p3.parse())))
    print(list(map(str, p4.parse())))
    print(list(map(str, p5.parse())))
    print('02.0'.isnumeric())
    print(float('02'))

    pass


