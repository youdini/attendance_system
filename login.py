import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter import messagebox

import mysql.connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


print("connecting to database ....")

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'
)
cursor = db.cursor()
# create database
cursor.execute(
    "CREATE DATABASE IF NOT EXISTS thesis"
)
cursor.execute(
    "USE thesis"
)

# create table for users
query = ("""
CREATE TABLE IF NOT EXISTS users (
id INT PRIMARY KEY AUTO_INCREMENT, 
username VARCHAR(40), 
password VARCHAR(40)
)
""")
cursor.execute(query)

print("loading modules .....")


def login_function(username, password):
    get_user = """
    SELECT * FROM users WHERE 
    username = '{username}' AND 
    password = '{password}'
    """.format(username=username, password=password)

    if username == '' or password == '':
        messagebox.showerror(
            "Error",
            "Username and Password is required to log in."
        )
    else:
        cursor.execute(get_user)
        data = cursor.fetchall()
        print(data)
        if len(data) == 0:
            messagebox.showerror(
                "Error",
                "Username and Password is incorrect."
            )
        else:
            messagebox.showinfo(
                "Success",
                "Welcome {username}!".format(username=username)
            )
            return True


print("starting .....")


class LoginWindow:
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

        self.username_image = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            753.5,
            325.0,
            image=self.username_image
        )
        self.username = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("ArialMT", 14 * -1)

        )
        self.username.place(
            x=619.0,
            y=309.0,
            width=269.0,
            height=30.0
        )

        self.password_image = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            753.5,
            402.0,
            image=self.password_image
        )
        self.password = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("ArialMT", 14 * -1),
            show="•"
        )
        self.password.place(
            x=619.0,
            y=386.0,
            width=269.0,
            height=30.0
        )

        self.login_image = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.login = Button(
            image=self.login_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.login.place(
            x=591.0,
            y=442.0,
            width=325.0,
            height=50.0
        )

        self.register_image = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.register = Button(
            image=self.register_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.register,
            relief="flat"
        )
        self.register.place(
            x=690.0,
            y=538.0,
            width=128.68695068359375,
            height=26.0
        )

        self.canvas.create_text(
            669.0,
            508.0,
            anchor="nw",
            text="Don’t have an account? ",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            613.0,
            279.0,
            anchor="nw",
            text="Username",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            613.0,
            356.0,
            anchor="nw",
            text="Password",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            97.0,
            293.0,
            anchor="nw",
            text="Face Recognition\nStudent Identifier",
            fill="#FFFFFF",
            font=("Arial BoldMT", 32 * -1)
        )

        self.password.focus_set()
        self.username.focus_set()
        self.register.focus_set()
        self.login.focus_set()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        print(username, password)
        success = login_function(username, password)
        if success:
            self.master.destroy()
            subprocess.run(['python', './home.py'])
        else:
            pass

    def test_function(self):
        username = self.username.get()
        password = self.password.get()
        print(username, password)

    def register(self):
        self.master.destroy()
        subprocess.run(['python', 'register.py'])


window = Tk()
app = LoginWindow(window)
window.resizable(False, False)
window.mainloop()
