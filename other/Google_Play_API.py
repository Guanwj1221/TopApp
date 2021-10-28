# coding=utf-8

import json
import time
import os
# pip install PyExecJS
import execjs
import Keyword_Utility
from other import Excel_Utility
import Thread_Utility

google_play_json_dir_path = 'GooglePlay/JsonData'
google_play_dir_path = 'GooglePlay'


# 判断获取json数据的结果
def get_json_result(file_name):
    num = 0
    file = file_name
    json_data = ""
    while num < 5:
        time.sleep(1)
        if os.path.exists(file):
            file_data = open(file)
            try:
                json_data = json.load(file_data)
            except:
                break
            break
        else:
            num += 1
        print("loading...")
    return json_data


# Reviews API: 获取App的评论数据的json数据
# app_id: App ID，必填
# lang: 语言
# country: 国家
# sort: 排序方式
# num: 评论数量
def get_app_reviews_json(app_id, lang, country, sort, num):
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function reviews(app_id, lang, country, sort, num, file_name) {
        gplay.reviews({
        appId: app_id,
        lang: lang,
        country: country,
        sort: sort,
        num: num
        })
        .then((body) => {
            fs.writeFile(file_name, JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    file_name = google_play_json_dir_path + '/' + app_id + 'Reviews.json'
    ctx.call("reviews", app_id, lang, country, sort, num, file_name)
    json_data = get_json_result(file_name=file_name)

    return json_data


# List API: 获取App排行和App详情的json数据
# collection: Google Play 榜单
# category: App 种类，默认无
# num: App数量
# lang: 语言
# country: 国家
def get_app_list_json(category, collection, num, lang, country, full_detail):
    if full_detail:
        print("开始获取Google Play App Name And ID数据")
    else:
        print("开始获取Google Play App排行数据")
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function list(category, collection, num, lang, country, full_detail, file_name) {
        gplay.list({
        category: category,
        collection: collection,
        num: num,
        lang: lang,
        country: country,
        fullDetail: full_detail
        }).then((body) => {
            fs.writeFile(file_name, JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    file_name = google_play_json_dir_path + '/List.json'
    ctx.call("list", category, collection, num, lang, country, full_detail, file_name)
    json_data = get_json_result(file_name=file_name)
    if full_detail:
        print("获取Google Play App Name And ID数据结果：", (json_data != ""))
    else:
        print("获取Google Play App排行数据结果：", (json_data != ""))
    return json_data


# Search API: 获取与关键词相关的App的json数据
# term: 关键词，必须
# num: App数量
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
def get_search_app_json_data(term, num, lang, country):
    print("开始获取Google Play App排行数据")
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function search(term, num, lang, country, file_name) {
        gplay.search({
        term: term,
        num: num,
        lang: lang,
        country: country
        }).then((body) => {
            fs.writeFile(file_name, JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    file_name = google_play_json_dir_path + '/Search.json'
    ctx.call("search", term, num, lang, country, file_name)

    json_data = get_json_result(file_name=file_name)
    print("获取Google Play App排行数据结果：", (json_data != ""))
    return json_data


# App API: 获取与App的json数据
# term: 关键词，必须
# lang: 语言
# country: 国家
def get_app_json_data(app_id, lang, country):
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function app(app_id, lang, country, file_name) {
        gplay.app({
        appId: app_id,
        lang: lang,
        country: country
        }).then((body) => {
            fs.writeFile(file_name, JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    file_name = google_play_json_dir_path + '/' + app_id + 'App.json'
    ctx.call("app", app_id, lang, country, file_name)

    json_data = get_json_result(file_name=file_name)
    return json_data


# 获取所有App的名称和ID
def get_all_app_name_id(json_data):
    app_names = []
    app_ids = []
    for index in range(len(json_data)):
        app_name, app_id = get_app_name_id(json_data[index])
        app_names.append(app_name)
        app_ids.append(app_id)
    return app_names, app_ids


# 获取App的详情
def get_app_details_by_json(json_data):
    try:
        app_name = json_data['title']
        app_id = json_data['appId']
        app_max_installs = json_data['maxInstalls']
        app_score = json_data['score']
        app_ratings = json_data['ratings']
        app_histogram = json_data['histogram']
        app_reviews = json_data['reviews']
        app_price = json_data['price']
        app_genre = json_data['genre']
        app_version = json_data['version']
        app_summary = json_data['summary']
        app_description = json_data['description']
        app_screenshots = json_data['screenshots']
        # 名称 ID 最大安装量 评分 评分人数 星级分布 评论人数 价格 类型 版本号 摘要 描述 截图
        details = [app_name, app_id, app_max_installs, app_score,
                   app_ratings, app_histogram, app_reviews, app_price,
                   app_genre, app_version, app_summary, app_description,
                   app_screenshots]
    except:
        return []
    return details


# 获取App的详情
# app_id
# lang: 语言
# country: 国家
def get_app_details_by_id(app_id, lang, country):
    json_data = get_app_json_data(app_id, lang, country)
    details = get_app_details_by_json(json_data)
    return details


# 获取App的名称和ID
def get_app_name_id(json_data):
    try:
        app_name = json_data['title']
        app_id = json_data['appId']
    except:
        return None
    return app_name, app_id


# 获取榜单所有App的详情
def get_all_app_details(category, collection, num, lang, country):
    json_data = get_app_list_json(category, collection, num, lang, country, True)
    contents = [['名称', 'ID', '最大安装量', '评分',
                 '评分人数', '星级分布', '评论人数', '价格',
                 '类型', '版本号', '摘要', '描述',
                 '截图', '关键词']]

    for index in range(len(json_data)):
        details = get_app_details_by_json(json_data[index])
        find_string = details[10] + details[11]
        key_words = Keyword_Utility.find_keyword(find_string)
        details.append(key_words)
        contents.append(details)
    return contents


# 获取App的评论
# lang: 语言
# country: 国家
# sort: 排序方式
# num: 评论数量
def get_app_reviews(app_id, lang, country, sort, num):
    json_data = get_app_reviews_json(app_id, lang, country, sort, num)
    try:
        data_array = json_data['data']
    except:
        return
    app_reviews = [['用户名', '分数', '标题', '内容',
                    '日期', '回复', '回复时间', '版本号',
                    '点赞数']]
    for i in range(len(data_array)):
        try:
            user_name = data_array[i]['userName']
            score = data_array[i]['score']
            title = data_array[i]['title']
            text = data_array[i]['text']
            # text_translate = translate(text)
            # if text_translate is not None:
            #     text += '\nTranslate：' + text_translate
            date = data_array[i]['date']
            reply_text = data_array[i]['replyText']
            reply_date = data_array[i]['replyDate']
            version = data_array[i]['version']
            thumbs_up = data_array[i]['thumbsUp']
            review = [user_name, score, title, text,
                      date, reply_text, reply_date, version,
                      thumbs_up]
            app_reviews.append(review)
        except:
            continue
    return app_reviews


# 获取App的排行和评论
# path: Excel表格名称
# collection: Google Play 榜单
# category: App 种类
# app_num: App数量
# lang: 语言
# country: 国家
# review_num: 评论数量
def save_app_list_ranking_reviews(path, category, collection,
                                  app_num, lang, country,
                                  sort, reviews_num):
    json_data = get_app_list_json(category, collection, app_num, lang, country, False)
    app_names, app_ids = get_all_app_name_id(json_data)
    if len(app_names) == 0 or len(app_ids) == 0:
        print("获取App数据失败")
        return
    content_thread = Thread_Utility.MyThread(
        get_all_app_details, args=(category, collection, app_num, lang, country,))
    content_thread.start()

    print("开始获取Google Play App评论数据")
    app_reviews = Thread_Utility.get_google_play_reviews(
        get_app_reviews, app_ids, lang, country, sort, reviews_num)

    content_thread.join()
    contents = content_thread.get_result()

    app_rank_name = []
    for index in range(len(app_names)):
        app_rank_name.append(str(index + 1) + '_' + app_names[index])

    print("开始加载Google Play App数据...")
    Excel_Utility.write_content(path, 'AllAppRanking', contents, app_rank_name, app_reviews)


# 讲搜索的App信息写入表格
# path：Excel表格路径
# term：关键词
# app_num: App数量，默认100
# reviews_num: 评论数量，默认500
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
# sort: 排序方式，默认为 Sort.NEWEST
def save_search_app_ranking_reviews(path, term, app_num, reviews_num, lang, country, sort):
    rank = [['名称', 'ID', '最大安装量', '评分',
             '评分人数', '星级分布', '评论人数', '价格',
             '类型', '版本号', '摘要', '描述',
             '截图', '关键词']]
    json_data = get_search_app_json_data(term, app_num, lang, country)
    app_names, app_ids = get_all_app_name_id(json_data)

    thread1 = Thread_Utility.MyThread(Thread_Utility.get_google_play_reviews,
                                      (get_app_reviews, app_ids, lang, country, sort, reviews_num))
    thread2 = Thread_Utility.MyThread(Thread_Utility.get_google_play_details,
                                      (get_app_details_by_id, app_ids, lang, country))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    all_reviews = thread1.result

    details = thread2.result
    rank += details
    Excel_Utility.write_content(path, "rank", rank, app_names, all_reviews)
