from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/grade")
async def view_list_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS student_sn, name as student_name  FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS course_sn, name as course_name  FROM course ORDER BY name
        """)
        courses = list(db)


        db.execute("""
        SELECT g.student_sn, g.course_sn, 
            s.name as student_name, 
            c.name as course_name, 
            g.term,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.student_sn = s.sn
            INNER JOIN course as c  ON g.course_sn = c.sn
        ORDER BY student_sn, course_sn;
        """)

        items = list(db)

    return render_html(request, 'grade_list.html',
                       students=students,
                       courses=courses,
                       items=items)


@web_routes.get('/grade/edit/{student_sn}/{course_sn}/{term}')
def view_grade_editor(request):
    student_sn = request.match_info.get("student_sn")
    course_sn = request.match_info.get("course_sn")
    if student_sn is None or course_sn is None :
        return web.HTTPBadRequest(text="student_sn, course_sn must be required")

    with db_block() as db:
        db.execute("""
        SELECT grade,term FROM course_grade
            WHERE student_sn = %(student_sn)s AND course_sn = %(course_sn)s ;
        """, dict(student_sn=student_sn, course_sn=course_sn))

        record = db.fetch_first()
    


    if record is None:
        return web.HTTPNotFound(text=f"no such grade,term: student_sn={student_sn}, course_sn={course_sn}")

    return render_html(request, "grade_edit.html",
                       student_sn=student_sn,
                       course_sn=course_sn,
                       term=record.term,
                       grade=record.grade)


@web_routes.get("/grade/delete/{student_sn}/{course_sn}/{term}")
def grade_deletion_dialog(request):
    student_sn = request.match_info.get("student_sn")
    course_sn = request.match_info.get("course_sn")
    if student_sn is None or course_sn is None:
        return web.HTTPBadRequest(text="student_sn, course_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT g.student_sn, g.course_sn,
            s.name as student_sn, 
            c.name as course_sn, 
            g.term,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.student_sn = s.sn
            INNER JOIN course as c  ON g.course_sn = c.sn
        WHERE student_sn = %(student_sn)s AND course_sn = %(course_sn)s;
        """, dict(student_sn=student_sn, course_sn=course_sn))
        db.execute("""
        SELECT term ,grade,student_sn, course_sn
        FROM course_grade
        WHERE student_sn = %(student_sn)s AND course_sn = %(course_sn)s ;
        """, dict(student_sn=student_sn, course_sn=course_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade,term: student_sn={student_sn}, course_sn={course_sn}")

    return render_html(request, 'grade_dialog_deletion.html', record=record)
