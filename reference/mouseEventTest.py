# coding:utf-8

from PySide import QtCore, QtGui


class MyButtons(QtGui.QPushButton):
    
    def __init__(self, parent = None):
        super(MyButtons, self).__init__(parent)
    
    def enterEvent(self, event):
        print "Enter"
    
    def leaveEvent(self, event):
        print "Leave"
        
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            print "MRB Clicked"
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print "MLB Clicked"
    
    def wheelEvent(self, event):
        print "Wheeling"

def main():
    app = QtGui.QApplication([])
    testButton = MyButtons()
    testButton.show()
    app.exec_()
    
main()