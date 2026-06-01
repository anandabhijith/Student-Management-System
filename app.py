from flask import Flask,render_template,request
import sqlite3

app=Flask(__name__)

def init_db():
    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS students( 
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT, 
                   roll TEXT, 
                   department TEXT, 
                   attendance TEXT, 
                   dsa_marks integer,
                   java_marks integer,
                   python_marks integer,
                   cn_marks integer    )
    ''')
    conn.commit()
    conn.close()
    
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/student')
def student():
    return render_template("student.html")

@app.route('/teacher')
def teacher():
    return render_template("teacher.html")

@app.route('/studentlogin',methods=['POST'])
def studentlogin():
    rollno = request.form['userid']
    password = request.form['password']

    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()

    cursor.execute('''
        select * from students where roll=?
    ''',(rollno,))
    student = cursor.fetchone()
    conn.close()
    return render_template("student.html",student=student)

@app.route('/teacherlogin',methods=['POST'])
def teacherlogin():

    username = request.form['userid']
    password = request.form['password']

    if username == "teacher" and password == "admin":
        return render_template("teacher.html")

    return "Invalid Login"

@app.route('/addstudent',methods=['POST'])
def addstudent():

    name=request.form['name']
    rollno=request.form['roll']
    department=request.form['department']

    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()
    cursor.execute('''
        insert into students(
            name,roll,department,attendance,dsa_marks,java_marks,python_marks,cn_marks)
            values(?,?,?,?,?,?,?,?)
                   ''',(name,rollno,department,0,0,0,0,0))
    conn.commit()
    conn.close()
    return render_template("teacher.html")

@app.route('/manageattendance',methods=['POST'])
def manageattendance():
    rollno=request.form['roll']
    attendance=request.form['attendance']

    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()
    cursor.execute('''
        update students
        set attendance=?
        where roll=?           
                   ''',(attendance,rollno))
    conn.commit()
    conn.close()
    return render_template("teacher.html", active_section='manageattendance')

@app.route('/updatemarks',methods=['POST'])
def updatemarks():
    roll=request.form['roll']
    subject=request.form['subject'].lower()
    marks=request.form['marks']

    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()

    if subject=='dsa':
        cursor.execute(''' 
            update students
            set dsa_marks=?
            where roll=?
                ''',(marks,roll))
        
    elif subject=='java':
        cursor.execute(''' 
            update students
            set java_marks=?
            where roll=?
                ''',(marks,roll))
        
    elif subject=='python':
        cursor.execute(''' 
            update students
            set python_marks=?
            where roll=?
                ''',(marks,roll))
                   
    elif subject=='cn':
        cursor.execute(''' 
            update students
            set cn_marks=?
            where roll=?
                ''',(marks,roll))
    else:
        conn.close()
        return "Invalid subject name"
    
    conn.commit()
    conn.close()
    return render_template('teacher.html', active_section='updatemarks')

init_db()

@app.route('/viewstudent')
def viewstudent():
    
    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()
    cursor.execute('''
        select * from students 
    ''')
    students=cursor.fetchall()
    conn.close()
    return render_template('teacher.html',students=students,active_section='viewstudent')

@app.route('/deletestudent',methods=['POST'])
def deletestudent():
    rollno=request.form['roll']

    conn=sqlite3.connect('students.db')
    cursor=conn.cursor()
    cursor.execute(''' 
        delete from students
        where roll=?
    ''',(rollno,))
    conn.commit()
    conn.close()
    return render_template("teacher.html",active_section='deletestudent')

@app.route('/view')
def view():

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return str(data)
if __name__=='__main__':
    app.run(debug=True)