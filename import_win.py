# -*- coding: utf-8 -*-
# time: 2023/9/9 19:33
# file: import_win.py
# author: shuoshuof
import sys
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
from PyQt5 import QtCore, QtWidgets
import os
import pandas as pd
from  datetime import datetime
class ImportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Init()
    def Init(self):
        self.dir_input = QLineEdit()
        self.dir_input.setText(r'C:\Users\shuoshuo\Desktop\项目\单词app\单词.xlsx')
        btn_ChooseDir = QPushButton("选择单词表")
        btn_ChooseDir.clicked.connect(self.slot_btn_chooseDir)

        list_choose = QComboBox()
        list_choose.addItem("听写")
        list_choose.addItem("阅读")

        btn_submit = QPushButton("导入")
        btn_submit.clicked.connect(self.sumbit)

        btnbox = QGridLayout()
        btnbox.addWidget(self.dir_input,0,0,1,2)
        btnbox.addWidget(btn_ChooseDir,0,3,1,1)

        btnbox.addWidget(list_choose,1,0,1,1)
        btnbox.addWidget(btn_submit,1,3,1,1)

        self.setLayout(btnbox)

        self.setGeometry(300, 300,400, 400)
        self.setWindowTitle('导入单词')
        self.show()
    def slot_btn_chooseDir(self):
        dir_choose = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", "")
        print(dir_choose)
        if dir_choose == "":
            print("\n取消选择")
        else:
            self.dir_input.setText(dir_choose[0])
    def sumbit(self):

        path = self.dir_input.text()
        file_type = os.path.splitext(path)[-1]
        print(file_type)
        if file_type  not in ['.csv', '.xlsx']:
            print("文件类型错误")
        else:
            import_data = pd.read_excel(io=path).iloc[:, 0]
            import_data = pd.DataFrame(import_data)

            import_data.set_index('word', inplace=True)
            if os.path.exists('./data/words.xlsx') and  False:
                data = pd.read_excel(io='./data/words.xlsx')
            else:
                data = pd.DataFrame([], columns=['word', 'date', 'acc','review_date','test_num'])
            data.set_index('word', inplace=True)


            for word in import_data.index:
                data.loc[word, :] = [datetime.date(datetime.now()), 0,None,0]
            print(data)
            data.date = pd.to_datetime(data.date)
            data.to_excel('./data/words.xlsx')



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ImportWindow()
    apply_stylesheet(app, theme='light_blue.xml')

    sys.exit(app.exec_())
    # path = r'C:\Users\shuoshuo\Desktop\项目\单词app\单词.xlsx'
    # import_data = pd.read_excel(io=path).iloc[:, 0]
    # import_data = pd.DataFrame(import_data)
    #
    # import_data.set_index('word',inplace=True)
    # print(import_data)
    #
    # if os.path.exists('./data/words.xlsx'):
    #     data = pd.read_excel(io='./data/words.xlsx')
    # else:
    #     data = pd.DataFrame([], columns=['word','date', 'acc'])
    # data.set_index('word', inplace=True)
    #
    # for word in import_data.index:
    #
    #     data.loc[word, :] = [datetime.date(datetime.now()), 1]
    # print(data)
    # data.to_excel('./data/words.xlsx')