from django.shortcuts import render
#from blog.models import posts

# Create your views here.
 
def home(request):
    return render(request, 'index.html')