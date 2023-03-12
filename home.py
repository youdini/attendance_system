import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox

import cv2
import joblib
import mysql.connector as connector
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# create dir if no exist
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')

print("loading modules....")
print("connecting to database....")
# database
db = connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='thesis'
)
cursor = db.cursor()

create_table_attendance = """
CREATE TABLE IF NOT EXISTS attendance 
(att_id INT AUTO_INCREMENT PRIMARY KEY, 
firstname VARCHAR(40), 
lastname VARCHAR(40), 
student_id VARCHAR(10), 
course_code VARCHAR(40), 
time_in VARCHAR(40), 
time_out VARCHAR(40), 
date_attend VARCHAR(40), 
day_attend VARCHAR(40), 
lab_room VARCHAR(40))
"""

create_table_student = """
CREATE TABLE IF NOT EXISTS students (
id INT PRIMARY KEY AUTO_INCREMENT, 
firstname VARCHAR(40), lastname VARCHAR(40), 
course VARCHAR(50), section VARCHAR(40), 
student_id VARCHAR(10), course_code VARCHAR(40), 
time VARCHAR(40), day VARCHAR(40), 
lab_room VARCHAR(40) 
)
"""

cursor.execute(create_table_student)
cursor.execute(create_table_attendance)
print("loading.....")
# global variables
global identified_person

# time and date
CURRENT_TIME = time.strftime("%I:%M %p", time.localtime())
CURRENT_DATE = datetime.now().strftime("%B %d, %Y")
CURRENT_DAY = datetime.now().strftime("%A")

# face detector variable using haar cascade
face_detector = cv2.CascadeClassifier(
    "./resources/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    print("extracting face: ", face_points)
    return face_points


def identify_face(face_array):
    model = joblib.load('./static/face_recognition_model.pkl')
    face = model.predict(face_array)
    print("identified face: ", face)
    if len(face) == 0:
        return "Not Registered"
    else:
        return face


def train_model():
    print("training model....")
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
    print("opening camera please wait....")
    global identified_person
    cam = cv2.VideoCapture(0)
    ret = True
    while ret:
        ret, frame = cam.read()

        if len(extract_face(frame)) > 0:
            (x, y, w, h) = extract_face(frame)[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            proba = identify_face(face.reshape(1, -1))[0]
            knn = joblib.load('static/face_recognition_model.pkl')
            proba_matrix = knn.predict_proba(face.reshape(1, -1))
            max_proba = np.max(proba_matrix)
            accuracy = round(max_proba * 100, 2)
            cv2.putText(frame, f'{identified_person} ({accuracy}) ',
                        (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord(' '):
            break
    cam.release()
    cv2.destroyAllWindows()
    train_model()
    return identified_person


def push_record(student_id, course_code, category):
    print("fetching data .....")
    # get the info of the students
    get_info = f"""
    select firstname, lastname,
    lab_room from students where 
    student_id = '{student_id}' and 
    course_code = '{course_code}'
    """
    cursor.execute(get_info)
    data = cursor.fetchone()
    firstname = data[0]
    lastname = data[1]
    lab_room = data[2]

    # checking attendance
    print("checking attendance....")
    exists = check_attendance(student_id, course_code, lab_room)
    if exists is None:
        # push the data
        print("push data to database ....")
        insert_data = f"""
        insert into attendance ( 
        firstname, lastname,
        student_id, course_code, 
        time_in, time_out, date_attend,
        day_attend, lab_room) values (
        '{firstname}', '{lastname}', 
        '{student_id}', '{course_code}', 
        '{CURRENT_TIME}', '{""}', '{CURRENT_DATE}',
        '{CURRENT_DAY}', '{lab_room}')
        """
        cursor.execute(insert_data)
        db.commit()
        messagebox.showinfo(
            "Success",
            f"Student {student_id} has timed in Lab Room {lab_room} with the course {course_code}.\n"
            f"{category}: {CURRENT_TIME}"
        )
    else:
        # update time out
        print("updating record .....")
        update_timeout = f"""
        update attendance set time_out = '{CURRENT_TIME}' where 
        student_id = '{student_id}' and course_code = '{course_code}' and 
        date_attend = '{CURRENT_DATE}' and lab_room = '{lab_room}'
        """
        cursor.execute(update_timeout)
        db.commit()
        print(cursor.rowcount, "row updated")
        messagebox.showinfo(
            "Success",
            f"Student {student_id} has timed in Lab Room {lab_room} with the course {course_code}.\n"
            f"Time Out: {CURRENT_TIME}"
        )
        cursor.execute("select * from attendance")
        print(cursor.fetchall())


def time_in_function():
    exists = no_face_error()
    if exists:
        student = face_recognition()
        student_id = student.split("_")[0]
        course_code = student.split("_")[1]
        insert_record(student_id, course_code)
    else:
        messagebox.showerror("No Registered Students",
                             "There are no face registered. Register first before using the attendance.")


def time_out_function():
    exists = no_face_error()
    if exists:
        student = face_recognition()
        student_id = student.split("_")[0]
        course_code = student.split("_")[1]
        update_record(student_id, course_code)
    else:
        messagebox.showerror("No Registered Students",
                             "There are no face registered. Register first before using the attendance.")


def check_attendance(student_id, course_code, lab_room):
    get_attendance = f"""
    select * from attendance where 
    student_id = '{student_id}' and 
    course_code = '{course_code}' and 
    date_attend = '{CURRENT_DATE}' and 
    lab_room = '{lab_room}'
    """
    cursor.execute(get_attendance)
    return cursor.fetchone()


def check_row(student_id, course_code):
    get_attendance = f"""
    select * from attendance where 
    student_id = '{student_id}' and 
    course_code = '{course_code}' and 
    date_attend = '{CURRENT_DATE}'
    """
    cursor.execute(get_attendance)
    return cursor.fetchone()

def insert_record(student_id, course_code):
    current_time = time.strftime("%I:%M %p", time.localtime())
    print("fetching data .....")
    # get the info of the students
    get_info = f"""
    select firstname, lastname,
    lab_room from students where 
    student_id = '{student_id}' and 
    course_code = '{course_code}'
    """
    cursor.execute(get_info)
    data = cursor.fetchone()
    firstname = data[0]
    lastname = data[1]
    lab_room = data[2]
    exists = check_row(student_id, course_code)
    if exists is None:
        # insert data
        print("inserting data to database .......")
        # push the data
        print("push data to database ....")
        insert_data = f"""
                insert into attendance ( 
                firstname, lastname,
                student_id, course_code, 
                time_in, time_out, date_attend,
                day_attend, lab_room) values (
                '{firstname}', '{lastname}', 
                '{student_id}', '{course_code}', 
                '{current_time}', '{""}', '{CURRENT_DATE}',
                '{CURRENT_DAY}', '{lab_room}')
                """
        cursor.execute(insert_data)
        db.commit()
        messagebox.showinfo(
            "Success",
            f"Time In: {current_time}"
        )
    else:
        messagebox.showerror("Time In Error", "You already timed in this day.")


def update_record(student_id, course_code):
    current_time = time.strftime("%I:%M %p", time.localtime())
    exists = check_row(student_id, course_code)
    if exists is None:
        messagebox.showerror("No Record Found", "Please Time In first.")
    else:
        print("updating ....")
        update_timeout = f"""
                update attendance set time_out = '{current_time}' where 
                student_id = '{student_id}' and course_code = '{course_code}' and 
                date_attend = '{CURRENT_DATE}'
                """
        cursor.execute(update_timeout)
        db.commit()
        print(cursor.rowcount, "row updated")
        messagebox.showinfo(
            "Success",
            f"Time Out: {current_time}"
        )
        cursor.execute("select * from attendance")
        print(cursor.fetchall())

def no_face_error():
    if len(os.listdir('./static/faces')) > 0:
        return True
    else:
        return False


# test funtction
def test_function():
    print(CURRENT_TIME)

print("window is opening....")


class HomeWindow:
    def __init__(self, master):
        self.master = master

        self.master.geometry("1000x600")
        self.master.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            500.0,
            300.0,
            image=self.image_image_1
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_student,
            relief="flat"
        )
        self.button_1.place(
            x=522.0,
            y=106.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.update_student,
            relief="flat"
        )
        self.button_2.place(
            x=522.0,
            y=181.2080535888672,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_student,
            relief="flat"
        )
        self.button_3.place(
            x=522.0,
            y=256.4161071777344,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.list_student,
            relief="flat"
        )
        self.button_4.place(
            x=522.0,
            y=331.6241455078125,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.record_student,
            relief="flat"
        )
        self.button_5.place(
            x=524.0,
            y=407.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=test_function,
            relief="flat"
        )
        self.button_6.place(
            x=22.0,
            y=332.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        self.button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=time_out_function,
            relief="flat"
        )
        self.button_7.place(
            x=22.0,
            y=407.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_8 = PhotoImage(
            file=relative_to_assets("button_8.png"))
        self.button_8 = Button(
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=self.logout_function,
            relief="flat"
        )
        self.button_8.place(
            x=879.0,
            y=543.0,
            width=102.0,
            height=36.0
        )

    def add_student(self):
        self.master.destroy()
        subprocess.run(['python', './addstudent.py'])

    def update_student(self):
        self.master.destroy()
        subprocess.run(['python', './updatestudent.py'])

    def delete_student(self):
        self.master.destroy()
        subprocess.run(['python', './deletestudents.py'])

    def list_student(self):
        self.master.destroy()
        subprocess.run(['python', './liststudent.py'])

    def record_student(self):
        self.master.destroy()
        subprocess.run(['python', './attendance.py'])

    def logout_function(self):
        response = messagebox.askyesno(
            "Logout", "Are you sure you want to log out?"
        )
        if response:
            self.master.destroy()
            subprocess.run(["python", "./login.py"])


window = Tk()
app = HomeWindow(window)
window.resizable(False, False)
window.mainloop()
