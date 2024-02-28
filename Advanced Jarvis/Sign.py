import os
import time
import webbrowser
from cgitb import reset
import cv2
import pyautogui
import pyttsx3
import speech_recognition as sr
from Features import GoogleSearch
import wikipedia
import openai
import Automations
import pickle
import cv2
import mediapipe as mp
import numpy as np
import spotipy
import spotipy.util as util

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
    global query
    while True:
            model_dict = pickle.load(open('../sign-language-detector-python-master/model.p', 'rb'))
            model = model_dict['model']

            cap = cv2.VideoCapture(0)

            cap = cv2.VideoCapture(0)
            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles

            hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

            predicted_char = ""

            while True:
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

                    data_aux = []
                    x_ = []
                    y_ = []

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

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    roi = frame[y1:y2, x1:x2]

                    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
                    _, threshold = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    cnt = max(contours, key=lambda x: cv2.contourArea(x))

                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 0)
                    sign_img = threshold[y:y + h, x:x + w]

                    sign_img = cv2.resize(sign_img, (128, 128))
                    sign_img = np.array(sign_img)
                    sign_img = sign_img.reshape(-1, sign_img.shape[0] * sign_img.shape[1])

                    prediction = model.predict(sign_img)
                    predicted_char = labels_dict[prediction[0]]

                cv2.putText(frame, predicted_char, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                cv2.imshow("Output", frame)

                if cv2.waitKey(1) == ord("q"):
                    break
                    cap.release()
                    cv2.destroyAllWindows()
                    print("Predicted word: ", "".join(predicted_char))
                    query = predicted_char.lower()






                    if 'google search' in query:
                        query = input("type keyword to search")
                        GoogleSearch(query)

                    elif 'youtube search' in query:
                        Query = query.replace("jarvis", "")
                        query = input(" ")
                        from Features import YouTubeSearch
                        YouTubeSearch(query)

                        Automations.YouTubeAuto(query)

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


TaskExe()