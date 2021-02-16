import time

from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoConfig

from answer_per_question import answer_per_question
from deepmine import Deepmine
from aryana import aryana
from find_events_in_sentence import find_events_in_sentence
from nevisa import nevisa
from speechRec import google


class BOT:
    def __init__(self):
        self.modified = False

    def is_modified(self):
        return self.modified

    '''
    This method takes an string as input, the string contains the string of question.
    If you are using this method, we presume that you want to use nevisa and ariana.

    :Param Question : an string containing the question.

    : return : A dictionary containing the type of question, corresponding arguments, api_url and result.
    '''

    def AIBOT(self, Question):
        start = time.time()
        answer = {'type': [], 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [],
                  'event': [], 'api_url': [], 'result': []}
        answer_set = {'type': set(), 'city': set(), 'date': set(),
                      'time': set(), 'religious_time': set(), 'calendar_type': set(),
                      'event': set(), 'api_url': set(), 'result': []}

        from find_time import reformat_date_time
        Question = reformat_date_time(Question)

        # /var/www/AIBot/media/bert-base-parsbert-ner-uncased
        tokenizer = AutoTokenizer.from_pretrained("bert-base-parsbert-ner-uncased")
        model = AutoModelForTokenClassification.from_pretrained("bert-base-parsbert-ner-uncased")
        events, event_keys = find_events_in_sentence(Question)
        Questions = Question.split(' . ')  # TODO
        for sentence in Questions:
            q_answer = answer_per_question(sentence, model, tokenizer, events, event_keys)

            for key in answer_set.keys():
                if key == "type":
                    answer_set[key].add(q_answer[key])
                elif key == "result":
                    if not q_answer[key] == "":
                        answer_set[key].append(q_answer[key])
                else:
                    answer_set[key].update(q_answer[key])
        for key in answer.keys():
            answer[key] = list(answer_set[key])
        return answer

    '''
    This method takes an string as input, the string contains the address of .wav file.

    :Param Address : an string containing the path of .wav file.

    : return : A dictionary containing the type of question, corresponding arguments, api_url and result.
    Also you should return your generated sentences as data stream. which mean what aryana returns.
    '''

    def aibot(self, Address):
        answer = {'type': [], 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [], 'event': [], 'api_url': [''], 'result': []}
        '''
        You should implement your code right here.
        '''

        start = time.time()

        file = open(Address, mode='rb')

        """ Google """
        text = google(file)

        """ Nevisa """
        # comment="0024399744"
        # text = nevisa(file,comment)

        """ Deepmine """
        # #Create instance Deepmine()
        # m = Deepmine()
        # # get text of your file! return status,text: if status==0 error occured.
        # status,text = m.get_text(Address)

        print("Text::", text)

        end = time.time()
        print(f"Runtime of the speechRecognition API is {end - start}")

        answer = self.AIBOT(text)

        start = time.time()

        generated_sentence = "این یک جمله‌ای صرفا برای امتحان کردن است"
        response = aryana(generated_sentence)

        end = time.time()
        print(f"Runtime of the text-to-speech API is {end - start}")

        with open("response.wav", mode='bw') as f:
            f.write(response.content)

        return answer, response
