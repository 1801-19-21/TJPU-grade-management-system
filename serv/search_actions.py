from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes, render_html


@web_routes.post('/action/search/edit_stu')
async def search_edit_stu(request):
    
    params = await request.post()
    params = dict(params)
    print(params)
    student_sn = params['student_sn']
    with db_block() as db:
        db.execute("""
        SELECT g.student_sn, g.course_sn,
            s.name as student_name, 
            c.name as course_name, 
            g.term,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.student_sn = s.sn
            INNER JOIN course as c  ON g.course_sn = c.sn
        WHERE student_sn = %(student_sn)s ;
        """, dict(student_sn=student_sn))

        items = list(db)

    return render_html(request, 'search_edit.html', items=items)

@web_routes.post('/action/search/edit_com')
async def search_edit_stu(request):
    course_sn = request.match_info.get("course_sn")
    term = request.match_info.get("term")
    

    params = await request.post()
    params = dict(params)
    print(params)
    course_sn = params['course_sn']
    term = params['term']

    

    with db_block() as db:
        db.execute("""
        SELECT g.student_sn, g.course_sn,
            s.name as student_name, 
            c.name as course_name, 
            g.term,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.student_sn = s.sn
            INNER JOIN course as c  ON g.course_sn = c.sn
        WHERE course_sn = %(course_sn)s AND term = %(term)s  ;
        """, dict(course_sn=course_sn,term=term))

        items = list(db)

    return render_html(request, 'search_edit.html', items=items)



