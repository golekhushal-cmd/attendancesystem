import os
import csv
import sqlite3
import tkinter as tk
from tkinter import messagebox


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "student_images"
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "database",
    "students.csv"
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "attendance.db"
)


def register_student(
    student_id,
    student_name
):

    folder_name = (
        f"{student_id}_{student_name}"
    )

    student_folder_path = (
        os.path.join(
            DATASET_PATH,
            folder_name
        )
    )

    os.makedirs(
        student_folder_path,
        exist_ok=True
    )

    file_exists = os.path.exists(
        CSV_FILE
    )

    with open(
        CSV_FILE,
        mode="a",
        newline=""
    ) as file:

        writer = csv.writer(
            file
        )

        if (
            not file_exists
            or
            os.path.getsize(
                CSV_FILE
            ) == 0
        ):
            writer.writerow([
                "student_id",
                "student_name"
            ])

        writer.writerow([
            student_id,
            student_name
        ])

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (
            student_id,
            student_name
        )
        VALUES (?, ?)
    """, (
        student_id,
        student_name
    ))

    connection.commit()
    connection.close()

    return student_folder_path


if __name__ == "__main__":

    def submit():
        sid = id_entry.get().strip()
        sname = name_entry.get().strip()

        if not sid or not sname:
            messagebox.showerror("Error", "Both fields are required!")
            return

        try:
            path = register_student(sid, sname)
            messagebox.showinfo(
                "Success",
                f"Student '{sname}' registered!\nFolder: {path}"
            )
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Register Student")
    root.geometry("350x200")
    root.resizable(False, False)

    tk.Label(root, text="Student ID:", font=("Arial", 12)).pack(pady=(20, 2))
    id_entry = tk.Entry(root, font=("Arial", 12), width=25)
    id_entry.pack()

    tk.Label(root, text="Student Name:", font=("Arial", 12)).pack(pady=(10, 2))
    name_entry = tk.Entry(root, font=("Arial", 12), width=25)
    name_entry.pack()

    tk.Button(
        root,
        text="Register",
        font=("Arial", 12),
        width=15,
        command=submit
    ).pack(pady=15)

    root.mainloop()