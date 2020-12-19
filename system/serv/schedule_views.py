from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/schedule")
async def view_list_schedules(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS course_sn, name as course_name FROM course ORDER BY name
        """)
        courses = list(db)
        db.execute("""
        SELECT  s.schedule_sn,
            s.course_sn, 
            c.name as schedule_name, 
            s.term,
            s.date,
            s.time,
            s.site
            
        FROM course_schedule as s
            INNER JOIN course as c  ON s.course_sn = c.sn
        ORDER BY  course_sn;
        """)

        items = list(db)

    return render_html(request, 'schedule_list.html',
                       courses=courses,
                       items=items)


#@web_routes.get('/schedule/edit/{schedule_sn}/{course_sn}/{term}/{date}/{time}/{site}')
@web_routes.get('/schedule/edit/{schedule_sn}')
def view_schedule_editor(request):
    schedule_sn = request.match_info.get("schedule_sn")
    if schedule_sn is None :
        return web.HTTPBadRequest(text=" schedule_sn must be required")

    with db_block() as db:
        db.execute("""
        SELECT course_sn,term,date,time,site FROM course_schedule
            WHERE  schedule_sn = %(schedule_sn)s ;
        """, dict(schedule_sn=schedule_sn))

        record = db.fetch_first()
    


    if record is None:
        return web.HTTPNotFound(text=f"no such course_sn,term,date,time,site:  schedule_sn={schedule_sn}")

    return render_html(request, "schedule_edit.html",
                       schedule_sn=schedule_sn,
                       course_sn=record.course_sn,
                       term=record.term,
                       date=record.date,
                       time=record.time,
                       site=record.site)


@web_routes.get("/schedule/delete/{schedule_sn}")
def schedule_deletion_dialog(request):
    schedule_sn = request.match_info.get("schedule_sn")
    if schedule_sn is None:
        return web.HTTPBadRequest(text="schedule_sn must be required")

    with db_block() as db:
        db.execute("""
        SELECT s.schedule_sn,
            s.course_sn,  
            s.term,
            s.date,
            s.time,
            s.site

        FROM course_schedule as s
            INNER JOIN course as c  ON s.course_sn = c.sn
        WHERE schedule_sn = %(schedule_sn)s ;
        """, dict(schedule_sn=schedule_sn))

        db.execute("""
        SELECT course_sn,term,date,time,site FROM course_schedule
            WHERE schedule_sn = %(schedule_sn)s ;
        """, dict(schedule_sn=schedule_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such course,term,date,time,site:  schedule_sn={record.course_sn}")

    return render_html(request, 'schedule_dialog_deletion.html', record=record,schedule_sn=schedule_sn)
