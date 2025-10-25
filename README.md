🎓 Student Feedback System
A web-based application built with Flask and PostgreSQL that allows students to submit feedback for teachers, and admins to manage teachers, subjects, and view feedback reports.

🚀 Features
  👨‍🎓 Student
Register and log in securely
Auto-fill feedback form fields using profile data
Submit feedback for assigned teachers and subjects
View submitted feedback history

  👨‍🏫 Teacher / Admin
Admin dashboard to manage teachers, subjects, and students
Role-based login (Admin and Student)
View and analyze feedback responses
One-to-one mapping between teachers and subjects

🏗️ Tech Stack
Component	              Technology
Backend	               Flask (Python)
Frontend	          HTML, CSS, Bootstrap
Database	              PostgreSQL
Authentication	        Flask-Login
Server	          Flask Development Server
Environment	            PostgreSQL

⚙️ Installation & Setup
      git clone https://github.com/<your-username>/<repo-name>.git
      cd <repo-name>
2️⃣ Create Virtual Environment
      python -m venv venv
      venv\Scripts\activate     # On Windows
      source venv/bin/activate  # On macOS/Linux
3️⃣ Install Dependencies
      pip install -r requirements.txt


🗂️ Project Structure
feedback-system/
│
├── app.py                 # Main Flask app
├── templates/             # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   └── feedback_form.html
│
├── static/                # CSS, JS, Images
│   ├── style.css
│   └── script.js
│
├── models.py              # Database models (Student, Teacher, Feedback)
├── forms.py               # Flask-WTF forms
├── requirements.txt       # Dependencies
└── README.md              # Project documentation

🧠 Database Design

Entities:
    Student (id, name, email, password, course)
    Teacher (id, name, subject_id)
    Subject (id, name)
    Feedback (id, student_id, teacher_id, rating, comments)

Relationships:
    1️⃣ One-to-one between Teacher and Subject
    🔁 One-to-many between Teacher and Feedback

🔒 Authentication & Roles
    Students can only submit and view their feedback.
    Admins can view feedback reports, manage users, and subjects.

🧩 Future Enhancements
    Add feedback analytics (charts using Chart.js or Plotly)
    Email notifications for feedback submission
    Export feedback data to CSV or Excel
    Admin reports dashboard








      











