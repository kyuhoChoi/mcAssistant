#mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\scene\animation\motioncapture\FBX\choice\161227\Etc_orc_attacked_fall_01.fbx'
#mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\scene\animation\motioncapture\FBX\choice\161227\D_01_KO_Fight_knight_look_M_02.fbx'
mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\assets\mc\motionCapture\A_01_pov_run_knight_orc_conner_01_M_02.ma'
outputFoler_motionCapture = 'D:/Users/kyuho_choi/Desktop/motionCapture/motionCapture'
outputFoler_ainmClip      = 'D:/Users/kyuho_choi/Desktop/motionCapture/animClip'
outputFolder_playblast    = 'D:/Users/kyuho_choi/Desktop/motionCapture/preview'

#mcCharFile = 'D:/Users/kyuho_choi/Desktop/MC/MC.ma'
mcCharFile = 'D:/Users/kyuho_choi/Desktop/mc.ma'
sampleJntName = 'Hips'
charPrefixs = ['charA','charB','charC','charD','charE','charF','charG','charH']
mocapNamespace = 'data'

#---------------
#
# Motion Key Transfer
#
#---------------
# 새파일
pm.newFile( force=True )

# 레퍼런스로 모션 부름
refNode = pm.createReference( mocapSrcFile, namespace='mocapSrcFile')

# src_HIKs
src_HIKs = pm.ls(type='HIKCharacterNode')

#
for src_HIK, prefix in zip( src_HIKs, charPrefixs ):
    #src_HIK = src_HIKs[0]
    #prefix = charPrefixs[0]
        
    # 캐릭터 수량에 따른 조정 내용
    importOpt = {"returnNewNodes":True }
    prefix_ = ''
    if len(src_HIKs)>1 :
        importOpt = {"returnNewNodes":True, "renameAll":True, "renamingPrefix":prefix}
        prefix_ = prefix + '_'
        
    # 모션캡쳐 캐릭터 파일 임포트
    newNodes = pm.importFile( mcCharFile, **importOpt )
    
    # HIK
    HIK = pm.ls(newNodes, type='HIKCharacterNode')[0]
    
    # 현재 캐릭터 변경
    pm.mel.hikSetCurrentCharacter(HIK)
    pm.mel.HIKCharacterControlsTool()
    
    # 콘트롤 리그 생성
    pm.mel.hikCreateControlRig()
    
    # 연결
    pm.mel.mayaHIKsetCharacterInput( HIK, src_HIK )
    pm.mel.hikUpdateCurrentCharacterFromScene()
    pm.mel.HIKCharacterControlsTool()
    
    # 타임라인 영역 조정
    pm.mel.setPlaybackRangeToEnabledClips()
    
    # bake
    pm.mel.hikBakeCharacter( 0); 
    
    # 컨트롤 리그 삭제
    pm.mel.hikDeleteControlRig()

# 레퍼런스 날림
refNode.remove()
    
# 화면 갱신
pm.refresh()

#---------------
#
# animClip
#
#---------------
# 캐릭터 셋 이름 확인
charSets = pm.ls( type='character')
animClips = []

for charSet in charSets:
    # 애니메이션 클립 생성
    #charSet = charSets[2]
    animClip = pm.clip(charSet, name='animClip', scheduleClip=True, allAbsolute=True, animCurveRange=True)[0]
    animClip = pm.PyNode( animClip )
    
    # 클립 이름 결정
    animClipName = pm.mel.basenameEx( mocapSrcFile )
    if len(charSets)>1 :
        animClipName = animClipName + '__' + charSet.name().split('_')[0]
    
    # 리네임
    animClip.rename( pm.mel.formValidObjectName( animClipName ) )
    animClips.append(animClip)

#---------------
#
# Export
#
#---------------
# 클립길이로 타임라인 조정
pm.mel.setPlaybackRangeToEnabledClips()

# 애니메이션 클립 우선 저장
for animClip in animClips:
    exportPath = outputFoler_ainmClip +'/'+ animClip.name() +'.ma'

    pm.select(animClip)
    pm.mel.source( "doExportClipArgList.mel" )
    pm.mel.clipEditorExportClip( exportPath, "ma")

# 파일저장
exportPath = outputFoler_motionCapture +'/'+ pm.mel.basenameEx( mocapSrcFile ) +'.ma'

exportNodes = pm.ls( type=['joint','character', 'HIKCharacterNode'])
pm.select( exportNodes ) 
pm.exportSelected( exportPath, f=True )
    
# 화면 갱신
pm.refresh()

#---------------
#
# playblast
#
#---------------

#---------------
# 그리드 생성
#---------------
#그리드 하나당 1m
gridScale=1000 

# 프리뷰 그리드 생성 : 얇은 줄
mesh = pm.polyPlane(sh=10,sw=10)[0]
mesh.s.set(gridScale,gridScale,gridScale) #그리드 하나당 1m
mesh.getShape().overrideEnabled.set(True)
mesh.getShape().overrideDisplayType.set(1) # 템플릿
mesh.getShape().overrideShading.set(0)
pm.polyDelEdge( [mesh.e[11], mesh.e[32], mesh.e[53], mesh.e[74], mesh.e[95], mesh.e[105], mesh.e[107], mesh.e[109], mesh.e[111], mesh.e[113], mesh.e[115:117], mesh.e[119], mesh.e[121], mesh.e[123], mesh.e[137], mesh.e[158], mesh.e[179], mesh.e[200]], cv=True, ch=1 )

# 프리뷰 그리드 생성 : 중앙 굵은 줄
mesh2 = pm.polyPlane(sh=2,sw=2,h=1.01,w=1.01)[0]
mesh2.s.set(gridScale,gridScale,gridScale) #그리드 하나당 1m
mesh2.getShape().overrideEnabled.set(True)
mesh2.getShape().overrideDisplayType.set(2) # 레퍼런스
mesh2.getShape().overrideShading.set(0)

# 하나로 합치고 이름 변경
pm.parent( mesh2.getShape(), mesh, s=True, r=True )
pm.delete( mesh2 )   
mesh.rename('previewGrid_10mx10m')

# 위치 조정
sampleJoints = pm.ls(type='joint')
if sampleJoints:
    pm.delete( pm.pointConstraint(sampleJoints,mesh) )
    mesh.ty.set(0)

# 화면 갱신
pm.refresh()

#---------------
# follow cam 생성
#---------------
# 카메라와 그룹 생성
cam = pm.camera(n='followCam')[0]
grp = pm.group( cam, n='followCam_grp' )

# 컨스트레인
pm.pointConstraint( pm.ls(type='joint'), grp ) # 컨스트레인

# 카메라 조정
cam.tz.set(1200)
cam.focalLength.set(100)
cam.centerOfInterest.set(1200)
cam.filmFit.set(2) # vertical

cam.r.set(-15, 15, 0)

# 패널 조정
activePanel = pm.playblast( activeEditor=True ).split('|')[-1]
pm.modelPanel( activePanel, edit=True, camera=cam )

# 카메라 핏 시킴
pm.select( pm.ls(type='joint') )
pm.viewFit( cam, fitFactor=1 )
pm.select(cl=True)

# 화면 갱신
pm.refresh()

#---------------
# 플레이 블라스트
#---------------
# 클립길이로 타임라인 조정
pm.mel.setPlaybackRangeToEnabledClips()

# 임시 헤드업 디스플레이
#if pm.headsUpDisplay('tmpHUD', q=True, exists=True):
#    pm.headsUpDisplay('tmpHUD', rem=True )

#sceneName = outputFoler_motionCapture +'/'+ pm.mel.basenameEx( mocapSrcFile ) +'.ma'
#pm.headsUpDisplay('tmpHUD',
#    section=6,
#    block=0,
#    blockSize = 'medium',
#    label = 'FileName :',
#    labelFontSize = 'large',
#    command = pm.Callback( pm.mel.basenameEx, sceneName ),
#    )

# 플레이 블라스트
pm.playblast( 
    #filename="D:/Users/kyuho_choi/Desktop/testssss.mov",
    filename= outputFolder_playblast +'/'+ pm.mel.basenameEx( mocapSrcFile ) +'.mov',
    forceOverwrite=True,

    format='qt',
    compression="H.264",
    quality=80,
    sequenceTime=0,

    clearCache=True,
    #viewer=True,
    viewer=False,
    showOrnaments=True,
    offScreen=True,
    fp=4,

    widthHeight=[512,512],
    percent=100,
    )

# 임시 헤드업 디스플레이 삭제
#pm.headsUpDisplay( 'tmpHUD', rem=True )