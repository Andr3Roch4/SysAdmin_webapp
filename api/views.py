from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def listar(request):
    return JsonResponse([{"ola":[1,2,3]}, {"adeus":2}], safe=False)