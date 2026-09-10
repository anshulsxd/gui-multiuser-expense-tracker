import customtkinter as ctk

window = ctk.CTk()

window.title("Expense Tracker")
window.geometry("1000x600")
window.resizable(False, False)

label = ctk.CTkLabel(window, text="Welcome to Expense Tracker!")
label.pack()
button = ctk.CTkButton(window, text="Click me")
button.pack(pady=50)

window.mainloop()