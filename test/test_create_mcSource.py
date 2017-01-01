mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\scene\animation\motioncapture\FBX\choice\161227\Etc_orc_attacked_fall_01.fbx'
#mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\scene\animation\motioncapture\FBX\choice\161227\D_01_KO_Fight_knight_look_M_02.fbx'
outputFoler_motionCapture = 'D:/Users/kyuho_choi/Desktop/motionCapture/motionCapture'
outputFoler_ainmClip      = 'D:/Users/kyuho_choi/Desktop/motionCapture/animClip'
outputFolder_playblast    = 'D:/Users/kyuho_choi/Desktop/motionCapture/preview'

mcCharFile = 'D:/Users/kyuho_choi/Desktop/MC/MC.ma'
jnts = []
sampleJntName = 'Spine'
charPrefixs = ['charA','charB','charC','charD','charE','charF','charG','charH']
mocapNamespace = 'data'

# 조인트 리스트
if not jnts:
    # 새파일
    pm.newFile( force=True )
    
    # 모션캡쳐 캐릭터 임포트
    pm.importFile( mcCharFile )
    
    # 조인트 리스트
    jnts = [ jnt.name() for jnt in pm.ls(type='joint')]


#---------------
#
# Motion Key Transfer
#
#---------------
# 새파일
pm.newFile( force=True )

# 레퍼런스로 모션 부름
refNode = pm.createReference( mocapSrcFile, namespace=mocapNamespace)

# 캐릭터 수량 파악
sampleJnts = []
mocapNamespaces = []
for jnt in pm.ls(type='joint'):    
    # 네임스페이스를 제거한 이름이
    name = jnt.name().replace( jnt.namespace(), '' )
    
    # 샘플과 맞으면
    if sampleJntName == name:
        sampleJnts.append(jnt)
        mocapNamespaces.append(jnt.namespace())
        
for sourceNamespace, prefix in zip( mocapNamespaces, charPrefixs ):
    #sourceNamespace = mocapNamespaces[0]
    #prefix = charPrefixs[0]
    
    # 캐릭터 수량에 따른 조정 내용
    importOpt = {"returnNewNodes":True }
    prefix_ = ''
    if len(mocapNamespaces)>1 :
        importOpt = {"returnNewNodes":True, "renameAll":True, "renamingPrefix":prefix}
        prefix_ = prefix + '_'
    
    # 모션캡쳐 캐릭터 파일 임포트
    newNodes = pm.importFile( mcCharFile, **importOpt )
   
    # 모션캡쳐 조인트에서 키값 복 붙
    errorLine = []
    for jnt in jnts:
        source_jnt = pm.PyNode( sourceNamespace + jnt )
        target_jnt = pm.PyNode( prefix_ + jnt )
    
        print '%s --> %s'%(source_jnt, target_jnt)
    
        if jnt=='Hips':
            attrs = ['tx','ty','tz','rx','ry','rz']
        else:
            attrs = ['rx','ry','rz']
    
        for attr in attrs: 
            source_attr = source_jnt.attr(attr)
            target_attr = target_jnt.attr(attr)
            
            try:
                pm.copyKey( source_attr )
                pm.pasteKey( target_attr, option='merge' )
    
            except:
                # 에러가 발생하면.. (키가없거나.. 할 수도 있음)
                errorLine.append( u'#    %s >> %s' % (source_attr, target_attr ) )
    
                # 그냥 값을 입력받아서 적어넣음.
                target_attr.set( source_attr.get() )
    
# 레퍼런스 날림
refNode.remove()
            
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

#---------------
# 플레이 블라스트
#---------------
pm.playblast( 
    #filename="D:/Users/kyuho_choi/Desktop/testssss.mov",
    filename= outputFolder_playblast +'/'+ pm.mel.basenameEx( mocapSrcFile ) +'.mov',
    forceOverwrite=True,

    format='qt',
    compression="H.264",
    quality=80,
    sequenceTime=0,

    clearCache=True,
    viewer=True,
    showOrnaments=True,
    offScreen=True,
    fp=4,

    widthHeight=[512,512],
    percent=100,
    )