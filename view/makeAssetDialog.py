# coding:utf-8

from PySide import QtGui
import folderSearchWidget
reload(folderSearchWidget)
from folderSearchWidget import FolderSearchWidget
import os

class MakseAssetDailog(QtGui.QDialog):
    
    def __init__(self, callback=None, parent = None):
        super(MakseAssetDailog, self).__init__(parent)
        self.callback = callback
        
        
        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)
        
        text = u'''모션캡쳐 업체에서 받은 파일을 일괄적으로 처리합니다.
        
    1. 모션캡쳐 업체에서 받은 데이터를 animclip으로 변환후 사용자가 지정한 폴더에 저장.
    2. 처리된 파일은 레퍼런스로 불러도 타임라인 조정 가능.
    3. Trax Editor에서 모션블렌드를 할 수 있도록, 처리된 animclip은 프로젝트셋 clip폴더에 
       동일한 파일명으로 export.
        '''
        pathLayout     = QtGui.QGridLayout()
        description    = QtGui.QTextEdit()
        description.setText(text)
        description.setReadOnly(True)
        sourceLabel     = QtGui.QLabel("Source :")
        self.sourceDir  = FolderSearchWidget()
        mocapLabel      = QtGui.QLabel("Motion Capture :")
        self.mocapDir   = FolderSearchWidget()
        clipLabel       = QtGui.QLabel("Animation Clip :")
        self.clipDir    = FolderSearchWidget()
        previewLabel    = QtGui.QLabel("Preview :")
        self.previewDir = FolderSearchWidget()
        
        pathLayout.addWidget(description,    0,0, 1,2)
        pathLayout.addWidget(sourceLabel,    1,0)
        pathLayout.addWidget(self.sourceDir, 1,1)
        pathLayout.addWidget(mocapLabel,     2,0)
        pathLayout.addWidget(self.mocapDir,  2,1)
        pathLayout.addWidget(clipLabel,      3,0)
        pathLayout.addWidget(self.clipDir,   3,1)
        pathLayout.addWidget(previewLabel,   4,0)
        pathLayout.addWidget(self.previewDir,4,1)
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch()
        self.exportButton = QtGui.QPushButton()
        pix = QtGui.QPixmap(MakseAssetDailog.getImagePath()+"/make.png")
        icon = QtGui.QIcon(pix)
        self.exportButton.setIcon(icon)
        self.exportButton.setFixedWidth(50)
        buttonLayout.addWidget(self.exportButton)

        mainLayout.addLayout(pathLayout)
        mainLayout.addLayout(buttonLayout)
        
        self.setWindowTitle("Make Asset")
        self.setFixedSize(600,300)
    
        # Connection
        self.exportButton.clicked.connect(self.makeAsset)
        self.sourceDir.pathLinedit.textChanged.connect(self.updatePath)
        
    def makeAsset(self):
        try:
            self.callback(self.sourceDir.getDirectory(), 
                          self.mocapDir.getDirectory(), 
                          self.clipDir.getDirectory(),
                          self.previewDir.getDirectory())
            self.accept()
        except:
            self.rect()
    
    def updatePath(self):
        path = self.sourceDir.getDirectory()
        self.mocapDir.pathLinedit.setText(os.path.join(path,'hik'))
        self.clipDir.pathLinedit.setText(os.path.join(path,'clip'))
        self.previewDir.pathLinedit.setText(os.path.join(path,'preview'))
        
    @classmethod
    def getRootPath(cls):
        path = os.path.dirname(__file__)
        return os.path.dirname(path)
    
    @classmethod
    def getImagePath(cls):
        return os.path.join(cls.getRootPath(),'view/images')
        

def testCallback(source, mocap, clip, preview):
    print source
    print mocap
    print clip
    print preview
        
def main():
    app = QtGui.QApplication([])
    dlg = MakseAssetDailog(testCallback)
    dlg.show()
    app.exec_()
    
if __name__ == "__main__":
    main()