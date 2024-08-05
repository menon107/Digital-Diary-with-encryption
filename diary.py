import datetime
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class DiaryApp:
    def _init_(self, master):
        self.master = master
        self.master.title('Diary')
        self.create_directory()

        self.text_entry = tk.Text(self.master, height=20, width=50)
        self.text_entry.pack()

        self.save_button = tk.Button(self.master, text='Save', command=self.save_entry)
        self.save_button.pack()

        self.read_button = tk.Button(self.master, text='Read', command=self.read_entries)
        self.read_button.pack()

        self.quit_button = tk.Button(self.master, text='Quit', command=self.master.quit)
        self.quit_button.pack()

    def create_directory(self):
        today = datetime.date.today()
        directory_name = today.strftime("%Y-%m-%d")

        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

    def save_entry(self):
        entry_content = self.text_entry.get("1.0", 'end-1c')

        if not entry_content:
            messagebox.showwarning("Warning", "Please enter a diary entry before saving.")
            return

        today = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H-%M-%S")
        filename = f"{today} {current_time}.txt"
        directory_name = today.strftime("%Y-%m-%d")

        file_path = os.path.join(directory_name, filename)

        with open(file_path, 'w') as file:
            file.write(entry_content)

        messagebox.showinfo("Success", f"Diary entry saved successfully.\nFile: {file_path}")

    def read_entries(self):
        today = datetime.date.today()
        directory_name = today.strftime("%Y-%m-%d")

        files = os.listdir(directory_name)

        if not files:
            messagebox.showinfo("Info", "No diary entries found.")
            return

        files.sort(reverse=True)  # Sort files by date, newest first

        # Create a list of file paths
        file_paths = [os.path.join(directory_name, file) for file in files]

        # Display a listbox with all previous entries
        listbox_window = Toplevel(self.master)
        listbox_window.title("Previous Entries")

        listbox = Listbox(listbox_window, selectmode=SINGLE)
        for path in file_paths:
            listbox.insert(END, os.path.basename(path))

        listbox.pack()

        # Buttons for view and delete
        view_button = Button(listbox_window, text="View", command=lambda: self.view_selected_entry(listbox.get(listbox.curselection())))
        view_button.pack()

        delete_button = Button(listbox_window, text="Delete", command=lambda: self.delete_selected_entry(listbox, listbox.get(listbox.curselection())))
        delete_button.pack()

    def view_selected_entry(self, selected_file):
        today = datetime.date.today()
        directory_name = today.strftime("%Y-%m-%d")
        file_path = os.path.join(directory_name, selected_file)

        with open(file_path, 'r') as file:
            content = file.read()

        messagebox.showinfo("Diary Entry", content)

    def delete_selected_entry(self, listbox, selected_file):
        today = datetime.date.today()
        directory_name = today.strftime("%Y-%m-%d")
        file_path = os.path.join(directory_name, selected_file)

        try:
            os.remove(file_path)
            messagebox.showinfo("Success", f"Entry '{selected_file}' deleted successfully.")
            listbox.delete(listbox.curselection())
        except FileNotFoundError:
            messagebox.showinfo("Info", "File not found.")
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")

class LoginInterface(Frame):
    def _init_(self, master=None):
        Frame._init_(self, master)
        self.master = master
        self.security()

    def security(self):
        self.master.title("LOGIN")
        self.pack(fill=BOTH, expand=1)
        lbl = Label(self, text="PASSWORD").grid(column=0, row=0)

        self.pwrd = Entry(self, show="*")
        self.pwrd.focus_set()
        self.pwrd.grid(column=1, row=0)

        login = Button(self, text="Login", width=20, command=self.login)
        login.grid(column=1, row=2)

    def login(self):
        if self.pwrd.get() == "your_password":  # Replace "your_password" with the actual password
            self.destroy()

            diary_app = Tk()
            diary_app.geometry("500x500")
            app_b = DiaryApp(diary_app)
            diary_app.mainloop()

        else:
            messagebox.showinfo("ERROR", "Retry wrong password")

if _name_ == "_main_":
    root = Tk()
    root.geometry("250x50")
    app = LoginInterface(root)
    app.mainloop()