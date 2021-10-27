#!/usr/bin/python3
# coding=utf-8
import urllib.request
import ssl
import json
import Excel_Utility
import Thread_Utility
from urllib.parse import quote
import string
from mtranslate import translate

apple_store_dir_path = 'AppStore'
app_ids = []
app_names = []


# 获取所有app的name id
def get_app_ranking_content(term, num, lang, country):
    app_ids.clear()
    app_names.clear()
    content = [['App名称', 'App评分', 'App评分用户数',
                'App类型', 'App支持语言', 'App版本号',
                'App简介', 'App界面截图', 'App价格']]
    url = 'https://itunes.apple.com/search?' \
          'term=' + term + '&limit=' + str(num) + \
          '&country=' + country + '&entity=software&lang=' + lang
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
    else:
        print("抓取App排行内容成功")
    return content


# 获取App的评论
def get_app_one_page_reviews(index, app_id, lang, country):
    content = []
    url = 'https://itunes.apple.com/rss/customerreviews/page=' + \
          str(index) + '/id=' + str(app_id) + \
          '/sortby=mostrecent/json?l=' + lang + '&&cc=' + country
    json_text = get_html_text(url)
    if json_text is None or json_text == "":
        print(app_id, "获取reviews json data失败")
        return content
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
        text = value['content']['label']
        # text_translate = translate(text)
        # if text_translate is not None:
        #     text += '\nTranslate：' + text_translate
        values.append(text)
        # 评分
        values.append(value['im:rating']['label'])
        # 版本号
        values.append(value['im:version']['label'])
        # 投票数
        values.append(value['im:voteCount']['label'])
        # 更新时间
        values.append(value['updated']['label'])
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


def get_app_reviews(app_id, lang, country, num):
    content = [['用户名', '标题', '内容', '评分', '版本号', '投票数', '更新时间']]
    pages = min(int(num) / 50, 10)
    for i in range(int(pages)):
        reviews = get_app_one_page_reviews(i + 1, app_id, lang, country)
        if reviews is not None:
            content += reviews
    return content


# 将评论写进excel
def get_reviews(lang, country, num):
    reviews = Thread_Utility.get_apple_store_reviews(get_app_reviews, app_ids, lang, country, num)
    return reviews


def save_ranking_reviews(term, sort, app_num, reviews_num, path, lang, country):
    rank = get_app_ranking_content(term, app_num, lang, country)
    reviews = get_reviews(lang, country, reviews_num)
    Excel_Utility.write_content(path, term, rank, app_names, reviews)


