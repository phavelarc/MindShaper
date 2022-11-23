from django.shortcuts import render
from app.forms import LivrosForm
# Create your views here.
def home(request):
  return render(request, 'index.html')

def form(request):
  data = {}
  data['form'] = LivrosForm()
  return render(request, 'form.html', data)
  
