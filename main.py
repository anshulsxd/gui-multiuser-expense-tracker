import customtkinter as ctk

window = ctk.CTk()

window.title("Expense Tracker")
window.geometry("600x400")

label = ctk.CTkLabel(window, text="Welcome to Expense Tracker!")
label.pack()
button = ctk.CTkButton(window, text="Click me")
button.pack(pady=50)

window.mainloop()