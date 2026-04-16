import requests
from bs4 import BeautifulSoup

# --- البيانات دي أهم من عهده المخزن ---
TOKEN = "8651775947:AAHM1F0fLZfCmKLKmEwU5z0oKhWbJp2TUvU"
CHAT_ID = "1385986683"
# ------------------------------------

def check_amazon():
    # رابط المنتج اللي انت عايزه (كمثال)
    url = "https://www.amazon.eg/dp/B0BYMSY98K" 
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # بنحاول نجيب السعر
        price_raw = soup.find("span", {"class": "a-offscreen"}).text
        # تنظيف السعر من العملة والفواصل عشان نعرف نقارنه
        current_price = float(price_raw.replace('EGP', '').replace(',', '').strip())
        
        # هنا بقى اللوجيك المحاسبي: لو السعر اقل من 15000 ابعتلي
        if current_price < 15000:
            message = f"🚨 الحق لقطة! السعر نزل لـ {current_price} ج.م \nالرابط: {url}"
            send_link = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
            requests.get(send_link)
            print("Done! Alert Sent.")
        else:
            print(f"No luck! Price is still {current_price}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_amazon()
