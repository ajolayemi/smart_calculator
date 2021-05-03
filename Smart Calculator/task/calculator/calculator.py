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
        self.is_var = '=' in self.expression
        self.var_value_dict = {}

    @staticmethod
    def check_variable_val_name(val_name: str):
        """ Checks to see that the value of a variable is valid. """
        return re.search(variable_value_ptn, val_name) is not None

    @staticmethod
    def check_variable_name(var_name: str):
        """ Checks to see that variable name is valid. """
        return re.search(variable_pattern, var_name) is not None

    def expr_evaluator(self):
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
            print(expr_class.expr_evaluator())


if __name__ == '__main__':
    main()
