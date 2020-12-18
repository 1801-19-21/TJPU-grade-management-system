DELETE FROM course_grade;
DELETE FROM student_course;
DELETE FROM course_schedule;
DELETE FROM course;
DELETE FROM student;




INSERT INTO student (sn, no, name, college, major, class_name)  VALUES
    (101, 'S001',  '张三', '经济与管理学院', '信息管理与信息系统','信息1801'),
    (102, 'S002',  '李四', '计算机学院', '物联网工程', '物联1801'), 
    (103, 'S003',  '王五', '经济与管理学院', '信息管理与信息系统','信息1801'),
    (104, 'S004',  '马六', '经济与管理学院', '财务管理', '财务1801');

INSERT INTO course (sn, no, name,teacher)  VALUES 
    (101, 'C01',  '高数', '陈老师'), 
    (102, 'C02',  '外语', '白老师'),
    (103, 'C03',  '线代', '刘老师');


INSERT INTO course_schedule (schedule_sn,course_sn, term, date, time, site)  VALUES 
    (101,101, '2020-2021第一学期', '周一', '第一大节', '第一公共教学楼A111'), 
    (102, 101, '2020-2021第二学期', '周二',  '第四大节', '第一公共教学楼A111'),
    (103, 102,'2020-2021第一学期',  '周三', '第二大节', '第一公共教学楼C210'),
    (104, 103, '2020-2021第一学期', '周四', '第一大节',   '软件园B208');

INSERT INTO student_course (student_sn, schedule_sn)  VALUES 
    (101,  101), 
    (102,  102),
    (103,  103),
    (102,  101);


DELETE from student_course ;

INSERT INTO course_grade (student_sn, course_sn,term, grade)  VALUES 
    (101, 101, '2020-2021第一学期', 91), 
    (102, 101, '2020-2021第一学期', 89),
    (103, 101, '2020-2021第一学期', 90),
    (104, 102, '2020-2021第一学期', 89),
    (101, 103, '2019-2020第二学期', 77);
