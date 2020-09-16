from django.shortcuts import render
from blog.models import posts
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot

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
    return render(request, 'index.html', {'posts' : entries})

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
    context = {'title': 'Dashboard'}
    return render(request, template_name, context)