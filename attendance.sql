
CREATE DATABASE AttendanceProgram;      # DB 만들때
DROP DATABASE AttendanceProgram;        # DB 지울때

USE AttendanceProgram;

# TABLE 만들때
CREATE TABLE stu_info (
  studentID INTEGER UNSIGNED NOT NULL,  
  studentName VARCHAR(45) NOT NULL,     
  PRIMARY KEY(studentID)
);

CREATE TABLE lecture_info(
  lectureID INTEGER UNSIGNED NOT NULL,  # 강의 번호
  lectureName VARCHAR(45) NOT NULL,     # 강의 이름
  PRIMARY KEY(lectureID)
);

CREATE TABLE attend_info (
  attendID INTEGER UNSIGNED NOT NULL
                      AUTO_INCREMENT,   # 출결 인덱스
  studentID INTEGER UNSIGNED NOT NULL,  # 학생 학번
  attendanceDate DATE NOT NULL,         # 출석 날짜
  attendanceTime TIME NULL,             # 출석 시간
  isAttendance BOOLEAN NOT NULL,        # 출석 여부
  lectureID INTEGER UNSIGNED NULL,      # 출석 강의 번호
  PRIMARY KEY(attendID),
  FOREIGN KEY(studentID) 
  REFERENCES stu_info(studentID),
  FOREIGN KEY(lectureID) 
  REFERENCES lecture_info(lectureID)
);

# 값 추가할때
INSERT INTO stu_info (studentID, studentName) VALUES (201610560, 'Daejeong');
INSERT INTO stu_info (studentID, studentName) VALUES (201610587, 'Chanmuk');
INSERT INTO stu_info (studentID, studentName) VALUES (201510581, 'Junsu');

INSERT INTO lecture_info (lectureID, lectureName) VALUES (1, 'Programming');

# isAttendance 1 = True, 0 = False
INSERT INTO attend_info (studentID, attendanceDate, isAttendance, lectureID) VALUES (201610560, '2021-06-08', 0, 1);
INSERT INTO attend_info (studentID, attendanceDate, isAttendance, lectureID) VALUES (201610587, '2021-06-08', 0, 1);
INSERT INTO attend_info (studentID, attendanceDate, isAttendance, lectureID) VALUES (201510581, '2021-06-08', 0, 1);

# 값 변경할때 attendance False -> True
UPDATE attend_info 
SET isAttendance = 0, attendanceTime = NULL 
WHERE studentID = (SELECT studentID FROM stu_info WHERE studentName = 'Daejeong')
  AND attendanceDate = "2021-06-08";

SELECT * FROM stu_info;
SELECT * FROM attend_info;

SELECT isAttendance, studentID, (SELECT studentName FROM stu_info s WHERE s.studentID = a.studentID) as studentName 
FROM attend_info a 
WHERE attendanceDate = "2021-06-08"; 

