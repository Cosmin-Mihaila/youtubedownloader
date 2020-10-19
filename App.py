from PyQt5.QtWidgets import *
from pytube import YouTube
import os

class App():
    def __init__(self, parent=None):
        self.url = QLineEdit()
        self.url.setText("Enter video URL")

        self.downButton = QPushButton("Download")
        self.downButton.clicked.connect(self.onPushDownload)

        self.bar = QProgressBar()

        self.fname = QFileDialog()

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.onPushBrowse)

        self.path = os.getcwd()

        self.ys = None

        self.downTitle = QLabel()
        self.downTitle.setVisible(False)
        self.downTitle.adjustSize()

        self.savePath = QLabel("Save at " + self.path)
        self.savePath.adjustSize()

        # Add all widgets declared
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.url)
        self.layout.addWidget(self.savePath)
        self.layout.addWidget(self.downTitle)
        self.layout.addWidget(self.downButton)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.browseButton)

        self.browseButton.setGeometry(0,0,1,1)

        # Set the window and show it
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.window.setWindowTitle("YouTube Downloader")
        self.window.setFixedSize (500, 200)
        self.window.show()


    def onPushDownload(self):

        self.yt = YouTube( self.url.text())
        self.yt.register_on_progress_callback(self.progressFunc)
        self.yt.register_on_complete_callback(self.complete)

        # Here it can be modified to download any resolution we want
        self.ys = self.yt.streams.get_highest_resolution()

        # Show the title of downloading video
        self.downTitle.setText("Downloading " + self.ys.title)
        self.downTitle.setVisible(True)

        self.ys.download(self.path)

    def onPushBrowse(self):
        auxStr = self.fname.getExistingDirectory()

        # Verify if the user pressed "Cancel". If not, set the new path
        if len(auxStr) > 0 :
            self.path = auxStr

        self.savePath.setText("Save at " + self.path)

        # Function to show that the download has been completed
    def complete (self, file_path, last):
        self.downTitle.setVisible(False)
        QMessageBox().about(self.window, "Title", "COMPLETED")
        self.bar.reset()

        # Function that show the progress of download
    def progressFunc(self, stream, chunk, bytes_remaining):
        size = self.ys.filesize
        progress = (float(abs(bytes_remaining-size)/size))*float(100)
        self.bar.setValue( int(progress) )

app = QApplication([])
downloader = App()
app.exec_()
