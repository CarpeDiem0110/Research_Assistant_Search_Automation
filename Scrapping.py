from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import datetime
import openpyxl
from TelegramBot import TelegramBot
from selenium.webdriver.chrome.options import Options


class Scraping:
    def __init__(self, telegram_bot):
        self.telegram_bot = telegram_bot
        self.driver = None
        self.setup_driver()

    def take_today_date(self):
        today = str(datetime.date.today())
        today_formatted = datetime.datetime.strptime(today, "%Y-%m-%d").strftime("%d.%m.%Y")
        return today_formatted

    

    def setup_driver(self):
        self.driver = webdriver.Chrome()

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def scrape_and_notify(self, pages=2):
        current_date = self.take_today_date()
        print("Today is:", currentDate)

        for i in range(pages):
            url = self._build_url(i + 1)
            print(f"Checking page {i+1}: {url}")
            self.driver.get(url)
            self._wait_for_page()

            başlıklar = self._get_announcements()
            print(f"NUMBER OF ANNOUNCEMENT FOUND FOR {i+1}TH PAGE: {len(başlıklar)}")
            print("--------------------")

            self._process_announcements(başlıklar, currentDate)

        


    



    ### HELPER FUNCTIONS ###

    # Build the URL for the given page number
    def _build_url(self, page_number):
        return f"https://www.ilan.gov.tr/ilan/kategori/73/akademik-personel-alimlari?currentPage={page_number}&field=publish_time&order=desc"

    # Wait for the take University names from the page
    def _wait_for_page(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.col.col-4.col-lg-4.col-border")))

    # Get University names from the page
    def _get_announcements(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "div.col.col-4.col-lg-4.col-border")

    # Process all the announcements for the current page
    def _process_announcements(self, başlıklar, current_date):
        j = 0
        while j < len(başlıklar):
            başlıklar = self._get_announcements()
            text = başlıklar[j].text
            

            if self._is_unwanted_announcement(text):
                print("BU BIR DUZELTME VEYA IPTAL ILANI BUNU PAS GEÇ")
                print(text.strip())
                print("-------")
                j += 1
                continue

            başlıklar[j].click()
            self._wait_for_details()

            date_elements = self.driver.find_elements(By.CLASS_NAME, "list-desc")
            self._process_single_announcement(date_elements, current_date)

            self.driver.back()
            time.sleep(2)
            j += 1

    # Check if an announcement is unwanted
    def _is_unwanted_announcement(self, text):
        unwanted_keywords = ["Düzeltme İlanı", "Düzeltme ilanı", "İptal İlanı"]
        return any(keyword in text for keyword in unwanted_keywords)
    
    # Wait for the details of the announcement to load
    def _wait_for_details(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list-desc")))
    
    # Process a single announcement and send notification if applicable
    def _process_single_announcement(self, date_elements, current_date):
        
        if len(date_elements) == 5:
            university_name = date_elements[0].text
            date_value = date_elements[4].text
            print("UNIVERSITY NAME:", university_name)
            print("DATE:", date_value)

            
            
            if date_value == current_date:
                print("Today is the date of the announcement.")
                announcement_url = self.driver.current_url 
                  

                is_compatible = self.check_compatability_to_your_area(announcement_url)

                if is_compatible:
                    compatibility_text = "✅ Bu ilan bilgisayar mühendisliği ile ilgili olabilir "
                else:
                    compatibility_text = "❌ Bu ilan senin verdiğin anahtar kelimelere uygun değildir."     
                
                message = (
                    f"📢 <b>Yeni Akademik Personel İlanı</b>\n\n"
                    f"🏛️ Üniversite: <b>{university_name}</b>\n"
                    f"📅 Tarih: <b>{date_value}</b>\n"
                    f"🔗 <a href='{announcement_url}'>İlan Linki</a>\n"
                    f"{compatibility_text}"
                    
                )
                self.telegram_bot.send_message(message)
                print("-------")
            else:
                print("This announcement is not for today.")
                print("-------")
        else:
            university_name = date_elements[0].text if date_elements else "UNKNOWN"
            print("UNIVERSITY NAME:", university_name)
            print("DATE: NONE")    


    def check_compatability_to_your_area(self,url):
        self.driver.get(url)
        

        wait = WebDriverWait(self.driver, 10)
        
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        except Exception as e:
            print("Table element did not load:", e)
            return
        
        td_elements = self.driver.find_elements(By.XPATH, "//table//td")


        if not td_elements:
            print("No <td> elements found.")
                
        else:
             # Extract the text of each <td>
            td_texts = [td.text for td in td_elements]

            # Define keywords to search
            keywords = ["Bilgisayar", "bilgisayar"]

            # Search for each keyword
            for keyword in keywords:
                for td_text in td_texts:
                    if keyword.lower() in td_text.lower():
                        print(f"✅ Found keyword '{keyword}' in: {td_text}")
                        return True
                        
            print("❌ Hiçbir anahtar kelime bulunamadı.")
            return False

            
        
        
