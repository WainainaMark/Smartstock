from django.shortcuts import render, HttpResponse

# Create your views here.
def backend(request):
    return render(request, HttpResponse("Hello World"))