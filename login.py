from tkinter import *
from tkinter import messagebox
from dynamicdashboard import MaritimeTrackingApp  # Import the dashboard class

class LoginApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Login Page")
        self.root.geometry("1400x768")
        self.root.configure(bg="black")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        def verify_login():
            username = entry_username.get()
            password = entry_password.get()
            
            if username == "navy" and password == "india":
                messagebox.showinfo("Login", "Login Successfully")
                self.root.destroy()  # Close login window
                self.open_dashboard()  # Open the dashboard
            else:
                messagebox.showerror("Login Failed", "Invalid Credentials")

        container = Frame(self.root, bg="#3f8c86")
        container.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)

        Label(container, text="User Name:", font=("Arial", 16), fg="white", bg="#3f8c86").pack(pady=10)
        entry_username = Entry(container, font=("Arial", 16))
        entry_username.pack(pady=5)

        Label(container, text="Password:", font=("Arial", 16), fg="white", bg="#3f8c86").pack(pady=10)
        entry_password = Entry(container, font=("Arial", 16), show="*")
        entry_password.pack(pady=5)

        # Create button frame for styling
        self.button_frame = Frame(container, bg="#3f8c86")
        self.button_frame.pack(pady=10)

        # Create Login Button
        self.button2 = Button(self.button_frame, text="Login", font=("Arial", 16, "bold"), padx=10, pady=5, 
                              bg="#4CAF50", fg="white", command=verify_login)
        self.button2.pack(side="top", pady=10)

    def open_dashboard(self):
        root = Tk()  # Create a new Tk instance for the dashboard
        MaritimeTrackingApp(root)  # Pass root to MaritimeTrackingApp
        root.mainloop()  # Start the Tk event loop

if __name__ == "__main__":
    LoginApp()
