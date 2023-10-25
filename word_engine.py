import json, requests
from playsound import playsound
import os
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
        try:
            playsound('./audio.mp3')
            os.remove('./audio.mp3')
        except:
            print("音频错误")
if __name__ == '__main__':
    paraphrase_url = 'http://dict.youdao.com/suggest?num=1&doctype=json&q='
    audio_url = 'http://dict.youdao.com/dictvoice?type=1&audio='

    engine = WordEngine(paraphrase_url,audio_url)

    engine.get('successive')