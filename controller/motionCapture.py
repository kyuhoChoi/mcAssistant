# coding:utf-8

import pymel.core as pm
import maya.mel as mel
import math
import glob
import os
import shutil

mocapJoints = ['Hips', 'Spine', 'Spine1' , 'Spine2', 'Neck', 'Head',
               'LeftShoulder' , 'LeftArm', 'LeftForeArm', 'LeftHand' , 'LeftFingerBase',
               'RightShoulder','RightArm','RightForeArm', 'RightHand', 'RightFingerBase',
               'LeftUpLeg', 'LeftLeg', 'LeftFoot', 'LeftToeBase', 
               'RightUpLeg','RightLeg','RightFoot','RightToeBase']

chFile = 'I:/GoogleDrive/1_MayaPy/03_Utils/MotionCaptuerTool/file/MC.ma'
namespace= 'mcData'

def makePreviw(path):
    tempFloor = pm.polyPlane(n='tempFloor')
    tempFloor[0].scaleX.set(10000)
    tempFloor[0].scaleY.set(10000)
    tempFloor[0].scaleZ.set(10000)
    tempFloor[1].subdivisionsWidth.set(100)
    tempFloor[1].subdivisionsHeight.set(100)
    
    tempCam = pm.camera()[0]
    camNode = pm.PyNode(tempCam)
    camNode.rename('tempCam')
    pm.lookThru( camNode )
    pm.select('Hips', r=True)
    hipJnt = pm.PyNode('Hips')
    mel.eval('fitPanel -selected;')
    pointCon = pm.pointConstraint(hipJnt,camNode, mo=True)
    
    pm.select(tempFloor[0], r=True)
    pm.playblast(fp=4, clearCache=1, showOrnaments=0, sequenceTime=0, format='image', percent=100, 
                 filename=path , viewer=0, quality=100, widthHeight=(128, 128), compression="png")
    
    pm.lookThru( 'persp' )
    pm.delete(camNode, tempFloor, pointCon)
    
def importCharactor():
    pm.importFile( chFile )
    
def getSourceNamespace():
    source_namespace = ''
    HikNodes = pm.ls( type = 'HIKCharacterNode')
    HikNode = None
    for node in HikNodes:
        if node.name().startswith(namespace):
            HikNode=node
        
    cleanHipNodename = HikNode.Hips.get().partition("mcData:")[2]
    stripname = cleanHipNodename.partition(':')
    if stripname[1] == ':':
        source_namespace = stripname[0]
    else:
        source_namespace = ''
    return source_namespace

def makeAsset( source_mcDir=None, 
               export_mcDir=None, 
               export_clipDir=None, 
               export_previewDir=None):
        
    fileList = glob.glob( source_mcDir + '/*.mb')
    fileList.extend( glob.glob( source_mcDir + '/*.ma') )
    fileList.extend( glob.glob( source_mcDir + '/*.fbx') )
    
    for i, sourceFile in enumerate(fileList):
        sceneName = os.path.basename( sourceFile )
        pm.newFile( force=True )
        pm.importFile( chFile )
        charSet = pm.PyNode('set')
        refNode = pm.createReference( sourceFile, namespace=namespace)
        
        # 모션캡쳐 조인트에서 키복사 
        errorLine = []
        for jnt in mocapJoints:
            source_namespace = getSourceNamespace()
            if source_namespace:
                source_namespace += ':'
            else:
                source_namespace = ''

            sourceJnt = '{}:{}{}'.format(namespace,source_namespace,jnt)
            targetJnt = jnt
            print '{} --> {}'.format(sourceJnt, targetJnt)   
            
            if targetJnt == "Hips":
                attrs = ['tx','ty','tz','rx','ry','rz']    
            else:
                attrs = ['rx','ry','rz']
            
            for attr in attrs:
                try:
                    pm.copyKey ( sourceJnt + '.' + attr )
                    pm.pasteKey( targetJnt + '.' + attr, option='merge' )
                except:
                    errorLine.append( u'#    {}.{} >> {}.{}'.format(sourceJnt, attr, targetJnt, attr) )
        
        if errorLine:
            print u'# '
            print u'# "%s"'%sourceFile
            print u'# '

            print '\n'.join(errorLine)

            print u'# '
            print u'# 어트리뷰트 key 복사, 붙이기 과정에서 에러가 발생했습니당. 아래내용을 확인해주세요.'                    
            print u'#    1. 모션캡쳐파일에 animation Layer가 사용된경우 --> animation Layer를 merge시키세요.'
            print u'#    2. 위 attribute에 key가 존재하지않을경우 --> 처리된 파일엔 문제가 없을수도 있습니다. 이 에러가 마음에 걸리면, 위 어트리뷰트에 임의의 키를 주세요.'
            print u'#    3. 해당 노드가 삭제된 경우 --> 모션캡쳐 업체에 다시 문의하세요.'
            print u'# '

        # 레퍼런스 날림
        refNode.remove()
        
        # 타임라인 조정
        #animNodes = pm.keyframe('Hips', q=True, name=True )
        times = pm.keyframe('Hips',at='rx',q=True, tc=True)
        pm.playbackOptions( min= math.floor(times[ 0]), max= math.ceil (times[-1]) )
        
        # 애니메이션 클립 생성
        animClip = pm.clip(charSet, name='animClip', scheduleClip=True, allAbsolute=True, animCurveRange=True)[0]
        animClip = pm.PyNode( animClip )
        animClip.rename( pm.mel.formValidObjectName( sceneName ) )
        
        # 애니메이션 클립 내보냄 
        # 프로젝트의 clip폴더로 내보냄.
        exportPath = os.path.join( export_clipDir, sceneName)

        pm.select(animClip)
        pm.mel.source( "doExportClipArgList.mel" )
        pm.mel.clipEditorExportClip( exportPath, "ma")
        
        # 프리뷰를 만든다.
        print sourceFile
        fullFileName = os.path.basename(sourceFile)
        withoutExtFileName =  os.path.splitext(fullFileName)[0]
        # 폴더가 있는지 확인 하고 있으면 지운다
        previewDir = os.path.join(export_previewDir, withoutExtFileName + '_preview')
        print previewDir
        if os.path.exists(previewDir):
            shutil.rmtree(previewDir)
        
        os.makedirs(previewDir)
        makePreviw(os.path.join(previewDir,withoutExtFileName))
        
        # 파일저장
        print export_mcDir
        pm.saveAs( '%s\\%s.mb'%( export_mcDir, sceneName) )

        # 결과 출력
        print '#---------------------------------------------'
        print '#'
        print '# %d%% convert! (%03d/%03d) "%s"'%( math.floor( float(i+1)/len(fileList)*100 ), i+1,len(fileList),sceneName)
        print '#'
        print '#---------------------------------------------'
        

# def main():
#     source_mcDir      = 'D:/151006_Mocap_Data'
#     export_mcDir      = 'D:/151006_Mocap_Data/hik'
#     export_clipDir    = 'D:/151006_Mocap_Data/clip'
#     export_previewDir = 'D:/151006_Mocap_Data/preview'
#     makeAsset(source_mcDir, export_mcDir, export_clipDir, export_previewDir)
# 
# if __name__ == 'motionCapture':
#     main()