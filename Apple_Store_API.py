#!/usr/bin/python3
# coding=utf-8

import urllib.request
import json
import ssl
import Excel_Utility
import threading
from urllib.parse import quote
import string

app_ids = []
app_names = []


# 创建一个线程类
class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.result = ''
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# 获取所有app的name id
def get_app_ranking_content(term, num, lang, country):
    app_ids.clear()
    app_names.clear()
    content = [['App名称', 'App评分', 'App评分用户数',
                'App类型', 'App评论数', 'App版本号',
                'App简介', 'App界面截图', 'App价格']]
    url = 'https://itunes.apple.com/search?' \
          'term=' + term + '&limit=' + str(num) + '&country=' + country + '&entity=software&lang=' + lang
    url = quote(url, safe=string.printable)
    json_text = get_html_text(url)
    if json_text is None or json_text == "":
        print("抓取App排行数据为空")
        return
    try:
        data_results = json_text["results"]
    except:
        return
    for index in range(len(data_results)):
        print("获取App Store App排行数据%.1f" % ((index + 1) * 100 / len(data_results)), '%')
        values = []
        # AppID
        app_ids.append(data_results[index]['trackId'])
        # App名称
        values.append(data_results[index]['trackName'])
        app_names.append(data_results[index]['trackName'])
        # App评分
        values.append(data_results[index]['averageUserRatingForCurrentVersion'])
        # App评分用户数
        values.append(data_results[index]['userRatingCount'])
        # App类型
        genres = ' '
        for i in range(len(data_results[index]['genres'])):
            genres += (data_results[index]['genres'][i].strip() + " ")
        values.append(genres)
        # App支持的语言
        language = ' '
        for i in range(len(data_results[index]['languageCodesISO2A'])):
            language += (data_results[index]['languageCodesISO2A'][i].strip() + " ")
        values.append(language)
        # App版本号
        values.append(data_results[index]['version'])
        # App简介
        values.append(data_results[index]['description'])
        # App界面截图
        pictures = ' '
        for i in range(len(data_results[index]['screenshotUrls'])):
                pictures += (data_results[index]['screenshotUrls'][i].strip() + "\n")
        values.append(pictures)
        content.append(values)
    if content is None or content == "":
        print("抓取App排行内容失败")
    return content


# 将App ranking信息写进Excel表格
def write_ranking_in_excel(path, term, num, lang, country):
    # content = get_app_ranking_content(term, num, lang, country)
    # Excel_Utility.write_excel_content(path, 'AllAppRanking', content)

    content = [['用户名', '标题', '内容', '评分', '版本号', '投票数']]
    threads = []
    for i in range(10):
        my_thread = MyThread(get_app_reviews, args=(i + 1, term, lang, country,))
        threads.append(my_thread)
        my_thread.start()
    for thread in threads:
        thread.join()
    for thread in threads:
        try:
            content += thread.get_result()
        except:
            continue
    Excel_Utility.write_reviews(path, term, content)


# 获取App的评论
def get_app_reviews(index, app_id, lang, country):
    content = []
    url = 'https://itunes.apple.com/rss/customerreviews/page=' + \
          str(index) + '/id=' + str(app_id) + \
          '/sortby=mostrecent/json?l=' + lang + '&&cc=' + country
    json_text = get_html_text(url)
    if json_text is None or json_text == "":
        return
    try:
        data_feed = json_text['feed']
        entry = data_feed['entry']
    except:
        return
    for i in range(len(entry)):
        values = []
        try:
            value = entry[i]
        except:
            break
        # 用户名
        values.append(value['author']['name']['label'])
        # 标题
        values.append(value['title']['label'])
        # 内容
        values.append(value['content']['label'])
        # 评分
        values.append(value['im:rating']['label'])
        # 版本号
        values.append(value['im:version']['label'])
        # 投票数
        values.append(value['im:voteCount']['label'])
        content.append(values)
    return content


# 获取Html的文本内容
def get_html_text(url):
    my_json = ""
    for i in range(3):
        try:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(url, context=context)
            my_json = json.loads(response.read().decode())
            return my_json
        except:
            continue
    return my_json


# 将评论写进excel
def write_reviews_in_excel(path, lang, country):
    lock = threading.Lock()
    for index in range(len(app_ids)):
        print("获取App Store App评论数据%.1f" % ((index + 1) * 100 / len(app_ids)), '%')
        content = [['用户名', '标题', '内容', '评分', '版本号', '投票数']]
        threads = []
        for i in range(10):
            my_thread = MyThread(get_app_reviews, args=(i + 1, app_ids[index], lang, country,))
            print(my_thread)
            threads.append(my_thread)
            my_thread.start()
        for thread in threads:
            thread.join()
        for thread in threads:
            try:
                content += thread.get_result()
            except:
                continue
        Excel_Utility.write_excel_content(path, str(index + 1) + '_' + app_names[index], content)


# 获取App 排行和评论数据 并写入Excel表格
def get_app_ranking_reviews(path, term, num, lang, country):
    write_ranking_in_excel(path, term, num, lang, country)
    write_reviews_in_excel(path, lang, country)


