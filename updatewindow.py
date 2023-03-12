from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from courier import Courier
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

ASSETS_PATH_UPDATE_WINDOW = OUTPUT_PATH / Path(r".\assets\frame8")


def assets_update_window(path: str) -> Path:
    return ASSETS_PATH_UPDATE_WINDOW / Path(path)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def update_window_on_close():
    response = messagebox.askyesno("Cancel", "Are you sure you want to cancel the update?")
    if response:
        update_window.destroy()
    else:
        return


class UpdateWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("462x602")
        self.master.configure(bg="#FFFFFF")
        print(Courier.name)

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
            file=assets_update_window("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.update_info,
            relief="flat",
            master=self.master
        )
        self.button_1.place(
            x=163.0,
            y=554.0,
            width=135.71435546875,
            height=35.6824951171875
        )

        self.image_image_1 = PhotoImage(
            file=assets_update_window("image_1.png"))
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
            font=("ArialMT", 14 * -1)
        )
        self.entry_1.place(
            x=87.0,
            y=87.98681640625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_2 = PhotoImage(
            file=assets_update_window("entry_2.png"))
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
            font=("ArialMT", 14 * -1)
        )
        self.entry_2.place(
            x=87.0,
            y=138.18896484375,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_3 = PhotoImage(
            file=assets_update_window("entry_3.png"))
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
            font=("ArialMT", 14 * -1)
        )
        self.entry_3.place(
            x=87.0,
            y=188.39117431640625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_4 = PhotoImage(
            file=assets_update_window("entry_4.png"))
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
            font=("ArialMT", 14 * -1)
        )
        self.entry_4.place(
            x=87.0,
            y=238.59332275390625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_5 = PhotoImage(
            file=assets_update_window("entry_5.png"))
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
            font=("ArialMT", 14 * -1)
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
            font=("ArialMT", 14 * -1)
        )
        self.entry_6.place(
            x=87.0,
            y=360.3603515625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_7 = PhotoImage(
            file=assets_update_window("entry_7.png"))
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
            font=("ArialMT", 14 * -1)
        )
        self.entry_7.place(
            x=87.0,
            y=410.56256103515625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_8 = PhotoImage(
            file=assets_update_window("entry_8.png"))
        self.entry_bg_8 = self.canvas.create_image(
            230.5,
            470.555908203125,
            image=self.entry_image_8
        )
        self.entry_8 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            master=self.master,
            font=("ArialMT", 14 * -1)
        )
        self.entry_8.place(
            x=87.0,
            y=460.76470947265625,
            width=287.0,
            height=17.5823974609375
        )

        self.entry_image_9 = PhotoImage(
            file=assets_update_window("entry_9.png"))
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
            font=("ArialMT", 14 * -1)
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

    def update_info(self):
        print("updating .....")


update_window = Tk()
update_window.protocol("WM_DELETE_WINDOW", update_window_on_close)
update_app = UpdateWindow(update_window)
update_window.mainloop()
