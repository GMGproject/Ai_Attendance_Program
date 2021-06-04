import datetime

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

