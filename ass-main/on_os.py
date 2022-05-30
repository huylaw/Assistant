import re
import smtplib
import webbrowser
from email.message import EmailMessage

import pywhatkit as kit
import requests
import wikipedia

from youtube_search import YoutubeSearch

EMAIL = 'lhuy4831@gmail.com'
PASSWORD = '0377909471'
NEWS_API_KEY = '30a1abf62efb46bf8ac56a8754860e99'
OPENWEATHER_APP_ID = 'fe8d8c65cf345889139d8e545f57819a'
TMDB_API_KEY = '75917d21d84c74724b018347ef2ef457'


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    query = query.replace('wiki', '')
    query = query.replace('wikipidie', '')
    query = query.replace('Wiki', '')
    query = query.replace('Wikipidie', '')
    query = query.replace('tìm kiếm trên', '')
    query = query.replace('tìm kiếm', '')
    results = wikipedia.summary(query, sentences=10)
    return results


def play_on_youtube(video):
    kit.playonyt(video)
    return


def search_on_google(query):
    query = query.replace('google','')
    query = query.replace('Google', '')
    query = query.replace('tìm kiếm trên', '')
    query = query.replace('tìm kiếm', '')

    kit.search(query)
    return


def open_website(query):
    reg_ex = re.search('mở trang web (.+)', query)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain + ".com"
        webbrowser.open(url)
        return True
    else:
        return False


def play_song(mysong):
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=vi&apiKey={NEWS_API_KEY}&category=general").json()
    print(res)
    articles = res["articles"]
    print(articles)
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def read_news_about(query):
    params = {
        'apiKey': '15350f84b11c4c62be0d056f095f804a',
        "q": query,
    }
    api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
    """)
        if number <= 3:
            webbrowser.open(result['url'])

    return

def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()

    temperature = res["main"]["temp"]
    feels_like = res["main"]["humidity"]
    pressure = res["main"]["pressure"]
    return f"{pressure}atm", f"{temperature} độ C", f"{feels_like}%"


def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:10]


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']
