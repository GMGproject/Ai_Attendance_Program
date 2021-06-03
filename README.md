## 안면인식 기능을 활용한 자동 출결 시스템
우송대학교 게임멀티미디어 전공 졸업작품입니다.


역할|이름|학과|학번|비고
:---|:---|:---|:---|:---
팀장 & 모델개발|김대정|게임멀티미디어 전공|201610560|
팀원 & 프론트엔드|정준수|게임멀티미디어 학과|201510581|
팀원 & 백엔드|정찬묵|게임멀티미디어 전공|201610587|


### 제작 개요
1. 제작 기간 : 2021/05/25 ~ 2021/06/10
2. 제작 인원 : 3명

### 개발 환경
```
OS   : Windows 10
Tool : Visual Code
Lang : Pyhton 3.8
DB   : MySQL 8.0.23
```

### 패키지 설치
```
# 먼저 dlib을 설치해야 requirements 설치시 패키지 충돌 오류가 없습니다.
conda install -c conda-forge dlib
pip install -r requirements.txt
```

### 사용 방법
```
#Client 실행 방법
python c_main.py --host "host" --port port --cam camnumber

#Server 실행 방법
python s_main.py --host "host" --port
```


### 참고 논문
 - [이순기. "안면인식 기술을 이용한 출입통제 단말 장치 개발." 국내석사학위논문 경일대학교 대학원, 2013. 경상북도](http://kiu.dcollection.net/public_resource/pdf/000001624617_20210603222714.pdf)
 - [W. Liu, et al, SSD: Single Shot Multibox Detector, 2016, ECCV](https://arxiv.org/pdf/1512.02325.pdf)

### 참고 Github
 - KNN알고리즘 참고 : [ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)

