import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/student/list")
async def get_student_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS student_sn, no AS student_no, name AS student_name, gender, college, major,class_name FROM student
        """)
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.get("/api/student/{student_sn:\d+}")
async def get_student_profile(request):
    student_sn = request.match_info.get("student_sn")

    with db_block() as db:
        db.execute("""
        SELECT sn AS student_sn, no AS student_no, name AS student_name, gender, college, major,class_name FROM student
        WHERE sn=%(student_sn)s
        """, dict(student_sn=student_sn))
        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such student: student_sn={student_sn}")

    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.post("/api/student")
async def new_student(request):
    student = await request.json()

    with db_block() as db:
        db.execute("""
        INSERT INTO student (no, name, gender, college, major,class_name)
        VALUES(%(student_no)s, %(student_name)s, %(gender)s, %(college)s,%(major)s,%(class_name)s) RETURNING sn;
        """, student)
        record = db.fetch_first()

        student["student_sn"] = record.sn
    
    print(student)

    return web.Response(text=json_dumps(student), content_type="application/json")


@web_routes.put("/api/student/{student_sn:\d+}")
async def update_student(request):
    student_sn = request.match_info.get("student_sn")

    student = await request.json()
    

    with db_block() as db:
        db.execute("""
        UPDATE student SET
            no=%(student_no)s, name=%(student_name)s, gender=%(gender)s, college=%(college)s,major=%(major)s,class_name=%(class_name)s
        WHERE sn=%(student_sn)s;
        """, student)

    return web.Response(text=json_dumps(student), content_type="application/json")


@web_routes.delete("/api/student/{student_sn:\d+}")
async def delete_student(request):
    student_sn = request.match_info.get("student_sn")

    with db_block() as db:
        db.execute("""
        DELETE FROM student WHERE sn=%(student_sn)s;
        """, dict(student_sn=student_sn))

    return web.Response(text="", content_type="text/plain")
