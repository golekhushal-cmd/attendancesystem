import cv2
import os
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


def capture_faces(student_id, student_name):

    folder_name = f"{student_id}_{student_name}"

    save_path = os.path.join(
        DATASET_PATH,
        folder_name
    )

    os.makedirs(save_path, exist_ok=True)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        messagebox.showerror("Camera Error", "Could not open camera!\nMake sure your webcam is connected.")
        return

    count = 0
    max_images = 25

    print("\n Starting Face Capture... Press 'q' to quit early.")

    while True:

        success, frame = camera.read()

        if not success:
            print("\n ERROR: Failed to read from camera.")
            break

        cv2.imshow("Capturing Faces - Press Q to quit", frame)

        image_path = os.path.join(save_path, f"{count}.jpg")
        cv2.imwrite(image_path, frame)

        count += 1

        key = cv2.waitKey(100)

        if key == ord("q") or count >= max_images:
            break

    camera.release()
    cv2.destroyAllWindows()

    messagebox.showinfo(
        "Done",
        f"{count} images captured!\nSaved to: {save_path}"
    )
    print(f"\n {count} images captured and saved to: {save_path}")


if __name__ == "__main__":

    def submit():
        sid = id_entry.get().strip()
        sname = name_entry.get().strip()

        if not sid or not sname:
            messagebox.showerror("Error", "Both fields are required!")
            return

        root.destroy()
        capture_faces(sid, sname)

    root = tk.Tk()
    root.title("Capture Faces")
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
        text="Start Capture",
        font=("Arial", 12),
        width=15,
        command=submit
    ).pack(pady=15)

    root.mainloop()