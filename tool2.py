file = open('C:/Users/Administrator/Desktop/url.txt', 'r+')
output = open('C:/Users/Administrator/Desktop/www_url.txt', 'w+')

for line in file:
    output.write('www.' + line)
