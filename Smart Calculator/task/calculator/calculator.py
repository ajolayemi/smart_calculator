#!/usr/bin/env python
import re

DESCRIPTION = 'A smart calculator capable of handling addition and subtraction' \
              'operations. \nUser is prompted to enter the expression they want to ' \
              'evaluate and the evaluation result is printed out.'

complex_pattern = re.compile(r'^[-]?\d[-+\d ]+')


class Calculator:

    def __init__(self, expression: str):
        self.expression = expression
        self.is_complex = all((self.expression.count('+', 1) >= 1,
                               self.expression.count('-', 1) >= 1))
        self.is_add = all((self.expression.count('+') >= 1,
                           self.expression.count('-', 1) == 0))
        self.is_subtract = all((self.expression.count('-') >= 1,
                                self.expression.count('+', 1) == 0))
        self.single_expr = all((not self.is_add, not self.is_subtract,
                                not self.is_complex))

    def add_nums(self):
        """ Add two or more numbers. """
        split_expr = list(filter(lambda x: x != '', self.expression.split('+')))
        return sum([int(num.strip()) for num in split_expr])


if __name__ == '__main__':
    n = input()
    a = Calculator(n)
    print('Add', a.add_nums())
    print('Sub', a.is_subtract)
    print('Complex', a.is_complex)
    print('Single', a.single_expr)