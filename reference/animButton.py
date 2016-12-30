# coding:utf-8

import os
from PySide import QtGui, QtCore

class RepeatTimer(QtCore.QTimer):
    '''
    @brief :This class implements a timer which can be kicked of a fixed number if times
    This timer is a subClass of QTimer and implements the ability to make the timer go off
    for a fixed number of times defined by the user, rather the infinite times or 1 time.
    '''
    ## Public signal emit when the timeout signal is emitted as well but passing the iteration index
    timeoutCount = QtCore.Signal(int)
    ## Public signal which get fired at the end of all iterations
    endRepeat = QtCore.Signal()
    
    def __init__(self, numberOfRepeats = 1, delay = 10):
        '''
        The constructor
        @param numberOfRepeats: how many times to trigger the timer
        @param delay: every how many millisec to fire off the timer
        '''
        super(RepeatTimer, self).__init__()
        
        self.__numberOfRepeats = 1
        self.__delay = 10
        self.numberOfRepeats = numberOfRepeats
        self.delay = delay
        self.__internalCounter = 0
        
        self.timeout.connect(self.__eval)

    @property
    def delay(self):
        return self.__delay
    
    @delay.setter
    def delay(self, value):
        if value >= 0 and type(value).__name__ == "int":
            self.__delay = value
            self.setInterval(value)
    
    @property
    def numberOfRepeats(self):
        return self.__numberOfRepeats
    
    @numberOfRepeats.setter
    def numberOfRepeats(self, value):
        if value >=0 and type(value).__name__ == "int":
            self.__numberOfRepeats = value
        
    def __eval(self):
        '''
        This procedure checks if the timer did all the iteration, if so it stops it and resets it
        '''
        if self.__internalCounter >= self.__numberOfRepeats-1:
            self.stop()
            self.endRepeat.emit()
            self.timeoutCount.emit(self.__internalCounter)
            self.__internalCounter = 0
        else:
            self.timeoutCount.emit(self.__internalCounter)
            self.__internalCounter += 1
        
        
class AnimButton(QtGui.QPushButton):
    
    def __init__(self, parent = None):
        super(AnimButton, self).__init__(parent)
        
        ## The frames used for the anim
        self.__frames         = None
        ## The folder of the frames
        self.__basePath       = None
        ## The paths of the framse
        self.__framesPath     = None
        ## The size of the frames , it's automatically extracted from the first frame
        self.__frameSize      = None
        ## How many frames in the anim
        self.__numberOfFrames = None
        ## The internal timer for the swap of the frames
        self._timer           = RepeatTimer(10, 100)
        
        self.clicked.connect(self.playAnim)
        self._timer.timeoutCount.connect(self._setFrame)
    
    def setFrames(self, basePath = None, frames = [], resizeButton = True, speed = 41):
        '''
        This procedure lets you store in the class a series of frames, the get cached during
        the process so they don't get re from the folder everytime
        @param basePath: str, the folder of the frames
        @param frames: str[], all the path of the frames
        @param resizeButton: bool, where or not to resize the button to match the size of the frames
        @param speed: int, how long each frame lasts in millisec
        '''
        self.__frames = self._convertFrame(basePath, frames, resizeButton, speed)
        self._setFrame(0)
        
    def _convertFrame(self, basePath, frames = [], resizeButton = True, speed = 41):
        '''
        This procedure reads the frame from disk and converts them ready to be used
        Should not be used by the end user
        @param basePath: str, the folder of the frames
        @param frames: str[], all the path of the frames
        @param resizeButton: bool, where or not to resize the button to match the size of the frames
        @param speed: int, how long each frame lasts in millisec
        @return : QIcons[]
        '''
        
        processed = []
        
        # Lest loop the frames
        for i,f in enumerate(frames):
            # Convert the frame to pix map
            pix = QtGui.QPixmap(os.path.join(basePath,f))
            # If it is the first frame lets extract the size
            if i == 0:
                self.__frameSize = pix.size()
            # Convert to QIcon
            im = QtGui.QIcon(pix)
            processed.append(im)
        
        # Let's store some parameters
        self.__numberOfFrames = len(processed)
        self.__basePath       = basePath
        self.__framespath     = frames
        
        # Let's set the kick off of the timer based on the number of frames
        self._timer.numberOfRepeats = self.__numberOfFrames
        # Set the delay of the timer
        self._timer.delay = speed
        
        # If requested fits the button size to the frame's
        if resizeButton:
            self.setGeometry(100,100, self.__frameSize.width(), self.__frameSize.height())
        
        return processed
    
    def _setFrame(self, index = 0):
        '''
        This procedure sets which frame is visible
        Should not be used by the end user
        @param index : int, the index of the frame to display
        '''
        if (self.__frames and self.__frameSize and index <= (self.__numberOfFrames-1)):
            self.setIcon(self.__frames[index])
            self.setIconSize(self.__frameSize)
    
    def _setFrameData(self, data):
        self.__frames = data
            
    def playAnim(self):
        '''
        This procedure kicks of the anim if the button
        '''
        self._timer.start()
        
        
class AnimButtonOnOff(AnimButton):
    '''
    @brief Animation push button with up and down anim
    This class extend the AnimButton with tow difference sets of frame to use when the button is pressed,
    when button is pressed down the frames used internally are swapped , so we can have two animations,
    one when the button is pressed down one when the button is pressed up 
    '''
    def __init__(self, parent = None):
        super(AnimButtonOnOff, self).__init__(parent)
        
        ## The check for the press down frames
        self.__downFrames = None
        ## The check for the press up frames
        self.__upFrames = None
        ## Internal state of the button
        self.__toggle = False
        
        # Make needed connections
        self._timer.endRepeat.connect(self.__swap)
        
    def setDownFrames(self, basePath = None, frames = [], resizeButton = False, speed = 41):
        '''
        This procedure read the push down frames
        the process so they don't get re from the folder everytime
        @param basePath: str, the folder of the frames
        @param frames: str[], all the path of the frames
        @param resizeButton: bool, where or not to resize the button to match the size of the frames
        @param speed: int, how long each frame lasts in millisec
        '''
        self.__downFrames = self._convertFrame( basePath, frames, resizeButton, speed )
        self.__initFrames()
        self._setFrame(0)
        
    def setUpFrames(self, basePath = None, frames = [], resizeButton = False, speed = 41):
        '''
        This procedure read the push up frames
        the process so they don't get re from the folder everytime
        @param basePath: str, the folder of the frames
        @param frames: str[], all the path of the frames
        @param resizeButton: bool, where or not to resize the button to match the size of the frames
        @param speed: int, how long each frame lasts in millisec
        '''
        self.__upFrames = self._convertFrame( basePath, frames, resizeButton, speed )
        self.__initFrames()
        self._setFrame(0)
        
    def __initFrames(self):
        '''
        This procedure swaps the pointer to the corredt frames
        '''
        if self.__toggle == False:
            self._setFrameData(self.__downFrames)
            #self.__frames = self.__downFrames
        else:
            self._setFrameData(self.__upFrames)
    
    def __swap(self):
        '''
        This procedure change the toggle status and swaps the frames
        '''
        if not self.__toggle:
            self.__toggle = True
        else:
            self.__toggle = False
        
        self.__initFrames()
            
        
    
    
def main():
    app  = QtGui.QApplication([])
    #temp = AnimButton()
    temp = AnimButtonOnOff()
    
    basePath = 'images'
    frames = os.listdir(basePath)
    
    #temp.setFrames(basePath, frames)
    temp.setDownFrames(basePath, frames)
    temp.setUpFrames(basePath, reversed(frames))
    
    temp.show()
    app.exec_()
    
main()