# coding:utf-8

from PySide import QtCore, QtGui
 
class PunchingBag(QtCore.QObject):
    ''' Represents a punching bag; when you punch it, it
        emits a signal that indicates that it was punched. '''
    punched = QtCore.Signal()
 
    def __init__(self):
        # Initialize the PunchingBag as a QObject
        QtCore.QObject.__init__(self)
 
    def punch(self):
        ''' Punch the bag '''
        self.punched.emit()
    
@QtCore.Slot()
def say_punched():
    print('Bag was punched.')
      
bag = PunchingBag()
bag.punched.connect(say_punched)

for i in range(10):
    bag.punch()