import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
import random, time
from pygame import mixer
from mutagen.mp3 import MP3 # will help to find the length of the song
import style

musicList = []
mixer.init() 
muted = False
counter = 0
songLength = 0
index = 0


class Player(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Player')
        self.setGeometry(450,150,480,700)
        self.setStyleSheet(style.mainWindowBG())
        self.UI()
        self.show()

    
    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # ProgressBar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False) # To remove % symbol on the progressbar
        self.progressBar.setStyleSheet(style.progressBarStyle())

        # Song Length Labels
        self.songTimerLabel = QLabel('0:00')
        self.songTimerLabel.setStyleSheet(style.LabelStyle())
        self.songLengthLabel = QLabel('/ 0:00')
        self.songLengthLabel.setStyleSheet(style.LabelStyle())

        # Buttons
        self.addButton = QToolButton()
        self.addButton.setIcon(QIcon('icons\\add.png'))
        self.addButton.setIconSize(QSize(48,48)) # x and y Values
        self.addButton.setToolTip('Add a song')
        self.addButton.clicked.connect(self.addSongs)
        self.addButton.setStyleSheet(style.playStyle())

        self.shuffleButton = QToolButton()
        self.shuffleButton.setIcon(QIcon('icons\\shuffle.png'))
        self.shuffleButton.setIconSize(QSize(48,48)) # x and y Values
        self.shuffleButton.setToolTip('Shuffle songs')
        self.shuffleButton.clicked.connect(self.shufflePlayList)
        self.shuffleButton.setStyleSheet(style.playStyle())

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon('icons\\previous.png'))
        self.previousButton.setIconSize(QSize(48,48)) # x and y Values
        self.previousButton.setToolTip('Previous song')
        self.previousButton.clicked.connect(self.playPrevious)
        self.previousButton.setStyleSheet(style.playStyle())

        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon('icons\\play.png'))
        self.playButton.setIconSize(QSize(64,64)) # x and y Values
        self.playButton.setToolTip('Play')
        self.playButton.clicked.connect(self.playSong)
        self.playButton.setStyleSheet(style.playStyle())

        self.nextButton = QToolButton()
        self.nextButton.setIcon(QIcon('icons\\next.png'))
        self.nextButton.setIconSize(QSize(48,48)) # x and y Values
        self.nextButton.setToolTip('Next song')
        self.nextButton.clicked.connect(self.playNext)
        self.nextButton.setStyleSheet(style.playStyle())

        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon('icons\\mute.png'))
        self.muteButton.setIconSize(QSize(48,48)) # x and y Values
        self.muteButton.setToolTip('Mute')
        self.muteButton.clicked.connect(self.muteSong)
        self.muteButton.setStyleSheet(style.playStyle())

        # Volume Slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setToolTip('Volume')
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)
        self.volumeSlider.setStyleSheet(style.sliderStyle())

        # Play List
        self.playList = QListWidget()
        self.playList.doubleClicked.connect(self.playSong)
        self.playList.setStyleSheet(style.playListStyle())

        # Timer for Progress BAr
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgressBar)

    def layouts(self):
        # Creating Layouts
        self.mainLayout = QVBoxLayout()
        self.topMainLayout = QVBoxLayout()
        self.topGroupBox = QGroupBox()
        #self.topGroupBox = QGroupBox('Music Player')
        self.topGroupBox.setStyleSheet(style.groupboxStyle())
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        # Adding Widgets



        # Top Layout Widgets
        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLengthLabel)

        # Middle Layout Widgets
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.nextButton)
        self.middleLayout.addWidget(self.volumeSlider)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addStretch()
        
        # Bottom Layout Widgets
        self.bottomLayout.addWidget(self.playList)

        self.topMainLayout.addLayout(self.topLayout)
        self.topMainLayout.addLayout(self.middleLayout)
        self.topGroupBox.setLayout(self.topMainLayout)
        self.mainLayout.addWidget(self.topGroupBox,25)
        self.mainLayout.addLayout(self.bottomLayout,75)
        self.setLayout(self.mainLayout)


    def addSongs(self):
        directory = QFileDialog.getOpenFileName(self, 'Add Song', ' ', 'Songs Files (*.mp3 *.ogg *.wav)')
        filename = os.path.basename(directory[0]) # it will take only the song name.mp3 
        self.playList.addItem(filename)
        musicList.append(directory[0])

    def shufflePlayList(self):
        random.shuffle(musicList)
        self.playList.clear() # First we will delete the list and then add the shuffle list
        for song in musicList:
            filename = os.path.basename(song)
            self.playList.addItem(filename)

    def playSong(self):
        global songLength
        global counter
        global index
        counter = 0
        index = self.playList.currentRow()
        #print(index)
        #print(musicList[index])
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            songLength = sound.info.length
            songLength = round(songLength) # to remove the decimal numbers 212.13213
            print(songLength)
            min, sec = divmod(songLength, 60) # Song length for minutes and seconds 0:00
            self.songLengthLabel.setText('/ ' + str (min) + ':' + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)
        except:
            pass

    def playPrevious(self):
        global songLength
        global counter
        global index
        counter = 0
        items = self.playList.count()
        if index == 0:
            index = items
        index -= 1
        #print(index)
        #print(musicList[index])
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            songLength = sound.info.length
            songLength = round(songLength) # to remove the decimal numbers 212.13213
            print(songLength)
            min, sec = divmod(songLength, 60) # Song length for minutes and seconds 0:00
            self.songLengthLabel.setText('/ ' + str (min) + ':' + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)
        except:
            pass

    def playNext(self):
        global songLength
        global counter
        global index
        counter = 0
        items = self.playList.count()
        index += 1
        if index == items:
            index = 0
        
        #print(index)
        #print(musicList[index])
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            songLength = sound.info.length
            songLength = round(songLength) # to remove the decimal numbers 212.13213
            print(songLength)
            min, sec = divmod(songLength, 60) # Song length for minutes and seconds 0:00
            self.songLengthLabel.setText('/ ' + str (min) + ':' + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)
        except:
            pass

    def setVolume(self):
        self.volume = self.volumeSlider.value()
        #print(self.volume)
        self.muteButton.setIcon(QIcon('icons/unmuted.png'))
        if self.volume == 0:
            mixer.music.set_volume(0)
            self.muteButton.setIcon(QIcon('icons/mute.png'))
        elif self.volume >= 1:
            mixer.music.set_volume(self.volume/100)
            self.muteButton.setIcon(QIcon('icons/unmuted.png'))
        #mixer.music.set_volume(self.volume/100) # mixer use values from 0 to 1 thats why we divided it by 100


    def muteSong(self):
        global muted

        if muted == False:
            mixer.music.set_volume(0.0)
            muted = True
            self.muteButton.setToolTip('UnMuted')
            self.muteButton.setIcon(QIcon('icons/unmuted.png'))
            self.volumeSlider.setValue(0)
        else:
            mixer.music.set_volume(1.0)
            muted = False
            self.muteButton.setToolTip('Mute')
            self.muteButton.setIcon(QIcon('icons/mute.png'))
            self.volumeSlider.setValue(100)

    def updateProgressBar(self):
        global counter
        global songLength
        counter += 1
        self.progressBar.setValue(counter)
        self.songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(counter)))
        if counter == songLength:
            self.timer.stop()

    
def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()