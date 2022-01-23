from PyQt5 import *
from cityui import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


#---------- API adres--------------------------------------
import requests
url="http://api.openweathermap.org/data/2.5/weather?"
api_key="c85a7807defc54ff849ae03ceeb07bc7"
# https://openweathermap.org/weather-conditions
icon_url="http://openweathermap.org/img/wn/{}@2x.png"

# ---------style -color--------------------------------------------------------------
Uygulama=QApplication(sys.argv)
style = """
        QWidget{
            background-image:url('gunes.JPG') ;
        }
        QLabel{
           
           color: #212121;
           font-weight: bold;
          
        }
        QLabel#round_count_label, QLabel#highscore_count_label{
            border: 1px solid #fff;
            border-radius: 8px;
            padding: 2px;
            
        }
        QPushButton
        {
            color: black;
            background:#F57C00;
            font-weight: bold;
            font-size: 8pt;
            outline: none;
        }
        QTableWidget{
            border: 1px #C6C6C6 solid;
            color: #FFE0B2;
            background:#757575;
            font-weight: bold;
            font-size: 7pt;
            outline: none;
        }
        QLineEdit {
            background:#FFE0B2;
            padding: 1px;
            color: black;
            border-style: solid;
            border: 2px solid #fff;
            border-radius: 8px;
            font-weight: bold;
            font-size: 9pt;
        }
    """
Uygulama.setStyleSheet(style)

#----------------------VERİTABANI OLUSTUR-----------------#

import sqlite3
global curs
global conn

con_nl=sqlite3.connect('NETHERLAND.db')
cursor_nl=con_nl.cursor()

con_usa=sqlite3.connect('USA.db')
cursor_usa=con_usa.cursor()

con_tr=sqlite3.connect('TURKEY.db')
cursor_tr=con_tr.cursor()


#----------------------UYGULAMA OLUŞTUR-------------------#

Ana=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(Ana)
Ana.show()


#------------------NL veri cekme----------------------------------#  
def NL():
    
    ui.tbl.clear()
    ui.tbl.setHorizontalHeaderLabels(('CITY','PROVINCE','POPULATION'))
    
    cursor_nl.execute("SELECT * FROM HOLLAND ORDER BY  CENSUS DESC")
    
    for satirIndeks, satirVeri in enumerate(cursor_nl):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tbl.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    
    cursor_nl.execute("SELECT COUNT(*) FROM HOLLAND")
    kayitSayisi=cursor_nl.fetchall()
    ui.lblKayitSayisi.setText(" TOTAL :" + str(kayitSayisi[0][0]))
    
#------------------USA veri cekme----------------------------------# 
def USA():
    ui.tbl.clear()
    ui.tbl.setHorizontalHeaderLabels(('CITY','PROVINCE','POPULATION','MUNICIPALITY'))
    cursor_usa.execute("SELECT * FROM USA ORDER BY  CENSUS DESC")
    
    for satirIndeks, satirVeri in enumerate(cursor_usa):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tbl.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    
    cursor_usa.execute("SELECT COUNT(*) FROM USA")
    kayitSayisi=cursor_usa.fetchall()
    ui.lblKayitSayisi.setText(" TOTAL :" + str(kayitSayisi[0][0]))
    
#------------------TR veri cekme----------------------------------# 
def TR():
    
    ui.tbl.clear()
    ui.tbl.setHorizontalHeaderLabels(('CITY','PROVINCE','POPULATION','MUNICIPALITY'))
    cursor_tr.execute("SELECT * FROM TURKIYE ORDER BY  CENSUS DESC")
    
    for satirIndeks, satirVeri in enumerate(cursor_tr):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tbl.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    
    cursor_tr.execute("SELECT COUNT(*) FROM TURKIYE")
    kayitSayisi=cursor_tr.fetchall()
    ui.lblKayitSayisi.setText(" City count :" + str(kayitSayisi[0][0]))  
    
#==============VERILERI EKRANA YAZDIRMA ===================================================================  
# -----ekrana city,prov,nufus verilerini yazma-------------
def write(city,prv,nfs):
    ui.veri_city.clear()
    ui.veri_prv.clear()
    ui.veri_nfs.clear()
    ui.veri_city.setText(city)
    ui.veri_prv.setText(prv)
    ui.veri_nfs.setText(str(nfs))
# -----Databaseden veri cekme-----------------------------
def VERI_ISLEME(city):
    # print(city,"-------------------------------------------")
    data_tr=cursor_tr.execute("SELECT * FROM TURKIYE ")
    data_usa=cursor_usa.execute("SELECT * FROM USA ")
    data_nl=cursor_nl.execute("SELECT * FROM HOLLAND ")
    for i in [data_tr,data_usa,data_nl]:
        for x in i:
            # print(x[0])
            if x[0]==city:
                # print(x[0])
                # print("=======================================")
                city_,prv,nfs=x[0],x[1],x[2]
                weather(city_)
                write(city_,prv,nfs)
                break
#----------Api den verileri alma-yazma-------------------------------- 
def weather(sehir):
    ui.sehir.clear()
    ui.temp.clear()
    ui.durum.clear()
    ui.icon.clear()
    sehir=sehir.lower()
    # print(sehir)
    # ----------------API HAVA DURUMU------------
    params={"q":sehir,"appid":api_key,"lang":"en"}
    data=requests.get(url,params=params).json()
    # print(data)
    if data['cod']==200:
        
        city=data["name"].capitalize()
        country=data['sys']['country'].capitalize()
        durum=data["weather"][0]['description'].capitalize()
        temp=data["main"]['temp']
        temp=int(temp-273.15)
        icon_no=data["weather"][0]['icon']
        # print(city,country,durum,temp)
        
        # -----ekrana yazdirma------------------------------
        ui.durum.setText(city+","+country)
        ui.temp.setText(str(temp)+"°C")
        ui.sehir.setText(durum)
        
        # --------------------ICON ALMA-YAZMA----------------------
        from PyQt5.QtGui import QImage, QPixmap
        image = QImage()
        # -----icon request kismi burada
        image.loadFromData(requests.get(icon_url.format(icon_no)).content)
        ui.icon.setPixmap(QPixmap(image))
        ui.icon.show()
        
    ui.ln_city.clear()
# -------sehir aramasi yaparak veri alma-------------------------------

def ARA():
    city=ui.ln_city.text()
    if city:
        VERI_ISLEME(city.upper())
    
#==============TABLODAN VERI CEKME=================================================================== 
def TABLO(konum,y):
    # QTableWidget.selectionModel().selectionChanged.connect(TABLO) ====> 2 adet konum bilgisi donuyor.
    for location in konum.indexes():
        row=location.row()
        column=location.column()
        kontrol=ui.tbl.item(row,column)
        # print(row,column)
        if kontrol and column==0:
            cell_text=ui.tbl.item(row,column).text()
            # print(cell_text,"tablo")
            VERI_ISLEME(cell_text)
    
#=========================ÇIKIŞ======================================
def CIKIS():
    cevap=QMessageBox.question(Ana,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
    QMessageBox.Yes | QMessageBox.No)
    
    if cevap==QMessageBox.Yes:
        con_nl.close()
        con_tr.close()
        con_usa.close()
        sys.exit(Uygulama.exec_())
    else:
        Ana.show()
# ============PROGRAM BASLIYOR....====================================== 
ui.tbl.clear()
ui.tbl.setHorizontalHeaderLabels(('CITY','PROVINCE','POPULATION','MUNICIPALITY'))
# -----------transparan yapma---------------------------
ui.sehir.setAttribute(Qt.WA_TranslucentBackground, True)
ui.temp.setAttribute(Qt.WA_TranslucentBackground, True)
ui.durum.setAttribute(Qt.WA_TranslucentBackground, True)
ui.icon.setAttribute(Qt.WA_TranslucentBackground, True)
ui.tbl.setAttribute(Qt.WA_TranslucentBackground, True)
ui.veri_city.setAttribute(Qt.WA_TranslucentBackground, True)
ui.veri_prv.setAttribute(Qt.WA_TranslucentBackground, True)
ui.veri_nfs.setAttribute(Qt.WA_TranslucentBackground, True)
ui.label.setAttribute(Qt.WA_TranslucentBackground, True)
ui.label_4.setAttribute(Qt.WA_TranslucentBackground, True)
ui.label_3.setAttribute(Qt.WA_TranslucentBackground, True)
ui.label_5.setAttribute(Qt.WA_TranslucentBackground, True)
ui.lblKayitSayisi.setAttribute(Qt.WA_TranslucentBackground, True)
# ---------------------------------------------------------------------
ui.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
# ----------------fonksiyonlar--------------
ui.btn_tr.clicked.connect(TR)
ui.btn_nl.clicked.connect(NL)
ui.btn_usa.clicked.connect(USA)
ui.btn_cks.clicked.connect(CIKIS)
ui.btn_arama.clicked.connect(ARA)
ui.tbl.selectionModel().selectionChanged.connect(TABLO)

sys.exit(Uygulama.exec_())


