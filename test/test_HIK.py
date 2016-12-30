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
    [26,"Spine4"],          # Spine4
    [27,"Spine5"],          # Spine5
    [28,"Spine6"],          # Spine6
    [29,"Spine7"],          # Spine7
    [30,"Spine8"],          # Spine8
    
    [31,"Spine9"],          # Spine9
    [32,"Neck1"],           # Neck1
    [33,"Neck2"],           # Neck2          
    [34,"Neck3"],           # Neck3         
    [35,"Neck4"],           # Neck4
    [36,"Neck5"],           # Neck5
    [37,"Neck6"],           # Neck6
    [38,"Neck7"],           # Neck7
    [39,"Neck8"],           # Neck8
    [40,"Neck9"],           # Neck9
     
    [41,"LeftUpLegRoll"],    # LeftUpLegRoll
    [42,"LeftLegRoll"],      # LeftLegRoll
    [43,"RightUpLegRoll"],   # RightUpLegRoll
    [44,"RightLegRoll"],     # RightLegRoll
    [45,"LeftArmRoll"],      # LeftArmRoll
    [46,"LeftForeArmRoll"],  # LeftForeArmRoll
    [47,"RightArmRoll"],     # RightArmRoll
    [48,"RightForeArmRoll"], # RightForeArmRoll
    [49,"HipsTranslation"],  # HipsTranslation
    [50,"LeftHandThumb1"],   # LeftHandThumb1

    [51,"LeftHandThumb2"],   # LeftHandThumb2
    [52,"LeftHandThumb3"],   # LeftHandThumb3
    [53,"LeftHandThumb4"],   # LeftHandThumb4
    [54,"LeftHandIndex1"],   # LeftHandIndex1
    [55,"LeftHandIndex2"],   # LeftHandIndex2
    [56,"LeftHandIndex3"],   # LeftHandIndex3
    [57,"LeftHandIndex4"],   # LeftHandIndex4
    [58,"LeftHandMiddle1"],  # LeftHandMiddle1
    [59,"LeftHandMiddle2"],  # LeftHandMiddle2
    [60,"LeftHandMiddle3"],  # LeftHandMiddle3
    
    [61,"LeftHandMiddle4"],      # LeftHandMiddle4
    [62,"LeftHandRing1"],        # LeftHandRing1
    [63,"LeftHandRing2"],        # LeftHandRing2
    [64,"LeftHandRing3"],        # LeftHandRing3
    [65,"LeftHandRing4"],        # LeftHandRing4
    [66,"LeftHandPinky1"],       # LeftHandPinky1
    [67,"LeftHandPinky2"],       # LeftHandPinky2
    [68,"LeftHandPinky3"],       # LeftHandPinky3
    [69,"LeftHandPinky4"],       # LeftHandPinky4
    [70,"LeftHandExtraFinger1"], # LeftHandExtraFinger1
    
    [71,"LeftHandExtraFinger2"], # LeftHandExtraFinger2
    [72,"LeftHandExtraFinger3"], # LeftHandExtraFinger3
    [73,"LeftHandExtraFinger4"], # LeftHandExtraFinger4
    [74,"RightHandThumb1"],      # RightHandThumb1
    [75,"RightHandThumb2"],      # RightHandThumb2
    [76,"RightHandThumb3"],      # RightHandThumb3
    [77,"RightHandThumb4"],      # RightHandThumb4
    [78,"RightHandIndex1"],      # RightHandIndex1
    [79,"RightHandIndex2"],      # RightHandIndex2
    [80,"RightHandIndex3"],      # RightHandIndex3
    
    [81,"RightHandIndex4"],      # RightHandIndex4
    [82,"RightHandMiddle1"],     # RightHandMiddle1
    [83,"RightHandMiddle2"],     # RightHandMiddle2
    [84,"RightHandMiddle3"],     # RightHandMiddle3
    [85,"RightHandMiddle4"],     # RightHandMiddle4
    [86,"RightHandRing1"],       # RightHandRing1
    [87,"RightHandRing2"],       # RightHandRing2
    [88,"RightHandRing3"],       # RightHandRing3
    [89,"RightHandRing4"],       # RightHandRing4
    [90,"RightHandPinky1"],      # RightHandPinky1
    
    [91,"RightHandPinky2"],           #
    [92,"RightHandPinky3"],           #
    [93,"RightHandPinky4"],           #
    [94,"RightHandExtraFinger1"],           #
    [95,"RightHandExtraFinger2"],           #
    [96,"RightHandExtraFinger3"],           #
    [97,"RightHandExtraFinger4"],           #
    [98,"LeftFootThumb1"],           #
    [99,"LeftFootThumb2"],           #
    [100,"LeftFootThumb3"],           #
    
    [101,"LeftFootThumb4"],           #
    [102,"LeftFootIndex1"],           #
    [103,"LeftFootIndex2"],           #
    [104,"LeftFootIndex3"],           #
    [105,"LeftFootIndex4"],           #
    [106,"LeftFootMiddle1"],           #
    [107,"LeftFootMiddle2"],           #
    [108,"LeftFootMiddle3"],           #
    [109,"LeftFootMiddle4"],           #
    [110,"LeftFootRing1"],           #
    
    [111,"LeftFootRing2"],           #
    [112,"LeftFootRing3"],           #
    [113,"LeftFootRing4"],           #
    [114,"LeftFootPinky1"],           #
    [115,"LeftFootPinky2"],           #
    [116,"LeftFootPinky3"],           #
    [117,"LeftFootPinky4"],           #
    [118,"LeftFootExtraFinger1"],           #
    [119,"LeftFootExtraFinger2"],           #
    [120,"LeftFootExtraFinger3"],           #
 
    [121,"LeftFootExtraFinger4"],           #
    [122,"RightFootThumb1"],           #
    [123,"RightFootThumb2"],           #
    [124,"RightFootThumb3"],           #
    [125,"RightFootThumb4"],           #
    [126,"RightFootIndex1"],           #
    [127,"RightFootIndex2"],           #
    [128,"RightFootIndex3"],           #
    [129,"RightFootIndex4"],           #
    [130,"RightFootMiddle1"],           #
 
    [131,"RightFootMiddle2"],           #
    [132,"RightFootMiddle3"],           #
    [133,"RightFootMiddle4"],           #
    [134,"RightFootRing1"],           #
    [135,"RightFootRing2"],           #
    [136,"RightFootRing3"],           #
    [137,"RightFootRing4"],           #
    [138,"RightFootPinky1"],           #
    [139,"RightFootPinky2"],           #
    [140,"RightFootPinky3"],           #
    
    [141,"RightFootPinky4"],           #
    [142,"RightFootExtraFinger1"],           #
    [143,"RightFootExtraFinger2"],           #
    [144,"RightFootExtraFinger3"],           #
    [145,"RightFootExtraFinger4"],           #
    [146,"LeftInHandThumb"],           #
    [147,"LeftInHandIndex"],           #
    [148,"LeftInHandMiddle"],           #
    [149,"LeftInHandRing"],           #
    [150,"LeftInHandPinky"],           #

    [151,"LeftInHandExtraFinger"],           #
    [152,"RightInHandThumb"],           #
    [153,"RightInHandIndex"],           #
    [154,"RightInHandMiddle"],           #
    [155,"RightInHandRing"],           #
    [156,"RightInHandPinky"],           #
    [157,"RightInHandExtraFinger"],           #
    [158,"LeftInFootThumb"],           #
    [159,"LeftInFootIndex"],           #
    [160,"LeftInFootMiddle"],           #
    
    [161,"LeftInFootRing"],           #
    [162,"LeftInFootPinky"],           #
    [163,"LeftInFootExtraFinger"],           #
    [164,"RightInFootThumb"],           #
    [165,"RightInFootIndex"],           #
    [166,"RightInFootMiddle"],           #
    [167,"RightInFootRing"],           #
    [168,"RightInFootPinky"],           #
    [169,"RightInFootExtraFinger"],           #
    [170,"LeftShoulderExtra"],           #
    
    [171,"RightShoulderExtra"],           #
    [172,"LeafLeftUpLegRoll1"],           #
    [173,"LeafLeftLegRoll1"],           #
    [174,"LeafRightUpLegRoll1"],           #
    [175,"LeafRightLegRoll1"],           #
    [176,"LeafLeftArmRoll1"],           #
    [177,"LeafLeftForeArmRoll1"],           #
    [178,"LeafRightArmRoll1"],           #
    [179,"LeafRightForeArmRoll1"],           #
    [180,"LeafLeftUpLegRoll2"],           #
    
    [181,"LeafLeftLegRoll2"],           #
    [182,"LeafRightUpLegRoll2"],           #
    [183,"LeafRightLegRoll2"],           #
    [184,"LeafLeftArmRoll2"],           #
    [185,"LeafLeftForeArmRoll2"],           #
    [186,"LeafRightArmRoll2"],           #
    [187,"LeafRightForeArmRoll2"],           #
    [188,"LeafLeftUpLegRoll3"],           #
    [189,"LeafLeftLegRoll3"],           #
    [190,"LeafRightUpLegRoll3"],           #
    
    [191,"LeafRightLegRoll3"],           #
    [192,"LeafLeftArmRoll3"],           #
    [193,"LeafLeftForeArmRoll3"],           #
    [194,"LeafRightArmRoll3"],           #
    [195,"LeafRightForeArmRoll3"],           #
    [196,"LeafLeftUpLegRoll4"],           #
    [197,"LeafLeftLegRoll4"],           #
    [198,"LeafRightUpLegRoll4"],           #
    [199,"LeafRightLegRoll4"],           #
    [200,"LeafLeftArmRoll4"],           #
    
    [201,"LeafLeftForeArmRoll4"],           #
    [202,"LeafRightArmRoll4"],           #
    [203,"LeafRightForeArmRoll4"],           #
    [204,"LeafLeftUpLegRoll5"],           #
    [205,"LeafLeftLegRoll5"],           #
    [206,"LeafRightUpLegRoll5"],           #
    [207,"LeafRightLegRoll5"],           #
    [208,"LeafLeftArmRoll5"],           #
    [209,"LeafLeftForeArmRoll5"],           #
    [210,"LeafRightArmRoll5"],           #
    
    [211,"LeafRightForeArmRoll5"],           #
    ]

HIK = 'HIK'
for num, jnt in jnt2HIK_list:
    if pm.objExists(jnt):
        pm.mel.setCharacterObject(jnt, HIK, num, 0)


# 정의 롹1
pm.mel.hikToggleLockDefinition()

# 정의 롹2
pm.mel.HIKCharacterControlsTool() # 업데이트
lockState = pm.mel.hikIsDefinitionLocked('HIK')
pm.mel.hikCharacterLock('HIK',not lockState,1)
pm.mel.hikUpdateDefinitionButtonState() # Update the button states

#-----------------------
#
# 모션 적용
# 
#-----------------------
# 조작중인 HIK 캐릭터 
hikDef = pm.mel.hikGetCurrentCharacter()

# 변경
pm.mel.hikSetCurrentCharacter("MocapExample")
pm.mel.hikSetCurrentCharacter("HIK")
pm.mel.HIKCharacterControlsTool()

# 모캡데이터 연결
pm.mel.mayaHIKsetCharacterInput( "HIK", "MocapExample" )
pm.mel.hikUpdateCurrentCharacterFromScene()
pm.mel.HIKCharacterControlsTool()

