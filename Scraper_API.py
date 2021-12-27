# coding=utf-8
import execjs
from enum import Enum
import time
import os
import json

from other import Excel_Utility
import Keyword_Utility
import Thread_Utility

json_dir_path = 'JsonData'
google_play_dir_path = 'GooglePlay'
apple_store_dir_path = 'AppleStore'


# 判断获取json数据的结果
def get_json_result(file_name):
    num = 0
    json_data = ""
    while num < 5:
        time.sleep(1)
        if os.path.exists(file_name):
            file_data = open(file_name)
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
def get_app_reviews_json(platform, app_id, lang, country, sort, num):
    ctx = execjs.compile("""
    var count = 1
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function reviews(platform, app_id, lang, country, sort, num, file_name) {
        var page = num / 50
        if (page < 1)
            page = 1
        if (platform === 'apple_store')
        {
            for (var i = 1; i <= page; i++) {
                gplay = require('app-store-scraper')
                gplay.reviews({
                appId: app_id,
                country: country,
                sort: sort,
                page: i
                })
                .then((body) => {
                    let test_name = file_name.slice(0, file_name.length - 5) + "_test.json"
                    if ("[]" !== JSON.stringify(body)) {
                        fs.writeFile(test_name, JSON.stringify(body), {flag: 'a'}, (err) => {
                            if (err) {
                                console.error(err)
                            }
                        })
                    }
                    count += 1
                    if (count === page) {
                        fs.readFile(test_name, "utf8", function (err, data) {
                            let new_data = data.replaceAll('][', ', ')
                            if (err) {
                                console.log(err);
                            } else {
                                fs.writeFile(file_name, new_data, (err) => {
                                    if (err) {
                                        console.error(err)
                                    }
                                })
                            }
                        })
                    }
                })
            }
        }
        else
        {
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
                    }
                })
            })
        }
    }
    """)
    file_name = json_dir_path + '/' + platform + app_id + country + '_Reviews.json'
    try:
        ctx.call("reviews", platform, app_id, lang, country, sort, num, file_name)
    except:
        return ''
    json_data = get_json_result(file_name=file_name)
    return json_data


# List API: 获取App排行和App详情的json数据
# collection: Google Play 榜单
# category: App 种类，默认无
# num: App数量
# lang: 语言
# country: 国家
def get_app_list_json(platform, category, collection, num, lang, country, full_detail):
    print(platform, "Get app list data...")
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function list(platform, category, collection, num, lang, country, full_detail, file_name) {
        if (platform === 'apple_store')
            gplay = require('app-store-scraper')
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
                }
            })
        })
    }
    """)
    file_name = json_dir_path + '/' + platform + country + '_List.json'
    try:
        ctx.call("list", platform, category, collection, num, lang, country, full_detail, file_name)
    except:
        return ''
    json_data = get_json_result(file_name=file_name)
    print(platform, "Get app list data result: ", (json_data != ""))
    return json_data


# Search API: 获取与关键词相关的App的json数据
# term: 关键词，必须
# num: App数量
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
def get_search_app_json_data(platform, term, num, lang, country):
    print(platform, "Get search app data...")
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function search(platform, term, num, lang, country, file_name) {
        if (platform === 'apple_store')
            gplay = require('app-store-scraper')
        gplay.search({
        term: term,
        num: num,
        lang: lang,
        country: country
        }).then((body) => {
            fs.writeFile(file_name, JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                }
            })
        })
    }
    """)
    file_name = json_dir_path + '/' + platform + country + '_Search.json'
    try:
        ctx.call("search", platform, term, num, lang, country, file_name)
    except:
        return ''
    json_data = get_json_result(file_name=file_name)
    print(platform, "Get search app data result: ", (json_data != ""))
    return json_data


# App API: 获取与App的json数据
# term: 关键词，必须
# lang: 语言
# country: 国家
def get_app_json_data(platform, app_id, lang, country):
    ctx = execjs.compile("""
    var gplay = require('google-play-scraper')
    var fs = require("fs")
    function app(platform, app_id, lang, country, file_name) {
        if (platform === 'apple_store')
            gplay = require('app-store-scraper')
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
    file_name = json_dir_path + '/' + platform + app_id + country + '_App.json'
    try:
        ctx.call("app", platform, app_id, lang, country, file_name)
    except:
        return ''
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
def get_app_details_by_json(platform, json_data):
    try:
        app_name = json_data['title']
        app_id = json_data['appId']
        app_score = json_data['score']
        app_reviews = json_data['reviews']
        app_price = json_data['price']
        app_version = json_data['version']
        if platform == Platform.Google_Play.value:
            app_summary = json_data['summary']
        else:
            try:
                app_summary = json_data['releaseNotes']
            except:
                app_summary = ''
        app_description = json_data['description']
        app_screenshots = json_data['screenshots']
        find_string = app_summary + app_description
        key_words = Keyword_Utility.find_keyword(find_string)
        if platform == Platform.Google_Play.value:
            app_max_installs = json_data['maxInstalls']
            app_ratings = json_data['ratings']
            app_genre = json_data['genre']
            app_histogram = json_data['histogram']
            details = [app_name, app_id, app_max_installs, app_score,
                       app_ratings, app_histogram, app_reviews, app_price,
                       app_genre, app_version, app_summary, app_description,
                       app_screenshots, key_words]
        else:
            app_size = json_data['size']
            app_current_version_score = json_data['currentVersionScore']
            app_genres = json_data['genres']
            details = [app_name, app_id, app_size, app_score,
                       app_current_version_score, app_genres, app_reviews, app_price,
                       app_version, app_summary, app_description,
                       app_screenshots, key_words]
    except:
        return []
    return details


# 获取App的详情
# app_id
# lang: 语言
# country: 国家
def get_app_details_by_id(platform, app_id, lang, country):
    json_data = get_app_json_data(platform, app_id, lang, country)
    details = get_app_details_by_json(platform, json_data)
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
def get_all_app_details(platform, category, collection, num, lang, country):
    json_data = get_app_list_json(platform, category, collection, num, lang, country, True)
    if platform == Platform.Google_Play.value:
        contents = [['App Name', 'App ID', 'Max Installs', 'Score',
                     'Ratings', 'Histogram', 'Reviews', 'Price',
                     'Genre', 'Version', 'Summary', 'Description',
                     'Screenshots', 'Keywords']]
    else:
        contents = [['App Name', 'App ID', 'Size', 'Score',
                     'Current Version Score', 'Genres', 'Reviews', 'Price',
                     'Version', 'Summary', 'Description',
                     'Screenshots', 'Keywords']]

    for index in range(len(json_data)):
        details = get_app_details_by_json(platform, json_data[index])
        contents.append(details)
    return contents


# 获取App的评论
# lang: 语言
# country: 国家
# sort: 排序方式
# num: 评论数量
def get_app_reviews(platform, app_id, lang, country_array, sort, num):
    data_array = []
    for country in country_array:
        tem_lang = lang
        if platform == Platform.Google_Play.value:
            for name, member in CountyLangCode.__members__.items():
                if name == str(country).upper():
                    tem_lang = member.value
                    break
        json_data = get_app_reviews_json(platform, app_id, tem_lang, country, sort, num)
        if json_data == '':
            continue
        try:
            array = json_data['data']
        except:
            array = json_data
        data_array += array

    if platform == Platform.Google_Play.value:
        app_reviews = [['User ID', 'User Name', 'Store', 'Title', 'Comment',
                        'Date', 'Reply Date', 'Reply Text', 'Thumbs Up', 'Version']]
    else:
        app_reviews = [['User ID', 'User Name', 'Store', 'Title', 'Comment', 'Version']]
    for i in range(len(data_array)):
        try:
            user_id = data_array[i]['id']
            user_name = data_array[i]['userName']
            score = data_array[i]['score']
            title = data_array[i]['title']
            text = data_array[i]['text']
            # text_translate = translate(text)
            # if text_translate is not None:
            #     text += '\nTranslate：' + text_translate
            version = data_array[i]['version']
            if platform == Platform.Google_Play.value:
                date = data_array[i]['date']
                reply_text = data_array[i]['replyText']
                reply_date = data_array[i]['replyDate']
                thumbs_up = data_array[i]['thumbsUp']
                review = [user_id, user_name, score, title, text,
                          date, reply_text, reply_date, thumbs_up, version]
            else:
                review = [user_id, user_name, score, title, text, version]
            app_reviews.append(review)
        except:
            continue
    return app_id, app_reviews


# 获取App的排行和评论
# path: Excel表格名称
# collection: Google Play 榜单
# category: App 种类
# app_num: App数量
# lang: 语言
# country: 国家
# review_num: 评论数量
def save_app_list_ranking_reviews(platform, path, category, collection,
                                  app_num, lang, country,
                                  sort, reviews_num):

    json_data = get_app_list_json(platform, category, collection, app_num, lang, country, False)
    app_names, app_ids = get_all_app_name_id(json_data)
    if len(app_names) == 0 or len(app_ids) == 0:
        print(platform, "Get data fail")
        return
    content_thread = Thread_Utility.MyThread(
        get_all_app_details, args=(platform, category, collection, app_num, lang, country,))
    content_thread.start()

    print(platform, "Getting data...")
    complete_app, app_reviews = Thread_Utility.get_all_app_reviews(
        get_app_reviews, platform, app_ids, lang, [country], sort, reviews_num)
    sheet_names = []
    for i in range(len(complete_app)):
        index = app_ids.index(complete_app[i])
        sheet_names.append(app_names[index])

    content_thread.join()
    contents = content_thread.get_result()

    app_rank_name = []
    for index in range(len(app_names)):
        app_rank_name.append(sheet_names[index])

    print(platform, "Loading data...")
    Excel_Utility.write_content(path, 'Rank', contents, app_rank_name, app_reviews)


# 讲搜索的App信息写入表格
# path：Excel表格路径
# term：关键词
# app_num: App数量，默认100
# reviews_num: 评论数量，默认500
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
# sort: 排序方式，默认为 Sort.NEWEST
def save_search_app_ranking_reviews(platform, path, term, sort, app_num, reviews_num, lang, country, country_array):
    if platform == Platform.Google_Play.value:
        rank = [['App Name', 'App ID', 'Max Installs', 'Score',
                 'Ratings', 'Histogram', 'Reviews', 'Price',
                 'Genre', 'Version', 'Summary', 'Description',
                 'Screenshots', 'Keywords']]
    else:
        rank = [['App Name', 'App ID', 'Size', 'Score',
                 'Current Version Score', 'Genres', 'Reviews', 'Price',
                 'Version', 'Summary', 'Description',
                 'Screenshots', 'Keywords']]
    json_data = get_search_app_json_data(platform, term, app_num, lang, country)
    app_names, app_ids = get_all_app_name_id(json_data)

    thread1 = Thread_Utility.MyThread(Thread_Utility.get_all_app_reviews,
                                      (get_app_reviews, platform, app_ids, lang, country_array, sort, reviews_num))
    thread2 = Thread_Utility.MyThread(Thread_Utility.get_all_app_details,
                                      (get_app_details_by_id, platform, app_ids, lang, country))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    complete_app, all_reviews = thread1.result
    sheet_names = []
    for i in range(len(complete_app)):
        index = app_ids.index(complete_app[i])
        sheet_names.append(app_names[index])

    details = thread2.result
    rank += details
    Excel_Utility.write_content(path, "Rank", rank, sheet_names, all_reviews)


class Platform(Enum):
    Google_Play = 'google_play'
    Apple_Store = 'apple_store'


# 评论排序枚举
class GooglePlaySort(Enum):
    NEWEST = 2
    RATING = 3
    HELPFULNESS = 1


class AppleStoreSort(Enum):
    RECENT = 'mostRecent'
    HELPFUL = 'mostHelpful'


# 应用榜单枚举
class GooglePlayCollection(Enum):
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


class AppleStoreCollection(Enum):
    # TOP_MAC = 'topmacapps'
    # TOP_FREE_MAC = 'topfreemacapps'
    # TOP_GROSSING_MAC = 'topgrossingmacapps'
    # TOP_PAID_MAC = 'toppaidmacapps'
    TOP_FREE_IOS = 'topfreeapplications'
    TOP_FREE_IPAD = 'topfreeipadapplications'
    TOP_GROSSING_IOS = 'topgrossingapplications'
    TOP_GROSSING_IPAD = 'topgrossingipadapplications'
    TOP_PAID_IOS = 'toppaidapplications'
    TOP_PAID_IPAD = 'toppaidipadapplications'
    NEW_IOS = 'newapplications'
    NEW_FREE_IOS = 'newfreeapplications'
    NEW_PAID_IOS = 'newpaidapplications'


# 应用类型的枚举
class GooglePlayCategory(Enum):
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


class AppleStoreCategory(Enum):
    BOOKS = 6018
    BUSINESS = 6000
    CATALOGS = 6022
    EDUCATION = 6017
    ENTERTAINMENT = 6016
    FINANCE = 6015
    FOOD_AND_DRINK = 6023
    GAMES = 6014
    GAMES_ACTION = 7001
    GAMES_ADVENTURE = 7002
    GAMES_ARCADE = 7003
    GAMES_BOARD = 7004
    GAMES_CARD = 7005
    GAMES_CASINO = 7006
    GAMES_DICE = 7007
    GAMES_EDUCATIONAL = 7008
    GAMES_FAMILY = 7009
    GAMES_MUSIC = 7011
    GAMES_PUZZLE = 7012
    GAMES_RACING = 7013
    GAMES_ROLE_PLAYING = 7014
    GAMES_SIMULATION = 7015
    GAMES_SPORTS = 7016
    GAMES_STRATEGY = 7017
    GAMES_TRIVIA = 7018
    GAMES_WORD = 7019
    HEALTH_AND_FITNESS = 6013
    LIFESTYLE = 6012
    MAGAZINES_AND_NEWSPAPERS = 6021
    MAGAZINES_ARTS = 13007
    MAGAZINES_AUTOMOTIVE = 13006
    MAGAZINES_WEDDINGS = 13008
    MAGAZINES_BUSINESS = 13009
    MAGAZINES_CHILDREN = 13010
    MAGAZINES_COMPUTER = 13011
    MAGAZINES_FOOD = 13012
    MAGAZINES_CRAFTS = 13013
    MAGAZINES_ELECTRONICS = 13014
    MAGAZINES_ENTERTAINMENT = 13015
    MAGAZINES_FASHION = 13002
    MAGAZINES_HEALTH = 13017
    MAGAZINES_HISTORY = 13018
    MAGAZINES_HOME = 13003
    MAGAZINES_LITERARY = 13019
    MAGAZINES_MEN = 13020
    MAGAZINES_MOVIES_AND_MUSIC = 13021
    MAGAZINES_POLITICS = 13001
    MAGAZINES_OUTDOORS = 13004
    MAGAZINES_FAMILY = 13023
    MAGAZINES_PETS = 13024
    MAGAZINES_PROFESSIONAL = 13025
    MAGAZINES_REGIONAL = 13026
    MAGAZINES_SCIENCE = 13027
    MAGAZINES_SPORTS = 13005
    MAGAZINES_TEENS = 13028
    MAGAZINES_TRAVEL = 13029
    MAGAZINES_WOMEN = 13030
    MEDICAL = 6020
    MUSIC = 6011
    NAVIGATION = 6010
    NEWS = 6009
    PHOTO_AND_VIDEO = 6008
    PRODUCTIVITY = 6007
    REFERENCE = 6006
    SHOPPING = 6024
    SOCIAL_NETWORKING = 6005
    SPORTS = 6004
    TRAVEL = 6003
    UTILITIES = 6002
    WEATHER = 6001


class CountyLangCode(Enum):
    CN = 'zh'
    KR = 'kr'
    CA = 'ca'
    FR = 'fr'
    DE = 'de'
    JP = 'jp'
    IT = 'it'
    AR = 'ar'
    PT = 'pt'
    US = 'en'
    RU = 'ru'
    ES = 'es'
    PL = 'pl'
