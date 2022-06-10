import email
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from SVM import makecsv
import os.path
from my_parser import parse
import pandas as pd
from my_parser import parse
import pathlib
from parsefile import parsefile
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def makecsv(pathlabel=None):
    way = message_entry.get()  # Путь к папке с письмами
    files = os.listdir(way)
    folders = map(lambda name: os.path.join(way, name), files)
    data = list()
    mail_type = 1
    result = []
    for catalog in folders:
        if os.path.isdir(catalog):
            d[mail_type]=catalog
            print(catalog)
            data = parse(catalog, mail_type)
            mail_type = mail_type + 1
            result = result + data

# Создание SVM
    columns = ['Mail type', 'Email text']
    df = pd.DataFrame(result, columns=columns)
    print(df)
    df.to_csv(r'C:\Email_Analisator\data.csv')

    window2 = tkinter.messagebox.showinfo("Оповещение","CSV собран")

def sort(pathlabel=None):
    pathtofile = message_entry2.get()
    if (os.path.exists(pathtofile)):
        if pathlib.Path(pathtofile).suffix == '.eml':
            text = parsefile(pathtofile)
            dataSVM = pd.read_csv('C:\Email_Analisator\cartridge_accounting.csv')
            X = dataSVM['Email text'].values
            y = dataSVM['Mail type'].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123, shuffle=True)
            cv = CountVectorizer()
            X_train = cv.fit_transform(X_train)
            X_test = cv.transform(X_test)
            classifier = SVC(kernel='linear', probability=True)
            classifier.fit(X_train, y_train)
            x_pred = cv.transform([text])
            y_pred = classifier.predict(x_pred)
            prob = classifier.predict_proba(x_pred)

            way = message_entry.get()
            files = os.listdir(way)
            folders = map(lambda name: os.path.join(way, name), files)
            mail_type = 1
            d = {}
            for catalog in folders:
                if os.path.isdir(catalog):
                    d[mail_type] = catalog
                    mail_type = mail_type + 1

            st =''
            st = "Письмо попадет в папку " + d[int(y_pred)] + str(y_pred)  + ", вероятность = " + str(prob)
            window2 = tkinter.messagebox.showinfo('Результат', st)


        else:
            window2 = tkinter.messagebox.showinfo("Ошибка", "Файла не имеет расширения eml")
    else:
        window2 = tkinter.messagebox.showinfo(pathtofile, "Файла не существует")

def browsefunc(pathlabel=None):
    string = filedialog.askdirectory()
    message_entry.delete(0, END)
    message_entry.insert(0, "")
    message_entry.insert(0,string)

def browsefilefunc(pathlabel=None):
    string = filedialog.askopenfilename()
    message_entry2.delete(0, END)
    message_entry2.insert(0, "")
    message_entry2.insert(0,string)

window = Tk()
window.title("Analytic module")
window.geometry('800x600')

browsebutton = Button(window, text="Browse", command=browsefunc, padx="10", pady="5")
browsebutton.place(relx=.1, rely=.1, anchor="c")
message = StringVar()
message2 = StringVar()
message_entry = Entry(textvariable=message)
message_entry.place(relx=.3, rely=.1, anchor="c")
message_entry2 = Entry(textvariable=message2)
message_entry2.place(relx=.3, rely=.2, anchor="c")
message_entry.insert(0,"C:\mail")
csvbutton = Button(window, text="Make csv", command=makecsv, padx="10", pady="5")
csvbutton.place(relx=.5, rely=.1, anchor="c")
filebutton = Button(window, text="Choose email", command=browsefilefunc, padx="10", pady="5")
filebutton.place(relx=.1, rely=.2, anchor="c")
sortbutton = Button(window, text="Predict", command=sort, padx="20", pady="5")
sortbutton.place(relx=.1, rely=.3, anchor="c")


window.mainloop()
