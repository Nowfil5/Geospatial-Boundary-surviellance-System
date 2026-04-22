from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient

class IDGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ID Generator")
        self.root.geometry("1400x768")
        self.root.configure(bg="black")

        # MongoDB Connection
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["FishingDatabase"]
        self.collection = self.db["Fishermen"]

        # GUI Setup
        self.frame = Frame(self.root, bg="white", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text="Aadhar Number:", font=("Arial", 16), bg="white").grid(row=0, column=0, pady=5, padx=10)
        Label(self.frame, text="Unique ID:", font=("Arial", 16), bg="white").grid(row=1, column=0, pady=5, padx=10)
        Label(self.frame, text="Name:", font=("Arial", 16), bg="white").grid(row=2, column=0, pady=5, padx=10)
        Label(self.frame, text="Age:", font=("Arial", 16), bg="white").grid(row=3, column=0, pady=5, padx=10)
        Label(self.frame, text="Fishing Area:", font=("Arial", 16), bg="white").grid(row=4, column=0, pady=5, padx=10)

        self.entry_aadhar = Entry(self.frame, font=("Arial", 16))
        self.entry_aadhar.grid(row=0, column=1, pady=5, padx=10)
        self.entry_id = Entry(self.frame, font=("Arial", 16))
        self.entry_id.grid(row=1, column=1, pady=5, padx=10)
        self.entry_name = Entry(self.frame, font=("Arial", 16))
        self.entry_name.grid(row=2, column=1, pady=5, padx=10)
        self.entry_age = Entry(self.frame, font=("Arial", 16))
        self.entry_age.grid(row=3, column=1, pady=5, padx=10)
        self.entry_area = Entry(self.frame, font=("Arial", 16))
        self.entry_area.grid(row=4, column=1, pady=5, padx=10)

        Button(self.frame, text="Submit", font=("Arial", 16), command=self.submit_data, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=10)
        Button(self.frame, text="Back", font=("Arial", 16), command=self.go_back, bg="red", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

    def submit_data(self):
        aadhar = self.entry_aadhar.get()
        unique_id = self.entry_id.get()
        name = self.entry_name.get()
        age = self.entry_age.get()
        area = self.entry_area.get()

        if not aadhar or not unique_id or not name or not age or not area:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        data = {"Aadhar Number": aadhar, "Unique ID": unique_id, "Name": name, "Age": age, "Fishing Area": area}
        self.collection.insert_one(data)
        messagebox.showinfo("Success", "Data stored successfully!")

    def go_back(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = IDGeneratorApp(root)
    root.mainloop()
