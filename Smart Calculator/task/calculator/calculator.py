#!/usr/bin/env python

if __name__ == '__main__':
    expr = input().split()
    print(eval(f'{expr[0]} + {expr[1]}'))
