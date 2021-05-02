#!/usr/bin/env python
import re

DESCRIPTION = 'A smart calculator capable of handling addition and subtraction' \
              'operations. \nUser is prompted to enter the expression they want to ' \
              'evaluate and the evaluation result is printed out.'

SIGNS = ['-', '+']
invalid_expressions = re.compile(r'^[a-zA-Z +-]+$|[+-]$|^[\w\d ]+ [\w\d]+$')
variable_pattern = re.compile(r'^[a-zA-Z]+$')
variable_value_ptn = re.compile(r'^[a-zA-Z]+$|^[\d]+$')
commands = ['/help', '/exit']


class Calculator:
    def __init__(self, expression: str):
        self.expression = expression
        self.is_complex_expr = False
        self.is_add = all((self.expression.count('+') >= 1,
                           self.expression.count('-', 1) == 0))
        self.is_subtract = all((self.expression.count('-', 1) == 1,
                                self.expression.count('+', 1) == 0,
                                not self.expression.startswith('-')))
        self.is_var = '=' in self.expression

        self.is_complex()

        self.single_expr = all((not self.is_add, not self.is_subtract,
                                not self.is_complex, not self.is_var))
        self.var_value_dict = {}

    def module_caller(self):
        """ Decides which module to call"""
        if self.is_add:
            return self.add_nums()
        elif self.is_subtract:
            return self.subtract_nums()
        elif self.is_complex_expr:
            return self.complex_nums()
        else:
            return self.expression

    def check_variable_name(self):
        """ Checks to see that variable name is valid. """
        return re.search(variable_pattern,
                         self.expression[:self.expression.index('=')]) is not None

    def complex_nums(self):
        """ Deals with complex expressions. """

        value = self.expr_parser()
        try:
            result = 0
            signs = []
            while True:
                current_value = next(value)
                if current_value in SIGNS:
                    signs.append(current_value)

                else:
                    final_sign = self.sign_calculator(signs)
                    signs.clear()
                    if final_sign == '+':
                        result += int(current_value)
                    elif final_sign == '-':
                        result -= int(current_value)

        except StopIteration:
            return result

    @staticmethod
    def sign_calculator(signs: list):
        result = None
        if not signs:
            return '+'
        for sign in signs:
            if not result:
                result = sign
            elif sign == '-' and result == '-' or sign == '+' and result == '+':
                result = '+'
            else:
                result = '-'
        return result

    def expr_parser(self):
        index = 0
        while index < len(self.expression):
            if self.expression[index] != ' ':
                if index == len(self.expression) - 1:
                    yield self.expression[index].strip()
                    index += 1

                elif self.expression[index + 1].isnumeric():
                    yield self.expression[index:index+2].strip()
                    index += 2
                else:
                    yield self.expression[index].strip()
                    index += 1
            else:
                index += 1

    def subtract_nums(self):
        """ Subtracts two or more numbers """
        split_expr = list(filter(lambda x: x != '', self.expression.split('-')))
        result = int(split_expr[0])
        for _, num, in enumerate(split_expr[1:]):
            result -= int(num.strip())
        return result

    def add_nums(self):
        """ Add two or more numbers. """
        split_expr = list(filter(lambda x: x != '', self.expression.split('+')))
        return sum([int(num.strip()) for num in split_expr])

    def is_complex(self):
        """ Checks to see whether the provided expression
        is a complex one.
        An expression is considered to be complex when there are more than
        a single minus (-) sign in it or both minus (-) and addition (+)
        sign are present. """
        if self.expression.count('-', 1) >= 1 and '+' in self.expression:
            self.is_complex_expr = True
        elif self.expression.count('-') > 1:
            self.is_complex_expr = True


def main():

    while True:
        user_expr = input()
        if user_expr.startswith('/') and user_expr not in commands:
            print('Unknown command')
        elif re.search(invalid_expressions, user_expr):
            print('Invalid expression')
        elif not user_expr:
            continue
        elif user_expr == '/exit':
            print('Bye!')
            break
        elif user_expr == '/help':
            print(DESCRIPTION)
        else:
            expr_class = Calculator(user_expr)
            print(expr_class.module_caller())


if __name__ == '__main__':
    ex = 'a =2'
    print(Calculator(ex).check_variable_name())