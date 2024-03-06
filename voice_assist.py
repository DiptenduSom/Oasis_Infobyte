# Libraries to be installed
# pip install logging-config
# pip install pyttsx3
# pip install speech_recognition
# pip install datetime
# pip install pyowm
# pip install webbrowser
# pip install os
# pip install smtplib
# pip install pyjokes
# pip install pywhatkit
# pip install pyjokes
# pip install wikipedia


# Importing the libraries installed
from logging.config import listen
import pyttsx3 as p  # for the pythong text to speech
import speech_recognition as sr  # for giving voice commands to the assistant
import datetime as dt  # formal way of greeting
import pyowm as OWM  # weather api for accessing the weather data
import webbrowser as wb  # for the browser access
import os as os  # operating system related functions and establishing connection between them
import smtplib as smtp  # for sending emails
import pyjokes  # for a little sense of humour
import pywhatkit  # for establishing the usage of the browser
import wikipedia  # for information about a certain topic


sound = p.init("sapi5")
voices = sound.getProperty("voices")
sound.setProperty("voice", voices[1].id)


# define the audio
def speak(audio):
    sound.say(audio)
    sound.runAndWait()


# define greetings (goodmorning/goodafternoon/goodevening/goodnight according to time)
def greeting():
    hour = int(dt.datetime.now().hour)
    if 0 <= hour < 12:
        speak(" Good  Morning!  Sir")
    elif 12 <= hour < 18:
        speak(" Good  Afternoon!  Sir")
    elif 18 <= hour < 22:
        speak(" Good  Evening  Sir")
    else:
        speak("Good Night!  Sir")

    speak(" I  am  Spark ! How  may  I  help  You ?")


# define command to assitance
def command():

    mic = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        mic.pause_threshold = 1
        audio = mic.listen(source)

    try:
        print("Identifying...")
        question = mic.recognize_google(audio, language="en-in")
        print(f"user said: {question}\n")

    except Exception as e:
        print(" Can  you  Repeat  i  could  not  get")
        speak(
            " Can  you  Repeat?  i  could  not  get  other  wise  please  try  again  later."
        )
        return "none"
    return question


# function for getting information about the weather
def get_weather(city):
    owm = OWM("your_openweathermap_api_key")
    wethermanger = owm.weather_manager()
    observation = wethermanger.weather_at_place(city)
    w = observation.weather
    temperature = w.temperature("celsius")["temp"]
    status = w.status
    speak(f"The weather in {city} is")
    speak(status)
    speak(f" with a temperature of {temperature} degrees Celsius.")


# for sending of the emails by the assistance
def send_email(to, subject, body):
    msg = smtp.SMTP("smtp.gmail.com", 587)
    msg.ehlo()
    msg.starttls()
    msg.login("your_email@gmail.com", "your_password")
    message = f"subject: {subject}\n\n{body}"
    msg.sendmail("your_email@gmail.com", to, message)
    msg.quit()
    speak("Email sent Successfully.")


# main control of the commands
if __name__ == "__main__":
    greeting()
    while True:
        question = command().lower()

        # executing task base on command

        if "hello" in question:
            speak(" Hi There, How i can help you?")

        elif "youtube" in question:
            if "play" in command:
                song = command.replace("play", "")
                speak("playing" + song)
                pywhatkit.playonyt(song)
        elif "open google" in question:
            wb.open("google.com")
        elif "play song" in question:
            sound_dir = "C:\\Users\\singh\OneDrive\\Documents\\Voice Assistant"
            song = [
                file for file in os.listdir(sound_dir) if file.lower().endswith(".mp3")
            ]
            if song:
                print(f"Playing: {song[0]}")
                os.startfile(os.path.join(sound_dir, song[0]))
            else:
                print("No MP3 files found in the specified directory.")
        elif "get time" in question:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The Current Time is {strTime}")
        elif "get date" in question:
            strdate = dt.datetime.now().strftime("%Y-%m-%d")
            speak(f"The Current Time is {strdate}")
        elif "joke" in command:
            speak(pyjokes.get_joke())
        elif "tell me something about" in command:
            person = command.replace("tell me something about", "")
            info = wikipedia.summary(person, 5)
            print(info)
            speak(info)
        elif "email" in question:
            speak("To whom do you want to send a mail")
            recipient = listen()
            speak("what should be the subject of mail")
            email_subject = listen()
            speak("please dictate the body of the email.")
            email_body = listen()
            send_email(recipient, email_subject, email_body)
        elif "weather" in question:
            speak("Sure which city would you like to check the weather for")
            city = listen()
            if city:
                get_weather(city)
        elif "exit" or "bye" in question:
            speak("Goodbye! Have a great day.")
            quit()
