import datetime
import os

def chanegeAttendance(resultList):
    '''
    args discription
    resultList : List of recognized names
    '''
    resultName = max(resultList, key=resultList.count)
    
    if resultName == "Unknown":
        print("처음뵙는분이군요 반갑습니다.")
    else:        
        print("{}님 출석입니다.".format(resultName))

    return resultName

def getNowTime():
    '''
    return
    nowTime : 'HH:MM:SS'
    '''
    now = datetime.datetime.now()
    nowTime = now.strftime('%H:%M:%S')
    return nowTime

def getToday():
    '''
    return
    today : 'YYYY-mm-dd'
    '''
    today = datetime.date.today().strftime('%Y-%m-%d')
    return today

def makeFolder(path):
    '''
    args discription
    path : Path to create and check folder
    '''
    if not os.path.exists(path):
        os.makedirs(path)
        print("Create Folder : " + path)