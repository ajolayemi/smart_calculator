#!/usr/bin/env python
DESCRIPTION = 'A smart calculator capable of handling addition and subtraction' \
              'operations. \nUser is prompted to enter the expression they want to ' \
              'evaluate and the evaluation result is printed out.'

if __name__ == '__main__':
    while True:
        expr = input()
        if expr == '/exit':
            print('Bye!')
            break
        elif expr == '/help':
            print(DESCRIPTION)

        elif expr == '':
            continue

        else:
            print(eval(expr))
