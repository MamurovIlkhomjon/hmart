from os import lstat
from django.test import TestCase


lst = [
        {'product_name': 1},
        {'product_name': 3},
        {'product_name': 5},
        {'product_name': 11},
        ]

# print(lst)

# lst2 = []
# for i in lst:
#     lst2.append(i['product_name'])
# print(lst2)

func = lambda dict: dict['product_name']

print(list(map(func, lst)))

# print(list(map()))

# func = lambda item: item['name']

# print(func({'name': 'abror'}))