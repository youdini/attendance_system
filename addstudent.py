import csv
import os
import subprocess
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, messagebox, END

import cv2
import joblib
import mysql.connector
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame4")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="thesis"
)

cur = db.cursor()


def on_close():
    response = messagebox.askyesno(
        "Close", "Are you sure you want to close the window?")
    if response:
        window.destroy()
        subprocess.run(["python", "./home.py"])
    else:
        return


face_detector = cv2.CascadeClassifier(
    "./resources/haarcascade_frontalface_default.xml")


def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points


def identify_face(face_array):
    model = joblib.load('./static/face_recognition_model.pkl')
    return model.predict(face_array)


def train_model():
    faces = []
    labels = []
    user_list = os.listdir('./static/faces')
    for user in user_list:
        for image_name in os.listdir(f'./static/faces/{user}'):
            img = cv2.imread(f'./static/faces/{user}/{image_name}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)

    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, './static/face_recognition_model.pkl')


def face_recognition():
    cam = cv2.VideoCapture(0)
    ret = True
    while ret:
        ret, frame = cam.read()

        if len(extract_face(frame)) > 0:
            (x, y, w, h) = extract_face(frame)[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            cv2.putText(frame, identified_person,
                        (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()


def check_student(sid, crs_cd):
    cur.execute(
        "SELECT student_id FROM students "
        f"WHERE student_id = '{sid}' AND course_code = '{crs_cd}'")
    result = cur.fetchone()
    if result is None:
        print(f"Student {sid} is not registered, Available!")
        return False
    else:
        return True


def create_csv(crs_cd):
    if f'Students-{crs_cd}.csv' not in os.listdir('Attendance'):
        with open(f'./Attendance/Student-{crs_cd}.csv', 'w') as f:
            f.write(
                'Student Id,First name,Last name,Course,Section,Course Code,Time,Day,Lab Room')


def write_csv(sid, fn, ln, crs, sc, crs_cd, ts, ds, lr):
    with open(f'./Attendance/Students-{crs_cd}.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([sid, fn, ln, crs, sc, crs_cd, ts, ds])


class AddStudentWindow:
    def __init__(self, master):
        self.master = master

        window.geometry("462x602")
        window.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=602,
            width=462,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.submit,
            relief="flat"
        )
        self.button_1.place(
            x=163.0,
            y=554.0,
            width=135.71435546875,
            height=35.6824951171875
        )

        self.canvas.create_rectangle(
            0.0,
            0.0,
            462.0,
            602.0,
            fill="#FFFFFF",
            outline="")

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            230.0,
            308.53619384765625,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            230.5,
            97.77801513671875,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_1.place(
            x=87.0,
            y=87.98681640625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            230.5,
            147.98016357421875,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_2.place(
            x=87.0,
            y=138.18896484375,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(
            230.5,
            198.182373046875,
            image=self.entry_image_3
        )
        self.entry_3 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_3.place(
            x=87.0,
            y=188.39117431640625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(
            230.5,
            248.384521484375,
            image=self.entry_image_4
        )
        self.entry_4 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_4.place(
            x=87.0,
            y=238.59332275390625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_5 = PhotoImage(
            file=relative_to_assets("entry_5.png"))
        self.entry_bg_5 = self.canvas.create_image(
            230.5,
            298.58673095703125,
            image=self.entry_image_5
        )
        self.entry_5 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_5.place(
            x=87.0,
            y=288.7955322265625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_6 = PhotoImage(
            file=relative_to_assets("entry_6.png"))
        self.entry_bg_6 = self.canvas.create_image(
            230.5,
            370.15155029296875,
            image=self.entry_image_6
        )
        self.entry_6 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_6.place(
            x=87.0,
            y=360.3603515625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_7 = PhotoImage(
            file=relative_to_assets("entry_7.png"))
        self.entry_bg_7 = self.canvas.create_image(
            230.5,
            420.353759765625,
            image=self.entry_image_7
        )
        self.entry_7 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="grey",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_7.place(
            x=87.0,
            y=410.56256103515625,
            width=287.0,
            height=17.5823974609375
        )
        self.entry_7.insert(0, "09:00 AM - 10:30 AM")
        self.entry_7.bind("<FocusIn>", self.on_focus_in)
        self.entry_7.bind("<FocusOut>", self.on_focus_out)

        self.day = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]
        self.entry_8 = ttk.Combobox(
            background="#FFFFFF",
            foreground="#000716",
            font=("OpenSans Bold", 12 * - 1),
            state="readonly",
            values=self.day,
        )
        self.entry_8.current(0)
        self.entry_8.bind("<FocusIn>", self.change_day)

        self.entry_8.place(
            x=87.0,
            y=460.76470947265625,
            width=287.0,
            height=20
        )

        self.entry_image_9 = PhotoImage(
            file=relative_to_assets("entry_9.png"))
        self.entry_bg_9 = self.canvas.create_image(
            230.5,
            520.7582397460938,
            image=self.entry_image_9
        )
        self.entry_9 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 12 * -1)
        )
        self.entry_9.place(
            x=87.0,
            y=510.967041015625,
            width=287.0,
            height=17.5823974609375
        )

        self.canvas.create_text(
            165.0,
            21.0,
            anchor="nw",
            text="Add Students",
            fill="#9F9F9F",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.canvas.create_text(
            190.0,
            46.0,
            anchor="nw",
            text="Student Info",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            176.0,
            321.0,
            anchor="nw",
            text="Subject Info",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            68.0,
            65.29449462890625,
            anchor="nw",
            text="First name",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            115.4967041015625,
            anchor="nw",
            text="Last name",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            165.6988525390625,
            anchor="nw",
            text="Student ID",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            215.9010009765625,
            anchor="nw",
            text="Course",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            266.103271484375,
            anchor="nw",
            text="Section",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            337.66802978515625,
            anchor="nw",
            text="Course Code",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            387.8702392578125,
            anchor="nw",
            text="Time",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            438.0723876953125,
            anchor="nw",
            text="Day",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            488.274658203125,
            anchor="nw",
            text="Laboratory Room",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 12 * -1)
        )

    def on_focus_in(self, event):
        if self.entry_7.get() == "09:00 AM - 10:30 AM":
            self.entry_7.delete(0, "end")
            self.entry_7.config(fg="#000716", )

    def on_focus_out(self, event):
        if not self.entry_7.get():
            self.entry_7.insert(0, "09:00 AM - 10:30 AM")
            self.entry_7.config(fg="grey")

    def change_day(self, event):
        selected_day = self.entry_8.get()
        print(selected_day)

    def submit(self):
        first_name = self.entry_1.get().capitalize()
        last_name = self.entry_2.get().capitalize()

        # format the student_id into XXXX-XXXXX
        student_id = self.entry_3.get()
        formatted_id = f'{student_id[:4]}-{student_id[5:10]}'

        course = self.entry_4.get().upper()
        section = self.entry_5.get().upper()
        course_code = self.entry_6.get().upper()

        # formatted time into hh:mm or AM/PM
        time_schedule = self.entry_7.get().upper()
        formatted_time_am_am = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} AM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} AM'
        )

        formatted_time_am_pm = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} AM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} PM'
        )

        formatted_time_pm_am = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} PM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} AM'
        )

        formatted_time_pm_pm = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} PM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} PM'
        )

        day_schedule = self.entry_8.get().capitalize()
        lab_room = self.entry_9.get().upper()

        if (
                first_name == "" or last_name == "" or
                student_id == "" or course == "" or
                section == "" or course_code == "" or lab_room == ""
        ):
            messagebox.showerror(
                "Error", "Please don't leave any empty fields."
            )

        elif (
                time_schedule != formatted_time_am_am and
                time_schedule != formatted_time_am_pm and
                time_schedule != formatted_time_pm_am and
                time_schedule != formatted_time_pm_pm
        ):

            messagebox.showerror(
                "Error", "Please enter valid time. It must be in the format 'hh:mm' AM/PM - 'hh:mm' AM/PM."
            )

        elif len(student_id) != 10 or student_id != formatted_id:

            messagebox.showerror(
                "Error", "Invalid Student ID. It must be in the format of XXXX-XXXXX.")

        else:
            exists = check_student(student_id, course_code)
            if exists:
                messagebox.showerror(
                    "Error",
                    f"Student {student_id} is already registered in course {course_code}."
                )
            else:
                self.push_to_database(
                    first_name, last_name,
                    student_id, course,
                    section, course_code,
                    time_schedule, day_schedule,
                    lab_room
                )

    def push_to_database(self, fn, ln, sid, crs, sc, crs_cd, ts, ds, lr):
        print("pushing to database .....")
        query_insert = """
        INSERT INTO students (
        firstname, lastname,
        student_id, course,
        section, course_code,
        time, day, lab_room
        )
        """
        values = f"""
        VALUES (
        '{fn}', '{ln}', '{sid}', 
        '{crs}', '{sc}', '{crs_cd}',
        '{ts}', '{ds}', '{lr}'
        )
        """
        cur.execute(query_insert + values)
        db.commit()

        cur.execute(
            "SELECT * FROM students"
        )
        for x in cur:
            print(x)
        print(cur.rowcount, " students added")

        # create a csv file if not exist
        create_csv(crs_cd)

        # push to csv file
        write_csv(sid, fn, ln, crs, sc, crs_cd, ts, ds, lr)

        self.add()

    def clear_fields(self):
        self.entry_1.delete("0", END)
        self.entry_2.delete("0", END)
        self.entry_3.delete("0", END)
        self.entry_4.delete("0", END)
        self.entry_5.delete("0", END)
        self.entry_6.delete("0", END)
        self.entry_9.delete("0", END)

    def add(self):
        print("opening camera .....")
        student_id = self.entry_3.get()
        course_code = self.entry_6.get().upper()

        user_image_folder = f"./static/faces/{student_id}_{course_code}"

        if not os.path.isdir(user_image_folder):
            os.makedirs(user_image_folder)
        cam = cv2.VideoCapture(0)
        i, j = 0, 0
        while True:
            _, frame = cam.read()
            faces = extract_face(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
                cv2.putText(frame, f'Images Captured: {i}/50', (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
                if j % 10 == 0:
                    name = f"{student_id}_{course_code}_{i}.jpg"
                    cv2.imwrite(f"{user_image_folder}/{name}",
                                frame[y:y + h, x:x + w])
                    i += 1
                j += 1
            if j == 500:
                break
            cv2.imshow("Adding new user", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                r = messagebox.askyesno(
                    "Exit",
                    "Are you sure you want to exit?"
                )
                if r:
                    break
                else:
                    continue
            if cv2.waitKey(1) & 0xFF == ord(' '):
                r = messagebox.askyesno(
                    "Exit",
                    "Are you sure you want to exit?"
                )
                if r:
                    break
                else:
                    continue

        cam.release()
        cv2.destroyAllWindows()
        print("Training Models")
        train_model()

        response = messagebox.askyesno(
            "Success",
            f"Student {student_id} has been registered in course {course_code}."
            f"Do you want to clear all fields?"
        )
        if response:
            self.clear_fields()
        else:
            return

    def test_function(self):
        first_name = self.entry_1.get()
        last_name = self.entry_2.get()
        student_id = self.entry_3.get()
        course = self.entry_4.get()
        section = self.entry_5.get()
        course_code = self.entry_6.get()
        time_sched = self.entry_7.get()
        day_sched = self.entry_8.get()
        lab_room = self.entry_9.get()

        print(first_name, last_name, student_id, course, section, course_code, time_sched, day_sched, lab_room)


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = AddStudentWindow(window)
window.resizable(False, False)
window.mainloop()
