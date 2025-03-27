from django.db import models

# Create your models here.

class Produto(models.Model):
    nome=models.CharField()