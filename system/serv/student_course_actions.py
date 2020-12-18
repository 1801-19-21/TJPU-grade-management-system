from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/student_course/add')
async def student_course_add(request):
    params = await request.post()
    student_sn = params.get("student_sn")
    schedule_sn = params.get("schedule_sn")
    term = params.get("term")
    
    with db_block() as db:
            db.execute("""
            INSERT INTO student_course (student_sn, schedule_sn) 
            VALUES ( %(student_sn)s, %(schedule_sn)s)
            """, dict(student_sn=student_sn, schedule_sn = schedule_sn))
    

    return web.HTTPFound(location="/student_course")

@web_routes.post('/action/student_course/delete/{student_sn}/{schedule_sn}')
async def action_student_course_delete(request):
   
    student_sn = request.match_info.get("student_sn")
    schedule_sn = request.match_info.get("schedule_sn")
 
    with db_block() as db:
         db.execute("""
        DELETE FROM student_course
            WHERE student_sn = %(student_sn)s AND schedule_sn = %(schedule_sn)s
        """, dict(student_sn=student_sn, schedule_sn = schedule_sn))
    return web.HTTPFound(location="/student_course")