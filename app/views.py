from django.shortcuts import render, redirect
from app.forms import LivrosForm
from app.models import Livros
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
  return render(request, 'home.html')

def list(request):
  data = {}
  search = request.GET.get('search')
  if search:
    data['db'] = Livros.objects.filter(livro__icontains=search)
  else:
    data['db'] = Livros.objects.all()
    
  all = Livros.objects.all()
  paginator = Paginator(all, 2)
  pages = request.GET.get('page')
  data['db'] = paginator.get_page(pages)
  return render(request, 'index.html', data)

def createUser(request):
  return render(request, 'createUser.html')

def store(request):
  data = {}
  if(request.POST['password']) != request.POST['password-conf']:
    data['msg'] = 'Senha e confirmação de senha diferentes!'
    data['class'] = 'alert-danger'
  else:
    user = User.objects.create_user(request.POST['user'], request.POST['email'], request.POST['password'])
    user.first_name = request.POST['name']
    user.save()
    data['msg'] = 'Usuário cadastrado com sucesso!'
    data['class'] = 'alert-success'
  return render(request, 'createUser.html', data)

def painel(request):
  return render(request, 'painel.html')

def doLogin(request):
  data = {}
  user = authenticate(username=request.POST['user'], password=request.POST['password'])
  if user is not None:
    login(request, user)
    return redirect('/dashboard/')
  else:
    data['msg'] = 'Usuário ou senha inválidos!'
    data['class'] = 'alert-danger'
    return render(request, 'painel.html', data)

#Logout do sistema
def logouts(request):
  logout(request)
  return redirect('/painel/')

def painelChangePassword(request):
  return render(request, 'changePassword.html')

#Alterar a senha
def changePassword(request):
  user = User.objects.get(email=request.user.email)
  user.set_password(request.POST['newPassword'])
  user.save()
  logouts(request)
  return redirect('/painel/')

def form(request):
  data = {}
  data['form'] = LivrosForm()
  return render(request, 'form.html', data)

def create(request):
  form = LivrosForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect('list')

def view(request, pk):
  data = {}
  data['db'] = Livros.objects.get(pk=pk)
  return render(request, 'view.html', data)

def edit(request, pk):
  data = {}
  data['db'] = Livros.objects.get(pk=pk)
  data['form'] = LivrosForm(instance=data['db'])
  return render(request, 'form.html', data)

def update(request, pk):
  data = {}
  data['db'] = Livros.objects.get(pk=pk)
  form = LivrosForm(request.POST or None, instance=data['db'])
  if form.is_valid():
    form.save()
    return redirect('list')

def delete(request, pk):
  db = Livros.objects.get(pk=pk)
  db.delete()
  return redirect('list')
  
