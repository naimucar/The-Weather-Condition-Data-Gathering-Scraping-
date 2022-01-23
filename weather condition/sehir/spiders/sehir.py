
import scrapy
import sqlite3
# ---------------database nl-----------
con=sqlite3.connect("NETHERLAND.db")
cursor=con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS  HOLLAND (CITY TEXT,PROVINCE TEXT,CENSUS INT)")
con.commit()
# -----------database tr---------------
con_2=sqlite3.connect("TURKEY.db")
cursor_2=con_2.cursor()
cursor_2.execute("CREATE TABLE IF NOT EXISTS  TURKIYE (CITY TEXT,PROVINCE TEXT,CENSUS INT)")
con_2.commit()

# ----------database usa -----------------

con_3=sqlite3.connect("USA.db")
cursor_3=con_3.cursor()
cursor_3.execute("CREATE TABLE IF NOT EXISTS  USA (CITY TEXT,PROVINCE TEXT,CENSUS INT)")
con_3.commit()



class BookSpider(scrapy.Spider):
    name = 'sehir'
    start_urls = [
        'https://nl.wikipedia.org/wiki/Lijst_van_Nederlandse_plaatsen_met_stadsrechten',
        "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population",
        "https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27deki_illerin_n%C3%BCfuslar%C4%B1_(2020)",]
    
    def parse(self, response):
        # ---------------------------ABD---------------------------------
        
        tablo_usa=response.xpath('//*[@id="mw-content-text"]/div[1]/table[5]/tbody').css("tr")
        sehir_usa,eyalet_usa,nufus_usa="veri yok","veri yok",0
        for veri in tablo_usa[1:]:
            # print(veri)
            liste=veri.css("td ::text").getall()
            # print(liste)
            
            if liste:
            
                sehir_usa=liste[0].strip()
                
                # print(sehir_turkiye)
                if "[" in liste[1]:
                    nufus_usa=liste[5].strip().split(',')
                    nufus_usa="".join(nufus_usa)
                    nufus_usa=int(nufus_usa)
                    # print(nufus_usa)
                    eyalet_usa=liste[3].strip()
                    # print(eyalet_usa)
                else:
                    nufus_usa=liste[4].strip().split(',')
                    nufus_usa="".join(nufus_usa)
                    nufus_usa=int(nufus_usa)
                    # print(nufus_usa)
                    eyalet_usa=liste[2].strip()
                
                # print(sehir_usa,nufus_usa,"ABD")
                
            # yield {"city":sehir_usa,"Eyalet":eyalet_usa,"population":nufus_usa}
        
            cursor_3.execute("INSERT INTO USA (CITY,PROVINCE ,CENSUS ) VALUES(?,?,?)",(sehir_usa,eyalet_usa,nufus_usa,))
            con_3.commit()
        # ---------------------------TR-----------------------------------
        tablo_turkiye=response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody').css("tr")
        sehir_turkiye,eyalet_tr,nufus_turkiye="veri yok","veri yok",0
        for veri in tablo_turkiye[1:]:
            
            liste=veri.css("td ::text").getall()
            # print(liste)
            
            if liste:
                # print(liste)
                sehir_turkiye=liste[0].strip().upper()
                # print(sehir_turkiye)
                nufus_turkiye=liste[1].strip()
                nufus_turkiye=int(nufus_turkiye)
                # print(nufus_turkiye)
                eyalet_tr=liste[2].strip()
                # print(eyalet_tr) 
                # print(sehir_turkiye,nufus_turkiye,"turkiye")
                
            # yield {"sehir":sehir_turkiye,"Bolge":eyalet_tr,"nufus":nufus_turkiye}
            cursor_2.execute("INSERT INTO TURKIYE (CITY,PROVINCE ,CENSUS ) VALUES(?,?,?)",(sehir_turkiye,eyalet_tr,nufus_turkiye,))
            con_2.commit()
        
        
        # --------------------------NL-----------------------------------------------
        
        tablo=response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody').css("tr")
        for veri in tablo:
            href=veri.css("td a ::attr(href)").get()
            # print(href)
            url=response.urljoin(href)
            yield scrapy.Request(url, callback=self.detail)

    def detail(self,response):
        sehir_nl=response.css('h1.firstHeading ::text').get().strip()
        if "(" in sehir_nl:
            sehir_nl=sehir_nl.split('(')[0].strip()
        sehir_nl=sehir_nl.upper()
        if sehir_nl=="LIJST VAN NEDERLANDSE PLAATSEN MET STADSRECHTEN":
        # print(sehir)
            return
        tab=response.css('table.infobox tbody tr')
        eyalet_nl,nufus_nl="Geen Data",0
        for veriler in tab:
            veri=veriler.css("td ::text").getall()
            # print(veri)
            if veri[0]=='Provincie':
                eyalet_nl=veri[1]
                # print("eyalet: ",veri[1])
            elif veri[0]=='Inwoners '  or veri[0]=='Inwoners':
                if veri[1]==' ':
                    nufus_nl=veri[3].strip().split('.')
                    nufus_nl="".join(nufus_nl)
                    nufus_nl=int(nufus_nl)
                    print("nufus",veri[3])
                else:
                    nufus_nl=veri[2].strip().split('.')
                    nufus_nl="".join(nufus_nl)
                    nufus_nl=int(nufus_nl)
                    # print("nufus2",veri[2])
            
        # print(eyalet_nl,nufus_nl)
        cursor.execute("INSERT INTO HOLLAND (CITY,PROVINCE ,CENSUS ) VALUES(?,?,?)",(sehir_nl,eyalet_nl,nufus_nl,))
        con.commit()
