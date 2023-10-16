# -*- coding: utf-8 -*-
# time: 2023/9/9 12:46
# file: main_win.py
# author: shuoshuof

import sys
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.Init()
    def Init(self):
        self.btn_import = QPushButton("单词导入",self)

        self.btn_dictation = QPushButton("单词听写",self)

        self.btn_test = QPushButton("单词测试",self)

        self.btn_import.clicked.connect(self.import_words)
        self.btn_dictation.clicked.connect(self.dictation)
        self.btn_test.clicked.connect(self.test)


        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.btn_import)
        self.Vbox.addWidget(self.btn_dictation)
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
    def dictation(self):
        pass
    def test(self):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    apply_stylesheet(app, theme='light_blue.xml')

    sys.exit(app.exec_())