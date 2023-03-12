import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, Frame, BOTH, Scrollbar, messagebox, END, StringVar, \
    Toplevel
from tkinter.ttk import Style, Combobox

import mysql.connector as conn

print("connecting to database .....")
db = conn.connect(
    host='localhost',
    user='root',
    password='root',
    database='thesis'
)
cursor = db.cursor()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame5")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_close():
    response = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if response:
        window.destroy()
        subprocess.run(["python", "./home.py"])
    else:
        return


print("starting .....")


class UpdateStudentWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("462x602")
        self.master.configure(bg="#FFFFFF")
        self.search_value = StringVar()
        self.search_value.trace("w", lambda *args: self.update_student())

        self.canvas = Canvas(
            self.master,
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
            borderwidth=0,
            highlightthickness=0,
            # command=self.open_update_window,
            relief="flat"
        )
        self.button_1.place(
            x=163.0,
            y=554.0,
            width=135.71435546875,
            height=35.6824951171875
        )

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            232.0,
            301.0,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            231.5,
            99.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 14 * -1),
            textvariable=self.search_value
        )
        self.entry_1.place(
            x=87.0,
            y=82.0,
            width=289.0,
            height=32.0
        )

        self.canvas.create_text(
            69.0,
            58.0,
            anchor="nw",
            text="Search a student by name",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            147.0,
            21.0,
            anchor="nw",
            text="Update Students",
            fill="#9F9F9F",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.frame = Frame(self.canvas, bg="#fff")
        self.frame.place(x=32, y=145, width=400, height=360)

        self.heading = ttk.Style()
        self.heading.configure(
            "Treeview.Heading",
            font=("OpenSansRoman Bold", 18 * -1),
        )
        self.tree_style = Style()
        self.tree_style.configure(
            "Custom.Treeview",
            font=("OpenSansRoman Bold", 14 * -1),
            rowheight=50,
        )

        self.table = ttk.Treeview(
            self.frame,
            columns=(
                "Student ID",
                "First Name",
                "Last Name",
                "Course",
                "Section",
                "Course Code",
                "Time", "Day",
                "Lab Room"
            ), show="headings",
            style="Custom.Treeview",
            cursor="hand2"
        )

        self.table.pack(fill=BOTH, expand=True)

        self.table.heading("Student ID", text="Student ID")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Course", text="Course")
        self.table.heading("Section", text="Section")
        self.table.heading("Course Code", text="Course Code")
        self.table.heading("Time", text="Time")
        self.table.heading("Day", text="Day")
        self.table.heading("Lab Room", text="Lab Room")

        self.scrollX = Scrollbar(self.table, orient="horizontal", command=self.table.xview)
        self.scrollX.pack(side="bottom", fill="x")

        self.scrollY = Scrollbar(self.table, orient="vertical", command=self.table.yview)
        self.scrollY.pack(side="right", fill="y")
        self.table.configure(xscrollcommand=self.scrollX.set, yscrollcommand=self.scrollY.set)

        # bind a command in table
        self.table.bind("<ButtonRelease-1>", self.selected_item)

        self.get_students()

    def get_students(self):
        print("fetching the info .....")
        get_students = """
        select student_id, firstname, lastname, course, section,
         course_code, time, day, lab_room from students
        """
        cursor.execute(get_students)
        rows = cursor.fetchall()
        for row in rows:
            data_list = list(row)
            self.table.insert("", END, values=data_list)

    def selected_item(self, event):
        get_item = self.table.focus()
        print(get_item)
        print(self.table.item(get_item))
        values = self.table.item(get_item)['values']
        if len(values) > 0:
            student_id = values[0]
            firstname = values[1]
            lastname = values[2]
            course = values[3]
            section = values[4]
            course_code = values[5]
            time_sched = values[6]
            day_sched = values[7]
            lab_room = values[8]
            print(student_id, firstname, lastname, course, section, course_code, time_sched, day_sched, lab_room)

            self.master.withdraw()
            openwindow = Toplevel(self.master)
            UpdateWindow(
                openwindow,
                firstname, lastname, course,
                section, student_id, course_code,
                time_sched, day_sched, lab_room, self
            )

        else:
            return

    def update_student(self):
        search = self.search_value.get()
        print("fetching the info .....")

        for row in self.table.get_children():
            self.table.delete(row)

        get_students = f"""
                select student_id, firstname, lastname, course, section,
                 course_code, time, day, lab_room from students where firstname like 
                 '%{search}%' or lastname like '%{search}%' or student_id like '%{search}%' or
                 course like '%{search}%'
                """
        cursor.execute(get_students)
        rows = cursor.fetchall()
        for row in rows:
            data_list = list(row)
            self.table.insert("", END, values=data_list)


ASSETS_PATH_UPDATE_WINDOW = OUTPUT_PATH / Path(r".\assets\frame8")


def assets_update_window(path: str) -> Path:
    return ASSETS_PATH_UPDATE_WINDOW / Path(path)


def get_id(student_id, firstname, lastname, course, section, course_code, time, day, lab_room):
    get_id_query = f"""
    SELECT id from students WHERE student_id = '{student_id}' AND firstname = '{firstname}' 
    AND lastname ='{lastname}' AND course = '{course}' AND section = '{section}' AND 
    course_code ='{course_code}' AND time = '{time}' AND day = '{day}' AND 
    lab_room = '{lab_room}'
    """
    cursor.execute(get_id_query)
    fetch_id = cursor.fetchone()
    print(fetch_id)
    print(fetch_id[0])
    return fetch_id[0]


def check_student(sid, crs_cd):
    cursor.execute(
        "SELECT student_id FROM students "
        f"WHERE student_id = '{sid}' AND course_code = '{crs_cd}'")
    result = cursor.fetchone()
    if result is None:
        print(f"Student {sid} is not registered, Available!")
        return False
    else:
        return True


class UpdateWindow:
    def __init__(
            self, master,
            firstname, lastname,
            course, section,
            student_id, course_code,
            time, day, lab_room,
            main_window
    ):
        self.master = master
        self.master.geometry("462x602")
        self.master.configure(bg="#FFFFFF")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.firstname = StringVar()
        self.lastname = StringVar()
        self.course = StringVar()
        self.section = StringVar()
        self.student_id = StringVar()
        self.course_code = StringVar()
        self.time = StringVar()
        self.day_sched = day
        self.lab_room = StringVar()

        self.firstname.set(firstname)
        self.lastname.set(lastname)
        self.course.set(course)
        self.section.set(section)
        self.student_id.set(student_id)
        self.course_code.set(course_code)
        self.time.set(time)
        self.lab_room.set(lab_room)
        self.main_window = main_window

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=602,
            width=462,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.button_image_1 = PhotoImage(
            file=assets_update_window("button_1.png"),
            master=self.master
        )
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.submit,
            relief="flat",
            master=self.master,
            cursor="hand2"
        )
        self.button_1.place(
            x=163.0,
            y=554.0,
            width=135.71435546875,
            height=35.6824951171875
        )

        self.image_image_1 = PhotoImage(
            file=assets_update_window("image_1.png"),
            master=self.master)
        self.image_1 = self.canvas.create_image(
            230.0,
            308.53619384765625,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=assets_update_window("entry_1.png"))
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
            font=("ArialMT", 14 * -1),
            master=self.master,
            textvariable=self.firstname,
        )
        self.entry_1.place(
            x=87.0,
            y=87.98681640625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_2 = PhotoImage(
            file=assets_update_window("entry_2.png"),
            master=self.master)
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
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.lastname
        )
        self.entry_2.place(
            x=87.0,
            y=138.18896484375,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_3 = PhotoImage(
            file=assets_update_window("entry_3.png"),
            master=self.master)
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
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.student_id
        )
        self.entry_3.place(
            x=87.0,
            y=188.39117431640625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_4 = PhotoImage(
            file=assets_update_window("entry_4.png"),
            master=self.master)
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
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.course
        )
        self.entry_4.place(
            x=87.0,
            y=238.59332275390625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_5 = PhotoImage(
            file=assets_update_window("entry_5.png"),
            master=self.master)
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
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.section
        )
        self.entry_5.place(
            x=87.0,
            y=288.7955322265625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_6 = PhotoImage(
            file=assets_update_window("entry_6.png"))
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
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.course_code
        )
        self.entry_6.place(
            x=87.0,
            y=360.3603515625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_7 = PhotoImage(
            file=assets_update_window("entry_7.png"),
            master=self.master)
        self.entry_bg_7 = self.canvas.create_image(
            230.5,
            420.353759765625,
            image=self.entry_image_7
        )
        self.entry_7 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.time
        )
        self.entry_7.place(
            x=87.0,
            y=410.56256103515625,
            width=287.0,
            height=17.5823974609375
        )

        # self.entry_image_8 = PhotoImage(
        #     file=assets_update_window("entry_8.png"),
        #     master=self.master)
        # self.entry_bg_8 = self.canvas.create_image(
        #     230.5,
        #     470.555908203125,
        #     image=self.entry_image_8
        # )
        # self.entry_8 = Entry(
        #     bd=0,
        #     bg="#FFFFFF",
        #     fg="#000716",
        #     highlightthickness=0,
        #     master=self.master,
        #     font=("ArialMT", 14 * -1),
        #     textvariable=self.day
        # )

        self.day = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]

        index = self.day.index(self.day_sched)

        self.entry_8 = Combobox(
            background="#FFFFFF",
            foreground="#000716",
            font=("OpenSans Bold", 12 * - 1),
            state="readonly",
            values=self.day,
            master=self.master,
            height=50
        )
        self.entry_8.current(index)
        self.entry_8.bind("<FocusIn>", self.change_day)

        self.entry_8.place(
            x=87.0,
            y=460.76470947265625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_9 = PhotoImage(
            file=assets_update_window("entry_9.png"),
            master=self.master)
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
            master=self.master,
            font=("ArialMT", 14 * -1),
            textvariable=self.lab_room
        )
        self.entry_9.place(
            x=87.0,
            y=510.967041015625,
            width=287.0,
            height=17.5823974609375
        )

        self.canvas.create_text(
            147.0,
            15.0,
            anchor="nw",
            text="Update Students",
            fill="#9F9F9F",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.canvas.create_text(
            192.0,
            47.0,
            anchor="nw",
            text="Student Info",
            fill="#9F9F9F",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            194.0,
            319.0,
            anchor="nw",
            text="Subject Info",
            fill="#9F9F9F",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            68.0,
            66.29449462890625,
            anchor="nw",
            text="First name",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            116.4967041015625,
            anchor="nw",
            text="Last name",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            166.6988525390625,
            anchor="nw",
            text="Student ID",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            216.9010009765625,
            anchor="nw",
            text="Course",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            267.103271484375,
            anchor="nw",
            text="Section",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            338.66802978515625,
            anchor="nw",
            text="Course Code",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            388.8702392578125,
            anchor="nw",
            text="Time",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            439.0723876953125,
            anchor="nw",
            text="Day",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.canvas.create_text(
            68.0,
            489.274658203125,
            anchor="nw",
            text="Laboratory Room",
            fill="#9F9F9F",
            font=("ArialMT", 12 * -1)
        )

        self.id = get_id(student_id, firstname, lastname, course, section, course_code, time, day, lab_room)

    def on_close(self):
        self.master.destroy()
        self.main_window.master.update()
        self.main_window.master.deiconify()

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
        firstname = self.firstname.get().capitalize()
        lastname = self.lastname.get().capitalize()
        student_id = self.student_id.get()
        course = self.course.get().upper()
        section = self.section.get().upper()
        course_code = self.course_code.get().upper()
        time = self.time.get().upper()
        day = self.entry_8.get().capitalize()
        lab_room = self.lab_room.get().upper()
        data_id = self.id
        print(firstname, lastname, student_id, course, section, course_code, time, day, lab_room, data_id)

        formatted_id = f'{student_id[:4]}-{student_id[5:10]}'
        print(formatted_id, student_id)

        formres = len(student_id) != 10 or formatted_id != student_id
        print(formres)

        formatted_time_am_am = (
            f'{time[:2]}:{time[3:5]} AM - '
            f'{time[11:13]}:{time[14:16]} AM'
        )

        formatted_time_am_pm = (
            f'{time[:2]}:{time[3:5]} AM - '
            f'{time[11:13]}:{time[14:16]} PM'
        )

        formatted_time_pm_am = (
            f'{time[:2]}:{time[3:5]} PM - '
            f'{time[11:13]}:{time[14:16]} AM'
        )

        formatted_time_pm_pm = (
            f'{time[:2]}:{time[3:5]} PM - '
            f'{time[11:13]}:{time[14:16]} PM'
        )
        print(len(student_id))

        # exists = check_student(student_id, course_code)

        if (
                firstname == "" or lastname == "" or student_id == "" or course == "" or section == "" or
                course_code == "" or time == "" or day == "" or lab_room == ""
        ):
            messagebox.showerror("Field Empty", "All fields are required")
        elif len(student_id) != 10 or formatted_id != student_id:
            messagebox.showerror("Student ID Invalid", "Student ID must be in the format of XXXX-XXXXX.")
        elif (
                time != formatted_time_am_am and
                time != formatted_time_am_pm and
                time != formatted_time_pm_am and
                time != formatted_time_pm_pm
        ):
            messagebox.showerror("Time Format Error", "Time must be in the format of 09:00 AM - 10:30 PM")
        # elif exists:
        #     messagebox.showerror("Student Registered",
        #                          f"Student {student_id} is currently registered in course {course_code}.")
        else:

            response = messagebox.askyesno("Update", "Are you sure you want to update the student information?")
            if response:
                print("updating ......")
                update_data = f"""
                UPDATE students SET firstname = '{firstname}', lastname = '{lastname}', student_id = '{student_id}', 
                course = '{course}', section = '{section}', time = '{time}', day = '{day}', lab_room = '{lab_room}' 
                WHERE id = '{data_id}'
                """
                cursor.execute(update_data)
                db.commit()
                messagebox.showinfo("Success", "Student Information Updated")
                quit_window = messagebox.askyesno("Close", "Do you want to close the update window?")
                if quit_window:
                    self.master.destroy()
                    self.main_window.master.destroy()
                    subprocess.run(["python", "updatestudent.py"])
                else:
                    return
            else:
                return


window = Tk()
app = UpdateStudentWindow(window)
window.protocol("WM_DELETE_WINDOW", on_close)
window.resizable(False, False)
window.mainloop()
