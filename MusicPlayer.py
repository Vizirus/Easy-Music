from PyQt5 import QtWidgets, uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl
from mutagen.mp3 import MP3
import os
class Main():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.desin = uic.loadUi("Desine.ui")
        self.desin2 = uic.loadUi("Seccond.ui")
        self.desin3 = uic.loadUi("saveAlbums.ui")
        self.desin.show()
        self.songs = os.listdir(path="Songs\\")
        for i in self.songs:
            self.desin.comboBox_2.addItem(i)
            self.desin2.comboBox.addItem(i)
        self.albums = {}
        self.media_player = QMediaPlayer()
        self.desin.dial.valueChanged.connect(mainFunctions.set_Volume)
        self.desin.horizontalSlider.sliderMoved.connect(mainFunctions.getHeight)
        self.desin.pushButton_4.clicked.connect(mainFunctions.playSong)
        self.desin.pushButton_6.clicked.connect(mainFunctions.pause)
        self.desin.pushButton_7.clicked.connect(playListWorker.openScreen)
        self.desin2.pushButton.clicked.connect(playListWorker.addFromFolder)
        self.desin.pushButton_8.clicked.connect(playListWorker.playPlayList)
        self.desin2.pushButton_3.clicked.connect(playListWorker.creatAlbum)
        self.desin2.pushButton_4.clicked.connect(playListWorker.close)
        self.desin.horizontalSlider.sliderReleased.connect(mainFunctions.released)
        self.media_player.positionChanged.connect(playListWorker.positionChange)
        self.desin2.pushButton_5.clicked.connect(playListWorker.deleteMedia)
        self.desin2.comboBox_2.currentTextChanged.connect(playListWorker.appendSongs)
        self.desin2.pushButton_6.clicked.connect(playListWorker.saveAlbum)
        self.desin.comboBox.currentTextChanged.connect(playListWorker.changeAlbums)
        self.desin.action.triggered.connect(saveWorker.openSaveInterface)
        self.desin.action_2.triggered.connect(saveWorker.openFile)
        self.desin3.pushButton.clicked.connect(saveWorker.saveAlbums)

class mainFunctions(Main): 
    def playSong():
        m.sng = "Songs\\" + m.desin.comboBox_2.currentText()
        m.url = QMediaContent(QUrl.fromLocalFile(m.sng))
        m.media_player.setMedia(m.url)
        m.media_player.play()
        m.desin.horizontalSlider.setMaximum(int(MP3(m.sng).info.length * 1000))
        m.desin.label_5.setText(str(int(MP3(m.sng).info.length / 60)))


    def getHeight():
        m.media_player.blockSignals(True)
        m.media_player.setPosition(m.desin.horizontalSlider.value())
    
    def released():
        m.media_player.blockSignals(False)

    def set_Volume():
        m.media_player.setVolume(m.desin.dial.value())


    def pause():
        def unpause(): 
            m.desin.pushButton_6.setText("Пауза")
            m.desin.pushButton_6.clicked.connect(mainFunctions.pause)
            m.media_player.play()

        m.media_player.pause()
        m.desin.pushButton_6.setText("Продолжить")
        m.desin.pushButton_6.clicked.connect(unpause)

    

class playListWorker(Main):
    def openScreen():
        m.desin2.show()


    def creatAlbum():
        m.albums[m.desin2.lineEdit.text()] = QMediaPlaylist()
        m.desin2.comboBox_2.addItem(m.desin2.lineEdit.text())


    def addFromFolder():
        media = "Songs\\" + m.desin2.comboBox.currentText()
        m.albums[m.desin2.comboBox_2.currentText()].addMedia(QMediaContent(QUrl.fromLocalFile(media)))
        m.desin2.listWidget.addItem(m.desin2.comboBox.currentText())

    def close():
        m.desin2.close()

    def saveAlbum():
        m.desin.comboBox_4.clear()
        m.desin.comboBox_4.addItem("По очереди")
        m.desin.comboBox.blockSignals(True)
        m.desin.comboBox.addItem(m.desin2.comboBox_2.currentText())
        for i in range(m.albums[m.desin2.comboBox_2.currentText()].mediaCount()):
            m.desin.comboBox_4.addItem(m.albums[m.desin2.comboBox_2.currentText()].media(i).canonicalUrl().fileName())
        m.desin.comboBox.blockSignals(False)

    def songChanged(media):
        print(media)
        if not media.isNull():
            global value
            url = "Songs\\" + media.canonicalUrl().fileName()
            value = int(MP3(url).info.length * 1000)
            m.desin.horizontalSlider.setSliderPosition(0)
            m.desin.horizontalSlider.setMaximum(int(MP3(url).info.length * 1000))
            m.desin.label_5.setText(str(int(MP3(url).info.length / 60)))


    def playPlayList():
        m.albums[m.desin.comboBox.currentText()].currentMediaChanged.connect(playListWorker.songChanged)
    
        if m.desin.comboBox_4.currentText() == "По очереди":
            m.media_player.setPlaylist(m.albums[m.desin.comboBox.currentText()])
            m.media_player.play()
        else:
            m.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("Songs\\" + m.desin.comboBox_4.currentText())))
            m.desin.horizontalSlider.setMaximum(int(MP3("Songs\\" + m.desin.comboBox_4.currentText()).info.length * 1000))
            m.desin.label_5.setText(str(int(MP3("Songs\\" + m.desin.comboBox_4.currentText()).info.length / 60)))
            m.media_player.play()

    def positionChange(position):
        m.desin.horizontalSlider.setSliderPosition(position)

    def deleteMedia():
        m.albums[m.desin2.comboBox_2.currentText()].removeMedia(m.desin2.listWidget.currentRow())
        m.desin2.listWidget.takeItem(m.desin2.listWidget.currentRow())

    def appendSongs():
        m.desin2.listWidget.clear()
        for i in range(m.albums[m.desin2.comboBox_2.currentText()].mediaCount()):
            m.desin2.listWidget.addItem(m.albums[m.desin2.comboBox_2.currentText()].media(i).canonicalUrl().fileName())

    def changeAlbums():
        m.desin.comboBox_4.clear()
        m.desin.comboBox_4.addItem("По очереди")
        for i in range(m.albums[m.desin.comboBox.currentText()].mediaCount()):
            m.desin.comboBox_4.addItem(m.albums[m.desin.comboBox.currentText()].media(i).canonicalUrl().fileName())

class saveWorker(Main):
    def openSaveInterface():
        m.desin3.comboBox.addItems(m.albums)
        m.desin3.show()

    def saveAlbums():
        file = QtWidgets.QFileDialog.getSaveFileName(m.desin, "Сохранение альбома", "./", "Текст (*.txt)")
        save = open(file[0], "w")
        save.write(m.desin3.comboBox.currentText())
        for i in range(m.albums[m.desin2.comboBox_2.currentText()].mediaCount()):
            save.write("," + m.albums[m.desin2.comboBox_2.currentText()].media(i).canonicalUrl().fileName())
        save.close()

    def openFile():
        fileName = QtWidgets.QFileDialog.getOpenFileName(m.desin, "Save file name", "./", "Text (*.txt)")
        file = open(fileName[0], "r")
        line = file.read().split(",")
        m.albums[line[0]] = QMediaPlaylist()
        for i in range(1, len(line)):
            m.albums[line[0]].addMedia(QMediaContent(QUrl.fromLocalFile("Songs\\" + str(line[i]))))
        m.desin.comboBox.addItem(line[0])
        file.close()

m = Main()
m.app.exec()