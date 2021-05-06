#!/usr/bin/env python
import re

DESCRIPTION = 'A smart calculator capable of handling the following arithmetic operations:\n' \
              '1. Addition and subtraction of two or more numbers\n' \
              '2. Variable declaration and usage in expressions later on\n' \
              'User is prompted to enter the expression they want to ' \
              'evaluate and the evaluation result is printed out.'

SIGNS = ['-', '+']
invalid_expressions = re.compile(r'^[+-]+$|[+-]$|^[\w\d ]+ [\w\d]+$')
variable_pattern = re.compile(r'^[a-zA-Z]+$')
variable_value_ptn = re.compile(r'^[a-zA-Z]+$|^[\d]+$')
variable_request = re.compile(r'^[a-zA-Z]+$')
variable_expression_ptn = re.compile(r'^[\w +-]+[ +-]+[\w]$')
commands = ['/help', '/exit']


class Calculator:
    var_value_dict = {}

    def __init__(self, expression: str):
        self.expression = expression
        self.is_var_declaration = '=' in self.expression
        self.is_var_request = re.search(variable_request, self.expression)
        self.is_var_expression = re.search(variable_expression_ptn, self.expression)

    def module_caller(self):
        """ Decides which module to call for calculation. """
        if self.is_var_declaration:
            self.var_declaration_handler()

        elif self.is_var_request:
            self.var_request_handler()

        else:
            self.variable_expression_eval()

    def var_request_handler(self):
        """ Responds to when user is requesting to view the value of a
        variable. """
        if self.expression not in Calculator.var_value_dict:
            print('Unknown variable')
        else:
            print(Calculator.var_value_dict.get(self.expression))

    def var_declaration_handler(self):
        """ Responds to when user is trying to declare new variables. """
        variable_name = self.expression[:self.expression.find('=')].strip()
        variable_value = self.expression[self.expression.find('=') + 1:].strip()
        if not self.check_variable_name(variable_name):
            print('Invalid identifier')
        elif not self.check_variable_val_name(variable_value) or \
                self.expression.count('=') > 1:
            print('Invalid assignment')
        elif variable_value.isalpha() and variable_value not in Calculator.var_value_dict:
            print('Unknown variable')
        else:
            if variable_value.isalpha():
                Calculator.var_value_dict[variable_name] = Calculator.var_value_dict.get(variable_value)
            else:
                Calculator.var_value_dict[variable_name] = variable_value

    @staticmethod
    def check_variable_val_name(val_name: str) -> True:
        """ Checks to see that the value of a variable is valid.
        :returns True if val_name is valid
        :returns False otherwise. """
        return re.search(variable_value_ptn, val_name) is not None

    @staticmethod
    def check_variable_name(var_name: str):
        """ Checks to see that variable name is valid.
        :returns True if var_name is valid.
        :returns False otherwise"""
        return re.search(variable_pattern, var_name) is not None

    def variable_expression_eval(self):
        """ Handles expressions that contains variable."""
        value = self.expr_parser()
        try:
            output = 0
            signs = []
            while True:
                current_value = next(value)
                if current_value.isalpha():
                    if not self.check_variable_name(current_value) or \
                            current_value not in Calculator.var_value_dict:
                        print(f'Variable -- {current_value} is unknown.')
                        break
                    else:
                        final_sign = self.sign_calculator(signs)
                        signs.clear()
                        variable_value = int(Calculator.var_value_dict.get(current_value))
                        output = self.calculation_helper(current_value=output,
                                                         sign=final_sign,
                                                         value_to_add_or_sub=variable_value)
                elif current_value in SIGNS:
                    signs.append(current_value)
                else:
                    final_sign = self.sign_calculator(signs)
                    signs.clear()
                    output = self.calculation_helper(current_value=output,
                                                     sign=final_sign,
                                                     value_to_add_or_sub=current_value)
        except StopIteration:
            print(output)

    @staticmethod
    def calculation_helper(current_value, sign, value_to_add_or_sub):
        """ Helps the two module that handles calculation. """
        if sign == '+':
            return current_value + int(value_to_add_or_sub)
        elif sign == '-':
            return current_value - int(value_to_add_or_sub)

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
            expr_class.module_caller()


if __name__ == '__main__':
    main()
