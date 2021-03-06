import os
import pymel.core as pm

mcCharFile = 'D:/Users/kyuho_choi/Desktop/MC/MC.ma'
jnts = []

def makeMCAssets(sourceFolderPath, outputFolderPath, getAnimClip=True, getPlayblast=True):
    # sourceFolderPath = 'Z:/2016_Dark_Avenger3/B_production/scene/animation/motioncapture/FBX/choice/161227'
    # outputFolderPath = 'D:/Users/kyuho_choi/Desktop/motionCapture'

    # 입력값 검증
    sourceFolderPath = sourceFolderPath.replace('\\','/')
    outputFolderPath = outputFolderPath.replace('\\','/')

    if sourceFolderPath[-1] == '/': sourceFolderPath = sourceFolderPath[:-1]
    if outputFolderPath[-1] == '/': outputFolderPath = outputFolderPath[:-1]

    if not os.path.exists(sourceFolderPath):
        raise AttributeError(u'소스 폴더가 존재하지 않습니다.') 

    # 처리할 모캡파일 리스트 확보
    sourceFiles = []
    for item in os.listdir(sourceFolderPath):
        ext = os.path.splitext(item)[-1]
        if ext in ['.fbx','.mb','.ma']:
            sourceFiles.append( sourceFolderPath+'/'+item)

    # 처리결과 저장할 곳 세팅 
    mocapInputFolder    = outputFolderPath + '/inputFiles'   
    animClipFolder      = outputFolderPath + '/animClip'
    motionCaptureFolder = outputFolderPath + '/motionCapture'
    previewFolder       = outputFolderPath + '/preview'
    for path in [mocapInputFolder, animClipFolder, motionCaptureFolder, previewFolder]:
        if not os.path.exists(path):
            os.makedirs(path)

    # 시작~
    for mocapSrcFile in sourceFiles:
        batch(mocapSrcFile)


def batch(mocapSrcFile):



#mcCharFile = 'D:/Users/kyuho_choi/Desktop/MC/MC.ma'
#jnts = []
sampleJntName = 'Spine'

#mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\scene\animation\motioncapture\FBX\choice\161227\Etc_orc_attacked_fall_01.fbx'
mocapSrcFile = r'Z:\2016_Dark_Avenger3\B_production\scene\animation\motioncapture\FBX\choice\161227\D_01_KO_Fight_knight_look_M_02.fbx'
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

# 새파일
pm.newFile( force=True )

# 씬 이름
sceneName = pm.mel.basenameEx( mocapSrcFile )

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
        
charSets = []
animClips = []
for sourceNamespace, prefix in zip( mocapNamespaces, charPrefixs ):
    #sourceNamespace = mocapNamespaces[0]
    #prefix = charPrefixs[0]
    
    # 캐릭터 수량에 따른 조정 내용
    importOpt = {"returnNewNodes":True }
    prefix_ = ''
    subfix_ = ''
    if len(mocapNamespaces)>1 :
        importOpt = {"returnNewNodes":True, "renameAll":True, "renamingPrefix":prefix}
        prefix_ = prefix + '_'
        subfix_ = '_' + prefix
    
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
charSet = pm.ls( newNodes, type='character')[0]
charSets.append( charSet )

# 애니메이션 클립 생성
animClip = pm.clip(charSet, name='animClip', scheduleClip=True, allAbsolute=True, animCurveRange=True)[0]
animClip = pm.PyNode( animClip )
animClipName = sceneName
if prefix:
    animClipName = sceneName + subfix_ 
animClip.rename( pm.mel.formValidObjectName( animClipName ) )
animClips.append(animClip)
