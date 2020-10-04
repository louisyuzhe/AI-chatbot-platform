from django.shortcuts import render
from blog.models import posts
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot.models import Statement, Tag
from django.db.models import Count, Max, Sum
from chatterbot.trainers import ListTrainer #train chatbot on a custom list of statements
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.db.models.functions import TruncDay
from datetime import datetime

#Import for Django-tables and django-filter
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from blog.tables import StatementTable
from blog.filters import StatementFilter

# Create your views here.

"""
Instantiating a ChatBot Instance
"""
#chatbot will be set to read_only to avoid learning after training
# Train based on the english corpus
chatbot1 = ChatBot(name = 'chatbot1',
                  read_only = False,
                  logic_adapters = ["chatterbot.logic.BestMatch"],
                  storage_adapter = "chatterbot.storage.DjangoStorageAdapter")
                  #database_uri='mysql://root:G7h7y7%40%40@127.0.0.1:3306/firstblog')


def home(request):
    """
    content = {
        'title' : 'My First Post',
        'author' : 'Giles',
        'date' : '18th September 2011',
        'body' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam cursus tempus dui, ut vulputate nisl eleifend eget. Aenean justo felis, dapibus quis vulputate at, porta et dolor. Praesent enim libero, malesuada nec vestibulum vitae, fermentum nec ligula. Etiam eget convallis turpis. Donec non sem justo.',
    }
    """
    entries = posts.objects.all()[:10]
    return render(request, 'index.html', {'posts' : entries, 'title': 'Chatbot 1.0'})

def updates(request):
    """
    content = {
        'title' : 'My First Post',
        'author' : 'Giles',
        'date' : '18th September 2011',
        'body' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam cursus tempus dui, ut vulputate nisl eleifend eget. Aenean justo felis, dapibus quis vulputate at, porta et dolor. Praesent enim libero, malesuada nec vestibulum vitae, fermentum nec ligula. Etiam eget convallis turpis. Donec non sem justo.',
    }
    """
    entries = posts.objects.all()[:10]
    return render(request, 'updates.html', {'posts' : entries})


@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		message = data['message']

		chat_response = chatbot1.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)

def chatbot(request, template_name="chatbot.html"):
    context = {'title': 'Chatbot 1.0'}
    return render(request, template_name, context)

def dashboard(request, template_name="dashboard.html"):
    entries = Statement.objects.filter(conversation='')
    """
    q1 = Statement.objects.values("search_text").annotate(resp_freq=Count("search_text")).order_by('-resp_freq')
    print(q1)
    q2 = Statement.objects.values("in_response_to").annotate(Count("text")).order_by()
    print(q2)
    q3 = Statement.objects.values("text").annotate(Count("in_response_to")).order_by() #how many in_response_to per text
    print(q3)
    q4 = Statement.objects.values("in_response_to").annotate(resp_freq=Count("in_response_to")).order_by('-resp_freq')
    print(q4)
    """
    nonTrainingData = Statement.objects.filter(conversation='')
    q1 = nonTrainingData.values("in_response_to").annotate(count=Count("in_response_to"),date=TruncDay('created_at'))#.order_by('date')
    #print(q1.aggregate(Sum("count")))
    resp_count_dict={}
    for responses in q1:
        temp_key=responses['in_response_to']
        timeStamp = responses['date']
        date = timeStamp.strftime("%D")

        if(temp_key in resp_count_dict.keys()):
            resp_count_dict[temp_key].append([responses['count'], date])
        else:
            resp_count_dict.setdefault(temp_key, [])
            resp_count_dict[temp_key].append([responses['count'], date])
    #print(resp_count_dict['Hi'][0][1])
    resp_count_dict.pop(None)
    q4 = nonTrainingData.values("in_response_to").annotate(resp_freq=Count("in_response_to")).order_by('-resp_freq')[:10]

    #for Pie chart
    conversation_count = Statement.objects.values("conversation").annotate(conv_count=Count("conversation")).order_by('-conv_count')

    context = {'title': 'Chatbot 1.0', 'chatterbot_data' : entries, 'in_response_to_query':q4, 'resp_count_dict':resp_count_dict, 'conversation_count':conversation_count}
    return render(request, template_name, context)

@csrf_exempt
def training(request, template_name="training.html"):

    if request.method == 'POST':
        train_option = request.POST['train_option']
        result = trainer(int(train_option), request)
        return HttpResponse(result)
    else:
        corpusDict = retrieveCorpus()
        context = {'title': 'Chatbot 1.0', 'corpusDict':json.dumps(corpusDict)}
    return render(request, template_name, context)

def retrieveCorpus():
    import os
    root_dir = "train_data/chatterbot_corpus/data"
    corpus_list = {}
    for dir_, _, files in os.walk(root_dir):
        corpus_list[dir_.replace('\\','/').replace("train_data/chatterbot_corpus/data/", "")]=files
    del corpus_list["train_data/chatterbot_corpus/data"]
    return corpus_list

def trainer(train_option, data):
    if(train_option == 2):
        #instantiate a ChatterBotCorpusTrainer object with the chatbot as arg
        corpus_trainer = ChatterBotCorpusTrainer(chatbot1)
        #Train dataset (ChatterBot-Corpus)
        #corpus_trainer.train("train_data/chatterbot_corpus/data/english")
        moduleType = data.POST['corpusSpecific']
        if(moduleType=="all"):
            corpusDir = "train_data/chatterbot_corpus/data/"+data.POST['corpusFull']
            resultStatement = "Training of all corpora of the "+ data.POST['corpusFull'] +" module have been completed"
        else:
            corpusDir = "train_data/chatterbot_corpus/data/"+data.POST['corpusFull']+"/"+moduleType
            resultStatement = "Training of "+ moduleType.replace(".yml", "") +" corpus of the "+ data.POST['corpusFull'] +" module has been completed"
        corpus_trainer.train(corpusDir)

        return(resultStatement)


    elif(train_option == 3):
        manual_conversation = [
            data.POST['inResponseTo'],
            data.POST['responseText']
        ]

        #Initializing Trainer Object
        trainer = ListTrainer(chatbot1)

        #Training BankBot
        trainer.train(manual_conversation)
        return("Manual training has been completed")

class FilteredStatementView(ExportMixin, SingleTableMixin, FilterView):
    table_class = StatementTable
    model = Statement
    template_name = "bootstrap_template.html"

    filterset_class = StatementFilter

    export_formats = ("csv", "xls")
    def get_queryset(self):
        return super().get_queryset()

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}
