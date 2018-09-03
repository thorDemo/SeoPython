# -*- coding=utf-8 -*-

file = open('yuming/yuming.txt', 'r+')

for line in file:
    print('http://www.' + line)
