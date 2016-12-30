#-----------------------
#
# Character Set
#
#-----------------------
# Create Character Set
charSet = pm.character(name="set")

# Add to Character Set
attrs = [
    'Hips.tx','Hips.ty','Hips.tz',
    'Hips.rx','Hips.ry','Hips.rz',
    
    'Spine.rx','Spine.ry','Spine.rz',
    'Spine1.rx','Spine1.ry','Spine1.rz',
    'Spine2.rx','Spine2.ry','Spine2.rz',    
    'Neck.rx','Neck.ry','Neck.rz',
    'Head.rx','Head.ry','Head.rz',
    
    'LeftShoulder.rx','LeftShoulder.ry','LeftShoulder.rz',
    'LeftArm.rx','LeftArm.ry','LeftArm.rz',
    'LeftForeArm.rx','LeftForeArm.ry','LeftForeArm.rz',
    'LeftHand.rx','LeftHand.ry','LeftHand.rz',

    'RightShoulder.rx','RightShoulder.ry','RightShoulder.rz',
    'RightArm.rx','RightArm.ry','RightArm.rz',
    'RightForeArm.rx','RightForeArm.ry','RightForeArm.rz',
    'RightHand.rx','RightHand.ry','RightHand.rz',
    
    'LeftUpLeg.rx','LeftUpLeg.ry','LeftUpLeg.rz',
    'LeftLeg.rx','LeftLeg.ry','LeftLeg.rz',
    'LeftFoot.rx','LeftFoot.ry','LeftFoot.rz',
    'LeftToeBase.rx','LeftToeBase.ry','LeftToeBase.rz',    
    
    'RightUpLeg.rx','RightUpLeg.ry','RightUpLeg.rz',
    'RightLeg.rx','RightLeg.ry','RightLeg.rz',
    'RightFoot.rx','RightFoot.ry','RightFoot.rz',
    'RightToeBase.rx','RightToeBase.ry','RightToeBase.rz', 
    ]
for attr in attrs:
    pm.character( attr, add=charSet )
    
#-----------------------
#
# Animation Clip
#
#-----------------------
# 애니메이션 클립 생성
animClip = pm.clip(charSet, name='animClip', scheduleClip=True, allAbsolute=True, animCurveRange=True)[0]
animClip = pm.PyNode( animClip )
animClip.rename( pm.mel.formValidObjectName( sceneName ) )

#-----------------------
#
# Animation Clip 저장
#
#-----------------------
# 프로젝트의 clip폴더로 내보냄.
# projectDir = pm.workspace( q=True, rd=True)
# clipDir    = projectDir+'clips/'
# exportPath = clipDir + sceneName
exportPath = '%s\\%s.mb'%( export_clipDir, sceneName)

pm.select(animClip)
pm.mel.source( "doExportClipArgList.mel" )
pm.mel.clipEditorExportClip( exportPath, "ma")

#-----------------------
#
# Animation Clip 저장
#
#-----------------------
pm.saveAs( '%s\\%s.mb'%( export_mcDir, sceneName) )

