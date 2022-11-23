from django.forms import ModelForm
from app.models import Livros

# Create the form class.
class LivrosForm(ModelForm):
  class Meta:
    model = Livros
    fields = ['livro', 'autor', 'editora', 'ano']