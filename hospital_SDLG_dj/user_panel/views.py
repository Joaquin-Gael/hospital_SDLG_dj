from django.shortcuts import render

# Create your views here.
def user_panel(request):
    return render(request,'panel.html')