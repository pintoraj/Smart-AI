import ctypes
import datetime
import os
import pickle
import shutil
import time
import webbrowser
import cv2
import mediapipe as mp
import numpy as np
import openai
import pyautogui
import pyjokes
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
import winshell
import wolframalpha
from bs4 import BeautifulSoup
import Automations
from Features import GoogleSearch

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)
openai.api_key = "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"


def Speak(audio):
    print(" ")
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()
    print(" ")


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        Speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        Speak("Good Afternoon Sir !")
    else:
        Speak("Good Evening Sir !")

    assname = ("Jarvis !!!")
    Speak("I am your Assistant" + " " + assname)


def Username():
    Speak("What should i call you sir")
    uname = TakeCommand()
    Speak("Welcome Mister" + " " + uname)
    columns = shutil.get_terminal_size().columns
    Speak("How can i Help you, Sir")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def TakeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        pyttsx3.speak("Jarvis Here")
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


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("AI Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from AI Speech Recognition service; {e}")


def Summary():
    filename = "input.wav"
    print("Say your question...")
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        source.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
    text = transcribe_audio_to_text(filename)
    if text:
        print(f"You: {text}")

        response = generate_response(text)
        print(f"Jarvis: {response}")
        speak_text(response)

    time.sleep(10)


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def TaskExe():
    print("Would you like to give input using Sign Recogntion '1' ")
    print("Would you like to give input using Voice Recognition AI '2' ")
    choice = input("Choose your Option or Exit?")
    if choice == '1':
        while True:
            model_dict = pickle.load(open('../sign-language-detector-python-master/model.p', 'rb'))
            model = model_dict['model']

            cap = cv2.VideoCapture(0)

            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles

            hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

            labels_dict = {
                0: 'Hey', 1: 'Hello Jarvis', 2: 'Where is ?', 3: 'Youtube search', 4: 'set Alarm',
                5: 'Whatsapp message',
                6: 'My Location', 7: 'Let me ask you a question', 8: 'Where is ', 9: 'write a note',
                10: 'call', 11: 'show chat', 12: 'who is ', 13: 'Google search', 14: 'Bye', 15: 'Activate the Bulb',
                16: 'How are you Jarvis', 17: 'GoodBye Jarvis', 18: 'Who is Jarvis',
                19: 'Corona Cases', 20: 'write a note', 21: '', 22: '', 23: '', 24: '', 25: '', 26: 'Exit', 27: 'Bye',
                28: 'go', 29: 'none',
            }

            predicted_char = ""

            while True:

                data_aux = []
                x_ = []
                y_ = []

                ret, frame = cap.read()

                if frame is None:
                    break
                else:
                    H, W, _ = frame.shape

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = hands.process(frame_rgb)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,  # image to draw
                            hand_landmarks,  # model output
                            mp_hands.HAND_CONNECTIONS,  # hand connections
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            x_.append(x)
                            y_.append(y)

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))

                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10

                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10

                    prediction = model.predict([np.asarray(data_aux)])

                    predicted_character = labels_dict[int(prediction[0])]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    predicted_char = predicted_character

                    cv2.imshow("Frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    print("Predicted word: ", "".join(predicted_char))
                    query = predicted_char.lower()
                    if 'google search' in query:
                        query = input("type keyword to search")
                        import Features
                        Features.searchGoogle(query)

                    elif 'youtube search' in query:
                        Query = query.replace("jarvis", "")
                        query = input("Enter what do you want to search? ")
                        from Features import YouTubeSearch
                        YouTubeSearch(query)

                        Automations.YouTubeAuto(query)

                    elif 'set alarm' in query:
                        import Alarm
                        Alarm.set_alarm()

                    elif 'download' in query:
                        from Features import DownloadYouTube
                        DownloadYouTube()

                    elif 'whatsapp message' or 'send whatsapp message to' or 'message ' or 'message to' in query:

                        name = query.replace("whatsapp message", "")
                        name = name.replace("send ", "")
                        name = name.replace("to ", "")
                        Name = str(name)
                        Speak(f"Whats The Message For {Name}")
                        MSG = input(" ")
                        from Automations import WhatsappMsg
                        WhatsappMsg(Name, MSG)

                    elif 'call' in query:
                        from Automations import WhatsappCall
                        name = query.replace("call ", "")
                        name = name.replace("jarvis ", "")
                        Name = input(" ")
                        WhatsappCall(Name)

                    elif 'show chat' in query:
                        Speak("With Whom ?")
                        name = input(" ")
                        from Automations import WhatsappChat
                        WhatsappChat(name)

                    elif 'who is' in query:
                        person = input('who is _____ ?')
                        info = wikipedia.summary(person, 1)
                        print(info)
                        pyttsx3.speak(info)

                    elif 'let me ask you a question' in query:
                        query = input("Enter the Qn")
                        if query:
                            print(f"You: {query}")

                            response = generate_response(query)
                            print(f"Jarvis: {response}")

                        time.sleep(10)

                    elif 'my location' in query:
                        from Features import My_Location
                        My_Location()

                    elif 'where is' in query:

                        from Automations import GoogleMaps
                        Place = input("Enter the District/State/Country")
                        Place = Place.replace("jarvis", "")
                        GoogleMaps(Place)


                    elif 'write a note' in query:
                        Speak("Tell Me The Query .")
                        Speak("I Am Ready To Write .")
                        write = input(" ")
                        filename = str(time).replace(":", "-") + "-note.txt"
                        with open(filename, "w") as file:
                            file.write(write)
                        path_1 = "E:\\JARVIS_AI\\Advanced Jarvis\\" + str(filename)

                        path_2 = "E:\\JARVIS_AI\\DataBase\\NotePad\\" + str(
                            filename)

                        os.rename(path_1, path_2)

                        os.startfile(path_2)

                    elif 'close notepad' in query:

                        from Automations import CloseNotepad

                        CloseNotepad()



                    elif 'activate the bulb' in query:

                        from DataBase.HomeAuto.SmartBulb import Activate

                        Activate()

                        Speak("Should I Start Or Close The Bulb ?")

                        step = TakeCommand()

                        if 'close' in step:

                            from DataBase.HomeAuto.SmartBulb import CloseLight

                            CloseLight()

                        elif 'start' in step:

                            from DataBase.HomeAuto.SmartBulb import StartLight

                            StartLight()

                    elif 'corona cases' in query:

                        from Features import CoronaVirus

                        Speak("Which Country's Information ?")

                        corona = input("Country:")

                        CoronaVirus(corona)

                    else:

                        from DataBase.ChatBot.ChatBot import ChatterBot

                        reply = ChatterBot(query)

                        Speak(reply)

                        if 'bye' in query:

                            break

                        elif 'exit' in query:

                            break

                        elif 'go' in query:

                            break
    elif choice == '2':
        wishMe()
        Username()
        while True:
            query = TakeCommand()
            if "jarvis" in query:
                wishMe()
                Speak("Jarvis in your service Mister")

            elif 'google search' in query:
                import Features
                Features.searchGoogle(query)

            elif 'youtube search' in query:
                Query = query.replace("jarvis", "")
                query = Query.replace("youtube search", "")
                from Features import YouTubeSearch
                YouTubeSearch(query)
                Automations.YouTubeAuto(query)

            elif 'wikipedia' or 'wikipedia search' in query:
                import Features
                Features.searchWikipedia(query)

            elif 'temperature in' in query:
                import Features
                Features.Weather(query)

            elif "weather" or 'weather in' in query:
                search = query
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                Speak(f"current{search} is {temp}")

            elif "the time" or "whats the time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M")
                Speak(f"Sir, the time is {strTime}")


            elif 'song please' in query or 'play some song' in query or 'could you play some song' in query:
                Speak('Sir what song should i play...')
                song = TakeCommand()
                webbrowser.open(f'https://open.spotify.com/search/{song}')
                time.sleep(13)
                pyautogui.click(x=793, y=298)
                Speak('Playing' + song)

            elif 'play' in query or 'can you play' in query or 'please play' in query:
                Speak("OK! here you go!!")
                query = query.replace("play", "")
                query = query.replace("could you play", "")
                query = query.replace("please play", "")
                webbrowser.open(f'https://open.spotify.com/search/{query}')
                time.sleep(13)
                pyautogui.click(x=793, y=298)
                print('Enjoy!')
                Speak("Enjoy Sir!!")

            elif 'set alarm' in query:
                import Alarm
                Alarm.set_alarm()

            elif 'download' in query:
                from Features import DownloadYouTube
                DownloadYouTube()

            elif 'whatsapp message' in query:

                name = query.replace("whatsapp message", "")
                name = name.replace("send ", "")
                name = name.replace("to ", "")
                Name = str(name)
                Speak(f"Whats The Message For {Name}")
                MSG = TakeCommand()
                from Automations import WhatsappMsg
                WhatsappMsg(Name, MSG)

            elif 'call' in query:
                from Automations import WhatsappCall
                name = query.replace("call ", "")
                name = name.replace("jarvis ", "")
                Name = str(name)
                WhatsappCall(Name)

            elif 'show chat' in query:
                Speak("With Whom ?")
                name = TakeCommand()
                print(name)
                from Automations import WhatsappChat
                WhatsappChat(name)

            elif 'who is' in query:
                person = query.replace('who is', '')
                info = wikipedia.summary(person, 1)
                print(info)
                pyttsx3.speak(info)

            elif 'let me ask you a question' in query:
                Summary()

            elif 'my location' in query:
                from Features import My_Location
                My_Location()

            elif 'where is' in query:

                from Automations import GoogleMaps
                Place = query.replace("where is ", "")
                Place = Place.replace("jarvis", "")
                GoogleMaps(Place)



            elif 'write a note' in query:
                from Automations import Notepad
                Notepad()

            elif 'close notepad' in query:

                from Automations import CloseNotepad

                CloseNotepad()

            elif 'joke' in query:
                Speak(pyjokes.get_joke())

            elif "calculate" in query:

                app_id = " A4QTV6-22557QHK8K"
                client = wolframalpha.Client(app_id)
                indx = query.lower().split().index('calculate')
                query = query.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                print("The answer is " + answer)
                Speak("The answer is " + answer)

            elif 'recycle bin' or 'clear recycle bin' or 'recycle the recycle bin' in query:
                Speak("Hold on a Second ! Your Recycle bin is goin to be Recycled")
                try:
                    bin = winshell.recycle_bin()
                    bin.empty(confirm=False, show_progress=True, sound=True)
                    Speak('Recycle Bin is Cleared')
                except:
                    print("Recycle bin is Already Clear")
                    Speak("Recycle bin is Already Clear")

            elif 'system lock' or 'lock system' or 'lock the system' or 'sleep mode' or 'system sleep' in query:
                Speak("locking the device")
                ctypes.windll.user32.LockWorkStation()

            elif 'system shutdown' or 'shutdown' or 'shutdown system' in query:
                print("Do you really want to force shutdown your system? say yes or no")
                Speak("Do you really want to force shutdown your system? say yes or no")
                choice = TakeCommand()
                choice = choice.lower()
                if 'yes' in choice:
                    Speak("Hold On a Sec ! Your system is on its way to shut down")
                    os.system("shutdown /s /t 1")
                elif 'no' in choice:
                    pass

            elif 'activate the bulb' in query:

                from DataBase.HomeAuto.SmartBulb import Activate

                Activate()

                Speak("Should I Start Or Close The Bulb ?")

                step = TakeCommand()

                if 'close' in step:

                    from DataBase.HomeAuto.SmartBulb import CloseLight

                    CloseLight()

                elif 'start' in step:

                    from DataBase.HomeAuto.SmartBulb import StartLight

                    StartLight()

            elif 'corona cases' in query:

                from Features import CoronaVirus

                Speak("Which Country's Information ?")

                corona = TakeCommand()

                CoronaVirus(corona)

            else:

                from DataBase.ChatBot.ChatBot import ChatterBot

                reply = ChatterBot(query)

                Speak(reply)

                if 'bye' in query:
                    break

                elif 'exit' in query:
                    break

                elif 'go' in query:
                    break


TaskExe()
