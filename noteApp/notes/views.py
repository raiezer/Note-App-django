import datetime

from django.shortcuts import render, redirect,HttpResponseRedirect
from django.http import HttpResponse
# Create your views here.
from django.template import loader
from .models import User_model,Note_model

def check_session(func):
    def wrapper(request):
        if request.session.has_key("username"):
            return func(request)
        else:
            return redirect("/notes/login-page/")
    return wrapper
def register(request):
    if request.method=='POST':
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["psw"]

        obj_model=User_model(username=username,email=email,password=password)
        obj_model.save()
        return redirect("/notes/login-page/")
    return render(request,"notes/registration_page.html",{'page':'register'})

def login(request):
    if request.method == 'POST':
        username=request.POST["username"]
        password=request.POST["psw"]
        obj_model=User_model.objects.filter(username=username,password=password)
        if (obj_model):
            print("hello")
            request.session["username"]=username
            return redirect("/notes/to-do/")
        else:
            print("incorrect username or password")
            return render(request, "notes/login_page.html", {'page': 'login','msg':'invalid'})
    return render(request, "notes/login_page.html", {'page': 'login'})

@check_session
def to_do(request):
    if request.method=='POST':
        notes=request.POST["notes"]
        date=datetime.datetime.now()
        user=User_model.objects.get(username=request.session["username"])
        obj_model=Note_model(notes=notes,date_time=date,user_id=user.id)
        obj_model.save()

    user = User_model.objects.get(username=request.session["username"])
    all_notes=Note_model.objects.filter(user_id=user.id)
    if  ( all_notes):
        return render(request, "notes/to_do.html", {'page': 'home', 'all_notes': all_notes})
    else:
        print ('nothing to show')
        message='nothing to show'
        return render(request, "notes/to_do.html", {'page': 'home','message':message})
    return render(request,"notes/to_do.html",{'page':'home'})

def logout(request):
    try:
        del request.session["username"]
    except:
        pass
    return redirect("/notes/login-page/")

def delete_notes(request,id):
    print (id)
    obj=Note_model.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect("/notes/to-do/")

def edit_notes(request,id):
    if request.method=='POST':
        notes=request.POST['notes']
        obj_notes=Note_model.objects.get(id=id)
        obj_notes.notes=notes
        obj_notes.save()
        return HttpResponseRedirect("/notes/to-do/")
    else:
        obj_notes=Note_model.objects.get(id=id)

        return render(request,"notes/edit_page.html",{'obj_notes':obj_notes})

