# -*- coding: utf-8 -*-
# time: 2023/9/9 13:37
# file: dictation_win.py
# author: shuoshuof

import sys
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
from PyQt5 import QtCore, QtWidgets
from  datetime import datetime
import pandas as pd
from word_engine import WordEngine
import time
class DictationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Init()
    def Init(self):
        word_list = self.get_words_list()
    def get_words_list(self):
        words = pd.read_excel('./data/words.xlsx')
        date = datetime.date(datetime.now())
        word_list = words[words['date']==date]
        print(word_list)
        return word_list
def get_words_list():
    words = pd.read_excel('./data/words.xlsx')
    date = datetime.date(datetime.now())

    word_list = words.query(f"date =='{date}'")
    return word_list

if __name__ == '__main__':
    engine = WordEngine()
    word_list = get_words_list()
    words = list(word_list['word'])[:5]

    while True:
        word = words.pop(0)
        explain = engine.get(word)
        answer = str(input())

        if word != answer:
            words.append(word)
            print('错误')
            print(word)
            while str(input())!=word:
                pass
        print(explain)
        time.sleep(1)
