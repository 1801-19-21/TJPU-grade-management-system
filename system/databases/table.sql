DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student  (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --学号
    name     TEXT,        --姓名
    gender   CHAR(1),     --性别(F/M/O)
    college  TEXT,      --学院
    major    TEXT,        --专业
    class_name    TEXT,        --班级名称
    PRIMARY KEY(sn)
);

-- 给sn创建一个自增序号
CREATE SEQUENCE seq_student_sn 
    START 10000 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
-- 学号唯一
CREATE UNIQUE INDEX idx_student_no ON student(no);


-- === 课程
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course  (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --课程号
    name     TEXT,        --课程名称
    teacher  TEXT,        --教师姓名
    PRIMARY KEY(sn)
);
CREATE SEQUENCE seq_course_sn 
    START 10000 INCREMENT 1 OWNED BY course.sn;
ALTER TABLE course ALTER sn 
    SET DEFAULT nextval('seq_course_sn');
CREATE UNIQUE INDEX idx_course_no ON course(no);




-- ===课程计划
DROP TABLE IF EXISTS course_schedule;
CREATE TABLE IF NOT EXISTS course_schedule  (
    schedule_sn INTEGER,  --课程计划序号
    course_sn INTEGER,    -- 课程序号
    term    TEXT,     -- 学期
    date TEXT,    -- 日期（周几）
    time TEXT,    -- 时间（第几节）
    site TEXT,    -- 地点
    PRIMARY KEY(schedule_sn)
);

CREATE SEQUENCE seq_schedule_sn 
    START 10000 INCREMENT 1 OWNED BY course_schedule.schedule_sn;
ALTER TABLE course_schedule ALTER schedule_sn 
    SET DEFAULT nextval('seq_schedule_sn');
-- 学号唯一


-- ===学生选课表
DROP TABLE IF EXISTS student_course;
CREATE TABLE IF NOT EXISTS student_course  (
    student_sn INTEGER,    -- 学生序号
    schedule_sn INTEGER,     -- 课程计划序号
    PRIMARY KEY(student_sn,schedule_sn)
);
ALTER TABLE student_course drop CONSTRAINT student_course_pkey;



-- ===学生成绩表
DROP TABLE IF EXISTS course_grade;
CREATE TABLE IF NOT EXISTS course_grade  (
    student_sn INTEGER,    -- 学生序号
    course_sn INTEGER,     -- 课程序号
    term     TEXT,         -- 学期
    grade  NUMERIC(5,2),   -- 最终成绩
    PRIMARY KEY(student_sn, course_sn, term)
);

ALTER TABLE course_grade ALTER COLUMN term TYPE TEXT;
ALTER TABLE course_grade drop CONSTRAINT course_grade_pkey;
ALTER TABLE course_grade add PRIMARY KEY(student_sn, course_sn);

ALTER TABLE course_schedule 
    ADD CONSTRAINT course_sn_fk FOREIGN KEY (course_sn) REFERENCES course(sn);
ALTER TABLE course_grade 
    ADD CONSTRAINT student_sn_fk FOREIGN KEY (student_sn) REFERENCES student(sn);
ALTER TABLE course_grade 
    ADD CONSTRAINT course_sn_fk FOREIGN KEY (course_sn) REFERENCES course(sn);
ALTER TABLE student_course 
    ADD  FOREIGN KEY (student_sn) REFERENCES student(sn);
ALTER TABLE course_grade DROP CONSTRAINT course_grade_student_sn_fkey;
ALTER TABLE student_course 
    ADD CONSTRAINT schedule_sn_fk FOREIGN KEY (schedule_sn) REFERENCES course_schedule;