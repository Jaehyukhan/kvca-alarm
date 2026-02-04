import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def send_telegram(message):
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, params=params)

def crawl_kvca():
    # 한국벤처캐피탈협회
    url = "https://www.kvca.or.kr/Program/invest/list.html?a_gb=board&a_cd=8&a_item=0&sm=2_2_2"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    today = datetime.now().strftime('%Y.%m.%d')
    posts = []
    
    rows = soup.select('table.board_list tbody tr')
    for row in rows:
        date_text = row.select('td')[-2].text.strip() # 날짜 위치
        if date_text == today:
            title = row.select_one('td.subject a').text.strip()
            link_path = row.select_one('td.subject a')['href']
            link = f"https://www.kvca.or.kr/Program/invest/{link_path}"
            posts.append(f"📢 [KVCA] {title}\n🔗 {link}")
    return posts

def crawl_kgrowth():
    # 한국성장금융
    url = "https://www.kgrowth.or.kr/notice.asp"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    today = datetime.now().strftime('%Y-%m-%d')
    posts = []
    
    rows = soup.select('table.board_list tbody tr')
    for row in rows:
        date_tag = row.select_one('td.date')
        if date_tag and date_tag.text.strip() == today:
            title_tag = row.select_one('td.subject a')
            title = title_tag.text.strip()
            link = "https://www.kgrowth.or.kr/" + title_tag['href']
            posts.append(f"📢 [성장금융] {title}\n🔗 {link}")
    return posts

if __name__ == "__main__":
    all_posts = crawl_kvca() + crawl_kgrowth()
    if all_posts:
        final_message = "✅ 오늘의 신규 공고입니다!\n\n" + "\n\n".join(all_posts)
        send_telegram(final_message)
    else:
        # 테스트를 위해 게시물이 없어도 메시지를 받고 싶다면 아래 주석을 해제하세요
        # send_telegram("오늘 새로 올라온 공고가 없습니다.")
        pass
