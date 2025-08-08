from ..extension import mysql

# CREATE TABLE college (
#     code VARCHAR(10) PRIMARY KEY,
#     name VARCHAR(255) NOT NULL
# );


class College():
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name
        self.connection = mysql.connection

    def add(self):
        cursor = self.connection.cursor()
        cursor.execute(" INSERT INTO college (code, name) VALUES (%s, %s)",
                            (self.code, self.name))
        self.connection.commit()
        cursor.close()
    
    def update(self,code):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE college SET code=%s, name=%s WHERE code=%s" , (self.code,self.name,code))
        self.connection.commit()
        cursor.close()

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM college WHERE code=%s", (self.code,))
        self.connection.commit()
        cursor.close()

    @classmethod
    def search(cls, input,filter):
        cursor = mysql.connection.cursor()
        colleges = []

        if filter == "0":
            cursor.execute("SELECT * FROM college WHERE code LIKE %s OR name LIKE %s", (f"%{input}%",f"%{input}%"))
        elif filter == "1":
            cursor.execute("SELECT * FROM college WHERE code LIKE %s", (f"%{input}%",))
        elif filter =="2":
            cursor.execute("SELECT * FROM college WHERE name LIKE %s", (f"%{input}%",))
        for college_data in cursor.fetchall():
            college = College(code = college_data[0] , name = college_data[1])
            colleges.append(college)
        cursor.close

        return colleges


    @classmethod
    def get_all(cls,table_name = 'college'):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        colleges = []
        for college_data in cursor.fetchall():
            college = College(code=college_data[0], name=college_data[1])
            colleges.append(college)
        cursor.close()
        return colleges
    
    @classmethod
    def check_existing_code(cls,code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM college WHERE code = %s", (code,))
        existing_college = cursor.fetchone()
        cursor.close()
        return existing_college is not None
    
    @classmethod
    def get_one(clr, code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM college WHERE code = %s", (code,))
        existing_college = cursor.fetchone()
        cursor.close()

        if existing_college:
            return College(code=existing_college[0], name=existing_college[1])
        else:
            return None

    
    
