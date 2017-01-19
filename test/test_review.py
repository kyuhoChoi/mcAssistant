# 캐릭터 일부 선택
sel = pm.selected()
if not sel:
    raise

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

# find root
node = sel[0]
root = pm.PyNode( node.name(long=True).split("|")[1] )

# 컨스트레인
pm.select(root)
pm.select(hi=True)
jnts = pm.ls( sl=True, type='joint')

pm.pointConstraint( jnts, grp ) # 컨스트레인

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
pm.select( jnts )
pm.viewFit( cam, fitFactor=1 )
pm.select(cl=True)

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
