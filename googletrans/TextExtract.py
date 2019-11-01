

import nltk,os,re
from PyQt5 import QtCore, QtGui, QtWidgets
from aqt.utils import *
from . import BookText
from .BookText import get_text, web
from . import Translations
from aqt import mw


nltk.download('punkt')
os.environ["path"] = os.path.join(os.getcwd(),r"utils/poppler-0.68.0/bin")
class Ui_Dialog(QtWidgets.QDialog):

    def setupUi(self, Dialog,limit,lang, trans, translang,userange,min, max, deck, note, field,type, field2,files,link,
                     file):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 62)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.threadClass = ThreadClass2(limit,lang,trans,translang, userange,min, max, deck, note, field,type, field2,files,link,
                     file)

        self.threadClass.start()

        self.threadClass.updateNum.connect(self.updateProgress)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Adding cards"))
        self.label.setText(_translate("Adding cards", "Generating"))

    def updateProgress(self,val):

        self.progressBar.setValue(val)


class ThreadClass2(QtCore.QThread):
    updateNum = QtCore.pyqtSignal(int)


    def __init__(self,limit,lang, trans, translang,userange,min, max, deck, note, field,type, field2=None,files=None,link=None,
                     file=None,parent=None):
        super(ThreadClass2,self).__init__(parent)
        self.files = files
        self.limit = limit
        self.trans = trans
        self.lang = lang
        self.min = min
        self.max = max
        self.deck = deck
        self.note = note
        self.field = field
        self.type = type
        self.field2 = field2
        self.file = file
        self.translang = translang
        self.userange = userange
        self.link = link

    def isRange(self,min, max, sen):
        if Translations.check_lang(sen):
            if len(sen.split()) in range(min, max + 1):
                return True
            return False
        else:
            return False

    def addToFile(self,sen, file):
        with open(file, "a", encoding='utf-8') as w:
            w.write(sen + '\n')

    def add_to_deck(self,deck_name, note, field, sen, field2=None, sen2=None):
        myRe = re.compile(": (.*)")
        new_field = myRe.search(field).group(1)
        if field2:
            new_field2 = myRe.search(field2).group(1)

        deckId = mw.col.decks.id(deck_name)

        # todo Not sure why a simple 'select' doesnt do the model stuff for me...
        mw.col.decks.select(deckId)
        basic_model = mw.col.models.byName(note)
        basic_model['did'] = deckId
        mw.col.models.save(basic_model)
        mw.col.models.setCurrent(basic_model)

        senCard = mw.col.newNote()
        senCard[new_field] = sen
        if field2:
            senCard[new_field2] = sen2
        mw.col.addNote(senCard)
        mw.col.save()
        mw.col.close()

    def book_run(self,files, limit,lang, trans, translang,userange,min, max, deck, note, field,field2=None,
                     file=None):
        count = 1

        for i in files:
            text = get_text(i)
            if lang in BookText.supportedLangs:
                tokenizer = nltk.data.load(f'nltk:tokenizers/punkt/{lang}.pickle')
            elif lang in ["japanese","chinese (simplified)","chinese (traditional)"]:
                tokenizer = nltk.RegexpTokenizer(u'[^ 「」!?。．）]*[!?。]')
            for card in tokenizer.tokenize(text):
                card = card.replace(r"\r\n","")
                if count == limit + 1:
                    break
                if userange == "True":
                    if not self.isRange(min, max, card):
                        continue
                if trans:
                    translated = Translations.translate(card, translang)

                    self.add_to_deck(deck, note, field, card, field2, translated)
                else:
                    self.add_to_deck(deck, note, field, card)
                if file:
                    try:
                        self.addToFile(card, file)
                    except:
                        pass

                count += 1
                percent = (count / limit) * 100

                self.updateNum.emit(percent)
            if count < limit:
                continue
            else:
                break
        self.updateNum.emit(100)
    def webRun(self,link,limit,lang,trans,translang,userange,min,max,deck,note,field,field2=None,file=None):
        text = web(link)
        if lang in BookText.supportedLangs:
            tokenizer = nltk.data.load(f'nltk:tokenizers/punkt/{lang}.pickle')
        else:
            tokenizer = nltk.RegexpTokenizer(u'[^ 「」!?。．）]*[!?。]')
        count=1
        for i in tokenizer.tokenize(text):
            card = i.replace(r"\r\n", "")
            if count == limit + 1:
                break
            if userange == "True":
                if not self.isRange(min, max, card):
                    continue
            if trans:
                translated = Translations.translate(card, translang)
                self.add_to_deck(deck, note, field, card, field2, translated)
            else:
                self.add_to_deck(deck, note, field, card)
            if file:
                try:
                    self.addToFile(card, file)
                except:
                    pass

            count += 1
            percent = (count / limit) * 100
            self.updateNum.emit(percent)
        self.updateNum.emit(100)
    def run(self):
        if self.type == "Book":
            self.book_run(self.files,
                          self.limit,
                            self.lang,
                            self.trans,
                            self.translang,
                            self.userange,
                            self.min ,
                            self.max,
                            self.deck,
                            self.note ,
                            self.field,
                            self.field2 ,
                            self.file )

        elif self.type == "Website":
            self.webRun(self.link,
                        self.limit,
                        self.lang,
                        self.trans,
                        self.translang,
                        self.userange,
                        self.min,
                        self.max,
                        self.deck,
                        self.note,
                        self.field,
                        self.field2,
                        self.file
                        )




def run(limit,lang, trans, translang,userange, min, max, deck, note, field,type, field2=None,
                     files=None,link=None,file=None):

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog,limit,lang, trans, translang,userange, min, max, deck, note, field,type, field2,files,link,
                     file)
    Dialog.show()

    Dialog.exec_()




















