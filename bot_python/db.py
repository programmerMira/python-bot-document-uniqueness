import sqlite3
from check import check_files

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки для log """
        with self.connection:
            result_log=[]
            result_ids = self.cursor.execute('SELECT id FROM Result').fetchall()
            for id in result_ids:
                tmp_result_log=""
                tmp_result_log += self.cursor.execute('SELECT file FROM CourseProject, Result WHERE CourseProject.id=Result.CourseProject_ID AND Result.id=?',(int(id[0]),)).fetchall()[0][0]
                tmp_result_log += " - "               
                tmp_result_log += self.cursor.execute('SELECT file FROM CourseProject, Result WHERE CourseProject.id=Result.CourseProject_compared_ID AND Result.id=?',(int(id[0]),)).fetchall()[0][0]
                tmp_result_log += " -> "
                tmp_result_log += str(self.cursor.execute('SELECT result FROM Result WHERE Result.id=?',(int(id[0]),)).fetchall()[0][0])
                result_log.append(tmp_result_log)
            return result_log
            
    def select_plural(self, rownum):
        """ Получаем все строки с номером текущего документа """
        with self.connection:
            return self.cursor.execute('SELECT * FROM Result WHERE courseProject_ID = ?', (rownum,)).fetchall()
    
    def select_single(self, rownum):
        """ Получаем общий результат с номером текущего документа """
        with self.connection:
            id = self.cursor.execute('SELECT id FROM CourseProject WHERE file = ?', (rownum,)).fetchall()[0]
            temp = self.cursor.execute('SELECT AVG(result) FROM Result WHERE courseProject_ID = ?', (int(id[0]),)).fetchall()
            return temp
    
    def insert_student(self, filename):
        with self.connection:
            filedata = filename.replace('.docx','').replace('.doc','').split('_')
            print(filename)
            if len(filedata)==6:
                self.cursor.execute('INSERT INTO Student(Surname, Name, FatherName, acadYear, faculty) VALUES(?,?,?,?,?)  ', (filedata[0],filedata[1],filedata[2],int(filedata[3]),filedata[4]))
                self.connection.commit()
            elif len(filedata)==7:
                self.cursor.execute('INSERT INTO Student(Surname, Name, FatherName, acadYear, faculty) VALUES(?,?,?,?,?)  ', (filedata[0],filedata[1],filedata[2],int(filedata[3]),filedata[4]+'-'+filedata[5]))
                self.connection.commit()
            elif len(filedata)==8:
                self.cursor.execute('INSERT INTO Student(Surname, Name, FatherName, acadYear, faculty) VALUES(?,?,?,?,?)  ', (filedata[0],filedata[1],filedata[2],int(filedata[3]),filedata[4]+'-'+filedata[5]))
                self.connection.commit()
    
    def insert_project(self, filepath):
        with self.connection:
            student = self.cursor.execute('SELECT id FROM Student ORDER BY id DESC').fetchone()[0]
            self.cursor.execute('INSERT INTO CourseProject(student_ID, file) VALUES(?,?)  ', (int(student),filepath))
            self.connection.commit()
        
    def insert_result(self, filedata):
        with self.connection:
            initial = self.cursor.execute('SELECT id FROM CourseProject WHERE CourseProject.file=?',(filedata,)).fetchone()[0]
            print(initial)
            files = self.cursor.execute('SELECT id FROM CourseProject WHERE id!=?',(int(initial),)).fetchall()
            print("Files")
            print(files)
            for file in files:
                file_path = self.cursor.execute('SELECT file FROM CourseProject WHERE id=?',(int(file[0]),)).fetchall()[0]
                print("Filepath")
                print(file_path)
                print(filedata)
                result = check_files(filedata, file_path)
                print("Here")
                self.cursor.execute('INSERT INTO Result(courseProject_ID, courseProject_compared_ID, result) VALUES(?,?,?)  ', (int(initial),int(file[0]),result))
                self.connection.commit()
    
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()