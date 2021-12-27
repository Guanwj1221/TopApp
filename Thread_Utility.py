#!/usr/bin/python3
# coding=utf-8
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class MyThread(threading.Thread):
    def __init__(self, func, args) -> object:
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


def get_all_app_reviews(func, system, app_ids, lang, country, sort, review_num):
    contents = []
    complete_app = []
    all_task = []
    num = 0
    executor = ThreadPoolExecutor(max_workers=10)
    for app_id in app_ids:
        task = executor.submit(func, system, app_id, lang, country, sort, review_num)
        all_task.append(task)
    for future in as_completed(all_task):
        app_id, data = future.result()
        contents.append(data)
        complete_app.append(app_id)
        num += 1
        per = num / len(app_ids) * 100
    return complete_app, contents


def get_all_app_details(func, system, app_ids, lang, country):
    contents = []
    all_task = []
    num = 0
    executor = ThreadPoolExecutor(max_workers=10)
    for app_id in app_ids:
        task = executor.submit(func, system, app_id, lang, country)
        all_task.append(task)
    for future in as_completed(all_task):
        data = future.result()
        contents.append(data)
        num += 1
        per = num / len(app_ids) * 100
    return contents


