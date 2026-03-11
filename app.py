from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import pandas as pd
import os
import re
from chatbot import get_bot_response
# Import your existing utility functions
from utils import db_manager

app = Flask(__name__)
# Set a secret key for session management
app.secret_key = 'your_super_secret_key_here'

# Create 'uploads' directory if it doesn't exist
UPLOAD_DIR = "uploads/"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# --- Utility Functions (Adapted for Flask) ---
def save_uploaded_file(uploaded_file, folder="uploads"):
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(folder, uploaded_file.filename)
        uploaded_file.save(file_path)
        return file_path
    return None


def extract_youtube_video_id(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&?%]{11})')
    match = re.match(youtube_regex, url)
    if match:
        return match.group(6)
    return None


# --- Routes ---
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        if session['user_type'] == 'Admin':
            return redirect(url_for('admin_dashboard'))
        elif session['user_type'] == 'Faculty':
            return redirect(url_for('faculty_dashboard'))
        elif session['user_type'] == 'Student':
            return redirect(url_for('student_dashboard'))
    return render_template('login.html', user_type="Login")


@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    email = request.form['email']
    password = request.form['password']
    print(user_type)
    print(email)
    print(password)

    if user_type == "Admin":
        admin = db_manager.get_admin_by_email(email)
        print("Admin DB result:", admin)

        if admin and password == admin['password']:
            session['logged_in'] = True
            session['user_type'] = "Admin"
            session['user_id'] = admin['id']
            session['user_name'] = admin['name']
            return redirect(url_for('admin_dashboard'))
    elif user_type == "Faculty":
        faculty = db_manager.get_faculty_by_email(email)
        if faculty and password == faculty['password']:
            session['logged_in'] = True
            session['user_type'] = "Faculty"
            session['user_id'] = faculty['id']
            session['user_name'] = faculty['name']
            return redirect(url_for('faculty_dashboard'))
    elif user_type == "Student":
        student = db_manager.get_student_by_email(email)
        if student and password == student['password']:
            session['logged_in'] = True
            session['user_type'] = "Student"
            session['user_id'] = student['id']
            session['user_name'] = student['name']
            return redirect(url_for('student_dashboard'))

    return render_template('login.html', error="Invalid credentials", user_type=user_type)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        s_class = request.form['s_class']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            if db_manager.add_student(name, email, s_class, password):
                return render_template('login.html', success="Registration successful! Please log in.",
                                       user_type="Student")
            else:
                return render_template('login.html', error="Registration failed. Email might already exist.",
                                       user_type="Register Student")
        else:
            return render_template('login.html', error="Passwords do not match.", user_type="Register Student")

    return render_template('login.html', user_type="Register Student")


# --- Admin Routes ---
@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in') or session.get('user_type') != 'Admin':
        return redirect(url_for('index'))

    faculties = db_manager.get_faculties()
    return render_template('admin.html', user_name=session.get('user_name'), faculties=faculties)


@app.route('/admin/add_faculty', methods=['POST'])
def add_faculty():
    if not session.get('logged_in') or session.get('user_type') != 'Admin':
        return redirect(url_for('index'))

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    if db_manager.add_faculty(name, email, password):
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))  # TODO: Add error handling message


@app.route('/admin/update_faculty/<int:faculty_id>', methods=['POST'])
def update_faculty(faculty_id):
    if not session.get('logged_in') or session.get('user_type') != 'Admin':
        return redirect(url_for('index'))

    new_name = request.form['new_name']
    new_email = request.form['new_email']
    db_manager.update_faculty(faculty_id, new_name, new_email)
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_faculty/<int:faculty_id>', methods=['POST'])
def delete_faculty(faculty_id):
    if not session.get('logged_in') or session.get('user_type') != 'Admin':
        return redirect(url_for('index'))

    db_manager.delete_faculty(faculty_id)
    return redirect(url_for('admin_dashboard'))


# --- Faculty Routes ---
@app.route('/faculty')
def faculty_dashboard():
    if not session.get('logged_in') or session.get('user_type') != 'Faculty':
        return redirect(url_for('index'))

    courses = db_manager.get_courses()
    materials = db_manager.get_materials_by_faculty(session['user_id'])

    return render_template('faculty.html', user_name=session.get('user_name'), courses=courses, materials=materials)


@app.route('/faculty/upload_material', methods=['POST'])
def upload_material():
    if not session.get('logged_in') or session.get('user_type') != 'Faculty':
        return redirect(url_for('index'))

    title = request.form['title']
    description = request.form['description']
    course_id = request.form['course_id']
    youtube_link = request.form.get('youtube_link')

    video_file = request.files.get('video_file')
    pdf_file = request.files.get('pdf_file')
    std_class = request.form['std_class']

    video_path = save_uploaded_file(video_file, UPLOAD_DIR)
    pdf_path = save_uploaded_file(pdf_file, UPLOAD_DIR)

    youtube_embed_link = None
    if youtube_link:
        youtube_id = extract_youtube_video_id(youtube_link)
        if youtube_id:
            youtube_embed_link = f"https://www.youtube.com/embed/{youtube_id}"

    db_manager.add_material(
        session['user_id'],
        course_id,
        title,
        description,
        video_path,
        youtube_embed_link,
        pdf_path,
        std_class
    )

    return redirect(url_for('faculty_dashboard'))


@app.route('/faculty/update_material/<int:material_id>', methods=['POST'])
def update_material(material_id):
    if not session.get('logged_in') or session.get('user_type') != 'Faculty':
        return redirect(url_for('index'))

    new_title = request.form['new_title']
    new_description = request.form['new_description']

    update_youtube_link = request.form.get('update_youtube_link')

    update_video_file = request.files.get('update_video_file')
    update_pdf_file = request.files.get('update_pdf_file')


    material = db_manager.get_material_by_id(material_id)
    updated_video_path = material['video_path']
    updated_pdf_path = material['pdf_path']
    updated_youtube_link = material['youtube_link']

    if update_video_file and update_video_file.filename != '':
        updated_video_path = save_uploaded_file(update_video_file, UPLOAD_DIR)

    if update_pdf_file and update_pdf_file.filename != '':
        updated_pdf_path = save_uploaded_file(update_pdf_file, UPLOAD_DIR)

    if update_youtube_link:
        youtube_id = extract_youtube_video_id(update_youtube_link)
        if youtube_id:
            updated_youtube_link = f"https://www.youtube.com/embed/{youtube_id}"
        else:
            updated_youtube_link = None
    else:
        updated_youtube_link = None

    db_manager.update_material(
        material_id,
        new_title,
        new_description,
        updated_video_path,
        updated_youtube_link,
        updated_pdf_path

    )
    return redirect(url_for('faculty_dashboard'))


@app.route('/faculty/delete_material/<int:material_id>', methods=['POST'])
def delete_material(material_id):
    if not session.get('logged_in') or session.get('user_type') != 'Faculty':
        return redirect(url_for('index'))

    db_manager.delete_material(material_id)
    return redirect(url_for('faculty_dashboard'))


# --- Student Routes ---
@app.route('/student')
def student_dashboard():
    if not session.get('logged_in') or session.get('user_type') != 'Student':
        return redirect(url_for('index'))

    courses = db_manager.get_courses()

    selected_course_id = request.args.get('course_id')
    select_std_class= request.args.get('std_class')
    materials = []
    if selected_course_id:
        materials = db_manager.get_materials_by_course(selected_course_id,select_std_class)

    return render_template('student.html', user_name=session.get('user_name'), courses=courses, materials=materials,
                           selected_course_id=selected_course_id)
# --- Chatbot Page ---
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if not session.get('logged_in'):
        return redirect(url_for('index'))

    bot_reply = None
    if request.method == 'POST':
        user_message = request.form['message']
        bot_reply = get_bot_response(user_message)

    return render_template('chatbot.html', user_name=session.get('user_name'), bot_reply=bot_reply)


# --- Quiz Page ---
@app.route('/quiz')
def quiz():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('quiz.html', user_name=session.get('user_name'))


@app.route('/download/<path:filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return send_from_directory(UPLOAD_DIR, filename)

@app.route('/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)