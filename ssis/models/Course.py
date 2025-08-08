from ..extension import mysql

# CREATE TABLE IF NOT EXISTS course (
#     code VARCHAR(20) PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     college_code VARCHAR(10),
#     FOREIGN KEY (college_code) REFERENCES college(code) ON DELETE CASCADE ON UPDATE CASCADE
# );


class Course():
    def __init__(self, code=None, name=None, college_code= None):
        self.code = code
        self.name = name
        self.college_code = college_code
        self.connection = mysql.connection

    def add(self):
        cursor = self.connection.cursor()
        cursor.execute(" INSERT INTO course (code, name, college_code) VALUES (%s, %s, %s)",
                            (self.code, self.name, self.college_code))
        self.connection.commit()
        cursor.close()
    
    def update(self,code):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE course SET code=%s, name=%s , college_code=%s WHERE code=%s" , (self.code,self.name,self.college_code,code))
        self.connection.commit()
        cursor.close()

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM course WHERE code=%s", (self.code,))
        self.connection.commit()
        cursor.close()

    @classmethod
    def search(cls, input, filter):
        cursor = mysql.connection.cursor()
        coursess = []

        if filter == "0":
            cursor.execute("SELECT * FROM course WHERE code LIKE %s OR name LIKE %s OR college_code LIKE %s", (f"%{input}%", f"%{input}%", f"%{input}%"))
        elif filter == "1":
            cursor.execute("SELECT * FROM course WHERE code LIKE %s", (f"%{input}%",))
        elif filter == "2":
            cursor.execute("SELECT * FROM course WHERE name LIKE %s", (f"%{input}%",))
        elif filter == "3":
            cursor.execute("SELECT * FROM course WHERE college_code LIKE %s", (f"%{input}%",))
        for courses_data in cursor.fetchall():
            courses = Course(code=courses_data[0], name=courses_data[1], college_code=courses_data[2])
            coursess.append(courses)
        cursor.close()

        return coursess


    @classmethod
    def get_all(cls,table_name = 'course'):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        coursess = []
        for courses_data in cursor.fetchall():
            courses = Course(code=courses_data[0], name=courses_data[1], college_code=courses_data[2])
            coursess.append(courses)
        cursor.close()
        return coursess
    
    @classmethod
    def check_existing_code(cls,code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM course WHERE code = %s", (code,))
        existing_courses = cursor.fetchone()
        cursor.close()
        return existing_courses is not None
    
    @classmethod
    def get_one(clr, code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM course WHERE code = %s", (code,))
        existing_courses = cursor.fetchone()
        cursor.close

        if existing_courses:
            return Course(code=existing_courses[0], name=existing_courses[1], college_code=existing_courses[2])
        else:
            return None

    
    
