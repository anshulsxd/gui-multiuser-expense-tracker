import customtkinter as ctk # external lib
import account # file import
import expenses # file import
from datetime import date # inbuilt lib
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

window = ctk.CTk()

window.iconbitmap(resource_path("assets/appicon.ico"))
account.create_table()
expenses.create_table()
window.title("Expense Tracker")
window.geometry("1000x600")
window.resizable(False, False)

def UserLogin():
    login_scr = ctk.CTkFrame(window)
    createAcc_scr = ctk.CTkFrame(window)
    dashboard_scr = ctk.CTkFrame(window)
    expenses_scr = ctk.CTkFrame(window)
    current_username = None
    current_user_id = None
    addExp_scr = ctk.CTkFrame(window)
    delExp_scr = ctk.CTkFrame(window)

    def switchToSignin():
        login_scr.pack_forget()
        createAcc_scr.pack(fill="both", expand=True)

    def switchToLogin():
        createAcc_scr.pack_forget()
        login_scr.pack(fill="both", expand=True)

    def successLogin(username, user_id):
        nonlocal current_username, current_user_id
        current_username = username
        current_user_id = user_id
        login_scr.pack_forget()
        userLabel.configure(text=f"👤 Hi, {username}")
        total_amount.configure(text=f"$ {expenses.get_total_exp(user_id):.2f}")
        this_month.configure(text=f"$ {expenses.get_this_month(user_id):.2f}")
        total_entries.configure(text=str(expenses.get_total_entries(user_id)))
        today_spend.configure(text=f"$ {expenses.get_today_expense(user_id):.2f}")
        dashboard_scr.pack(fill="both", expand=True)

    def logout():
        dashboard_scr.pack_forget()
        expenses_scr.pack_forget()
        addExp_scr.pack_forget()
        delExp_scr.pack_forget()
        login_scr.pack(fill="both", expand=True)

    def showDashboard():
        expenses_scr.pack_forget()
        addExp_scr.pack_forget()
        delExp_scr.pack_forget()
        dashboard_scr.pack(fill="both", expand=True)

    def expensesScrShow():
        dashboard_scr.pack_forget()
        addExp_scr.pack_forget()
        delExp_scr.pack_forget()
        expenses_scr.pack(fill="both", expand=True)
        userLabelExp.configure(text=f"👤 Hi, {current_username}")
        fetch_expenses()

    def fetch_expenses():
        date_value = searchBar.get().strip()
        if not date_value:
            date_value = date.today().isoformat()
            searchBar.delete(0, "end")
            searchBar.insert(0, date_value)

        for widget in expense_results.winfo_children():
            widget.destroy()

        records = expenses.get_expenses(current_user_id, date_value)
        if not records:
            ctk.CTkLabel(expense_results, text="No expenses found for this date.").pack(pady=12)
            return

        for expense_id, title, amount, category, description, expense_date in records:
            expense_box = ctk.CTkFrame(expense_results, corner_radius=10, border_width=1)
            expense_box.pack(fill="x", padx=8, pady=6)

            ctk.CTkLabel(
                expense_box,
                text=f"ID: {expense_id}  |  {title}  |  ${amount:.2f}",
                anchor="w",
                font=("Segoe UI", 16, "bold")
            ).pack(fill="x", padx=12, pady=(10, 2))

            details = f"{expense_date}  |  {category}"
            if description:
                details += f"  |  {description}"

            ctk.CTkLabel(
                expense_box,
                text=details,
                anchor="w",
                justify="left",
                wraplength=650
            ).pack(fill="x", padx=12, pady=(0, 10))

    def addExpense():
        UserID = current_user_id
        ExpTitle = addTitle.get()
        ExpPrice = addPrice.get()
        ExpCategory = addCategory.get()
        ExpDescription = addDescription.get()

        if not ExpTitle or not ExpPrice or not ExpCategory:
            errorText.configure(text="Please fill required fields!")
            window.after(5000, lambda: errorText.configure(text=""))
            return

        else:
            expenses.add_expense(UserID, ExpTitle, ExpPrice, ExpCategory, ExpDescription)
            addTitle.delete(0, "end")
            addPrice.delete(0, "end")
            addCategory.set("Food")
            addDescription.delete(0, "end")

    def switchToAddExp():
        dashboard_scr.pack_forget()
        expenses_scr.pack_forget()
        delExp_scr.pack_forget()
        addExp_scr.pack(fill="both", expand=True)
        userLabelAddExp.configure(text=f"👤 Hi, {current_username}")

    def showDelExp_scr():
        dashboard_scr.pack_forget()
        expenses_scr.pack_forget()
        addExp_scr.pack_forget()
        delExp_scr.pack(fill="both", expand=True)
        userLabelDelExp.configure(text=f"👤 Hi, {current_username}")

    def deleteExpense():
        expense_id = delExpIDEntry.get().strip()

        try:
            expense_id = int(expense_id)
        except ValueError:
            deleteStatus.configure(text="Enter a valid expense ID.")
            return

        if expenses.delete_expense(expense_id, current_user_id):
            deleteStatus.configure(text="Expense deleted.")
            delExpIDEntry.delete(0, "end")
        else:
            deleteStatus.configure(text="Expense not found.")

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
            usrnmeEntery.delete(0, "end")
            passEntery.delete(0, "end")
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
            createUsrnme.delete(0, "end")
            createPass.delete(0, "end")

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

    expenses_btn = ctk.CTkButton(sideBar, text="Expenses", width=170, command=expensesScrShow)
    expenses_btn.pack(pady=10, padx=15)

    add_expense_btn = ctk.CTkButton(sideBar, text="+ Add Expense", width=170, command=switchToAddExp)
    add_expense_btn.pack(pady=10, padx=15)

    delExp_btn = ctk.CTkButton(sideBar, text="- Delete expense", width=170, command=showDelExp_scr)
    delExp_btn.pack(pady=10, padx=15)

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

    today_expense_dashb = ctk.CTkFrame(dashboard_scr, width=225, height=125, corner_radius=15)
    today_expense_dashb.place(x=483, y=350)
    today_expense_dashb.pack_propagate(False)

    total_amount_title = ctk.CTkLabel(total_amount_dashb, text="Total Amount", font=("Segoe UI", 20, "bold"))
    total_amount_title.pack(pady=10)

    this_month_title = ctk.CTkLabel(this_month_dashb, text="This Month", font=("Segoe UI", 20, "bold"))
    this_month_title.pack(pady=10)

    total_entries_title = ctk.CTkLabel(total_entries_dashb, text="Total Entries", font=("Segoe UI", 20, "bold"))
    total_entries_title.pack(pady=10)

    today_expense_title = ctk.CTkLabel(today_expense_dashb, text="Money spend today", font=("Segoe UI", 20, "bold"))
    today_expense_title.pack(pady=10)

    #data print
    total_amount = ctk.CTkLabel(total_amount_dashb, text="", font=("Segoe UI", 20, "bold"))
    total_amount.pack(pady=5)

    this_month = ctk.CTkLabel(this_month_dashb, text="", font=("Segoe UI", 20, "bold"))
    this_month.pack(pady=5)

    total_entries = ctk.CTkLabel(total_entries_dashb, text="", font=("Segoe UI", 20, "bold"))
    total_entries.pack(pady=5)

    today_spend = ctk.CTkLabel(today_expense_dashb, text="", font=("Segoe UI", 20, "bold"))
    today_spend.pack(pady=5)

    # ----------- expenses ------------

    topBarExp = ctk.CTkFrame(expenses_scr, height=40, corner_radius=0)
    topBarExp.pack(fill="x")
    
    userLabelExp = ctk.CTkLabel(topBarExp, text="")
    userLabelExp.pack(side="right", padx=15)
    
    sideBarExp = ctk.CTkFrame(expenses_scr, width=200, corner_radius=15)
    sideBarExp.pack(side="left", fill="y", padx=12, pady=12)
    sideBarExp.pack_propagate(False)
    
    dashboard_btn = ctk.CTkButton(sideBarExp, text="Dashboard", width=170, command=showDashboard)
    dashboard_btn.pack(pady=(40, 10), padx=15)
    
    expenses_btn = ctk.CTkButton(sideBarExp, text="Expenses", width=170)
    expenses_btn.pack(pady=10, padx=15)
    
    add_expense_btn = ctk.CTkButton(sideBarExp, text="+ Add Expense", width=170, command=switchToAddExp)
    add_expense_btn.pack(pady=10, padx=15)
    
    delExp_btn = ctk.CTkButton(sideBarExp, text="- Delete expense", width=170, command=showDelExp_scr)
    delExp_btn.pack(pady=10, padx=15)
    
    logout_btn = ctk.CTkButton(sideBarExp, text="Logout", width=170, fg_color="gray", hover_color="red", command=logout)
    logout_btn.pack(side="bottom", pady=25, padx=15)

    expenses_title = ctk.CTkLabel(expenses_scr, text="Expenses", font=("Segoe UI", 50, "bold"))
    expenses_title.pack(pady=35)

    searchBar = ctk.CTkEntry(expenses_scr, placeholder_text="Date (YYYY-MM-DD)", height=50, width=500)
    searchBar.place(x=245, y=185)
    searchBar.insert(0, date.today().isoformat())

    searchButton = ctk.CTkButton(expenses_scr, text="GO   ---->", height=49, width=200, command=fetch_expenses)
    searchButton.place(x=760, y=185)

    expense_results = ctk.CTkScrollableFrame(expenses_scr, width=715, height=275)
    expense_results.place(x=245, y=255)

    # --------- add expenses ----------

    topBarAddExp = ctk.CTkFrame(addExp_scr, height=28, corner_radius=0)
    topBarAddExp.pack(fill="x")

    userLabelAddExp = ctk.CTkLabel(topBarAddExp, text="")
    userLabelAddExp.pack(side="right", padx=15)

    sideBarAddExp = ctk.CTkFrame(addExp_scr, width=200, corner_radius=15)
    sideBarAddExp.pack(side="left", fill="y", padx=12, pady=12)
    sideBarAddExp.pack_propagate(False)

    dashboard_btn = ctk.CTkButton(sideBarAddExp, text="Dashboard", width=170, command=showDashboard)
    dashboard_btn.pack(pady=(40, 10), padx=15)
    
    expenses_btn = ctk.CTkButton(sideBarAddExp, text="Expenses", width=170, command=expensesScrShow)
    expenses_btn.pack(pady=10, padx=15)
    
    add_expense_btn = ctk.CTkButton(sideBarAddExp, text="+ Add Expense", width=170)
    add_expense_btn.pack(pady=10, padx=15)
    
    delExp_btn = ctk.CTkButton(sideBarAddExp, text="- Delete expense", width=170, command=showDelExp_scr)
    delExp_btn.pack(pady=10, padx=15)
    
    logout_btn = ctk.CTkButton(sideBarAddExp, text="Logout", width=170, fg_color="gray", hover_color="red", command=logout)
    logout_btn.pack(side="bottom", pady=25, padx=15)

    addExpenses_title = ctk.CTkLabel(addExp_scr, text="Add Expenses", font=("Segoe UI", 50, "bold"))
    addExpenses_title.pack(pady=35)

    addTitle = ctk.CTkEntry(addExp_scr, placeholder_text="Expense title *", height=50, width=700)
    addTitle.place(x=245, y=185)

    addPrice = ctk.CTkEntry(addExp_scr, placeholder_text="Amount ($) *", height=50, width=350)
    addPrice.place(x=245, y=280)

    addCategory = ctk.CTkOptionMenu(addExp_scr, values=[
        "Food",
        "Beverage",
        "Transport",
        "Shopping",
        "Bills",
        "Entertainment",
        "Other"
    ], height=50, width=325, fg_color="gray25", button_color="gray25", button_hover_color="gray35")
    addCategory.place(x=620, y=280)

    addDescription = ctk.CTkEntry(addExp_scr, placeholder_text="Description", height=75, width=700)
    addDescription.place(x=245, y=375)

    errorText = ctk.CTkLabel(addExp_scr, text="")
    errorText.place(x=530, y=465)

    addExpButton = ctk.CTkButton(addExp_scr, text="Add", height=50, width=150, command=addExpense)
    addExpButton.place(x=525, y=500)

    # --------- del expense ------------

    topBarDelExp = ctk.CTkFrame(delExp_scr, height=28, corner_radius=0)
    topBarDelExp.pack(fill="x")

    userLabelDelExp = ctk.CTkLabel(topBarDelExp, text="")
    userLabelDelExp.pack(side="right", padx=15)

    sideBarAddExp = ctk.CTkFrame(delExp_scr, width=200, corner_radius=15)
    sideBarAddExp.pack(side="left", fill="y", padx=12, pady=12)
    sideBarAddExp.pack_propagate(False)

    dashboard_btn = ctk.CTkButton(sideBarAddExp, text="Dashboard", width=170, command=showDashboard)
    dashboard_btn.pack(pady=(40, 10), padx=15)
    
    expenses_btn = ctk.CTkButton(sideBarAddExp, text="Expenses", width=170, command=expensesScrShow)
    expenses_btn.pack(pady=10, padx=15)
    
    add_expense_btn = ctk.CTkButton(sideBarAddExp, text="+ Add Expense", width=170, command=switchToAddExp)
    add_expense_btn.pack(pady=10, padx=15)
    
    delExp_btn = ctk.CTkButton(sideBarAddExp, text="- Delete expense", width=170)
    delExp_btn.pack(pady=10, padx=15)

    logout_btn = ctk.CTkButton(sideBarAddExp, text="Logout", width=170, fg_color="gray", hover_color="red", command=logout)
    logout_btn.pack(side="bottom", pady=25, padx=15)

    delExpenses_title = ctk.CTkLabel(delExp_scr, text="Delete Expenses", font=("Segoe UI", 50, "bold"))
    delExpenses_title.pack(pady=35)

    delExpIDEntry = ctk.CTkEntry(delExp_scr, placeholder_text="Enter expense ID to delete", height=50, width=700)
    delExpIDEntry.place(x=245, y=185)

    delExpButton = ctk.CTkButton(delExp_scr, text="DELETE", width=170, height=50, command=deleteExpense)
    delExpButton.place(x=500, y=300)

    deleteStatus = ctk.CTkLabel(delExp_scr, text="")
    deleteStatus.place(x=500, y=365)

UserLogin()
window.mainloop()