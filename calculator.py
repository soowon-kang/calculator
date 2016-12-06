# -*- coding: utf-8 -*-
import math


def debug_type(_var, _type):
    return "%s should be %s type." % (_var, _type)


class Node:
    left_paren = "[{("
    right_paren = ")}]"
    paren = left_paren + right_paren
    digit = '1234567890'
    dot = '.'
    numeric = dot + digit
    binary_op = '+-*/%^'
    unary_op = 'EL'
    op = binary_op + unary_op
    lev0_op = paren
    lev1_op = unary_op
    lev2_op = '*/%^'
    lev3_op = '+-'

    def __init__(self, _expr):
        assert isinstance(_expr, (str, float)), \
            debug_type("_expr", "str or float")
        self.value = None
        self.priority = -1
        self.archive(_expr)
        pass

    def __str__(self):
        return "%s" % self.value

    def archive(self, _expr):
        try:
            # number
            self.value = float(_expr)
        except ValueError:
            if isinstance(_expr, str):
                _expr = _expr.strip()
            self.value = _expr
            if _expr in self.paren:
                # parenthesis
                self.value = _expr
                self.priority = 4
            else:
                # otherwise
                self.value = _expr
                if _expr in self.lev1_op:
                    self.priority = 1
                elif _expr in self.lev2_op:
                    self.priority = 2
                elif _expr in self.lev3_op:
                    self.priority = 3

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
                    result.append(Node(val))
                result.append(Node(s))
                val = ''
            elif s in Node.numeric:
                val += s
            elif s == ' ':
                pass
            else:
                raise AssertionError("Invalid expr")
        if val:
            result.append(Node(val))

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


class Calculator:
    def __init__(self, _expr):
        assert isinstance(_expr, str), debug_type("_expr", "str")
        self.infix_expr = []
        self.is_valid(_expr)
        for e in self.infix_expr:
            assert isinstance(e, Node), debug_type("Expression", "Node")
        self.stack = []
        self.postfix_expr = []
        pass

    def is_valid(self, _expr):
        try:
            parser = Parser(_expr)
            self.infix_expr = parser.parse()
        except AssertionError:
            print("Expression is wrong.")
            self.infix_expr = ""
        pass

    def make_postfix(self):
        for e in self.infix_expr:
            assert isinstance(e, Node), debug_type("Expression", "Node")
            if isinstance(e.value, float):
                # number
                self.postfix_expr.append(e)
            elif e.priority == 1:
                # E L
                self.stack.append(e)
            elif e.priority == 2:
                # * / % ^
                while self.stack and self.stack[-1].priority < 2:
                    self.postfix_expr.append(self.stack.pop())
                self.stack.append(e)
            elif e.priority == 3:
                # + -
                while self.stack and self.stack[-1].priority < 3:
                    self.postfix_expr.append(self.stack.pop())
                self.stack.append(e)
            elif e.priority == 4:
                if e.value in Node.right_paren:
                    # )}]
                    while self.stack and self.stack[-1].priority != e.priority:
                        self.postfix_expr.append(self.stack.pop())
                    self.stack.pop()
                else:
                    # [{(
                    self.stack.append(e)
            else:
                raise AssertionError("Invalid syntax.")
        while self.stack:
            self.postfix_expr.append(self.stack.pop())

        pass

    def calc(self):
        # TODO: remove redundant Node.
        self.make_postfix()
        for e in self.postfix_expr:
            assert isinstance(e, Node), debug_type("Expression", "Node")
            if isinstance(e.value, float):
                self.stack.append(e)
            elif e.priority == 1:
                operand0 = self.stack.pop()
                if e.value == 'E':
                    self.stack.append(Node(pow(10.0, operand0.value)))
                elif e.value == 'L':
                    self.stack.append(Node(math.log2(operand0.value)))
            elif e.priority > 1:
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                if e.value == '*':
                    self.stack.append(Node(operand1.value * operand2.value))
                elif e.value == '/':
                    self.stack.append(Node(operand1.value / operand2.value))
                elif e.value == '%':
                    self.stack.append(Node(operand1.value % operand2.value))
                elif e.value == '^':
                    self.stack.append(Node(operand1.value ** operand2.value))
                elif e.value == '+':
                    self.stack.append(Node(operand1.value + operand2.value))
                elif e.value == '-':
                    self.stack.append(Node(operand1.value - operand2.value))
                else:
                    raise AssertionError("Invalid syntax")
            else:
                raise AssertionError("Invalid syntax")
        return self.stack.pop()

    pass


if __name__ == "__main__":
    expr1 = '1+2'
    expr2 = '2*3+4^2-3*2'
    expr3 = '4%2'
    expr4 = '1.0/2. 3'
    expr5 = 'E(2) + {L2}'
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
    """
    print(p1.parse())
    print(p2.parse())
    print(p3.parse())
    print(p4.parse())
    print(p5.parse())
    """

    c1 = Calculator(expr1)
    print(c1.calc())
    c2 = Calculator(expr2)
    print(c2.calc())
    c3 = Calculator(expr3)
    print(c3.calc())
    c4 = Calculator(expr4)
    print(c4.calc())
    c5 = Calculator(expr5)
    print(c5.calc())

    pass
