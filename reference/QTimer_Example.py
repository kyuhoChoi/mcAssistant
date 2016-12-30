# coding:utf-8

from PySide import QtGui, QtCore
import sys

class myLCDNumber(QtGui.QLCDNumber):
    value = 60
    
    @QtCore.Slot()
    def count(self):
        self.display(self.value)
        self.value = self.value-1
    
    
def main():    
    app      = QtGui.QApplication(sys.argv)
    lcdNumber     = myLCDNumber()
    
    #Resize width and height
    lcdNumber.resize(250,250)    
    lcdNumber.display(60)
    timer = QtCore.QTimer()
    timer.timeout.connect(lcdNumber.count)
    timer.start(41) 
    
    lcdNumber.show()    
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()