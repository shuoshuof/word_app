# -*- coding: utf-8 -*-
# time: 2023/10/21 22:31
# file: setting_win.py
# author: shuoshuof

import sys
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QButtonGroup
from  datetime import datetime
import pandas as pd
from word_engine import WordEngine
import time
from utils import WordSmapler,WordEngine,EWMA,get_excel,modify_excel
from PyQt5.QtCore import pyqtSignal
class SettingWindow(QDialog):
    return_dict = pyqtSignal(dict)
    def __init__(self):
        super(SettingWindow, self).__init__()
        self.Init()
    def Init(self):
        self.list_dir = QLineEdit()
        btn_ChooseDir = QPushButton("选择单词表")
        btn_ChooseDir.clicked.connect(self.slot_btn_chooseDir)

        btn_submit = QPushButton("确认")
        btn_submit.clicked.connect(self.sumbit)

        self.review_num = QLineEdit()
        self.review_num.setText("50")

        label = QLabel("单词数目")
        self.num_words = QLineEdit()
        self.num_words.setText("50")

        self.dictation_btn = QRadioButton("听写",self)
        self.dictation_btn.setChecked(True)

        self.reading_btn = QRadioButton("复习",self)

        self.mode = "听写"
        self.dictation_btn.toggled.connect(self.buttonState)
        self.reading_btn.toggled.connect(self.buttonState)


        # self.button_group = QButtonGroup(self)
        # self.button_group.addButton(self.dictation_mode,11)
        # self.button_group.addButton(self.reading_mode,21)

        self.gbox = QGridLayout()
        self.gbox.addWidget(self.list_dir,0,0,1,2)
        self.gbox.addWidget(btn_ChooseDir, 0, 3, 1, 1)
        self.gbox.addWidget(label,1,0,1,1)
        self.gbox.addWidget(self.num_words,1,1,1,1)

        self.gbox.addWidget(self.dictation_btn,1,2,1,1)
        self.gbox.addWidget(self.reading_btn,1,3,1,1)
        self.gbox.addWidget(btn_submit,2,1,1,1)
        self.setLayout(self.gbox)

        self.setGeometry(300, 200,400, 400)
        self.setWindowTitle('复习设置')
        self.show()
    def buttonState(self):
        btn= self.sender()
        if btn.isChecked():
            self.mode = btn.text()
            print(self.mode)
    def slot_btn_chooseDir(self):
        dir_choose = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", "")
        print(dir_choose)
        if dir_choose == "":
            print("\n取消选择")
        else:
            self.list_dir.setText(dir_choose[0])
    def sumbit(self):
        path = self.list_dir.text()
        num_words = int(self.num_words.text())
        print(path)
        self.return_attr = {"path": path, "num_words": int(num_words),"mode": self.mode}
        self.accept()
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SettingWindow()
    apply_stylesheet(app, theme='light_blue.xml')

    sys.exit(app.exec_())
