from django.db import models

# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    peso_carregamento = models.IntegerField()
    agua = models.IntegerField()
    luz = models.IntegerField()
    CO2 = models.IntegerField()
    cat = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Distribuidor(models.Model):
    nome = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    coefLuz = models.FloatField()

    # Calculo de coefs

    def __str__(self):
        return self.nome
    
class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    coefAgua = models.FloatField()
    coefLuz = models.FloatField()
    coefCO2 = models.FloatField()
    local = models.CharField(max_length=100)
    cat = models.CharField(max_length=50)

    # Calculo de coefs

    def __str__(self):
        return self.nome
    
class Transportador(models.Model):
    nome = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    coefLuz = models.FloatField()
    coefCO2 = models.FloatField()

    # calculo de coefs com min de 50km

    def __str__(self):
        return self.nome