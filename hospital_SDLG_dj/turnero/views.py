from django.shortcuts import render

# Create your views here.
def form_turnero(request):
    return render(request, 'formulario.html')

def loguin_turnero(request):
    return render(request, 'Login.html')

def signup_turnero(request):
    return render(request,'SignUp.html')