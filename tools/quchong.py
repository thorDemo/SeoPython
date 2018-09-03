from peewee import *

DB = MySQLDatabase('station', user='root', password='123456', host='localhost', port=3306)


class NewsArt(Model):
    title = CharField(255, unique=True)
    content = TextField()

    class Meta:
        database = DB
        table_bane = 'NewsArt'


# if NewsArt.table_exists() is False:
#     NewsArt.create_table()
# file = open('C:/Users/Administrator/Desktop/2.txt', 'r+', encoding='utf-8')
# for line in file:
#     text = line.split('##########')
#     data = {
#         'title': text[0],
#         'content': text[1].replace('http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:http:', '')
#     }
#     try:
#         print(text[0])
#         NewsArt.insert(data).execute()
#     except IntegrityError:
#         print('重复数据 跳过！')
query = NewsArt.select()
result = open('C:/Users/Administrator/Desktop/Ada.txt', 'w+', encoding='utf-8')
webname = open('C:/Users/Administrator/Desktop/webname.txt', 'w+', encoding='utf-8')
temp = 1
for line in query:
    # result.write(line.title + '##########' + line.content)
    webname.write(line.title + '\n')
    print('%s  -  %s' % (temp, line.title))
    temp += 1
