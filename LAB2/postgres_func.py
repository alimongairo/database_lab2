import psycopg2
import psycopg2.extras
from psycopg2 import Error
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class myDB():
    def __init__(self,db):
        try:
            self.connection = psycopg2.connect(user="kek",
                                          password="12345",
                                          host="127.0.0.1",
                                          port="5432",
                                          database=db)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

        except (Exception, Error) as error:
            h = 2
#            print("Ошибка при работе с PostgreSQL", error)
        finally:
            h = 1
#            print("Соединение с PostgreSQL закрыто")

    def query(self, q):
        self.cursor.execute(q)
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def callproc(self, func, params):
        return self.cursor.callproc(func, params)


def create_db():
    db = myDB('tmp')
    db.query('DROP DATABASE IF EXISTS lab2')
    db.query('CREATE DATABASE lab2')
    db.connection.close()

    db = myDB('lab2')

    teachers_table_q = '''CREATE TABLE teachers (
        id  SERIAL ,
        surname text NOT NULL,
        name text NOT NULL,
        PRIMARY KEY (id)
        );
        INSERT INTO teachers (name,surname) VALUES
        ('Стас','Клюков'),
        ('Наталья','Уланова');'''

    students_table_q = '''CREATE TABLE students (
        id  SERIAL ,
        surname text NOT NULL,
        name text NOT NULL,
        phone char(11)
        CHECK (phone LIKE '8%'),
        PRIMARY KEY (id)
        );
        CREATE INDEX name_ind ON students (name);'''

    attend_table_q = '''CREATE TABLE attendance (
        id  SERIAL ,
        class_id int NOT NULL UNIQUE,
        student_id int NOT NULL UNIQUE,
        PRIMARY KEY (id)
        );'''

    lessons_table_q = '''CREATE TABLE lessons (
        id  SERIAL ,
        max_num int NOT NULL,
        CHECK (max_num > 0),
        style text NOT NULL,
        class_num char(1),
        CHECK (class_num IN ('1','2','3','4','5')),
        PRIMARY KEY (id)
        );
        INSERT INTO lessons (max_num, style, class_num) VALUES
        ('7','Хип-хоп', '2'),
        ('12','Вог', '4'),
        ('1','Контемпорари', '3');'''

    timetable_table_q = '''CREATE TABLE timetable (
        id  SERIAL ,
        date date NOT NULL,
        time time NOT NULL,
        teacher_id int NOT NULL UNIQUE,
        lesson_id int NOT NULL UNIQUE,
        PRIMARY KEY (id),
        FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE
        );
        INSERT INTO timetable (date, time, teacher_id, lesson_id) VALUES
        ('2021-12-3','18:00', '1', '1'),
        ('2021-12-3','19:00', '2', '2');'''
        #CREATE OR REPLACE FUNCTION trigger()
        #RETURNS trigger AS $$
        #    BEGIN
        #        NEW.stud_amount = COUNT (*) FROM attendance
        #        WHERE attendance.class_id = timetable.id;
        #        RETURN NEW;
        #    END;
        #$$ LANGUAGE plpgsql;
        #CREATE TRIGGER amount_update
        #BEFORE INSERT OR UPDATE OR DELETE ON attendance FOR EACH ROW
        #EXECUTE PROCEDURE trigger();

    db.query(teachers_table_q)
    db.query(students_table_q)
    db.query(attend_table_q)
    db.query(lessons_table_q)
    db.query(timetable_table_q)

    show_teachers_table_f = '''
        CREATE OR REPLACE FUNCTION prog_show_teachers()
        RETURNS TABLE(id int, surname text, name text) AS $$
            BEGIN
            RETURN QUERY
            SELECT * FROM teachers;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(show_teachers_table_f)

    show_students_table_f = '''
        CREATE OR REPLACE FUNCTION prog_show_students()
        RETURNS TABLE(id int, surname text, name text, phone char(3)) AS $$
            BEGIN
            RETURN QUERY
            SELECT * FROM students ORDER BY id;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(show_students_table_f)

    show_attend_table_f = '''
        CREATE OR REPLACE FUNCTION prog_show_attendance()
        RETURNS TABLE(id int, date_ date, time_ time, name text, surname text) AS $$
            BEGIN
            RETURN QUERY
            SELECT attendance.id, date, time, students.name, students.surname FROM attendance
            LEFT JOIN students ON students.id = attendance.student_id
            LEFT JOIN timetable ON timetable.id = attendance.class_id;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(show_attend_table_f)

    show_lessons_table_f = '''
        CREATE OR REPLACE FUNCTION prog_show_lessons()
        RETURNS TABLE(id int, max_num int, style text, class_num char(1)) AS $$
            BEGIN
            RETURN QUERY
            SELECT * FROM lessons;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(show_lessons_table_f)

    show_timetable_table_f = '''
        CREATE OR REPLACE FUNCTION prog_show_timetable()
        RETURNS TABLE(id int, les_date date, les_time time, teacher_id int, lesson_id int) AS $$
            BEGIN
            RETURN QUERY
            SELECT * FROM timetable;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(show_timetable_table_f)

    add_student_f = '''
                CREATE OR REPLACE FUNCTION prog_add_student(aname text, asurname text, aphone char(11))
                RETURNS int AS $$
                    DECLARE
                        iid int;
                    BEGIN
                    INSERT INTO students (name,surname,phone) VALUES (aname,asurname,aphone) RETURNING id INTO iid;
                    RETURN
                    iid;
                    END;
                $$ LANGUAGE plpgsql;
                '''
    db.query(add_student_f)

    get_student_by_id_f = '''
            CREATE OR REPLACE FUNCTION prog_get_student_by_id(s_id int)
            RETURNS TABLE(id int, surname text, name text, phone char(3)) AS $$
                BEGIN
                RETURN QUERY
                SELECT * FROM students WHERE students.id = s_id;
                END;
            $$ LANGUAGE plpgsql;
            '''
    db.query(get_student_by_id_f)

    edit_student_by_id_f = '''
            CREATE OR REPLACE FUNCTION prog_edit_student(aid int, aname text, asurname text, aphone char(11))
                RETURNS int AS $$
                    BEGIN
                    UPDATE students SET name=aname,surname=asurname,phone=aphone WHERE id = aid;
                    RETURN aid;
                    END;
                $$ LANGUAGE plpgsql;
                '''
    db.query(edit_student_by_id_f)

    add_attend_f = '''
            CREATE OR REPLACE FUNCTION prog_add_attend(cls_id int, st_id int)
            RETURNS int AS $$
                DECLARE
                    iid int;
                BEGIN
                INSERT INTO attendance (class_id, student_id) VALUES (cls_id, st_id) RETURNING id INTO iid;
                RETURN
                iid;
                END;
            $$ LANGUAGE plpgsql;
            '''
    db.query(add_attend_f)

    delete_attend_by_id_f = '''
            CREATE OR REPLACE FUNCTION prog_delete_attendance(atd_id int)
                RETURNS int AS $$
                    BEGIN
                    DELETE FROM attendance WHERE id = atd_id;
                    RETURN atd_id;
                    END;
                $$ LANGUAGE plpgsql;
                '''
    db.query(delete_attend_by_id_f)

    get_student_by_name_f = '''
        CREATE OR REPLACE FUNCTION prog_get_student_by_name(st_surname text)
        RETURNS TABLE(id int, surname text, name text, phone char(3)) AS $$
            BEGIN
            RETURN QUERY
            SELECT * FROM students WHERE students.surname = st_surname;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(get_student_by_name_f)

    delete_student_by_name_f = '''
        CREATE OR REPLACE FUNCTION prog_delete_student_by_name(st_surname text)
            RETURNS text AS $$
                BEGIN
                DELETE FROM students WHERE surname = st_surname;
                RETURN st_surname;
                END;
            $$ LANGUAGE plpgsql;
            '''
    db.query(delete_student_by_name_f)

    get_all_students_by_name = '''
        CREATE OR REPLACE FUNCTION prog_get_all_students_by_name(st_surname text)
        RETURNS TABLE(id int, surname text, name text, phone char(3)) AS $$
            BEGIN
            RETURN QUERY
            SELECT * FROM students WHERE students.surname = st_surname;
            END;
        $$ LANGUAGE plpgsql;
        '''
    db.query(get_all_students_by_name)



def delete_db():
    db = myDB('tmp')
    db.query('DROP DATABASE lab2')


def delete_table(name):
    db = myDB('lab2')
    db.query('TRUNCATE TABLE {}'.format(name))


def add_student(name, surname, phone):
    db = myDB('lab2')
    db.callproc('prog_add_student', [name, surname, phone])


def add_attendance(stud_id, class_id):
    db = myDB('lab2')
    db.callproc('prog_add_attend', [class_id, stud_id])


def delete_attendance(stud_id):
    db = myDB('lab2')
    db.callproc('prog_delete_attendance', [stud_id])


def get_stud_by_id(id):
    db = myDB('lab2')
    db.callproc('prog_get_student_by_id', [id])
    res = db.fetchall()
    return res[0]


def edit_stud_by_id(id, name, surname, phone):
    db = myDB('lab2')
    db.callproc('prog_edit_student', [id, name, surname, phone])
    res = db.fetchall()
    return res[0]


def get_student_by_name(surname):
    db = myDB('lab2')
    db.callproc('prog_get_student_by_name', [surname])
    res = db.fetchall()
    return res[0][1]


def delete_student_by_name(surname):
    db = myDB('lab2')
    db.callproc('prog_delete_student_by_name', [surname])
    res = db.fetchall()
    return res[0]


def search_students_by_name(surname):
    db = myDB('lab2')
    db.callproc('prog_get_all_students_by_name', [surname])
    res = db.fetchall()
    return res


def get_teachers():
    db = myDB('lab2')
    db.callproc('prog_show_teachers', [])
    res = db.fetchall()
    return res


def get_students():
    db = myDB('lab2')
    db.callproc('prog_show_students', [])
    res = db.fetchall()
    return res


def get_attendance():
    db = myDB('lab2')
    db.callproc('prog_show_attendance', [])
    res = db.fetchall()
    return res


def get_lessons():
    db = myDB('lab2')
    db.callproc('prog_show_lessons', [])
    res = db.fetchall()
    return res


def get_timetable():
    db = myDB('lab2')
    db.callproc('prog_show_timetable', [])
    res = db.fetchall()
    return res
