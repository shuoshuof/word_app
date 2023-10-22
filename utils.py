# -*- coding: utf-8 -*-
# time: 2023/10/13 16:35
# file: utils.py
# author: shuoshuof
import pandas as pd
from  datetime import datetime
import math
import json, requests
from playsound import playsound
import os
import time
import keyboard
class WordEngine:
    def __init__(self,paraphrase_url='http://dict.youdao.com/suggest?num=1&doctype=json&q=',
                 audio_url='http://dict.youdao.com/dictvoice?type=1&audio='):
        self.paraphrase_url = paraphrase_url
        self.audio_url = audio_url
    def get(self,word):
        explain = self.get_paraphrase(word)
        self.get_audio(word)
        return explain
    def get_paraphrase(self,word:str):
        url = self.paraphrase_url+word
        res = requests.get(url).json()
        data = res['data']
        entries = data['entries']
        explain = entries[0]['explain']
        return explain
    def get_audio(self,word):
        url = self.audio_url+word
        sound_bytes  = requests.get(url).content
        with open('./audio.mp3', 'wb') as file:  # 保存到本地的文件名
            file.write(sound_bytes)
            file.flush()
        playsound('./audio.mp3')
        os.remove('./audio.mp3')

class WordSmapler:
    def __init__(self,sample_size=50):
        self.sample_size = sample_size

    def get_new_vocabulary(self):
        words = pd.read_excel('./data/words.xlsx')
        date = datetime.date(datetime.now())
        # word_list = words.query(f"date =='{date}'")
        # # 去除今天已经复习的单词
        # word_list = word_list.query(f"review_date != '{date}'")
        # 提取测试次数为0 或 今天新录入的单词
        word_list = words.query(f"test_num == 0 or date =='{date}'")
        word_list = word_list.head(self.sample_size)
        word_list = list(word_list['word'])
        return word_list
    def get_review_vocabulary(self):
        words = pd.read_excel('./data/words.xlsx')
        date = datetime.date(datetime.now())
        # 去除复习日期为当天的单词，即单词今天已经复习过了
        review_list = words.query(f"review_date !='{date}'")
        review_list = review_list.sort_values(by='acc',ascending=True)
        review_list = review_list.head(self.sample_size)

        review_list = list(review_list['word'])
        return review_list

class WordTrainer:
    def __init__(self,word_list:list):
        self.word_list = word_list
        self.word_engine = WordEngine()
        self.acc_calculator = EWMA()
    def dictation_train(self):
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
    def reading_train(self):
        while len(self.word_list):
            word = self.word_list.pop(0)

            acc,test_num = get_excel(word,attributes=['acc','test_num'])
            explain = self.word_engine.get(word)

            print(word)
            input()
            print(explain)
            answer = str(input('是否记得？'))

            test_num += 1

            if answer=='y':
                acc = self.acc_calculator.update(V_t=acc, theta_t=1, t=test_num)
                modified_data = {
                    'review_date': datetime.date(datetime.now()),
                    'test_num': test_num,
                    'acc': acc
                }

            else:
                self.word_list.append(word)
                acc = self.acc_calculator.update(V_t=acc,theta_t=0,t=test_num)
                # 更改acc 和测试次数，当输入错误时，不更新复习日期
                modified_data = {
                    'test_num': test_num,
                    'acc':acc
                }
            modify_excel(word, modified_data)
class EWMA:
    def __init__(self,sample_num=5):
        self.sample_num = sample_num
        self.beta =math.exp(-1/self.sample_num)
    def update(self,V_t,theta_t,t):
        # V_t : acc theta: answer is right or not t: test_num

        V_t = self.beta*V_t + (1-self.beta)*theta_t
        V_t = V_t/(1-self.beta**t)
        return V_t

def modify_excel(word,modified_data,excel_path ='./data/words.xlsx'):
    words = pd.read_excel(excel_path,index_col=0)
    for key,value in modified_data.items():
        if value is not None:
            words.loc[word,key] = value

    words.to_excel(excel_path)
def get_excel(word,attributes,excel_path ='./data/words.xlsx'):
    words = pd.read_excel(excel_path,index_col=0)
    return [words.loc[word,attr] for attr in attributes]
if __name__ == '__main__':
    #modify_excel(word='critical',modified_data={'test_num':0})
    word_sampler = WordSmapler(sample_size=2)
    word_list = word_sampler.get_new_vocabulary()
    WordTrainer = WordTrainer(word_list)
    WordTrainer.reading_train()
