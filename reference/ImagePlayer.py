# coding:utf-8

from PySide import QtGui, QtCore

class ImagePlayer(QtGui.QWidget):
    def __init__(self, filename, title, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Load the file into a QMovie
        self.movie = QtGui.QMovie(filename, QtCore.QByteArray(), self)

        size = self.movie.scaledSize()
        self.setGeometry(200, 200, size.width(), size.height())
        self.setWindowTitle(title)

        self.movie_screen = QtGui.QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)

        # Create the layout
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        
        
if __name__ == "__main__":
    gif = "C:/Users/guenmo_kim/Desktop/bbb.gif"
    app = QtGui.QApplication([])
    player = ImagePlayer(gif, 'Test')
    player.show()
    app.exec_()