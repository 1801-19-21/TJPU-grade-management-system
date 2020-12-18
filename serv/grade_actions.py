from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/grade/add')
async def action_grade_add(request):
    params = await request.post()
    student_sn = params.get("student_sn")
    course_sn = params.get("course_sn")
    term=params.get("term")
    grade = params.get("grade")

    if student_sn is None or course_sn is None or grade is None:
        return web.HTTPBadRequest(text="student_sn, course_sn, grade must be required")

    try:
        student_sn = int(student_sn)
        course_sn = int(course_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO course_grade (student_sn, course_sn, term,grade) 
            VALUES ( %(student_sn)s, %(course_sn)s,%(term)s, %(grade)s)
            """, dict(student_sn=student_sn, course_sn=course_sn,term=term, grade=grade))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生的课程成绩",
            "return": "/grade"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location="/grade")


@web_routes.post('/action/grade/edit/{student_sn}/{course_sn}/{term}')
async def edit_grade_action(request):
    student_sn = request.match_info.get("student_sn")
    course_sn = request.match_info.get("course_sn")
    if student_sn is None or course_sn is None:
        return web.HTTPBadRequest(text="student_sn, course_sn, must be required")

    params = await request.post()
    grade = params.get("grade")

    try:
        student_sn = int(student_sn)
        course_sn = int(course_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE course_grade SET grade=%(grade)s
        WHERE student_sn = %(student_sn)s AND course_sn = %(course_sn)s
        """, dict(student_sn=student_sn, course_sn=course_sn,grade=grade))

    return web.HTTPFound(location="/grade")


@web_routes.post('/action/grade/delete/{student_sn}/{course_sn}/{term}')
def delete_grade_action(request):
    student_sn = request.match_info.get("student_sn")
    course_sn = request.match_info.get("course_sn")
    if student_sn is None or course_sn is None:
        return web.HTTPBadRequest(text="student_sn, course_sn, must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM course_grade
            WHERE student_sn = %(student_sn)s AND course_sn = %(course_sn)s
        """, dict(student_sn=student_sn, course_sn=course_sn))

    return web.HTTPFound(location="/grade")
