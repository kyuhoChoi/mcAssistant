# coding:utf-8

from PySide import QtCore, QtGui
    
class ZeroSpinBox(QtGui.QSpinBox):
    atZero = QtCore.Signal(int)
    zeors = 0
    
    def __init__(self, parent = None):
        super(ZeroSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.checkzero)
    
    def checkzero(self):
        if self.value() == 0:
            self.zeors += 1
            self.atZero.emit(self.zeors)
        

class Form(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        
        dial = QtGui.QDial()
        dial.setNotchesVisible(True)
        zerospinbox = ZeroSpinBox()
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(zerospinbox)
        self.setLayout(layout)
        
        dial.valueChanged.connect(zerospinbox.setValue)
        zerospinbox.valueChanged.connect(dial.setValue)
        zerospinbox.atZero.connect(self.printZero)
        
    def printZero(self, zeros):
        print("zerospinbox has been at zero " + str(zeros) + " times.")

def main():
    app = QtGui.QApplication([])
    temp = Form()
    temp.show()
    app.exec_()
    
if __name__ == '__main__':
    main()