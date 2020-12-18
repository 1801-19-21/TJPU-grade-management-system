from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/schedule/add')
async def action_schedule_add(request):
    params = await request.post()
    print(params)
    schedule_sn = params.get("schedule_sn")
    course_sn = params.get("course_sn")
    term = params.get("term")
    date = params.get("date")
    time = params.get("time")
    site = params.get("site")

    try:
        schedule_sn = int(schedule_sn)
        course_sn = int(course_sn)
        
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO course_schedule (schedule_sn, course_sn, term, date, time, site) 
            VALUES (  %(schedule_sn)s, %(course_sn)s, %(term)s, %(date)s, %(time)s, %(site)s)
            """, dict(schedule_sn=schedule_sn, course_sn=course_sn, term=term, date=date, time=time, site=site))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该课程计划",
            "return": "/schedule"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此课程计划: {ex}")

    return web.HTTPFound(location="/schedule")


#@web_routes.post('/action/schedule/edit/{schedule_sn}/{course_sn}/{term}/{date}/{time}/{site}')
@web_routes.post('/action/schedule/edit/{schedule_sn}')
async def edit_schedule_action(request):
    schedule_sn = request.match_info.get("schedule_sn")
    if schedule_sn is None:
        return web.HTTPBadRequest(text="schedule_sn must be required")

    params = await request.post()
    print(params)
    course_sn= params.get("course_sn")
    term = params.get("term")
    date = params.get("date")
    time = params.get("time")
    site = params.get("site")
    

    try:
        course_sn = int(course_sn)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE course_schedule SET course_sn=%(course_sn)s, term=%(term)s, date=%(date)s, time=%(time)s, site=%(site)s
        WHERE schedule_sn = %(schedule_sn)s 
        """, dict(schedule_sn=schedule_sn, course_sn=course_sn, term=term, date=date, time=time, site=site))

    return web.HTTPFound(location="/schedule")


@web_routes.post('/action/schedule/delete/{schedule_sn}')

def delete_schedule_action(request):

    schedule_sn = request.match_info.get("schedule_sn")
    print(schedule_sn)
    print(123)
    if schedule_sn is None:
        return web.HTTPBadRequest(text="schedule_sn must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM course_schedule
            WHERE schedule_sn = %(schedule_sn)s
        """, dict(schedule_sn=schedule_sn ))
    print(123)
    return web.HTTPFound(location="/schedule")


