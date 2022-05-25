import tkinter as tk
import tkinter.ttk as ttk
from datetime import date, datetime
from tkinter import messagebox
import pymysql
from tkcalendar import DateEntry

from main import get_sensor_data
from send_notification import send_notification

DB = pymysql.connect(host='localhost',
                     user='root',
                     password='2051868d',
                     db='projects_competition')

cur = DB.cursor()  # Курсор по БД-шке

shelfs_headings = (
    'Название полки', 'Название товара', 'Дата последнего изменения', 'Количество контейнеров объёмом 100см^3',
    'Длина полки в см', 'Описание устройства отслеживания')
goods_headings = (
    'Название товара', 'Количество товара', 'Срок годности', 'Количество товара в одном контейнере(100см^3)',
    'Стоимость товара', 'Описание товара')

MainWindow = tk.Tk()
MainWindow.title("Учёт товаров на складе")
MainWindow.attributes("-fullscreen", True)
MainWindow["bg"] = "#20B2AA"

ShelfsList = []
GoodsList = []

operation_state = "none"


def UpdateShelfsList():
    global ShelfsList
    ShelfsList = []
    cur.execute("SELECT * FROM shelfs")
    query_result = cur.fetchall()
    for shelf in query_result:
        ShelfsList.append(shelf[1])
    ShelfsList.sort()


def UpdateGoodsList():
    global GoodsList
    GoodsList = []
    cur.execute("SELECT * FROM goods")
    query_result = cur.fetchall()
    for good in query_result:
        GoodsList.append(good[1])
    GoodsList.sort()


UpdateShelfsList()
UpdateGoodsList()

Var_OutputMenu = tk.StringVar(MainWindow)
Var_OutputMenu.set("Выбрать справочник")

Var_Edit_ShelfName_or_GoodName = tk.StringVar(MainWindow)
Var_OutputMenu_Shelfs_or_Goods = tk.StringVar(MainWindow)
Var_Edit_Chosen_GoodLastChangedDate_or_LifeCycle = tk.StringVar(MainWindow)
Var_Edit_GoodQuantity = tk.StringVar(MainWindow)
Var_Edit_GoodLastChangedDate_or_LifeCycle = tk.StringVar(MainWindow)
Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer = tk.StringVar(MainWindow)
Var_Edit_GoodShelfLengthInSM_or_GoodCost = tk.StringVar(MainWindow)

Var_Edit_ShelfGoodName = tk.StringVar(MainWindow)
Var_OutputMenu_Goods = tk.StringVar(MainWindow)


def CheckShelfName(str):
    if str == "":
        messagebox.showerror("Ошибка ввода названия полки", "Название полки не может быть пустым!")
    else:
        if "Выбрать полку для" in str:
            messagebox.showerror("Ошибка ввода названия полки", "Полка не может быть с таким странным именем!")
            return False
        cur.execute('SELECT EXISTS(SELECT * FROM shelfs WHERE shelfName = %s)', str)
        exist_or_not = cur.fetchall()[0][0]
        if exist_or_not == 1:
            messagebox.showerror("Ошибка ввода названия полки", "Полка с таким именем уже есть в базе данных!")
            return False
        return True
    return False


def CheckIfShelfChosen(str):
    if "Выбрать полку для" in str:
        messagebox.showerror("Ошибка выбора полки", "Вы не выбрали Полку!")
    else:
        return True
    return False


def CheckShelfGoodName(str):
    if str == "Выбрать товар для полки":
        messagebox.showerror("Ошибка ввода названия товара для полки", "Вы не выбрали название товара для полки!")
    else:
        return True
    return False


def CheckGoodQuantity(str):
    if str == "":
        messagebox.showerror("Ошибка ввода количества товара", "Вы не выбрали количество товара!")
    else:
        return True
    return False


def CheckShelfLastDateChange(str):
    if str == "":
        messagebox.showerror("Ошибка выбора даты создания полки", "Вы не выбрали дату создания полки!")
    else:
        return True
    return False


def CheckContainersQuantity(str):
    try:
        goods_num = int(str)
        if goods_num < 1:
            messagebox.showerror("Ошибка ввода количества контенеров объёмом 100см^3",
                                 "Вы ввели не положительное количество контейнеров объёмом 100см^3!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода количества контенеров объёмом 100см^3", "Вы ввели не целое количество "
                                                                                   "контейнеров объёмом 100см^3!")
        return False


def CheckGoodShelfLengthInSM(str):
    try:
        invests = float(str)
        if invests < 0.0:
            messagebox.showerror("Ошибка ввода длины полки в сантиметрах", "Вы ввели отрицательное значение длины "
                                                                           "полки в сантиметрах!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода длины полки в сантиметрах", "В поле для длины полки в сантиметрах вы ввели "
                                                                       "не число!")
        return False


def CheckIsThereEnoughPlace(container_quantity, shelf_length):
    try:
        if int(container_quantity) * 100 > int(shelf_length):
            messagebox.showerror("Ошибка подходящих значений", "Для полки такой длины не хватит места для стольких "
                                                               "контейнеров")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка подходящих значений", "Для полки такой длины не хватит места для стольких "
                                                           "контейнеров")
        return False


def CheckGoodName(str):
    if str == "":
        messagebox.showerror("Ошибка ввода названия товара", "Название товара не может быть пустым!")
    else:
        return True
    return False


def CheckIfGoodChosen(str):
    if "Выбрать товар для" in str:
        messagebox.showerror("Ошибка выбора товара", "Вы не выбрали товар!")
    else:
        return True
    return False


def CheckLifeCycle(str):
    if str == "":
        messagebox.showerror("Ошибка выбора срока годности", "Вы не выбрали срок годности товара!")
    else:
        return True
    return False


def CheckGoodQuantityInOneContainer(str):
    try:
        tasks_num = int(str)
        if tasks_num < 1:
            messagebox.showerror("Ошибка ввода числа количества товара в одном контейнере объёмом 100см^3",
                                 "Вы ввели не положительное число количества товара в одном контейнере объёмом 100см^3!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода числа количества товара в одном контейнере объёмом 100см^3",
                             "Вы ввели не целое число количества товара в одном контейнере объёмом 100см^3!")
        return False


def CheckGoodCost(str):
    try:
        rating = float(str)
        if rating < 0.0:
            messagebox.showerror("Ошибка ввода стоимости товара",
                                 "Вы ввели отрицательное значение стоимость товара!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода стоимости товара", "В поле для стоимости товара вы ввели не число!")
        return False


def Update_Data_By_Sensor():
    sensor_data = get_sensor_data()

    if sensor_data < 20.2:
        cur.execute(
            "UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s",
            (date.today(), 3, 1))
        cur.execute(
            "UPDATE goods SET goodQuantity = %s WHERE goodID = %s",
            (36, 1))
    elif (sensor_data > 20.2) and (sensor_data < 120.2):
        cur.execute(
            "UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s",
            (date.today(), 2, 1))
        cur.execute(
            "UPDATE goods SET goodQuantity = %s WHERE goodID = %s",
            (24, 1))
    elif (sensor_data > 120.2) and (sensor_data < 220.2):
        cur.execute(
            "UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s",
            (date.today(), 1, 1))
        cur.execute(
            "UPDATE goods SET goodQuantity = %s WHERE goodID = %s",
            (12, 1))
        # send_notification("There only 12 packs of milk left in your warehouse")
    elif sensor_data > 220.2:
        cur.execute(
            "UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s",
            (date.today(), 0, 1))
        cur.execute(
            "UPDATE goods SET goodQuantity = %s WHERE goodID = %s",
            (0, 1))
        # send_notification("There no packs of milk left in your warehouse")

    Select_Data()

    cur.execute("SELECT * FROM goods WHERE goodID = 1")
    query_result = cur.fetchall()
    for str_i in query_result:

        difference = abs((str_i[3] - date.today()).days)

        if difference <= 7:
            message = "Product Milk will expire in " + str(difference) + " days"
            print(message)
            send_notification(message)


def Select_Data():
    if Var_OutputMenu.get() == "полки":
        for row in Table_Shelfs_output.get_children():
            Table_Shelfs_output.delete(row)
        cur.execute("SELECT * FROM shelfs")
        query_result = cur.fetchall()
        goodNAMEs_list = []
        i = 0
        for str in query_result:
            i += 1
            if i == 16:
                a = 5
            if str[2] is None:
                cur.execute("SELECT goodOldHereName FROM shelfs WHERE shelfID = %s", str[0])
            else:
                cur.execute("SELECT goodNAME FROM goods WHERE goodID = %s", str[2])
            goodNAME = ''.join(cur.fetchall()[0])
            goodNAMEs_list.append(goodNAME)
        i = 0
        for str in query_result:
            dsc_text = str[6].replace('\n', ' ')
            Table_Shelfs_output.insert('', tk.END,
                                       values=tuple([str[1], goodNAMEs_list[i], str[3], str[4], str[5], dsc_text]))
            i += 1
    elif Var_OutputMenu.get() == "товар":
        for row in Table_Goods_output.get_children():
            Table_Goods_output.delete(row)
        cur.execute("SELECT * FROM goods")
        query_result = cur.fetchall()
        for str in query_result:
            dsc_text = str[6].replace('\n', ' ')
            Table_Goods_output.insert('', tk.END, values=tuple([str[1], str[2], str[3], str[4], str[5], dsc_text]))


def Start_Any_Operation():
    OutputMenu_ChooseDir["state"] = "disabled"
    Btn_Select_Data["state"] = "disabled"
    Btn_Add_Data["state"] = "disabled"
    Btn_Edit_Data["state"] = "disabled"
    Btn_Delete_Data["state"] = "disabled"
    Btn_Cancel.place(relx=0.12, rely=0.93, anchor="c")
    if Var_OutputMenu.get() == "полки":
        Table_Shelfs_output.place_forget()
        Table_Shelfs_output_scroll_vertical.place_forget()
        Table_Shelfs_output_scroll_horizontal.place_forget()
        Lbl_Enter_Shelf_Name.place(relx=0.188, rely=0.27, anchor="c")
        Lbl_Enter_Shelf_ShelfGoodName.place(relx=0.17, rely=0.37, anchor="c")
        Lbl_Enter_Shelf_DateLastChange.place(relx=0.16, rely=0.47, anchor="c")
        Lbl_Enter_Shelf_ContainersQuantity.place(relx=0.168, rely=0.57, anchor="c")
        Lbl_Enter_Shelf_LengthInSM.place(relx=0.175, rely=0.67, anchor="c")
        Lbl_Enter_Shelf_Description.place(relx=0.187, rely=0.77, anchor="c")
        TxtEdit_Enter_ShelfDateLastChange_or_LifeCycle.place(relx=0.353, rely=0.47, anchor="c")
        TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer.place(relx=0.47, rely=0.57, anchor="c")
        TxtEdit_Enter_ShelfLengthInSM_or_GoodCost.place(relx=0.47, rely=0.67, anchor="c")
        Text_Enter_Shelf_or_Good_Description.place(relx=0.481, rely=0.79, anchor="c")
        Description_scroll_vertical.place(relx=0.305, rely=0.73, height=107, width=25)
        Description_scroll_horizontal.place(relx=0.32, rely=0.85, height=25, width=493)
        Lbl_Enter_Description_Additional.place(relx=0.19, rely=0.82, anchor="c")
    elif Var_OutputMenu.get() == "товар":
        Table_Goods_output.place_forget()
        Table_Goods_output_scroll_vertical.place_forget()
        Table_Goods_output_scroll_horizontal.place_forget()
        Lbl_Enter_Good_Name.place(relx=0.184, rely=0.3, anchor="c")
        Lbl_Enter_Good_LifeCycle.place(relx=0.184, rely=0.38, anchor="c")
        Lbl_Enter_Shelf_GoodQuantity.place(relx=0.16, rely=0.46, anchor="c")
        Lbl_Enter_Good_Quantity_in_one_container.place(relx=0.159, rely=0.54, anchor="c")
        Lbl_Enter_Good_Cost.place(relx=0.158, rely=0.66, anchor="c")
        Lbl_Enter_Good_Description.place(relx=0.158, rely=0.77, anchor="c")
        Lbl_Enter_Description_Additional.place(relx=0.16, rely=0.82, anchor="c")
        TxtEdit_Enter_ShelfDateLastChange_or_LifeCycle.place(relx=0.353, rely=0.38, anchor="c")
        TxtEdit_Enter_Good_quantity.place(relx=0.469, rely=0.46, anchor="c")
        TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer.place(relx=0.47, rely=0.54, anchor="c")
        TxtEdit_Enter_ShelfLengthInSM_or_GoodCost.place(relx=0.47, rely=0.66, anchor="c")
        Text_Enter_Shelf_or_Good_Description.place(relx=0.481, rely=0.78, anchor="c")
        Description_scroll_vertical.place(relx=0.305, rely=0.719, height=107, width=25)
        Description_scroll_horizontal.place(relx=0.32, rely=0.85, height=25, width=493)


def Update_option_menu(curr_menu, new_list, var_str):
    new_menu = curr_menu["menu"]
    new_menu.delete(0, "end")
    for str in new_list:
        new_menu.add_command(label=str, command=lambda value=str: var_str.set(value))


def Finish_Any_Operation():
    global operation_state
    operation_state = "none"
    UpdateShelfsList()
    UpdateGoodsList()
    Update_option_menu(OutputMenu_Choose_Good, GoodsList, Var_OutputMenu_Goods)
    OutputMenu_ChooseDir["state"] = "normal"
    Btn_Select_Data["state"] = "normal"
    Btn_Add_Data["state"] = "normal"
    Btn_Edit_Data["state"] = "normal"
    Btn_Delete_Data["state"] = "normal"
    Btn_Cancel.place_forget()
    Lbl_Add_Data.place_forget()
    Lbl_Edit_Data.place_forget()
    Lbl_Delete_Data.place_forget()
    TxtEdit_Enter_ShelfName_or_GoodName.place_forget()
    Var_Edit_ShelfName_or_GoodName.set("")
    OutputMenu_Choose_Good.place_forget()
    OutputMenu_Choose_Shelf_or_Good.place_forget()
    TxtEdit_Enter_ShelfDateLastChange_or_LifeCycle.place_forget()
    Var_Edit_GoodQuantity.set("")
    Var_Edit_GoodLastChangedDate_or_LifeCycle.set("")
    Btn_Choose_Date.place_forget()
    TxtEdit_Enter_Good_quantity.place_forget()
    TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer.place_forget()
    Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.set("")
    TxtEdit_Enter_ShelfLengthInSM_or_GoodCost.place_forget()
    Var_Edit_GoodShelfLengthInSM_or_GoodCost.set("")
    Description_scroll_vertical.place_forget()
    Description_scroll_horizontal.place_forget()
    Btn_Add_Data_Commit.place_forget()
    Btn_Edit_Data_Commit.place_forget()
    Btn_Delete_Data_Commit.place_forget()
    TxtEdit_Enter_Good_quantity["state"] = "normal"
    TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer["state"] = "normal"
    TxtEdit_Enter_ShelfLengthInSM_or_GoodCost["state"] = "normal"
    Text_Enter_Shelf_or_Good_Description["state"] = "normal"
    Text_Enter_Shelf_or_Good_Description.place_forget()
    Text_Enter_Shelf_or_Good_Description.delete(1.0, tk.END)
    Lbl_Enter_Description_Additional.place_forget()
    if Var_OutputMenu.get() == "полки":
        Update_option_menu(OutputMenu_Choose_Shelf_or_Good, ShelfsList, Var_OutputMenu_Shelfs_or_Goods)
        Lbl_Enter_Shelf_Name.place_forget()
        Lbl_Enter_Shelf_ShelfGoodName.place_forget()
        Lbl_Enter_Shelf_DateLastChange.place_forget()
        Lbl_Enter_Shelf_ContainersQuantity.place_forget()
        Lbl_Enter_Shelf_LengthInSM.place_forget()
        Lbl_Enter_Shelf_Description.place_forget()
        TxtEdit_ShelfGoodName.place_forget()
        Var_Edit_ShelfGoodName.set("")
        TxtEdit_ShelfGoodName["state"] = "normal"
        for row in Table_Shelfs_output.get_children():
            Table_Shelfs_output.delete(row)
        Table_Shelfs_output_scroll_vertical.place(relx=0.003, rely=0.14, height=706, width=25)
        Table_Shelfs_output_scroll_horizontal.place(relx=0.02, rely=0.96, height=25, width=993)
        Table_Shelfs_output.place(relx=0.02, rely=0.14)
    elif Var_OutputMenu.get() == "товар":
        Update_option_menu(OutputMenu_Choose_Shelf_or_Good, GoodsList, Var_OutputMenu_Shelfs_or_Goods)
        Lbl_Enter_Good_Name.place_forget()
        Lbl_Enter_Good_LifeCycle.place_forget()
        Lbl_Enter_Shelf_GoodQuantity.place_forget()
        Lbl_Enter_Good_Quantity_in_one_container.place_forget()
        Lbl_Enter_Good_Cost.place_forget()
        Lbl_Enter_Good_Description.place_forget()
        for row in Table_Goods_output.get_children():
            Table_Goods_output.delete(row)
        Table_Goods_output_scroll_vertical.place(relx=0.003, rely=0.14, height=706, width=25)
        Table_Goods_output_scroll_horizontal.place(relx=0.02, rely=0.96, height=25, width=993)
        Table_Goods_output.place(relx=0.02, rely=0.14)


CalWindow = tk.Toplevel(MainWindow)
CalWindow.title("Выбрать дату из календаря")
CalWindow.geometry("500x300")
CalWindow.resizable(width=False, height=False)
CalWindow["bg"] = "#20B2AA"
CalWindow.withdraw()


def Close_Cal_Window():
    Btn_Choose_Date["state"] = "normal"
    Btn_Add_Data_Commit["state"] = "normal"
    Btn_Edit_Data_Commit["state"] = "normal"
    Btn_Cancel["state"] = "normal"
    date_data_list = Var_Edit_Chosen_GoodLastChangedDate_or_LifeCycle.get().split("/")
    if len(date_data_list[1]) == 1:
        date_data_list[1] = '0' + date_data_list[1]
    if len(date_data_list[0]) == 1:
        date_data_list[0] = '0' + date_data_list[0]
    Var_Edit_GoodLastChangedDate_or_LifeCycle.set(
        date_data_list[1] + '.' + date_data_list[0] + '.20' + date_data_list[2])
    CalWindow.withdraw()


CalWindow.protocol("WM_DELETE_WINDOW", Close_Cal_Window)


def Choose_Date():
    Btn_Choose_Date["state"] = "disabled"
    Btn_Add_Data_Commit["state"] = "disabled"
    Btn_Edit_Data_Commit["state"] = "disabled"
    Btn_Cancel["state"] = "disabled"
    CalWindow.deiconify()
    Lbl_Choose_Date_From_Calendar = tk.Label(CalWindow, text='Выберите дату:',
                                             font=("Arial Bold", 28), bg="#20B2AA")
    Lbl_Choose_Date_From_Calendar.place(relx=0.5, rely=0.1, anchor="c")
    cal = DateEntry(CalWindow, font=("Arial Bold", 28), width=15, background='#008B8B', borderwidth=7, state="readonly",
                    textvariable=Var_Edit_Chosen_GoodLastChangedDate_or_LifeCycle)
    cal.place(relx=0.5, rely=0.3, anchor="c")
    Btn_Confirm_Chosen_Date = tk.Button(CalWindow, text="Подтвердить дату", font=("Arial Bold", 24), bd=10,
                                        background="#008B8B", command=Close_Cal_Window, width=20)
    Btn_Confirm_Chosen_Date.place(relx=0.5, rely=0.7, anchor="c")


def Add_Data():
    global operation_state
    operation_state = "add"
    Start_Any_Operation()
    Lbl_Add_Data.place(relx=0.34, rely=0.18, anchor="c")
    Btn_Add_Data_Commit.place(relx=0.47, rely=0.925, anchor="c")
    if Var_OutputMenu.get() == "полки":
        Var_OutputMenu_Goods.set("Выбрать товар для полки")
        OutputMenu_Choose_Good.place(relx=0.47, rely=0.37, anchor="c")
        TxtEdit_Enter_ShelfName_or_GoodName.place(relx=0.47, rely=0.27, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.47, anchor="c")
    elif Var_OutputMenu.get() == "товар":
        TxtEdit_Enter_ShelfName_or_GoodName.place(relx=0.47, rely=0.3, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.38, anchor="c")


def Add_Data_Confirm():
    if Var_OutputMenu.get() == "полки":
        shelfName = Var_Edit_ShelfName_or_GoodName.get()
        shelfGoodName = Var_OutputMenu_Goods.get()
        shelfCrDate = Var_Edit_GoodLastChangedDate_or_LifeCycle.get()
        shelfContainersQuantity = Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.get()
        goodShelfLengthInSM = Var_Edit_GoodShelfLengthInSM_or_GoodCost.get()
        shelfDescription = Text_Enter_Shelf_or_Good_Description.get(1.0, tk.END)
        if CheckShelfName(shelfName):
            if CheckShelfGoodName(shelfGoodName):
                if CheckShelfLastDateChange(shelfCrDate):
                    if CheckContainersQuantity(shelfContainersQuantity):
                        if CheckGoodShelfLengthInSM(goodShelfLengthInSM):
                            if CheckIsThereEnoughPlace(shelfContainersQuantity, goodShelfLengthInSM):
                                try:
                                    cur.execute("SELECT goodID FROM goods WHERE goodNAME = %s", shelfGoodName)
                                    goodID = cur.fetchall()[0][0]
                                    shelfCrDateList = shelfCrDate.split('.')
                                    day = shelfCrDateList[0]
                                    month = shelfCrDateList[1]
                                    year = shelfCrDateList[2]
                                    shelfCrDate = year + '-' + month + '-' + day
                                    if shelfDescription == "\n":
                                        shelfDescription = "No additional information"
                                    cur.execute(
                                        'INSERT INTO shelfs (shelfName, goodHereID, goodLastChangedDate,'
                                        ' goodContainersAmount, goodShelfLengthInSM, shelfDescript, goodOldHereName)'
                                        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                        (
                                            shelfName, goodID, shelfCrDate, shelfContainersQuantity,
                                            goodShelfLengthInSM,
                                            shelfDescription,
                                            shelfGoodName))
                                    messagebox.showinfo("Успешное добавление записи в базу данных",
                                                        "Добавление записи о Полке в базу данных проведено успешно!")
                                    DB.commit()
                                    Finish_Any_Operation()
                                except:
                                    DB.rollback()
                                    messagebox.showerror("Ошибка при добавлении данных в базу",
                                                         "По неизвестной причине не удалось добавить данные в БД!")
    elif Var_OutputMenu.get() == "товар":
        goodName = Var_Edit_ShelfName_or_GoodName.get()
        lifeCycle = Var_Edit_GoodLastChangedDate_or_LifeCycle.get()
        goodQuantity = Var_Edit_GoodQuantity.get()
        goodQuantityInOneContainer = Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.get()
        goodCost = Var_Edit_GoodShelfLengthInSM_or_GoodCost.get()
        goodDescription = Text_Enter_Shelf_or_Good_Description.get(1.0, tk.END)
        if CheckGoodName(goodName):
            if CheckLifeCycle(lifeCycle):
                if CheckGoodQuantity(goodQuantity):
                    if CheckGoodQuantityInOneContainer(goodQuantityInOneContainer):
                        if CheckGoodCost(goodCost):
                            try:
                                lifeCycleList = lifeCycle.split('.')
                                day = lifeCycleList[0]
                                month = lifeCycleList[1]
                                year = lifeCycleList[2]
                                lifeCycle = year + '-' + month + '-' + day
                                if goodDescription == "\n":
                                    goodDescription = "No additional information"
                                cur.execute(
                                    'INSERT INTO goods (goodNAME, goodQuantity, shelfLife, goodQuantityInOneContainer,'
                                    ' goodCost, goodDescript)'
                                    'VALUES (%s, %s, %s, %s, %s, %s)',
                                    (goodName, goodQuantity, lifeCycle, goodQuantityInOneContainer,
                                     goodCost, goodDescription))
                                messagebox.showinfo("Успешное добавление записи в базу данных",
                                                    "Добавление записи о товаре в базу данных проведено успешно!")
                                DB.commit()
                                Finish_Any_Operation()
                            except:
                                DB.rollback()
                                messagebox.showerror("Ошибка при добавлении данных в базу",
                                                     "По неизвестной причине не удалось добавить данные в БД!")


def Edit_Data():
    global operation_state
    operation_state = "edit"
    Start_Any_Operation()
    Lbl_Edit_Data.place(relx=0.34, rely=0.18, anchor="c")
    Btn_Edit_Data_Commit.place(relx=0.47, rely=0.925, anchor="c")
    if Var_OutputMenu.get() == "полки":
        Var_OutputMenu_Shelfs_or_Goods.set("Выбрать полку для изменений")
        Var_OutputMenu_Goods.set("Выбрать товар для полки")
        OutputMenu_Choose_Shelf_or_Good.place(relx=0.47, rely=0.27, anchor="c")
        OutputMenu_Choose_Good.place(relx=0.47, rely=0.37, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.47, anchor="c")
    elif Var_OutputMenu.get() == "товар":
        Var_OutputMenu_Shelfs_or_Goods.set("Выбрать товара для изменений")
        OutputMenu_Choose_Shelf_or_Good.place(relx=0.47, rely=0.3, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.38, anchor="c")


def Edit_Data_Confirm():
    if Var_OutputMenu.get() == "полки":
        shelfName = Var_OutputMenu_Shelfs_or_Goods.get()
        shelfGoodName = Var_OutputMenu_Goods.get()
        shelfCrDate = Var_Edit_GoodLastChangedDate_or_LifeCycle.get()
        shelfContainersQuantity = Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.get()
        goodShelfLengthInSM = Var_Edit_GoodShelfLengthInSM_or_GoodCost.get()
        shelfDescription = Text_Enter_Shelf_or_Good_Description.get(1.0, tk.END)
        if CheckIfShelfChosen(shelfName):
            if CheckShelfGoodName(shelfGoodName):
                if CheckShelfLastDateChange(shelfCrDate):
                    if CheckContainersQuantity(shelfContainersQuantity):
                        if CheckGoodShelfLengthInSM(goodShelfLengthInSM):
                            if CheckIsThereEnoughPlace(shelfContainersQuantity, goodShelfLengthInSM):
                                try:
                                    cur.execute("SELECT shelfID FROM shelfs WHERE shelfName = %s", shelfName)
                                    shelfID = cur.fetchall()[0][0]
                                    cur.execute("SELECT goodID FROM goods WHERE goodNAME = %s", shelfGoodName)
                                    goodID = cur.fetchall()[0][0]
                                    shelfCrDateList = shelfCrDate.split('.')
                                    day = shelfCrDateList[0]
                                    month = shelfCrDateList[1]
                                    year = shelfCrDateList[2]
                                    shelfCrDate = year + '-' + month + '-' + day
                                    if shelfDescription == "\n":
                                        shelfDescription = "No additional information"
                                    cur.execute(
                                        'UPDATE shelfs SET shelfName = %s, goodHereID = %s, goodLastChangedDate = %s, goodContainersAmount = %s,'
                                        'goodShelfLengthInSM = %s, shelfDescript = %s, goodOldHereName = %s WHERE shelfID = %s',
                                        (shelfName, goodID, shelfCrDate, shelfContainersQuantity, goodShelfLengthInSM,
                                         shelfDescription,
                                         shelfGoodName, shelfID))
                                    messagebox.showinfo("Успешное редактирование записи в базе данных",
                                                        "Редактирование записи о Полке в базе данных проведено успешно!")
                                    DB.commit()
                                    Finish_Any_Operation()
                                except:
                                    DB.rollback()
                                    messagebox.showerror("Ошибка при редактировании данных в базу",
                                                         "По неизвестной причине не удалось редактировать данные в БД!")
    elif Var_OutputMenu.get() == "товар":
        goodName = Var_OutputMenu_Shelfs_or_Goods.get()
        lifeCycle = Var_Edit_GoodLastChangedDate_or_LifeCycle.get()
        goodQuantity = Var_Edit_GoodQuantity.get()
        goodQuantityInOneContainer = Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.get()
        goodCost = Var_Edit_GoodShelfLengthInSM_or_GoodCost.get()
        goodDescription = Text_Enter_Shelf_or_Good_Description.get(1.0, tk.END)
        if CheckIfGoodChosen(goodName):
            if CheckLifeCycle(lifeCycle):
                if CheckGoodQuantity(goodQuantity):
                    if CheckGoodQuantityInOneContainer(goodQuantityInOneContainer):
                        if CheckGoodCost(goodCost):
                            try:
                                cur.execute("SELECT goodID FROM goods WHERE goodNAME = %s", goodName)
                                goodID = cur.fetchall()[0][0]
                                lifeCycleList = lifeCycle.split('.')
                                day = lifeCycleList[0]
                                month = lifeCycleList[1]
                                year = lifeCycleList[2]
                                lifeCycle = year + '-' + month + '-' + day
                                if goodDescription == "\n":
                                    goodDescription = "No additional information"
                                cur.execute(
                                    'UPDATE goods SET goodNAME = %s, goodQuantity = %s, shelfLife = %s, goodQuantityInOneContainer = %s,'
                                    'goodCost = %s, goodDescript = %s WHERE goodID = %s',
                                    (goodName, goodQuantity, lifeCycle, goodQuantityInOneContainer,
                                     goodCost, goodDescription, goodID))
                                messagebox.showinfo("Успешное редактирование записи в базе данных",
                                                    "Редактирование записи о товаре в базе данных проведено успешно!")
                                DB.commit()
                                Finish_Any_Operation()
                            except:
                                DB.rollback()
                                messagebox.showerror("Ошибка при редактировании данных в базе",
                                                     "По неизвестной причине не удалось редактировать данные в БД!")


def Delete_Data():
    global operation_state
    operation_state = "delete"
    Start_Any_Operation()
    Lbl_Delete_Data.place(relx=0.34, rely=0.18, anchor="c")
    Btn_Delete_Data_Commit.place(relx=0.47, rely=0.925, anchor="c")
    if Var_OutputMenu.get() == "полки":
        Var_OutputMenu_Shelfs_or_Goods.set("Выбрать полку для удаления")
        OutputMenu_Choose_Shelf_or_Good.place(relx=0.47, rely=0.27, anchor="c")
        TxtEdit_ShelfGoodName.place(relx=0.47, rely=0.37, anchor="c")
        TxtEdit_ShelfGoodName["state"] = "readonly"
        TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer["state"] = "readonly"
        TxtEdit_Enter_ShelfLengthInSM_or_GoodCost["state"] = "readonly"
        Text_Enter_Shelf_or_Good_Description["state"] = "disable"
    elif Var_OutputMenu.get() == "товар":
        Var_OutputMenu_Shelfs_or_Goods.set("Выбрать товара для удаления")
        OutputMenu_Choose_Shelf_or_Good.place(relx=0.47, rely=0.3, anchor="c")
        TxtEdit_Enter_Good_quantity["state"] = "readonly"
        TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer["state"] = "readonly"
        TxtEdit_Enter_ShelfLengthInSM_or_GoodCost["state"] = "readonly"
        Text_Enter_Shelf_or_Good_Description["state"] = "disable"


def Delete_Data_Confirm():
    if Var_OutputMenu.get() == "полки":
        shelfName = Var_OutputMenu_Shelfs_or_Goods.get()
        if CheckIfShelfChosen(shelfName):
            try:
                cur.execute("DELETE FROM shelfs WHERE shelfName = %s", shelfName)
                messagebox.showinfo("Успешное удаление записи из базы данных",
                                    "Удаление записи о Полке из базы данных проведено успешно!")
                DB.commit()
                Finish_Any_Operation()
            except:
                DB.rollback()
                messagebox.showerror("Ошибка при удалении данных из базы",
                                     "По неизвестной причине не удалось удалить данные в БД!")
    elif Var_OutputMenu.get() == "товар":
        goodName = Var_OutputMenu_Shelfs_or_Goods.get()
        if CheckIfGoodChosen(goodName):
            try:

                cur.execute("UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE goodHereID ="
                            "(SELECT goodID FROM goods WHERE goodNAME = %s)", (date.today(), 0, goodName))
                cur.execute("DELETE FROM goods WHERE goodNAME = %s", goodName)
                messagebox.showinfo("Успешное удаление записи из базы данных",
                                    "Удаление записи о товаре из базы данных проведено успешно!")
                DB.commit()
                Finish_Any_Operation()
            except:
                DB.rollback()
                messagebox.showerror("Ошибка при удалении данных из базы",
                                     "По неизвестной причине не удалось удалить данные в БД!")


def Shelf_or_Good_For_Delete_Chosen(*args):
    global operation_state
    if operation_state == "delete":
        shelf_or_good_Name = Var_OutputMenu_Shelfs_or_Goods.get()
        if Var_OutputMenu.get() == "полки":
            if "Выбрать полку для" not in shelf_or_good_Name:
                cur.execute("SELECT * FROM shelfs WHERE shelfName = %s", shelf_or_good_Name)
                shelf_info = cur.fetchall()
                leader_id = shelf_info[0][2]
                cur.execute("SELECT goodNAME FROM goods WHERE goodID = %s", leader_id)
                Var_Edit_ShelfGoodName.set(cur.fetchall()[0][0])
                Var_Edit_GoodLastChangedDate_or_LifeCycle.set(str(shelf_info[0][3]))
                Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.set(str(shelf_info[0][4]))
                Var_Edit_GoodShelfLengthInSM_or_GoodCost.set(shelf_info[0][5])
                Text_Enter_Shelf_or_Good_Description["state"] = "normal"
                Text_Enter_Shelf_or_Good_Description.delete(1.0, tk.END)
                Text_Enter_Shelf_or_Good_Description.insert(tk.END, shelf_info[0][6])
                Text_Enter_Shelf_or_Good_Description["state"] = "disable"
        elif Var_OutputMenu.get() == "товар":
            if "Выбрать товара для" not in shelf_or_good_Name:
                cur.execute("SELECT * FROM goods WHERE goodNAME = %s", shelf_or_good_Name)
                shelf_or_good_info = cur.fetchall()
                Var_Edit_GoodQuantity.set(str(shelf_or_good_info[0][2]))
                Var_Edit_GoodLastChangedDate_or_LifeCycle.set(str(shelf_or_good_info[0][3]))
                Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer.set(str(shelf_or_good_info[0][4]))
                Var_Edit_GoodShelfLengthInSM_or_GoodCost.set(shelf_or_good_info[0][5])
                Text_Enter_Shelf_or_Good_Description["state"] = "normal"
                Text_Enter_Shelf_or_Good_Description.delete(1.0, tk.END)
                Text_Enter_Shelf_or_Good_Description.insert(tk.END, shelf_or_good_info[0][6])
                Text_Enter_Shelf_or_Good_Description["state"] = "disable"


Var_OutputMenu_Shelfs_or_Goods.trace("w", Shelf_or_Good_For_Delete_Chosen)

Lbl_FIO = tk.Label(MainWindow, text="Система учёта товаров на складе",
                   font=("Arial Bold", 28), bg="#20B2AA")
Lbl_FIO.place(relx=0.215, rely=0.025, anchor="c")

Lbl_Start = tk.Label(MainWindow, text='Программа для ручного учёта товаров на складе\n\n'
                                      'База данных автоматически обновляется по кнопке\n\n'
                                      'Язык программирования: Python\n\n'
                                      'Технологии: Tkinter, pymysql\n\n'
                                      'Среда разработки: PyCharm\n\n',
                     font=("Times New Roman", 32), bg="#20B2AA")
Lbl_Start.place(relx=0.33, rely=0.5, anchor="c")


def Dir_Chosen(*args):
    Lbl_Start.place_forget()
    if Var_OutputMenu.get() == "полки":
        UpdateShelfsList()
        Update_option_menu(OutputMenu_Choose_Shelf_or_Good, ShelfsList, Var_OutputMenu_Shelfs_or_Goods)
        OutputMenu_Choose_Shelf_or_Good.config(font=("Times New Roman", 24), width=29)
        Lbl_Dir_Goods.place_forget()
        Table_Goods_output_scroll_vertical.place_forget()
        Table_Goods_output_scroll_horizontal.place_forget()
        Table_Goods_output.place_forget()
        for row in Table_Shelfs_output.get_children():
            Table_Shelfs_output.delete(row)
        Lbl_Dir_Shelfs.place(relx=0.34, rely=0.1, anchor="c")
        Table_Shelfs_output_scroll_vertical.place(relx=0.003, rely=0.14, height=706, width=25)
        Table_Shelfs_output_scroll_horizontal.place(relx=0.02, rely=0.96, height=25, width=993)
        Table_Shelfs_output.place(relx=0.02, rely=0.14)
    elif Var_OutputMenu.get() == "товар":
        UpdateGoodsList()
        Update_option_menu(OutputMenu_Choose_Shelf_or_Good, GoodsList, Var_OutputMenu_Shelfs_or_Goods)
        OutputMenu_Choose_Shelf_or_Good.config(font=("Times New Roman", 18), width=39)
        Lbl_Dir_Shelfs.place_forget()
        Table_Shelfs_output_scroll_vertical.place_forget()
        Table_Shelfs_output_scroll_horizontal.place_forget()
        Table_Shelfs_output.place_forget()
        for row in Table_Goods_output.get_children():
            Table_Goods_output.delete(row)
        Lbl_Dir_Goods.place(relx=0.34, rely=0.1, anchor="c")
        Table_Goods_output_scroll_vertical.place(relx=0.003, rely=0.14, height=706, width=25)
        Table_Goods_output_scroll_horizontal.place(relx=0.02, rely=0.96, height=25, width=993)
        Table_Goods_output.place(relx=0.02, rely=0.14)
    Btn_Select_Data["state"] = "normal"
    Btn_Add_Data["state"] = "normal"
    Btn_Edit_Data["state"] = "normal"
    Btn_Delete_Data["state"] = "normal"


Lbl_ChooseDir = tk.Label(MainWindow, text="Выберите интересующий вас справочник:",
                         font=("Arial Bold", 18), bg="#20B2AA")
Lbl_ChooseDir.place(relx=0.83, rely=0.07, anchor="c")

OutputMenu_ChooseDir = tk.OptionMenu(MainWindow, Var_OutputMenu, "полки", "товар")
OutputMenu_ChooseDir.config(font=("Times New Roman", 28), bg="#008B8B", bd=5, width=20)
OutputMenu_ChooseDir.place(relx=0.83, rely=0.14, anchor="c")

Var_OutputMenu.trace("w", Dir_Chosen)

Btn_Update_Data_By_Sensor = tk.Button(MainWindow, text="Обновить данные полок (Shelf 1-1-1)", font=("Arial Bold", 14),
                                      bd=10, background="#008B8B", command=Update_Data_By_Sensor, width=40)
Btn_Update_Data_By_Sensor.place(relx=0.83, rely=0.22, anchor="c")

Btn_Select_Data = tk.Button(MainWindow, text="Вывести все записи", font=("Arial Bold", 28), bd=10,
                            background="#008B8B", command=Select_Data, width=20, state="disabled")
Btn_Select_Data.place(relx=0.83, rely=0.34, anchor="c")

Lbl_Add_Data = tk.Label(MainWindow, text='Добавление записи',
                        font=("Arial Bold", 36), bg="#20B2AA")

Lbl_Edit_Data = tk.Label(MainWindow, text='Редактирование записи',
                         font=("Arial Bold", 36), bg="#20B2AA")

Lbl_Delete_Data = tk.Label(MainWindow, text='Удаление записи',
                           font=("Arial Bold", 36), bg="#20B2AA")

Lbl_Enter_Shelf_Name = tk.Label(MainWindow, text='Название полки:',
                                font=("Arial Bold", 28), bg="#20B2AA")

Lbl_Enter_Good_Name = tk.Label(MainWindow, text='Название товара:',
                               font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_ShelfName_or_GoodName = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                               textvariable=Var_Edit_ShelfName_or_GoodName)

OutputMenu_Choose_Shelf_or_Good = tk.OptionMenu(MainWindow, Var_OutputMenu_Shelfs_or_Goods, *ShelfsList)
OutputMenu_Choose_Shelf_or_Good.config(font=("Times New Roman", 24), bg="#008B8B", bd=5, width=29)

Lbl_Enter_Shelf_ShelfGoodName = tk.Label(MainWindow, text='Название товара для полки:',
                                         font=("Arial Bold", 23), bg="#20B2AA")

TxtEdit_ShelfGoodName = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                 textvariable=Var_Edit_ShelfGoodName)

OutputMenu_Choose_Good = tk.OptionMenu(MainWindow, Var_OutputMenu_Goods, *GoodsList)
OutputMenu_Choose_Good.config(font=("Times New Roman", 24), bg="#008B8B", bd=5, width=29)

Lbl_Enter_Shelf_DateLastChange = tk.Label(MainWindow, text='Дата последнего изменения на полке:',
                                          font=("Arial Bold", 18), bg="#20B2AA")

Lbl_Enter_Good_LifeCycle = tk.Label(MainWindow, text='Срок годности:',
                                    font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_ShelfDateLastChange_or_LifeCycle = tk.Entry(MainWindow, width=10, bd=5, font=("Arial Bold", 20),
                                                          textvariable=Var_Edit_GoodLastChangedDate_or_LifeCycle,
                                                          state="readonly")

Btn_Choose_Date = tk.Button(MainWindow, text="Выбрать дату", font=("Arial Bold", 22), bd=10,
                            background="#008B8B", command=Choose_Date, width=18)

Lbl_Enter_Shelf_ContainersQuantity = tk.Label(MainWindow, text='Количество контейнеров объёмом 100см^3:',
                                              font=("Arial Bold", 15), bg="#20B2AA")

Lbl_Enter_Shelf_GoodQuantity = tk.Label(MainWindow, text='Количество товара:',
                                        font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_Good_quantity = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                       textvariable=Var_Edit_GoodQuantity)

Lbl_Enter_Good_Quantity_in_one_container = tk.Label(MainWindow, text='Количество товара в одном контейнере(100см^3):',
                                                    font=("Arial Bold", 14), bg="#20B2AA")

TxtEdit_Enter_ShelfGoodsAmount_or_GoodQuantityInOneContainer = tk.Entry(MainWindow, width=34, bd=5,
                                                                        font=("Arial Bold", 20),
                                                                        textvariable=Var_Edit_GoodContainersAmount_or_GoodQuantityInOneContainer)

Lbl_Enter_Shelf_LengthInSM = tk.Label(MainWindow, text='Длина полки в см:',
                                      font=("Arial Bold", 24), bg="#20B2AA")

Lbl_Enter_Good_Cost = tk.Label(MainWindow, text='Стоимость товара:',
                               font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_ShelfLengthInSM_or_GoodCost = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                                     textvariable=Var_Edit_GoodShelfLengthInSM_or_GoodCost)

Lbl_Enter_Shelf_Description = tk.Label(MainWindow, text='Описание устройства отслеживания полки:',
                                       font=("Arial Bold", 13), bg="#20B2AA")

Lbl_Enter_Good_Description = tk.Label(MainWindow, text='Описание товара:',
                                      font=("Arial Bold", 28), bg="#20B2AA")

Lbl_Enter_Description_Additional = tk.Label(MainWindow, text='(не обязательно)',
                                            font=("Arial Bold", 13), bg="#20B2AA")

Text_Enter_Shelf_or_Good_Description = tk.Text(MainWindow, height=3, width=34, bd=5, font=("Times New Roman", 20))

Btn_Cancel = tk.Button(MainWindow, text="Отмена", font=("Arial Bold", 24), bd=5,
                       background="#008B8B", command=Finish_Any_Operation, width=15)

Btn_Add_Data_Commit = tk.Button(MainWindow, text="Подтвердить добавление", font=("Arial Bold", 28), bd=10,
                                background="#008B8B", command=Add_Data_Confirm, width=22)

Btn_Edit_Data_Commit = tk.Button(MainWindow, text="Подтвердить изменение", font=("Arial Bold", 28), bd=10,
                                 background="#008B8B", command=Edit_Data_Confirm, width=22)

Btn_Delete_Data_Commit = tk.Button(MainWindow, text="Подтвердить удаление", font=("Arial Bold", 28), bd=10,
                                   background="#008B8B", command=Delete_Data_Confirm, width=22)

Btn_Add_Data = tk.Button(MainWindow, text="Добавить запись", font=("Arial Bold", 28), bd=10,
                         background="#008B8B", command=Add_Data, width=20, state="disabled")
Btn_Add_Data.place(relx=0.83, rely=0.46, anchor="c")

Btn_Edit_Data = tk.Button(MainWindow, text="Редактировать запись", font=("Arial Bold", 28), bd=10,
                          background="#008B8B", command=Edit_Data, width=20, state="disabled")
Btn_Edit_Data.place(relx=0.83, rely=0.58, anchor="c")

Btn_Delete_Data = tk.Button(MainWindow, text="Удалить запись", font=("Arial Bold", 28), bd=10,
                            background="#008B8B", command=Delete_Data, width=20, state="disabled")
Btn_Delete_Data.place(relx=0.83, rely=0.7, anchor="c")

Lbl_Dir_Shelfs = tk.Label(MainWindow, text='Справочник "полки"',
                          font=("Arial Bold", 28), bg="#20B2AA")

Lbl_Dir_Goods = tk.Label(MainWindow, text='Справочник "товар"',
                         font=("Arial Bold", 28), bg="#20B2AA")

Table_Shelfs_output = ttk.Treeview(MainWindow, height=34, show="headings", selectmode="browse")
Table_Shelfs_output["columns"] = shelfs_headings
Table_Shelfs_output["displaycolumns"] = shelfs_headings
Table_Shelfs_output.heading(shelfs_headings[0], text=shelfs_headings[0], anchor=tk.CENTER)
Table_Shelfs_output.column(shelfs_headings[0], width=115, anchor=tk.CENTER)
Table_Shelfs_output.heading(shelfs_headings[1], text=shelfs_headings[1], anchor=tk.CENTER)
Table_Shelfs_output.column(shelfs_headings[1], width=115, anchor=tk.CENTER)
Table_Shelfs_output.heading(shelfs_headings[2], text=shelfs_headings[2], anchor=tk.CENTER)
Table_Shelfs_output.column(shelfs_headings[2], width=175, anchor=tk.CENTER)
Table_Shelfs_output.heading(shelfs_headings[3], text=shelfs_headings[3], anchor=tk.CENTER)
Table_Shelfs_output.column(shelfs_headings[3], width=255, anchor=tk.CENTER)
Table_Shelfs_output.heading(shelfs_headings[4], text=shelfs_headings[4], anchor=tk.CENTER)
Table_Shelfs_output.column(shelfs_headings[4], width=120, anchor=tk.CENTER)
Table_Shelfs_output.heading(shelfs_headings[5], text=shelfs_headings[5], anchor=tk.CENTER)
Table_Shelfs_output.column(shelfs_headings[5], width=210, anchor=tk.CENTER)
Table_Shelfs_output.column('#' + str(1), minwidth=180, stretch=False)
Table_Shelfs_output.column('#' + str(2), minwidth=200, stretch=False)
Table_Shelfs_output.column('#' + str(3), minwidth=85, stretch=False)
Table_Shelfs_output.column('#' + str(4), minwidth=160, stretch=False)
Table_Shelfs_output.column('#' + str(5), minwidth=135, stretch=False)
Table_Shelfs_output.column('#' + str(6), minwidth=230, stretch=False)

Table_Goods_output = ttk.Treeview(MainWindow, height=34, show="headings", selectmode="browse")
Table_Goods_output["columns"] = goods_headings
Table_Goods_output["displaycolumns"] = goods_headings
Table_Goods_output.heading(goods_headings[0], text=goods_headings[0], anchor=tk.CENTER)
Table_Goods_output.column(goods_headings[0], width=100, anchor=tk.CENTER)
Table_Goods_output.heading(goods_headings[1], text=goods_headings[1], anchor=tk.CENTER)
Table_Goods_output.column(goods_headings[1], width=120, anchor=tk.CENTER)
Table_Goods_output.heading(goods_headings[2], text=goods_headings[2], anchor=tk.CENTER)
Table_Goods_output.column(goods_headings[2], width=100, anchor=tk.CENTER)
Table_Goods_output.heading(goods_headings[3], text=goods_headings[3], anchor=tk.CENTER)
Table_Goods_output.column(goods_headings[3], width=300, anchor=tk.CENTER)
Table_Goods_output.heading(goods_headings[4], text=goods_headings[4], anchor=tk.CENTER)
Table_Goods_output.column(goods_headings[4], width=120, anchor=tk.CENTER)
Table_Goods_output.heading(goods_headings[5], text=goods_headings[5], anchor=tk.CENTER)
Table_Goods_output.column(goods_headings[5], width=250, anchor=tk.CENTER)
Table_Goods_output.column('#' + str(1), minwidth=100, stretch=False)
Table_Goods_output.column('#' + str(2), minwidth=120, stretch=False)
Table_Goods_output.column('#' + str(3), minwidth=100, stretch=False)
Table_Goods_output.column('#' + str(4), minwidth=300, stretch=False)
Table_Goods_output.column('#' + str(5), minwidth=120, stretch=False)
Table_Goods_output.column('#' + str(6), minwidth=250, stretch=False)

Table_Shelfs_output_scroll_vertical = tk.Scrollbar(MainWindow, command=Table_Shelfs_output.yview)
Table_Shelfs_output.configure(yscrollcommand=Table_Shelfs_output_scroll_vertical.set)

Table_Goods_output_scroll_vertical = tk.Scrollbar(MainWindow, command=Table_Goods_output.yview)
Table_Goods_output.configure(yscrollcommand=Table_Goods_output_scroll_vertical.set)

Description_scroll_vertical = tk.Scrollbar(MainWindow, command=Text_Enter_Shelf_or_Good_Description.yview)
Text_Enter_Shelf_or_Good_Description.configure(yscrollcommand=Description_scroll_vertical.set)

Table_Shelfs_output_scroll_horizontal = tk.Scrollbar(MainWindow, command=Table_Shelfs_output.xview, orient='horizontal')
Table_Shelfs_output.configure(xscrollcommand=Table_Shelfs_output_scroll_horizontal.set)

Table_Goods_output_scroll_horizontal = tk.Scrollbar(MainWindow, command=Table_Goods_output.xview, orient='horizontal')
Table_Goods_output.configure(xscrollcommand=Table_Goods_output_scroll_horizontal.set)

Description_scroll_horizontal = tk.Scrollbar(MainWindow, command=Text_Enter_Shelf_or_Good_Description.xview,
                                             orient='horizontal')
Text_Enter_Shelf_or_Good_Description.configure(xscrollcommand=Description_scroll_horizontal.set)

Btn_Exit = tk.Button(MainWindow, text="Выход", font=("Arial Bold", 28), bd=10,
                     background="#008B8B", command=MainWindow.quit, width=20)
Btn_Exit.place(relx=0.83, rely=0.925, anchor="c")

MainWindow.mainloop()
