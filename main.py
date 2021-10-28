import os
import time
import threading
import tkinter
from tkinter import ttk

import Thread_Utility

# GUI
import Scraper_API


class Application(tkinter.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.google_play_category_name = []
        self.google_play_category_member = []
        self.google_play_collection_name = []
        self.google_play_collection_member = []
        self.google_play_sort_name = []
        self.google_play_sort_member = []

        self.apple_store_category_name = []
        self.apple_store_category_member = []
        self.apple_store_collection_name = []
        self.apple_store_collection_member = []
        self.apple_store_sort_name = []
        self.apple_store_sort_member = []
        self.master = master
        master.title("TopApp")

        # 创建主窗口
        system_width = master.winfo_screenwidth()
        system_height = master.winfo_screenheight()
        window_width = 480
        window_height = 440
        x = (system_width - window_width) / 2
        y = (system_height - window_height) / 2
        master.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        self.pack()

        self.google_play_category_label = ttk.Label(master, text='Google Play Category')
        self.google_play_category_label.place(x=10, y=10)

        self.google_play_category_value = tkinter.StringVar()
        self.google_play_category_box_list = ttk.Combobox(master=master,
                                                          textvariable=self.google_play_category_value)
        self.google_play_category_box_list.place(x=10, y=30)

        self.apple_store_category_label = ttk.Label(master, text='Apple Store Category')
        self.apple_store_category_label.place(x=220, y=10)

        self.apple_store_category_value = tkinter.StringVar()
        self.apple_store_category_box_list = ttk.Combobox(master=master,
                                                          textvariable=self.apple_store_category_value)
        self.apple_store_category_box_list.place(x=220, y=30)

        self.google_play_collection_label = ttk.Label(master, text='Google Play Collection')
        self.google_play_collection_label.place(x=10, y=60)

        self.google_play_collection_value = tkinter.StringVar()
        self.google_play_collection_box_list = ttk.Combobox(master=master,
                                                            textvariable=self.google_play_collection_value)
        self.google_play_collection_box_list.place(x=10, y=80)

        self.apple_store_collection_label = ttk.Label(master, text='Apple Store Collection')
        self.apple_store_collection_label.place(x=220, y=60)

        self.apple_store_collection_value = tkinter.StringVar()
        self.apple_store_collection_box_list = ttk.Combobox(master=master,
                                                            textvariable=self.apple_store_collection_value)
        self.apple_store_collection_box_list.place(x=220, y=80)

        self.google_play_sort_label = ttk.Label(master, text='Google Play Sort')
        self.google_play_sort_label.place(x=10, y=110)

        self.google_play_sort_value = tkinter.StringVar()
        self.google_play_sort_box_list = ttk.Combobox(master=master, textvariable=self.google_play_sort_value)
        self.google_play_sort_box_list.place(x=10, y=130)

        self.apple_store_sort_label = ttk.Label(master, text='Apple Store Sort')
        self.apple_store_sort_label.place(x=220, y=110)

        self.apple_store_sort_value = tkinter.StringVar()
        self.apple_store_sort_box_list = ttk.Combobox(master=master, textvariable=self.apple_store_sort_value)
        self.apple_store_sort_box_list.place(x=220, y=130)

        self.term_label = ttk.Label(master, text='Or Use Keywords')
        self.term_label.place(x=140, y=160)
        self.term_value = tkinter.StringVar()
        self.term_value.set('Soundcore')
        self.term_input = ttk.Entry(master, textvariable=self.term_value)
        self.term_input.place(x=140, y=180)

        self.num_label = ttk.Label(master, text='Number of apps（Max 200）')
        self.num_label.place(x=10, y=210)
        self.num_value = tkinter.StringVar()
        self.num_value.set(3)
        self.num_input = ttk.Entry(master, textvariable=self.num_value)
        self.num_input.place(x=10, y=230)

        self.country_label = ttk.Label(master, text='Country code（Like "us" or "us cn fr..."）')
        self.country_label.place(x=220, y=260)
        self.country_value = tkinter.StringVar()
        self.country_value.set('us cn kr')
        self.country_input = ttk.Entry(master, textvariable=self.country_value)
        self.country_input.place(x=220, y=280)

        self.count_label = ttk.Label(master, text='Number of comments'
                                                  '（Google Play max 5000, Apple Store max 500）')
        self.count_label.place(x=10, y=310)
        self.count_value = tkinter.StringVar()
        self.count_value.set(50)
        self.count_input = ttk.Entry(master, textvariable=self.count_value)
        self.count_input.place(x=10, y=330)

        self.alertButton = ttk.Button(master, text='Submit', command=self.start)
        self.alertButton.place(x=180, y=380)
        self.init_window()

    def init_window(self):
        for name, member in Scraper_API.GooglePlayCategory.__members__.items():
            self.google_play_category_name.append(name.title().replace('_', ' '))
            self.google_play_category_member.append(member.value)

        for name, member in Scraper_API.AppleStoreCategory.__members__.items():
            self.apple_store_category_name.append(name.title().replace('_', ' '))
            self.apple_store_category_member.append(member.value)

        for name, member in Scraper_API.GooglePlayCollection.__members__.items():
            self.google_play_collection_name.append(name.title().replace('_', ' '))
            self.google_play_collection_member.append(member.value)

        for name, member in Scraper_API.AppleStoreCollection.__members__.items():
            self.apple_store_collection_name.append(name.title().replace('_', ' '))
            self.apple_store_collection_member.append(member.value)

        for name, member in Scraper_API.GooglePlaySort.__members__.items():
            self.google_play_sort_name.append(name.title().replace('_', ' '))
            self.google_play_sort_member.append(member.value)

        for name, member in Scraper_API.AppleStoreSort.__members__.items():
            self.apple_store_sort_name.append(name.title().replace('_', ' '))
            self.apple_store_sort_member.append(member.value)

        self.google_play_category_box_list['value'] = self.google_play_category_name
        self.google_play_category_box_list.current(0)

        self.apple_store_category_box_list['value'] = self.apple_store_category_name
        self.apple_store_category_box_list.current(0)

        self.google_play_collection_box_list['value'] = self.google_play_collection_name
        self.google_play_collection_box_list.current(0)

        self.apple_store_collection_box_list['value'] = self.apple_store_collection_name
        self.apple_store_collection_box_list.current(0)

        self.google_play_sort_box_list['value'] = self.google_play_sort_name
        self.google_play_sort_box_list.current(0)

        self.apple_store_sort_box_list['value'] = self.apple_store_sort_name
        self.apple_store_sort_box_list.current(0)

    def start(self):
        google_play_category = self.google_play_category_box_list.current() or 0
        google_play_collection = self.google_play_collection_box_list.current() or 0
        google_play_sort = self.google_play_sort_box_list.current() or 0

        apple_store_category = self.apple_store_category_box_list.current() or 0
        apple_store_collection = self.apple_store_collection_box_list.current() or 0
        apple_store_sort = self.apple_store_sort_box_list.current() or 0

        term = self.term_input.get()
        app_num = self.num_input.get() or 100

        country = self.country_input.get() or 'us'
        lang = 'en'
        reviews_num = self.count_input.get() or 500

        make_dir()
        country_array = country.split(' ')
        if term is None or term == "":
            rank(self.google_play_category_member[google_play_category],
                 self.google_play_collection_member[google_play_collection],
                 self.google_play_sort_member[google_play_sort],
                 self.apple_store_category_name[apple_store_category],
                 self.apple_store_category_member[apple_store_category],
                 self.apple_store_collection_name[apple_store_collection],
                 self.apple_store_collection_member[apple_store_collection],
                 self.apple_store_sort_member[apple_store_sort],
                 app_num, lang, country_array, reviews_num)
        else:
            search(term, self.google_play_sort_member[google_play_sort],
                   self.apple_store_sort_member[apple_store_sort],
                   app_num, reviews_num, lang, country_array)


def delete_google_json_data():
    os.system('rm -rf ' + Scraper_API.json_dir_path)


def make_dir():
    # 创建JsonData文件夹
    if not os.path.exists(Scraper_API.json_dir_path):
        os.mkdir(Scraper_API.json_dir_path)

    # 创建Google Play文件夹
    if not os.path.exists(Scraper_API.google_play_dir_path):
        os.mkdir(Scraper_API.google_play_dir_path)

    # 创建AppStore文件夹
    if not os.path.exists(Scraper_API.apple_store_dir_path):
        os.mkdir(Scraper_API.apple_store_dir_path)


# path: Excel表格名称
# collection: Google Play 榜单，默认为 Collection.TOP_FREE
# category: App 种类，默认为无
# app_num: App数量，默认 500
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
# sort: 排序方式，默认为 Sort.NEWEST
# review_num: 评论数量
def rank(google_play_category='', google_play_collection='', google_play_sort='',
         apple_store_category_name='', apple_store_category='',
         apple_store_collection_name='', apple_store_collection='', apple_store_sort='',
         app_num=100, lang='en', country_array=['us'], review_num=500):
    for country in country_array:
        thread_1 = threading.Thread(
            target=get_google_play_data,
            args=(
                google_play_category,  google_play_collection,
                app_num, lang, country, google_play_sort, review_num))
        thread_2 = threading.Thread(
            target=get_app_store_data,
            args=(apple_store_category_name, apple_store_category,
                  apple_store_collection_name, apple_store_collection,
                  app_num, lang, country, apple_store_sort, review_num))
        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()
    delete_google_json_data()
    print('finish')


# 获取Google Play的数据
def get_google_play_data(category, collection, app_num, lang, country, sort, review_num):
    start_time = time.time()
    google_play_excel_name = country + '_' + category + '_' + collection + '_google_play.xlsx'
    google_play_path = os.path.join(Scraper_API.google_play_dir_path, google_play_excel_name)
    Scraper_API.save_app_list_ranking_reviews(
        Scraper_API.Platform.Google_Play.value, google_play_path,
        category, collection, app_num, lang, country, sort, review_num)
    print('Google play search end, Time-consuming %d' % (time.time() - start_time), "s")


# 获取App Store的数据
def get_app_store_data(category_name, category, collection_name, collection,
                       app_num, lang, country, sort, review_num):
    # 获取App Store的数据开始的时间
    start_time = time.time()

    # 获取Excel表格名称
    apple_store_excel_name = country + '_' + category_name + '_' + collection_name + '_app_store.xlsx'
    apple_store_path = os.path.join(Scraper_API.apple_store_dir_path, apple_store_excel_name)

    Scraper_API.save_app_list_ranking_reviews(
        Scraper_API.Platform.Apple_Store.value, apple_store_path,
        category, collection, app_num, lang, country, sort, review_num)
    print('Apple store search end, Time-consuming %d' % (time.time() - start_time), "s")


def search(term, google_play_sort, apple_store_sort, app_num, reviews_num, lang='en', country_array=['us']):
    for country in country_array:
        thread1 = Thread_Utility.MyThread(apple_store_search,
                                          (term, apple_store_sort, app_num, reviews_num, lang, country, country_array))
        thread2 = Thread_Utility.MyThread(google_play_search,
                                          (term, google_play_sort, app_num, reviews_num, lang, country, country_array))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    delete_google_json_data()
    print('finish')


def apple_store_search(term, sort, app_num, reviews_num, lang, country, country_array):
    start_time = time.time()
    apple_store_excel_name = country + '_' + term + '_apple_store.xlsx'
    apple_store_path = os.path.join(Scraper_API.apple_store_dir_path, apple_store_excel_name)
    Scraper_API.save_search_app_ranking_reviews(
        Scraper_API.Platform.Apple_Store.value, apple_store_path, term, sort, app_num,
        reviews_num, lang, country, country_array)
    print('Apple store search end, Time-consuming %d' % (time.time() - start_time), "s")


def google_play_search(term, sort, app_num, reviews_num, lang, country, country_array):
    start_time = time.time()
    google_play_excel_name = country + '_' + term + '_google_play.xlsx'
    google_play_path = os.path.join(Scraper_API.google_play_dir_path, google_play_excel_name)

    Scraper_API.save_search_app_ranking_reviews(
        Scraper_API.Platform.Google_Play.value, google_play_path, term, sort, app_num,
        reviews_num, lang, country, country_array)
    print('Google play search end, Time-consuming %d' % (time.time() - start_time), "s")


if __name__ == '__main__':
    root = tkinter.Tk()
    app = Application(master=root)
    app.mainloop()
