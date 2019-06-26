from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
   
   if request.method == "GET":
      return render(request, "quote/index.html")
   if request.method == "POST":
      errors = User.objects.basic_validator(request.POST)    
      if len(errors) > 0:
         for key, value in errors.items():
            
            messages.error(request, value)
         return redirect('/')
      else:   
         hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
         user = User.objects.create(    
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_password
         )
         request.session['user_id'] = user.id
         return redirect("/dashboard")
     
def process_login(request):
   errors = User.objects.login_validator(request.POST)
   if len(errors) > 0:
      for key, value in errors.items():
         
         messages.error(request, value)
      return redirect("/")
   else:  
      user = User.objects.filter(email=request.POST['email'])
      request.session['user_id'] = user[0].id
      return redirect("/dashboard")

def dashboard(request):
   if not "user_id" in request.session:
      return redirect("/")
   
   fav = Quote.objects.filter(liked_by=request.session['user_id'])
   un_fav = Quote.objects.exclude(liked_by=request.session['user_id'])
   user = User.objects.get(id=request.session['user_id'])
   context = {
      "user": user,
      "un_fav": un_fav,
      "fav": fav,
   }
   return render(request, "quote/dashboard.html", context)

def create_quote(request):
   if request.method == "POST":
      errors = User.objects.quote_validator(request.POST)
      if len(errors) > 0:
         for key, value in errors.items():
              
               messages.error(request, value)
         return redirect('/dashboard')
     
      else:
         user = User.objects.get(id=request.session['user_id'])
         added_quote = Quote.objects.create( 
               quoted_by = request.POST['quoted_by'],   
               message = request.POST['message'],      
               uploaded_by = user
         )
         added_quote.liked_by.add(user)
         added_quote.save()
         return redirect("/dashboard")

def add_favorites(request, id):
   if not "user_id" in request.session:
      return redirect("/")
   user = User.objects.get(id=request.session['user_id'])
   quote = Quote.objects.get(id=id)
   quote.liked_by.add(user)
   quote.save()
   
   return redirect("/dashboard")

def un_favorites(request, id):
   if not "user_id" in request.session:
      return redirect("/")
   user = User.objects.get(id=request.session['user_id'])
   quote = Quote.objects.get(id=id)
   quote.liked_by.remove(user)
   quote.save()
   
   return redirect("/dashboard")    

def quote(request, id):
   if not "user_id" in request.session:
      return redirect("/")
   user = User.objects.get(id=request.session['user_id'])
   uploaded_by = User.objects.get(id=id)
   quotes = Quote.objects.filter(uploaded_by=uploaded_by.id)
   context = {
      "quotes": Quote.objects.filter(uploaded_by=id),
      "uploaded_by": uploaded_by,
      "count": quotes.count(),
   }
   return render(request, "quote/quote.html", context)
   

def logout(request):
   request.session.clear()
   return redirect("/")