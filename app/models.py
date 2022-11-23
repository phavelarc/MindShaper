from django.db import models

# Create your models here.
class Livros(models.Model):
  livro = models.CharField(max_length=150)
  autor = models.CharField(max_length=150)
  editora = models.CharField(max_length=100) 
  ano = models.IntegerField() 
  
  
