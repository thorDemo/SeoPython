 # -*- coding=utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import paramiko
import os
import time
from selenium.common.exceptions import NoSuchElementException
from paramiko.ssh_exception import SSHException
from selenium.common.exceptions import TimeoutException
import platform

local = os.path.normcase(os.path.abspath('.')) #项目相对路径
localpath = local + '/down/'    #本地上传路径

file1 = open(local + "/yuming/yuming.txt", "r+")

def parse(driver, phone, password):
    locator = (By.XPATH, '//form/p[1]/span/input')
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_all_elements_located(locator))
    driver.set_window_size(1000, 1000)  # 分辨率 1280*800
    select = driver.find_element_by_xpath("//form/p[3]/a")
    driver.execute_script("arguments[0].scrollIntoView();", select)  # 拖动到可见的元素去
    select = driver.find_element_by_xpath("//form/p[1]/span/input")
    select.send_keys(phone)
    select = driver.find_element_by_xpath("//form/p[2]/span/input")
    select.send_keys(password)
    select = driver.find_element_by_xpath("//form/p[5]/input")  # 点击登陆
    select.click()
    print("尝试登陆360站长平台！")
    while True:
        try:
            # 1、尝试获取添加标签
            driver.find_element_by_xpath("//*[@id='site']/div[2]/input")  # 尝试获取添加URL按钮
            print("恭喜你登录成功！！")
            return driver
        except NoSuchElementException:
            print('loading...')
            # 5、等待1s
            time.sleep(1)
            # 2、获取添加标签失败
            # 3、是否有验证码等待输入 或者验证码失败
            try:
                if driver.find_element_by_xpath("//*[@id='loginWrap']/div[1]/div[1]/p").text == '请输入验证码':
                    # 4、无验证码等待输入
                    print("请输入验证码")
                    verify = input("code: ")
                    select = driver.find_element_by_xpath('//form/p[3]/span/input')
                    select.clear()
                    select.send_keys(verify)
                    # 8、点击登陆
                    select = driver.find_element_by_xpath("//form/p[5]/input")
                    select.click()
                    print('loading 3s ...')
                    time.sleep(3)
                elif driver.find_element_by_xpath("//*[@id='loginWrap']/div[1]/div[1]/p").text == '验证码错误请重新输入':
                    print("验证码错误请重新输入")
                    verify = input("code: ")
                    select = driver.find_element_by_xpath('//form/p[3]/span/input')
                    select.clear()
                    select.send_keys(verify)
                    # 8、点击登陆
                    select = driver.find_element_by_xpath("//form/p[5]/input")
                    select.click()
                    print('loading 5s ...')
                    time.sleep(5)
                else:
                    pass
                    # 6、有验证码等待输入
                    # 7、输入验证码

            # 3、无验证码等待输入
            except NoSuchElementException:
                print('loading...')
                time.sleep(1)


def add_url(driver):
    driver.get('http://zhanzhang.so.com/?m=Site&a=index')
    add_one = driver.find_element_by_xpath("//*[@id='site']/div[2]/input")
    add_one.click()
    while True:
        add_one = driver.find_element_by_xpath("//body/div[4]/div[3]/input")
        read_url = file1.readline()
        if read_url == '':
            raise RuntimeError('全部url读取完毕!')
        print("尝试提交 url: " + read_url)
        add_one.clear()
        add_one.send_keys(read_url)
        driver.find_element_by_id('add_btn').click()
        try:
            print('loading...')
            locator = (By.XPATH, '//body/div[4]/div[1]')
            driver.find_element_by_xpath("//body/div[4]/div[1]")
            time.sleep(2)
            WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable(locator))
            print('这个网站已经提交过了 url: ' + read_url)
        except TimeoutException:
            print('添加成功！url: ' + read_url)
            return read_url


def verify_url(driver, sftp):
    driver.find_element_by_xpath("//tbody/tr[2]/td[2]/a").click()
    locator = (By.ID, 'verity_tab_2')
    WebDriverWait(driver, 5, 0.5).until(EC.element_to_be_clickable(locator))
    driver.find_element_by_id('verity_tab_2').click()
    locator = (By.XPATH, "//*[@id='verity_con_2']/ol[1]/li[1]/a")
    WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable(locator))
    driver.find_element_by_xpath("//*[@id='verity_con_2']/ol[1]/li[1]/a").click()
    print("下载验证文件")
    print("loading...")
    time.sleep(1)
    downland_path = 'D:/Documents/Downloads'
    filename = os.listdir(downland_path)
    print('获取本地文件 :' + filename[0])
    while True:
        try:
            print('上传本地文件')
            sftp.put(downland_path + '/' + filename[0], '/www/wwwroot/xbw/' + filename[0])  # 将本地的Windows.txt文件上传至服务器/root/Windows.txt
            time.sleep(2)
            print("上传文件成功 path: " + '/www/wwwroot/xbw/' + filename[0])
            break
        except Exception:
            print("连接失败！ 再次重试上传")
            print("loading...")
            time.sleep(3)
            break
    print('点击验证')
    driver.find_element_by_xpath('//body/div[4]/div[3]/div[1]/div[6]/a').click()
    print('loading...')
    time.sleep(2)
    locator = (By.XPATH, '//tbody/tr[2]/td[2]/a')
    try:
        WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable(locator))
    except TimeoutException:
        raise RuntimeError("验证文件失败 请检查！！")
    finally:
        print('删除远程文件')
        sftp.remove('/www/wwwroot/xbw/' + filename[0])
        my_file = downland_path + '/' + filename[0]
        if os.path.exists(my_file):
            print('删除下载文件')
            os.remove(downland_path + '/' + filename[0])
            print('删除成功')


def add_sitemap(driver, post_url):
    print('尝试提交sitemap.xml')
    real_url = "http://zhanzhang.so.com/?m=Sitemap&a=index&host=" + post_url
    driver.get(real_url)
    driver.find_element_by_xpath("//body/div[1]/div[2]/div[1]/div[2]/input[2]").click()
    locator = (By.XPATH, "//body/div[3]/div[3]/a")
    try:
        WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable(locator))
        select = driver.find_element_by_xpath("//body/div[3]/div[3]/textarea")
        select.clear()
        select.send_keys(post_url.split('\n')[0] + '/sitemap.xml')
        driver.find_element_by_xpath("//body/div[3]/div[3]/a").click()
    except TimeoutException:
        raise RuntimeError("点击添加失败！请检查网络！")
    try:
        locator = (By.XPATH, "//tbody/tr[2]/td[5]/a")
        WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable(locator))
        print("提交成功！")
    except TimeoutException:
        raise RuntimeError("提交sitemap失败！请检查网络！")


def add_second_url(driver):
    driver.get("http://zhanzhang.so.com/?m=Site&a=index")
    driver.find_element_by_xpath("//tbody/tr[2]/td[2]/a[2]").click()
    driver.find_element_by_xpath("//body/div[4]/div[3]/div[1]/div[2]/div[1]/textarea")
    pass

sysstr = platform.system()
if sysstr =="Windows":
    path = local + "/driver/chromedriver.exe"  # 谷歌控制器路径
    profile = 'C:/Users/username/AppData/Local/Google/Chrome/User Data/test_profile'

else:
    path = local + "/driver/chromedriver"  # 谷歌控制器路径
    profile = '/Users/YV/Library/Application Support/Google/Chrome/Default'

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': localpath, 'profile.managed_default_content_settings.images': 2}
options.add_argument("--user-data-dir="+profile)
options.add_experimental_option('prefs', prefs)
web = webdriver.Chrome(path, chrome_options=options)
web.get("http://zhanzhang.so.com")
parse(web, '18782991033', 'Ptyw1q2w3e$R')
print('正在连接服务器')
host = '142.234.162.99'
root = 'root'
password = 'free@0516'
temp = 1
while True:
    transport = paramiko.Transport(host, 22)
    try:
        transport.connect(username=root, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print('服务器连接成功')
        while True:
            url = add_url(web)
            verify_url(web, sftp)
            add_sitemap(web, url)
            add_second_url(web)
            print('this is :' + str(temp))
            temp += 1
    except SSHException as e:
        print('服务器连接失败 尝试连接服务器...')
    finally:
        transport.close()
        print("over do")
        #break
