# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
import redis

try:
    # Se conecta a la base de datos 1 de Redis en localhost, puerto 6379 y decodifica las respuestas a strings.
    r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
    r.ping()  # Envía un PING para probar la conexión.
    print("Connected to Redis database 1")
except redis.ConnectionError as e:
    # Si ocurre un error de conexión, lo muestra.
    print(f"Redis connection error: {e}")


def get_client_ip(request):
    """
    Obtiene la IP del cliente.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registro de usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                
                # Guardar datos de sesión en Redis usando JSON.SET
                session_key = f"user:signup:{user.id}"
                session_data = {
                    "_auth_user_id": user.id,
                    "username": user.username,
                    "password": user.password,  # Nota: esta ya está hasheada
                    "start_date": datetime.utcnow().isoformat()
                }
                r.execute_command('HSET', session_key, '.', json.dumps(session_data))
                
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {'error': 'El usuario ya existe'})
        return render(request, 'signup.html', {'error': 'Las contraseñas no son iguales'})

@login_required
def signout(request):
    logout(request)
    return redirect('home')
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'error': 'Username or password incorrect'})
        else:
            login(request, user)
            
            # Definir la clave del hash en Redis (puedes definir el nombre que prefieras)
            session_key = f"user:signin:{user.id}:{request.session.session_key}"
            # Construir el diccionario con los valores
            session_data = {
                "_auth_user_id": str(user.id),     # Convertir a string para asegurar compatibilidad
                "username": user.username,
                "password": user.password,         # Esta contraseña ya viene hasheada
                "ip_address": get_client_ip(request),
                "last_activity": datetime.utcnow().isoformat(),
            }
            
            # Almacenar el hash en Redis
            r.execute_command('HSET', session_key, '.', json.dumps(session_data))
            
            return redirect('home')

