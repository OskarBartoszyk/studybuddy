import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Toplevel  # Import Toplevel for creating new windows
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import languages
import re
import webbrowser
import recording
text_content = ''

def speak(text):
    tts = gTTS(text=text, lang='en') #only english available
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def beep():
    os.system("cvlc --play-and-exit boop.mp3")

def function(output_text, lang):
    beep()
    recognizer = sr.Recognizer()
    while True:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Say something...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Capture the audio input from the microphone
            audio_data = recognizer.listen(source)

        print("Recognizing...")
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio_data, language=lang)
        print("You said:", text)
        output_text.insert(tk.END, text + "\n")  # Update the output text in the GUI
        output_text.see(tk.END)  # Scroll to the end of the text widget
        if text == "stop recording":
            print("Stopped")
            break

def start_listening(output_text, lang):
    thread = threading.Thread(target=lambda: function(output_text, lang))
    thread.start()

def submit_lang():
    language_selected = listbox.get(listbox.curselection())
    lang_code = languages.languages[language_selected]
    return lang_code

def important(text_content):
    folder_name = "important"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("Folder Created")
    else:
        print("Folder already exists")
    exclamation_mark = re.findall(r'!(.*?)!', text_content)
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd,folder_name))
    with open('test1.txt','a') as file:
        for words in exclamation_mark:
            file.write(words + '\n')
    file.close()

def callback(search_query):
    search_url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open_new(search_url)

def create_hlink(text_content):
    question_mark = re.findall(r'\?(.*?)\?', text_content)
    for item in question_mark:
        link = tk.Label(root, text=item, fg='blue', cursor='hand2')
        link.pack()
        # Bind the callback function with the specific search query
        link.bind("<Enter>", lambda e, query=item: callback(query))

def open_text_file():
    global text_content

    # file type
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    # show the open file dialog
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        # read the text file and show its content on the Text widget 
        with open(filename, 'r') as file:
            text_content = file.read()
            master.delete('1.0', tk.END)
            master.insert('1.0', text_content)
            create_hlink(text_content)

def save_file():
    global text_content 
    files = [('All Files', '*.*'),  
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt'),
             ('PDF Document', '*.pdf')] 
    filename = filedialog.asksaveasfilename(filetypes=files, defaultextension=".txt")
    if filename:
        text_content = output_text.get("1.0", tk.END)  # Get the content of the output_text widget
        with open(filename, 'w') as file:
            file.write(text_content)
        important(text_content)
        create_hlink(text_content)

def update_function():
    # Define the functionality for the update button here
    pass

# Create main window
root = tk.Tk()
root.title("studybuddy")

open_file_button =  tk.Button(root, text='Open File')
open_file_button.pack(anchor=tk.NW)

def open_new_window(event):
    NewWindow(master)

open_file_button.bind("<Button-1>", open_new_window)

listbox = tk.Listbox(root)
listbox.pack()

for language in languages.languages.keys(): 
    listbox.insert(tk.END, language)

submit_button = tk.Button(root, text="submit", command=submit_lang)
submit_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack(fill=tk.X,ipady=80)

start_button = tk.Button(root, text="Start Listening", command=lambda: start_listening(output_text, submit_lang()))
start_button.pack()

save_button = tk.Button(root, text='Save',command=save_file)
save_button.pack()

update_button =  tk.Button(root, text='Update',command=update_function)
update_button.pack()

read_button = tk.Button(root, text="Read", command=lambda: speak(text_content))
read_button.pack()

audio_button = tk.Button(root, text="Audio", command=recording.start_audio())
audio_button.pack()
root.mainloop()



if __name__== "__main__":
    recording.start_audio()
