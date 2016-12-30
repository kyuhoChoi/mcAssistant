# coding:utf-8

from PySide import QtGui, QtCore
import os
import maya.OpenMayaUI as OpenMayaUI
from shiboken import wrapInstance

import animListWidget
reload(animListWidget)
from animListWidget import AnimListWidget

import makeAssetDialog
reload(makeAssetDialog)
from makeAssetDialog import MakseAssetDailog

import animButton
reload(animButton)
from animButton import AnimButton

import Control.motionCapture as Mocap
reload(Mocap)



__version__ = "1.0.0"

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

def mayaToQtObject( inMayaUI ):
    ptr = OpenMayaUI.MQtUtil.findControl( inMayaUI )
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout( inMayaUI )
    if ptr is None:
        ptr= OpenMayaUI.MQtUtil.findMenuItem( inMayaUI )
    if ptr is not None:
        return wrapInstance( long( ptr ), QtGui.QWidget )


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, size=128, parent = getMayaWindow()):
        super(MainWindow, self).__init__(parent)
        
        self.__rootPath    = MainWindow.getRootPath()
        self.__imagePath   = MainWindow.getImagePath()
        self.__sourcePath  = self.__rootPath
        self.__assetPath   = self.__rootPath
        self.__clipPath    = self.__rootPath
        self.__previewPath = self.__rootPath
        self.__imageSize   = size
        self.__fileType    = "hik"
        self.__operation   = "reference" 
        
        # Central Widget
        self.animListWidget = AnimListWidget()
        self.animListWidget.setMinimumSize(500,500)
        self.animListWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setCentralWidget(self.animListWidget)
        
        # Status Bar
        self.status = self.statusBar()
        #self.status.showMessage("Ready", 5000)
        
        # Add Menu Actions
        charactorAction = self.createAction( "Import Character", slot=self.importCharacter, icon="character", tip=u"모션캡쳐 업체로 보낼 캐릭터를 임포트 합니다.")
        makeAssetAction = self.createAction( "Make Asset", slot=self.makeAsset, icon="make", tip=u"모션캡쳐 업체에서 받은 파일을 처리 합니다.")
        loadAssetAction = self.createAction( "Load Asset", slot=self.loadAsset, icon="load", tip=u"처리된 데이터들을 로드 합니다.")
        quitAction      = self.createAction( "Quit", slot=self.close, icon="quit",tip=u"프로그램을 종료 합니다.")     
        
        # Add File Type Actions
        self.fileTypeGroup = QtGui.QActionGroup(self)
        hikAction = self.createAction( "HIK", slot=self.setHIK, icon="HIK", tip=u"HIK 타입 파일로 설정 합니다.", checkable=True, signal="toggled")
        aniAction = self.createAction( "ANI", slot=self.setANI, icon="ANI", tip=u"Clip 타입 파일로 설정 합니다.", checkable=True, signal="toggled")
        fbxAction = self.createAction( "FBX", slot=self.setFBX, icon="FBX", tip=u"FBX 타입 파일로 설정 합니다.",     checkable=True, signal="toggled")
        self.fileTypeGroup.addAction(hikAction)
        self.fileTypeGroup.addAction(aniAction)
        self.fileTypeGroup.addAction(fbxAction)
        hikAction.setChecked(True)
        
        # Add Operation Actions
        self.operationGroup = QtGui.QActionGroup(self)
        openPoseAction      = self.createAction( "Open", slot=self.setOpen, icon="open", tip=u"파일 처리를 open 으로 설정 합니다.", checkable=True, signal="toggled")
        importPoseAction    = self.createAction( "Import", slot=self.setImport, icon="import", tip=u"파일 처리를 import 로 설정 합니다.", checkable=True, signal="toggled")
        referencePoseAction = self.createAction( "Reference", slot=self.setReference, icon="reference", tip=u"파일 처리를 reference 설정 합니다.", checkable=True, signal="toggled")
        self.operationGroup.addAction(openPoseAction)
        self.operationGroup.addAction(importPoseAction)
        self.operationGroup.addAction(referencePoseAction)
        referencePoseAction.setChecked(True)
        
        # Add Menu Menu
        self.menu = self.menuBar().addMenu("Menu")
        self.menuActions = [charactorAction, makeAssetAction, loadAssetAction, None, quitAction]
        self.addActions(self.menu, self.menuActions)    
        
        # Add File Type Menu
        self.fileType = self.menuBar().addMenu("File Type")
        self.fileTypeActions = [hikAction, aniAction, fbxAction]
        self.addActions(self.fileType, self.fileTypeActions)    
        
        # Add Operation Menu
        self.operation = self.menuBar().addMenu("Operation")
        self.operationActions = [openPoseAction, importPoseAction, referencePoseAction]
        self.addActions(self.operation, self.operationActions)
        
        # Add Menu Tool Bar
        menuToolbar = self.addToolBar("Menu")
        self.addActions(menuToolbar, [charactorAction, makeAssetAction, loadAssetAction])
        
        # Add File Type Tool Bar
        fileTypeToolbar = self.addToolBar("FileType")
        self.addActions(fileTypeToolbar, [hikAction, aniAction, fbxAction])
        
        # Add Operation Tool Bar
        operationToolbar = self.addToolBar("Operation")
        self.addActions(operationToolbar, [openPoseAction, importPoseAction, referencePoseAction])
        
        # Add Animation Speed Tool Bar
        animSpeedToolbar = self.addToolBar("AnimSpeed")
        self.animSpeedSlider = QtGui.QDial()
        self.animSpeedSlider.setSingleStep(1)
        self.animSpeedSlider.setFixedSize(40,40)
        self.animSpeedSlider.setMinimum(1)
        self.animSpeedSlider.setMaximum(50)
        self.animSpeedSlider.setValue(30)
        self.animSpeedSlider.valueChanged.connect(self.setSpeed)
        animSpeedToolbar.addWidget(self.animSpeedSlider)
        
        # Add Path Tool Bar
        pathToolbar = self.addToolBar("Path")
        self.pathLineEdit = QtGui.QLineEdit(self.__assetPath)
        pathToolbar.addWidget(self.pathLineEdit)
        
        # Add RMB Click Menu
        self.addActions(self.animListWidget, [hikAction, aniAction, fbxAction, "separator", openPoseAction, importPoseAction, referencePoseAction])
        
        # Window Setting
        self.setWindowTitle("Motion Capture Pose Tool")
        self.setGeometry(500, 500, 1000, 500)
        
    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon("{}/{}.png".format(self.__imagePath,icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            elif action == "separator":
                separator = QtGui.QAction(self)
                separator.setSeparator(True)
                target.addAction(separator) 
            else:
                target.addAction(action) 
    
    def importCharacter(self):
        Mocap.importCharactor()
        
    def makeAsset(self):        
        dlg = MakseAssetDailog(self.setPath)
        if dlg.exec_():
            self.pathLineEdit.setText(self.__previewPath)
            self.printStaus(u"작업이 성공 적으로 완료 되었습니다.", "yellow")
        else:
            self.printStaus(u"작업이 실패 또는 취소 됬습니다.", "red")
        
    def loadAsset(self):
        loadPath = QtGui.QFileDialog.getExistingDirectory(dir=self.__previewPath)
        
        if loadPath:
            self.animListWidget.clear()
            self.animListWidget.setDefault()
            self.pathLineEdit.setText(loadPath)    
            
            buttons = []
            previewPathList = os.listdir(loadPath)
            for basePath in previewPathList:
                animButton = AnimButton(20)
                basePath = os.path.join(loadPath,basePath)
                frames = os.listdir(basePath)
                animButton.setFrames(basePath, frames)
                animButton.setSize(QtCore.QSize(128, 128))
                buttons.append(animButton)
            self.animListWidget.setItems(buttons)
        else:
            print self.__assetPath
            
    def setHIK(self):
        self.__fileType = "hik"
        self.animListWidget.setOption(self.__fileType, self.__operation)
        
    def setANI(self):
        self.__fileType = "ani"
        self.animListWidget.setOption(self.__fileType, self.__operation)
        
    def setFBX(self):
        self.__fileType = "fbx"
        self.animListWidget.setOption(self.__fileType, self.__operation)
        
    def setOpen(self):
        self.__operation = "open"
        self.animListWidget.setOption(self.__fileType, self.__operation)
        
    def setImport(self):
        self.__operation = "import"
        self.animListWidget.setOption(self.__fileType, self.__operation)
        
    def setReference(self):
        self.__operation = "reference"
        self.animListWidget.setOption(self.__fileType, self.__operation)
    
    def setPath(self, source, mocap, clip, preview):
        self.__sourcePath  = source
        self.__assetPath   = mocap
        self.__clipPath    = clip
        self.__previewPath = preview
        Mocap.makeAsset(source, mocap, clip, preview, self.__imageSize)
        
    def printStaus(self, text, fontcolor):
        self.status.setStyleSheet("QStatusBar{color:%s;font-weight:bold;}" %(fontcolor))
        self.status.showMessage(text, 3000)
        self.status.setStyleSheet("QStatusBar{color:black;}")
    
    def setSpeed(self):
        speed = self.animSpeedSlider.value()
        self.animListWidget.setSpeed(speed)
        
    @classmethod
    def getRootPath(cls):
        path = os.path.dirname(__file__)
        return os.path.dirname(path)
    
    @classmethod
    def getImagePath(cls):
        return os.path.join(cls.getRootPath(),'view/images')
    
def main():
    global win
    try:
        win.close()
        win.deleteLater()
    except: 
        pass
    win = MainWindow()
    """buttons = []
    for i in range(10):
        animButton = AnimButton(5)
        basePath = 'D:/151006_Mocap_Data/preview/A_01_M_Stand_Look_Breath_01_M_03_preview'
        frames = os.listdir(basePath)
        animButton.setFrames(basePath, frames)
        animButton.setSize(QtCore.QSize(128, 128))
        buttons.append(animButton)
        print i
    win.animListWidget.setItems(buttons)"""
    win.show()

main()