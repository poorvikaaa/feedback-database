from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras
from datetime import date

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="stu_feed",
        user="postgres",
        password="poor",
        cursor_factory=psycopg2.extras.DictCursor
    )

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_otas', methods=["GET", "POST"])
def login_otas():
    if request.method == "POST":
        year = request.form.get("year")
        password = request.form.get("password")

        if year == "2027" and password == "123":
            return redirect(url_for("submit_feedback"))
        else:
            error = "Incorrect year or password. Please try again."
            return render_template("login_otas.html", error=error)

    return render_template("login_otas.html")


# Feedback form route
@app.route("/submit_feedback", methods=["GET", "POST"])
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def submit_feedback(id=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM departments")
            departments = cursor.fetchall()
            cursor.execute("SELECT * FROM teachers")
            teachers = cursor.fetchall()
            cursor.execute("SELECT * FROM subjects")
            subjects = cursor.fetchall()
        
        feedback = None
        if id:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM feedback WHERE id = %s", (id,))
                feedback = cursor.fetchone()
        
        if request.method == "POST":
            student_name = request.form['student_name']
            student_email = request.form['student_email']
            department_id = request.form['department']
            teacher_id = request.form['teacher']
            subject_id = request.form['subject']
            rating = int(request.form['rating'])
            comments = request.form['comments']

            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM students WHERE email = %s", (student_email,))
                student = cursor.fetchone()
                if not student:
                    cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s) RETURNING id", (student_name, student_email))
                    student_id = cursor.fetchone()['id']
                else:
                    student_id = student['id']

                if id:
                    cursor.execute("UPDATE feedback SET rating = %s, comments = %s WHERE id = %s",
                                   (rating, comments, id))
                else:
                    cursor.execute(
                        "INSERT INTO feedback (student_id, teacher_id, subject_id, rating, comments, date) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (student_id, teacher_id, subject_id, rating, comments, date.today())
                    )
                conn.commit()
            
            return redirect(url_for("feedbacks"))

        return render_template("submit_feedback.html", departments=departments, teachers=teachers, subjects=subjects, feedback=feedback)
    finally:
        conn.close()

# Show all feedback entries
@app.route("/feedbacks")
def feedbacks():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT f.id, s.name AS student_name, s.email, t.name AS teacher_name, subj.name AS subject_name,
                       f.rating, f.comments, f.date
                FROM feedback f
                JOIN students s ON f.student_id = s.id
                JOIN teachers t ON f.teacher_id = t.id
                JOIN subjects subj ON f.subject_id = subj.id
                ORDER BY f.date DESC
            """)
            feedbacks = cursor.fetchall()
        return render_template("feedbacks.html", feedbacks=feedbacks)
    finally:
        conn.close()

# Delete feedback
@app.route("/delete/<int:id>")
def delete_feedback(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM feedback WHERE id = %s", (id,))
            conn.commit()
        return redirect(url_for("feedbacks"))
    finally:
        conn.close()

# Summary route
@app.route('/feedback_summary')
def feedback_summary():
    conn = get_db_connection()
    try:
       with conn.cursor() as cur:
            cur.execute("""
                SELECT t.name AS teacher_name, 
                    subj.name AS subject_name, 
                    ROUND(AVG(f.rating) * 20, 2) AS avg_percentage
                FROM feedback f
                JOIN teachers t ON f.teacher_id = t.id
                JOIN subjects subj ON f.subject_id = subj.id
                GROUP BY t.name, subj.name
                ORDER BY avg_percentage DESC
            """)
            results = cur.fetchall()
            return render_template("feedback_summary.html", results=results)
    finally:
        conn.close()

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:5432/feedback_database'

# Run the app
if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)
