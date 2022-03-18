# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:58:02 2022

@author: jared
"""

import mysql.connector
import pandas as pd
import terminal

ceis236db = mysql.connector.connect(
  host="10.10.0.2",
  user="ceis236",
  password="ceis236",
  database="CEIS236"
)

cursor = ceis236db.cursor()
cursor.execute("SELECT DISTINCT SNAME FROM STUDENT")
studentsPre = cursor.fetchall()
students = []
for i in studentsPre:
    students.append(i[0])
cursor.execute("SELECT DISTINCT CNAME FROM COURSE;")
coursesPre = cursor.fetchall()
courses = []
for i in coursesPre:
    courses.append(i[0])

print(terminal.red('*** Jared\'s Quick \'n\' Dirty CEIS236 lookup tool ***'))
searchBy = str(input(terminal.yellow("Search by (N)ames or (C)ourses: ")))
if searchBy == 'N':
    print(terminal.green(students))
    name = str(input(terminal.yellow("Student name: ")))
    cursor.execute("SELECT STUDENT.SNAME, COURSE.CNAME, RESULT.GRADE \
                   FROM RESULT \
                   INNER JOIN STUDENT ON STUDENT.SNO = RESULT.SNO \
                   INNER JOIN COURSE ON COURSE.CNO = RESULT.CNO \
                   WHERE STUDENT.SNAME = %s",(name,))
    
    result = cursor.fetchall()
    # print(terminal.green(result))
    df = pd.DataFrame(result, columns =['Name', 'Course', 'Grade'])
    print(terminal.green(df))
if searchBy == 'C':
    print(terminal.green(courses))
    course = str(input(terminal.yellow("Course name: ")))
    cursor.execute("SELECT STUDENT.SNAME, COURSE.CNAME, RESULT.GRADE \
                   FROM RESULT \
                   INNER JOIN STUDENT ON STUDENT.SNO = RESULT.SNO \
                   INNER JOIN COURSE ON COURSE.CNO = RESULT.CNO \
                   WHERE COURSE.CNAME = %s",(course,))
    result = cursor.fetchall()
    
    df = pd.DataFrame(result, columns =['Name', 'Course', 'Grade'])
    print(terminal.green(df))
