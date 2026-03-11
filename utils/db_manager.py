import mysql.connector
from mysql.connector import Error
import random


def get_db_connection():
    
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Or your MySQL host
            database="onlinedb",
            user="root",  # Your MySQL username
            password="root",
            port="3308",
            charset="utf8"  # Your MySQL password
        )
        if conn.is_connected():
            print("Successfully connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    
'''
   try:
        conn = mysql.connector.connect(
            host="rizwandb.ct6ciy2asq7v.ap-south-1.rds.amazonaws.com",  # Or your MySQL host
            database="online_learning_db",
            user="admin",  # Your MySQL username
            password="MyDatabase1234",
            port="3306",
            charset="utf8"  # Your MySQL password
        )
        if conn.is_connected():
            print("Successfully connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
'''  
   
# --- Admin Operations ---
def add_admin(username, password):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Storing plain text password - DANGER!
            query = "INSERT INTO admins (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))  # No hashing
            conn.commit()
            return True
        except Error as e:
            print(f"Error adding admin: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def get_admin_by_email(email):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM admins WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching faculty: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


# --- Faculty Operations ---
def add_faculty(name, email, password):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Storing plain text password - DANGER!
            query = "INSERT INTO faculties (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))  # No hashing
            conn.commit()
            return True
        except Error as e:
            print(f"Error adding faculty: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def get_faculties():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, name, email FROM faculties"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching faculties: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


def get_faculty_by_email(email):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM faculties WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching faculty: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


def update_faculty(faculty_id, name, email):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE faculties SET name = %s, email = %s WHERE id = %s"
            cursor.execute(query, (name, email, faculty_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error updating faculty: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def delete_faculty(faculty_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM faculties WHERE id = %s"
            cursor.execute(query, (faculty_id,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error deleting faculty: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


# --- Student Operations ---
def add_student(name, email, s_class, password):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Storing plain text password - DANGER!
            query = "INSERT INTO students (name, email, class, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, s_class, password))  # No hashing
            conn.commit()
            return True
        except Error as e:
            print(f"Error adding student: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def get_student_by_email(email):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM students WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching student: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


# --- Material Operations ---
def get_courses():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM courses"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching courses: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


def add_material(faculty_id, course_id, title, description, video_path, youtube_link, pdf_path, std_class):
    conn = get_db_connection()
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO materials 
                (faculty_id, course_id, title, description, video_path, youtube_link, pdf_path, std_class)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (faculty_id, course_id, title, description, video_path, youtube_link, pdf_path, std_class)
            print("DEBUG VALUES:", values)  # 👈 Check what's being inserted

            cursor.execute(query, values)
            conn.commit()
            return True
        except Error as e:
            print(f"Error adding material: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn.is_connected():
                conn.close()
    else:
        print("❌ Database connection failed.")
        return False


def get_materials_by_faculty(faculty_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT m.id, m.title, m.description, m.video_path, m.youtube_link, m.pdf_path,m.std_class, c.name as course_name
            FROM materials m
            JOIN courses c ON m.course_id = c.id
            WHERE m.faculty_id = %s
            ORDER BY m.uploaded_at DESC
            """
            cursor.execute(query, (faculty_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching materials: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


def get_materials_by_course(course_id, std_class):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT m.id, m.title, m.description, m.video_path, m.youtube_link, m.pdf_path, f.name as faculty_name, c.name as course_name
            FROM materials m
            JOIN faculties f ON m.faculty_id = f.id
            JOIN courses c ON m.course_id = c.id
            WHERE m.course_id = %s and m.std_class= %s
            ORDER BY m.uploaded_at DESC
            """
            cursor.execute(query, (course_id, std_class))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching materials by course: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


def update_material(id, title, description, video_path, youtube_link, pdf_path, std_class):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            UPDATE materials
            SET title = %s, description = %s, video_path = %s, youtube_link = %s, pdf_path = %s, std_class = %s
            WHERE id = %s
            """
            cursor.execute(query, (title, description, video_path, youtube_link, pdf_path, std_class, id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error updating material: {e}")
            return False
        finally:
            cursor.close()
            conn.close()



def delete_material(material_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM materials WHERE id = %s"
            cursor.execute(query, (material_id,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error deleting material: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


# --- Quiz Method (Corrected) ---
def get_quiz_questions(subject):
    """Fetches 10 random questions for a given subject from the database."""
    questions_list = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT question, option1, option2, option3, answer FROM quiz_questions WHERE subject = %s ORDER BY RAND() LIMIT 10"
            cursor.execute(query, (subject,))

            rows = cursor.fetchall()

            for row in rows:
                options = [row['option1'], row['option2'], row['option3']]
                random.shuffle(options)

                questions_list.append({
                    'question': row['question'],
                    'options': options,
                    'answer': row['answer']
                })
        except Error as err:
            print(f"Error fetching quiz questions: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    return questions_list


def get_material_by_id(material_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM materials where id= %s"
            cursor.execute(query, (material_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching student: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def save_feedback(name, feedback):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO feedback (name, feedback) VALUES (%s, %s)"
        cursor.execute(query, (name, feedback))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_feedback():
    conn = get_db_connection()
    feedbacks = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, feedback, submitted_at FROM feedback ORDER BY submitted_at DESC")
            feedbacks = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching feedbacks: {e}")
        finally:
            cursor.close()
            conn.close()
    return feedbacks
#-----------------roadmap---------------------------
def save_roadmap(std_class, pdf_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO roadmaps (std_class, pdf_name) VALUES (%s, %s)", (std_class, pdf_name))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_all_roadmaps():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM roadmaps")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_roadmap_by_id(roadmap_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM roadmaps WHERE id = %s", (roadmap_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def delete_roadmap(roadmap_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM roadmaps WHERE id = %s", (roadmap_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_roadmaps_by_class(std_class):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM roadmaps WHERE std_class = %s", (std_class,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


