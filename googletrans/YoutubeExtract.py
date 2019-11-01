

from PyQt5 import QtCore, QtGui, QtWidgets
from . import Translations
from . import Youtube
from aqt.utils import *
from aqt import mw
import re

class Ui_Dialog(QtWidgets.QDialog):

    def setupUi(self, Dialog,link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field,type, field2,
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

        self.threadClass = ThreadClass(link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field,type, field2,
                     file)
        try:
            self.threadClass.start()
        except:
            self.close()
        self.threadClass.updateNum.connect(self.updateProgress)




    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Adding cards"))
        self.label.setText(_translate("Adding cards", "Generating"))

    def updateProgress(self,val):

        self.progressBar.setValue(val)


class ThreadClass(QtCore.QThread):
    updateNum = QtCore.pyqtSignal(int)


    def __init__(self,link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field,type, field2=None,
                     file=None,parent=None):
        super(ThreadClass,self).__init__(parent)
        self.link = link
        self.limit = limit
        self.trans = trans
        self.lang = lang
        self.title = title
        self.delEng = delEng
        self.useRange = useRange
        self.min = min
        self.max = max
        self.deck = deck
        self.note = note
        self.field = field
        self.type = type
        self.field2 = field2
        self.file = file

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

    def generate_vid(self,link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field, field2=None,
                     file=None):
        try:
            vid = Youtube.YoutubeVideo(link)
        except:
            showCritical("Wrong Link")

        i = 1
        for comment in vid.gen_comm():
            if i == limit + 1:
                break
            if useRange == "True":
                if not self.isRange(min, max, comment):
                    continue
            if delEng:
                if Translations.isEng(comment):
                    continue
            if trans:
                translated = Translations.translate(comment, lang)
                self.add_to_deck(deck, note, field, comment, field2, translated)
            else:
                self.add_to_deck(deck, note, field, comment)
            if file:
                try:
                    self.addToFile(comment, file)
                except:
                    pass

            i += 1
            percent = (i / limit) * 100
            self.updateNum.emit(percent)

        if i < limit:

            if title:
                vidtitle = vid.title
                if useRange:
                    if not self.isRange(min, max, vidtitle):
                        pass
                if delEng:
                    if Translations.isEng(vidtitle):
                        pass
                if trans:
                    translate = Translations.translate(vidtitle, lang)
                    self.add_to_deck(deck, note, field, vidtitle, field2, translate)

                else:
                    self.add_to_deck(deck, note, field, vidtitle)
                if file:
                    try:
                        self.addToFile(vidtitle, file)
                    except:
                        pass
                i += 1
                percent = (i / limit) * 100
                self.updateNum.emit(percent)


        self.updateNum.emit(100)
    def generate_channel(self,link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field, field2=None,
                         file=None):

        channel = Youtube.YoutubeChannel(link)
        count = 1
        for video in channel.all_videos:
            try:
                vid = Youtube.YoutubeVideo("https://www.youtube.com/watch?v=" + video)
            except:
                continue
            vidtitle = vid.title
            for comment in vid.gen_comm():
                if count == limit + 1:
                    break
                if useRange == "True":
                    if not self.isRange(min, max, comment):
                        continue
                if delEng:
                    if Translations.isEng(comment):
                        continue
                if trans:
                    translated = Translations.translate(comment, lang)
                    self.add_to_deck(deck, note, field, comment, field2, translated)
                else:
                    self.add_to_deck(deck, note, field, comment)
                if file:
                    try:
                        self.addToFile(comment, file)
                    except:
                        pass
                count += 1
                percent = (count / limit) * 100
                self.updateNum.emit(percent)
            if count < limit:
                if title:
                    if useRange:
                        if not self.isRange(min, max, vidtitle):
                            pass
                    if delEng:
                        if Translations.isEng(vidtitle):
                            pass

                    if trans:
                        translate = Translations.translate(title, lang)
                        self.add_to_deck(deck, note, field, vidtitle, field2, translate)
                    else:
                        self.add_to_deck(deck, note, field, vidtitle)
                    if file:
                        try:
                            self.addToFile(vidtitle, file)
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

    def generate_playlist(self,link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field, field2=None,
                          file=None):
        playlist = Youtube.YoutubePlaylist(link)
        count = 1
        for video in playlist.playlist_vids:
            try:
                vid = Youtube.YoutubeVideo("https://www.youtube.com/watch?v=" + video)
            except:
                continue
            vidtitle = vid.title
            for comment in vid.gen_comm():
                if count == limit + 1:
                    break
                if useRange == "True":
                    if not self.isRange(min, max, comment):
                        continue
                if delEng:
                    if Translations.isEng(comment):
                        continue

                if trans:
                    translated = Translations.translate(comment, lang)
                    self.add_to_deck(deck, note, field, comment, field2, translated)
                else:
                    self.add_to_deck(deck, note, field, comment)
                if file:
                    try:
                        self.addToFile(comment, file)
                    except:
                        pass
                count += 1
                percent = (count / limit) * 100
                self.updateNum.emit(percent)
            if count < limit:
                if title:
                    if useRange:
                        if not self.isRange(min, max, vidtitle):
                            pass
                    if delEng:
                        if Translations.isEng(vidtitle):
                            pass
                    if trans:
                        translate = Translations.translate(title, lang)
                        self.add_to_deck(deck, note, field, vidtitle, field2, translate)
                    else:
                        self.add_to_deck(deck, note, field, vidtitle)

                    if file:
                        try:
                            self.addToFile(vidtitle, file)
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

    def run(self):
        if self.type == "Video":
            try:
                self.generate_vid(self.link,self.limit,
                            self.trans,
                            self.lang,
                            self.title,
                            self.delEng ,
                            self.useRange,
                            self.min ,
                            self.max,
                            self.deck,
                            self.note ,
                            self.field,
                            self.field2 ,
                            self.file )
            except:
                showCritical("Wrong link")

        elif self.type == "Channel":
            self.generate_channel(self.link, self.limit,
                              self.trans,
                              self.lang,
                              self.title,
                              self.delEng,
                              self.useRange,
                              self.min,
                              self.max,
                              self.deck,
                              self.note,
                              self.field,
                              self.field2,
                              self.file)
        else:
            self.generate_playlist(self.link, self.limit,
                                  self.trans,
                                  self.lang,
                                  self.title,
                                  self.delEng,
                                  self.useRange,
                                  self.min,
                                  self.max,
                                  self.deck,
                                  self.note,
                                  self.field,
                                  self.field2,
                                  self.file)





def run(link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field,type, field2=None,
                     file=None):

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog,link, limit, trans, lang, title, delEng, useRange, min, max, deck, note, field,type, field2,
                     file)

    Dialog.exec_()





#
# run("https://www.youtube.com/watch?v=Bb5VfiFy0kY",
#                     10,
#                     False,
#                     "",
#                     False,
#                     False,
#                     False,
#                     0,
#                     0,
#                     "comments",
#                     "Basic",
#                     "Basic: Front",
#                     "Video",
#                     "",
#                     )




















