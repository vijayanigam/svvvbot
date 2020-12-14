from django.shortcuts import render
# from google.colab import files
from .models import msgs, reply
from django.http import HttpResponse, HttpResponseRedirect
import nltk
import random
import numpy as np
import string
from nltk.stem import WordNetLemmatizer
# from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Create your views here.
def index(request):
    # r = reply(reply="BOT: My name is Bot. I am your personel assistant. If you want to exit, type Bye!")
    # r.save()
    msgs.objects.all().delete()
    reply.objects.all().delete()
    return render(request, 'index.html')


def enter(request):
    a = open("svvvbot/static/svvvbot/admission.txt", "r", encoding="utf8")
    data = a.read()
    data.lower()
    nltk.download("punkt")
    nltk.download("wordnet")
    sent = nltk.sent_tokenize(data)
    word = nltk.word_tokenize(data)
    lem = nltk.stem.WordNetLemmatizer()

    def Lemmetizing(tokens):
        # print(lem.lemmatize(token) for token in tokens)
        return [lem.lemmatize(token) for token in tokens if not token in set(stopwords.words('english'))]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    # print(remove_punct_dict)
    def LemNormalize(text):
        # print(Lemmetizing(nltk.word_tokenize(text.lower().translate(remove_punct_dict))))
        return Lemmetizing(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
    INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
    RESPONSES = ["Hi", "Hiii", "Hey", "Hello", "Hey! How can i help you?", "hi there",
                 "I am glad! You are talking to me", "Greetings", "What's up"]
    endresponse = ["Bye", "Bye bye!", "See you later", "Goodbye", "Bbye,Have a nice day",
                   "Bye Take care!"]

    def greeting(sentence):
        for word in sentence.split():
            if word.lower() in INPUTS:
                return random.choice(RESPONSES)

    def ending(sentence):
        return random.choice(endresponse)

    def response(user_response):
        robo_response = ''
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
        # print(TfidfVec)
        tfidf = TfidfVec.fit_transform(sent)
        # print(tfidf)
        vals = cosine_similarity(tfidf[-1], tfidf)
        # print(vals)
        idx = vals.argsort()[0][-2]
        # print(idx)
        flat = vals.flatten()
        flat.sort()
        # print(flat)
        req_tfidf = flat[-2]
        if (req_tfidf == 0):
            robo_response = robo_response + "I am sorry!I don't understand you"
            return robo_response
        else:
            robo_response = robo_response + sent[idx]
            return robo_response

    valu = ""
    # data=['a']
    m3 = []
    flag = True
    d = False
    # print(d)
    print("BOT: My name is Bot. I am your personal assistant. If you want to exit, type Bye!")
    # params = {valu: "BOT: My name is Bot. I am your personal assistant. If you want to exit, type Bye!", flag: "flag"}
    # return render(request, "index.html", params)

    while (flag == True):
        user_response = str(request.POST.get('text1'))
        m = msgs(message=user_response)
        m.save()
        # removes all the punctuations and numbers
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
        no_punct = ""
        for char in user_response:
            if char not in punctuations:
                no_punct = no_punct + char
        user_response = no_punct
        user_response = user_response.lower()
        user = user_response.split()

        if user_response != 'bye' or "bye" not in user:
            if user_response == 'thanks' or "thanks" in user or "thankyou" in user or user_response == 'thank you':
                flag = False
                r = reply(reply=ending(user_response))
                r.save()
                m1 = msgs.objects.all()
                r1 = reply.objects.all()
                m2 = []
                for k in range(1, len(m1) + 1):
                    m2.append(msgs.objects.get(id=k))
                    m2.append(reply.objects.get(id=k))
                '''for n in range(0,len(m2)-1,2):
                    print("use: ",m2[n])
                    print("bot: ",m2[n+1])'''
                # print(m1)
                # print('mmmmmmmmmmmmmmm222222222222222222222222222222222')
                # print(m2)
                # print(m3)
                # print(data)
                params = {'d': d, 'valu': ending(user_response), 'flag': user_response, 'm1': m1, 'm2': m2, 'x': True,
                          'data': data}
                return render(request, "result.html", params)
                # return HttpResponse("BOT: " + ending(user_response))

            elif user_response == "how are you":

                r = reply(reply="I am fine! How may I help you?")
                r.save()
                # d = [0, 1]
                link=""
                m1 = msgs.objects.all()
                r1 = reply.objects.all()
                m2 = []
                # print('hjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
                # print(len(m1))
                # print(m1, r1)
                # print(msgs)
                # print(msgs.objects)
                # print(msgs.objects.get(id=0))
                # f={}
                for k in range(1, len(m1) + 1):
                    # print('in for      mnnnnnnnnnnnnnnnnnnnnnnnnn')
                    a = msgs.objects.get(id=k)

                    m2.append(a)
                    a = reply.objects.get(id=k)
                    m2.append(a)
                    # f[msgs.objects.get(id=k)]=reply.objects.get(id=k)
                    # m3.append(msgs.objects.get(id=k))
                # print(m1,m2,m3)
                # data = list(zip(m2, m3))
                params = {'d': d, 'valu': "I am fine! How may I help you?", 'flag': user_response, 'm1': m1, 'm2': m2,
                          'x': True, 'data': data}
                return render(request, "result.html", params)

                # return HttpResponse("BOT: I am fine! How may I help you?")
# response to how are you -------------------------------------------------------------------------
            elif user_response == "how you doing" or user_response == "how do you do":
                r = reply(reply="I am doing great.How may I help you?")
                r.save()
                m1 = msgs.objects.all()
                r1 = reply.objects.all()
                m2 = []
                # print(m1, r1)
                # d = [0, 1]

                for k in range(1, len(m1) + 1):
                    m2.append(msgs.objects.get(id=k))
                    m2.append(reply.objects.get(id=k))

                params = {'d': d, 'valu': "I am doing great.How may I help you?", 'flag': user_response, 'm1': m1,
                          'm2': m2,
                          'x': True, 'data': data}
                return render(request, "result.html", params)
                # return HttpResponse("BOT: I am doing great.How may I help you?")
# to return brochure --------- or fees ------------------------------------------------
            elif user_response == 'brochure' or "brochure" in user:
                #link="http://www.svvv.edu.in/uploaded_files/Information_Brochure21.04.2020.pdf "
                r = reply(reply="Click on the link below to download Brochure 👉")
                r.save()
                m1 = msgs.objects.all()
                r1 = reply.objects.all()
                m2 = []
                # print(m1, r1)
                # d = [0, 1]

                for k in range(1, len(m1) + 1):
                    m2.append(msgs.objects.get(id=k))
                    m2.append(reply.objects.get(id=k))
                    m3.append(msgs.objects.get(id=k))
                # data = list(zip(m2, m3))
                # print(data)
                params = {'d': True, 'valu': "click here", 'flag': user_response, 'm1': m1,
                          'm2': m2, 'x': True, 'data': data}

                return render(request, "result.html", params)
                # return HttpResponse("BOT: I am doing great.How may I help you?")
# calling greeting function ----------------------------------------------------------------------------------
            else:
                if greeting(user_response) is not None:
                    r = reply(reply=greeting(user_response)+"🖐")
                    r.save()
                    m1 = msgs.objects.all()
                    r1 = reply.objects.all()
                    m2 = []
                    m3 = []
                    # print(m1, r1)
                    # d = [0, 1]
                    for k in range(1, len(m1) + 1):
                        m2.append(msgs.objects.get(id=k))
                        m2.append(reply.objects.get(id=k))
                    # data=list(zip(m2,m3))
                    # print(data)
                    params = {'d': d, 'valu': greeting(user_response)+"🖐", 'flag': user_response,
                              'm1': m1, 'm2': m2, 'x': True, 'data': data}
                    return render(request, "result.html", params)
                    # return HttpResponse("BOT: " + greeting(user_response))
# getting response from response() ---------------------------------------------
                else:
                    sent.append(user_response)
                    word = word + nltk.word_tokenize(user_response)
                    final_words = list(set(word))
                    r = reply(reply=response(user_response))
                    r.save()
                    m1 = msgs.objects.all()
                    r1 = reply.objects.all()
                    m2 = []
                    # print(m1, r1)
                    # d = [0, 1]
                    for k in range(1, len(m1) + 1):
                        m2.append(msgs.objects.get(id=k))
                        m2.append(reply.objects.get(id=k))
                        #m3.append(msgs.objects.get(id=k))
                    # data = list(zip(m2, m3))
                    # print(data)
                    params = {'d': d, 'valu': response(user_response), 'flag': user_response, 'm1': m1, 'm2': m2,
                              'x': True, 'data': data}
                    return render(request, "result.html", params)
                    # return HttpResponse(response(user_response))
                    sent.remove(user_response)
# if bye ------------------------------------------------------------
        else:
            flag = False
            r = reply(reply="Bye!"+"😄")
            r.save()
            m1 = msgs.objects.all()
            r1 = reply.objects.all()
            m2 = []
            print(m1, r1)
            # d = [0, 1]
            for k in range(1, len(m1) + 1):
                m2.append(msgs.objects.get(id=k))
                m2.append(reply.objects.get(id=k))
                #m3.append(msgs.objects.get(id=k))

            # data = list(zip(m2, m3))
            # print(data)
            params = {'d': d, 'valu': " Bye!", 'flag': user_response, 'm1': m1, 'm2': m2, 'x': True, 'data': data}
            return render(request, "result.html", params)
            # return HttpResponse("BOT: Bye!")
