import pywhatkit
import wikipedia
from pytube import YouTube
from pywikihow import RandomHowTo, search_wikihow
import os
import speech_recognition as sr
import webbrowser as web
import bs4
import pyttsx3
from time import sleep
import json
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


def Speak(audio):
    print(" ")
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()
    print(" ")


def TakeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print(": Listening....")

        r.pause_threshold = 1

        audio = r.listen(source)

    try:

        print(": Recognizing...")

        query = r.recognize_google(audio, language='en-in')

        print(f": Your Command : {query}\n")

    except:
        return ""

    return query.lower()


def GoogleSearch(term):
    query = term.replace("jarvis", "")
    query = query.replace("what is", "")
    query = query.replace("how to", "")
    query = query.replace("what is", "")
    query = query.replace(" ", "")
    query = query.replace("what do you mean by", "")

    writeab = str(query)

    oooooo = open('E:\\JARVIS_AI\\Advanced Jarvis\\Data.txt', 'a')
    oooooo.write(writeab)
    oooooo.close()

    Query = str(term)

    pywhatkit.search(Query)

    os.startfile(
        'E:\\JARVIS_AI\\DataBase\\ExtraPro\\start.py')

    if 'how to' in Query:

        max_result = 1

        how_to_func = search_wikihow(query=Query, max_results=max_result)

        assert len(how_to_func) == 1

        how_to_func[0].print()

        Speak(how_to_func[0].summary)

    else:

        search = wikipedia.summary(Query, 2)

        Speak(f": According To Your Search : {search}")


def YouTubeSearch(term):
    result = "https://www.youtube.com/results?search_query=" + term
    web.open(result)
    Speak("This Is What I Found For Your Search .")
    pywhatkit.playonyt(term)
    Speak("This May Also Help You Sir .")


def Alarm(query):
    TimeHere = open('E:\\JARVIS_AI\\Advanced Jarvis\\Data.txt', 'a')
    TimeHere.write(query)
    TimeHere.close()
    os.startfile(
        "E:\\JARVIS_AI\\DataBase\\ExtraPro\\Alarm.py")


def DownloadYouTube():
    from pytube import YouTube
    from pyautogui import click
    from pyautogui import hotkey
    import pyperclip
    from time import sleep
    sleep(2)
    click(x=942, y=59)
    hotkey('ctrl', 'c')
    value = pyperclip.paste()
    Link = str(value)


def Download(link):
    url = YouTube(link)

    video = url.streams.first()

    video.download('E:\\JARVIS_AI\\DataBase\\')

    Download(link)

    Speak("Done Sir , I Have Downloaded The Video .")

    Speak("You Can Go And Check It Out.")

    os.startfile('E:\\JARVIS_AI\\DataBase\\')


def searchWikipedia(query):
    if "wikipedia" in query:
        Speak("Searching from wikipedia....")
        query = query.replace("wikipedia", "")
        query = query.replace("search wikipedia", "")
        query = query.replace("jarvis", "")
        results = wikipedia.summary(query, sentences=3)
        Speak("According to wikipedia..")
        print(results)
        Speak(results)


def Weather(query):
    query = query.replace('temperature', 'temperature in')
    query = query.replace('temperature in', 'temperature in')
    url = f"https://www.google.com/search?q={query}"
    r = requests.get(url)
    data = bs4.BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    Speak(f"current {query} is {temp}")


def latestnews():
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=64827dab6e4b4756b79ff3ae2e66b5d8",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=64827dab6e4b4756b79ff3ae2e66b5d8",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=64827dab6e4b4756b79ff3ae2e66b5d8",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=64827dab6e4b4756b79ff3ae2e66b5d8",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=64827dab6e4b4756b79ff3ae2e66b5d8",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=64827dab6e4b4756b79ff3ae2e66b5d8"
    }

    content = None
    url = None
    Speak("Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
    field = TakeCommand()
    for key, value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            Speak("The Required News was Found")
            break
        else:
            url = True
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    Speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        print(article)
        Speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")
        break
    Speak("thats all")


def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        pyttsx3.speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 2)
            pyttsx3.speak(result)

        except:
            pyttsx3.speak("No speakable output available")


def DateConverter(Query):
    Date = Query.replace(" and ", "-")
    Date = Date.replace(" and ", "-")
    Date = Date.replace("and", "-")
    Date = Date.replace("and", "-")
    Date = Date.replace(" ", "")

    return str(Date)


def My_Location():
    op = "https://www.google.com/maps/place/Srinivasa+Ramanujam+Block/@9.5745115,77.6768954,17.65z/data=!4m6!3m5!1s0x3b06dbe9f24d63cd:0x56346966dabfd7f!8m2!3d9.5747458!4d77.6753113!16s%2Fg%2F11gdkwz8dn"

    Speak("Checking....")

    web.open(op)


def CoronaVirus(Country):
    countries = str(Country).replace(" ", "")

    url = f"https://www.worldometers.info/coronavirus/#countries{countries}/"

    result = requests.get(url)

    soups = bs4.BeautifulSoup(result.text, 'lxml')

    corona = soups.find_all('div', class_='maincounter-number')

    Data = []

    for case in corona:
        span = case.find('span')

        Data.append(span.string)

    cases, Death, recovered = Data

    Speak(f"Cases : {cases}")
    Speak(f"Deaths : {Death}")
    Speak(f"Recovered : {recovered}")
