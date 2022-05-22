import tkinter as tk
import tkinter.ttk as ttk
from datetime import date
from tkinter import messagebox
import pymysql
from tkcalendar import DateEntry

from main import get_sensor_data

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
DevsList = []

operation_state = "none"


def UpdateShelfsList():
    global ShelfsList
    ShelfsList = []
    cur.execute("SELECT * FROM shelfs")
    query_result = cur.fetchall()
    for pr in query_result:
        ShelfsList.append(pr[1])
    ShelfsList.sort()


def UpdateGoodsList():
    global DevsList
    DevsList = []
    cur.execute("SELECT * FROM goods")
    query_result = cur.fetchall()
    for dev in query_result:
        DevsList.append(dev[1])
    DevsList.sort()


UpdateShelfsList()
UpdateGoodsList()

Var_OutputMenu = tk.StringVar(MainWindow)
Var_OutputMenu.set("Выбрать справочник")

Var_Edit_ProjectName_or_DevName = tk.StringVar(MainWindow)
Var_OutputMenu_Shelfs_or_Devs = tk.StringVar(MainWindow)
Var_Edit_Chosen_ProjectCreationDate_or_ShelfLife = tk.StringVar(MainWindow)
Var_Edit_GoodQuantity = tk.StringVar(MainWindow)
Var_Edit_ProjectCreationDate_or_ShelfLife = tk.StringVar(MainWindow)
Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer = tk.StringVar(MainWindow)
Var_Edit_ProjectInvests_or_GoodCost = tk.StringVar(MainWindow)

Var_Edit_LeaderFIO = tk.StringVar(MainWindow)
Var_OutputMenu_Devs = tk.StringVar(MainWindow)


def CheckProjectName(str):
    if str == "":
        messagebox.showerror("Ошибка ввода названия полки", "Название полки не может быть пустым!")
    else:
        if "Выбрать полку для" in str:
            messagebox.showerror("Ошибка ввода имени полки", "Полку не может быть с таким дурацким именем!")
            return False
        cur.execute('SELECT EXISTS(SELECT * FROM shelfs WHERE shelfName = %s)', str)
        exist_or_not = cur.fetchall()[0][0]
        if exist_or_not == 1:
            messagebox.showerror("Ошибка ввода имени полки", "Полку с таким именем уже есть в базе данных!")
            return False
        return True
    return False


def CheckIfProjectChosen(str):
    if "Выбрать полку для" in str:
        messagebox.showerror("Ошибка выбора полки", "Вы не выбрали Полку!")
    else:
        return True
    return False


def CheckLeaderFIOName(str):
    if str == "Выбрать товар для полки":
        messagebox.showerror("Ошибка ввода Название товара полки", "Вы не выбрали Название товара полки!")
    else:
        return True
    return False

def CheckGoodQuantity(str):
    if str == "":
        messagebox.showerror("Ошибка ввода количества товара", "Вы не выбрали количество товара!")
    else:
        return True
    return False


def CheckProjectCrDate(str):
    if str == "":
        messagebox.showerror("Ошибка выбора даты создания полки", "Вы не выбрали дату создания полки!")
    else:
        return True
    return False


def CheckDevsAmount(str):
    try:
        devs_num = int(str)
        if devs_num < 1:
            messagebox.showerror("Ошибка ввода числа товаров",
                                 "Вы ввели не положительное Количество контейнеров объёмом 100см^3!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода числа товаров", "Вы ввели не целое Количество контейнеров объёмом 100см^3!")
        return False


def CheckInvests(str):
    try:
        invests = float(str)
        if invests < 0.0:
            messagebox.showerror("Ошибка ввода инвестиций", "Вы ввели отрицательное значение инвестиций!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода инвестиций", "В поле для инвестиций вы ввели не число!")
        return False


def CheckDevName(str):
    if str == "":
        messagebox.showerror("Ошибка ввода Название товара", "Название товара не может быть пустым!")
    else:
        if str.count(' ') != 1 and str.count(' ') != 2:
            messagebox.showerror("Ошибка ввода Название товара",
                                 "Название товара должно состоять из двух или трёх слов!")
        else:
            str_without_spaces = str.replace(' ', '')
            if str_without_spaces.isalpha():
                words = str.split(' ')
                for word in words:
                    if not word[0].isupper():
                        messagebox.showerror("Ошибка ввода Название товара",
                                             "Каждое из двух или трёх слов Название товара должно начинаться с большой буквы!")
                        return False
                cur.execute('SELECT EXISTS(SELECT * FROM goods WHERE goodNAME = %s)', str)
                exist_or_not = cur.fetchall()[0][0]
                if exist_or_not == 1:
                    messagebox.showerror("Ошибка ввода имени товара",
                                         "товар с таким ФИО уже есть в базе данных!")
                    return False
                return True
            else:
                messagebox.showerror("Ошибка ввода Название товара",
                                     "В Название товара могут быть использованы только буквы!")
    return False


def CheckIfDevChosen(str):
    if "Выбрать товара для" in str:
        messagebox.showerror("Ошибка выбора товара", "Вы не выбрали товара!")
    else:
        return True
    return False


def CheckShelfLife(str):
    if str == "":
        messagebox.showerror("Ошибка выбора даты рождения", "Вы не выбрали дату рождения товара!")
    else:
        return True
    return False


def CheckGoodQuantityInOneContainer(str):
    try:
        tasks_num = int(str)
        if tasks_num < 1:
            messagebox.showerror("Ошибка ввода числа Количество товара в одном контейнере объёмом 100см^3 товара",
                                 "Вы ввели не положительное число Количество товара в одном контейнере объёмом 100см^3!")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода числа Количество товара в одном контейнере объёмом 100см^3 товара",
                             "Вы ввели не целое число Количество товара в одном контейнере объёмом 100см^3!")
        return False


def CheckGoodCost(str):
    try:
        rating = float(str)
        if rating < 0.0:
            messagebox.showerror("Ошибка ввода Стоимость товараа",
                                 "Вы ввели отрицательное значение Стоимость товараа товара!")
            return False
        if rating > 10.0:
            messagebox.showerror("Ошибка ввода Стоимость товараа",
                                 "Вы ввели значение Стоимость товараа, превышающее максимальное! (> 10.0)")
            return False
        return True
    except ValueError:
        messagebox.showerror("Ошибка ввода Стоимость товараа", "В поле для Стоимость товараа товара вы ввели не число!")
        return False


def Select_Data():
    sensor_data = get_sensor_data()
    if sensor_data < 20.2:
        cur.execute(
            'UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s',
            (date.today(), 3, 1))
    elif (sensor_data > 20.2) and (sensor_data < 120.2):
        cur.execute(
            'UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s',
            (date.today(), 2, 1))
    elif (sensor_data > 120.2) and (sensor_data < 220.2):
        cur.execute(
            'UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s',
            (date.today(), 1, 1))
    elif sensor_data > 220.2:
        cur.execute(
            'UPDATE shelfs SET goodLastChangedDate = %s, goodContainersAmount = %s WHERE shelfID = %s',
            (date.today(), 0, 1))

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
        Lbl_Enter_Project_Name.place(relx=0.188, rely=0.27, anchor="c")
        Lbl_Enter_Project_LeaderFIO.place(relx=0.17, rely=0.37, anchor="c")
        Lbl_Enter_Project_CreationDate.place(relx=0.16, rely=0.47, anchor="c")
        Lbl_Enter_Project_DevsAmount.place(relx=0.168, rely=0.57, anchor="c")
        Lbl_Enter_Project_Investments.place(relx=0.175, rely=0.67, anchor="c")
        Lbl_Enter_Project_Description.place(relx=0.187, rely=0.77, anchor="c")
        TxtEdit_Enter_ProjectCreationDate_or_ShelfLife.place(relx=0.353, rely=0.47, anchor="c")
        TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer.place(relx=0.47, rely=0.57, anchor="c")
        TxtEdit_Enter_ProjectInvestments_or_GoodCost.place(relx=0.47, rely=0.67, anchor="c")
        Text_Enter_Project_or_Dev_Description.place(relx=0.481, rely=0.79, anchor="c")
        Description_scroll_vertical.place(relx=0.305, rely=0.73, height=107, width=25)
        Description_scroll_horizontal.place(relx=0.32, rely=0.85, height=25, width=493)
        Lbl_Enter_Description_Additional.place(relx=0.19, rely=0.82, anchor="c")
    elif Var_OutputMenu.get() == "товар":
        Table_Goods_output.place_forget()
        Table_Goods_output_scroll_vertical.place_forget()
        Table_Goods_output_scroll_horizontal.place_forget()
        Lbl_Enter_Dev_Name.place(relx=0.184, rely=0.3, anchor="c")
        Lbl_Enter_Dev_BirthDate.place(relx=0.184, rely=0.38, anchor="c")
        Lbl_Enter_PrCount.place(relx=0.16, rely=0.46, anchor="c")
        Lbl_Enter_Dev_SolvedPrCount.place(relx=0.159, rely=0.54, anchor="c")
        Lbl_Enter_Dev_Rating.place(relx=0.246, rely=0.66, anchor="c")
        Lbl_Enter_Dev_Description.place(relx=0.158, rely=0.77, anchor="c")
        Lbl_Enter_Description_Additional.place(relx=0.16, rely=0.82, anchor="c")
        TxtEdit_Enter_ProjectCreationDate_or_ShelfLife.place(relx=0.353, rely=0.38, anchor="c")
        TxtEdit_Enter_Good_quantity.place(relx=0.469, rely=0.46, anchor="c")
        TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer.place(relx=0.47, rely=0.54, anchor="c")
        TxtEdit_Enter_ProjectInvestments_or_GoodCost.place(relx=0.47, rely=0.66, anchor="c")
        Text_Enter_Project_or_Dev_Description.place(relx=0.481, rely=0.78, anchor="c")
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
    Update_option_menu(OutputMenu_Choose_Dev, DevsList, Var_OutputMenu_Devs)
    OutputMenu_ChooseDir["state"] = "normal"
    Btn_Select_Data["state"] = "normal"
    Btn_Add_Data["state"] = "normal"
    Btn_Edit_Data["state"] = "normal"
    Btn_Delete_Data["state"] = "normal"
    Btn_Cancel.place_forget()
    Lbl_Add_Data.place_forget()
    Lbl_Edit_Data.place_forget()
    Lbl_Delete_Data.place_forget()
    TxtEdit_Enter_ProjectName_or_DevName.place_forget()
    Var_Edit_ProjectName_or_DevName.set("")
    OutputMenu_Choose_Dev.place_forget()
    OutputMenu_Choose_Project_or_Dev.place_forget()
    TxtEdit_Enter_ProjectCreationDate_or_ShelfLife.place_forget()
    Var_Edit_GoodQuantity.set("")
    Var_Edit_ProjectCreationDate_or_ShelfLife.set("")
    Btn_Choose_Date.place_forget()
    TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer.place_forget()
    Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.set("")
    TxtEdit_Enter_ProjectInvestments_or_GoodCost.place_forget()
    Var_Edit_ProjectInvests_or_GoodCost.set("")
    Description_scroll_vertical.place_forget()
    Description_scroll_horizontal.place_forget()
    Btn_Add_Data_Commit.place_forget()
    Btn_Edit_Data_Commit.place_forget()
    Btn_Delete_Data_Commit.place_forget()
    TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer["state"] = "normal"
    TxtEdit_Enter_ProjectInvestments_or_GoodCost["state"] = "normal"
    Text_Enter_Project_or_Dev_Description["state"] = "normal"
    Text_Enter_Project_or_Dev_Description.place_forget()
    Text_Enter_Project_or_Dev_Description.delete(1.0, tk.END)
    Lbl_Enter_Description_Additional.place_forget()
    if Var_OutputMenu.get() == "полки":
        Update_option_menu(OutputMenu_Choose_Project_or_Dev, ShelfsList, Var_OutputMenu_Shelfs_or_Devs)
        Lbl_Enter_Project_Name.place_forget()
        Lbl_Enter_Project_LeaderFIO.place_forget()
        Lbl_Enter_Project_CreationDate.place_forget()
        Lbl_Enter_Project_DevsAmount.place_forget()
        Lbl_Enter_Project_Investments.place_forget()
        Lbl_Enter_Project_Description.place_forget()
        TxtEdit_LeaderFIO.place_forget()
        Var_Edit_LeaderFIO.set("")
        TxtEdit_LeaderFIO["state"] = "normal"
        for row in Table_Shelfs_output.get_children():
            Table_Shelfs_output.delete(row)
        Table_Shelfs_output_scroll_vertical.place(relx=0.003, rely=0.14, height=706, width=25)
        Table_Shelfs_output_scroll_horizontal.place(relx=0.02, rely=0.96, height=25, width=993)
        Table_Shelfs_output.place(relx=0.02, rely=0.14)
    elif Var_OutputMenu.get() == "товар":
        Update_option_menu(OutputMenu_Choose_Project_or_Dev, DevsList, Var_OutputMenu_Shelfs_or_Devs)
        Lbl_Enter_Dev_Name.place_forget()
        Lbl_Enter_Dev_BirthDate.place_forget()
        Lbl_Enter_PrCount.place_forget()
        Lbl_Enter_Dev_SolvedPrCount.place_forget()
        Lbl_Enter_Dev_Rating.place_forget()
        Lbl_Enter_Dev_Description.place_forget()
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
    date_data_list = Var_Edit_Chosen_ProjectCreationDate_or_ShelfLife.get().split("/")
    if len(date_data_list[1]) == 1:
        date_data_list[1] = '0' + date_data_list[1]
    if len(date_data_list[0]) == 1:
        date_data_list[0] = '0' + date_data_list[0]
    Var_Edit_ProjectCreationDate_or_ShelfLife.set(
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
                    textvariable=Var_Edit_Chosen_ProjectCreationDate_or_ShelfLife)
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
        Var_OutputMenu_Devs.set("Выбрать товар для полки")
        OutputMenu_Choose_Dev.place(relx=0.47, rely=0.37, anchor="c")
        TxtEdit_Enter_ProjectName_or_DevName.place(relx=0.47, rely=0.27, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.47, anchor="c")
    elif Var_OutputMenu.get() == "товар":
        TxtEdit_Enter_ProjectName_or_DevName.place(relx=0.47, rely=0.3, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.38, anchor="c")


def Add_Data_Confirm():
    if Var_OutputMenu.get() == "полки":
        shelfName = Var_Edit_ProjectName_or_DevName.get()
        prLeaderFIO = Var_OutputMenu_Devs.get()
        prGoodQuantity = Var_Edit_GoodQuantity.get()
        prCrDate = Var_Edit_ProjectCreationDate_or_ShelfLife.get()
        prDevAmount = Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.get()
        goodShelfLengthInSM = Var_Edit_ProjectInvests_or_GoodCost.get()
        shelfDescription = Text_Enter_Project_or_Dev_Description.get(1.0, tk.END)
        if CheckProjectName(shelfName):
            if CheckLeaderFIOName(prLeaderFIO):
                if CheckGoodQuantity(prGoodQuantity):
                    if CheckProjectCrDate(prCrDate):
                        if CheckDevsAmount(prDevAmount):
                            if CheckInvests(goodShelfLengthInSM):
                                try:
                                    cur.execute("SELECT goodID FROM goods WHERE goodNAME = %s", prLeaderFIO)
                                    goodID = cur.fetchall()[0][0]
                                    prCrDateList = prCrDate.split('.')
                                    day = prCrDateList[0]
                                    month = prCrDateList[1]
                                    year = prCrDateList[2]
                                    prCrDate = year + '-' + month + '-' + day
                                    if shelfDescription == "\n":
                                        shelfDescription = "No additional information"
                                    cur.execute(
                                        'INSERT INTO shelfs (shelfName, goodHereID, goodLastChangedDate, goodContainersAmount, goodShelfLengthInSM, shelfDescript, goodOldHereName)'
                                        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                        (shelfName, goodID, prCrDate, prDevAmount, goodShelfLengthInSM, shelfDescription,
                                         prLeaderFIO))
                                    messagebox.showinfo("Успешное добавление записи в базу данных",
                                                        "Добавление записи о Полке в базу данных проведено успешно!")
                                    DB.commit()
                                    Finish_Any_Operation()
                                except:
                                    DB.rollback()
                                    messagebox.showerror("Ошибка при добавлении данных в базу",
                                                         "По неизвестной причине не удалось добавить данные в БД!")
    elif Var_OutputMenu.get() == "товар":
        devName = Var_Edit_ProjectName_or_DevName.get()
        goodQuantity = Var_Edit_GoodQuantity.get()
        shelfLife = Var_Edit_ProjectCreationDate_or_ShelfLife.get()
        goodQuantityInOneContainer = Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.get()
        goodCost = Var_Edit_ProjectInvests_or_GoodCost.get()
        goodDescription = Text_Enter_Project_or_Dev_Description.get(1.0, tk.END)
        if CheckDevName(devName):
            if CheckShelfLife(shelfLife):
                if CheckGoodQuantityInOneContainer(goodQuantityInOneContainer):
                    if CheckGoodCost(goodCost):
                        try:
                            shelfLifeList = shelfLife.split('.')
                            day = shelfLifeList[0]
                            month = shelfLifeList[1]
                            year = shelfLifeList[2]
                            shelfLife = year + '-' + month + '-' + day
                            if goodDescription == "\n":
                                goodDescription = "No additional information"
                            cur.execute(
                                'INSERT INTO goods (goodNAME, goodQuantity, shelfLife, goodQuantityInOneContainer, goodCost, goodDescript)'
                                'VALUES (%s, %s, %s, %s, %s, %s)',
                                (devName, shelfLife, goodQuantityInOneContainer, goodCost, goodDescription))
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
        Var_OutputMenu_Shelfs_or_Devs.set("Выбрать полку для изменений")
        Var_OutputMenu_Devs.set("Выбрать товар для полки")
        OutputMenu_Choose_Project_or_Dev.place(relx=0.47, rely=0.27, anchor="c")
        OutputMenu_Choose_Dev.place(relx=0.47, rely=0.37, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.47, anchor="c")
    elif Var_OutputMenu.get() == "товар":
        Var_OutputMenu_Shelfs_or_Devs.set("Выбрать товара для изменений")
        OutputMenu_Choose_Project_or_Dev.place(relx=0.47, rely=0.3, anchor="c")
        Btn_Choose_Date.place(relx=0.525, rely=0.38, anchor="c")


def Edit_Data_Confirm():
    if Var_OutputMenu.get() == "полки":
        shelfName = Var_OutputMenu_Shelfs_or_Devs.get()
        prLeaderFIO = Var_OutputMenu_Devs.get()
        prGoodQuantity = Var_Edit_GoodQuantity.get()
        prCrDate = Var_Edit_ProjectCreationDate_or_ShelfLife.get()
        prDevAmount = Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.get()
        goodShelfLengthInSM = Var_Edit_ProjectInvests_or_GoodCost.get()
        shelfDescription = Text_Enter_Project_or_Dev_Description.get(1.0, tk.END)
        if CheckIfProjectChosen(shelfName):
            if CheckLeaderFIOName(prLeaderFIO):
                if CheckProjectCrDate(prCrDate):
                    if CheckDevsAmount(prDevAmount):
                        if CheckInvests(goodShelfLengthInSM):
                            try:
                                cur.execute("SELECT shelfID FROM shelfs WHERE shelfName = %s", shelfName)
                                shelfID = cur.fetchall()[0][0]
                                cur.execute("SELECT goodID FROM goods WHERE goodNAME = %s", prLeaderFIO)
                                goodID = cur.fetchall()[0][0]
                                prCrDateList = prCrDate.split('.')
                                day = prCrDateList[0]
                                month = prCrDateList[1]
                                year = prCrDateList[2]
                                prCrDate = year + '-' + month + '-' + day
                                if shelfDescription == "\n":
                                    shelfDescription = "No additional information"
                                cur.execute(
                                    'UPDATE shelfs SET shelfName = %s, goodHereID = %s, goodLastChangedDate = %s, goodContainersAmount = %s,'
                                    'goodShelfLengthInSM = %s, shelfDescript = %s, goodOldHereName = %s WHERE shelfID = %s',
                                    (shelfName, goodID, prCrDate, prDevAmount, goodShelfLengthInSM, shelfDescription,
                                     prLeaderFIO, shelfID))
                                messagebox.showinfo("Успешное редактирование записи в базе данных",
                                                    "Редактирование записи о Полке в базе данных проведено успешно!")
                                DB.commit()
                                Finish_Any_Operation()
                            except:
                                DB.rollback()
                                messagebox.showerror("Ошибка при редактировании данных в базу",
                                                     "По неизвестной причине не удалось редактировать данные в БД!")
    elif Var_OutputMenu.get() == "товар":
        devName = Var_OutputMenu_Shelfs_or_Devs.get()
        goodQuantity = Var_Edit_GoodQuantity.get()
        shelfLife = Var_Edit_ProjectCreationDate_or_ShelfLife.get()
        goodQuantityInOneContainer = Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.get()
        goodCost = Var_Edit_ProjectInvests_or_GoodCost.get()
        goodDescription = Text_Enter_Project_or_Dev_Description.get(1.0, tk.END)
        if CheckIfDevChosen(devName):
            if CheckShelfLife(shelfLife):
                if CheckGoodQuantityInOneContainer(goodQuantityInOneContainer):
                    if CheckGoodCost(goodCost):
                        try:
                            cur.execute("SELECT goodID FROM goods WHERE goodNAME = %s", devName)
                            goodID = cur.fetchall()[0][0]
                            shelfLifeList = shelfLife.split('.')
                            day = shelfLifeList[0]
                            month = shelfLifeList[1]
                            year = shelfLifeList[2]
                            shelfLife = year + '-' + month + '-' + day
                            if goodDescription == "\n":
                                goodDescription = "No additional information"
                            cur.execute(
                                'UPDATE goods SET goodNAME = %s, shelfLife = %s, goodQuantityInOneContainer = %s,'
                                'goodCost = %s, goodDescript = %s WHERE goodID = %s',
                                (devName, shelfLife, int(goodQuantityInOneContainer), float(goodCost), goodDescription,
                                 goodID))
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
        Var_OutputMenu_Shelfs_or_Devs.set("Выбрать полку для удаления")
        OutputMenu_Choose_Project_or_Dev.place(relx=0.47, rely=0.27, anchor="c")
        TxtEdit_LeaderFIO.place(relx=0.47, rely=0.37, anchor="c")
        TxtEdit_LeaderFIO["state"] = "readonly"
        TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer["state"] = "readonly"
        TxtEdit_Enter_ProjectInvestments_or_GoodCost["state"] = "readonly"
        Text_Enter_Project_or_Dev_Description["state"] = "disable"
    elif Var_OutputMenu.get() == "товар":
        Var_OutputMenu_Shelfs_or_Devs.set("Выбрать товара для удаления")
        OutputMenu_Choose_Project_or_Dev.place(relx=0.47, rely=0.3, anchor="c")
        TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer["state"] = "readonly"
        TxtEdit_Enter_ProjectInvestments_or_GoodCost["state"] = "readonly"
        Text_Enter_Project_or_Dev_Description["state"] = "disable"


def Delete_Data_Confirm():
    if Var_OutputMenu.get() == "полки":
        shelfName = Var_OutputMenu_Shelfs_or_Devs.get()
        if CheckIfProjectChosen(shelfName):
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
        devName = Var_OutputMenu_Shelfs_or_Devs.get()
        if CheckIfDevChosen(devName):
            try:
                cur.execute("DELETE FROM goods WHERE goodNAME = %s", devName)
                messagebox.showinfo("Успешное удаление записи из базы данных",
                                    "Удаление записи о товаре из базы данных проведено успешно!")
                DB.commit()
                Finish_Any_Operation()
            except:
                DB.rollback()
                messagebox.showerror("Ошибка при удалении данных из базы",
                                     "По неизвестной причине не удалось удалить данные в БД!")


def Project_or_Dev_For_Delete_Chosen(*args):
    global operation_state
    if operation_state == "delete":
        pr_or_dev_Name = Var_OutputMenu_Shelfs_or_Devs.get()
        if Var_OutputMenu.get() == "полки":
            if "Выбрать полку для" not in pr_or_dev_Name:
                cur.execute("SELECT * FROM shelfs WHERE shelfName = %s", pr_or_dev_Name)
                pr_info = cur.fetchall()
                leader_id = pr_info[0][2]
                cur.execute("SELECT goodNAME FROM goods WHERE goodID = %s", leader_id)
                Var_Edit_LeaderFIO.set(cur.fetchall()[0][0])
                Var_Edit_GoodQuantity.set(str(pr_info[0][3]))
                Var_Edit_ProjectCreationDate_or_ShelfLife.set(str(pr_info[0][4]))
                Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.set(str(pr_info[0][5]))
                Var_Edit_ProjectInvests_or_GoodCost.set(pr_info[0][6])
                Text_Enter_Project_or_Dev_Description["state"] = "normal"
                Text_Enter_Project_or_Dev_Description.delete(1.0, tk.END)
                Text_Enter_Project_or_Dev_Description.insert(tk.END, pr_info[0][7])
                Text_Enter_Project_or_Dev_Description["state"] = "disable"
        elif Var_OutputMenu.get() == "товар":
            if "Выбрать товара для" not in pr_or_dev_Name:
                cur.execute("SELECT * FROM goods WHERE goodNAME = %s", pr_or_dev_Name)
                pr_or_dev_info = cur.fetchall()
                Var_Edit_GoodQuantity.set(str(pr_or_dev_info[0][2]))
                Var_Edit_ProjectCreationDate_or_ShelfLife.set(str(pr_or_dev_info[0][3]))
                Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer.set(str(pr_or_dev_info[0][4]))
                Var_Edit_ProjectInvests_or_GoodCost.set(pr_or_dev_info[0][5])
                Text_Enter_Project_or_Dev_Description["state"] = "normal"
                Text_Enter_Project_or_Dev_Description.delete(1.0, tk.END)
                Text_Enter_Project_or_Dev_Description.insert(tk.END, pr_or_dev_info[0][6])
                Text_Enter_Project_or_Dev_Description["state"] = "disable"


Var_OutputMenu_Shelfs_or_Devs.trace("w", Project_or_Dev_For_Delete_Chosen)

Lbl_FIO = tk.Label(MainWindow, text="Система учёта товаров на складе",
                   font=("Arial Bold", 28), bg="#20B2AA")
Lbl_FIO.place(relx=0.215, rely=0.025, anchor="c")

Lbl_Start = tk.Label(MainWindow, text='Программа для ручного учёта товаров на складе\n\n'
                                      'База данных автоматически изменяется со временем\n\n'
                                      'Язык программирования: Python\n\n'
                                      'Технологии: Tkinter, pymysql\n\n'
                                      'Среда разработки: PyCharm\n\n',
                     font=("Times New Roman", 32), bg="#20B2AA")
Lbl_Start.place(relx=0.33, rely=0.5, anchor="c")


def Dir_Chosen(*args):
    Lbl_Start.place_forget()
    if Var_OutputMenu.get() == "полки":
        UpdateShelfsList()
        Update_option_menu(OutputMenu_Choose_Project_or_Dev, ShelfsList, Var_OutputMenu_Shelfs_or_Devs)
        OutputMenu_Choose_Project_or_Dev.config(font=("Times New Roman", 24), width=29)
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
        Update_option_menu(OutputMenu_Choose_Project_or_Dev, DevsList, Var_OutputMenu_Shelfs_or_Devs)
        OutputMenu_Choose_Project_or_Dev.config(font=("Times New Roman", 18), width=39)
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

Btn_Select_Data = tk.Button(MainWindow, text="Вывести все записи", font=("Arial Bold", 28), bd=10,
                            background="#008B8B", command=Select_Data, width=20, state="disabled")
Btn_Select_Data.place(relx=0.83, rely=0.34, anchor="c")

Lbl_Add_Data = tk.Label(MainWindow, text='Добавление записи',
                        font=("Arial Bold", 36), bg="#20B2AA")

Lbl_Edit_Data = tk.Label(MainWindow, text='Редактирование записи',
                         font=("Arial Bold", 36), bg="#20B2AA")

Lbl_Delete_Data = tk.Label(MainWindow, text='Удаление записи',
                           font=("Arial Bold", 36), bg="#20B2AA")

Lbl_Enter_Project_Name = tk.Label(MainWindow, text='Название полки:',
                                  font=("Arial Bold", 28), bg="#20B2AA")

Lbl_Enter_Dev_Name = tk.Label(MainWindow, text='Название товара:',
                              font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_ProjectName_or_DevName = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                                textvariable=Var_Edit_ProjectName_or_DevName)

OutputMenu_Choose_Project_or_Dev = tk.OptionMenu(MainWindow, Var_OutputMenu_Shelfs_or_Devs, *ShelfsList)
OutputMenu_Choose_Project_or_Dev.config(font=("Times New Roman", 24), bg="#008B8B", bd=5, width=29)

Lbl_Enter_Project_LeaderFIO = tk.Label(MainWindow, text='Название товара для полки:',
                                       font=("Arial Bold", 23), bg="#20B2AA")

TxtEdit_LeaderFIO = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                             textvariable=Var_Edit_LeaderFIO)

OutputMenu_Choose_Dev = tk.OptionMenu(MainWindow, Var_OutputMenu_Devs, *DevsList)
OutputMenu_Choose_Dev.config(font=("Times New Roman", 24), bg="#008B8B", bd=5, width=29)

Lbl_Enter_Project_CreationDate = tk.Label(MainWindow, text='Дата последнего изменения на полке:',
                                          font=("Arial Bold", 18), bg="#20B2AA")

Lbl_Enter_Dev_BirthDate = tk.Label(MainWindow, text='Срок годности:',
                                   font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_ProjectCreationDate_or_ShelfLife = tk.Entry(MainWindow, width=10, bd=5, font=("Arial Bold", 20),
                                                          textvariable=Var_Edit_ProjectCreationDate_or_ShelfLife,
                                                          state="readonly")

Btn_Choose_Date = tk.Button(MainWindow, text="Выбрать дату", font=("Arial Bold", 22), bd=10,
                            background="#008B8B", command=Choose_Date, width=18)

Lbl_Enter_Project_DevsAmount = tk.Label(MainWindow, text='Количество контейнеров объёмом 100см^3:',
                                        font=("Arial Bold", 15), bg="#20B2AA")

Lbl_Enter_PrCount = tk.Label(MainWindow, text='Количество товара:',
                             font=("Arial Bold", 28), bg="#20B2AA")

TxtEdit_Enter_Good_quantity = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                       textvariable=Var_Edit_ProjectInvests_or_GoodCost)

Lbl_Enter_Dev_SolvedPrCount = tk.Label(MainWindow, text='Количество товара в одном контейнере(100см^3):',
                                       font=("Arial Bold", 14), bg="#20B2AA")

TxtEdit_Enter_ProjectDevsAmount_or_GoodQuantityInOneContainer = tk.Entry(MainWindow, width=34, bd=5,
                                                                         font=("Arial Bold", 20),
                                                                         textvariable=Var_Edit_ProjectDevsAmount_or_GoodQuantityInOneContainer)

Lbl_Enter_Project_Investments = tk.Label(MainWindow, text='Длина полки в см:',
                                         font=("Arial Bold", 24), bg="#20B2AA")

Lbl_Enter_Dev_Rating = tk.Label(MainWindow, text='Стоимость товара:',
                                font=("Arial Bold", 14), bg="#20B2AA")

TxtEdit_Enter_ProjectInvestments_or_GoodCost = tk.Entry(MainWindow, width=34, bd=5, font=("Arial Bold", 20),
                                                        textvariable=Var_Edit_ProjectInvests_or_GoodCost)

Lbl_Enter_Project_Description = tk.Label(MainWindow, text='Описание устройства отслеживания полки:',
                                         font=("Arial Bold", 13), bg="#20B2AA")

Lbl_Enter_Dev_Description = tk.Label(MainWindow, text='Описание товара:',
                                     font=("Arial Bold", 28), bg="#20B2AA")

Lbl_Enter_Description_Additional = tk.Label(MainWindow, text='(не обязательно)',
                                            font=("Arial Bold", 13), bg="#20B2AA")

Text_Enter_Project_or_Dev_Description = tk.Text(MainWindow, height=3, width=34, bd=5, font=("Times New Roman", 20))

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

Description_scroll_vertical = tk.Scrollbar(MainWindow, command=Text_Enter_Project_or_Dev_Description.yview)
Text_Enter_Project_or_Dev_Description.configure(yscrollcommand=Description_scroll_vertical.set)

Table_Shelfs_output_scroll_horizontal = tk.Scrollbar(MainWindow, command=Table_Shelfs_output.xview, orient='horizontal')
Table_Shelfs_output.configure(xscrollcommand=Table_Shelfs_output_scroll_horizontal.set)

Table_Goods_output_scroll_horizontal = tk.Scrollbar(MainWindow, command=Table_Goods_output.xview, orient='horizontal')
Table_Goods_output.configure(xscrollcommand=Table_Goods_output_scroll_horizontal.set)

Description_scroll_horizontal = tk.Scrollbar(MainWindow, command=Text_Enter_Project_or_Dev_Description.xview,
                                             orient='horizontal')
Text_Enter_Project_or_Dev_Description.configure(xscrollcommand=Description_scroll_horizontal.set)

Btn_Exit = tk.Button(MainWindow, text="Выход", font=("Arial Bold", 28), bd=10,
                     background="#008B8B", command=MainWindow.quit, width=20)
Btn_Exit.place(relx=0.83, rely=0.925, anchor="c")

MainWindow.mainloop()
