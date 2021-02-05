# question to athena and answers have been added

import speech_recognition as sr
import wolframalpha
import wikipedia
import requests
import webbrowser
import time
import pyttsx3
import http.client as hype


appId = ''  # get the wolfram alpha app id


class Virtual:

    client = wolframalpha.Client(appId)
    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')  # getting details of current voice
    speaker.setProperty('voice', voices[1].id)
    rate = speaker.getProperty('rate')  # getting details of current speaking rate: 200
    speaker.setProperty('rate', 160)  # setting up new voice rate
    speech = sr.Recognizer()

    def __init__(self):
        self.result = ''
        self.question = ''
        self.loop = True


        """main thing begins here"""
        self.conn = hype.HTTPConnection("www.google.com", timeout=5)
        try:
            self.conn.request("HEAD", "/")
            self.conn.close()
            print("say 'end' to quit...")
            print('...')
            while self.loop:
                try:
                    with sr.Microphone() as source:
                        print('listening...')
                        Virtual.speech.adjust_for_ambient_noise(source)
                        audio = Virtual.speech.listen(source)
                        self.co = Virtual.speech.recognize_google(audio)
                        print(self.co)
                        if self.co == 'end':
                            self.loop = False
                            print('process has been ended')
                        else:
                            self.search(self.co)
                except:
                    print('didn\'t catch that, could you come again?')
        except:
            print('there is no internet connection')
            self.conn.close()

    def wolfram_search(self, variable):
        res = Virtual.client.query(variable)
        if res['@success'] == 'false':
            print('Question cannot be resolved... you are being redirected to google')
            time.sleep(5)
            webbrowser.open(f'http://google.com/search?q={variable}')  # Go to google.com
        else:
            # pod[0] is the question
            pod0 = res['pod'][0]
            # pod[1] may contain the answer
            pod1 = res['pod'][1]
            if (('definition' in pod1['@title'].lower()) or ('result' in pod1['@title'].lower()) or (
                    pod1.get('@primary', 'false') == 'true')):
                # extracting result from pod1
                result = self.fix_list(pod1['subpod'])
                self.play_n_print(result)
                question = self.fix_list(pod0['subpod'])
                question = self.remove_brackets(question)
                # self.primaryImage(question)
            else:
                # extracting wolfram question interpretation from pod0
                question = self.fix_list(pod0['subpod'])
                # removing unnecessary parenthesis
                question = self.remove_brackets(question)
                # searching for response from wikipedia
                self.wikipedia_search(question)
                # self.primaryImage(question)

    def wikipedia_search(self, variable):
        # running the query
        search_results = wikipedia.search(variable)
        # If there is no result, print no result
        if not search_results:
            print("No result from Wikipedia... you are being redirected to google")
            time.sleep(5)
            webbrowser.open(f'http://google.com/search?q={variable}')  # Go to google.com
        # Search for page... try block
        try:
            page = wikipedia.page(search_results[0])
        except (wikipedia.DisambiguationError, error):
            page = wikipedia.page(error.options[0])

        wiki_title = str(page.title.encode('utf-8'))
        # wiki_summary = str(page.summary.encode('utf-8'))
        # print(wiki_summary)
        wiki_2 = str(page.summary)
        self.play_n_print(wiki_2)

    def remove_brackets(self, variable):
        return variable.split('(')[0]

    def fix_list(self, variable):
        if isinstance(variable, list):
            return variable[0]['plaintext']
        else:
            return variable['plaintext']

    def play_sound(self, variable):
        Virtual.speaker.say(variable)
        Virtual.speaker.runAndWait()
        Virtual.speaker.stop()

    def primaryImage(self, variable):
        url = 'http://en.wikipedia.org/w/api.php'
        data = {'action': 'query', 'prop': 'pageimages', 'format': 'json', 'piprop': 'original', 'titles': variable}
        try:
            res = requests.get(url, params=data)
            key = res.json()['query']['pages'].keys()
            for i in key:
                keys = i
            if keys == "-1":
                pass
            else:
                imageUrl = res.json()['query']['pages'][keys]['original']['source']
                print(imageUrl)
        except:
            print('there was an exception processing the image')

    def play_n_print(self, variable):
        statement_1 = variable
        print(statement_1)
        self.play_sound(statement_1)

    def search(self, variable):
        if variable == "what is your name":
            self.play_n_print('My name is Athena, thanks for asking.')
        elif variable == "what would you like to call yourself":
            self.play_n_print('I would like to be called "The greatest dopest finest virtual beauty there is" but'
                              ' Lord psarris says its too much')
        elif variable == "when were you created":
            self.play_n_print('I have no idea. You can ask Lord psarris about that.')
        elif variable == "who is lord psarris":
            self.play_n_print('Lord is my creator, he\'s a really awesome guy')
        elif variable == "who is jesus":
            self.play_n_print('Jesus is the Son of God, who died to redeem us from the curse of the law.')
        elif variable == "thank you":
            self.play_n_print('you are welcome.')
            self.loop = False
        elif variable == "thank you that will be all":
            self.play_n_print('you are welcome.')
            self.loop = False
        else:
            self.wolfram_search(variable)



if __name__ == "__main__":
    Virtual()
