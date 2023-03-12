import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

import mysql.connector

OUTPUT_PATH = Path(__file__).parent
print(OUTPUT_PATH)
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame1")
print(ASSETS_PATH)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='thesis'
)
cursor = db.cursor()


def register_function(username, password, confirm_password):

    if (
            username == "" or
            password == "" or
            confirm_password == ""
    ):
        messagebox.showerror(
            'Error',
            "Please don't leave a blank."
        )
    else:
        if password != confirm_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )
        else:
            print(username, password, confirm_password)

            get_username = """
            SELECT * FROM users WHERE 
            username = '{username}'
            """.format(username=username)
            cursor.execute(get_username)
            exists = cursor.fetchall()
            print(exists)
            if len(exists) > 0:
                messagebox.showerror(
                    "Error",
                    "Username is already taken."
                )

            else:
                push = """
                INSERT INTO users (username, password) 
                VALUES ('{username}', '{password}')
                """.format(username=username, password=password)
                cursor.execute(push)
                db.commit()
                messagebox.showinfo(
                    "Success!",
                    "Registered successfully."
                )
                return True


class RegisterWindow:
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
            301.0,
            image=self.image_image_1
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.register,
            relief="flat"
        )
        self.button_1.place(
            x=547.0,
            y=390.88629150390625,
            width=405.0,
            height=55.846160888671875
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.button_2.place(
            x=668.4073486328125,
            y=510.6722412109375,
            width=162.185302734375,
            height=28.3277587890625
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            749.5,
            154.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("ArialMT", 14 * -1)
        )
        self.entry_1.place(
            x=582.0,
            y=137.0,
            width=335.0,
            height=33.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            749.5,
            242.5,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("ArialMT", 14 * -1),
            show="•"

        )
        self.entry_2.place(
            x=582.0,
            y=225.0,
            width=335.0,
            height=33.0
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(
            749.5,
            330.5,
            image=self.entry_image_3
        )
        self.entry_3 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("ArialMT", 14 * -1),
            show="•"

        )
        self.entry_3.place(
            x=582.0,
            y=313.0,
            width=335.0,
            height=33.0
        )

        self.canvas.create_text(
            664.0,
            61.0,
            anchor="nw",
            text="Register",
            fill="#A1A1A1",
            font=("ArialMT", 30 * -1)
        )

        self.canvas.create_text(
            582.0,
            105.0,
            anchor="nw",
            text="Username",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            582.0,
            193.0,
            anchor="nw",
            text="Password",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            582.0,
            282.0,
            anchor="nw",
            text="Confirm Password",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            649.0,
            473.0,
            anchor="nw",
            text="Already have an account?",
            fill="#8E8E8E",
            font=("ArialMT", 14 * -1)
        )

        self.canvas.create_text(
            116.0,
            293.0,
            anchor="nw",
            text="Face Recognition\nStudent Identifier",
            fill="#FFFFFF",
            font=("Arial BoldMT", 32 * -1)
        )

    def test_function(self):
        username = self.entry_1.get()
        password = self.entry_2.get()
        confirm_password = self.entry_3.get()
        print(username, password, confirm_password)

    def login(self):
        self.master.destroy()
        subprocess.run(['python', './login.py'])

    def register(self):
        username = self.entry_1.get()
        password = self.entry_2.get()
        confirm_password = self.entry_3.get()
        success = register_function(username, password, confirm_password)
        if success:
            self.login()
        else:
            pass


window = Tk()
app = RegisterWindow(window)
window.resizable(False, False)
window.mainloop()
