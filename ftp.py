import os
from ftplib import FTP

local = os.path.normcase(os.path.abspath('.')) #项目相对路径
localpath = local + '/down/'    #本地上传路径
filename = os.listdir(localpath)
host = "23.248.249.138" #服务器host
root = "hentai"   #账号
password = "123456" #密码

print('正在连接FTP服务器')
ftp = FTP()                         #设置变量
ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
ftp.connect(host, 21)          #连接的ftp sever和端口
ftp.login(root, password)      #连接的用户名，密码
print(ftp.getwelcome())            #打印出欢迎信息

bufsize = 1024  # 设置缓冲块大小
file_handler = open(localpath + filename[0], 'rb')  # 以读模式在本地打开文件
ftp.storbinary('STOR %s' % os.path.basename(filename[0]), file_handler, bufsize)  # 上传文件
ftp.set_debuglevel(0)
file_handler.close()
while 1:
    if ftp.size(filename[0]) > -1:
        print('上传成功')
        break
    else:
        print("还未上传成功，请等待!")





