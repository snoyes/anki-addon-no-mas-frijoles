import os, sys
sys.path.append(".")
import time
from PyQt5 import QtCore,QtWidgets
from aqt import mw
from aqt.qt import *
from aqt.utils import showCritical
import json
from .Translations import LANGUAGES
import re, urllib.parse as urlparse
from .BookText import supported, spacedLangs, allsupported
import requests
from . import TextExtract

try:
    from YoutubeExtract import run
except:
    pass


class Info:

    def get_decks(self):
        decks = mw.col.decks.allNames()
        return decks

    def get_notes(self):
        notes = mw.col.models.allNames()
        return notes


    def get_field(self):

        modeljson = mw.col.db.all("select models from col")[0][0]
        pyjson = json.loads(modeljson)
        fields = []

        for key in pyjson.keys():
            for i in pyjson[key]["flds"]:
                fields.append(pyjson[key]["name"] + ": " + i["name"])

        return fields



#config
with open(r"config.json") as c:
    alljson = c.read()

config = json.loads(alljson)


class ThumbListWidget(QtWidgets.QListWidget):

    def __init__(self,type,parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            filename, extension = os.path.splitext(filepath)
            if extension in supported:
                item = QtWidgets.QListWidgetItem(filepath , self)
            else:
                dialog = QtWidgets.QMessageBox()
                dialog.setWindowTitle("Error: Invalid Filetype")
                dialog.setText("File type not supported")
                dialog.setIcon(QtWidgets.QMessageBox.Warning)
                dialog.exec_()


class Ui_Form(object):

    def setupUi(self, Form):
        userInfo = Info()
        decks = userInfo.get_decks()
        fields = userInfo.get_field()
        notes = userInfo.get_notes()
        langs = LANGUAGES.values()
        Form.setObjectName("")
        Form.setFixedSize(690,550)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName("groupBox_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 40, 540, 20))
        self.lineEdit_2.setObjectName("link input")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 40, 65, 20))
        self.comboBox_2.setObjectName("youtube_drop_down")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.comboBox_5 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_5.setObjectName("deck")
        self.comboBox_5.addItems(decks)
        self.horizontalLayout_10.addWidget(self.comboBox_5)
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_4.setObjectName("note")
        self.comboBox_4.addItems(notes)

        self.horizontalLayout_10.addWidget(self.comboBox_4)
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_3.setObjectName("field")
        self.comboBox_3.addItems(fields)
        self.horizontalLayout_10.addWidget(self.comboBox_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_2.setObjectName("generate_translation")
        self.horizontalLayout_11.addWidget(self.checkBox_2)
        self.checkBox_2.stateChanged.connect(self.transBool)
        self.comboBox_6 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_6.setObjectName("languages")
        self.comboBox_6.addItem("Language To Translate To")
        self.comboBox_6.addItems(langs)
        self.horizontalLayout_11.addWidget(self.comboBox_6)

        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.comboBox_9 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_9.setObjectName("Deck_trans")
        self.comboBox_9.addItems(decks)
        self.horizontalLayout_12.addWidget(self.comboBox_9)
        self.comboBox_8 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_8.setObjectName("note_trans")
        self.comboBox_8.addItems(notes)
        self.horizontalLayout_12.addWidget(self.comboBox_8)
        self.comboBox_7 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_7.setObjectName("fields_trans")
        self.comboBox_7.addItems(fields)
        self.horizontalLayout_12.addWidget(self.comboBox_7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_4.setObjectName("titlebool")
        self.horizontalLayout_13.addWidget(self.checkBox_4)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_3.setObjectName("deleteEng")
        self.horizontalLayout_13.addWidget(self.checkBox_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_15.addWidget(self.label_5)
        self.spinBox_4 = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_4.setObjectName("limit")
        self.spinBox_4.setRange(0, 1000000000)
        self.horizontalLayout_15.addWidget(self.spinBox_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_2.setObjectName("Generate")
        self.horizontalLayout_14.addWidget(self.pushButton_2)
        self.pushButton_2.setStyleSheet("QWidget#Generate {color:green}")
        self.pushButton_2.clicked.connect(self.pressed)

        self.verticalLayout_3.addLayout(self.horizontalLayout_14)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_8)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_8)
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setGeometry(QtCore.QRect(10, 20, 601, 16))
        self.label_8.setObjectName("label_8")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox_6)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 625, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tableFiles = ThumbListWidget(self)
        self.verticalLayout_8.addWidget(self.tableFiles)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_5.setGeometry(QtCore.QRect(90, 210, 161, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.deleteItem)

        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_7.setGeometry(QtCore.QRect(350, 210, 161, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.clearList)
        self.verticalLayout_4.addWidget(self.groupBox_6)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_8)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.comboBox_10 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItems(decks)
        self.horizontalLayout_16.addWidget(self.comboBox_10)
        self.comboBox_11 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_11.addItems(notes)
        self.horizontalLayout_16.addWidget(self.comboBox_11)
        self.comboBox_12 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_12.addItems(fields)
        self.horizontalLayout_16.addWidget(self.comboBox_12)

        self.verticalLayout_6.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_17.addWidget(self.checkBox_5)
        self.checkBox_5.stateChanged.connect(self.transBoolBook)
        self.comboBox_13 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("Language To Translate To")
        self.horizontalLayout_17.addWidget(self.comboBox_13)
        self.comboBox_13.addItems(langs)
        self.verticalLayout_6.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.comboBox_14 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_14.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_14.addItems(decks)

        self.horizontalLayout_18.addWidget(self.comboBox_14)
        self.comboBox_15 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_15.setObjectName("comboBox_15")
        self.comboBox_15.addItems(notes)

        self.horizontalLayout_18.addWidget(self.comboBox_15)
        self.comboBox_16 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_16.setObjectName("comboBox_16")
        self.comboBox_16.addItems(fields)

        self.horizontalLayout_18.addWidget(self.comboBox_16)
        self.verticalLayout_6.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_21.addWidget(self.label_9)
        self.spinBox_5 = QtWidgets.QSpinBox(self.groupBox_5)
        self.spinBox_5.setObjectName("spinBox_5")
        self.horizontalLayout_21.addWidget(self.spinBox_5)
        self.spinBox_5.setRange(0, 1000000000)
        self.verticalLayout_6.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_22.addWidget(self.pushButton_4)
        self.pushButton_4.setStyleSheet("QWidget {color:green}")
        self.pushButton_4.clicked.connect(self.pressBook)
        self.verticalLayout_6.addLayout(self.horizontalLayout_22)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_7)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab_7)
        self.groupBox_7.setObjectName("groupBox_7")
        self.label_10 = QtWidgets.QLabel(self.groupBox_7)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.label_10.setObjectName("label_10")
        self.URLBox = QtWidgets.QLineEdit(self.groupBox_7)
        self.URLBox.setGeometry(QtCore.QRect(80, 30, 531, 20))
        self.URLBox.setObjectName("URLBox")
        self.verticalLayout_5.addWidget(self.groupBox_7)
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_7)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.comboBox_17 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_17.setObjectName("comboBox_17")
        self.comboBox_17.addItems(decks)

        self.horizontalLayout_19.addWidget(self.comboBox_17)
        self.comboBox_18 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_18.setObjectName("comboBox_18")
        self.comboBox_18.addItems(notes)

        self.horizontalLayout_19.addWidget(self.comboBox_18)
        self.comboBox_19 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItems(fields)

        self.horizontalLayout_19.addWidget(self.comboBox_19)
        self.verticalLayout_7.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.checkBox_8 = QtWidgets.QCheckBox(self.groupBox_8)
        self.checkBox_8.setObjectName("checkBox_8")

        self.horizontalLayout_23.addWidget(self.checkBox_8)
        self.checkBox_8.stateChanged.connect(self.transBoolWeb)
        self.comboBox_20 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_20.setObjectName("comboBox_20")
        self.comboBox_20.addItem("Language To Translate To")
        self.comboBox_20.addItems(langs)

        self.horizontalLayout_23.addWidget(self.comboBox_20)
        self.verticalLayout_7.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.comboBox_21 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_21.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBox_21.setObjectName("comboBox_21")
        self.comboBox_21.addItems(decks)

        self.horizontalLayout_24.addWidget(self.comboBox_21)
        self.comboBox_22 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_22.setObjectName("comboBox_22")
        self.comboBox_22.addItems(notes)

        self.horizontalLayout_24.addWidget(self.comboBox_22)
        self.comboBox_23 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_23.setObjectName("comboBox_23")
        self.comboBox_23.addItems(fields)

        self.horizontalLayout_24.addWidget(self.comboBox_23)
        self.verticalLayout_7.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_12 = QtWidgets.QLabel(self.groupBox_8)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_26.addWidget(self.label_12)
        self.spinBox_7 = QtWidgets.QSpinBox(self.groupBox_8)
        self.spinBox_7.setObjectName("spinBox_7")
        self.horizontalLayout_26.addWidget(self.spinBox_7)
        self.spinBox_7.setRange(0, 1000000000)
        self.verticalLayout_7.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_8)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_27.addWidget(self.pushButton_6)

        self.pushButton_6.clicked.connect(self.webpress)
        self.verticalLayout_7.addLayout(self.horizontalLayout_27)
        self.pushButton_6.setStyleSheet("QWidget {color:green}")
        self.verticalLayout_5.addWidget(self.groupBox_8)
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 92, 16))
        self.label.setObjectName("label")
        self.label.setStyleSheet("QWidget#label {color:red}")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(110, 40, 511, 20))
        self.lineEdit.setObjectName("APIKey")
        self.verticalLayout_2.addWidget(self.groupBox)
        self.lineEdit.setText(str(config["API KEY"]))
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 191, 16))
        self.label_7.setObjectName("label_7")
        self.label_7.setStyleSheet("QWidget {color:red}")
        self.learnLang = QtWidgets.QComboBox(self.groupBox)
        self.learnLang.setGeometry(QtCore.QRect(210, 110, 101, 22))
        self.learnLang.setObjectName("learnLang")
        self.learnLang.addItem("Language")
        self.learnLang.addItems(langs)
        self.learnLang.setCurrentText(config["LangLearning"])
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 181, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget_2)
        self.toolButton.setObjectName("outFile")
        self.toolButton.clicked.connect(self.filePicker)
        self.horizontalLayout_5.addWidget(self.toolButton)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(20, 110, 181, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox.setObjectName("MinWords")
        self.spinBox.setRange(0, 150)
        self.horizontalLayout_6.addWidget(self.spinBox)
        self.spinBox.setValue(config["MinWords"])
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 160, 181, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_7.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.horizontalLayoutWidget_4)
        self.spinBox_2.setObjectName("maxwords")
        self.spinBox_2.setValue(config["MaxWords"])
        self.horizontalLayout_7.addWidget(self.spinBox_2)
        self.spinBox_2.setRange(0, 150)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(300, 30, 246, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout_3.addWidget(self.tabWidget)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 190, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.save_pref)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(20, 90, 441, 17))
        self.checkBox.setObjectName("checkBox")

        if config["UseRange"] == "True":
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)
        self.retranslateUi(Form)
        self.checkBox.stateChanged.connect(self.wordbool)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.comboBox_6.setEnabled(False)
        self.comboBox_9.setEnabled(False)
        self.comboBox_8.setEnabled(False)
        self.comboBox_7.setEnabled(False)
        self.comboBox_20.setEnabled(False)
        self.comboBox_21.setEnabled(False)
        self.comboBox_22.setEnabled(False)
        self.comboBox_23.setEnabled(False)
        self.comboBox_13.setEnabled(False)
        self.comboBox_14.setEnabled(False)
        self.comboBox_15.setEnabled(False)
        self.comboBox_16.setEnabled(False)

        if config["UseRange"] == "False":
            self.spinBox.setEnabled(False)
            self.spinBox_2.setEnabled(False)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sentence Factory"))
        self.groupBox_3.setTitle(_translate("Form", "Link"))
        self.comboBox_2.setItemText(0, _translate("Form", "Video"))
        self.comboBox_2.setItemText(1, _translate("Form", "Channel"))
        self.comboBox_2.setItemText(2, _translate("Form", "Playlist"))
        self.groupBox_4.setTitle(_translate("Form", "Deck Settings"))
        self.comboBox_5.setItemText(0, _translate("Form", "Target Deck"))
        self.comboBox_4.setItemText(0, _translate("Form", "Note Type"))
        self.comboBox_3.setItemText(0, _translate("Form", "Field"))
        self.checkBox_2.setText(_translate("Form", "Automatically Generate Translations (Not Reccomended)"))
        self.comboBox_9.setItemText(0, _translate("Form", "Target Deck"))
        self.comboBox_8.setItemText(0, _translate("Form", "Note Type"))
        self.comboBox_7.setItemText(0, _translate("Form", "Field"))
        self.checkBox_4.setText(_translate("Form", "Include Titles"))
        self.checkBox_3.setText(_translate("Form", "Automatically Delete All English Cards"))
        self.label_5.setText(_translate("Form", "Number Of Cards To Generate"))
        self.pushButton_2.setText(_translate("Form", "Generate"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Youtube"))
        self.groupBox_6.setTitle(_translate("Form", "Book/Text"))
        self.label_8.setText(_translate("Form", "Drag and drop files into the box"))
        self.groupBox_5.setTitle(_translate("Form", "Deck Settings"))
        self.comboBox_10.setItemText(0, _translate("Form", "Target Deck"))
        self.comboBox_11.setItemText(0, _translate("Form", "Note Type"))
        self.comboBox_12.setItemText(0, _translate("Form", "Field"))
        self.checkBox_5.setText(_translate("Form", "Automatically Generate Translations (Not Reccomended)"))
        self.comboBox_14.setItemText(0, _translate("Form", "Target Deck"))
        self.comboBox_15.setItemText(0, _translate("Form", "Note Type"))
        self.comboBox_16.setItemText(0, _translate("Form", "Field"))
        self.label_9.setText(_translate("Form", "Number Of Cards To Generate"))
        self.pushButton_4.setText(_translate("Form", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("Form", "Book/Text"))
        self.groupBox_7.setTitle(_translate("Form", "Link"))
        self.label_10.setText(_translate("Form", "Website URL"))
        self.groupBox_8.setTitle(_translate("Form", "Deck Settings"))
        self.comboBox_17.setItemText(0, _translate("Form", "Target Deck"))
        self.comboBox_18.setItemText(0, _translate("Form", "Note Type"))
        self.comboBox_19.setItemText(0, _translate("Form", "Field"))
        self.checkBox_8.setText(_translate("Form", "Automatically Generate Translations (Not Reccomended)"))
        self.pushButton_5.setText(_translate("Form", "Delete item"))
        self.pushButton_7.setText(_translate("Form", "Clear"))
        self.comboBox_21.setItemText(0, _translate("Form", "Target Deck"))
        self.comboBox_22.setItemText(0, _translate("Form", "Note Type"))
        self.comboBox_23.setItemText(0, _translate("Form", "Field"))
        self.label_12.setText(_translate("Form", "Number Of Cards To Generate"))
        self.pushButton_6.setText(_translate("Form", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Form", "Website"))
        self.groupBox.setTitle(_translate("Form", "API Key"))
        self.label.setText(_translate("Form", "API Key (Required)"))
        self.label_7.setText(_translate("Form", "Language currently learning (Required)"))
        self.groupBox_2.setTitle(_translate("Form", "Additional Settings"))
        self.label_4.setText(_translate("Form", "Always Add Sentences to File"))
        self.toolButton.setText(_translate("Form", "..."))
        self.label_3.setText(_translate("Form", "Min Words in A Card"))
        self.label_2.setText(_translate("Form", "Max Words in A Card"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "Settings"))
        self.pushButton_3.setText(_translate("Form", "Save Settings"))
        self.checkBox.setText(_translate("Form", "Use a specific word range(No support for languages with no spaces in between words)"))

    def transBool(self, state):
        if state == QtCore.Qt.Checked:
            self.comboBox_6.setEnabled(True)
            self.comboBox_9.setEnabled(True)
            self.comboBox_8.setEnabled(True)
            self.comboBox_7.setEnabled(True)
    def wordbool(self,state):
        if state == QtCore.Qt.Checked:
            self.spinBox.setEnabled(True)
            self.spinBox_2.setEnabled(True)

    def check_link(self,link, tubeType):
        if tubeType == "Video":
            reID = re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)')
            mo = reID.search(link)
            if mo == None:
                return False
            return True
        elif tubeType == "Channel":
            channelRE = re.compile("channel/(.*)")
            mo = channelRE.search(link)
            if mo == None:
                return False
            return True
        else:
            url_data = urlparse.urlparse(link)
            query = urlparse.parse_qs(url_data.query)
            try:
                playlistId = query["list"][0]
            except:
                return False
            else:
                return True

    def pressed(self):
        self.tubeType = self.comboBox_2.currentText()
        self.deckChoice = self.comboBox_5.currentText()
        self.noteChoice = self.comboBox_4.currentText()
        self.fieldChoice = self.comboBox_3.currentText()
        self.deckChoice2 = self.comboBox_9.currentText()
        self.noteChoice2 = self.comboBox_8.currentText()
        self.fieldChoice2 = self.comboBox_7.currentText()
        self.langChoice = self.comboBox_6.currentText()
        self.numcards = self.spinBox_4.value()
        self.inclTitle = self.checkBox_4.isChecked()
        self.delEng = self.checkBox_3.isChecked()
        self.link = self.lineEdit_2.text()
        self.trans = self.checkBox_2.isChecked()

        try:
            if not self.check_link(self.link, self.tubeType):
                showCritical("Invalid link. Check link and try again")
                raise FileNotFoundError
            if self.deckChoice == "Target Deck" or self.noteChoice == "Note Type" or self.fieldChoice == "Field":
                showCritical("Enter deck options")
                raise FileNotFoundError
            if self.trans:
                if self.deckChoice2 == "Target Deck":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.noteChoice2 == 'Note Type':
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.fieldChoice2 == "Field":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.langChoice == "Language To Translate To":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
            if config["UseRange"]== "True" and config["LangLearning"] in spacedLangs:
                showCritical("Language not supported for use range")
                raise FileNotFoundError
            start = time.perf_counter()
            run(self.link,
                    self.numcards,
                    self.trans,
                    self.langChoice,
                    self.inclTitle,
                    self.delEng,
                    config["UseRange"],
                    config["MinWords"],
                    config["MaxWords"],
                    self.deckChoice,
                    self.noteChoice,
                    self.fieldChoice,
                    self.tubeType,
                    self.fieldChoice2,
                    config["OutFile"])
        except FileNotFoundError:
            pass
        except:
            showCritical("Looks like something went wrong. \nCheck your API key and try again")
        else:
            stop = time.perf_counter()
            diff = stop - start
            res = f"Generated all cards in {str(diff)} seconds"
            showCritical(res,"info")
    def filePicker(self):

        filename = QtWidgets.QFileDialog.getOpenFileName(None,None,None,"Text files (*.txt)")
        config["OutFile"] = filename[0]

    def save_pref(self):
        config["API KEY"] = self.lineEdit.text()
        config["LangLearning"] = self.learnLang.currentText()
        if self.checkBox.isChecked():
            config["MinWords"] = self.spinBox.value()
            config["MaxWords"] = self.spinBox_2.value()
            config["UseRange"] = str(self.checkBox.isChecked())
        else:
            config["MinWords"] = 0
            config["MaxWords"] = 0
            config["UseRange"] = str(False)
        with open(r"config.json","w",encoding="utf-8") as a:
            json.dump(config, a)
    def transBoolWeb(self,state):
        if state == QtCore.Qt.Checked:
            self.comboBox_20.setEnabled(True)
            self.comboBox_21.setEnabled(True)
            self.comboBox_22.setEnabled(True)
            self.comboBox_23.setEnabled(True)
    def transBoolBook(self,state):
        if state == QtCore.Qt.Checked:
            self.comboBox_13.setEnabled(True)
            self.comboBox_14.setEnabled(True)
            self.comboBox_15.setEnabled(True)
            self.comboBox_16.setEnabled(True)
    def webpress(self):
        self.deckChoice = self.comboBox_17.currentText()
        self.noteChoice = self.comboBox_18.currentText()
        self.fieldChoice = self.comboBox_19.currentText()
        self.deckChoice2 = self.comboBox_21.currentText()
        self.noteChoice2 = self.comboBox_22.currentText()
        self.fieldChoice2 = self.comboBox_23.currentText()
        self.langChoice = self.comboBox_20.currentText()
        self.numcards = self.spinBox_7.value()
        self.link = self.URLBox.text()
        self.trans = self.checkBox_8.isChecked()

        try:
            if self.deckChoice == "Target Deck" or self.noteChoice == "Note Type" or self.fieldChoice == "Field":
                showCritical("Enter deck options")
                raise FileNotFoundError
            if self.trans:
                if self.deckChoice2 == "Target Deck":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.noteChoice2 == 'Note Type':
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.fieldChoice2 == "Field":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.langChoice == "Language To Translate To":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
            if not config["LangLearning"]:
                showCritical("Enter the language that you're learning in settings")
                raise FileNotFoundError
            if config["UseRange"]== "True" and config["LangLearning"] in spacedLangs:
                showCritical("Language not supported for use range option")
                raise FileNotFoundError
            if config["LangLearning"] not in allsupported:
                showCritical("This operation is not supported for the language you are learning.\n Try the Youtube version instead.")
                raise FileNotFoundError
            start = time.perf_counter()
            TextExtract.run(self.numcards,
                    config["LangLearning"],
                    self.trans,
                    self.langChoice,
                    config["UseRange"],
                    config["MinWords"],
                    config["MaxWords"],
                    self.deckChoice,
                    self.noteChoice,
                    self.fieldChoice,
                    "Website",
                    self.fieldChoice2,
                    "",
                    self.link,
                    config["OutFile"])
        except FileNotFoundError:
            pass
        except:
            showCritical("Looks like something went wrong.")
        else:
            stop = time.perf_counter()
            diff = stop - start
            res = f"Generated all cards in {str(diff)} seconds"
            showCritical(res,"info")

    def pressBook(self):
        self.deckChoice = self.comboBox_10.currentText()
        self.noteChoice = self.comboBox_11.currentText()
        self.fieldChoice = self.comboBox_12.currentText()
        self.deckChoice2 = self.comboBox_14.currentText()
        self.noteChoice2 = self.comboBox_15.currentText()
        self.fieldChoice2 = self.comboBox_16.currentText()
        self.langChoice = self.comboBox_13.currentText()
        self.numcards = self.spinBox_5.value()
        self.files = [str(self.tableFiles.item(i).text()) for i in range(self.tableFiles.count())]
        self.trans = self.checkBox_5.isChecked()
        try:
            if self.deckChoice == "Target Deck" or self.noteChoice == "Note Type" or self.fieldChoice == "Field":
                showCritical("Enter deck options")
                raise FileNotFoundError
            if self.trans:
                if self.deckChoice2 == "Target Deck":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.noteChoice2 == 'Note Type':
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.fieldChoice2 == "Field":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
                if self.langChoice == "Language To Translate To":
                    showCritical("Enter deck info for translations")
                    raise FileNotFoundError
            if not config["LangLearning"]:
                showCritical("Enter the language you're learning in settings")
                raise FileNotFoundError
            if config["UseRange"] == "True" and config["LangLearning"] in spacedLangs:
                showCritical("Language not supported for use range option")
                raise FileNotFoundError
            if config["LangLearning"] not in allsupported:
                showCritical("This operation is not supported for the language you are learning.\n Try the Youtube version instead.")
                raise FileNotFoundError
            start = time.perf_counter()
            TextExtract.run(self.numcards,
                    config["LangLearning"],
                    self.trans,
                    self.langChoice,
                    config["UseRange"],
                    config["MinWords"],
                    config["MaxWords"],
                    self.deckChoice,
                    self.noteChoice,
                    self.fieldChoice,
                    "Book",
                    self.fieldChoice2,
                    self.files,
                    "",
                    config["OutFile"])
        except FileNotFoundError:
            pass
        except:
            showCritical("Looks like something went wrong.")
        else:
            stop = time.perf_counter()
            diff = stop - start
            res = f"Generated all cards in {str(diff)} seconds"
            showInfo(res)



    def deleteItem(self):
        listItems = self.tableFiles.selectedItems()
        if not listItems:
            self.tableFiles.setCurrentItem(self.tableFiles.item(0))
            if self.tableFiles.count() > 0:
                self.deleteItem()
        for item in listItems:
            self.tableFiles.takeItem(self.tableFiles.row(item))

    def clearList(self):
        self.tableFiles.setCurrentItem(self.tableFiles.item(0))
        for i in range(self.tableFiles.count()):
            self.tableFiles.clear()
    def check_web_link(self,link):
        try:
            res = requests.get(link)
        except:
            return False
        else:
            return True

def run_now():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())



