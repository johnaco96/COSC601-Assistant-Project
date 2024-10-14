import os
import openai
import pyttsx3
import sys
import io
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
from gtts import gTTS
from deep_translator import GoogleTranslator
from imdb import Cinemagoer
import requests
import pyjokes
import assist  




engine = pyttsx3.init()


def speak(audio):
    print(f"Speaking: {audio}")  
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")
    else:
        speak("Good Evening Sir !")
    assname = "Assistant 1 point o"
    speak("I am your Assistant")
    speak(assname)

def username():
    speak("Welcome")
    # uname = takeCommand()
    # if uname == "None":
    #     uname = "User"  # Default name if none detected
    # speak("Welcome")
    # speak(uname)
    # print("#####################")
    print(f"Welcome")
    print("#####################")
    speak("How can I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"
    return query

def list_projects():
    projects_folder = os.path.expanduser("~/Documents/Projects")
    if os.path.exists(projects_folder):
        projects = os.listdir(projects_folder)
        if projects:
            return "You are currently working on the following projects: " + ", ".join(projects)
        else:
            return "Your projects folder is empty."
    else:
        return "Projects folder not found."

def list_files_in_folder(folder_name, search_directory="~/Documents/Projects"):
    search_directory = os.path.expanduser(search_directory)
    folder_path = os.path.join(search_directory, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        if files:
            return f"The following files are in the {folder_name} folder: " + ", ".join(files)
        else:
            return f"The {folder_name} folder is empty."
    else:
        return f"Folder {folder_name} not found."

def find_file(filename, search_directory="~/Documents/Projects"):
    search_directory = os.path.expanduser(search_directory)
    for root, dirs, files in os.walk(search_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def debug_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        compile(content, file_path, 'exec')
        return f"No syntax errors found in {file_path}."
    except SyntaxError as e:
        return f"Syntax error in {file_path}: {e}"
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def ask_question_memory(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant named Assistant. You are to provide help as best you can. Be funny and witty. Keep it brief and serious. Be a little sassy in your responses."},
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def TTS(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def analyze_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant named Assistant. You are to provide help as best you can. Be funny and witty. Keep it brief and serious. Be a little sassy in your responses."},
                {"role": "user", "content": f"Analyze the following file content:\n{content}"}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error analyzing {file_path}: {e}"

def generate_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant named Assistant. You are to provide help as best you can. Be funny and witty. Keep it brief and serious. Be a little sassy in your responses."},
            {"role": "user", "content": f"Write a Python function to {prompt}"}
        ]
    )
    code = response['choices'][0]['message']['content'].strip()
    return code

def save_code(file_path, code):
    try:
        with open(file_path, 'w') as file:
            file.write(code)
        return f"Code saved to {file_path}"
    except Exception as e:
        return f"Error saving code to {file_path}: {e}"

def debug_and_fix_code(code):
    try:
        compile(code, '<string>', 'exec')
        return "Code has no syntax errors."
    except SyntaxError as e:
        prompt = f"Fix the following Python code to remove syntax errors:\n{code}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant named Assistant. You are to provide help as best you can. Be funny and witty. Keep it brief and serious. Be a little sassy in your responses."},
                {"role": "user", "content": prompt}
            ]
        )
        fixed_code = response['choices'][0]['message']['content'].strip()
        return fixed_code
    except Exception as e:
        return f"Error debugging code: {e}"

def execute_code(code):
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        exec(code)
        output = new_stdout.getvalue()
    except Exception as e:
        output = f"Error executing code: {e}"
    finally:
        sys.stdout = old_stdout

    return output

def parse_filename(command, keyword):
    return command.lower().replace(keyword, "").strip()

def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)

def tellTime():
    time = str(datetime.datetime.now())
    hour = time[11:13]
    min = time[14:16]
    speak("The time is " + hour + " Hours and " + min + " Minutes")

def Hello():
    speak("Hello sir, I am your desktop assistant. Tell me how may I help you.")

def web_search(query):
    if "open google" in query:
        speak("Opening Google")
        webbrowser.open("www.google.com")
    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("www.youtube.com")
    elif "open stackoverflow" in query:
        speak("Opening Stack Overflow")
        webbrowser.open("www.stackoverflow.com")
    elif "wikipedia" in query:
        speak("Checking Wikipedia")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=4)
        speak("According to Wikipedia")
        speak(result)
    else:
        speak("I can only open Google, YouTube, Stack Overflow, and Wikipedia right now.")

def translate_speech():
    recog1 = sr.Recognizer()
    mc = sr.Microphone()

    with mc as source:
        print("Speak 'hello' to initiate the Translation!")
        recog1.adjust_for_ambient_noise(source, duration=0.2)
        audio = recog1.listen(source)
        MyText = recog1.recognize_google(audio)
        MyText = MyText.lower()

    if 'hello' in MyText:
        translator = GoogleTranslator(source='auto', target='hi')

        with mc as source:
            print("Speak a sentence...")
            recog1.adjust_for_ambient_noise(source, duration=0.6)
            audio = recog1.listen(source)

            try:
                get_sentence = recog1.recognize_google(audio)
                print("Phrase to be Translated: " + get_sentence)
                text = translator.translate(get_sentence)
                speak = gTTS(text=text, lang='hi', slow=False)
                speak.save("captured_voice.mp3")
                os.system("start captured_voice.mp3")
            except sr.UnknownValueError:
                print("Unable to Understand the Input")
            except sr.RequestError as e:
                print(f"Unable to provide Required Output: {e}")

def search_movie():
    ia = Cinemagoer()
    text = takeCommand()

    movies = ia.search_movie(text)
    speak("Searching for " + text)
    if len(movies) == 0:
        speak("No result found")
    else:
        speak("I found these:")
        for movie in movies:
            title = movie['title']
            year = movie['year']
            speak(f'{title} - {year}')
            info = movie.getID()
            movie = ia.get_movie(info)
            title = movie['title']
            year = movie['year']
            rating = movie['rating']
            plot = movie['plot outline']

            if year < int(datetime.datetime.now().strftime("%Y")):
                speak(f'{title} was released in {year} has IMDB rating of {rating}. The plot summary of movie is {plot}')
                break
            else:
                speak(f'{title} will release in {year} has IMDB rating of {rating}. The plot summary of movie is {plot}')
                break

def tellJoke():
    joke = pyjokes.get_joke()
    TTS(joke)
    return joke

    

def process_command(current_text):
    prompt = parse_filename(current_text, "generate code to")  
    if "projects folder" in current_text.lower():
        return list_projects()
    elif "view" in current_text.lower() and "folder" in current_text.lower():
        folder_name = parse_filename(current_text, "view")
        return list_files_in_folder(folder_name)
    elif "debug file" in current_text.lower():
        filename = parse_filename(current_text, "debug file")
        file_path = find_file(filename)
        if file_path:
            return debug_file(file_path)
        else:
            return f"File {filename} not found."
    elif "read file" in current_text.lower():
        filename = parse_filename(current_text, "read file")
        file_path = find_file(filename)
        if file_path:
            return read_file(file_path)
        else:
            return f"File {filename} not found."
    elif "analyze file" in current_text.lower():
        filename = parse_filename(current_text, "analyze file")
        file_path = find_file(filename)
        if file_path:
            return analyze_file(file_path)
        else:
            return f"File {filename} not found."
    elif "generate code" in current_text.lower():
        prompt = parse_filename(current_text, "generate code to")
        code = generate_code(prompt)
        save_code("./generated_code.py", code)
        return "Code has been generated and saved to ./generated_code.py. What would you like me to do next?"
    elif "save code" in current_text.lower():
        filename = parse_filename(current_text, "save code to")
        code = generate_code(prompt)
        return save_code(filename, code)
    elif "debug code" in current_text.lower():
        code = generate_code(prompt)
        return debug_and_fix_code(code)
    elif "search" in current_text.lower():
        query = parse_filename(current_text, "search")
        web_search(query)
        return f"Searching for {query}"
    elif "translate" in current_text.lower():
        translate_speech()
        return "Translation complete."
    elif "movie" in current_text.lower():
        search_movie()
        return "Movie search complete."
    elif "time" in current_text.lower():
        tellTime()
        return "Told the time."
    elif "day" in current_text.lower():
        tellDay()
        return "Told the day."
    elif "hello" in current_text.lower():
        Hello()
        return "Greeted the user."
    elif "joke" in current_text.lower():
        return tellJoke()
    else:
        return ask_question_memory(current_text)



