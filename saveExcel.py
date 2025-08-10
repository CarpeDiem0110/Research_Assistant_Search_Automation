from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import datetime
import openpyxl
from TelegramBot import TelegramBot

# What kind of features is going to be added  !!!!
# 
# Send the message to telegram bot if the date is today
# Integrate with windows scheduler to run the script daily
# Cloud'a host edersen scheduler ayarlayıp buradan kendine mesaj attırabilirsin


TELEGRAM_BOT_TOKEN = "7796630658:AAGQWYsg_1TEK1Mpy30gzqBxPFeDGhNPw6s"
TELEGRAM_CHAT_ID = "5219479758"


def take_today_date():
    today = str(datetime.date.today())
    today_formatted = datetime.datetime.strptime(today, "%Y-%m-%d").strftime("%d.%m.%Y")
    return today_formatted



def initalize_bot():
    bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    return bot

    

print("Today is: ", take_today_date())

filename = "deneme.xlsx" 



time.sleep(2)

# Create a new Excel workbook and worksheet and if excel table exist on the project folder, append new data to it 

if os.path.exists(filename):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    print("Excel file exists. Loaded the existing workbook.")
else:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Deneme"
    ws.append(["UNIVERSITY NAME", "DATE"])  # Add headers only when creating new file
    print("Excel file not found. Created a new workbook.")
    


TelegramBot = initalize_bot()

print("BOT IS CONNECTED")


driver = webdriver.Chrome()






# Iterate through each announcement. We will check the first 2 pages for now
for i in range(2):
    url = f"https://www.ilan.gov.tr/ilan/kategori/73/akademik-personel-alimlari?currentPage={i+1}&field=publish_time&order=desc"
    
    print(f"Checking page {i+1}: {url}")
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
    #wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search-results-row")))
    #announcements = driver.find_elements(By.CLASS_NAME, "search-results-row")

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.col.col-4.col-lg-4.col-border")))
    başlıklar = driver.find_elements(By.CSS_SELECTOR, "div.col.col-4.col-lg-4.col-border")

    
    print("NUMBER OF ANNOUNCEMENT FOUND  FOR  " ,i+1 ,"TH PAGE : ", len(başlıklar))

    print("--------------------")

    j = 0
     
    while j < len(başlıklar):    
        başlıklar = driver.find_elements(By.CSS_SELECTOR, "div.col.col-4.col-lg-4.col-border")
        
        
        
        if "Düzeltme İlanı" in başlıklar[j].text or "Düzeltme ilanı" in başlıklar[j].text or "İptal İlanı" in başlıklar[j].text :
            print("BU BIR DUZELTME VEYA IPTAL ILANI BUNU PAS GEÇ")
            print(başlıklar[j].text.strip())
            j += 1
            print("-------")
            continue
        
            
        başlıklar[j].click()
        # Wait for the page to load
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list-desc")))
        date_elements = driver.find_elements(By.CLASS_NAME, "list-desc") # It returns a list of elements 
            

            # CHECK IF DATE ELEMENTS ARE PRESENT IN THE LIST 
        if len(date_elements) == 5:
            university_name = date_elements[0].text
            date_value = date_elements[4].text
            print("UNIVERSITY NAME : ", university_name)
            print(date_value)
            current_date = take_today_date()

            if date_value == current_date:
                print("Today is the date of the announcement.")
                ws.append([university_name, date_value]) 
                message = (
                        f"📢 <b>Yeni Akademik Personel İlanı</b>\n\n"
                        f"🏛️ Üniversite: <b>{university_name}</b>\n"
                        f"📅 Tarih: <b>{date_value}</b>\n"
                    )
                TelegramBot.send_message(message) # AYNI TARIHE SAHIPSE ILANI EKLE 
                print("-------")
            else:
                print("This announcement is not for today.")
                print("-------")
                    
        else: 
            university_name = date_elements[0].text
            date_value = "NONE"
            print("UNIVERSITY NAME : ", university_name)
            print(date_value)
            current_date = take_today_date()
            if date_value == current_date:
                print("Today is the date of the announcement.")
                ws.append([university_name, date_value])
                print("-------")
        j += 1
        driver.back()  # Go back to the listing page
        time.sleep(2) # Wait for the page to load

# After the loop, save the Excel file
wb.save("deneme.xlsx")

print("Excel file saved successfully.")



