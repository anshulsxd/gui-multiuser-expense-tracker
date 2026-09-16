import customtkinter as ctk
import account
import expenses

DEV_MODE = True

window = ctk.CTk()
account.create_table()
expenses.create_table()
window.title("Expense Tracker")
window.geometry("1000x600")
window.resizable(False, False)

def UserLogin():
    login_scr = ctk.CTkFrame(window)
    createAcc_scr = ctk.CTkFrame(window)
    dashboard_scr = ctk.CTkFrame(window)

    def switchToSignin():
        login_scr.pack_forget()
        createAcc_scr.pack(fill="both", expand=True)

    def switchToLogin():
        createAcc_scr.pack_forget()
        login_scr.pack(fill="both", expand=True)

    def successLogin(username, user_id):
        login_scr.pack_forget()
        userLabel.configure(text=f"👤 Hi, {username}")
        total_amount.configure(text=f"$ {expenses.get_total_exp(user_id):.2f}")
        dashboard_scr.pack(fill="both", expand=True)

    def logout():
        dashboard_scr.pack_forget()
        login_scr.pack(fill="both", expand=True)

    # ------- login scr ------:
    title_login = ctk.CTkLabel(login_scr, text="Login", font=("Segoe UI", 50, "bold"))
    title_login.pack(pady=50)

    usrnmeEntery = ctk.CTkEntry(login_scr, placeholder_text="Username", width=300, height=40)
    usrnmeEntery.pack()

    passEntery = ctk.CTkEntry(login_scr, placeholder_text="Password", show="*", width=300, height=40)
    passEntery.pack(pady=25)

    def signin():
        username = usrnmeEntery.get()
        password = passEntery.get()

        if not username or not password:
            login_label.configure(text="Fill all the fields!")

            window.after(5000, lambda: login_label.configure(text=""))
            return

        check = account.login(username, password)

        if check:
            successLogin(username, check)

        else:
            login_label.configure(text="Incorrect username or password!")

            window.after(5000, lambda: login_label.configure(text=""))
            return


    login_label = ctk.CTkLabel(login_scr, text="")
    login_label.pack(pady=10)
    
    loginButton = ctk.CTkButton(login_scr, text="Login", command=signin, width=300, height=40)
    loginButton.pack(pady=30)

    signupButton= ctk.CTkButton(login_scr, text="Create Account", width=300, height=40, command=switchToSignin)
    signupButton.pack()

    login_scr.pack(fill="both", expand=True)

    # ------ signup ------

    title_signup = ctk.CTkLabel(createAcc_scr, text="Signup", font=("Segoe UI", 50, "bold"))
    title_signup.pack(pady=50)

    createUsrnme = ctk.CTkEntry(createAcc_scr, placeholder_text="Create Username", width=300, height=40)
    createUsrnme.pack(pady=25)

    createPass = ctk.CTkEntry(createAcc_scr, placeholder_text="Create Password", width=300, height=40)
    createPass.pack()

    def signup():
        username = createUsrnme.get()
        password = createPass.get()
    
        if not username or not password:
            signup_label.configure(text="Fill all the fields!")
            
            window.after(5000, lambda: signup_label.configure(text=""))
            return
    
        success = account.create_account(username, password)
    
        if success:
            switchToLogin()
        else:
            signup_label.configure(text="Username already exist!")

            window.after(5000, lambda:signup_label.configure(text=""))
            return

    signup_label = ctk.CTkLabel(createAcc_scr, text="")
    signup_label.pack(pady=10)

    createButton = ctk.CTkButton(createAcc_scr, text="Signup", width=300, height=40, command=signup)
    createButton.pack(pady=30)

    backToLogin = ctk.CTkButton(createAcc_scr, text="Back to Login screen?", width=300, height=40, command=switchToLogin)
    backToLogin.pack()

    # ------- dashboard -------

    topBar = ctk.CTkFrame(dashboard_scr, height=40, corner_radius=0)
    topBar.pack(fill="x")

    userLabel = ctk.CTkLabel(topBar, text="")
    userLabel.pack(side="right", padx=15)

    sideBar = ctk.CTkFrame(dashboard_scr, width=200, corner_radius=15)
    sideBar.pack(side="left", fill="y", padx=12, pady=12)
    sideBar.pack_propagate(False)

    dashboard_btn = ctk.CTkButton(sideBar, text="Dashboard", width=170)
    dashboard_btn.pack(pady=(40, 10), padx=15)

    expenses_btn = ctk.CTkButton(sideBar, text="Expenses", width=170)
    expenses_btn.pack(pady=10, padx=15)

    add_expense_btn = ctk.CTkButton(sideBar, text="+ Add Expense", width=170)
    add_expense_btn.pack(pady=10, padx=15)

    settings_btn = ctk.CTkButton(sideBar, text="Settings", width=170)
    settings_btn.pack(pady=10, padx=15)

    logout_btn = ctk.CTkButton(sideBar, text="Logout", width=170, fg_color="gray", hover_color="red", command=logout)
    logout_btn.pack(side="bottom", pady=25, padx=15)

    dashboard_title = ctk.CTkLabel(dashboard_scr, text="Stats", font=("Segoe UI", 50, "bold"))
    dashboard_title.pack(pady=35)

    total_amount_dashb = ctk.CTkFrame(dashboard_scr, width=200, height=125, corner_radius=15)
    total_amount_dashb.place(x=275, y=200)
    total_amount_dashb.pack_propagate(False)

    this_month_dashb = ctk.CTkFrame(dashboard_scr, width=200, height=125, corner_radius=15)
    this_month_dashb.place(x=495, y=200)
    this_month_dashb.pack_propagate(False)

    total_entries_dashb = ctk.CTkFrame(dashboard_scr, width=200, height=125, corner_radius=15)
    total_entries_dashb.place(x=720, y=200)
    total_entries_dashb.pack_propagate(False)

    total_amount_title = ctk.CTkLabel(total_amount_dashb, text="Total Amount", font=("Segoe UI", 20, "bold"))
    total_amount_title.pack(pady=10)

    this_month_title = ctk.CTkLabel(this_month_dashb, text="This Month", font=("Segoe UI", 20, "bold"))
    this_month_title.pack(pady=10)

    total_entries_title = ctk.CTkLabel(total_entries_dashb, text="Total Entries", font=("Segoe UI", 20, "bold"))
    total_entries_title.pack(pady=10)

    #data print
    total_amount = ctk.CTkLabel(total_amount_dashb, text="", font=("Segoe UI", 20, "bold"))
    total_amount.pack(pady=5)

    if __name__ == "__main__":

        if DEV_MODE:
            successLogin("devID", account.login("devID", "devID"))

UserLogin()
window.mainloop()