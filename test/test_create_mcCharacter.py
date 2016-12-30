#-----------------------
#
# Load Plug-ins
# 
#-----------------------
pm.pluginInfo( "mayaHIK", q=True, l=True)
pm.loadPlugin( "mayaHIK" )
pm.pluginInfo( "mayaCharacterization", q=True, l=True)
pm.loadPlugin( "mayaCharacterization" )
pm.pluginInfo( "OneClick", q=True, l=True)
pm.loadPlugin( "OneClick" )

#-----------------------
#
# Human IK Window Open/ Update
# 
#-----------------------
pm.mel.HIKCharacterControlsTool()

#-----------------------
#
# Definition
# 
#-----------------------
pm.mel.hikCreateDefinition()

# 현재 Definition 리턴
hikDef = pm.mel.hikGetCurrentCharacter()
hikDef = pm.melGlobals['gHIKCurrentCharacter']

# Definition 이름변경
hikDef = pm.PyNode(hikDef)
hikDef.rename('HIK')

# 각 파트 어싸인
jnt2HIK_list=[
    [ 0,"Reference"],   # Reference
    
    [ 1,"Hips"],        # Hips
    [ 2,"LeftUpLeg"],   # LeftUpLeg
    [ 3,"LeftLeg"],     # LeftLeg
    [ 4,"LeftFoot"],    # LeftFoot
    [ 5,"RightUpLeg"],  # RightUpLeg
    [ 6,"RightLeg"],    # RightLeg
    [ 7,"RightFoot"],   # RightFoot
    [ 8,"Spine"],       # Spine
    [ 9,"LeftArm"],     # LeftArm
    [10,"LeftForeArm"], # LeftForeArm
    
    [11,"LeftHand"],     # LeftHand
    [12,"RightArm"],     # RightArm
    [13,"RightForeArm"], # RightForeArm
    [14,"RightHand"],    # RightHand
    [15,"Head"],         # Head
    [16,"LeftToeBase"],  # LeftToeBase
    [17,"RightToeBase"], # RightToeBase
    [18,"LeftShoulder"], # LeftShoulder
    [19,"RightShoulder"],# RightShoulder
    [20,"Neck"],         # Neck

    [21,"LeftFingerBase"],  # LeftFingerBase
    [22,"RightFingerBase"], # RightFingerBase
    [23,"Spine1"],          # Spine1
    [24,"Spine2"],          # Spine2
    [25,"Spine3"],          # Spine3
    ]

for num, jnt in jnt2HIK_list:
    if pm.objExists(jnt):
        pm.mel.setCharacterObject(jnt, hikDef, num, 0)



# 정의 롹2
pm.mel.HIKCharacterControlsTool() # 업데이트
lockState = pm.mel.hikIsDefinitionLocked('HIK')
pm.mel.hikCharacterLock('HIK',not lockState,1)
pm.mel.hikUpdateDefinitionButtonState() # Update the button states


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
    'Spine3.rx','Spine3.ry','Spine3.rz',  
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
