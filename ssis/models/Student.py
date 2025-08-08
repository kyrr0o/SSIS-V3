from ..extension import mysql
# CREATE TABLE IF NOT EXISTS student (
# 	id VARCHAR(20) PRIMARY KEY,
#     firstname VARCHAR(255) NOT NULL,
#     lastname VARCHAR(255) NOT NULL,
#     course_code VARCHAR(20) NOT NULL,
#     year INT NOT NULL,
#     size ENUM('Male', 'Female', 'Other') NOT NULL,
#     FOREIGN KEY (course_code) REFERENCES course(code) ON DELETE CASCADE ON UPDATE CASCADE
# );


class Student():
    def __init__(self, id=None, firstname=None, lastname=None, course_code= None, year=None, gender=None, college = None, picture = None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.course_code = course_code
        self.year=year
        self.gender = gender
        self.college = college
        self.connection = mysql.connection
        self.picture = picture

    def add(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO student (id, firstname, lastname, course_code, year, gender, picture) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (self.id, self.firstname, self.lastname, self.course_code, self.year, self.gender, self.picture)
        )
        self.connection.commit()
        cursor.close()
    
    def update(self,id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE student SET id=%s, firstname=%s, lastname=%s, course_code=%s, year=%s, gender=%s , picture=%s WHERE id=%s" , (self.id, self.firstname,self.lastname, self.course_code, self.year, self.gender,self.picture,id))
        self.connection.commit()
        cursor.close()

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM student WHERE id=%s", (self.id,))
        self.connection.commit()
        cursor.close()

    @classmethod
    def search(cls, input, filter):
        cursor = mysql.connection.cursor()
        students = []
        if filter == "0":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.id LIKE %s OR student.firstname LIKE %s OR student.lastname LIKE %s OR student.course_code LIKE %s OR student.year LIKE %s OR student.gender LIKE %s", (f"%{input}%", f"%{input}%", f"%{input}%", f"%{input}%", f"%{input}%", f"%{input}%"))
        elif filter == "1":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.id LIKE %s", (f"%{input}%",))
        elif filter == "2":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.firstname LIKE %s", (f"%{input}%",))
        elif filter == "3":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.lastname LIKE %s", (f"%{input}%",))
        elif filter == "4":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.course_code LIKE %s", (f"%{input}%",))
        elif filter == "5":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.year LIKE %s", (f"%{input}%",))
        elif filter == "6":
            cursor.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code WHERE student.gender = %s", (f"{input}",))
        elif filter == "7":
            cursor.execute("""
                SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code, student.picture
                FROM student 
                INNER JOIN course ON student.course_code = course.code 
                INNER JOIN college ON course.college_code = college.code 
                WHERE college.name LIKE %s OR college.code LIKE %s
            """, (f"%{input}%", f"%{input}%"))

        for student_data in cursor.fetchall():
            student = Student(
                id=student_data[0],
                firstname=student_data[1],
                lastname=student_data[2],
                course_code=student_data[3],
                year=student_data[4],
                gender=student_data[5],
                college=student_data[6],
                picture=student_data[7]  
            )
            students.append(student)
        cursor.close()
        return students



    @classmethod
    def get_all(cls,table_name = 'student'):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code , student.picture FROM student INNER JOIN course ON student.course_code = course.code INNER JOIN college ON course.college_code = college.code ORDER BY student.id")
        student = []
        for student_data in cursor.fetchall():
            courses = Student(id = student_data[0] , firstname = student_data[1], lastname=student_data[2], course_code=student_data[3], year=student_data[4], gender=student_data[5], college=student_data[6], picture = student_data[7])
            student.append(courses)
        cursor.close()
        return student
    
    @classmethod
    def check_existing_id(cls,id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data is not None
    
    @classmethod
    def get_one(clr, id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
        student_data = cursor.fetchone()
        cursor.close

        if student_data:
            return Student(id = student_data[0] , firstname = student_data[1], lastname=student_data[2], course_code=student_data[3], year=student_data[4], gender=student_data[5], picture=student_data[6])
        else:
            return None

    @classmethod
    def get_paginated(cls, limit=50, offset=0):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT student.id, student.firstname, student.lastname, student.course_code, 
                   student.year, student.gender, course.college_code, student.picture
            FROM student
            INNER JOIN course ON student.course_code = course.code
            INNER JOIN college ON course.college_code = college.code
            ORDER BY student.id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        students = []
        for student_data in cursor.fetchall():
            student = Student(
                id=student_data[0],
                firstname=student_data[1],
                lastname=student_data[2],
                course_code=student_data[3],
                year=student_data[4],
                gender=student_data[5],
                college=student_data[6],
                picture=student_data[7]
            )
            students.append(student)
        cursor.close()
        return students

    @classmethod
    def get_total_count(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM student")
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    
    
