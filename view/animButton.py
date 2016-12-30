# coding:utf-8

import os
from PySide import QtGui, QtCore
import Control.motionCapture as mocap
reload(mocap)

class AnimButton(QtGui.QPushButton):
    
    def __init__(self, speed = 30, parent = None):
        super(AnimButton, self).__init__(parent)
        self.__operation = 'reference'
        self.__fileType  = 'hik'
        
        self.pad = 3
        self.minSize = 8
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        
        self.__index  = 0
        self.__speed  = speed
        
        self.__frames         = None # QIcons [] 
        self.__basePath       = None # 이미지 폴더 str
        self.__framesPath     = None # 이미지 이름들 []
        self.__frameSize      = None # 이미지 싸이즈 (with, height)
        self.__numberOfFrames = None # 이미지 개수 int
        
        self._timer = QtCore.QTimer()
        self._timer.setInterval(self.__speed)
        self._timer.timeout.connect(self.runAnim)
    
    def runAnim(self):
        self._setFrame(self.__index)
        self.__index +=1
        
    def setFrames(self, basePath = None, frames = []):
        '''
        모든 초기 값을 설정한다.
        
        @param basePath     : str, 폴더 경로
        @param frames       : str[], basePath 폴더 안에 이미지 시퀀스 리스트 
        @param resizeButton : boo, button의 크기 조절 가능 또는 불가능
        @param speed        : int, 애니메이션 속도 ( 41 == 1/24 )
        '''
        self.__frames = self._convertFrame(basePath, frames)
        self._setFrame(0)
        
    def _convertFrame(self, basePath = None, frames = []):
        '''
        해당 경로의 모든 이미지들을 QIcons으로 만들어 QIcons[]로 반환 한다.
        QIcons[]를 제외한 나머지 변수의 초기 값을 설정해 준다. 
        self.__basePath, self.__framesPath, self.__frameSize, self.__numberOfFrames, buttonSize, speed
        @param basePath     : str, 폴더 경로
        @param frames       : str[], basePath 폴더 안에 이미지 시퀀스 리스트 
        @param resizeButton : boo, button의 크기 조절 가능 또는 불가능
        @param speed        : int, 애니메이션 속도 ( 41 == 1/24 )
        @return : QIcons[]
        '''
        processed = [] # QIcons[]
        
        for i,f in enumerate(frames):
            pix = QtGui.QPixmap(os.path.join(basePath,f))
            if i == 0:
                if pix.size() != QtCore.QSize(0,0):
                    self.__frameSize = QtCore.QSize(50,50)
            im = QtGui.QIcon(pix)
            processed.append(im)
        
        self.__numberOfFrames = len(processed)
        self.__basePath       = basePath
        self.__framesPath     = frames
        
        return processed
    
    def _setFrame(self, index = 0):
        '''
        button의 보여질 이미지를 설정한다
        @param index: int, 보여질 이미지 인덱스
        '''
        if self.__frames and self.__frameSize :
            self.setIcon(self.__frames[index%self.__numberOfFrames])
            self.setIconSize(self.__frameSize)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            dirName = os.path.dirname(self.__basePath)
            fileName = self.__framesPath[0].partition('.')[0]
            
            folder = ''
            fileExt = ''
            if self.__fileType == 'hik':
                folder = 'hik'
                fileExt = 'mb'
            elif self.__fileType == 'ani':
                folder = 'clip'
                fileExt = 'ma'
            else:
                folder = ''
                fileExt = 'fbx'
                 
            targetFile = '{}.{}'.format(os.path.join(dirName.replace('preview', folder), fileName), fileExt)
            
            print u'{} 파일을 {} 합니다.'.format( targetFile, self.__operation)
            
            if self.__operation == 'open':
                mocap.openFile(targetFile)
            elif self.__operation == 'import':
                mocap.importFile(targetFile)
            elif self.__operation == 'reference':
                mocap.referenceFile(targetFile)
                
    
    def setOption(self, fileType, operation):
        self.__fileType = fileType
        self.__operation = operation
            
    def enterEvent(self, event):
        self._timer.start()

    def leaveEvent(self, event):
        self._timer.stop()
        self._setFrame(0)
        self.__index = 0
    
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        ## get default style
        opt = QtGui.QStyleOptionButton()
        self.initStyleOption(opt)
        ## scale icon to button size 
        Rect = opt.rect
        h = Rect.height()
        w = Rect.width()
        iconSize = max(min(h, w) - 2 * self.pad, self.minSize)
        opt.iconSize = QtCore.QSize(iconSize, iconSize)
        ## draw button
        self.style().drawControl(QtGui.QStyle.CE_PushButton, opt, qp, self)
        qp.end()
    
    def setSpeed(self, speed):
        self._timer.setInterval(speed) 
    
    def setSize(self, size):
        self.setFixedSize(size)
        
    def getPath(self):
        return self.__basePath

def main():
    app = QtGui.QApplication([])
    temp = AnimButton(24)
    basePath = "../reference/images"
    frames = os.listdir(basePath)

    temp.setFrames(basePath, frames)
    temp.show()
    
    temp.setSize(QtCore.QSize(100, 100))
    temp.setSpeed(10)
    app.exec_()
    
if __name__ == "__main__":
    main()
    