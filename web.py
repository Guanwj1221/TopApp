from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import ssl
from requests_html import HTML
from bs4 import BeautifulSoup

driver = webdriver.Chrome("/Users/Anker/ChromeDriver84/chromedriver")

# 加载界面
driver.get("https://play.google.com/store/search?q=music&c=apps")
time.sleep(3)

# 获取页面初始高度
js = "return action=document.body.scrollHeight"
height = driver.execute_script(js)

# 将滚动条调整至页面底部
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(5)

# 定义初始时间戳（秒）
t1 = int(time.time())

# 定义循环标识，用于终止while循环
status = True

# 重试次数
num = 0

while status:
    # 获取当前时间戳（秒）
    t2 = int(time.time())
    # 判断时间初始时间戳和当前时间戳相差是否大于3秒，小于3秒则下拉滚动条
    if t2 - t1 < 3:
        new_height = driver.execute_script(js)
        if new_height > height:
            time.sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            # 重置初始页面高度
            height = new_height
            # 重置初始时间戳，重新计时
            t1 = int(time.time())
    elif num < 3:  # 当超过3秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待3秒
        time.sleep(3)
        num = num + 1
    else:  # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
        print("滚动条已经处于页面最下方！")
        status = False
        # 滚动条调整至页面顶部
        driver.execute_script('window.scrollTo(0, 0)')
        break

# 打印页面源码
content = driver.page_source
# print(content)

ssl._create_default_https_context = ssl._create_unverified_context
soup = BeautifulSoup(content, 'html.parser')
html = soup.find_all('a', class_='poRVub')
print(len(html))
for item in html:
    print(item.attrs['href'].split('=')[1])


