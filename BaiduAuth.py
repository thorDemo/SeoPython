from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import platform
import paramiko
from paramiko.ssh_exception import SSHException
from selenium.common.exceptions import TimeoutException


local = os.path.normcase(os.path.abspath('.')) #项目相对路径
host = "23.110.211.170" #服务器host
root = "root"   #账号
password = "Hxt414722027" #密码
remotepath = '/www/wwwroot/xbw/' #远程提交路径
localpath = local + '/down/'    #本地上传路径
yuming = local + '/yuming/pre_9_88.txt' #域名库文件
sysstr = platform.system()
if sysstr =="Windows":
    path = local + "/driver/chromedriver.exe"  # 谷歌控制器路径
    profile = 'C:/Users/username/AppData/Local/Google/Chrome/User Data/test_profile'

else:
    path = local + "/driver/chromedriver"  # 谷歌控制器路径
    profile = '/Users/YV/Library/Application Support/Google/Chrome/Default'

print('正在连接SSH服务器')
while True:
    transport = paramiko.Transport(host, 223)
    try:
        transport.connect(username=root, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print('服务器连接成功')
        break
    except SSHException as e:
        print('服务器连接失败 尝试连接服务器...')


options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': localpath, 'profile.managed_default_content_settings.images': 2}
options.add_argument("--user-data-dir="+profile)
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(path, chrome_options=options)  # 打开 Chrome 浏览器
driver.implicitly_wait(10)   # seconds
driver.get("https://ziyuan.baidu.com/login/index?u=/site/index")
print('登陆成功')
driver.get("https://ziyuan.baidu.com/site/index")
cookie = driver.get_cookies()
print(cookie)
time.sleep(1)
print('点击确认添加站点')
site_add = driver.find_element_by_id('site-add-btn')
site_add.click()
time.sleep(1)
file = open(yuming)
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for url in lines:
        pass
        print('更改协议头')
        http = driver.find_element_by_xpath("//div[@id='protocolSelect']/input")
        driver.execute_script("arguments[0].value = 'http://'", http)
        print('添加url:' + url)
        sendurl = driver.find_element_by_class_name('add-site-input')
        sendurl.send_keys(url)
        urladd = driver.find_element_by_id('site-add')
        urladd.click()
        time.sleep(1)
        try:
            if driver.find_element_by_class_name('add-site-errtip').text == "您已添加过这个网站":
                print('该网站url已经提交过了')
                driver.get("https://ziyuan.baidu.com/site/siteadd")
                continue
            a = True
        except:
            a = False
        while 1:
            start = time.clock()
            # check0 = driver.find_element_by_id('check0')
            # ActionChains(driver).click(check0)
            try:
                print('选择领域')
                driver.find_element_by_xpath('//ul/li[18]/label').click()
                print(driver.find_element_by_xpath('//ul/li[18]/label').is_selected())
                driver.find_element_by_xpath('//ul/li[10]/label').click()
                print(driver.find_element_by_xpath('//ul/li[10]/label').is_selected())
                driver.find_element_by_xpath('//ul/li[25]/label').click()
                print(driver.find_element_by_xpath('//ul/li[25]/label').is_selected())
                print('设置成功')
                break
            except Exception as e:
                print(e)
                print("正在验证中，请等待!")
        print('后退浏览器')
        driver.back()
        print('再次点击添加网站')
        time.sleep(2)
        driver.find_element_by_id('site-add').click()
        print('确认域名领域')
        if driver.find_element_by_xpath('//ul/li[18]/label').is_selected() is False:
            driver.find_element_by_xpath('//ul/li[18]/label').click()
        if driver.find_element_by_xpath('//ul/li[10]/label').is_selected() is False:
            driver.find_element_by_xpath('//ul/li[10]/label').click()
        if driver.find_element_by_xpath('//ul/li[25]/label').is_selected() is False:
            driver.find_element_by_xpath('//ul/li[25]/label').click()
        time.sleep(2)
        driver.find_element_by_id('sub-attr').click()
        print('开始下载验证文件')
        while 1:
            try:
                driver.find_element_by_xpath("//dd[@id='file']/p[2]/a[1]").click()
                print('已定位到元素')
                end = time.clock()
                break
            except:
                print("还未定位到元素!")
        print('定位耗费时间：' + str(end - start))
        time.sleep(2)
        filename = os.listdir(localpath)
        print('已找到下载文件' + filename[0])
        print('上传本地文件')

        while True:
            try:
                print('上传本地文件')
                sftp.put(localpath + '/' + filename[0],
                         '/www/wwwroot/xbw/' + filename[0])  # 将本地的Windows.txt文件上传至服务器/root/Windows.txt
                time.sleep(2)
                print("上传文件成功 path: " + '/www/wwwroot/xbw/' + filename[0])
                break
            except Exception:
                print("连接失败！ 再次重试上传")
                print("loading...")
                time.sleep(3)
                break
        state = True
        num = 1
        while state:
            if num > 5:
                raise TimeoutException
            filename = os.listdir(localpath)
            files = sftp.listdir('/www/wwwroot/xbw/')
            for name in files:
                print(name.strip('\n') + '  对比文件  ' + filename[0])
                if str(name) == str(filename[0]):
                    state = False
                    break
            print('等待上传...')
            time.sleep(1)
            num += 1
        print('上传成功！')
        print('点击验证')
        time.sleep(5)
        my_file = localpath + filename[0]
        if os.path.exists(my_file):
            print('删除本地下载文件')
            os.remove(localpath + filename[0])
        else:
            print('文件没有删除')
            print('开始验证服务器文件')
        driver.find_element_by_id('verifySubmit').click()
        while 1:
            start = time.clock()
            try:
                driver.find_element_by_id("dialog").click()
                print('验证成功')
                end = time.clock()
                break
            except:
                print("正在验证中，请等待!")
        driver.get("https://ziyuan.baidu.com/site/siteadd")
sftp.close()
print('SSH关闭')
