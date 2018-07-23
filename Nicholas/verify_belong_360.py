# -*- coding=utf-8 -*-
# @author Nicholas
# @version 弹出网络延迟优化
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import paramiko
import os
import time
import linecache
from selenium.common.exceptions import NoSuchElementException
from paramiko.ssh_exception import SSHException
from selenium.common.exceptions import TimeoutException


def parse(driver, phone, password):
    locator = (By.XPATH, '//form/p[1]/span/input')
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_all_elements_located(locator))
    driver.set_window_size(1000, 1030)  # 分辨率 1280*800
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
    global temp
    # file1 = open("C:/Users/Administrator/Desktop/www_urls_all_5.txt", "r+")
    driver.get('http://zhanzhang.so.com/?m=Site&a=index')
    add_one = driver.find_element_by_xpath("//*[@id='site']/div[2]/input")
    add_one.click()
    while True:
        add_one = driver.find_element_by_xpath("//body/div[4]/div[3]/input")
        read_url = linecache.getline('C:/Users/Administrator/Desktop/www_urls_all_5.txt', temp)
        print("读取到第 " + str(temp) + " 行")
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
            temp += 1
        except TimeoutException:
            print('添加成功！url: ' + read_url)
            temp += 1
            return read_url


def verify_url(driver, sftp):
    driver.find_element_by_xpath("//tbody/tr[2]/td[2]/a").click()
    locator = (By.ID, 'verity_tab_2')
    WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(locator))
    driver.find_element_by_id('verity_tab_2').click()
    locator = (By.XPATH, "//*[@id='verity_con_2']/ol[1]/li[1]/a")
    WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable(locator))
    driver.find_element_by_xpath("//*[@id='verity_con_2']/ol[1]/li[1]/a").click()
    print("下载验证文件")
    while True:
        try:
            print('loading...')
            downland_path = 'D:/Documents/Downloads'
            filename = os.listdir(downland_path)
            if filename[0].count('crdownload') > 0:
                time.sleep(0.5)
            else:
                break
        except IndexError:
            time.sleep(1)
            continue
    print("下载成功...")
    while True:
        try:
            downland_path = 'D:/Documents/Downloads'
            filename = os.listdir(downland_path)
            print('获取本地文件 :' + filename[0])
            print('上传本地文件')
            # 将本地的Windows.txt文件上传至服务器/root/Windows.txt
            sftp.put(downland_path + '/' + filename[0], '/www/wwwroot/xbw/' + filename[0])
            print("上传文件 path: " + '/www/wwwroot/xbw/' + filename[0])
            break
        except Exception:
            print("连接失败！ 再次重试上传")
            print("loading...")
            time.sleep(1)
    state = True
    num = 1
    while state:
        if num > 5:
            raise TimeoutException
        downland_path = 'D:/Documents/Downloads'
        filename = os.listdir(downland_path)
        files = sftp.listdir('/www/wwwroot/xbw/')
        for name in files:
            if name == filename[0]:
                state = False
        print('等待上传...')
        time.sleep(1)
        num += 1
    print('上传成功！')
    print('点击验证')
    driver.find_element_by_xpath('//body/div[4]/div[3]/div[1]/div[6]/a').click()
    print('loading...')
    time.sleep(3)
    locator = (By.XPATH, '//tbody/tr[2]/td[2]/a[2]')
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable(locator))
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


def parse_sitemap(driver, post_url, state):
    if state:
        print('尝试提交sitemap.xml')
        add_sitemap(driver, post_url)
        return post_url
    else:
        print('尝试提交主站 ' + post_url.strip("\n") + ' 子域名')
        path = 'C:/Users/Administrator/Desktop/url/' + post_url.split('\n', 1)[0]
        file = open(path, 'r+')
        for second_url in file:
            print('尝试提交子域名' + second_url + 'sitemap.xml')
            add_sitemap(driver, second_url)
        return post_url


def add_sitemap(driver, post_url):
        real_url = "http://zhanzhang.so.com/?m=Sitemap&a=index&host=" + post_url
        time.sleep(1)
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
            WebDriverWait(driver, 5, 0.5).until(EC.element_to_be_clickable(locator))
            print("提交成功！")
            return post_url
        except TimeoutException:
            raise RuntimeError("提交sitemap失败！请检查网络！")


def read_lines(www_url):
    path = 'C:/Users/Administrator/Desktop/url/' + www_url.strip('\n')
    print("读取文件 path = " + path)
    file = open(path, 'r+')
    lines = file.readlines()
    text1 = ''
    text = []
    for x in range(0, 17):
        text1 += lines[x]
    text.append(text1)
    return text


def add_second_url(driver, www_url):
    global second
    print("尝试主域名添加子站 ：" + www_url + "loading...")
    if second == 0:
        page_url = "http://zhanzhang.so.com/?m=Site&a=index"
        driver.get(page_url)
        driver.find_element_by_xpath("//tbody/tr[2]/td[2]/a[2]").click()
    else:
        page_url = 'http://zhanzhang.so.com/?m=Site&a=index&p=2'
        driver.get(page_url)
        driver.find_element_by_xpath("//tbody/tr[2]/td[9]/a[2]").click()
    locator = (By.ID, 'submit-sites')
    WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable(locator))
    select = driver.find_element_by_xpath("//textarea")
    second_url = www_url.strip('\n')
    text_area = read_lines(second_url)
    select.clear()
    select.send_keys(text_area[0])
    driver.find_element_by_id('submit-sites').click()
    while not EC.alert_is_present()(driver):
        print("loading ...")
        time.sleep(1)
    al = driver.switch_to_alert()
    time.sleep(1)
    al.accept()
    print("添加子站成功！")


web = webdriver.Chrome()
web.get("http://zhanzhang.so.com")
parse(web, '18782991033', 'Ptyw1q2w3e$R')
print('正在连接服务器')
host = '142.234.162.99'
root = 'root'
password = 'free@0516'
temp = 1
second = 0
while True:
    transport = paramiko.Transport(host, 22)
    try:
        transport.connect(username=root, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print('服务器连接成功')
        while True:
            url = add_url(web)
            verify_url(web, sftp)
            url = parse_sitemap(web, url, True)
            add_second_url(web, url)
    except(EOFError, SSHException):
        print('服务器连接失败 尝试连接服务器...')
        print("loading...")
        time.sleep(1)
    finally:
        downland_path = 'D:/Documents/Downloads'
        filename = os.listdir(downland_path)
        my_file = ''
        try:
            my_file = downland_path + '/' + filename[0]
        except IndexError:
            pass
        if os.path.exists(my_file):
            print('删除下载文件')
            os.remove(downland_path + '/' + filename[0])
            print('删除成功')
        transport.close()
        print("程序结束。。。")

