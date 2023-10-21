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
from utils import WordSmapler,WordEngine,EWMA,get_excel,modify_excel

class DictationWindow():
    def __init__(self,word_list:list):
        super().__init__()
        self.word_list = word_list
        self.word_engine = WordEngine()
        self.acc_calculator = EWMA()
        self.Init()
    def Init(self):
        pass
    def train(self):
        while len(self.word_list):
            word = self.word_list.pop(0)

            acc,test_num = get_excel(word,attributes=['acc','test_num'])
            explain = self.word_engine.get(word)
            answer = str(input())

            test_num += 1

            if word != answer:
                self.word_list.append(word)
                print('错误')
                print(word)
                acc = self.acc_calculator.update(V_t=acc,theta_t=0,t=test_num)
                # 更改acc 和测试次数，当输入错误时，不更新复习日期
                modified_data = {
                    'test_num': test_num,
                    'acc':acc
                }

                while str(input()) != word:
                    pass
            else:
                acc = self.acc_calculator.update(V_t=acc,theta_t=1,t=test_num)
                modified_data = {
                    'review_date':datetime.date(datetime.now()),
                    'test_num': test_num,
                    'acc':acc
                }
            modify_excel(word, modified_data)
            print(explain)
            time.sleep(1)


if __name__ == '__main__':
    # engine = WordEngine()
    # word_list = get_words_list()
    # words = list(word_list['word'])[:5]
    #
    # while True:
    #     word = words.pop(0)
    #     explain = engine.get(word)
    #     answer = str(input())
    #
    #     if word != answer:
    #         words.append(word)
    #         print('错误')
    #         print(word)
    #         while str(input())!=word:
    #             pass
    #     print(explain)
    #     time.sleep(1)
    word_sampler = WordSmapler(sample_size=50)
    word_list = word_sampler.get_new_vocabulary()
    dictation_win = DictationWindow(word_list)
    dictation_win.train()

