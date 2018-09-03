# coding:utf-8
import os

movie_name = os.listdir('C:/Users/Administrator/Downloads/news')
for temp in movie_name:
    new_name = temp + '.jpg'
    os.rename('C:/Users/Administrator/Downloads/news/' + temp, 'C:/Users/Administrator/Downloads/news/' + new_name)
