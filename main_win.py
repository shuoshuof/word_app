# -*- coding: utf-8 -*-
# time: 2023/9/9 12:46
# file: main_win.py
# author: shuoshuof

import sys
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
from setting_win import SettingWindow
from utils import WordSmapler,WordTrainer
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.Init()
    def Init(self):
        self.btn_import = QPushButton("词表导入",self)

        self.btn_input = QPushButton("单词写入",self)

        self.btn_test = QPushButton("单词测试",self)

        self.btn_import.clicked.connect(self.import_words)
        self.btn_input.clicked.connect(self.input)
        self.btn_test.clicked.connect(self.test)


        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.btn_import)
        self.Vbox.addWidget(self.btn_input)
        self.Vbox.addWidget(self.btn_test)

        self.Hbox = QHBoxLayout()
        self.Hbox.addStretch(1)
        self.Hbox.addLayout(self.Vbox)
        self.Hbox.addStretch(1)
        self.setLayout(self.Hbox)

        self.setGeometry(300, 300,400, 400)
        self.setWindowTitle('单词APP')
        self.show()

    def import_words(self):
        pass
    def input(self):
        pass
    def test(self):
        setting_window = SettingWindow()
        if setting_window.exec_() == QDialog.Accepted:
            attr = setting_window.return_attr
            word_sampler = WordSmapler(sample_size=attr['num_words'])
            if attr['path'] =='':
                self.word_list = word_sampler.get_new_vocabulary()
            else:
                self.word_list = word_sampler.get_from_file(attr['path'])

            word_trainer= WordTrainer(self.word_list)
            if attr['mode'] == '听写':
                word_trainer.dictation_train()
            if attr['mode'] == '复习':
                word_trainer.reading_train()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    apply_stylesheet(app, theme='light_blue.xml')

    sys.exit(app.exec_())