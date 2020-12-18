from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode
from .config import db_block, web_routes, render_html


@web_routes.get("/search")
async def view_lists_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS student_sn, name as student_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS course_sn, name as course_name FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT g.student_sn, g.course_sn, 
            s.name as student_name, 
            c.name as course_name, 
            g,term,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.student_sn = s.sn
            INNER JOIN course as c  ON g.course_sn = c.sn
        ORDER BY student_sn, course_sn;
        """)

        items = list(db)

    return render_html(request, 'search_list.html',
                       students=students,
                       courses=courses,
                       items=items)










   
       
    

    




   