from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from classify import classify


class Interface(tk.Tk):

    def __init__(self):
        """Initialize methods proper to the class"""

        tk.Tk.__init__(self)
        self.create_widgets()
        self.images()
        self.scan_text(self)
        self.clear()

    def create_widgets(self):
        """Create widgets"""

        # Label for text to scan
        self.label_input = tk.Label(self, text="Put here the text to scan", fg="SlateBlue2",
                                    bg="snow", font=("Annabelle 15", 20))
        # Text field for text
        self.text_input = tk.Text(self, width=70, height=20, bd=5, wrap=tk.WORD, bg="light yellow", state=NORMAL,
                                  cursor="mouse", insertbackground="IndianRed2")
        # Mouse activation in the field for text to scan
        self.text_input.insert(tk.INSERT, 1.0)
        # Scroll in the field for text to scan
        self.scroll_input = tk.Scrollbar(orient="vertical", command=self.text_input.yview)
        # Button for scanning the text
        self.button_scan_text = tk.Button(self, text="SCAN", width=15, bg='brown1',
                                          fg='black', font=('Lobster 15 bold', 20),
                                          command=lambda: self.scan_text(self.text_input))
        # Button for saving in file the text
        self.button_save_file = tk.Button(self, text="Save in file", width=15, bg='grey',
                                          fg='black', font=('Lobster 15 bold', 20), command=self.save_in_file)
        # Text field for the result
        self.text_output = tk.Text(self, width=20, height=3, bd=5, wrap=tk.WORD, bg="light yellow", font=("Helvetica", 20))
        # Button for clearing in file the text
        self.button_clear = tk.Button(self, text="Clear", height=2, width=15, bg='light blue',
                                      fg='black', font=('Roboto Slab', 20), command=self.clear)
        # Button to quit the GUI
        self.button_quit = tk.Button(self, text="Quit", height=2, width=15, bg='light blue',
                                     fg='black', font=('Roboto Slab', 20), command=self.quit)
        # Positioning widgets with built-in layout manager grid
        self.label_input.grid(column=1, row=0, sticky=tk.N)
        self.text_input.grid(column=1, row=0, sticky=tk.S)
        self.scroll_input.grid(column=1, row=0, sticky=tk.E)
        self.text_input.config(yscrollcommand=self.scroll_input.set)
        self.button_scan_text.grid(column=1, row=1, sticky=tk.S)
        # self.label_output.grid(column=1, row=2, sticky=tk.N)
        self.text_output.grid(column=1, row=2, sticky=tk.N)
        self.button_save_file.grid(column=1, row=3, sticky=tk.S)
        self.button_clear.grid(column=0, row=2, sticky=tk.N)
        self.button_quit.grid(column=2, row=2, sticky=tk.N)
        # Adjusting the GUI to screen format
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.attributes("-fullscreen", False)
        # self.geometry("600x300")

    def images(self):
        """Add pictures in the GUI and choose a position for them"""

        self.image_1 = Image.open("spam.jpg")
        self.photo_1 = ImageTk.PhotoImage(self.image_1)
        self.img_1 = tk.Label(image=self.photo_1, width=450, height=450)
        self.img_1.image = self.photo_1
        self.img_1.grid(rowspan=2, column=0, row=0)
        self.image_2 = Image.open("ham_.jpg")
        self.photo_2 = ImageTk.PhotoImage(self.image_2)
        self.img_2 = tk.Label(image=self.photo_2, width=450, height=450)
        self.img_2.image = self.photo_2
        self.img_2.grid(rowspan=2, column=2, row=0)

    def scan_text(self, text):
        """Classify texts on spam or ham using classify method"""

        try:
            text = self.text_input.get(1.0, END)
            text_to_scan = self.text_output.insert(END, classify(text))
            return text_to_scan
        except Exception as e:
            messagebox.showerror(e)

    def save_in_file(self):
        """Save ham text into a file"""

        file_path = fd.asksaveasfilename(title="Choose your filename", defaultextension='txt')
        file_type = [('File .txt', '*.txt'), ('File word', '.doc')]
        if not file_type:
            return
        text = self.text_input.get(1.0, END)
        with open(file_path, "w", encoding='utf-8') as output_file:
            output_file.write(f'{str(text)}')

    def clear(self):
        """Clear text fields"""
        self.text_input.delete(1.0, END)
        self.text_output.delete(1.0, END)


app = Interface()
# Label for GUI
app.title("GUI for scanning mails")
# Activation of the GUI
app.mainloop()
