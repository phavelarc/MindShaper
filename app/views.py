from django.shortcuts import render, redirect, HttpResponseRedirect
from app.forms import LivrosForm
from app.models import Livros
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.connection.connection import connection
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
import MySQLdb
import json

# Home
def home(request):
  return render(request, 'home.html')

# Dashboard
def dashboard(request):
  data = {}
  search = request.GET.get('search')
  livros = []
  # profile_list = Livros.objects.get_queryset().order_by('id')
  if search:
    print('1')
    livros = Livros.objects.filter(livro__icontains=search)
  else:
    print('2')
    livros = Livros.objects.all().order_by('id')

  paginator = Paginator(livros, 10)
  pages = request.GET.get('page')
  data['db'] = paginator.get_page(pages)

  return render(request, 'index.html', data)

def createUser(request):
  return render(request, 'createUser.html')

# Criar Usuário
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

# Login
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

#Forms
def form(request):
  data = {}
  data['form'] = LivrosForm()
  return render(request, 'form.html', data)

#Criar um novo livro
def create(request):
  user = User.objects.get(id=request.user.id)
  if not user.has_perm('can_add_books'):
    return redirect('/dashboard/')

  form = LivrosForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect('dashboard')

#Visualizar detalher de um livro
def view(request, pk):
  data = {}
  data['db'] = Livros.objects.get(pk=pk)
  return render(request, 'view.html', data)

#Editar um livro
def edit(request, pk):
  data = {}
  data['db'] = Livros.objects.get(pk=pk)
  data['form'] = LivrosForm(instance=data['db'])
  user = User.objects.get(id=request.user.id)

  if not user.has_perm('app.can_edit_books'):
    return redirect('/dashboard/')

  print('aqui')
  return render(request, 'form.html', data)

def update(request, pk):
  data = {}
  data['db'] = Livros.objects.get(pk=pk)
  form = LivrosForm(request.POST or None, instance=data['db'])
  if form.is_valid():
    print('aqui2')
    form.save()
    return redirect('/dashboard/')

#Deletar um livro
def delete(request, pk):
  user = User.objects.get(id=request.user.id)
  if not user.has_perm('app.can_delete_books'):
    return redirect('/dashboard/')

  db = Livros.objects.get(pk=pk)
  db.delete()

  return redirect('dashboard')
  
#Exportar dados
def exportData(request):
  dbConnect = connection()
  cursor = dbConnect.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute("SELECT * FROM app_livros ORDER BY id")
  dbConnect.close()
  linhas = json.dumps(cursor.fetchall())
  print(linhas)
  response = HttpResponse(linhas)
  response['Content-Disposition'] = 'attachment; filename=livros.json'

  return response

#Importar dados
def importData(request):
  files = json.loads(request.FILES['file'].read())
  dbConnect = connection()
  cursor = dbConnect.cursor(MySQLdb.cursors.DictCursor)
  print(files)
  for file in files:
    cursor.execute(f""" INSERT INTO app_livros(livro, autor, editora, ano) VALUES('{file["livro"]}', '{file["editora"]}', '{file["autor"]}', '{file["ano"]}')""")
  dbConnect.close()

  return redirect('dashboard')

def about(request):
  return render(request, 'about.html')