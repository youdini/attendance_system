import csv
import os.path
import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, Frame, BOTH, Scrollbar, messagebox, END, StringVar, \
    Toplevel, filedialog
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
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/list_assets")


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


class ListStudentWindow:
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
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.download,
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
            text="Search a course or course code",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            147.0,
            21.0,
            anchor="nw",
            text="Lists of students",
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


    def update_student(self):
        search = self.search_value.get()
        print("fetching the info .....")

        for row in self.table.get_children():
            self.table.delete(row)

        get_students = f"""
                select student_id, firstname, lastname, course, section,
                 course_code, time, day, lab_room from students where 
                 course like '%{search}%' or course_code like '%{search}%'
                """
        cursor.execute(get_students)
        rows = cursor.fetchall()
        for row in rows:
            data_list = list(row)
            self.table.insert("", END, values=data_list)

    def download(self):
        ask = messagebox.askyesno(
            "Export Data", "Are you sure you want to export the data into CSV file?"
        )
        if ask:
            print("downloading .....")
            search = self.search_value.get().upper()
            print(search)
            if search == "":
                messagebox.showerror("Search Error", "Please enter a course or course code.")
            else:
                data = []
                headers = (
                    "Student ID",
                    "First Name",
                    "Last Name",
                    "Course",
                    "Section",
                    "Course Code",
                    "Time", "Day",
                    "Lab Room"
                )
                data.append(headers)
                for child in self.table.get_children():
                    values = self.table.item(child)["values"]
                    data.append(values)

                # modified version

                # filename = os.path.expanduser(f"~/Downloads/List_of_students_in_{search}.csv")
                # with open(filename, "w", newline="") as f:
                #     writer = csv.writer(f)
                #     writer.writerows(data)
                # messagebox.showinfo("Export to CSV", f"Data exported to {filename}\n"
                #                                      "Do you want to view the file?")
                # answer = messagebox.askyesno("View File", "Do you want to view the file?")
                # if answer:
                #     os.startfile(os.path.dirname(filename))

                file = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    initialfile="List_of_students_in_" + search + ".csv",
                    title="Save CSV File",
                    filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
                )

                if file:
                    with open(file, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerows(data)
                    messagebox.showinfo("Export to CSV", f"Data exported to {file}\nDo you want to view the file?")
                    answer = messagebox.askyesno("View File", "Do you want to view the file?")
                    if answer:
                        os.startfile(os.path.dirname(file))


window = Tk()
app = ListStudentWindow(window)
window.protocol("WM_DELETE_WINDOW", on_close)
window.resizable(False, False)
window.mainloop()
