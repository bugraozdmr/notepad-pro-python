#pyqt5 kütüphanesi ile yapılmıştır
#basit not defteri
#
#BUĞRA
#




from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QStackedWidget, QFileDialog
from PyQt5.QtGui import QIcon

import sys
import datetime
import os
import sqlite3



class notepad(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        loadUi(r"C:\Users\bugra\OneDrive\Masaüstü\notepad-pro\main.ui", self)

        #uygulama açıldığında bize saat dilimine göre mesaj yazsın :)

        now = datetime.datetime.now()
        self.label_2.setText("{}".format(datetime.datetime.strftime(now, "%D")))
        if now.hour < 24 and now.hour >= 18:
            self.label.setText("iyi akşamlar Buğra  :)")
        elif now.hour < 18 and now.hour >= 12:
            self.label.setText("iyi öğleden sonraları Buğra  :)")
        elif now.hour < 6 and now.hour >= 0:
            self.label.setText("iyi geceler Buğra  :)")
        else:
            self.label.setText("hayırlı sabahlar Buğra  :)")

        self.baglan()

        self.pushButton.clicked.connect(self.note)
        self.pushButton_2.clicked.connect(self.exit)

        self.cursor.execute("select * from note")
        list = self.cursor.fetchall()
        a = len(list)



        # geri dönüş yapıldığında bize son 3 notu göstermesi için veritabanındna çektik bilgileri
        # list indexi 3 den büyükse sıkıntısız setText()'ler çalışır
        # diğer olasılıklar için azaltarak yazdım
        # mp3 converter'dan aldım kodu sırasıyla değiştirme....
        if a >= 3:
            self.label_6.setText("{}".format(list[a - 1][0]))
            self.textEdit.setText("{}".format(list[a - 1][1]))
            self.label_7.setText("{}".format(list[a - 1][2]))
            self.label_5.setText("{}".format(list[a - 2][0]))
            self.textEdit_2.setText("{}".format(list[a - 2][1]))
            self.label_8.setText("{}".format(list[a - 2][2]))
            self.label_4.setText("{}".format(list[a - 3][0]))
            self.textEdit_3.setText("{}".format(list[a - 3][1]))
            self.label_9.setText("{}".format(list[a - 3][2]))

        elif a == 2:
            self.label_6.setText("{}".format(list[a - 1][0]))
            self.textEdit.setText("{}".format(list[a - 1][1]))
            self.label_7.setText("{}".format(list[a - 1][2]))
            self.label_5.setText("{}".format(list[a - 2][0]))
            self.textEdit_2.setText("{}".format(list[a - 2][1]))
            self.label_8.setText("{}".format(list[a - 2][2]))
        elif a == 1:
            self.label_6.setText("{}".format(list[a - 1][0]))
            self.textEdit.setText("{}".format(list[a - 1][1]))
            self.label_7.setText("{}".format(list[a - 1][2]))
        else:
            pass


        #sqlite bağlantısı şart
        #diğer sınıfdada bağlantı yaptım ordaki bilgileri burdan çektik
        #sınıflar arası kalıtım sıkıntılı olunca sqlite kurtarıcı oluyor
        #sqlite bağlantısı sıralama yapmamıda sağladı

    def baglan(self):
        self.con = sqlite3.connect("notes.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS note(baslik TEXT,notum TEXT,zaman INT)")
        self.con.commit()



    def exit(self):
        QApplication.exit()


    def note(self):
        notepad1 = note()
        widget.addWidget(notepad1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class note(QDialog):
    def __init__(self):
        super(note, self).__init__()
        loadUi(r"C:\Users\bugra\OneDrive\Masaüstü\notepad-pro\note.ui", self)

        self.pushButton.clicked.connect(self.geri)
        self.pushButton_2.clicked.connect(self.sil)
        self.pushButton_4.clicked.connect(self.konum)
        self.pushButton_3.clicked.connect(self.kaydet)

        self.path = "emty"

        self.baglan()

    def baglan(self):
        self.con = sqlite3.connect("notes.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS note(baslik TEXT,notum TEXT,zaman INT)")
        self.con.commit()

    def geri(self):
        geri1 = notepad()
        widget.addWidget(geri1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sil(self):
        self.textEdit.setText("")
        self.lineEdit.setText("")

    def konum(self):
        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))  # varolanı seçtirir

    def kaydet(self):
        # textedit için toPlainText()
        # line edit için text() çalışır


        #eğer path seçilmediyse çalıştığım klosör seçilsin

        if self.path == "emty":
            self.path = r"C:/Users/bugra/OneDrive/Masaüstü/notepad-pro"
            print("wdqwdq")

        #eğer kullanıcı klosör seçtiyse o path kullanılsın

        with open(self.path + "/{}.txt".format(self.lineEdit.text()), "w", encoding="utf-8") as file:
            file.write("{}".format(self.textEdit.toPlainText()))
        print("kayıt alındı")

        os.chdir(self.path)

        # saniye cinsinden verilen değeri tarihe çevirdim
        # fromtimestamp sanite = > zaman (date)

        zaman = datetime.datetime.fromtimestamp(os.stat(self.lineEdit.text() + ".txt").st_ctime)

        self.tam_zaman = datetime.datetime.strftime(zaman, "%D\t%X")



        self.cursor.execute("INSERT into note values(?,?,?) ",(self.lineEdit.text(), self.textEdit.toPlainText(), self.tam_zaman))
        self.con.commit()


        self.geri()


app = QApplication(sys.argv)
main1 = notepad()
widget = QStackedWidget()
widget.addWidget(main1)
widget.setWindowTitle("Notepad-Pro")
widget.setWindowIcon(QIcon(r"C:\Users\bugra\OneDrive\Masaüstü\notepad-pro\ıcon.png"))
widget.setFixedWidth(1200)
widget.setFixedHeight(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("çıkılıyor")