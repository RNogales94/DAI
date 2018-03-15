from django.shortcuts import render, HttpResponse
from .models import *
import json

# Create your views here.

def index(request):
    return render(request, 'restaurants_table.html')

def  test_template(request):
   iterador = restaurantes.find().limit(10)
   context = {
      "lista": list(iterador)
   }
   return render(request, 'test.html', context)

def void(key):
    a = []
    return json.dumps(a)


#nota: page es "" cuando accedemos sin especificar la pagina mediante la api
#nota: la primera pagina es page=0
def query(request, key, value, page):
    #Control de errores
    if page=="":
        page = 0
    page = int(page)
    if page < 0:
        page = 0

    #Logica de la aplicacion
    result = find_restaurant(key, value, page)
    myjson = [{"name":row["name"], "street":row["address"]["street"] + " " + row["address"]["building"], "borough":row["borough"],  "cuisine":row["cuisine"]} for row in result]
    myjson = json.dumps(myjson)
    return HttpResponse(myjson, content_type='application/json')
