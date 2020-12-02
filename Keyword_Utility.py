#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def get_exclude_words():
    file = open('words.txt', "r+", 1024, "utf-8")
    content = ''
    for line in file:
        content += line.replace("_", " ")
    words = content.split(" ")
    # 去重
    words_set = list(dict.fromkeys(words))
    print("需要去除的词语", words_set)
    return words_set


def find_keyword(find_string):
    # 去重
    find_works = find_string.split(" ")
    find_works = list(dict.fromkeys(find_works))
    print("需要查找的词语", find_works)
    # 获取需要去除的词语
    exclude_words = get_exclude_words()

    result_words = []
    # 遍历
    for find_word in find_works:
        # 只匹配字母
        word = re.sub(r'\W*', '', find_word)
        if word is not '':
            result_words.append(word)
            for exclude_word in exclude_words:
                if exclude_word.lower() == word.lower() or exclude_word.lower() is word.lower():
                    result_words.remove(word)
                    break
                else:
                    continue
    print("最终剩下的词语", len(result_words), result_words)
    return result_words
