import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/course/list")
async def get_course_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS course_sn, no AS course_no, name AS course_name, teacher FROM course
        """)
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.get("/api/course/{course_sn:\d+}")
async def get_course_profile(request):
    course_sn = request.match_info.get("course_sn")

    with db_block() as db:
        db.execute("""
        SELECT sn AS course_sn, no AS course_no, name AS course_name, teacher FROM course
        WHERE sn=%(course_sn)s
        """, dict(course_sn=course_sn))
        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such course: course_sn={course_sn}")

    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.post("/api/course")
async def new_course(request):
    course = await request.json()

    with db_block() as db:
        db.execute("""
        INSERT INTO course (no, name, teacher)
        VALUES(%(course_no)s, %(course_name)s, %(teacher)s) RETURNING sn;
        """, course)
        record = db.fetch_first()

        course["course_sn"] = record.sn
    
    print(course)

    return web.Response(text=json_dumps(course), content_type="application/json")


@web_routes.put("/api/course/{course_sn:\d+}")
async def update_course(request):
    course_sn = request.match_info.get("course_sn")

    course = await request.json()
    

    with db_block() as db:
        db.execute("""
        UPDATE course SET
            no=%(course_no)s, name=%(course_name)s, teacher=%(teacher)s
        WHERE sn=%(course_sn)s;
        """, course)

    return web.Response(text=json_dumps(course), content_type="application/json")


@web_routes.delete("/api/course/{course_sn:\d+}")
async def delete_course(request):
    course_sn = request.match_info.get("course_sn")

    with db_block() as db:
        db.execute("""
        DELETE FROM course WHERE sn=%(course_sn)s;
        """, dict(course_sn=course_sn))

    return web.Response(text="", content_type="text/plain")
