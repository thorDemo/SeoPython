# -*-coding=utf-8-*-

urls = open('yuming/9_2.txt', 'r+')
post = open('yuming/http_9.txt', 'w+')
for url in urls:
    print(url)
    post.write('http://www.' + url)