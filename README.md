# Selenium Otomasyon Projesi

## Proje Hakkında
Python ve Selenium kullanılarak geliştirilmiş bu otomasyon projesi, ilanlar.gov sitesinde paylaşılan araştırma görevlisi ilanlarını günlük olarak takip eder 
ve verdiğiniz kelimelere göre sizin için arama yapıp hangi ilanların o gün için size uyumlu olduğunu kontrol eder ve oluşturduğunuz Telegram bota mesaj gönderir . \n  
Başlıca hedefi, gündelik olarak ilanlara bakan insanlara zaman tasarrufu sağlamaktır.  
Proje AWS, Google gibi platformlarda **cron job** ile zamanlanabilir ve kendi bilgisayarınızda scripti sürekli çalıştırmadan kurulum yapılabilir.

---

## 🌟 Temel Değerler
- **Otomasyon:** Tekrarlayan arama görevlerinin hızla tamamlanması  
- **Esneklik:** Farklı ortamlarda (yerel, bulut) çalışabilirlik  
- **Kolay Kurulum:** Basit ve anlaşılır kurulum adımları  

---

## 🛠️ Teknolojiler
- Python 3.8+  
- Selenium WebDriver  
- ChromeDriver  
- AWS EC2  (opsiyonel)  
- Cron (Linux/Mac) veya Task Scheduler (Windows)  (opsiyonel) 

---

## 🚀 Kurulum

### 1. Projeyi Klonla
```bash
git clone https://github.com/CarpeDiem0110/Research_Assistant_Search_Automation.git
cd proje_adi
pip install -r requirements.txt

```
### 2. Telegram Bot oluştur
```bash
BotFather ile yeni bir bot oluşturun
Projeyi oluşturduğunuz klasör içerisinde .env dosyası oluşturun

 
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""


Oluşturduğunuz .env dosyasında bu parametreleri doldurun

```
### 3. Projeyi çalıştırın

python main.py 


--- 


## TEST VIDEO 

https://github.com/user-attachments/assets/b1645b96-51b9-4a78-afad-4853ba7f557b









