import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from abc import ABC, abstractmethod

con = sqlite3.connect("HyperDatabase.db")

cursor = con.cursor()


# Abstraction abtract class
class Transaction(ABC):
    @abstractmethod
    def assign_id(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def view(self):
        pass

    @abstractmethod
    def total(self):
        pass


# single inheritance from abstract class
class Sales(Transaction):
    sale_id = "S000"
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Sales(ID TEXT, Date TEXT,Name TEXT, Price Integer,Quantity Integer, Amount INTEGER)")
    con.commit()

    # polymorphism type method overriding is used.
    def assign_id(self):
        def assign():
            a = list(Sales.sale_id)
            b = a[1] + a[2] + a[3]
            b = int(b)
            b += 1
            if len(str(b)) == 1:
                b = '0' + '0' + str(b)
            elif len(str(b)) == 2:
                b = '0' + str(b)
            elif len(str(b)) == 3:
                b = str(b)
            d = a[0] + str(b)
            Sales.sale_id = d
            return d

        a = cursor.execute("Select ID from Sales")
        con.commit()
        k = None
        for i in a:
            for j in i:
                k = j
        if k != None:
            Sales.sale_id = k
            i = assign()
            return i

        else:
            j = assign()
            return j

    def add(self, Id, date, pro_name, price, quantity, amount):
        self.amount = int(price) * int(quantity)
        try:
            cursor.execute("INSERT INTO Sales (ID,Date,Name,Price,Quantity,Amount)Values(?,?,?,?,?,?)"
                           , (Id, date, pro_name, price, quantity, self.amount))
            con.commit()
            Stock.delete(self, pro_name)
        except sqlite3.Error as error:
            print("Failed to add reocord in a Sales table", error)
        finally:
            print("Record Added")

    def view(self):
        a = cursor.execute("Select * from Sales")
        con.commit()
        for i in a:
            print(i)

    def delete(self, ch):
        try:
            if ch.lower() == 'yes':
                cursor.execute("Delete * from Sales ")
                con.commit()
            elif ch.lower == 'no':
                Id = str(input("Enter Id to delete: "))
                cursor.execute("DELETE from Sales WHERE ID = ?", (Id,))
                con.commit()
        except sqlite3.Error as error:
            print("Failed to remove record from Expense table", error)
        finally:
            print("Record Deleted")

    def total(self):
        try:
            sat = cursor.execute("SELECT Amount from Sales")
            st = 0
            for i in sat:
                for a in i:
                    st += a
            return st
        except sqlite3.Error as error:
            print("Failed to select record", error)
        finally:
            print("Sales Total: ", st)


# Single inheritance from abstract class
class Purchase(Transaction):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Purchase(ID TEXT, Date TEXT,Name TEXT,Price INTEGER,Quantity INTGER, Amount INTEGER)")
    con.commit()
    pur_id = "P000"

    def assign_id(self):
        def assign():
            a = list(Purchase.pur_id)
            b = a[1] + a[2] + a[3]
            b = int(b)
            b += 1
            if len(str(b)) == 1:
                b = '0' + '0' + str(b)
            elif len(str(b)) == 2:
                b = '0' + str(b)
            elif len(str(b)) == 3:
                b = str(b)
            d = a[0] + str(b)
            Purchase.pur_id = d
            return d

        a = cursor.execute("Select ID from Purchase")
        con.commit()
        k = None
        for i in a:
            for j in i:
                k = j
        # print(k)
        if k != None:
            Purchase.pur_id = k
            i = assign()
            return i

        else:
            j = assign()
            return j

    def add(self, Id, date, name, price, quan, amount):
        self.amount = int(price) * int(quan)
        try:
            cursor.execute("INSERT INTO Purchase(ID,Date,Name,Price, Quantity, Amount)Values(?,?,?,?,?,?)"
                           , (Id, date, name, price, quan, self.amount))
            con.commit()
            Stock.add(self, Id, Stock.assign_id(self), name, price, quan, self.amount)
        except sqlite3.Error as error:
            print("Failed to add record", error)
        finally:
            print("Record added")

    def view(self):
        a = cursor.execute("Select * from Purchase")
        con.commit()
        for i in a:
            for j in i:
                print(j)

    def delete(self):
        try:
            ch = str(input("Want to delete all Records: "))
            if ch.lower() == 'yes':
                cursor.execute("Delete * from Purchase")
                con.commit()
            elif ch.lower() == 'no':
                Id = str(input("Enter ID to delete: "))
                cursor.execute("Delete from Purchase where ID= ?", (Id,))
                con.commit()
        except sqlite3.Error as error:
            print("Record not deleted", error)
        finally:
            print("Record deleted")

    def total(self):
        try:
            a = cursor.execute("Select Amount from Purchase")
            con.commit()
            pt = 0
            for i in a:
                for j in i:
                    pt += j
            return pt
        except sqlite3.Error as error:
            print("Failed to total amount", error)
        finally:
            print("Purchase total: ", pt)


# single inheritance from transaction abstract class
class Expense(Transaction):
    cursor.execute("CREATE TABLE IF NOT EXISTS Expense(ID INTEGER, Date TEXT,Type TEXT, Amount INTEGER)")
    con.commit()
    exp_id = "E000"

    def assign_id(self):
        def assign():
            a = list(Expense.exp_id)
            b = a[1] + a[2] + a[3]
            b = int(b)
            b += 1
            if len(str(b)) == 1:
                b = '0' + '0' + str(b)
            elif len(str(b)) == 2:
                b = '0' + str(b)
            elif len(str(b)) == 3:
                b = str(b)
            d = a[0] + str(b)
            Expense.exp_id = d
            return d

        a = cursor.execute("Select ID from Expense")
        con.commit()
        k = None
        for i in a:
            for j in i:
                k = j
        # print(k)
        if k != None:
            Expense.exp_id = k
            i = assign()
            return i

        else:
            j = assign()
            return j

    def add(self, Id, date, title, amount):
        try:
            cursor.execute("INSERT INTO Expense(ID,Date,Type,Amount)Values(?,?,?,?)"
                           , (Id, date, title, amount))
            con.commit()
        except sqlite3.Error as error:
            print("Failed to record", error)

    def delete(self):
        try:
            ch = input("Delete all expenses: ")
            if ch.lower() == 'yes':
                cursor.execute("Delete # from Expense")
                con.commit()
            elif ch.lower() == 'no':
                Id = input("Enter Id to delete: ")
                cursor.execute("DELETE from Expense WHERE ID= ? ", (Id,))
                con.commit()
        except sqlite3.Error as error:
            print("Failed to delete record", error)
        finally:
            print("Record Deleted")

    def view(self):
        a = cursor.execute("Select * from Expense")
        con.commit()
        for i in a:
            for j in i:
                print(j)

    def total(self):
        try:
            exp = cursor.execute("SELECT Amount from Expense")
            ext = 0
            for i in exp:
                for a in i:
                    ext += a
            return ext
        except sqlite3.Error as error:
            print("Failed to total expense amount")
        finally:
            print("Expense total: ", ext)


# multiple and multi-level inheritance from sale purchase class
class Stock(Sales, Purchase):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Stock(ID TEXT, Name TEXT,Quantity INTEGER,Price INTEGER, Amount INTEGER)")
    con.commit()
    stock_id = "I000"

    def assign_id(self):
        def assign():
            a = list(Stock.stock_id)
            b = a[1] + a[2] + a[3]
            b = int(b)
            b += 1
            if len(str(b)) == 1:
                b = '0' + '0' + str(b)
            elif len(str(b)) == 2:
                b = '0' + str(b)
            elif len(str(b)) == 3:
                b = str(b)
            d = a[0] + str(b)
            Stock.stock_id = d
            return d

        a = cursor.execute("Select ID from Stock")
        con.commit()
        k = None
        for i in a:
            for j in i:
                k = j
        # print(k)
        if k != None:
            Stock.stock_id = k
            i = assign()
            return i

        else:
            j = assign()
            return j

    def add(self, Tr_id, Id, name, price, quantity, amount):
        self.amt = int(price) * int(quantity)
        try:
            cursor.execute("INSERT INTO Stock(ID,Name,Quantity,Price,Amount)VALUES(?,?,?,?,?)"
                           , (Id, name, quantity, price, self.amt))
            con.commit()

        except sqlite3.Error as error:
            print("Failed to add record", error)
        finally:
            print("Record Added")

    def view(self):
        a = cursor.execute("Select * from Stock")
        con.commit()
        for i in a:
            for j in i:
                print(j)

    def delete(self, name):
        try:
            cursor.execute("DELETE from Stock WHERE Name = ?", (name,))
            con.commit()
        except sqlite3.Error as error:
            print("Failed to delete record from stock", error)
        finally:
            print("Recrod Deleted")

    def total(self):
        try:
            stock = cursor.execute("Select Amount from Stock")
            stt = 0
            for i in stock:
                for a in i:
                    stt += a
            return stt
        except sqlite3.Error as error:
            print("Faled to select", error)
        finally:
            print("Stock total: ", stt)


class CashFlow:
    def profit(self):
        a = Purchase.total(self)
        int(a)
        b = Expense.total(self)
        int(b)
        c = Sales.total(self)
        int(c)
        ex = b + a
        profit = c - ex
        return profit

    def sale(self):
        a = Sales.total(self)
        return a

    def purchase(self):
        p = Purchase.total(self)
        return p

    def total_stock(self):
        s = Stock.total(self)
        return s

    def exp_total(self):
        e = Expense.total(self)
        return e


class HyperMart_CashFlow:
    def __init__(self, location):
        self.location = location
        self.interface()

    def interface(self):
        win = Tk()
        win.geometry("700x500")
        win.title("HyperMart")
        win.configure(background="blue")
        can = Canvas(win, width=700, height=600)
        label = Label(win, text=" HYPER MART \nDEPARTMENTAL\nSTORE", bg="blue", fg="yellow",
                      font=("Times new roman", 25, 'italic', 'bold')).pack(fill='both')
        image1 = Image.open("win.png")
        photo = ImageTk.PhotoImage(image1)
        Limg = Label(image=photo)
        Limg.pack()
        style = ttk.Style()
        menubar = Menu(win)

        def one():
            win.destroy()
            self.cashflow()

        def add_sa():
            win.destroy()
            self.add_sales()

        def sale():
            win.destroy()
            self.view_sale()

        def del_sa():
            cursor.execute("Delete from Sales")
            messagebox.showinfo("Deleting...", "All records are deleted from Sales table")

        def add_p():
            win.destroy()
            self.add_pur()

        def Purchase():
            win.destroy()
            self.view_purchase()

        def del_p():
            cursor.execute("Delete from Purchase")
            messagebox.showinfo("Deleting...", "All records are deleted from Purchase table")

        def add_e():
            win.destroy()
            self.add_expense()

        def exp():
            win.destroy()
            self.view_exp()

        def del_e():
            cursor.execute("Delete from Expense")
            messagebox.showinfo("Deleting...", "All records are deleted from Expense table")

        def add_s():
            win.destroy()
            self.add_stock()

        def stock():
            win.destroy()
            self.view_stock()

        def del_s():
            cursor.execute("Delete from Stock")
            messagebox.showinfo("Deleting...", "All records are deleted from Stock table")

        def ab_sys():
            messagebox.showinfo("About",
                                "System\n HYPERMART CASHFLOW: The system is to take records of cash flow within the store"
                                "and tells whether the store is in profit or in loss. So, for this record we must take record of every transaction"
                                "in store like sales purchases expenses so at the end of the month or any time period we could know that store is in"
                                "profit or not.\nSo, for achieving this goal we need to break it into following parts (classes)."
                                "\nWe have 6 classes:\n1.Transaction\n2.Sale\n3.Purchase\n4.Expense\n5.Stock\n6.Cashflow")

        def mod():
            messagebox.showinfo("Modules", "Modules are used in this project."
                                           "\n1. sqlite3 for database"
                                           "\n2. tkinter for GUI"
                                           "\n3. tkcalender for calender display"
                                           "\n4. pillow for inserting image in GUI "
                                           "\n5. tkinter ttk"
                                           "\n6. tkinter messagebox"
                                           "\n7. abc for abstract class")

        def close():
            win.destroy()

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=close)
        menubar.add_cascade(label="File", menu=file_menu)

        add_menu = Menu(menubar, tearoff=0)
        add_menu.add_separator()
        menubar.add_cascade(label="Add", menu=add_menu)
        add_menu.add_command(label="Sales", command=add_sa)
        add_menu.add_command(label="Purchase", command=add_p)
        add_menu.add_command(label="Expense", command=add_e)
        add_menu.add_command(label="Stock", command=add_s)

        del_menu = Menu(menubar, tearoff=0)
        del_menu.add_separator()
        menubar.add_cascade(label="Delete", menu=del_menu)
        del_menu.add_command(label="Sales", command=del_sa)
        del_menu.add_command(label="Purchase", command=del_p)
        del_menu.add_command(label="Expense", command=del_e)
        del_menu.add_command(label="Stock", command=del_s)

        view_menu = Menu(menubar, tearoff=0)
        view_menu.add_separator()
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Sales", command=sale)
        view_menu.add_command(label="Purchase", command=Purchase)
        view_menu.add_command(label="Expense", command=exp)
        view_menu.add_command(label="Stock", command=stock)

        cf_menu = Menu(menubar, tearoff=0)
        cf_menu.add_separator()
        menubar.add_cascade(label="Statement", menu=cf_menu)
        cf_menu.add_command(label="Cashflow", command=one)

        ab_menu = Menu(menubar, tearoff=0)
        ab_menu.add_separator()
        menubar.add_cascade(label="About", menu=ab_menu)
        ab_menu.add_command(label="System", command=ab_sys)
        ab_menu.add_command(label="modules", command=mod)

        win.config(menu=menubar)
        win.mainloop()

    def add_sales(self):
        sale_win = tk.Tk()
        sale_win.geometry("1000x1200")
        sale_win.title("SALES")
        win_h = 600
        win_w = 1200
        sale_win.configure(bg="powder blue")
        style = ttk.Style()
        a = Label(sale_win, text="Enter Sales Data", bg="blue", fg='yellow',
                  font=("Times new roman", 30, "italic", 'bold')).pack(fill='both')  # place(x=50,y=50)
        b = Label(sale_win, text="Select Date: ", font=("Times new roman", 14)).place(x=50, y=80)
        cal = Calendar(sale_win, font=("Times new roman", 10, 'bold'), selectmode='day', cursor="hand1", year=2020,
                       month=7, day=5)
        cal.place(x=50, y=100)
        frame = tk.Frame(sale_win)
        frame.place(x=20, y=350)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Date")
        tree.heading(3, text="Product Name")
        tree.heading(4, text="Price")
        tree.heading(5, text="Quantity")
        tree.heading(6, text="Amount")
        tree.column(1, width=50)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=120)
        tree.column(5, width=100)
        tree.column(6, width=80)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)

        Label(sale_win, text="Product Name:", bg="white", font=("Times new roman", 14)).place(x=400, y=80)
        ty = Entry(sale_win, font=("Times new roman", 14))
        ty.place(x=520, y=80)

        Label(sale_win, text="Price:", bg="white", font=("Times new roman", 14)).place(x=400, y=140)
        pr = Entry(sale_win, font=("Times new roman", 14))
        pr.place(x=520, y=140)

        Label(sale_win, text="Quantity:", bg="white", font=("Times new roman", 14)).place(x=400, y=200)
        quan = Spinbox(sale_win, from_=1, to=1000, width=5, font=("Times new roman", 14))
        quan.place(x=520, y=200)

        def add():
            i = Sales.assign_id(self)
            a = cal.selection_get()
            c = ty.get()
            d = pr.get()
            e = quan.get()
            f = int(d) * int(e)
            print(i, a, c, d, e, f)
            tree.insert('', 'end', values=(i, a, c, d, e, f))
            Sales.add(self, i, a, c, d, e, f)
            messagebox.showinfo('Confirmation', 'Record is added successesfully')

        b1 = Button(sale_win, text="Confirm", font=("Times new roman", 12), command=add).place(x=550, y=300)

        def back():
            sale_win.destroy()
            self.interface()

        b2 = Button(sale_win, text="Main Menu", font=("Times new roman", 12), command=back).place(x=750, y=300)

    def view_sale(self):
        view_sale = Tk()
        view_sale.geometry("800x600")
        view_sale.title("SALES")
        view_sale.configure(bg="powder blue")
        Label(view_sale, text="Sales", fg="yellow", bg="blue", font=("Times new roman", 30, 'italic', 'bold')).pack(
            fill='both')
        frame = Frame(view_sale)
        frame.place(x=10, y=100)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Date")
        tree.heading(3, text="Product Name")
        tree.heading(4, text="Price")
        tree.heading(5, text="Quantity")
        tree.heading(6, text="Amount")
        tree.column(1, width=30)
        tree.column(2, width=80)
        tree.column(3, width=120)
        tree.column(4, width=100)
        tree.column(5, width=80)
        tree.column(6, width=80)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)
        Sales.view(self)
        con = sqlite3.connect("HyperDatabase.db")
        cursor = con.cursor()
        a = cursor.execute("Select * from Sales")
        con.commit()
        Label(view_sale, text=('Sales Total'), bg='white', fg='blue', width=10,
              font=('times new roman', 16, 'bold')).place(x=570, y=200)
        Label(view_sale, text=(Sales.total(self)), bg='white', fg='blue', width=10,
              font=('times new roman', 16, 'bold')).place(x=570, y=230)
        for i in a:
            print(i)
            tree.insert('', 'end', values=(i))

        def add():
            view_sale.destroy()
            self.add_sales()

        b1 = Button(view_sale, text="Add", fg='green', font=('times new roman', 12), command=add).place(x=50, y=400)

        def back():
            view_sale.destroy()
            self.interface()

        b2 = Button(view_sale, text="Back", fg="black", font=('times new roman', 12), command=back).place(x=450, y=400)

    def add_pur(self):
        pur_win = Tk()
        pur_win.geometry("1000x1200")
        pur_win.title("Purchase")
        win_h = 600
        win_w = 1200
        pur_win.configure(bg="powder blue")
        style = ttk.Style()
        a = Label(pur_win, text="Enter Purhase Data", fg="yellow", bg='blue',
                  font=("Times new roman", 30, "italic", 'bold')).pack(fill='both')  # place(x=50,y=50)
        b = Label(pur_win, text="Select Date", font=("Times new roman", 12)).place(x=50, y=70)
        cal = Calendar(pur_win, font=("Times new roman", 10, 'bold'), selectmode='day', cursor="hand1", year=2020,
                       month=7, day=5)
        cal.place(x=50, y=100)
        frame = tk.Frame(pur_win)
        frame.place(x=50, y=350)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Date")
        tree.heading(3, text="Product Name")
        tree.heading(4, text="Price")
        tree.heading(5, text="Quantity")
        tree.heading(6, text="Amount")
        tree.column(1, width=50)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=120)
        tree.column(5, width=100)
        tree.column(6, width=80)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)
        Label(pur_win, text="Product Name:", bg="white", font=("Times new roman", 14)).place(x=400, y=80)
        ty = Entry(pur_win, font=("Times new roman", 14))
        ty.place(x=520, y=80)

        Label(pur_win, text="Price: ", bg="white", font=("Times new roman", 14)).place(x=400, y=140)
        pr = Entry(pur_win, font=("Times new roman", 14))
        pr.place(x=520, y=140)

        Label(pur_win, text="Quantity: ", bg="white", font=("Times new roman", 14)).place(x=400, y=190)
        quan = Spinbox(pur_win, from_=1, to=1000, width=5, font=("Times new roman", 14))
        quan.place(x=520, y=200)

        def add():
            i = Purchase.assign_id(self)
            a = cal.selection_get()
            c = ty.get()
            d = pr.get()
            e = quan.get()
            f = int(d) * int(e)
            print(i, a, c, d, e, f)
            tree.insert('', 'end', values=(i, a, c, d, e, f))
            Purchase.add(self, i, a, c, d, e, f)
            messagebox.showinfo('Confirmation', 'Record is added successesfully')

        b1 = Button(pur_win, text="Confirm", command=add).place(x=700, y=330)

        def back():
            pur_win.destroy()
            self.interface()

        b2 = Button(pur_win, text="Main Menu", command=back).place(x=850, y=330)

    def view_purchase(self):
        pur = Tk()
        pur.geometry("800x500")
        pur.title("PURCHASE")
        pur.configure(background="powder blue")
        Label(pur, text="Purchase", fg="yellow", bg="blue", font=("Times new roman", 30, 'italic', 'bold')).pack(
            fill='both')
        frame = Frame(pur)
        frame.place(x=10, y=100)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Date")
        tree.heading(3, text="Name")
        tree.heading(4, text="Price")
        tree.heading(5, text="Quantity")
        tree.heading(6, text="Amount")
        tree.column(1, width=30)
        tree.column(2, width=80)
        tree.column(3, width=100)
        tree.column(4, width=100)
        tree.column(5, width=100)
        tree.column(6, width=100)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)
        Purchase.view(self)
        con = sqlite3.connect("HyperDatabase.db")
        cursor = con.cursor()
        a = cursor.execute("Select * from Purchase")
        con.commit()
        Label(pur, text='Purchase Total', bg='white', width=15, fg='blue', font=('times new roman', 14, 'bold')).place(
            x=600, y=200)
        Label(pur, text=(Purchase.total(self)), bg='white', fg='blue', width=15,
              font=('times new roman', 14, 'bold')).place(x=600, y=220)
        for i in a:
            print(i)
            tree.insert('', 'end', values=(i))

        def add():
            pur.destroy()
            self.add_pur()

        b1 = Button(pur, text="Add", fg='green', font=('times new roman', 12, 'bold'), command=add).place(x=50, y=350)

        def back():
            pur.destroy()
            self.interface()

        b2 = Button(pur, text="Back", fg="black", font=('times new roman', 12, 'bold'), command=back).place(x=450,
                                                                                                            y=350)

    def add_expense(self):
        exp_win = Tk()
        exp_win.geometry("800x1000")
        exp_win.title("Expense")
        win_h = 600
        win_w = 1200
        exp_win.configure(bg="powder blue")
        style = ttk.Style()
        a = Label(exp_win, text="Enter Expense Data", bg="blue", fg='Yellow',
                  font=("Times new roman", 30, "italic", 'bold')).pack(fill='both')  # place(x=50,y=50)
        b = Label(exp_win, text="Select Date: ", font=("Times new roman", 14)).place(x=50, y=70)
        cal = Calendar(exp_win, font=("Times new roman", 10, 'bold'), selectmode='day', cursor="hand1", year=2020,
                       month=7, day=5)
        cal.place(x=50, y=100)
        frame = tk.Frame(exp_win)
        frame.place(x=50, y=320)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Date")
        tree.heading(3, text="Expense Title")
        tree.heading(4, text="Amount")
        tree.column(1, width=50)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=120)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)

        Label(exp_win, text="Expense Title: ", bg="white", font=("Times new roman", 14)).place(x=400, y=100)
        ty = Entry(exp_win, font=("Times new roman", 14))
        ty.place(x=520, y=100)

        Label(exp_win, text="Amount", bg="white", font=("Times new roman", 14)).place(x=400, y=160)
        amt = Entry(exp_win, font=("Times new roman", 14))
        amt.place(x=520, y=160)

        def add():
            i = Expense.assign_id(self)
            a = cal.selection_get()
            c = ty.get()
            f = amt.get()
            print(i, a, c, f)
            tree.insert('', 'end', values=(i, a, c, f))
            Expense.add(self, i, a, c, f)
            messagebox.showinfo('Confirmation', 'Record is added successesfully')

        b1 = Button(exp_win, text="Confirm", command=add).place(x=400, y=250)

        def back():
            exp_win.destroy()
            self.interface()

        b2 = Button(exp_win, text="Main Menu", command=back).place(x=600, y=250)

    def view_exp(self):
        exp = Tk()
        exp.geometry("800x500")
        exp.title("Expense")
        exp.configure(background="powder blue")
        Label(exp, text="Expense", bg="blue", fg="yellow", font=("Times new roman", 30, 'italic')).pack(fill='both')
        frame = Frame(exp)
        frame.place(x=50, y=100)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Date")
        tree.heading(3, text="Title")
        tree.heading(4, text="Amount")
        tree.column(1, width=50)
        tree.column(2, width=80)
        tree.column(3, width=100)
        tree.column(4, width=80)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)
        Expense.view(self)
        con = sqlite3.connect("HyperDatabase.db")
        cursor = con.cursor()
        a = cursor.execute("Select * from Expense")
        con.commit()
        Label(exp, text='Expense Total', width=15, bg='white', fg='blue', font=('times new roman', 14, 'bold')).place(
            x=500, y=200)
        Label(exp, text=(Expense.total(self)), width=15, bg='white', fg='blue',
              font=('times new roman', 14, 'bold')).place(x=500, y=220)
        for i in a:
            print(i)
            tree.insert('', 'end', values=(i))

        def add():
            exp.destroy()
            self.add_expense()

        b1 = Button(exp, text="Add", fg='green', font=('times new roman', 12, 'bold'), command=add).place(x=100, y=350)

        def back():
            exp.destroy()
            self.interface()

        b2 = Button(exp, text="Back", fg="black", font=('times new roman', 12, 'bold'), command=back).place(x=500,
                                                                                                            y=350)

    def add_stock(self):
        st_win = Tk()
        st_win.geometry("800x1000")
        st_win.title("Expense")
        win_h = 600
        win_w = 1200
        st_win.configure(bg="powder blue")
        style = ttk.Style()
        a = Label(st_win, text="Enter Stock Data", bg="blue", fg='yellow',
                  font=("Times new roman", 30, "italic", 'bold')).pack(fill='both')  # place(x=50,y=50)
        frame = tk.Frame(st_win)
        frame.place(x=10, y=350)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Name")
        tree.heading(3, text="Price")
        tree.heading(4, text="Quantity")
        tree.heading(5, text="Amount")
        tree.column(1, width=50)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=120)
        tree.column(5, width=120)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)

        Label(st_win, text="Product Name: ", bg="white", font=("Times new roman", 14)).place(x=50, y=100)
        ty = Entry(st_win, font=("Times new roman", 14))
        ty.place(x=170, y=100)

        Label(st_win, text="Price: ", bg="white", font=("Times new roman", 14)).place(x=50, y=160)
        pr = Entry(st_win, font=("Times new roman", 14))
        pr.place(x=170, y=160)

        Label(st_win, text="Quantity: ", bg="white", font=("Times new roman", 14)).place(x=50, y=220)
        quan = Spinbox(st_win, from_=1, to=1000, width=5, font=("Times new roman", 14))
        quan.place(x=170, y=220)

        def add():
            i = Stock.assign_id(self)
            c = ty.get()
            d = pr.get()
            e = quan.get()
            f = int(d) * int(e)
            print(i, c, d, e, f)
            tree.insert('', 'end', values=(i, c, d, e, f))
            Stock.add(self, i, i, c, d, e, f)
            messagebox.showinfo('Confirmation', 'Record is added successesfully')

        b1 = Button(st_win, text="Confirm", command=add).place(x=450, y=200)

        def back():
            st_win.destroy()
            self.interface()

        b2 = Button(st_win, text="Main Menu", command=back).place(x=650, y=200)

    def view_stock(self):
        stock = Tk()
        stock.geometry("800x500")
        stock.title("Stock")
        stock.configure(background="powder blue")
        Label(stock, text="Stock", bg="blue", fg="yellow", font=("Times new roman", 30, 'italic', 'bold')).pack(
            fill='both')
        frame = Frame(stock)
        frame.place(x=30, y=100)
        tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), height=10, show="headings", style="mystyle.Treeview")
        tree.pack(side='left')
        tree.heading(1, text='ID')
        tree.heading(2, text="Product Name")
        tree.heading(3, text="Price")
        tree.heading(4, text="Quantity")
        tree.heading(5, text="Amount")
        tree.column(1, width=50)
        tree.column(2, width=120)
        tree.column(3, width=100)
        tree.column(4, width=80)
        tree.column(5, width=80)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)
        Stock.view(self)
        print(Stock.total(self))
        con = sqlite3.connect("HyperDatabase.db")
        cursor = con.cursor()
        a = cursor.execute("SELECT * from Stock")
        con.commit()
        for i in a:
            print(i)
            tree.insert('', 'end', values=(i))
        Label(stock, text="Total Stock", bg='white', fg="blue", font=('Times new roman', 14, 'bold'), width=15).place(
            x=500, y=200)
        Label(stock, text=(Stock.total(self)), bg='white', fg="blue", font=('Times new roman', 14, 'bold'),
              width=15).place(x=500, y=220)

        def add():
            stock.destroy()
            self.add_stock()

        b1 = Button(stock, text="Add", fg='green', font=('times new roman', 12, 'bold'), command=add).place(x=100,
                                                                                                            y=350)

        def back():
            stock.destroy()
            self.interface()

        b2 = Button(stock, text="Back", fg="black", font=('times new roman', 12, 'bold'), command=back).place(x=500,
                                                                                                              y=350)

    def cashflow(self):
        win1 = Tk()
        win1.geometry("1000x800")
        win1.title("HyperMart - Cash Flow")
        win_height = 500
        win_width = 800
        screen_width = win1.winfo_screenwidth()
        screen_height = win1.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (win_width / 2))
        y_cordinate = int((screen_height / 2) - (win_height / 2))
        win1.geometry("{}x{}+{}+{}".format(win_width, win_height, x_cordinate, y_cordinate))
        win1.configure(bg="powder blue")
        style = ttk.Style()
        Label(win1, text='Cash-Flow Statement', bg='blue', fg='yellow',
              font=('Times new roman', 30, 'bold', 'italic')).pack(fill='both')
        Label(win1, text="Sale", fg='blue', font=('Times new roman', 20, 'bold'), width=10).place(x=50, y=80)
        Label(win1, text=(CashFlow.sale(self)), fg='blue', font=('Times new roman', 20, 'bold'), width=10).place(x=50,
                                                                                                                 y=120)

        Label(win1, text="Purchase", fg='yellow', font=('Times new roman', 20, 'bold'), width=10).place(x=250, y=80)
        Label(win1, text=(CashFlow.purchase(self)), fg='yellow', font=('Times new roman', 20, 'bold'), width=10).place(
            x=250, y=120)

        Label(win1, text="Expense", fg='red', font=('Times new roman', 20, 'bold'), width=10).place(x=450, y=80)
        Label(win1, text=(CashFlow.exp_total(self)), fg='red', font=('Times new roman', 20, 'bold'), width=10).place(
            x=450, y=120)

        Label(win1, text="Stock", fg='brown', font=('Times new roman', 20, 'bold'), width=10).place(x=350, y=200)
        Label(win1, text=(CashFlow.total_stock(self)), fg='brown', font=('Times new roman', 20, 'bold'),
              width=10).place(x=350, y=240)

        a = CashFlow.profit(self)
        Label(win1, text="Profit", fg='green', font=('Times new roman', 20, 'bold'), width=10).place(x=150, y=200)
        Label(win1, text=(a), fg='green', font=('Times new roman', 20, 'bold'), width=10).place(x=150, y=240)
        if int(a) > 0:
            messagebox.showinfo('CashFlow', 'Conratulation! your store is in profit')
        elif int(a) < 0:
            messagebox.showinfo('CashFlow',
                                'Sorry! Your store is in loss, try improve your salesand lower your expenses')
        elif int(a) == 0:
            messagebox.showinfo('CashFlow', 'It looks like your store is not in profit nor in loss')

        def back():
            win1.destroy()
            self.interface()

        b2 = Button(win1, text="close", fg="black", font=('times new roman', 12, 'bold'), command=back).place(x=500, y=400)


h = HyperMart_CashFlow('nazimabad')

