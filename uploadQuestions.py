import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import mysql.connector

# Database connection details (Update as per your system)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',   # your MySQL password
    'database': 'online_learning_db',
    'port':'3308',
    'charset':'utf8'# your database name
}

def upload_to_database(csv_path):
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)

        # Ensure all required columns are present
        required_cols = ['id', 'subject', 'question', 'option1', 'option2', 'option3', 'answer']
        if not all(col in df.columns for col in required_cols):
            messagebox.showerror("Error", f"CSV must contain columns: {', '.join(required_cols)}")
            return

        # Connect to MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz (
                id INT PRIMARY KEY,
                subject VARCHAR(255),
                question TEXT,
                option1 VARCHAR(255),
                option2 VARCHAR(255),
                option3 VARCHAR(255),
                answer VARCHAR(255)
            )
        """)

        # Loop through CSV and insert/update data
        for _, row in df.iterrows():
            data_tuple = (
                int(row['id']),
                row['subject'],
                row['question'],
                row['option1'],
                row['option2'],
                row['option3'],
                row['answer']
            )

            cursor.execute("""
                INSERT INTO quiz (id, subject, question, option1, option2, option3, answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    subject = VALUES(subject),
                    question = VALUES(question),
                    option1 = VALUES(option1),
                    option2 = VALUES(option2),
                    option3 = VALUES(option3),
                    answer = VALUES(answer)
            """, data_tuple)

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "New data added and existing records updated successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload data.\n{e}")

def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)
        upload_to_database(file_path)

# ------------------ Tkinter UI ------------------
root = tk.Tk()
root.title("Quiz Question Uploader")
root.geometry("500x200")
root.resizable(False, False)

label_title = tk.Label(root, text="Upload Quiz Questions (CSV → MySQL)", font=("Arial", 14, "bold"))
label_title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

entry_path = tk.Entry(frame, width=50)
entry_path.grid(row=0, column=0, padx=10)

btn_browse = tk.Button(frame, text="Browse & Upload", command=browse_file, bg="#4CAF50", fg="white", width=15)
btn_browse.grid(row=0, column=1)

footer = tk.Label(root, text="Existing data will stay safe — only new/updated rows will change.", fg="gray", font=("Arial", 9))
footer.pack(pady=10)

root.mainloop()
