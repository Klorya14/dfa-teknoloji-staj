from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def scrapping():
    url=entry.get()
    if "hepsiburada" not in url:
     messagebox.showerror("Geçersiz Sayfa", "Bu sayfa Hepsiburada'ya ait değil.")
     return

    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(2)

    try:
        buton=driver.find_element(By.CLASS_NAME,"M6iJLUpgHKlEPzGcOggE")
        buton.click()
        time.sleep(2)
    except:
         print("Diğer satıcılar butonu bulunamadı!")

    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")


    sellers=[]
    

    for item in soup.find_all("div", class_="VwUAvtsSpdiwukfc0VGp IsAfBKbg4xH3kdMRzVZO mnWNji9_P_vYbkjHXtoH"):
        try:
            product_name=soup.find("h1", attrs={"data-test-id":"title"}).text.strip()
        except:
            product_name="None"
        try:
             name=item.find("a",attrs={"data-test-id":"merchant-name"}).text.strip()
        except:
          name="None"
        try:
             price=item.find("div", attrs={"data-test-id":"price-current-price"}).text.strip()
        except:
             price="None"
        try:
          cargo=item.find("div",attrs={"data-test-id":"shipment-text"}).text.strip()
        except:
             cargo="None"
        try:
             rate=item.find("span",attrs={"data-test-id":"merchant-rating"}).text.strip()
        except:
             rate="None"
        
        sellers.append({
        "Satıcı":name,
        "Fiyat":price,
        "Satıcı Puanı":rate,
        "Kargo Bilgisi":cargo,
        "Ürün Adı":product_name
        })

    if(len(sellers)<5):
        driver.quit()
        messagebox.showerror(title="Hata!",message="Seçtiğiniz üründe en az 5 satıcı bulunmalıdır.")
        

    df=pd.DataFrame(sellers)
    df.to_csv("satıcılar.csv",index=False, encoding="utf-8-sig")
    msg=f"Ürün Adı: {product_name}\n\n"

    cheapest = df.sort_values("Fiyat").head(5)

    for _, row in cheapest.iterrows():
        msg+=f"- Satıcı: {row['Satıcı']}\n"
        msg+=f"  Fiyat: {row['Fiyat']}\n"
        msg+=f"  Puan: {row['Satıcı Puanı']}\n"
        msg+=f"  Kargo: {row['Kargo Bilgisi']}\n\n"
            

    msg2=f"Ürün Adı: {product_name}\n\n"
    expensive=df.sort_values("Fiyat", ascending=False).head(5)

    for _, row in expensive.iterrows():
        msg2+=f"- Satıcı: {row['Satıcı']}\n"
        msg2+=f"  Fiyat: {row['Fiyat']}\n"
        msg2+=f"  Puan: {row['Satıcı Puanı']}\n"
        msg2+=f"  Kargo: {row['Kargo Bilgisi']}\n"

    driver.quit()
    messagebox.showinfo(title="En Ucuz 5 Satıcı:",message=msg)
    messagebox.showinfo(title="En Pahalı 5 Satıcı:",message=msg2)

    

form=tk.Tk()
form.title("Hepsiburada Fiyat Karşılaştırma Aracı")
form.geometry("500x400")
form.resizable(False,False) 
buton=tk.Button(text="Url'yi Ekle",width=10,height=2,command=scrapping,bg="#ff6305")
buton.place(x=150,y=190)
entry=tk.Entry()
entry.place(x=175,y=140)
exit_button=tk.Button(text="Çıkış",width=10,height=2,command=exit,bg="#ff6305")
exit_button.place(x=250,y=190)
image = Image.open("logo.png") 
image = image.resize((125, 50))
photo = ImageTk.PhotoImage(image)
label = tk.Label(form, image=photo)
label.image = photo  
label.place(x=174, y=70)


form.mainloop()
