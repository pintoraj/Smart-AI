import datetime
import time
import os
import speech_recognition as sr

def set_alarm():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak the time for the alarm in HH:MM format: ")
        audio = r.listen(source)

    try:
        # convert the user input into datetime format
        alarm_time = datetime.datetime.strptime(r.recognize_google(audio), "%H:%M").time()
        # get the current time
        current_time = datetime.datetime.now().time()
        # calculate the time delta between the current time and the alarm time
        time_delta = datetime.datetime.combine(datetime.date.today(), alarm_time) - datetime.datetime.combine(datetime.date.today(), current_time)
        if time_delta.total_seconds() < 0:
            # if the alarm time is in the past, add 1 day to the alarm time
            alarm_time = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(days=1)).time()
            time_delta = datetime.datetime.combine(datetime.date.today(), alarm_time) - datetime.datetime.combine(datetime.date.today(), current_time)
        # wait for the specified time
        print(f"Alarm set for {alarm_time.strftime('%I:%M %p')}.")
        import Main
        Main.TaskExe()
        print("Waiting for alarm...")
        time.sleep(time_delta.seconds)
        # play the alarm sound
        print("Alarm!")
        os.system("E:\\JARVIS_AI\\DataBase\\Sounds\\1.mp3")  # replace with the command to play the sound file

    except sr.UnknownValueError:
        print("Sorry, I could not understand your input.")
    except ValueError:
        print("Invalid time format. Please try again.")
