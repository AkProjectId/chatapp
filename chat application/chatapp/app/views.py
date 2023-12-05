from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from app.models import Room,Message
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

# Create your views here.
def loginPage(request):
     if request.method == "POST":
       username = request.POST['Uname']
       email = request.POST['email']
       password = request.POST['password']
       ConfirmPassword = request.POST['ConfirmPassword']
       if password == ConfirmPassword:
          if User.objects.filter(email=email).exists():
            messages.info(request, 'email already used')
            return redirect('alert')
          elif User.objects.filter(username=username).exists():
            messages.info(request, 'username already exist')
            return redirect('alert')
          else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save(); 
            return redirect('AccSucess')
       else:
        messages.info(request, 'password is wrong')
        return redirect('alert')    

     else:
        return render(request,"login.html")

def checklogin(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('AccSucess')  # Redirect to success page upon successful login
            else:
                return render(request, 'alert.html', {'error_message': 'Invalid username or password'})
        else:
            return render(request, 'alert.html', {'error_message': 'Username and password are required'})

    return render(request, 'sucess.html')     


def room(request, room):
   username = request.GET.get('username')
   room_details = Room.objects.get(name=room)
   return render(request, "room.html", {
    'room_details': room_details,
    'username': username,
    'room': room
   })

def alert(request):
    return render(request,"alert.html")

def checkroom(request):
    if request.method == 'POST':
        room = request.POST['chatroom']
        username = request.POST['username']

        if Room.objects.filter(name=room).exists():
            return redirect('/' + room + '/?username=' + username)
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect('/' + room + '/?username=' + username)
    else:
        return HttpResponse("Invalid request method")

from django.http import HttpResponse, HttpResponseBadRequest
from .models import Room

def send(request):
        message = request.POST['message']
        username = request.POST['username']
        room_id = request.POST['room_id']

        #import pdb; pdb.set_trace()

        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        return HttpResponse('success')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
  

 


