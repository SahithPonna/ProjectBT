from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
import re
@login_required(login_url='login')

def HomePage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        medical_info = request.POST.get('medical_info')

        # Do something with the user details, like storing in the database
        # For example, if you have a model for User:
        # from .models import User
        # user = User(username=username, email=email, age=age, medical_info=medical_info)
        # user.save()

        # You can redirect the user to another page or render a success message.
        #return render(request, 'success.html', {'username': username})
    
    # If it's a GET request or the form is not submitted, just render the page.
    return render(request, 'home.html')

def SignupPage(request):
    context = {}  # Create an empty dictionary to hold context data

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')   
        pass2 = request.POST.get('password2')

        # Check for empty fields
        if not uname or not email or not pass1 or not pass2:
            context['error'] = "Please fill in all fields."
        else:
            # Valid characters for username (alphanumeric and underscore)
            if not re.match(r'^\w+$', uname):
                context['error'] = "Invalid characters in the username."

            # Minimum length for username and password (modify the numbers as per your requirements)
            elif len(uname) < 4 or len(pass1) < 6:
                context['error'] = "Username must have at least 4 characters and password must have at least 6 characters."
            
            # Check if passwords match
            elif pass1 != pass2:
                context['error'] = "Your password and confirm password do not match!!"
            else:
                # Create the user and save it
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')

    return render(request, 'signup.html', context)

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        
        # Check for empty fields
        if not username or not email or not pass1:
            return HttpResponse("Please fill in all fields.")
        
        # Valid characters for username (alphanumeric and underscore)
        if not re.match(r'^\w+$', username):
            return HttpResponse("Invalid characters in the username.")
        
        # Minimum length for username and password (modify the numbers as per your requirements)
        if len(username) < 4 or len(pass1) < 6:
            return HttpResponse("Username must have at least 4 characters and password must have at least 6 characters.")
        
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')