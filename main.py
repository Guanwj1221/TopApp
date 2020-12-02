import os
import Google_Play_API
import Excel_Utility
import Apple_Store_API
import time
import threading
import tkinter
from tkinter import *
from tkinter import ttk


# GUI
class Application(tkinter.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.category_name = []
        self.category_member = []
        self.collection_name = []
        self.collection_member = []
        self.sort_name = []
        self.sort_member = []
        self.master = master
        master.title("TopApp")
        master.geometry('480x580')
        self.pack()

        self.category_label = Label(master, text='选择类型')
        self.category_label.place(x=10, y=10)

        self.category_value = tkinter.StringVar()
        self.category_box_list = ttk.Combobox(master=master, textvariable=self.category_value)
        self.category_box_list.place(x=200, y=10)

        self.collection_label = Label(master, text='选择榜单')
        self.collection_label.place(x=10, y=50)

        self.collection_value = tkinter.StringVar()
        self.collection_box_list = ttk.Combobox(master=master, textvariable=self.collection_value)
        self.collection_box_list.place(x=200, y=50)

        self.sort_label = Label(master, text='评论排序')
        self.sort_label.place(x=10, y=90)

        self.sort_value = tkinter.StringVar()
        self.sort_box_list = ttk.Combobox(master=master, textvariable=self.sort_value)
        self.sort_box_list.place(x=200, y=90)

        self.term_label = Label(master, text='查找APP的关键词')
        self.term_label.place(x=10, y=130)
        self.term_value = tkinter.StringVar()
        self.term_input = Entry(master, textvariable=self.term_value)
        self.term_input.place(x=200, y=130)

        self.num_label = Label(master, text='输入App数量(max 200)')
        self.num_label.place(x=10, y=170)
        self.num_value = tkinter.StringVar()
        self.num_value.set(100)
        self.num_input = Entry(master, textvariable=self.num_value)
        self.num_input.place(x=200, y=170)

        self.lang_label = Label(master, text='输入语言代码')
        self.lang_label.place(x=10, y=210)
        self.lang_value = tkinter.StringVar()
        self.lang_value.set('en')
        self.lang_input = Entry(master, textvariable=self.lang_value)
        self.lang_input.place(x=200, y=210)

        self.country_label = Label(master, text='输入国家代码')
        self.country_label.place(x=10, y=250)
        self.country_value = tkinter.StringVar()
        self.country_value.set('us')
        self.country_input = Entry(master, textvariable=self.country_value)
        self.country_input.place(x=200, y=250)

        self.count_label = Label(master, text='输入评论数量(max 5000)')
        self.count_label.place(x=10, y=290)
        self.count_value = tkinter.StringVar()
        self.count_value.set(500)
        self.count_input = Entry(master, textvariable=self.count_value)
        self.count_input.place(x=200, y=290)

        self.alertButton = Button(master, text='开始', command=self.start)
        self.alertButton.place(x=195, y=330)
        self.init_window()

    def init_window(self):
        for name, member in Google_Play_API.Category.__members__.items():
            self.category_name.append(name.title().replace('_', ' '))
            self.category_member.append(member.value)

        for name, member in Google_Play_API.Collection.__members__.items():
            self.collection_name.append(name.title().replace('_', ' '))
            self.collection_member.append(member.value)

        for name, member in Google_Play_API.Sort.__members__.items():
            self.sort_name.append(name.title().replace('_', ' '))
            self.sort_member.append(member.value)

        # self.category_label.pack()
        self.category_box_list['value'] = self.category_name
        self.category_box_list.current(0)
        # self.category_box_list.pack()

        # self.collection_label.pack()
        self.collection_box_list['value'] = self.collection_name
        self.collection_box_list.current(0)
        # self.collection_box_list.pack()

        # self.sort_label.pack()
        self.sort_box_list['value'] = self.sort_name
        self.sort_box_list.current(0)
        # self.sort_box_list.pack()

        # self.term_label.pack()
        # self.term_input.pack()
        #
        # self.num_label.pack()
        # self.num_input.pack()
        #
        # self.lang_label.pack()
        # self.lang_input.pack()
        #
        # self.country_label.pack()
        # self.country_input.pack()
        #
        # self.count_label.pack()
        # self.count_input.pack()

        # self.score_label.pack()
        # self.score_input.pack()

        # self.alertButton.pack()

    def start(self):
        category = self.category_box_list.current() or 0
        collection = self.collection_box_list.current() or 0
        sort = self.sort_box_list.current() or 0

        term = self.term_input.get()
        app_num = self.num_input.get() or 100

        country = self.country_input.get() or 'us'
        lang = self.lang_input.get() or 'en'
        review_num = self.count_input.get() or 500

        if term is None or term == "":
            rank(self.category_member[category], self.collection_member[collection],
                 app_num, lang, country, self.sort_member[sort], review_num)
        else:
            search(term, self.sort_member[sort], review_num, lang, country)


# 获取Google Play的数据
def get_google_play_data(category, collection, app_num, lang, country, sort, review_num):
    start_time = time.time()
    google_play_dir_path = 'GooglePlay'
    if not os.path.exists(google_play_dir_path):
        os.system('mkdir ' + google_play_dir_path)
    reviews_path = os.path.join(google_play_dir_path, 'JsonData')
    if not os.path.exists(reviews_path):
        os.system('mkdir ' + reviews_path)
    google_play_excel_name = category + '_' + collection + '_google_play.xlsx'
    google_play_path = os.path.join(google_play_dir_path, google_play_excel_name)
    Google_Play_API.get_app_ranking_reviews(
        google_play_path, category, collection, app_num, lang, country, sort, review_num)
    os.system('rm -rf ' + reviews_path + '/*')
    print('耗时%d' % (time.time() - start_time), "s")


# 获取App Store的数据
def get_app_store_data(term, num, lang, country):
    start_time = time.time()
    apple_store_dir_path = 'AppStore'
    if not os.path.exists(apple_store_dir_path):
        os.system('mkdir ' + apple_store_dir_path)
    apple_store_excel_name = term + '_app_store.xlsx'
    apple_store_path = os.path.join(apple_store_dir_path, apple_store_excel_name)

    Apple_Store_API.write_ranking_in_excel(apple_store_path, term, num, lang, country)
    print('耗时%d' % (time.time() - start_time), "s")


# path: Excel表格名称
# collection: Google Play 榜单，默认为 Collection.TOP_FREE
# category: App 种类，默认为无
# app_num: App数量，默认 500
# lang: 语言，默认为 'en'
# country: 国家，默认为 'us'
# sort: 排序方式，默认为 Sort.NEWEST
# review_num: 评论数量
def rank(category='', collection='', app_num=100, lang='en',
         country='us', sort='', review_num=500):
    thread_1 = threading.Thread(
        target=get_google_play_data,
        args=(category, collection, app_num, lang, country, sort, review_num,))
    # thread_2 = threading.Thread(target=get_app_store_data, args=(term, num, lang, country,))
    thread_1.start()
    # thread_2.start()


def search(term, sort, num, lang='en', country='us'):
    start_time = time.time()
    content = Google_Play_API.get_app_reviews('com.intsig.camscanner', lang, country, sort, num)
    print(content)
    apple_store_dir_path = 'AppStore'
    if not os.path.exists(apple_store_dir_path):
        os.system('mkdir ' + apple_store_dir_path)
    apple_store_excel_name = term + '_google_play.xlsx'
    Excel_Utility.write_reviews(apple_store_excel_name, term, content)
    print('耗时%d' % (time.time() - start_time), "s")

    # thread_2 = threading.Thread(target=get_app_store_data, args=(term, num, lang, country,))
    # thread_1.start()
    # thread_2.start()


if __name__ == '__main__':
    root = tkinter.Tk()
    app = Application(master=root)
    app.mainloop()