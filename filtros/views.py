from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import cv2
import numpy as np
from django.http import HttpResponse

def index(request):
   return render(request, 'filtros/index.html')

def filtro_bn(imagen):
  """Convierte la imagen a escala de grises."""
  imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
  return imagen_gris

def filtro_sepia(imagen):
  """Aplica un filtro sepia a la imagen."""
  kernel_sepia = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.439, 0.577, 0.380]])
  imagen_sepia = cv2.transform(np.array(imagen), kernel_sepia)
  return imagen_sepia

def filtro_invertido(imagen):
  """Invierte los colores de la imagen."""
  imagen_invertida = 255 - imagen
  return imagen_invertida

def aplicar_filtro(request):
  print(request)
  if (request.method == 'POST'):
    filtro = request.POST.get('filtro')
    imagen = request.FILES.get('image')

    imagen_np = np.asarray(bytearray(imagen.read()), dtype=np.uint8)
    imagen_cv2 = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

    # Aplicar el filtro seleccionado
    if filtro == 'bn':
      imagen_filtrada = filtro_bn(imagen_cv2)
    elif filtro == 'sepia':
      imagen_filtrada = filtro_sepia(imagen_cv2)
    elif filtro == 'invertido':
      imagen_filtrada = filtro_invertido(imagen_cv2)
    else:
      return HttpResponseBadRequest("Filtro no válido")


    # Convertir el array de NumPy a una imagen
    imagen_filtrada = cv2.imencode('.jpg', imagen_filtrada)[1].tobytes()

    return HttpResponse(content_type='image/jpg', content=imagen_filtrada)
