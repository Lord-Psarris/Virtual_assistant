"""
prompts before redirecting to google
can open apps from the search menu
"""

# imports
import speech_recognition as sr
import wolframalpha
import wikipedia
import requests
import webbrowser
import time
import pyttsx3
import http.client as http
import pyautogui

# necessities
appId = ''  # get the wolfram alpha app id
client = wolframalpha.Client(appId)
speaker = pyttsx3.init()
voices = speaker.getProperty('voices')  # getting details of current voice
speaker.setProperty('voice', voices[1].id)
rate = speaker.getProperty('rate')  # getting details of current speaking rate: 200
speaker.setProperty('rate', 170)  # setting up new voice rate
speech = sr.Recognizer()

print('checking connection...\n')


def prompt(param):
    print('we could not find an answer to your question \n do you want to be redirected to google?')
    loop = True
    while loop:
        ask = input('y/n ')
        if ask == 'Y' or ask == 'y':
            print('you are being redirected')
            time.sleep(3)
            webbrowser.open(f'https://google.com/search?q={param}')
            loop = False
        elif ask == 'N' or ask == 'n':
            print('okay')
            loop = False
            return None
        else:
            print('Wrong input')
            continue


def search(param):
    pyautogui.hotkey('win', 's')
    pyautogui.typewrite(param, interval=0.5)
    pyautogui.typewrite(['enter'])


# main class
class Main:

    def __init__(self):
        self.loop = True

        """main thing begins here"""
        self.connection = http.HTTPConnection("www.google.com", timeout=5)
        try:
            self.connection.request("HEAD", "/")
            self.connection.close()
            print("say 'end' to quit...;\nto open a file or application, say 'open <filename>';\n"
                  "the listener only works for 5 seconds but it can be adjusted.")
            print('...')
            while self.loop:
                try:
                    print('listening...')
                    with sr.Microphone() as source:
                        speech.adjust_for_ambient_noise(source)
                        audio = speech.listen(source)
                        command = speech.recognize_google(audio)
                        print(command)
                        haystack = command
                        count = haystack.find('open')
                        if command == 'end':
                            self.loop = False
                            print('process has been ended')
                        elif count == 0:
                            param = command.replace('open ', '')
                            search(param)
                            print(f'opening {param}')
                            Play(f'opening {param}').__()
                            time.sleep(3)
                        else:
                            print('processing...')
                            answer = Personalised(command)
                            answer = answer.__()
                            if answer is None:
                                answer = Wolfram(command).__()
                                if answer is None:
                                    wiki = Wiki(command).__()
                                    if wiki is None:
                                        continue
                                    else:
                                        print(wiki)
                                        Play(wiki).__()

                                        print('inna')
                                else:
                                    print(answer)
                                    Play(answer).__()
                                    image = Image(command).__()
                                    if image is None:
                                        pass
                                    else:
                                        print(image)
                            else:
                                print(answer)
                                Play(answer).__()

                                # restart question
                        print('do you wanna go again? ')
                        loop = True
                        while loop:
                            question = input('y/n ')
                            if question == 'Y' or question == 'y':
                                loop = False
                                continue
                            elif question == 'N' or question == 'n':
                                print('thank you for your time')
                                loop = False
                                self.loop = False
                            else:
                                print('Wrong input')
                                continue
                except Exception as e:
                    if e:
                        print('didn\'t catch that, could you come again?, or the problem was ' + str(e))
                        time.sleep(1)
                    else:
                        print('didnt catch that... come again')
        except Exception as e:
            print('there is no internet connection, or ' + str(e))
            self.connection.close()


# other classes
class Wiki:

    def __init__(self, variable):
        self.variable = variable

    def __(self):

        results = wikipedia.search(self.variable)
        # If there is no result, print no result
        if not results:
            prompt(self.variable)
        try:
            page = wikipedia.page(results[0])
        except (wikipedia.DisambiguationError, error):
            page = wikipedia.page(error.options[0])

        wiki = str(page.summary)
        return wiki


class Wolfram:

    def __init__(self, variable):
        self.variable = variable

    def __(self):
        res = client.query(self.variable)
        if res['@success'] == 'false':
            prompt(self.variable)
        else:
            # pod[0] is the question
            # pod0 = res['pod'][0]
            # pod[1] may contain the answer
            pod1 = res['pod'][1]
            if (('definition' in pod1['@title'].lower()) or ('result' in pod1['@title'].lower()) or (
                    pod1.get('@primary', 'false') == 'true')):
                # extracting result from pod1
                result = FixQuestion(pod1['subpod'])
                return result.fix()
            else:
                return None


class Image:

    def __init__(self, variable):
        self.variable = variable

    def __(self):
        url = 'http://en.wikipedia.org/w/api.php'
        data = {'action': 'query', 'prop': 'pageimages', 'format': 'json', 'piprop': 'original',
                'titles': self.variable}
        try:
            keys = ''
            res = requests.get(url, params=data)
            key = res.json()['query']['pages'].keys()
            for i in key:
                keys = i
            if keys == "-1":
                pass
            else:
                image_url = res.json()['query']['pages'][keys]['original']['source']
                return image_url
        except Exception as e:
            print('there was an exception processing the image ' + str(e))


class Personalised:

    def __init__(self, variable):
        self.variable = variable

    def __(self):
        if self.variable == "what is your name":
            return 'My name is Athena, thanks for asking.'
        elif self.variable == "what would you like to call yourself":
            return 'I would like to be called "The greatest dopest finest virtual beauty there is" but' \
                   ' Lord psarris says its too much'
        elif self.variable == "when were you created":
            return 'I have no idea. You can ask Lord psarris about that.'
        elif self.variable == "who is lord psarris":
            return 'Lord is my creator, he\'s a really awesome guy'
        elif self.variable == "who is jesus":
            return 'Jesus is the Son of God, who died to redeem us from the curse of the law.'
        else:
            return None


# helper classes
class FixQuestion:

    def __init__(self, question):
        self.question = question

    def fix(self):
        if isinstance(self.question, list):
            return self.question[0]['plaintext']
        else:
            return self.question['plaintext']

    def fix_(self):
        tried = self.question.split('(')[0]
        return tried


class Play:
    def __init__(self, variable):
        self.variable = variable

    def __(self):
        speaker.say(self.variable)
        speaker.runAndWait()
        speaker.stop()


if __name__ == "__main__":
    Main()
