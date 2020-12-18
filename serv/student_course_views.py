from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/student_course")
async def view_list_student_course(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS student_sn, name as student_name  FROM student ORDER BY sn
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS course_sn, name as course_name  FROM course ORDER BY sn
        """)
        courses = list(db)


        db.execute("""
        SELECT schedule_sn,course_sn, term, date, time, site   
        FROM course_schedule as cs
             
        """)
        schedules = list(db)


        db.execute("""
        SELECT sc.student_sn, sc.schedule_sn, 
            s.name as student_name, 
            c.name as course_name,
            cs.term,
            cs.date,
            cs.time,
            cs.site
            
        FROM student_course as sc
            INNER JOIN student as s ON sc.student_sn = s.sn
            INNER JOIN course_schedule as cs  ON sc.schedule_sn = cs.schedule_sn
            INNER JOIN course as c ON cs.course_sn = c.sn
        ORDER BY student_sn, schedule_sn;
        """)

        items = list(db)

    return render_html(request, 'student_course_list.html',
                       students=students,
                       schedules=schedules,
                       courses=courses,
                       items=items)




@web_routes.get("/student_course/delete/{student_sn}/{course_sn}")
def student_course_edit(request):
    student_sn = request.match_info.get("student_sn")
    schedule_sn = request.match_info.get("schedule_sn")
    

    with db_block() as db:
        db.execute("""
        SELECT sc.student_sn, sc.schedule_sn, 
            s.name as student_name, 
            c.name as course_name,
            cs.term,
            cs.date,
            cs.time,
            cs.site
            
        FROM student_course as sc
            INNER JOIN student as s ON sc.student_sn = s.sn
            INNER JOIN course_schedule as cs  ON sc.schedule_sn = cs.schedule_sn
            INNER JOIN course as c ON cs.course_sn = c.sn

        
        """, dict(student_sn=student_sn, schedule_sn=schedule_sn))

        record = db.fetch_first()
    
    
        


    return render_html(request, 'student_course_edit.html', record=record,)
