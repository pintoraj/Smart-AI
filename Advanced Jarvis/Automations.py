from datetime import datetime
from os import startfile
import os
from pyautogui import click
from keyboard import press
from keyboard import press_and_release
from keyboard import write
from time import sleep
import notifypy as Notifypy
import pyttsx3
import speech_recognition as sr
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import webbrowser as web

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


def WhatsappMsg(name, message):
    startfile("C:\\Users\\91959\\AppData\\Local\\WhatsApp\\WhatsApp.exe")

    sleep(0.5)

    click(x=635, y=278)

    sleep(0.5)

    click(x=568, y=404)

    sleep(0.5)

    click(x=1097, y=894)

    write(message)

    press('enter')


def WhatsappCall(name):
    startfile("C:\\Users\\91959\\AppData\\Local\\WhatsApp\\WhatsApp.exe")

    sleep(10)

    click(x=681, y=246)

    sleep(0.5)

    write(name)

    sleep(0.5)

    click(x=651, y=397)

    sleep(0.5)

    click(x=1562, y=187)

    sleep(0.5)


def WhatsappChat(name):
    startfile("C:\\Users\\91959\\AppData\\Local\\WhatsApp\\WhatsApp.exe")

    sleep(10)

    click(x=640, y=245)

    sleep(1)

    write(name)

    sleep(1)

    click(x=598, y=392)

    sleep(1)

    click(x=993, y=869)

    sleep(0.5)


def ChromeAuto(command):
    query = str(command)

    if 'new tab' in query:
        press_and_release('ctrl + t')

    elif 'close tab' in query:

        press_and_release('ctrl + w')

    elif 'new window' in query:

        press_and_release('ctrl + n')

    elif 'history' in query:

        press_and_release('ctrl + h')

    elif 'download' in query:

        press_and_release('ctrl + j')

    elif 'bookmark' in query:

        press_and_release('ctrl + d')

        press('enter')

    elif 'incognito' in query:

        press_and_release('Ctrl + Shift + n')

    elif 'switch tab' in query:

        tab = query.replace("switch tab ", "")
        Tab = tab.replace("to", "")

        num = Tab

        bb = f'ctrl + {num}'

        press_and_release(bb)

    elif 'open' in query:

        name = query.replace("open ", "")

        NameA = str(name)

        if 'youtube' in NameA:

            web.open("https://www.youtube.com/")

        elif 'instagram' in NameA:

            web.open("https://www.instagram.com/")

        else:

            string = "https://www." + NameA + ".com"

            string_2 = string.replace(" ", "")

            web.open(string_2)


def YouTubeAuto(command):
    query = str(command)

    if 'pause' in query:

        press('space bar')

    elif 'resume' in query:

        press('space bar')

    elif 'full screen' in query:

        press('f')

    elif 'film screen' in query:

        press('t')

    elif 'skip' in query:

        press('l')

    elif 'back' in query:

        press('j')

    elif 'increase' in query:

        press_and_release('SHIFT + .')

    elif 'decrease' in query:

        press_and_release('SHIFT + ,')

    elif 'previous' in query:

        press_and_release('SHIFT + p')

    elif 'next' in query:

        press_and_release('SHIFT + n')

    elif 'search' in query:

        click(x=667, y=146)

        Speak("What To Search Sir ?")

        search = TakeCommand()

        write(search)

        sleep(0.8)

        press('enter')

    elif 'mute' in query:

        press('m')

    elif 'unmute' in query:

        press('m')

    else:
        Speak("No Command Found!")


def WindowsAuto(command):
    query = str(command)

    if 'home screen' in query:

        press_and_release('windows + m')

    elif 'minimize' in query:

        press_and_release('windows + m')

    elif 'show start' in query:

        press('windows')

    elif 'open setting' in query:

        press_and_release('windows + i')

    elif 'open search' in query:

        press_and_release('windows + s')

    elif 'screen shot' in query:

        press_and_release('windows + SHIFT + s')

    elif 'restore windows' in query:

        press_and_release('Windows + Shift + M')

    else:
        Speak("Sorry , No Command Found!")


def GoogleMaps(Place):
    Url_Place = "https://www.google.com/maps/place/" + str(Place)

    geolocator = Nominatim(user_agent="myGeocoder")

    location = geolocator.geocode(Place, addressdetails=True)

    target_latlon = location.latitude, location.longitude

    web.open(url=Url_Place)

    location = location.raw['address']

    target = {'city': location.get('city', ''),
              'state': location.get('state', ''),
              'country': location.get('country', '')}

    current_loca = geocoder.ip('me')

    current_latlon = current_loca.latlng

    distance = str(great_circle(current_latlon, target_latlon))
    distance = str(distance.split(' ', 1)[0])
    distance = round(float(distance), 2)

    Speak(target)
    Speak(f"Sir , {Place} iS {distance} Kilometre Away From Your Location . ")


def Notepad():
    Speak("Tell Me The Query .")
    Speak("I Am Ready To Write .")

    writes = TakeCommand()

    time = datetime.now().strftime("%H:%M")

    filename = str(time).replace(":", "-") + "-note.txt"

    with open(filename, "w") as file:
        file.write(writes)

    path_1 = "E:\\JARVIS_AI\\Advanced Jarvis\\" + str(filename)

    path_2 = "E:\\JARVIS_AI\\DataBase\\NotePad\\" + str(filename)

    os.rename(path_1, path_2)

    os.startfile(path_2)


def CloseNotepad():
    os.system("TASK-KILL /F /im Notepad.exe")
