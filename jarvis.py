import speech_recognition as sr
import os
import webbrowser
import openai
import win32com.client
import datetime

speaker = win32com.client.Dispatch('SAPI.SpVoice')

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    chatStr += f"Probal: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    speaker.Speak(f'{text}')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"
        
def site(query):
    req = query.split()
    say(f"Opening {req[1]}...")
    webbrowser.open(f"https://{req[1].lower()}")
    
def start(query):
    req = query.split()
    say(f'Opening {req[1]}...')
    os.system(f"start {req[1]}")

if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        # sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        # for site in sites:
        #     if f"Open {site[0]}".lower() in query.lower():
        #         say(f"Opening {site[0]} sir...")
        #         webbrowser.open(site[1])
       

        if "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {time}")

        elif "website".lower() in query.lower():
            site(query)

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "open".lower() in query.lower():
            start(query)

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
