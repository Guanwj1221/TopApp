# coding=utf-8

import json
import time
import os
# pip install PyExecJS
import execjs
from enum import Enum
import Keyword_Utility
import Excel_Utility
import Thread_Utility


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


# 获取App的评论数据的json数据
# app_id: App ID，必填
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
# sort: 排序方式，默认为 Sort.NEWEST
# num: 评论数量，默认100
def get_app_reviews_json(app_id, lang, country, sort, num):
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function reviews(app_id, lang, country, sort, num) {
        gplay.reviews({
        appId: app_id,
        lang: lang,
        country: country,
        sort: sort,
        num: num
        })
        .then((body) => {
            fs.writeFile('GooglePlay/JsonData/' + app_id + 'Reviews.json', JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    ctx.call("reviews", app_id, lang, country, sort, num)
    json_data = get_json_result(file_name='GooglePlay/JsonData/' + app_id + 'Reviews.json')

    return json_data


# 获取App排行和App详情的json数据
# collection: Google Play 榜单，默认为 Collection.TOP_FREE
# category: App 种类，默认无
# num: App数量，默认 500
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
def get_app_list_json(category, collection, num, lang, country, fullDetail):
    if fullDetail:
        print("开始获取Google Play App Name And ID数据")
    else:
        print("开始获取Google Play App排行数据")
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function list(category, collection, num, lang, country, fullDetail) {
        gplay.list({
        category: category,
        collection: collection,
        num: num,
        lang: lang,
        country: country,
        fullDetail: fullDetail
        }).then((body) => {
            fs.writeFile('GooglePlay/JsonData/List.json', JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    ctx.call("list", category, collection, num, lang, country, fullDetail)
    json_data = get_json_result(file_name='TopApp/GooglePlay/JsonData/List.json')
    if fullDetail:
        print("获取Google Play App Name And ID数据结果：", (json_data != ""))
    else:
        print("获取Google Play App排行数据结果：", (json_data != ""))
    return json_data


# 获取与关键词相关的App的json数据
# term: 关键词，必须
# num: App数量，默认 20 最大 250
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
def get_top_app_json_data(term, num, lang, country):
    print("开始获取Google Play App排行数据")
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function search(term, num, lang, country) {
        gplay.search({
        term: term,
        num: num,
        lang: lang,
        country: country
        }).then((body) => {
            fs.writeFile('GooglePlay/JsonData/Search.json', JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            })
        })
    }
    """)
    ctx.call("search", term, num, lang, country)

    json_data = get_json_result(file_name='TopApp/GooglePlay/JsonData/Search.json')
    print("获取Google Play App排行数据结果：", (json_data != ""))
    return json_data


# 获取App的详情
def get_app_details(json_data):
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


# 获取App的名称和ID
def get_app_name_id(json_data):
    try:
        app_name = json_data['title']
        app_id = json_data['appId']
    except:
        return None
    return app_name, app_id


# 获取所有App的名称和ID
def get_all_app_name_id(category, collection, num, lang, country):
    json_data = get_app_list_json(category, collection, num, lang, country, False)
    app_names = []
    app_ids = []
    for index in range(len(json_data)):
        app_name, app_id = get_app_name_id(json_data[index])
        app_names.append(app_name)
        app_ids.append(app_id)
    return app_names, app_ids


# 获取所有App的详情
def get_all_app_details(category, collection, num, lang, country):
    json_data = get_app_list_json(category, collection, num, lang, country, True)
    contents = [['名称', 'ID', '最大安装量', '评分',
                 '评分人数', '星级分布', '评论人数', '价格',
                 '类型', '版本号', '摘要', '描述',
                 '截图', '关键词']]

    for index in range(len(json_data)):
        details = get_app_details(json_data[index])
        find_string = details[10] + details[11]
        key_words = Keyword_Utility.find_keyword(find_string)
        details.append(key_words)
        contents.append(details)
    return contents


# 获取App的评论
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
# collection: Google Play 榜单，默认为 Collection.TOP_FREE
# category: App 种类，默认无
# app_num: App数量，默认 500
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
# review_num: 评论数量
def get_app_ranking_reviews(path, category, collection,
                            app_num, lang, country,
                            sort, review_num):
    app_names, app_ids = get_all_app_name_id(category, collection, app_num, lang, country)
    if len(app_names) == 0 or len(app_ids) == 0:
        print("获取App数据失败")
        return
    content_thread = Thread_Utility.MyThread(
        get_all_app_details, args=(category, collection, app_num, lang, country,))
    content_thread.start()

    print("开始获取Google Play App评论数据")
    app_reviews = Thread_Utility.get_google_play_reviews(
        get_app_reviews, app_ids, lang, country, sort, review_num)

    app_rank_name = []
    for index in range(len(app_names)):
        app_rank_name.append(str(index + 1) + '_' + app_names[index])

    content_thread.join()
    contents = content_thread.get_result()

    print("开始加载Google Play App数据...")
    Excel_Utility.write_content(path, 'AllAppRanking', contents, app_rank_name, app_reviews)


# 评论排序枚举
class Sort(Enum):
    NEWEST = 2
    RATING = 3
    HELPFULNESS = 1


# 应用榜单枚举
class Collection(Enum):
    TOP_FREE = 'topselling_free'
    TOP_PAID = 'topselling_paid'
    GROSSING = 'topgrossing'
    TRENDING = 'movers_shakers'
    TOP_FREE_GAMES = 'topselling_free_games'
    TOP_PAID_GAMES = 'topselling_paid_games'
    TOP_GROSSING_GAMES = 'topselling_grossing_games'
    NEW_FREE = 'topselling_new_free'
    NEW_PAID = 'topselling_new_paid'
    NEW_FREE_GAMES = 'topselling_new_free_games'
    NEW_PAID_GAMES = 'topselling_new_paid_games'


# 应用类型的枚举
class Category(Enum):
    APPLICATION = 'APPLICATION'
    ANDROID_WEAR = 'ANDROID_WEAR'
    ART_AND_DESIGN = 'ART_AND_DESIGN'
    AUTO_AND_VEHICLES = 'AUTO_AND_VEHICLES'
    BEAUTY = 'BEAUTY'
    BOOKS_AND_REFERENCE = 'BOOKS_AND_REFERENCE'
    BUSINESS = 'BUSINESS'
    COMICS = 'COMICS'
    COMMUNICATION = 'COMMUNICATION'
    DATING = 'DATING'
    EDUCATION = 'EDUCATION'
    ENTERTAINMENT = 'ENTERTAINMENT'
    EVENTS = 'EVENTS'
    FINANCE = 'FINANCE'
    FOOD_AND_DRINK = 'FOOD_AND_DRINK'
    HEALTH_AND_FITNESS = 'HEALTH_AND_FITNESS'
    HOUSE_AND_HOME = 'HOUSE_AND_HOME'
    LIBRARIES_AND_DEMO = 'LIBRARIES_AND_DEMO'
    LIFESTYLE = 'LIFESTYLE'
    MAPS_AND_NAVIGATION = 'MAPS_AND_NAVIGATION'
    MEDICAL = 'MEDICAL'
    MUSIC_AND_AUDIO = 'MUSIC_AND_AUDIO'
    NEWS_AND_MAGAZINES = 'NEWS_AND_MAGAZINES'
    PARENTING = 'PARENTING'
    PERSONALIZATION = 'PERSONALIZATION'
    PHOTOGRAPHY = 'PHOTOGRAPHY'
    PRODUCTIVITY = 'PRODUCTIVITY'
    SHOPPING = 'SHOPPING'
    SOCIAL = 'SOCIAL'
    SPORTS = 'SPORTS'
    TOOLS = 'TOOLS'
    TRAVEL_AND_LOCAL = 'TRAVEL_AND_LOCAL'
    VIDEO_PLAYERS = 'VIDEO_PLAYERS'
    WEATHER = 'WEATHER'
    GAME = 'GAME'
    GAME_ACTION = 'GAME_ACTION'
    GAME_ADVENTURE = 'GAME_ADVENTURE'
    GAME_ARCADE = 'GAME_ARCADE'
    GAME_BOARD = 'GAME_BOARD'
    GAME_CARD = 'GAME_CARD'
    GAME_CASINO = 'GAME_CASINO'
    GAME_CASUAL = 'GAME_CASUAL'
    GAME_EDUCATIONAL = 'GAME_EDUCATIONAL'
    GAME_MUSIC = 'GAME_MUSIC'
    GAME_PUZZLE = 'GAME_PUZZLE'
    GAME_RACING = 'GAME_RACING'
    GAME_ROLE_PLAYING = 'GAME_ROLE_PLAYING'
    GAME_SIMULATION = 'GAME_SIMULATION'
    GAME_SPORTS = 'GAME_SPORTS'
    GAME_STRATEGY = 'GAME_STRATEGY'
    GAME_TRIVIA = 'GAME_TRIVIA'
    GAME_WORD = 'GAME_WORD'
    FAMILY = 'FAMILY'
    FAMILY_ACTION = 'FAMILY_ACTION'
    FAMILY_BRAINGAMES = 'FAMILY_BRAINGAMES'
    FAMILY_CREATE = 'FAMILY_CREATE'
    FAMILY_EDUCATION = 'FAMILY_EDUCATION'
    FAMILY_MUSICVIDEO = 'FAMILY_MUSICVIDEO'
    FAMILY_PRETEND = 'FAMILY_PRETEND'
