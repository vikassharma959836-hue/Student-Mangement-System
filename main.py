from tkinter import *
from tkinter import Toplevel, messagebox, filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
import pymysql
import time
import pandas as pd

root = Tk()
root.title('Student Management System')

# ======================= GREEN THEME ============================
BG_MAIN = "#C8E6C9"       # Light green main background
BG_FRAME = "#A5D6A7"      # Frame soft green
LABEL_BG = "#2E7D32"      # Dark green for labels
LABEL_FG = "white"
BTN_BG = "#43A047"        # Medium green button
BTN_FG = "white"
BTN_ACTIVE = "#2E7D32"    # Darker green on hover
ENTRY_BG = "white"
# ================================================================


root.config(bg=BG_MAIN)
root.geometry('1174x700+200+50')
root.resizable(False, False)


# ======================= ADD STUDENT FUNCTION ============================
def addstudent():
    def submitadd():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob = dobval.get()
        addedtime = time.strftime("%H:%M:%S")
        addeddate = time.strftime("%d/%m/%Y")
        try:
            strr = 'insert into studentdata1 values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(strr, (id, name, mobile, email, address, gender, dob, addeddate, addedtime))
            con.commit()
            res = messagebox.askyesnocancel('Notification', f'ID {id} Name {name} added successfully.\nClear form?')
            if res == True:
                idval.set('')
                nameval.set('')
                mobileval.set('')
                emailval.set('')
                addressval.set('')
                genderval.set('')
                dobval.set('')
        except:
            messagebox.showerror('Error', 'ID Already Exists')
        refresh_table()

    addroot = Toplevel(master=DataEntryFrame)
    addroot.grab_set()
    addroot.geometry('470x470+220+200')
    addroot.title('Add Student')
    addroot.config(bg=BG_MAIN)
    addroot.resizable(False, False)

    labels = ["Enter ID :", "Enter Name :", "Enter Mobile :", "Enter Email :", "Enter Address :", "Enter Gender :", "Enter D.O.B :"]
    y = 10
    for text in labels:
        Label(addroot, text=text, bg=LABEL_BG, fg=LABEL_FG, font=('times', 16, 'bold'), width=15).place(x=10, y=y)
        y += 60

    idval = StringVar()
    nameval = StringVar()
    mobileval = StringVar()
    emailval = StringVar()
    addressval = StringVar()
    genderval = StringVar()
    dobval = StringVar()

    entries = [idval, nameval, mobileval, emailval, addressval, genderval, dobval]
    y = 10
    for var in entries:
        Entry(addroot, font=('roman', 14), bd=4, bg=ENTRY_BG, textvariable=var).place(x=250, y=y)
        y += 60

    Button(addroot, text='Submit', font=('roman', 14, 'bold'), bg=BTN_BG, fg=BTN_FG,
           activebackground=BTN_ACTIVE, width=18, command=submitadd).place(x=150, y=420)

    addroot.mainloop()


# ===================== REFRESH TABLE ============================
def refresh_table():
    mycursor.execute('select * from studentdata1')
    datas = mycursor.fetchall()
    studenmttable.delete(*studenmttable.get_children())
    for i in datas:
        studenmttable.insert('', END, values=i)


# ======================= SEARCH STUDENT ============================
def searchstudent():
    def search():
        fields = {"id": idval.get(), "name": nameval.get(), "mobile": mobileval.get(),
                  "email": emailval.get(), "address": addressval.get(), "gender": genderval.get(),
                  "dob": dobval.get(), "date": dateval.get()}

        for col, val in fields.items():
            if val != "":
                strr = f"select * from studentdata1 where {col}=%s"
                mycursor.execute(strr, (val,))
                datas = mycursor.fetchall()
                studenmttable.delete(*studenmttable.get_children())
                for i in datas:
                    studenmttable.insert('', END, values=i)
                return

    searchroot = Toplevel(master=DataEntryFrame)
    searchroot.grab_set()
    searchroot.geometry('470x540+220+200')
    searchroot.title('Search Student')
    searchroot.config(bg=BG_MAIN)
    searchroot.resizable(False, False)

    labels = ["Enter ID :", "Enter Name :", "Enter Mobile :", "Enter Email :", "Enter Address :",
              "Enter Gender :", "Enter D.O.B :", "Enter Date :"]
    y = 10
    for text in labels:
        Label(searchroot, text=text, bg=LABEL_BG, fg=LABEL_FG, font=('times', 16, 'bold'), width=15).place(x=10, y=y)
        y += 60

    idval = StringVar()
    nameval = StringVar()
    mobileval = StringVar()
    emailval = StringVar()
    addressval = StringVar()
    genderval = StringVar()
    dobval = StringVar()
    dateval = StringVar()

    entries = [idval, nameval, mobileval, emailval, addressval, genderval, dobval, dateval]
    y = 10
    for var in entries:
        Entry(searchroot, font=('roman', 14), bd=4, bg=ENTRY_BG, textvariable=var).place(x=250, y=y)
        y += 60

    Button(searchroot, text='Search', font=('roman', 14, 'bold'), bg=BTN_BG, fg=BTN_FG,
           activebackground=BTN_ACTIVE, width=18, command=search).place(x=150, y=480)

    searchroot.mainloop()


# ======================= DELETE STUDENT ============================
def deletestudent():
    cc = studenmttable.focus()
    if cc == "":
        return
    pp = studenmttable.item(cc)['values'][0]
    mycursor.execute('delete from studentdata1 where id=%s', (pp,))
    con.commit()
    messagebox.showinfo('Notification', f'ID {pp} Deleted')
    refresh_table()


# ======================= UPDATE STUDENT ================================
def updatestudent():
    cc = studenmttable.focus()
    if cc == "":
        messagebox.showerror("Error", "Please select a student to update")
        return

    values = studenmttable.item(cc)['values']

    def submitupdate():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob = dobval.get()

        try:
            strr = '''
                update studentdata1 
                set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s
                where id=%s
            '''
            mycursor.execute(strr, (name, mobile, email, address, gender, dob, id))
            con.commit()
            messagebox.showinfo("Success", "Record Updated Successfully")
            updateroot.destroy()
            refresh_table()
        except Exception as e:
            messagebox.showerror("Error", f"Update Failed:\n{e}")

    updateroot = Toplevel(master=DataEntryFrame)
    updateroot.grab_set()
    updateroot.geometry('470x470+220+200')
    updateroot.title("Update Student")
    updateroot.config(bg=BG_MAIN)
    updateroot.resizable(False, False)

    labels = ["Enter ID :", "Enter Name :", "Enter Mobile :", "Enter Email :", "Enter Address :", "Enter Gender :", "Enter D.O.B :"]
    y = 10
    for text in labels:
        Label(updateroot, text=text, bg=LABEL_BG, fg=LABEL_FG, font=('times', 16, 'bold'), width=15).place(x=10, y=y)
        y += 60

    idval = StringVar(value=values[0])
    nameval = StringVar(value=values[1])
    mobileval = StringVar(value=values[2])
    emailval = StringVar(value=values[3])
    addressval = StringVar(value=values[4])
    genderval = StringVar(value=values[5])
    dobval = StringVar(value=values[6])

    entries = [idval, nameval, mobileval, emailval, addressval, genderval, dobval]
    y = 10
    for var in entries:
        Entry(updateroot, font=('roman', 14), bd=4, bg=ENTRY_BG, textvariable=var).place(x=250, y=y)
        y += 60

    Button(updateroot, text='Update', font=('roman', 14, 'bold'), bg=BTN_BG, fg=BTN_FG,
           activebackground=BTN_ACTIVE, width=18, command=submitupdate).place(x=150, y=420)

    updateroot.mainloop()


# ======================= EXPORT TO EXCEL ============================
def exportToExcel():
    try:
        mycursor.execute('select * from studentdata1')
        data = mycursor.fetchall()
        if not data:
            messagebox.showinfo("No Data", "No records available to export.")
            return

        df = pd.DataFrame(data, columns=['ID','Name','Mobile','Email','Address','Gender','D.O.B','Date','Time'])

        file = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                            filetypes=[("Excel files","*.xlsx")])

        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Success", f"Data Exported Successfully\nSaved at: {file}")

    except Exception as e:
        messagebox.showerror("Error", f"Error exporting data:\n{e}")


# ======================= EXIT FUNCTION ============================
def exitstudent():
    if messagebox.askyesno('Exit', 'Do you want to exit?'):
        root.destroy()


# ======================= CONNECT DATABASE ============================
def Connectdb():
    def submitdb():
        global con, mycursor
        try:
            con = pymysql.connect(host=hostval.get(), user=userval.get(), password=passwordval.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection Failed')
            return

        try:
            mycursor.execute('create database studentmanagementsystem1')
            mycursor.execute('use studentmanagementsystem1')
            mycursor.execute('''
                create table studentdata1(
                id int primary key,
                name varchar(20),
                mobile varchar(12),
                email varchar(30),
                address varchar(100),
                gender varchar(10),
                dob varchar(20),
                date varchar(20),
                time varchar(20))''')
            messagebox.showinfo('Success', 'Database Created & Connected')
        except:
            mycursor.execute('use studentmanagementsystem1')
            messagebox.showinfo('Connected', 'Database Connected')

        dbroot.destroy()

    dbroot = Toplevel()
    dbroot.grab_set()
    dbroot.geometry('470x250+800+230')
    dbroot.config(bg=BG_MAIN)

    labels = ["Enter Host :", "Enter User :", "Enter Password :"]
    y = 10
    for text in labels:
        Label(dbroot, text=text, bg=LABEL_BG, fg=LABEL_FG, font=('times', 16, 'bold')).place(x=10, y=y)
        y += 60

    hostval = StringVar()
    userval = StringVar()
    passwordval = StringVar()

    entries = [hostval, userval, passwordval]
    y = 10
    for var in entries:
        Entry(dbroot, font=('roman', 14), bd=4, bg=ENTRY_BG, textvariable=var).place(x=250, y=y)
        y += 60

    Button(dbroot, text='Connect', font=('roman', 14, 'bold'), bg=BTN_BG, fg=BTN_FG,
           activebackground=BTN_ACTIVE, width=18, command=submitdb).place(x=150, y=190)

    dbroot.mainloop()


# ======================= UI FRAMES & TABLE ============================
DataEntryFrame = Frame(root, bg=BG_FRAME, borderwidth=5)
DataEntryFrame.place(x=10, y=80, width=500, height=600)

Label(DataEntryFrame, text='--- Student Menu ---', bg=BG_FRAME, font=('arial', 20, 'bold')).pack(pady=10)

options = [
    ("Add Student", addstudent),
    ("Search Student", searchstudent),
    ("Update Student", updatestudent),
    ("Delete Student", deletestudent),
    ("Export to Excel", exportToExcel),
    ("Exit", exitstudent)
]

for text, command in options:
    Button(DataEntryFrame, text=text, width=25, font=('arial', 16, 'bold'), bd=6,
           bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE, command=command).pack(pady=10)

ShowDataFrame = Frame(root, bg=BG_FRAME, borderwidth=5)
ShowDataFrame.place(x=550, y=80, width=620, height=600)

style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), background=LABEL_BG, foreground='white')
style.configure('Treeview', font=('arial', 12), background='white', foreground='black', rowheight=28)

scroll_x = Scrollbar(ShowDataFrame, orient=HORIZONTAL)
scroll_y = Scrollbar(ShowDataFrame, orient=VERTICAL)

studenmttable = Treeview(ShowDataFrame, columns=('Id','Name','Mobile','Email','Address','Gender','D.O.B','Date','Time'),
                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=studenmttable.xview)
scroll_y.config(command=studenmttable.yview)

for col in studenmttable['columns']:
    studenmttable.heading(col, text=col)
    studenmttable.column(col, width=120)

studenmttable.pack(fill=BOTH, expand=True)

# Connect to DB
Connectdb()

root.mainloop()
