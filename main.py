from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import create_engine, text

# Flask App
app = Flask(__name__)

# Secret Key
app.secret_key = "secret"

# Connecting Database and Creating a Database Engine
engine = create_engine(
    "mysql://david@localhost/exam_webapp", echo=True)
connection = engine.connect()


# Routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        
        # Inserting Data into Database
        if role == 'Student':
            query = text("INSERT INTO student (name) VALUES (:name)")
            connection.execute(query, {'name': name})
            connection.commit()
        elif role == 'Teacher':
            query = text("INSERT INTO teacher (name) VALUES (:name)")
            connection.execute(query, {'name': name})
            connection.commit()
        
        flash('User Registered Successfully', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/all_accounts/', methods=['GET'])
def all_accounts():
    role_filter = request.args.get('role_filter', 'all')
    teacher_query = ""
    student_query = ""
    
    if role_filter == 'all':
        teacher_query = text("SELECT * FROM teacher")
        student_query = text("SELECT * FROM student")
    elif role_filter == 'teacher':
        teacher_query = text("SELECT * FROM teacher")
    elif role_filter == 'student':
        student_query = text("SELECT * FROM student")
    
    teachers = connection.execute(teacher_query) if teacher_query != "" else []
    students = connection.execute(student_query) if student_query != "" else []
    
    return render_template('all_accounts.html', teachers=teachers, students=students, role_filter=role_filter)


@app.route('/teacher_login/', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_name = request.form['teacher_name']
        query = text("SELECT * FROM teacher WHERE name=:teacher_name")
        result = connection.execute(query, {'teacher_name': teacher_name})
        row = result.fetchone()
        if row:
            return redirect(url_for('create_exam'))
        else:
            flash('Invalid Credentials', 'error')
            return redirect(url_for('teacher_login'))
    else:
        return render_template('teacher_login.html')


@app.route('/create_exam/', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']
        question4 = request.form['question4']

        # Inserting exam into Database
        query = text("INSERT INTO exam (teacher_id, question1, question2, question3, question4) VALUES (:teacher_id, :question1, :question2, :question3, :question4)")
        connection.execute(query, {'teacher_id': 1, 'question1': question1, 'question2': question2, 'question3': question3, 'question4': question4})
        connection.commit()

        return redirect(url_for('all_exams'))
    else:
        return render_template('create_exam.html')


@app.route('/all_exams/', methods=['GET'])
def all_exams():
    query = text("SELECT * FROM exam")
    exams = connection.execute(query)
    return render_template('all_exams.html', exams=exams)


@app.route('/edit_exam/', methods=['GET', 'POST'])
def edit_exam():
    if request.method == 'POST':
        exam_id = request.form['exam_id']
        exam = connection.execute(text("SELECT * FROM exam WHERE exam_id=:exam_id"), {"exam_id": exam_id}).fetchone()

        if exam:
            connection.execute(text("UPDATE exam SET teacher_id = :teacher_id, question1 = :question1, question2 = :question2, question3 = :question3, question4 = :question4 WHERE exam_id = :exam_id"), request.form)
            connection.commit()
            flash('Exam updated successfully', 'success')
        else:
            flash('Invalid Exam ID', 'error')
            
    return render_template('edit_exam.html')


@app.route('/delete_exam/', methods=['POST', 'GET'])
def delete_exam():
    if request.method == 'POST':
        exam_id = request.form['exam_id']
        exam = connection.execute(text("SELECT * FROM exam WHERE exam_id=:exam_id"), {"exam_id": exam_id}).fetchone()

        if exam:
            connection.execute(text("DELETE FROM exam WHERE exam_id=:exam_id"), {"exam_id": exam_id})
            connection.commit()
            flash('Exam deleted successfully', 'success')
        else:
            flash('Invalid Exam ID', 'error')
            
    return render_template('delete_exam.html')


@app.route('/exam_page/', methods=['POST'])
def exam_page():
    if request.method == 'POST':
        exam_id = request.form['exam_id']
        exam = connection.execute(text("SELECT * FROM exam WHERE exam_id=:exam_id"), {"exam_id": exam_id}).fetchone()

        if exam:
            flash('Exam submitted!', 'success')
            return render_template('exam_page.html', exam=exam)
        else:
            flash('Invalid Exam ID', 'error')
            return redirect(url_for('all_exams'))
    render_template('exam_page.html')



# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
