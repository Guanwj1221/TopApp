#!/usr/bin/python3
# coding=utf-8
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


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


def get_google_play_reviews(func, app_ids, lang, country, sort, review_num):
    contents = []
    all_task = []
    num = 0
    executor = ThreadPoolExecutor(max_workers=20)
    for app_id in app_ids:
        task = executor.submit(func, app_id, lang, country, sort, review_num)
        all_task.append(task)
    for future in as_completed(all_task):
        data = future.result()
        contents.append(data)
        num += 1
        per = num / len(app_ids) * 100
        print("获取Google play 评论数据进度：%.2f" % per, '%')
    return contents
