import customtkinter as ctk
import account
import expenses

window = ctk.CTk()
account.create_table()
expenses.create_table()
window.title("Expense Tracker")
window.geometry("1000x600")
window.resizable(False, False)

def UserLogin():
    login_scr = ctk.CTkFrame(window)
    createAcc_scr = ctk.CTkFrame(window)

    def switchToSignin():
        login_scr.pack_forget()
        createAcc_scr.pack(fill="both", expand=True)

    def switchToLogin():
        createAcc_scr.pack_forget()
        login_scr.pack(fill="both", expand=True)

    # login scr-----:
    title_login = ctk.CTkLabel(login_scr, text="Login", font=("Arial", 50, "bold"))
    title_login.pack(pady=50)

    usrnmeEntery = ctk.CTkEntry(login_scr, placeholder_text="Username", width=300, height=40)
    usrnmeEntery.pack()

    passEntery = ctk.CTkEntry(login_scr, placeholder_text="Password", show="*", width=300, height=40)
    passEntery.pack(pady=25)

    loginButton = ctk.CTkButton(login_scr, text="Login", width=300, height=40)
    loginButton.pack(pady=30)

    signupButton= ctk.CTkButton(login_scr, text="Create Account", width=300, height=40, command=switchToSignin)
    signupButton.pack()

    login_scr.pack(fill="both", expand=True)
    # signup---

    title_signup = ctk.CTkLabel(createAcc_scr, text="Signup", font=("Arial", 50, "bold"))
    title_signup.pack(pady=50)

    createUsrnme = ctk.CTkEntry(createAcc_scr, placeholder_text="Create Username", width=300, height=40)
    createUsrnme.pack(pady=25)

    createPass = ctk.CTkEntry(createAcc_scr, placeholder_text="Create Password", width=300, height=40)
    createPass.pack()

    def signup():
        username = createUsrnme.get()
        password = createPass.get()
    
        if not username or not password:
            print("Fill all fields")
            return
    
        success = account.create_account(username, password)
    
        if success:
            print("Account created!")
            switchToLogin()
        else:
            print("Username already exists")

    createButton = ctk.CTkButton(createAcc_scr, text="Signup", width=300, height=40, command=signup)
    createButton.pack(pady=30)

    backToLogin = ctk.CTkButton(createAcc_scr, text="Back to Login screen?", width=300, height=40, command=switchToLogin)
    backToLogin.pack()

UserLogin()
window.mainloop()